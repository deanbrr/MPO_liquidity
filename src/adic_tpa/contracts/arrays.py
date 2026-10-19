"""Array contracts (BUILD_SPEC v1.1 §1.5, §3, §3.17, §4.1).

Array containers are ``@dataclass(frozen=True, slots=True)`` (a few are mutable: ``ActionSlice``,
``UnitFinancing``, ``LedgerState``) subclasses of :class:`ArrayContainer`. They hold numpy arrays plus Pydantic
metadata; :meth:`ArrayContainer.validate` checks every declared field against ``ARRAY_SPECS[class name]``:
type, dtype, rank, shape symbols bound consistently across fields (``P``, ``U``, ``G``, ...; integer literals;
``SYM+1``), C-contiguity, finiteness of float arrays (NaN is illegal in engine arrays, brief P5), and the named
invariants of the §3.17 table. Cross-field invariants live in each container's ``_check_invariants`` hook.

Axis order is always [path, time, entity, type] (§1.5). Containers own their arrays: a frozen container stores
read-only views of the arrays it is given (also inside dict-of-array fields), so no code holding the container can
change an array in place under an unchanged checksum. The views share memory and the caller's own arrays keep their
flags, so a producer hands its arrays over and stops writing to them (copy first if it must keep a scratch buffer).
Pickling and copying rebuild a container through its constructor, so copies are frozen the same way. SciPy sparse
matrices (``LPModel.A``) are held as given.

``FlowSlice.intra`` nets to zero over groups within ``max(1e-9 × max(1, Σ_g|x|), 8 × eps_f32 × Σ_g|x|)``: §3.17
writes "1e-9 × scale" for float32 storage, where rounding alone leaves residuals near 6e-8 of the gross flow, so a
three-party bill (one client pays two, say) would otherwise fail. The float64 rule is unchanged.
"""

from __future__ import annotations

import hashlib
import json
import typing
from collections.abc import Callable, Mapping
from dataclasses import dataclass, fields
from pathlib import Path
from types import MappingProxyType, UnionType
from typing import Any, ClassVar, Final, Literal, Self

import numpy as np
import numpy.typing as npt
from pydantic import BaseModel, TypeAdapter

from adic_tpa.contracts.enums import (
    CFPStage, CreditState, ExitWindow, FinWindow, FLOW_SIGNS, HFLotState, MacroRegime, RowRole, SaleReason,
    ShockType, StressState,
)
from adic_tpa.contracts.errors import HashMismatch, SchemaError
from adic_tpa.contracts.hashing import array_checksum, content_hash

__all__ = [
    "F16", "F32", "F64", "I8", "I16", "I32", "U32", "U64", "B", "ArraySpec", "ArrayContainer", "ARRAY_SPECS",
    "INVARIANTS", "validate_container", "MAX_BLOCK_PATHS",
]

# §1.5: path simulations run in blocks of 2,000 paths; no array holds more than one block of unit-level data.
MAX_BLOCK_PATHS: Final = 2000
# float32 netting slack in units of machine epsilon times the gross flow (module docstring; review R03).
_F32_NETTING_EPS: Final = 8

F16 = npt.NDArray[np.float16]
F32 = npt.NDArray[np.float32]
F64 = npt.NDArray[np.float64]
I8 = npt.NDArray[np.int8]
I16 = npt.NDArray[np.int16]
I32 = npt.NDArray[np.int32]
U32 = npt.NDArray[np.uint32]
U64 = npt.NDArray[np.uint64]
B = npt.NDArray[np.bool_]


@dataclass(frozen=True, slots=True)
class ArraySpec:
    """Declared contract of one container field (§3.17).

    ``shape_symbols``: one entry per axis — a symbol (``"P"``), an integer literal (``"18"``) or ``"SYM+k"``.
    ``dtype``: numpy dtype code (``f2 f4 f8 i1 i2 i4 u4 u8 b1``); ignored for ``tuple`` and ``container`` kinds.
    ``kind``: ``array`` (ndarray), ``mapping`` (dict of ndarrays, each checked against the spec; a symbol
    written ``~X`` is bound per entry, every other symbol is shared with the container), ``tuple`` (a Python
    tuple whose length binds ``shape_symbols[0]``), ``container`` (a nested ArrayContainer, validated
    recursively), ``sparse`` (a scipy sparse matrix).
    """

    shape_symbols: tuple[str, ...]
    dtype: str
    units: str
    invariants: tuple[str, ...] = ()
    optional: bool = False
    kind: Literal["array", "mapping", "tuple", "container", "sparse"] = "array"


def _require(cond: bool, where: str, what: str) -> None:
    if not cond:
        raise SchemaError(f"{where}: {what}")


def _float_view(arr: np.ndarray) -> np.ndarray:
    return arr.astype(np.float64, copy=False)


def _inv_range(lo: float, hi: float, *, lo_open: bool = False, hi_open: bool = False) -> Callable[[np.ndarray, str], None]:
    def check(arr: np.ndarray, where: str) -> None:
        if arr.size == 0:
            return
        x = _float_view(arr)
        ok_lo = bool((x > lo).all()) if lo_open else bool((x >= lo).all())
        ok_hi = bool((x < hi).all()) if hi_open else bool((x <= hi).all())
        lb, rb = ("(" if lo_open else "["), (")" if hi_open else "]")
        _require(ok_lo and ok_hi, where, f"values outside {lb}{lo}, {hi}{rb} (min {x.min()}, max {x.max()})")
    return check


