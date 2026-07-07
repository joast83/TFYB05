"""Plotly bridge for the Streamlit version of the EM visualisation app.

The original application renders its right-hand 3-D panel with Matplotlib's
``Axes3D``. Streamlit can only display that as a static PNG via ``st.pyplot``.
This module provides a small Matplotlib-like adapter that accepts the 3-D draw
calls used by the problem classes and translates them into Plotly/WebGL traces.

It deliberately covers the API surface used by ``draw_3d(...)`` in this project:
surfaces, lines, scatter points, vector arrows, labels, limits and simple
Poly3DCollection boxes. The desktop Tkinter/Matplotlib app is left unchanged.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

import numpy as np
import plotly.graph_objects as go
from matplotlib import colors as mcolors


_PLOTLY_COLOR_SCALES = {
    "viridis": "Viridis",
    "plasma": "Plasma",
    "inferno": "Inferno",
    "magma": "Magma",
    "cividis": "Cividis",
    "blues": "Blues",
    "oranges": "Oranges",
    "rdbu": "RdBu",
    "rdbu_r": "RdBu",
    "coolwarm": "RdBu",
    "seismic": "RdBu",
}

_MPL_SHORT_COLORS = {
    "b": "blue",
    "g": "green",
    "r": "red",
    "c": "cyan",
    "m": "magenta",
    "y": "yellow",
    "k": "black",
    "w": "white",
}


class _TraceProxy:
    """Tiny proxy for Matplotlib return objects that are later labelled."""

    def __init__(self, trace: Any | None = None):
        self.trace = trace

    def set_label(self, label: str) -> None:
        if self.trace is not None:
            self.trace.name = str(label)
            self.trace.showlegend = True


@dataclass
class PlotlyFigureAdapter:
    """A Matplotlib-Figure-shaped object that records Plotly traces."""

    height: int = 620
    _figure: go.Figure = field(default_factory=go.Figure)
    _axes: list["PlotlyAxes3DAdapter"] = field(default_factory=list)

    def clear(self) -> None:
        self._figure = go.Figure()
        self._axes.clear()

    def add_subplot(self, *_args: Any, **_kwargs: Any) -> "PlotlyAxes3DAdapter":
        ax = PlotlyAxes3DAdapter(self)
        self._axes.append(ax)
        return ax

    def colorbar(self, *_args: Any, **_kwargs: Any) -> _TraceProxy:
        # Plotly surfaces manage their own color bars. Matplotlib colorbar calls
        # from the original code are therefore safe no-ops here. Return a proxy
        # because some problem classes call ``fig.colorbar(...).set_label(...)``.
        return _TraceProxy(None)

    def add_trace(self, trace: Any) -> None:
        self._figure.add_trace(trace)

    def to_plotly(self) -> go.Figure:
        fig = self._figure
        if self._axes:
            self._axes[0]._apply_layout(fig)
        fig.update_layout(
            height=self.height,
            margin=dict(l=0, r=0, t=44, b=0),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        )
        return fig


class PlotlyAxes3DAdapter:
    """Subset of Matplotlib Axes3D used by the problem ``draw_3d`` methods."""

    plotly_bridge = True

    def __init__(self, figure: PlotlyFigureAdapter):
        self._figure_adapter = figure
        self._title = ""
        self._xlabel = "x"
        self._ylabel = "y"
        self._zlabel = "z"
        self._xlim = None
        self._ylim = None
        self._zlim = None
        self._axis_off = False
        self._aspect = None
        self._camera_eye = None

    def get_figure(self) -> PlotlyFigureAdapter:
        return self._figure_adapter

    # ---- trace primitives -------------------------------------------------

    def plot_surface(self, X: Any, Y: Any, Z: Any, **kwargs: Any) -> _TraceProxy:
        x = _as_2d_float(X)
        y = _as_2d_float(Y)
        z = _as_2d_float(Z)
        surfacecolor = kwargs.get("surfacecolor")
        if surfacecolor is None and "facecolors" in kwargs:
            surfacecolor = _rgba_luminance(kwargs.get("facecolors"))
        if surfacecolor is None:
            surfacecolor = z
        else:
            surfacecolor = _as_2d_float(surfacecolor)

        colorscale = _plotly_colorscale(kwargs.get("colorscale") or kwargs.get("cmap"))
        opacity = float(kwargs.get("alpha", kwargs.get("opacity", 1.0)))
        showscale = bool(kwargs.get("showscale", True))
        trace_kwargs: dict[str, Any] = {
            "x": x,
            "y": y,
            "z": z,
            "surfacecolor": surfacecolor,
            "colorscale": colorscale,
            "opacity": opacity,
            "showscale": showscale,
            "hovertemplate": "x=%{x:.4g}<br>y=%{y:.4g}<br>z=%{z:.4g}<extra></extra>",
        }

        norm = kwargs.get("norm")
        if hasattr(norm, "vmin") and hasattr(norm, "vmax"):
            try:
                trace_kwargs["cmin"] = float(norm.vmin)
                trace_kwargs["cmax"] = float(norm.vmax)
            except Exception:
                pass
        for source, target in (("cmin", "cmin"), ("cmax", "cmax")):
            if source in kwargs:
                trace_kwargs[target] = kwargs[source]

        if "color" in kwargs and surfacecolor is z:
            color = _to_css_color(kwargs.get("color"))
            trace_kwargs["colorscale"] = [[0.0, color], [1.0, color]]
            trace_kwargs["surfacecolor"] = np.zeros_like(z, dtype=float)
            trace_kwargs["showscale"] = False

        trace = go.Surface(**trace_kwargs)
        self._figure_adapter.add_trace(trace)
        self._expand_limits(x, y, z)
        return _TraceProxy(trace)

    def plot(self, x: Any, y: Any, *args: Any, **kwargs: Any) -> list[_TraceProxy]:
        z = None
        style = None
        remaining = list(args)
        if remaining:
            if isinstance(remaining[0], str):
                style = remaining.pop(0)
            else:
                z = remaining.pop(0)
                if remaining and isinstance(remaining[0], str):
                    style = remaining.pop(0)
        if z is None:
            z = np.zeros_like(np.asarray(x, dtype=float))

        color = kwargs.get("color") or _color_from_style(style)
        width = kwargs.get("linewidth", kwargs.get("lw", 3))
        dash = _dash_from_style(style or kwargs.get("linestyle"))
        name = kwargs.get("label")

        xx, yy, zz = (_as_1d_float(v) for v in (x, y, z))
        trace = go.Scatter3d(
            x=xx,
            y=yy,
            z=zz,
            mode="lines",
            name=name if name and not str(name).startswith("_") else None,
            showlegend=bool(name and not str(name).startswith("_")),
            line=dict(color=_to_css_color(color) if color else None, width=float(width), dash=dash),
            hovertemplate="x=%{x:.4g}<br>y=%{y:.4g}<br>z=%{z:.4g}<extra></extra>",
        )
        self._figure_adapter.add_trace(trace)
        self._expand_limits(xx, yy, zz)
        return [_TraceProxy(trace)]

    def scatter(self, x: Any, y: Any, z: Any = None, **kwargs: Any) -> _TraceProxy:
        if z is None:
            z = np.zeros_like(np.asarray(x, dtype=float))
        xx, yy, zz = (_as_1d_float(v) for v in (x, y, z))
        size = kwargs.get("s", kwargs.get("size", 5))
        try:
            size = np.sqrt(float(np.asarray(size).ravel()[0]))
        except Exception:
            size = 5
        size = max(3, min(18, size))

        color = kwargs.get("color", kwargs.get("c", None))
        marker: dict[str, Any] = {"size": size}
        if color is not None:
            arr = np.asarray(color)
            if arr.size == xx.size and np.issubdtype(arr.dtype, np.number):
                marker.update(color=_as_1d_float(arr), colorscale="Viridis", showscale=False)
            else:
                marker["color"] = _to_css_color(color)

        trace = go.Scatter3d(
            x=xx,
            y=yy,
            z=zz,
            mode="markers",
            marker=marker,
            name=kwargs.get("label") or None,
            showlegend=bool(kwargs.get("label")),
            hovertemplate="x=%{x:.4g}<br>y=%{y:.4g}<br>z=%{z:.4g}<extra></extra>",
        )
        self._figure_adapter.add_trace(trace)
        self._expand_limits(xx, yy, zz)
        return _TraceProxy(trace)

    def quiver(self, X: Any, Y: Any, Z: Any, U: Any, V: Any, W: Any, **kwargs: Any) -> _TraceProxy:
        x, y, z, u, v, w = (_broadcast_flat(X, Y, Z, U, V, W))
        length = float(kwargs.get("length", 1.0))
        normalize = bool(kwargs.get("normalize", False))
        mag = np.sqrt(u * u + v * v + w * w)
        keep = np.isfinite(x) & np.isfinite(y) & np.isfinite(z) & np.isfinite(u) & np.isfinite(v) & np.isfinite(w) & (mag > 0)
        x, y, z, u, v, w, mag = (arr[keep] for arr in (x, y, z, u, v, w, mag))
        if x.size == 0:
            return _TraceProxy(None)
        if x.size > 450:
            step = int(np.ceil(x.size / 450))
            x, y, z, u, v, w, mag = (arr[::step] for arr in (x, y, z, u, v, w, mag))
        if normalize:
            u, v, w = u / mag * length, v / mag * length, w / mag * length
        else:
            u, v, w = u * length, v * length, w * length
        x2, y2, z2 = x + u, y + v, z + w

        color = _to_css_color(kwargs.get("color", "steelblue"))
        width = float(kwargs.get("linewidth", kwargs.get("lw", 3)))
        lines_x, lines_y, lines_z = [], [], []
        for a, b, c, d, e, f in zip(x, x2, y, y2, z, z2):
            lines_x.extend([a, b, None])
            lines_y.extend([c, d, None])
            lines_z.extend([e, f, None])
        line_trace = go.Scatter3d(
            x=lines_x,
            y=lines_y,
            z=lines_z,
            mode="lines",
            showlegend=False,
            line=dict(color=color, width=width),
            hoverinfo="skip",
        )
        self._figure_adapter.add_trace(line_trace)

        arrow_length_ratio = float(kwargs.get("arrow_length_ratio", 0.25))
        cone_scale = max(np.nanmax(np.sqrt(u * u + v * v + w * w)) * arrow_length_ratio, 1e-30)
        cone_trace = go.Cone(
            x=x2,
            y=y2,
            z=z2,
            u=u,
            v=v,
            w=w,
            anchor="tip",
            sizemode="absolute",
            sizeref=cone_scale,
            colorscale=[[0.0, color], [1.0, color]],
            showscale=False,
            hoverinfo="skip",
        )
        self._figure_adapter.add_trace(cone_trace)
        self._expand_limits(np.concatenate([x, x2]), np.concatenate([y, y2]), np.concatenate([z, z2]))
        return _TraceProxy(line_trace)

    def text(self, x: Any, y: Any, z: Any, s: Any, **kwargs: Any) -> _TraceProxy:
        trace = go.Scatter3d(
            x=[float(x)],
            y=[float(y)],
            z=[float(z)],
            text=[str(s)],
            mode="text",
            textposition="middle center",
            showlegend=False,
            hoverinfo="skip",
        )
        self._figure_adapter.add_trace(trace)
        self._expand_limits([x], [y], [z])
        return _TraceProxy(trace)

    def add_collection3d(self, collection: Any) -> _TraceProxy:
        # Supports the Poly3DCollection boxes produced by core._draw_box(...).
        vec = getattr(collection, "_vec", None)
        segslices = getattr(collection, "_segslices", None)
        if vec is None or segslices is None:
            return _TraceProxy(None)
        vec = np.asarray(vec, dtype=float)
        color = _collection_color(collection)
        opacity = float(getattr(collection, "_alpha", 0.5) or 0.5)
        for sl in segslices:
            pts = vec[:3, sl].T
            if pts.shape[0] < 3:
                continue
            i, j, k = [], [], []
            for idx in range(1, pts.shape[0] - 1):
                i.append(0)
                j.append(idx)
                k.append(idx + 1)
            trace = go.Mesh3d(
                x=pts[:, 0],
                y=pts[:, 1],
                z=pts[:, 2],
                i=i,
                j=j,
                k=k,
                color=color,
                opacity=opacity,
                showscale=False,
                hoverinfo="skip",
            )
            self._figure_adapter.add_trace(trace)
            self._expand_limits(pts[:, 0], pts[:, 1], pts[:, 2])
        return _TraceProxy(None)

    # ---- layout and labels -------------------------------------------------

    def set_title(self, title: str, *args: Any, **kwargs: Any) -> None:
        self._title = str(title)

    def set_xlabel(self, label: str, *args: Any, **kwargs: Any) -> None:
        self._xlabel = str(label)

    def set_ylabel(self, label: str, *args: Any, **kwargs: Any) -> None:
        self._ylabel = str(label)

    def set_zlabel(self, label: str, *args: Any, **kwargs: Any) -> None:
        self._zlabel = str(label)

    def set_xlim(self, *args: Any, **kwargs: Any) -> None:
        self._xlim = _range_from_args(args, kwargs)

    def set_ylim(self, *args: Any, **kwargs: Any) -> None:
        self._ylim = _range_from_args(args, kwargs)

    def set_zlim(self, *args: Any, **kwargs: Any) -> None:
        self._zlim = _range_from_args(args, kwargs)

    def set_axis_off(self) -> None:
        self._axis_off = True

    def legend(self, *args: Any, **kwargs: Any) -> None:
        return None

    def set_box_aspect(self, aspect: Iterable[float], *args: Any, **kwargs: Any) -> None:
        try:
            self._aspect = tuple(float(v) for v in aspect)
        except Exception:
            self._aspect = None

    def view_init(self, elev: float | None = None, azim: float | None = None, *args: Any, **kwargs: Any) -> None:
        # Approximate the Matplotlib view with a Plotly camera. Users can then
        # rotate freely in the browser.
        if elev is None or azim is None:
            return
        elev_rad = np.deg2rad(float(elev))
        azim_rad = np.deg2rad(float(azim))
        r = 1.8
        self._camera_eye = dict(
            x=r * np.cos(elev_rad) * np.cos(azim_rad),
            y=r * np.cos(elev_rad) * np.sin(azim_rad),
            z=r * np.sin(elev_rad),
        )

    # ---- internals ---------------------------------------------------------

    def _expand_limits(self, x: Any, y: Any, z: Any) -> None:
        def update(current: tuple[float, float] | None, values: Any):
            vals = np.asarray(values, dtype=float).ravel()
            vals = vals[np.isfinite(vals)]
            if vals.size == 0:
                return current
            lo, hi = float(np.min(vals)), float(np.max(vals))
            if current is None:
                return (lo, hi)
            return (min(current[0], lo), max(current[1], hi))

        self._xlim = update(self._xlim, x)
        self._ylim = update(self._ylim, y)
        self._zlim = update(self._zlim, z)

    def _apply_layout(self, fig: go.Figure) -> None:
        axis_visible = not self._axis_off
        scene = dict(
            xaxis=dict(title=self._xlabel, range=_padded_range(self._xlim), visible=axis_visible),
            yaxis=dict(title=self._ylabel, range=_padded_range(self._ylim), visible=axis_visible),
            zaxis=dict(title=self._zlabel, range=_padded_range(self._zlim), visible=axis_visible),
            aspectmode="cube" if self._aspect is None else "manual",
        )
        if self._aspect is not None:
            max_aspect = max(self._aspect) if self._aspect else 1.0
            if max_aspect > 0:
                scene["aspectratio"] = dict(
                    x=self._aspect[0] / max_aspect,
                    y=self._aspect[1] / max_aspect,
                    z=self._aspect[2] / max_aspect,
                )
        if self._camera_eye is not None:
            scene["camera"] = dict(eye=self._camera_eye)
        fig.update_layout(title=dict(text=self._title, x=0.02, xanchor="left"), scene=scene)


# ---- helper functions ------------------------------------------------------


def make_plotly_3d_figure(problem: Any, params: dict[str, Any], mode: str) -> go.Figure:
    """Render a problem's existing ``draw_3d`` method as an interactive Plotly figure."""

    adapter = PlotlyFigureAdapter()
    problem.draw_3d(adapter, params, mode)
    return adapter.to_plotly()


