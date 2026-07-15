"""Structured metadata and validation for editable problem parameters.

Legacy problem definitions use three-tuples ``(key, label, default_si)``.  The
normalisation helpers in this module keep those definitions working while allowing
new problems to opt into explicit bounds, control types, help text and unit choices.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import re
from typing import Iterable, Literal, Mapping, Sequence

from .unit_scaling import split_label

ControlKind = Literal["number", "slider", "log"]
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
    "resistans",
    "resistance",
    "kapacitans",
    "capacitance",
    "induktans",
    "inductance",
    "frekvens",
    "frequency",
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

    ``label`` may retain the historical ``"Text [SI-unit]"`` form.  ``si_unit`` is
    filled automatically from the label when omitted, so legacy definitions and new
    explicit definitions can coexist during a gradual migration.
    """

    key: str
    label: str
    default_si: float
    si_unit: str = ""
    display_units: tuple[str, ...] = ()
    minimum_si: float | None = None
    maximum_si: float | None = None
    step_si: float | None = None
    control: ControlKind = "number"
    help_text: str = ""

    def __post_init__(self) -> None:
        if not self.si_unit:
            _text, inferred_unit = split_label(self.label)
            object.__setattr__(self, "si_unit", inferred_unit)
        if not self.key:
            raise ValueError("ParameterSpec.key får inte vara tom.")
        if self.control not in {"number", "slider", "log"}:
            raise ValueError(f"Okänd kontrolltyp: {self.control}")
        if self.minimum_si is not None and self.maximum_si is not None:
            if self.minimum_si > self.maximum_si:
                raise ValueError(
                    f"minimum_si är större än maximum_si för parametern {self.key}."
                )
        if self.step_si is not None and self.step_si <= 0:
            raise ValueError(f"step_si måste vara positiv för parametern {self.key}.")
        if self.control == "log" and self.minimum_si is not None and self.minimum_si <= 0:
            raise ValueError(f"Logaritmisk parameter {self.key} måste ha positiv minimum_si.")

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
        minimum = _inferred_minimum(label, unit)
        control: ControlKind = "number"
        if minimum is not None and minimum > 0 and default > 0:
            if abs(default) < 1e-4 or abs(default) >= 1e4:
                control = "log"
        return cls(
            key=str(key),
            label=label,
            default_si=default,
            si_unit=unit,
            minimum_si=minimum,
            control=control,
        )

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

        unit_suffix = f" {self.si_unit}" if self.si_unit else ""
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

        default = float(self.default_si)
        if default != 0 and number != 0 and math.copysign(1.0, number) == math.copysign(1.0, default):
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
    """Infer only conservative non-negativity constraints for legacy parameters."""

    text, _unit = split_label(label)
    normalized = re.sub(r"\s+", " ", text.casefold())
    if any(word in normalized for word in _POSITIVE_LABEL_WORDS):
        return 0.0
    if unit in {"kg", "m²", "m³", "Hz", "Ω", "F", "H", "S/m"}:
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