def _inv_rows_sum_to_one(arr: np.ndarray, where: str) -> None:
    if arr.size == 0:
        return
    s = _float_view(arr).sum(axis=-1)
    _require(bool(np.all(np.abs(s - 1.0) <= 1e-5)), where, f"last axis must sum to 1 ± 1e-5 (worst {np.abs(s - 1).max()})")


def _inv_regime_codes(arr: np.ndarray, where: str) -> None:
    for col, enum in enumerate((MacroRegime, ExitWindow, ShockType)):
        v = arr[..., col]
        lo, hi = min(e.value for e in enum), max(e.value for e in enum)
        _require(bool(((v >= lo) & (v <= hi)).all()), where, f"column {col} outside {enum.__name__} codes")


def _inv_enum(enum: type[Any]) -> Callable[[np.ndarray, str], None]:
    codes = np.array(sorted(e.value for e in enum))

    def check(arr: np.ndarray, where: str) -> None:
        _require(bool(np.isin(arr, codes).all()), where, f"values outside {enum.__name__} codes")
    return check


def _inv_permutation_rows(arr: np.ndarray, where: str) -> None:
    if arr.size == 0:
        return
    n = arr.shape[-1]
    srt = np.sort(arr.astype(np.int64), axis=-1)
    _require(bool((srt == np.arange(n)).all()), where, f"each row must be a permutation of 0..{n - 1}")


def _inv_csr_pointers(arr: np.ndarray, where: str) -> None:
    _require(arr.size >= 1 and int(arr[0]) == 0, where, "CSR pointers must start at 0")
    _require(bool((np.diff(arr.astype(np.int64)) >= 0).all()), where, "CSR pointers must be non-decreasing")


def _inv_flow_signs(arr: np.ndarray, where: str) -> None:
    signs = np.asarray(FLOW_SIGNS, dtype=np.int8)
    _require(arr.shape[-1] == signs.size, where, f"last axis must have {signs.size} flow types")
    x = _float_view(arr)
    pos = x[..., signs > 0]
    neg = x[..., signs < 0]
    _require(bool((pos >= -1e-12).all()), where, "a positive-sign FlowType carries a negative value (§1.4)")
    _require(bool((neg <= 1e-12).all()), where, "a negative-sign FlowType carries a positive value (§1.4)")


def _inv_sum_axis1_zero(arr: np.ndarray, where: str) -> None:
    if arr.size == 0:
        return
    x = _float_view(arr)
    gross = np.abs(x).sum(axis=1)
    tol = 1e-9 * np.maximum(1.0, gross)
    if arr.dtype == np.float32:
        tol = np.maximum(tol, _F32_NETTING_EPS * float(np.finfo(np.float32).eps) * gross)
    residual = np.abs(x.sum(axis=1))
    _require(bool((residual <= tol).all()), where,
             f"intra-ADIC flows must sum to 0 over groups (worst residual {residual.max()})")


def _inv_abs_le_1e4(arr: np.ndarray, where: str) -> None:
    if arr.size:
        _require(bool((np.abs(_float_view(arr)) <= 1e4).all()), where, "|coefficient| must be ≤ 1e4")


def _inv_binary(arr: np.ndarray, where: str) -> None:
    _require(bool(np.isin(arr, (0, 1)).all()), where, "values must be 0 or 1")


INVARIANTS: Final[Mapping[str, Callable[[np.ndarray, str], None]]] = MappingProxyType({
    "unit_interval": _inv_range(0.0, 1.0),
    "half_open_unit": _inv_range(0.0, 1.0, hi_open=True),
    "nonnegative": _inv_range(0.0, np.inf),
    "positive": _inv_range(0.0, np.inf, lo_open=True),
    "bid_range": _inv_range(0.0, 1.2, lo_open=True),
    "rows_sum_to_one": _inv_rows_sum_to_one,
    "regime_codes": _inv_regime_codes,
    "permutation_rows": _inv_permutation_rows,
    "csr_pointers": _inv_csr_pointers,
    "flow_signs": _inv_flow_signs,
    "sum_axis1_zero": _inv_sum_axis1_zero,
    "abs_le_1e4": _inv_abs_le_1e4,
    "binary": _inv_binary,
    "month_range": _inv_range(-1.0, 119.0),
    "survival_range": _inv_range(0.0, 25.0),
    "draw_band": _inv_range(0.05, 0.10),
    "ge_minus_one": _inv_range(-1.0, np.inf),
    "enum:CFPStage": _inv_enum(CFPStage),
    "enum:FinWindow": _inv_enum(FinWindow),
    "enum:SaleReason": _inv_enum(SaleReason),
    "enum:StressState": _inv_enum(StressState),
    "enum:MacroRegime": _inv_enum(MacroRegime),
    "enum:RowRole": _inv_enum(RowRole),
    "enum:HFLotState": _inv_enum(HFLotState),
    "enum:CreditState": _inv_enum(CreditState),
    "tier_amber_red": _inv_range(1.0, 2.0),
    # "allow_inf" is a marker: float arrays may hold ±inf (never NaN); handled in _check_array.
})

_FLOAT_KINDS: Final = frozenset("f")


def _bind(sym: str, size: int, bindings: dict[str, int], where: str) -> None:
    if sym.isdigit():
        _require(size == int(sym), where, f"axis must have size {sym}, got {size}")
        return
    if "+" in sym:
        base, off = sym.split("+", 1)
        k = int(off)
        if base in bindings:
            _require(size == bindings[base] + k, where, f"axis {sym} must be {bindings[base] + k}, got {size}")
        else:
            bindings[base] = size - k
        return
    if sym in bindings:
        _require(size == bindings[sym], where, f"axis {sym} must be {bindings[sym]}, got {size}")
    else:
        bindings[sym] = size


