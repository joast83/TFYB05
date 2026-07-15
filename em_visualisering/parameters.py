"""Structured metadata and validation for editable problem parameters.

All numerical physics calculations use SI values.  ``ParameterSpec`` describes how a
value should be validated and edited without coupling the problem classes to a
specific GUI toolkit.  Historical three-tuples remain supported and are enriched by
``parameter_catalog`` when a problem is loaded.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import re
from typing import Iterable, Literal, Mapping, Sequence

from .unit_scaling import split_label

ControlKind = Literal["number", "slider", "log", "select"]
Severity = Literal["error", "warning"]

_POSITIVE_LABEL_WORDS = (
    "radie",
    "radius",
    "längd",
    "length",
    "avstånd",
    "distance",
    "bredd",
    "width",
    "tjocklek",
    "thickness",
    "höjd",
    "height",
    "diameter",
    "massa",
    "mass",
    "area",
    "volym",
    "volume",
    "konduktivitet",
    "conductivity",
    "resistivitet",
    "resistivity",
    "resistans",
    "resistance",
    "kapacitans",
    "capacitance",
    "induktans",
    "inductance",
    "frekvens",
    "frequency",
    "densitet",
    "density",
    "antal",
    "varv",
)


@dataclass(frozen=True)
class ValidationIssue:
    """One user-facing validation result."""

    severity: Severity
    message: str
    key: str | None = None


@dataclass(frozen=True)
class ParameterSpec:
    """Metadata for one parameter stored internally in SI units.

    ``minimum_si`` and ``maximum_si`` are hard physical/model bounds.  The separate
    ``ui_minimum_si`` and ``ui_maximum_si`` fields only define a convenient editing
    range and therefore never reject a manually entered value.
    """

    key: str
    label: str
    default_si: float
    si_unit: str = ""
    display_units: tuple[str, ...] = ()
    minimum_si: float | None = None
    maximum_si: float | None = None
    ui_minimum_si: float | None = None
    ui_maximum_si: float | None = None
    step_si: float | None = None
    control: ControlKind = "number"
    help_text: str = ""
    integer: bool = False
    choices: tuple[float, ...] = ()
    choice_labels: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.si_unit:
            _text, inferred_unit = split_label(self.label)
            object.__setattr__(self, "si_unit", inferred_unit)
        object.__setattr__(self, "display_units", tuple(self.display_units))
        object.__setattr__(self, "choices", tuple(float(value) for value in self.choices))
        object.__setattr__(self, "choice_labels", tuple(self.choice_labels))

        if not self.key:
            raise ValueError("ParameterSpec.key får inte vara tom.")
        if self.control not in {"number", "slider", "log", "select"}:
            raise ValueError(f"Okänd kontrolltyp: {self.control}")
        self._validate_range("minimum_si", self.minimum_si, "maximum_si", self.maximum_si)
        self._validate_range(
            "ui_minimum_si", self.ui_minimum_si, "ui_maximum_si", self.ui_maximum_si
        )
        if self.step_si is not None and self.step_si <= 0:
            raise ValueError(f"step_si måste vara positiv för parametern {self.key}.")
        if self.control == "log":
            lower = self.ui_minimum_si if self.ui_minimum_si is not None else self.minimum_si
            if lower is not None and lower <= 0:
                raise ValueError(
                    f"Logaritmisk parameter {self.key} måste ha en positiv UI-minimigräns."
                )
            if self.default_si <= 0:
                raise ValueError(
                    f"Logaritmisk parameter {self.key} måste ha ett positivt standardvärde."
                )
        if self.control == "select" and not self.choices:
            raise ValueError(f"Select-parametern {self.key} saknar choices.")
        if self.choice_labels and len(self.choice_labels) != len(self.choices):
            raise ValueError(
                f"choice_labels och choices måste vara lika långa för {self.key}."
            )
        if self.choices and self.default_si not in self.choices:
            raise ValueError(
                f"Standardvärdet för {self.key} måste finnas bland choices."
            )
        if self.integer and not float(self.default_si).is_integer():
            raise ValueError(f"Standardvärdet för heltalsparametern {self.key} är inte heltal.")

    @staticmethod
    def _validate_range(
        lower_name: str,
        lower: float | None,
        upper_name: str,
        upper: float | None,
    ) -> None:
        if lower is not None and upper is not None and lower > upper:
            raise ValueError(f"{lower_name} är större än {upper_name}.")

    @classmethod
    def from_legacy(cls, parameter: Sequence[object]) -> "ParameterSpec":
        """Convert a historical ``(key, label, default_si)`` tuple."""

        if len(parameter) != 3:
            raise ValueError(
                "Legacy-parametrar måste ha formen (key, label, default_si)."
            )
        key, label, default_si = parameter
        label = str(label)
        _text, unit = split_label(label)
        default = float(default_si)
        return cls(
            key=str(key),
            label=label,
            default_si=default,
            si_unit=unit,
            minimum_si=_inferred_minimum(label, unit),
        )

    @property
    def choice_map(self) -> dict[str, float]:
        labels = self.choice_labels or tuple(f"{value:g}" for value in self.choices)
        return dict(zip(labels, self.choices))

    def validate(self, value: object) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        try:
            number = float(value)
        except (TypeError, ValueError):
            return [
                ValidationIssue(
                    "error", f"{self.label} måste vara ett tal.", key=self.key
                )
            ]

        if not math.isfinite(number):
            return [
                ValidationIssue(
                    "error", f"{self.label} måste vara ett ändligt tal.", key=self.key
                )
            ]

        unit_suffix = f" {self.si_unit}" if self.si_unit and self.si_unit != "-" else ""
        if self.minimum_si is not None and number < self.minimum_si:
            issues.append(
                ValidationIssue(
                    "error",
                    f"{self.label} får inte vara mindre än {self.minimum_si:g}{unit_suffix}.",
                    key=self.key,
                )
            )
        if self.maximum_si is not None and number > self.maximum_si:
            issues.append(
                ValidationIssue(
                    "error",
                    f"{self.label} får inte vara större än {self.maximum_si:g}{unit_suffix}.",
                    key=self.key,
                )
            )
        if self.control == "log" and number <= 0:
            issues.append(
                ValidationIssue(
                    "error",
                    f"{self.label} måste vara positiv för logaritmisk skala.",
                    key=self.key,
                )
            )
        if self.integer and not number.is_integer():
            issues.append(
                ValidationIssue(
                    "error", f"{self.label} måste vara ett heltal.", key=self.key
                )
            )
        if self.choices and number not in self.choices:
            allowed = ", ".join(f"{value:g}" for value in self.choices)
            issues.append(
                ValidationIssue(
                    "error",
                    f"{self.label} måste vara ett av följande värden: {allowed}.",
                    key=self.key,
                )
            )

        default = float(self.default_si)
        if (
            default != 0
            and number != 0
            and math.copysign(1.0, number) == math.copysign(1.0, default)
        ):
            ratio = abs(number / default)
            if ratio >= 1e12 or ratio <= 1e-12:
                issues.append(
                    ValidationIssue(
                        "warning",
                        f"{self.label} ligger mer än tolv storleksordningar från standardvärdet; "
                        "visualiseringen kan bli numeriskt svårtolkad.",
                        key=self.key,
                    )
                )
        return issues


def _inferred_minimum(label: str, unit: str) -> float | None:
    """Infer conservative non-negativity constraints for legacy parameters."""

    text, _unit = split_label(label)
    normalized = re.sub(r"\s+", " ", text.casefold())
    # Start/end coordinates and signed coefficients must remain free to be negative.
    signed_markers = ("min", "start", "koefficient", "laddning", "fält", "potential")
    if any(marker in normalized for marker in signed_markers):
        return None
    if any(word in normalized for word in _POSITIVE_LABEL_WORDS):
        return 0.0
    if unit in {"kg", "m²", "m³", "Hz", "Ω", "F", "H", "S/m", "s"}:
        return 0.0
    return None


def normalize_parameter_specs(
    parameters: Iterable[ParameterSpec | Sequence[object] | Mapping[str, object]],
) -> tuple[ParameterSpec, ...]:
    """Return immutable specs from mixed legacy and structured definitions."""

    specs: list[ParameterSpec] = []
    seen: set[str] = set()
    for parameter in parameters:
        if isinstance(parameter, ParameterSpec):
            spec = parameter
        elif isinstance(parameter, Mapping):
            spec = ParameterSpec(**parameter)
        else:
            spec = ParameterSpec.from_legacy(parameter)
        if spec.key in seen:
            raise ValueError(f"Dubblett av parameternyckeln {spec.key!r}.")
        seen.add(spec.key)
        specs.append(spec)
    return tuple(specs)


def validate_parameter_values(
    specs: Iterable[ParameterSpec], params: Mapping[str, object]
) -> list[ValidationIssue]:
    """Validate presence, finiteness and per-parameter bounds."""

    issues: list[ValidationIssue] = []
    for spec in specs:
        if spec.key not in params:
            issues.append(
                ValidationIssue(
                    "error", f"Parametern {spec.key!r} saknas.", key=spec.key
                )
            )
            continue
        issues.extend(spec.validate(params[spec.key]))
    return issues
