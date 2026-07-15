"""Unit-aware presentation of problem parameters.

Problem definitions keep their values in SI units so the numerical physics code remains
unchanged.  This module chooses a readable engineering unit for the user interface and
converts values back to SI before validation and calculation.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import re

_LABEL_UNIT_RE = re.compile(r"^(?P<text>.*?)(?:\s*\[(?P<unit>[^\]]+)\])\s*$")

# Prefix exponent means: one displayed unit equals 10**exponent SI units.
_ENGINEERING_PREFIXES = (
    ("a", -18),
    ("f", -15),
    ("p", -12),
    ("n", -9),
    ("µ", -6),
    ("m", -3),
    ("", 0),
    ("k", 3),
    ("M", 6),
    ("G", 9),
    ("T", 12),
)

# Length prefixes include centimetres because they are common in teaching problems.
_LENGTH_PREFIXES = (
    ("p", -12),
    ("n", -9),
    ("µ", -6),
    ("m", -3),
    ("c", -2),
    ("", 0),
    ("k", 3),
)

_PREFIXABLE_SYMBOLS = ("Wb", "Hz", "C", "V", "A", "F", "S", "T", "N", "Ω", "H", "J", "W")


@dataclass(frozen=True)
class DisplayScale:
    """Description of one UI parameter's display conversion."""

    original_label: str
    label: str
    si_unit: str
    display_unit: str
    factor: float

    def to_display(self, si_value: float) -> float:
        return float(si_value) / self.factor

    def to_si(self, display_value: float) -> float:
        return float(display_value) * self.factor


def split_label(label: str) -> tuple[str, str]:
    match = _LABEL_UNIT_RE.match(label)
    if not match:
        return label.strip(), ""
    return match.group("text").rstrip(), match.group("unit").strip()


def _length_unit_candidates(unit: str) -> list[tuple[str, float]]:
    """Return display-unit/factor candidates when the unit starts with metre.

    The exponent belongs to the metre symbol itself.  Thus m² -> cm² uses a factor
    of (10^-2)^2 = 10^-4, while C/m² is handled by the non-length path and prefixes C.
    """

    match = re.match(r"^m(?P<power>²|³|\^\s*[-+]?\d+)?(?P<rest>$|[/· ].*)", unit)
    if not match:
        return []

    power_token = match.group("power") or ""
    rest = match.group("rest") or ""
    if power_token == "²":
        power = 2
    elif power_token == "³":
        power = 3
    elif power_token.startswith("^"):
        try:
            power = int(power_token[1:].strip())
        except ValueError:
            return []
    else:
        power = 1

    # Do not invent unusual inverse-length prefixes.
    if power <= 0:
        return []

    return [
        (f"{prefix}m{power_token}{rest}", 10.0 ** (exponent * power))
        for prefix, exponent in _LENGTH_PREFIXES
    ]



def _mass_unit_candidates(unit: str) -> list[tuple[str, float]]:
    """Readable mass units for parameters stored in kilograms."""

    if unit != "kg":
        return []
    return [
        ("µg", 1e-9),
        ("mg", 1e-6),
        ("g", 1e-3),
        ("kg", 1.0),
        ("t", 1e3),
    ]

def _general_unit_candidates(unit: str) -> list[tuple[str, float]]:
    for symbol in _PREFIXABLE_SYMBOLS:
        if unit == symbol or unit.startswith(symbol + "/") or unit.startswith(symbol + "·") or unit.startswith(symbol + " "):
            rest = unit[len(symbol) :]
            return [
                (f"{prefix}{symbol}{rest}", 10.0**exponent)
                for prefix, exponent in _ENGINEERING_PREFIXES
            ]
    return []


def _candidate_score(display_value: float, factor: float) -> tuple[float, float, float]:
    """Rank candidates toward readable values while mildly preferring SI."""

    magnitude = abs(display_value)
    if magnitude == 0 or not math.isfinite(magnitude):
        return (0.0 if factor == 1.0 else 10.0, 0.0, abs(math.log10(factor)) if factor > 0 else 99.0)

    # Best range for editable numeric controls; a secondary range avoids awkward
    # jumps such as 0.9 m -> 900 mm unless the base value is genuinely tiny/large.
    if 1.0 <= magnitude < 1000.0:
        range_penalty = 0.0
    elif 0.1 <= magnitude < 10000.0:
        range_penalty = 1.0
    else:
        logmag = math.log10(magnitude)
        range_penalty = 2.0 + min(abs(logmag), abs(logmag - 3.0))

    # Aim near 10 without forcing a prefix when the SI value is already comfortable.
    target_penalty = abs(math.log10(magnitude) - 1.0)
    prefix_penalty = 0.12 if factor != 1.0 else 0.0
    return (range_penalty + prefix_penalty, target_penalty, abs(math.log10(factor)))