def _as_1d_float(values: Any) -> np.ndarray:
    arr = np.asarray(values, dtype=float)
    if arr.ndim == 0:
        arr = arr.reshape(1)
    return arr.ravel()


def _as_2d_float(values: Any) -> np.ndarray:
    arr = np.asarray(values, dtype=float)
    if arr.ndim == 0:
        arr = arr.reshape(1, 1)
    if arr.ndim == 1:
        arr = arr.reshape(1, -1)
    return arr


def _broadcast_flat(*values: Any) -> tuple[np.ndarray, ...]:
    arrays = [np.asarray(v, dtype=float) for v in values]
    arrays = np.broadcast_arrays(*arrays)
    return tuple(a.ravel() for a in arrays)


def _to_css_color(color: Any) -> str:
    if color is None:
        return "steelblue"
    if isinstance(color, str):
        return _MPL_SHORT_COLORS.get(color, color)
    arr = np.asarray(color)
    if arr.ndim > 1:
        arr = arr.reshape(-1, arr.shape[-1])[0]
    try:
        r, g, b, a = mcolors.to_rgba(arr)
        return f"rgba({int(r * 255)}, {int(g * 255)}, {int(b * 255)}, {a:.3g})"
    except Exception:
        return "steelblue"


def _plotly_colorscale(cmap: Any) -> str:
    if cmap is None:
        return "Viridis"
    name = getattr(cmap, "name", str(cmap))
    return _PLOTLY_COLOR_SCALES.get(name.lower(), name)


