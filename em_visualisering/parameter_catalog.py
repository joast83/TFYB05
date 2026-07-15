"""Metadata profiles shared by all exercise problems.

The original exercise modules intentionally remain concise and continue to declare
``(key, label, default_si)`` tuples.  This catalogue turns those declarations into
fully structured :class:`ParameterSpec` objects.  Exact per-problem overrides live
here, while conservative semantic rules cover repeated concepts such as radii,
relative material constants, angles and sample counts.
"""

from __future__ import annotations

from dataclasses import replace
import math
import re

from .parameters import ParameterSpec, normalize_parameter_specs

_DISPLAY_UNITS: dict[str, tuple[str, ...]] = {
    "m": ("pm", "nm", "µm", "mm", "cm", "m", "km"),
    "m²": ("µm²", "mm²", "cm²", "m²"),
    "kg": ("mg", "g", "kg"),
    "C": ("pC", "nC", "µC", "mC", "C"),
    "C/m": ("pC/m", "nC/m", "µC/m", "mC/m", "C/m"),
    "C/m²": ("pC/m²", "nC/m²", "µC/m²", "mC/m²", "C/m²"),
    "C/m³": ("pC/m³", "nC/m³", "µC/m³", "mC/m³", "C/m³"),
    "V": ("mV", "V", "kV", "MV"),
    "V/m": ("V/m", "kV/m", "MV/m", "GV/m"),
    "A": ("µA", "mA", "A", "kA"),
    "A/m": ("A/m", "kA/m", "MA/m"),
    "A/m²": ("A/m²", "kA/m²", "MA/m²"),
    "A·m²": ("µA·m²", "mA·m²", "A·m²", "kA·m²"),
    "A m²": ("µA m²", "mA m²", "A m²", "kA m²"),
    "T": ("µT", "mT", "T"),
    "F": ("pF", "nF", "µF", "mF", "F"),
    "Wb": ("µWb", "mWb", "Wb"),
    "Ω": ("mΩ", "Ω", "kΩ", "MΩ"),
    "Ω m": ("mΩ m", "Ω m", "kΩ m", "MΩ m"),
    "S/m": ("µS/m", "mS/m", "S/m", "kS/m"),
    "S·m": ("µS·m", "mS·m", "S·m"),
    "N": ("mN", "N", "kN"),
}

_COUNT_KEYS = {"grid_n", "samples", "nmax", "N", "N1", "N2"}
_COORDINATE_KEYS = {"z0", "zmin", "xmin"}
_RELATIVE_EPS_KEYS = {"eps_r", "eps1", "eps2"}
_RELATIVE_MU_KEYS = {"mu_r"}

# Exact semantic exceptions.  Values are passed directly to dataclasses.replace.
_OVERRIDES: dict[tuple[str, str], dict[str, object]] = {
    ("CircularArcOnAxis", "loop"): {
        "control": "select",
        "choices": (1.0, 2.0),
        "choice_labels": ("Kvartsbåge", "Hel slinga"),
        "integer": True,
        "help_text": "Välj om geometrin är en kvarts cirkelbåge eller en hel strömslinga.",
    },
    ("ChargedSpheresSmallAngle", "g"): {
        "control": "slider",
        "minimum_si": 0.0,
        "ui_minimum_si": 0.1,
        "ui_maximum_si": 20.0,
        "step_si": 0.01,
        "help_text": "Tyngdaccelerationen; 9,81 m/s² motsvarar jordytan.",
    },
    ("LoopDipoleApproximationError", "tol"): {
        "control": "log",
        "minimum_si": 1e-6,
        "maximum_si": 1.0,
        "ui_minimum_si": 1e-4,
        "ui_maximum_si": 0.2,
        "help_text": "Relativ feltolerans för när dipolapproximationen betraktas som giltig.",
    },
    ("DipoleDipoleTorque", "theta_deg"): {
        "control": "slider",
        "minimum_si": 0.0,
        "maximum_si": 180.0,
        "ui_minimum_si": 0.0,
        "ui_maximum_si": 180.0,
        "step_si": 1.0,
    },
    ("AntarcticIceFlux", "latitude_deg"): {
        "control": "slider",
        "minimum_si": 0.0,
        "maximum_si": 90.0,
        "ui_minimum_si": 0.0,
        "ui_maximum_si": 90.0,
        "step_si": 1.0,
    },
}


def _nice_step(span: float, *, integer: bool = False) -> float:
    if not math.isfinite(span) or span <= 0:
        return 1.0 if integer else 0.1
    raw = span / 100.0
    exponent = math.floor(math.log10(raw))
    fraction = raw / (10.0**exponent)
    nice_fraction = 1.0 if fraction <= 1 else 2.0 if fraction <= 2 else 5.0
    step = nice_fraction * 10.0**exponent
    if integer:
        return float(max(1, round(step)))
    return step