def _check_array(arr: Any, spec: ArraySpec, bindings: dict[str, int], where: str) -> None:
    _require(isinstance(arr, np.ndarray), where, f"expected numpy.ndarray, got {type(arr).__name__}")
    _require(arr.dtype == np.dtype(spec.dtype), where, f"dtype must be {np.dtype(spec.dtype)}, got {arr.dtype}")
    _require(arr.ndim == len(spec.shape_symbols), where,
             f"rank must be {len(spec.shape_symbols)} {list(spec.shape_symbols)}, got shape {arr.shape}")
    local: dict[str, int] = {}  # "~X" symbols: bound per array (per mapping entry)
    for axis, (sym, size) in enumerate(zip(spec.shape_symbols, arr.shape, strict=True)):
        if sym.startswith("~"):
            _bind(sym[1:], size, local, f"{where} axis {axis}")
        else:
            _bind(sym, size, bindings, f"{where} axis {axis}")
    _require(arr.flags.c_contiguous, where, "array must be C-contiguous")
    if arr.dtype.kind in _FLOAT_KINDS and arr.size:
        if "allow_inf" in spec.invariants:
            _require(not bool(np.isnan(arr).any()), where, "NaN is illegal (brief P5)")
        else:
            _require(bool(np.isfinite(arr).all()), where, "non-finite values are illegal (brief P5)")
    for name in spec.invariants:
        if name == "allow_inf":
            continue
        check = INVARIANTS.get(name)
        if check is None:
            raise SchemaError(f"{where}: unknown invariant {name!r} in ARRAY_SPECS")
        check(arr, where)


def _check_sparse(mat: Any, spec: ArraySpec, bindings: dict[str, int], where: str) -> None:
    _require(hasattr(mat, "tocsc") and hasattr(mat, "data") and getattr(mat, "ndim", 0) == 2, where,
             f"expected a 2-d scipy sparse array, got {type(mat).__name__}")
    _require(mat.dtype == np.dtype(spec.dtype), where, f"dtype must be {np.dtype(spec.dtype)}, got {mat.dtype}")
    for axis, (sym, size) in enumerate(zip(spec.shape_symbols, mat.shape, strict=True)):
        _bind(sym, size, bindings, f"{where} axis {axis}")
    data = np.asarray(mat.data)
    if data.size:
        _require(bool(np.isfinite(data).all()), where, "non-finite coefficients are illegal")
    for name in spec.invariants:
        INVARIANTS[name](data, where)


def _check_field(owner: str, name: str, value: Any, spec: ArraySpec, bindings: dict[str, int]) -> None:
    where = f"{owner}.{name}"
    if value is None:
        _require(spec.optional, where, "is None but not optional")
        return
    if spec.kind == "tuple":
        _require(isinstance(value, tuple), where, f"expected tuple, got {type(value).__name__}")
        _bind(spec.shape_symbols[0], len(value), bindings, where)
    elif spec.kind == "container":
        _require(isinstance(value, ArrayContainer), where, f"expected an ArrayContainer, got {type(value).__name__}")
        value.validate()
    elif spec.kind == "mapping":
        _require(isinstance(value, Mapping), where, f"expected a mapping of arrays, got {type(value).__name__}")
        for key, arr in value.items():
            _check_array(arr, spec, bindings, f"{where}[{key!r}]")
    elif spec.kind == "sparse":
        _check_sparse(value, spec, bindings, where)
    else:
        _check_array(value, spec, bindings, where)


def _value_digest(value: Any) -> str:
    if value is None:
        return "none"
    if isinstance(value, np.ndarray):
        return array_checksum(value)
    if isinstance(value, ArrayContainer):
        return value.checksum()
    if hasattr(value, "tocsc") and hasattr(value, "indptr"):
        csc = value.tocsc()
        return array_checksum(np.asarray(csc.shape, dtype=np.int64), csc.data, csc.indices, csc.indptr)
    if isinstance(value, Mapping) and value and all(isinstance(v, np.ndarray) for v in value.values()):
        parts = sorted((content_hash(k), array_checksum(v)) for k, v in value.items())
        return content_hash(parts)
    return content_hash(value)


def _union_args(tp: Any) -> tuple[Any, ...]:
    origin = typing.get_origin(tp)
    if origin is typing.Union or isinstance(tp, UnionType):
        return typing.get_args(tp)
    return (tp,)


def _read_only(value: Any) -> Any:
    """A read-only view of an ndarray (a new dict of views for a dict holding ndarrays); anything else unchanged."""
    if isinstance(value, np.ndarray):
        if not value.flags.writeable:
            return value
        view = value.view()
        view.flags.writeable = False
        return view
    if isinstance(value, dict) and any(isinstance(v, np.ndarray) for v in value.values()):
        return {k: _read_only(v) for k, v in value.items()}
    return value


def _rebuild_container(cls: type[ArrayContainer], kwargs: dict[str, Any]) -> ArrayContainer:
    return cls(**kwargs)