def _color_from_style(style: str | None) -> str | None:
    if not style:
        return None
    for char, color in _MPL_SHORT_COLORS.items():
        if char in style:
            return color
    return None


def _dash_from_style(style: str | None) -> str | None:
    if not style:
        return None
    if "--" in style:
        return "dash"
    if ":" in style:
        return "dot"
    if "-." in style:
        return "dashdot"
    return None


def _rgba_luminance(facecolors: Any) -> np.ndarray | None:
    try:
        rgba = np.asarray(facecolors, dtype=float)
        if rgba.shape[-1] < 3:
            return None
        return 0.299 * rgba[..., 0] + 0.587 * rgba[..., 1] + 0.114 * rgba[..., 2]
    except Exception:
        return None


def _collection_color(collection: Any) -> str:
    for attr in ("_facecolor3d", "_facecolors"):
        colors = getattr(collection, attr, None)
        if colors is not None:
            try:
                return _to_css_color(np.asarray(colors)[0])
            except Exception:
                pass
    return "rgba(160, 160, 160, 0.5)"


def _range_from_args(args: tuple[Any, ...], kwargs: dict[str, Any]) -> tuple[float, float] | None:
    if len(args) >= 2:
        return (float(args[0]), float(args[1]))
    if len(args) == 1:
        value = args[0]
        if isinstance(value, (list, tuple, np.ndarray)) and len(value) >= 2:
            return (float(value[0]), float(value[1]))
    left = kwargs.get("left", kwargs.get("xmin", None))
    right = kwargs.get("right", kwargs.get("xmax", None))
    if left is not None and right is not None:
        return (float(left), float(right))
    bottom = kwargs.get("bottom", kwargs.get("ymin", None))
    top = kwargs.get("top", kwargs.get("ymax", None))
    if bottom is not None and top is not None:
        return (float(bottom), float(top))
    return None


def _padded_range(value_range: tuple[float, float] | None) -> list[float] | None:
    if value_range is None:
        return None
    lo, hi = value_range
    if not np.isfinite(lo) or not np.isfinite(hi):
        return None
    if hi <= lo:
        pad = max(abs(lo) * 0.05, 1.0)
    else:
        pad = (hi - lo) * 0.04
    return [lo - pad, hi + pad]
