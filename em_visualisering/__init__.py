"""Modulär version av EM-visualiseringsprogrammet."""

from .registry import PROBLEMS

__all__ = ["ElectrostaticsApp", "PROBLEMS"]

def __getattr__(name):
    if name == "ElectrostaticsApp":
        from .app import ElectrostaticsApp
        return ElectrostaticsApp
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