def _count_profile(spec: ParameterSpec) -> ParameterSpec:
    default = int(round(spec.default_si))
    text = spec.label.casefold()
    if spec.key == "grid_n" or "rutnät" in text:
        lower, upper, step = 31, max(201, default * 2 + 1), 2
    elif spec.key == "samples" or "punkter" in text:
        lower, upper, step = 20, max(1000, default * 2), 10
    elif spec.key == "nmax":
        lower, upper, step = 2, max(100, default * 3), 1
    else:
        lower, upper, step = 1, max(1000, default * 5), 1
    return replace(
        spec,
        integer=True,
        minimum_si=max(spec.minimum_si or 0.0, 1.0),
        ui_minimum_si=float(lower),
        ui_maximum_si=float(upper),
        step_si=float(step),
        control="slider",
        help_text=spec.help_text or "Diskret heltalsparameter.",
    )


def _material_profile(spec: ParameterSpec, *, magnetic: bool) -> ParameterSpec:
    if magnetic:
        return replace(
            spec,
            minimum_si=1e-12,
            ui_minimum_si=1.0,
            ui_maximum_si=max(1e5, spec.default_si * 100.0),
            control="log",
            help_text=spec.help_text
            or "Relativ permeabilitet. Logaritmisk kontroll används eftersom material kan skilja flera storleksordningar.",
        )
    return replace(
        spec,
        minimum_si=1e-12,
        ui_minimum_si=1.0,
        ui_maximum_si=max(20.0, spec.default_si * 3.0),
        step_si=0.1,
        control="slider",
        help_text=spec.help_text or "Relativ permittivitet för materialet.",
    )


def _is_length_like(spec: ParameterSpec) -> bool:
    return spec.si_unit == "m" and spec.key not in _COORDINATE_KEYS


def _is_positive_wide_range(spec: ParameterSpec) -> bool:
    if spec.default_si <= 0 or spec.minimum_si is None or spec.minimum_si < 0:
        return False
    text = spec.label.casefold()
    if any(word in text for word in ("radie", "längd", "avstånd", "höjd", "bredd", "tjocklek", "diameter")):
        return False
    return spec.si_unit in {
        "kg",
        "kg/m³",
        "m²",
        "F",
        "Ω",
        "Ω m",
        "S/m",
        "S·m",
        "s",
    } or any(
        word in text
        for word in (
            "densitet",
            "resistivitet",
            "konduktivitet",
            "kapacitans",
            "frekvens",
        )
    )


def enrich_parameter_spec(problem_class_name: str, spec: ParameterSpec) -> ParameterSpec:
    """Apply reusable and exact metadata to one normalized parameter."""

    display_units = spec.display_units or _DISPLAY_UNITS.get(spec.si_unit, ())
    enriched = replace(spec, display_units=display_units)

    exact = _OVERRIDES.get((problem_class_name, spec.key))
    if exact:
        return replace(enriched, **exact)

    if spec.key in _COUNT_KEYS and (
        spec.key != "N" or "varv" in spec.label.casefold() or "rutnät" in spec.label.casefold()
    ):
        return _count_profile(enriched)

    if spec.key in _RELATIVE_EPS_KEYS or "relativ permittivitet" in spec.label.casefold():
        return _material_profile(enriched, magnetic=False)
    if spec.key in _RELATIVE_MU_KEYS or "relativa permeabilitet" in spec.label.casefold():
        return _material_profile(enriched, magnetic=True)

    if spec.si_unit == "grad":
        return replace(
            enriched,
            control="slider",
            minimum_si=0.0,
            maximum_si=360.0,
            ui_minimum_si=0.0,
            ui_maximum_si=180.0,
            step_si=1.0,
        )

    if spec.key in _COORDINATE_KEYS or any(
        marker in spec.label.casefold() for marker in ("position", "z min", "xmin", "start för plott")
    ):
        return replace(
            enriched,
            control="number",
            help_text=enriched.help_text or "Signerad koordinat i den valda geometrin.",
        )

    if _is_length_like(enriched) and enriched.default_si > 0:
        lower = 0.0 if enriched.minimum_si == 0 else enriched.default_si * 0.05
        upper = max(enriched.default_si * 5.0, enriched.default_si + 1e-15)
        return replace(
            enriched,
            control="slider",
            ui_minimum_si=lower,
            ui_maximum_si=upper,
            step_si=_nice_step(upper - lower),
            help_text=enriched.help_text
            or "Geometrisk längd. Enhetsväljaren ändrar endast presentationen; beräkningen använder meter.",
        )

    if _is_positive_wide_range(enriched):
        lower = max(enriched.default_si * 1e-3, 1e-300)
        upper = enriched.default_si * 1e3
        return replace(
            enriched,
            control="log",
            ui_minimum_si=lower,
            ui_maximum_si=upper,
            help_text=enriched.help_text
            or "Positiv parameter med stort praktiskt variationsområde; kontrollen är logaritmisk.",
        )

    # Bounded non-negative quantities with comfortable magnitudes get a linear slider.
    if enriched.minimum_si == 0 and enriched.default_si > 0 and 1e-6 <= enriched.default_si <= 1e4:
        upper = enriched.default_si * 5.0
        return replace(
            enriched,
            control="slider",
            ui_minimum_si=0.0,
            ui_maximum_si=upper,
            step_si=_nice_step(upper),
        )

    return enriched


def parameter_specs_for_problem(problem_class_name: str, parameters) -> tuple[ParameterSpec, ...]:
    """Normalize and enrich all parameters for one exercise class."""

    return tuple(
        enrich_parameter_spec(problem_class_name, spec)
        for spec in normalize_parameter_specs(parameters)
    )