class ArrayContainer:
    """Base of every array container (§3, §4.1). Subclasses are slotted dataclasses.

    ``_CHECKSUM_EXCLUDE`` names fields left out of :meth:`checksum`; ``"field.sub"`` leaves out one field of a
    Pydantic ``field`` (e.g. ``ScenarioCube`` excludes ``meta.checksum``, which is derived from the arrays).
    """

    __slots__ = ()
    __tpa_array_container__: ClassVar[bool] = True
    _CHECKSUM_EXCLUDE: ClassVar[frozenset[str]] = frozenset()

    def __post_init__(self) -> None:
        if not type(self).__dataclass_params__.frozen:  # type: ignore[attr-defined]
            return  # ActionSlice, UnitFinancing and LedgerState are filled in place by design
        for f in fields(self):  # type: ignore[arg-type]
            value = getattr(self, f.name)
            frozen = _read_only(value)
            if frozen is not value:
                object.__setattr__(self, f.name, frozen)

    def __reduce__(self) -> tuple[Any, ...]:
        # through the constructor, so unpickled and copied containers hold read-only views again
        return (_rebuild_container, (type(self), {f.name: getattr(self, f.name) for f in fields(self)}))  # type: ignore[arg-type]

    # -- validation -------------------------------------------------------------------------------------
    def _bindings(self) -> dict[str, int]:
        """Symbols pre-bound from metadata (e.g. ``M`` from ``meta.months``); overridden by containers."""
        return {}

    def _check_invariants(self, bindings: Mapping[str, int]) -> None:
        """Cross-field invariants; overridden by containers."""

    def validate(self) -> None:
        """Check every field against ``ARRAY_SPECS[type(self).__name__]``; raise ``SchemaError``."""
        owner = type(self).__name__
        specs = ARRAY_SPECS.get(owner)
        if specs is None:
            raise SchemaError(f"{owner}: no ARRAY_SPECS entry")
        bindings = dict(self._bindings())
        for name, spec in specs.items():
            _check_field(owner, name, getattr(self, name), spec, bindings)
        self._check_invariants(bindings)

    # -- identity ---------------------------------------------------------------------------------------
    def checksum(self) -> str:
        """``sha256:`` over every field (arrays by ``array_checksum``, others by ``content_hash``), in field order,
        excluding ``_CHECKSUM_EXCLUDE``."""
        h = hashlib.sha256()
        for f in fields(self):  # type: ignore[arg-type]
            if f.name in self._CHECKSUM_EXCLUDE:
                continue
            value = getattr(self, f.name)
            sub = {s.split(".", 1)[1] for s in self._CHECKSUM_EXCLUDE if s.startswith(f.name + ".")}
            digest = (content_hash(value.model_dump(mode="python", exclude=sub)) if sub and isinstance(value, BaseModel)
                      else _value_digest(value))
            h.update(f.name.encode("utf-8") + b"=" + digest.encode("ascii") + b";")
        return "sha256:" + h.hexdigest()

    # -- persistence ------------------------------------------------------------------------------------
    def _flatten(self, prefix: str, arrays: dict[str, np.ndarray]) -> dict[str, Any]:
        hints = typing.get_type_hints(type(self))
        manifest: dict[str, Any] = {}
        for f in fields(self):  # type: ignore[arg-type]
            key = prefix + f.name
            value = getattr(self, f.name)
            if value is None:
                manifest[f.name] = {"kind": "none"}
            elif isinstance(value, np.ndarray):
                if value.dtype.hasobject:
                    raise SchemaError(f"{key}: object arrays cannot be persisted")
                arrays[key] = value
                manifest[f.name] = {"kind": "array"}
            elif isinstance(value, ArrayContainer):
                manifest[f.name] = {"kind": "container", "fields": value._flatten(key + "__", arrays)}
            elif hasattr(value, "tocsc") and hasattr(value, "indptr"):
                csc = value.tocsc()
                arrays[key + "__data"], arrays[key + "__indices"], arrays[key + "__indptr"] = csc.data, csc.indices, csc.indptr
                manifest[f.name] = {"kind": "sparse", "shape": list(csc.shape)}
            elif isinstance(value, Mapping) and all(isinstance(v, np.ndarray) for v in value.values()):
                # empty mappings land here too (a TypeAdapter cannot describe ndarray values); they reload as {}
                key_type = typing.get_args(hints[f.name])[0] if typing.get_args(hints[f.name]) else str
                keys = []
                for i, (k, v) in enumerate(value.items()):
                    arrays[f"{key}__{i}"] = v
                    keys.append(TypeAdapter(key_type).dump_python(k, mode="json"))
                manifest[f.name] = {"kind": "mapping", "keys": keys}
            else:
                adapter = TypeAdapter(hints[f.name])
                manifest[f.name] = {"kind": "json", "value": adapter.dump_python(value, mode="json")}
        return manifest

    @classmethod
    def _unflatten(cls, prefix: str, manifest: Mapping[str, Any], store: Any) -> Self:
        hints = typing.get_type_hints(cls)
        kwargs: dict[str, Any] = {}
        for f in fields(cls):  # type: ignore[arg-type]
            entry = manifest[f.name]
            key = prefix + f.name
            kind = entry["kind"]
            if kind == "none":
                kwargs[f.name] = None
            elif kind == "array":
                kwargs[f.name] = np.ascontiguousarray(store[key])
            elif kind == "container":
                sub = next(a for a in _union_args(hints[f.name]) if isinstance(a, type) and issubclass(a, ArrayContainer))
                kwargs[f.name] = sub._unflatten(key + "__", entry["fields"], store)
            elif kind == "sparse":
                from scipy import sparse  # lazy: only LPModel persists sparse data

                kwargs[f.name] = sparse.csc_array(
                    (store[key + "__data"], store[key + "__indices"], store[key + "__indptr"]), shape=tuple(entry["shape"]))
            elif kind == "mapping":
                key_type = typing.get_args(hints[f.name])[0]
                adapter = TypeAdapter(key_type)
                kwargs[f.name] = {adapter.validate_json(json.dumps(k)): np.ascontiguousarray(store[f"{key}__{i}"])
                                  for i, k in enumerate(entry["keys"])}
            else:
                kwargs[f.name] = TypeAdapter(hints[f.name]).validate_json(json.dumps(entry["value"]))
        return cls(**kwargs)

    def to_npz(self, path: Path) -> str:
        """Write every field to an uncompressed ``.npz`` (metadata as a JSON manifest); return the checksum."""
        arrays: dict[str, np.ndarray] = {}
        manifest = {"class": type(self).__name__, "fields": self._flatten("", arrays)}
        arrays["__manifest__"] = np.frombuffer(json.dumps(manifest, sort_keys=True).encode("utf-8"), dtype=np.uint8)
        with open(Path(path), "wb") as fh:
            np.savez(fh, **arrays)
        return self.checksum()

    @classmethod
    def from_npz(cls, path: Path, expected_checksum: str | None = None) -> Self:
        """Load a container written by :meth:`to_npz`; raise ``HashMismatch`` if ``expected_checksum`` differs."""
        with np.load(Path(path), allow_pickle=False) as store:
            manifest = json.loads(bytes(store["__manifest__"]).decode("utf-8"))
            if manifest.get("class") != cls.__name__:
                raise SchemaError(f"{path}: holds a {manifest.get('class')}, not a {cls.__name__}")
            obj = cls._unflatten("", manifest["fields"], store)
        if expected_checksum is not None and obj.checksum() != expected_checksum:
            raise HashMismatch(f"{path}: checksum {obj.checksum()} != expected {expected_checksum}",
                               {"path": str(path), "expected": expected_checksum})
        return obj