def display_scales_for(label: str) -> tuple[DisplayScale, ...]:
    """Return all supported display scales for a label, including the SI scale.

    The result is useful for interfaces that expose an explicit unit selector.  It is
    deliberately independent of the current value so changing a parameter does not
    silently change its unit.
    """

    text, unit = split_label(label)
    base = DisplayScale(label, label, unit, unit, 1.0)
    if not unit or unit == "-":
        return (base,)

    candidates = (
        _mass_unit_candidates(unit)
        or _length_unit_candidates(unit)
        or _general_unit_candidates(unit)
    )
    if not candidates:
        return (base,)

    scales = [
        DisplayScale(
            original_label=label,
            label=f"{text} [{display_unit}]",
            si_unit=unit,
            display_unit=display_unit,
            factor=factor,
        )
        for display_unit, factor in candidates
    ]
    if not any(scale.factor == 1.0 for scale in scales):
        scales.append(base)
    return tuple(sorted(scales, key=lambda scale: scale.factor))


def display_scale_by_unit(label: str, display_unit: str) -> DisplayScale:
    """Return the conversion for one explicitly requested display unit.

    Raises ``ValueError`` when the unit is not a valid presentation of the SI unit in
    ``label``.  This catches metadata typos during tests instead of silently applying
    an incorrect factor.
    """

    for scale in display_scales_for(label):
        if scale.display_unit == display_unit:
            return scale
    _text, si_unit = split_label(label)
    raise ValueError(
        f"Visningsenheten {display_unit!r} stöds inte för SI-enheten {si_unit!r}."
    )


def selectable_display_scales(
    label: str,
    default_value: float,
    display_units: tuple[str, ...] = (),
    *,
    max_options: int = 5,
) -> tuple[DisplayScale, ...]:
    """Return a compact, stable set of scales for an explicit unit selector.

    Problem metadata may provide an ordered allow-list.  Otherwise the automatically
    selected engineering prefix, nearby prefixes and the SI unit are retained.  The
    result does not change as the user edits the value, preventing surprising unit
    jumps.
    """

    all_scales = display_scales_for(label)
    if len(all_scales) == 1:
        return all_scales

    by_unit = {scale.display_unit: scale for scale in all_scales}
    if display_units:
        selected = []
        for unit in display_units:
            if unit not in by_unit:
                _text, si_unit = split_label(label)
                raise ValueError(
                    f"Visningsenheten {unit!r} stöds inte för SI-enheten {si_unit!r}."
                )
            selected.append(by_unit[unit])
        return tuple(selected)

    preferred = display_scale_for(label, default_value)
    ordered = list(all_scales)
    preferred_index = ordered.index(next(scale for scale in ordered if scale.display_unit == preferred.display_unit))
    indices = {preferred_index}
    for distance in range(1, len(ordered)):
        indices.add(preferred_index - distance)
        indices.add(preferred_index + distance)
        indices = {index for index in indices if 0 <= index < len(ordered)}
        if len(indices) >= max_options:
            break

    # Keep the base SI scale when possible because it is the canonical stored unit.
    si_index = next((i for i, scale in enumerate(ordered) if scale.factor == 1.0), None)
    if si_index is not None:
        indices.add(si_index)
    compact = [ordered[index] for index in sorted(indices)]
    if len(compact) > max_options:
        compact.sort(
            key=lambda scale: (
                0 if scale.display_unit == preferred.display_unit else 1,
                0 if scale.factor == 1.0 else 1,
                abs(math.log10(scale.factor / preferred.factor)),
            )
        )
        compact = compact[:max_options]
        compact.sort(key=lambda scale: scale.factor)
    return tuple(compact)

def display_scale_for(label: str, default_value: float) -> DisplayScale:
    """Choose a readable display unit from a parameter label and SI default.

    Unsupported or dimensionless units are returned unchanged.  The conversion is
    purely presentational; ``factor`` always converts the displayed value back to SI.
    """

    text, unit = split_label(label)
    base = DisplayScale(label, label, unit, unit, 1.0)
    if not unit or unit == "-":
        return base

    try:
        value = float(default_value)
    except (TypeError, ValueError):
        return base
    if value == 0 or not math.isfinite(value):
        return base

    candidates = (
        _mass_unit_candidates(unit)
        or _length_unit_candidates(unit)
        or _general_unit_candidates(unit)
    )
    if not candidates:
        return base

    ranked = sorted(
        ((display_unit, factor, value / factor) for display_unit, factor in candidates),
        key=lambda item: _candidate_score(item[2], item[1]),
    )
    display_unit, factor, displayed = ranked[0]

    # If even the best available prefix remains extremely awkward, scientific SI
    # notation is clearer than a misleading giant prefixed value.
    if not (1e-6 <= abs(displayed) < 1e9):
        return base

    display_label = f"{text} [{display_unit}]"
    return DisplayScale(label, display_label, unit, display_unit, factor)


def format_display_value(value: float) -> str:
    """Compact, round-trippable text for Tkinter entry fields."""

    return f"{float(value):.12g}"


def suggested_step(display_value: float) -> float:
    """Return a practical number-input increment in displayed units."""

    magnitude = abs(float(display_value))
    if magnitude == 0 or not math.isfinite(magnitude):
        return 0.1
    exponent = math.floor(math.log10(magnitude))
    step = 10.0 ** (exponent - 1)
    # Keep simple decimal steps and avoid underflow in UI widgets.
    return max(step, 1e-15)