def validate_container(obj: ArrayContainer) -> None:
    """Functional alias of ``obj.validate()``."""
    obj.validate()


def _a(shape: str, dtype: str, units: str, *invariants: str, optional: bool = False) -> ArraySpec:
    return ArraySpec(tuple(shape.split()), dtype, units, tuple(invariants), optional, "array")


def _t(symbol: str, units: str = "ids") -> ArraySpec:
    return ArraySpec((symbol,), "tuple", units, kind="tuple")


def _m(shape: str, dtype: str, units: str, *invariants: str) -> ArraySpec:
    return ArraySpec(tuple(shape.split()), dtype, units, tuple(invariants), False, "mapping")


def _c(*, optional: bool = False) -> ArraySpec:
    return ArraySpec((), "container", "nested container", (), optional, "container")


_GR4 = "P Q Gp Ab"
_NC3 = "N Gp Ab"

# §3.17 table, extended to every container of §3 (one entry per container class name).
ARRAY_SPECS: Final[Mapping[str, Mapping[str, ArraySpec]]] = MappingProxyType({
    "UnitIndex": MappingProxyType({
        "unit_ids": _t("U"), "group_of": _a("U", "i4", "taxonomy index", "nonnegative"),
        "engine_of": _t("U", "engine ids"),
        "age_bucket": _a("U", "i1", "age bucket index (-1: no age concept)", "ge_minus_one"),
        "red_tier": _a("U", "b1", "flag"),
    }),
    "OverlayGreeks": MappingProxyType({
        "delta": _a("3 K", "f8", "$bn per unit factor move"), "gamma_diag": _a("3 K", "f8", "$bn"),
        "vega": _a("3 J", "f8", "$bn per vol point"), "vanna": _a("3 J", "f8", "$bn"), "volga": _a("3 J", "f8", "$bn"),
        "theta": _a("3", "f8", "$bn per day"), "nv_eq": _a("S", "f8", "VIX-equivalent vega"),
        "pnl_stress": _a("3 S", "f8", "$bn"),
    }),
    "OverlayStressCoeffs": MappingProxyType({
        "stresses": _t("S"), "col_ids": _t("NC"),
        "nv_eq_tail": _a("S NC", "f8", "per unit column"), "nv_eq_ovl": _a("S NC", "f8", "per unit column"),
        "pnl_tail": _a("S NC", "f8", "$bn per unit column"), "pnl_opp": _a("S NC", "f8", "$bn per unit column"),
        "base_nv_eq_tail": _a("S", "f8", "VIX-equivalent vega"), "base_nv_eq_ovl": _a("S", "f8", "VIX-equivalent vega"),
        "base_pnl_tail": _a("S", "f8", "$bn"), "base_pnl_opp": _a("S", "f8", "$bn"),
    }),
    "ScenarioCube": MappingProxyType({
        "factors": _a("P M K", "f4", "per factor kind"),
        "regimes": _a("P M 3", "i1", "enum codes (S, e, Z)", "regime_codes"),
        "stress_post": _a("P M 3", "f4", "probability", "unit_interval", "rows_sum_to_one"),
        "vol": _a("P M V", "f4", "log vol index level"),
        "fin_window": _a("P M", "i1", "FinWindow", "enum:FinWindow"),
        "crowding_index": _a("P M", "f4", "index"),
        "asset_returns": _a("P M A", "f4", "monthly log return"),
        "brent": _a("P M", "f4", "USD/bbl", "positive"),
        "draw_rate": _a("P 11", "f4", "decimal a year", optional=True),       # Y = 11: FY2026–FY2036 (§1.3)
        "draw_override": _a("P 11", "b1", "flag", optional=True),
        "group_rates": _c(optional=True),
    }),
    "GroupRates": MappingProxyType({
        "delta": _a(_GR4, "f4", "per quarter", "unit_interval"),
        "qcall": _a(_GR4, "f4", "per quarter", "unit_interval"),
        "ret_simple": _a(_GR4, "f4", "simple return per quarter"),
        "bid": _a(_GR4, "f4", "fraction of economic NAV", "bid_range"),
        "income": _a(_GR4, "f4", "per quarter"),
        "u_per_nav": _a(_GR4, "f4", "ratio", "nonnegative"),
        "nav_share": _a(_GR4, "f4", "share", "unit_interval", "rows_sum_to_one"),
        "call_stress_12m": _a(_GR4, "f4", "per 12 months", "unit_interval"),
        "lo_ret": _a("P Q", "f4", "simple return per quarter"), "hf_ret": _a("P Q", "f4", "simple return per quarter"),
        "hf_phi": _a("P Q 4", "f4", "cash share", "unit_interval"),
        "vm_per_beta": _a("P Q", "f4", "$ per $ notional"), "cash_rate": _a("P Q", "f4", "per quarter"),
        "fac_rate": _a("P Q", "f4", "per quarter"), "ra_debt_rate": _a("P Q", "f4", "per quarter"),
        "ra_amort": _a("P Q", "f4", "per quarter"), "ra_direct_share": _a("P Q", "f4", "share", "unit_interval"),
        "tail_prem_rate": _a("P Q", "f4", "per quarter"), "tail_value": _a("P Q", "f4", "per unit notional"),
        "opp_pnl_rate": _a("P Q", "f4", "per quarter"), "delta_im_rate": _a("P Q", "f4", "per quarter"),
        "draw_rate_q": _a("P Q", "f4", "instalment ÷ B_y", "unit_interval"),
        "stress_class": _a("P Q", "i1", "StressState", "enum:StressState"),
        "obs": _a("P Q NOBS", "f4", "observable features"),
    }),
    "Tree": MappingProxyType({
        "parent": _a("N", "i4", "node index (-1 root)"), "t_end": _a("N", "i2", "quarter instant", "nonnegative"),
        "period_q": _a("N", "i1", "quarters"), "stage": _a("N", "i1", "stage index", "nonnegative"),
        "p": _a("N", "f8", "probability", "unit_interval"), "p_world": _a("N W", "f8", "probability", "unit_interval"),
        "is_leaf": _a("N", "b1", "flag"), "leaf_world": _a("N", "i1", "world index (-1 interior)"),
        "lr_weight": _a("N", "f8", "likelihood ratio", "positive"),
        "member_ptr": _a("N+1", "i4", "CSR pointers", "csr_pointers"),
        "member_idx": _a("NNZ", "i4", "pooled path index", "nonnegative"),
        "coef": _c(), "obs_centroid": _a("N NOBS", "f8", "observable features"),
        "regime_class": _a("N", "i1", "StressState", "enum:StressState"),
    }),
    "NodeCoefficients": MappingProxyType({
        **{name: _a(_NC3, "f8", "per period rate") for name in
           ("delta", "qcall", "ret_simple", "bid", "income", "u_per_nav", "nav_share", "call_stress_12m")},
        **{name: _a("N", "f8", "per period rate") for name in
           ("lo_ret", "hf_ret", "vm_per_beta", "cash_rate", "fac_rate", "draw_rate_q", "tau_lo", "h_im",
            "ra_debt_rate", "ra_amort", "ra_direct_share", "tail_prem_rate", "tail_value", "opp_pnl_rate",
            "delta_im_rate", "opex_rate")},
        "hf_phi": _a("N 4", "f8", "cash share", "unit_interval"),
        "fac_avail": _a("N NF", "f8", "availability multiplier", "unit_interval"),
        "amber_depth": _a("N GA", "f8", "depth fraction", "unit_interval"),
    }),
    "NoiseSlice": MappingProxyType({"u": _m("P ~NM ~NENT ~SLOTS", "f8", "uniform", "half_open_unit")}),
    "WorldSlice": MappingProxyType({
        "factors": _a("P NM K", "f4", "per factor kind"), "regimes": _a("P NM 3", "i1", "enum codes", "regime_codes"),
        "stress_post": _a("P NM 3", "f4", "probability", "unit_interval"), "vol": _a("P NM V", "f4", "log vol"),
        "fin_window": _a("P NM", "i1", "FinWindow", "enum:FinWindow"),
        "asset_returns": _a("P NM A", "f4", "monthly log return"), "brent": _a("P NM", "f4", "USD/bbl", "positive"),
    }),
    "ActionSlice": MappingProxyType({
        "sell_frac": _a("P U", "f4", "fraction", "unit_interval"),
        "sell_reason": _a("P U", "i1", "SaleReason", "enum:SaleReason"),
        "refi_draw_bn": _a("P U", "f4", "$bn", "nonnegative"), "add_bn": _a("P U", "f4", "$bn", "nonnegative"),
        "commit_bn": _a("P G", "f4", "$bn", "nonnegative"), "contingent_bn": _a("P G", "f4", "$bn", "nonnegative"),
        "hf_notice_frac": _a("P L", "f4", "fraction", "unit_interval"),
        "sma_runoff": _a("P", "f4", "rho", "unit_interval"),
        "p2s_bn": _a("P", "f4", "$bn"), "beta_add_bn": _a("P", "f4", "$bn"), "tail_notional_bn": _a("P", "f4", "$bn"),
        "opp_scale": _a("P", "f4", "multiplier", "nonnegative"), "monetize_frac": _a("P", "f4", "fraction", "unit_interval"),
        "fac_draw_bn": _a("P NF", "f4", "$bn", "nonnegative"), "fac_repay_bn": _a("P NF", "f4", "$bn", "nonnegative"),
        "reserve_target": _a("P", "f4", "HQLA* ÷ W", "nonnegative"),
        "recourse_order": _a("P 6", "i1", "rung permutation", "permutation_rows"),
        "preemptive_raise_bn": _a("P", "f4", "$bn", "nonnegative"),
    }),
    "FlowSlice": MappingProxyType({
        "by_group": _a("P G 18", "f4", "$bn per period, signed", "flow_signs"),
        "intra": _a("P G 18", "f4", "$bn per period, signed", "sum_axis1_zero"),
        "by_unit": _a("P UE 18", "f4", "$bn per period, signed", "flow_signs", optional=True),
        "recourse_unit_ids": _t("UR"),
        "by_recourse_unit": _a("P UR 18", "f4", "$bn per period, signed", "flow_signs"),
        "nav_econ": _a("P UE", "f4", "$bn", "nonnegative"), "nav_rep": _a("P UE", "f4", "$bn", "nonnegative"),
        "unfunded": _a("P UE", "f4", "$bn", "nonnegative"), "encumbered": _a("P UE", "f4", "$bn", "nonnegative"),
        "hqla_contrib_bn": _a("P", "f4", "$bn"),
    }),
    "UnitFinancing": MappingProxyType({
        "unit_ids": _t("UF"), "instrument_ids": _t("UF"),
        "balance_bn": _a("P UF", "f8", "$bn", "nonnegative"), "rate_q": _a("UF", "f8", "per quarter"),
        "amort_q": _a("UF", "f8", "per quarter", "unit_interval"), "ltv_covenant": _a("UF", "f8", "LTV", "nonnegative"),
        "breached": _a("P UF", "b1", "flag"),
    }),
    # column cubes hold Δ vs HOLD on CRN, so their values carry no FlowType sign rule
    "FlowCube": MappingProxyType({"values": _a("P Q U 18", "f4", "$bn per quarter, signed")}),
    "LedgerState": MappingProxyType({
        "hqla_unenc_bn": _a("P", "f8", "$bn"), "treasury_bn": _a("P 3", "f8", "$bn market value", "nonnegative"),
        "posted_im_bn": _a("P", "f8", "$bn", "nonnegative"), "vm_balance_bn": _a("P", "f8", "$bn"),
        "vm_in_transit_bn": _a("P", "f8", "$bn"),
        "fac_drawn_bn": _a("P NF", "f8", "$bn", "nonnegative"), "fac_limit_bn": _a("P NF", "f8", "$bn", "nonnegative"),
        "asset_debt_bn": _a("P", "f8", "$bn", "nonnegative"), "unit_debt_bn": _a("P", "f8", "$bn", "nonnegative"),
        "encumbrance_bn": _a("P", "f8", "$bn", "nonnegative"), "nav_econ_bn": _a("P", "f8", "$bn", "nonnegative"),
        "nav_rep_bn": _a("P", "f8", "$bn", "nonnegative"), "liquid_bn": _a("P", "f8", "$bn"),
        "nav_group_econ": _a("P G", "f8", "$bn", "nonnegative"), "nav_group_rep": _a("P G", "f8", "$bn", "nonnegative"),
        "unfunded_group": _a("P G", "f8", "$bn", "nonnegative"),
        "draw_basis_bn": _a("P", "f8", "$bn", "nonnegative"), "draw_rate": _a("P", "f8", "decimal a year"),
        "payout_ytd_bn": _a("P", "f8", "$bn", "nonnegative"),
        "twr_index": _a("P", "f8", "index", "positive"), "twr_peak": _a("P", "f8", "index", "positive"),
        "cushion": _a("P", "f8", "fraction of W"),
        "readiness": _a("P", "i1", "CFPStage", "enum:CFPStage"), "event": _a("P", "i1", "CFPStage", "enum:CFPStage"),
        "planning": _a("P", "i1", "CFPStage", "enum:CFPStage"), "playbook": _a("P", "i1", "CFPStage", "enum:CFPStage"),
        "event_hist": _a("P 2", "i1", "CFPStage", "enum:CFPStage"),
        "red_event": _a("P", "b1", "flag"), "payout_short": _a("P", "b1", "flag"), "failed": _a("P", "b1", "flag"),
        "red_month": _a("P", "i2", "month (-1 none)", "month_range"),
    }),
    "LedgerPaths": MappingProxyType({                                       # 121 monthly instants (§3.17)
        "row_keys": _t("R"), "rows": _a("P 121 R", "f4", "$bn slack"),
        "stages": _a("P 121 4", "i1", "CFPStage", "enum:CFPStage"),
    }),
    "StressReport": MappingProxyType({
        "headroom_bn": _a("P 24", "f8", "$bn"), "nco_bn": _a("P 24", "f8", "$bn"),
        "cbc_bn": _m("P 24", "f8", "$bn"), "survival_months": _m("P", "i2", "months (25 = > 24)", "survival_range"),
        "gap_bn": _a("P", "f8", "$bn"), "d0_bn": _a("P", "f8", "$bn", "nonnegative"),
    }),
    "RecourseAvailability": MappingProxyType({
        "unit_ids": _t("UR"), "group_of": _t("UR", "group ids"),
        "bid_frac": _a("P UR", "f4", "fraction of economic NAV", "bid_range"),
        "normal_bid_frac": _a("UR", "f4", "fraction of economic NAV", "bid_range"),
        "depth_frac": _a("P UR", "f4", "fraction", "unit_interval"),
        "lag_m": _a("P UR", "i1", "months", "nonnegative"),
        "tier": _a("UR", "i1", "1 amber, 2 red", "tier_amber_red"),
    }),
    "RecourseOutcome": MappingProxyType({
        "unit_ids": _t("UR"), "sold_frac": _a("P UR", "f4", "fraction", "unit_interval"),
        "month": _a("P UR", "i2", "month (-1 none)", "month_range"),
        "proceeds_bn": _a("P UR", "f8", "$bn", "nonnegative"), "red": _a("P UR", "b1", "flag"),
        "reason": _a("P UR", "i1", "SaleReason", "enum:SaleReason"),
    }),
    "BeliefSet": MappingProxyType({
        "unit_ids": _t("U"), "alpha_a": _a("U", "f8", "annual log excess return"), "benchmark_id": _t("U", "CMA classes"),
        "beta_hat": _a("U", "f8", "beta"), "bench_ref_a": _a("U", "f8", "annual log return"),
        "mu_total_a": _a("U", "f8", "annual log return"), "sigma_hat": _a("U", "f8", "annual", "nonnegative"),
        "band80": _a("U 2", "f8", "annual log return"), "mu_p10": _a("U", "f8", "annual log return"),
        "weights": _a("U 4", "f8", "fusion weight", "unit_interval"),
        "market_anchor": _a("U", "f8", "annual log return"), "has_market": _a("U", "b1", "flag"),
        "nowcast_nav_bn": _a("U", "f8", "$bn", "nonnegative"), "flags": _a("U", "u4", "bitmask"),
        "p_achieved": _a("U 2", "f8", "probability", "unit_interval"),
        "group_bias_mean": _a("G", "f8", "annual"), "group_bias_sd": _a("G", "f8", "annual", "nonnegative"),
        "kappa": _a("G", "f8", "ratio", "positive"), "info_value_usd_m": _a("G", "f8", "$m", optional=True),
    }),
    "BeliefDraws": MappingProxyType({
        "unit_ids": _t("U"), "gp_ids": _t("NGP"), "alpha0_q": _a("P U", "f4", "log return per quarter"),
        "group_bias_q": _a("P G", "f4", "log return per quarter"), "gp_effect_q": _a("P NGP", "f4", "log return per quarter"),
        "m_q": _a("U", "f8", "log return per quarter"), "phi": _a("U", "f8", "persistence"),
        "eta_sd_q": _a("U", "f8", "per quarter", "nonnegative"),
    }),
    "Observables": MappingProxyType({
        "values": _m("P", "f4", "registry units"), "unit_values": _m("P U", "f4", "registry units"),
        "group_values": _m("P G", "f4", "registry units"),
    }),
    "LPModel": MappingProxyType({
        "c": _a("NCOL", "f8", "W0 units", "abs_le_1e4"), "A": ArraySpec(("M", "NCOL"), "f8", "W0 units", ("abs_le_1e4",), kind="sparse"),
        "row_lo": _a("M", "f8", "W0 units", "allow_inf"), "row_hi": _a("M", "f8", "W0 units", "allow_inf"),
        "col_lo": _a("NCOL", "f8", "W0 units", "allow_inf"), "col_hi": _a("NCOL", "f8", "W0 units", "allow_inf"),
        "integrality": _a("NCOL", "i1", "0/1", "binary", optional=True),
        "row_keys": _t("M"), "col_keys": _t("NCOL"),
        "row_role": _a("M", "i1", "RowRole", "enum:RowRole"), "row_tier": _a("M", "i1", "Phase-I tier", "nonnegative"),
        "node_of_row": _a("M", "i4", "node index"), "node_of_col": _a("NCOL", "i4", "node index"),
    }),
    "DualSet": MappingProxyType({
        "pi_row": _a("M", "f8", "normalized shadow price"), "mu_cash": _a("N", "f8", "value of W0-unit cash"),
        "M_cash": _a("N", "f8", "dual mass"), "ell": _a("N", "f8", "per period"),
    }),
    "HSolution": MappingProxyType({"x": _a("NCOL", "f8", "W0 units"), "duals": _c()}),
    "LinearizedTier1": MappingProxyType({
        "row_keys": _t("MF"), "action_names": _t("NA"), "G": _a("MF NA", "f8", "row Jacobian"),
        "g0": _a("MF", "f8", "row value"), "delta": _a("MF", "f8", "amber buffer", "nonnegative"),
    }),
    "VarIndex": MappingProxyType({
        "state_names": _t("NS"), "decision_names": _t("ND"), "state_cols": _a("N NS", "i4", "column index"),
        "decision_cols": _a("N ND", "i4", "column index (-1 absent)"), "leaf_cols": _m("~L", "i4", "column index"),
    }),
    "RowBlock": MappingProxyType({
        "row_keys": _t("R"), "i": _a("NNZ", "i4", "row index", "nonnegative"),
        "j": _a("NNZ", "i4", "column index", "nonnegative"), "v": _a("NNZ", "f8", "coefficient", "abs_le_1e4"),
        "lo": _a("R", "f8", "W0 units", "allow_inf"), "hi": _a("R", "f8", "W0 units", "allow_inf"),
        "role": _a("R", "i1", "RowRole", "enum:RowRole"), "tier": _a("R", "i1", "Phase-I tier", "nonnegative"),
    }),
    "RowIndex": MappingProxyType({}),
    "PathMetrics": MappingProxyType({
        "quarterly": _a("P 41 KQ", "f4", "per series meta"), "terminal": _a("P KT", "f8", "per series meta"),
    }),
})
