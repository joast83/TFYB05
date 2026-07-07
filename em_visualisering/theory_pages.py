from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable

import numpy as np
import plotly.graph_objects as go

from .core import EPS0


@dataclass(frozen=True)
class TheoryPage:
    key: str
    title: str
    short_description: str


THEORY_PAGES = [
    TheoryPage(
        key="gauss_flux",
        title="Gauss flödessats",
        short_description="Slutna ytor, elektriskt flöde och vad som faktiskt räknas som innesluten laddning.",
    ),
    TheoryPage(
        key="stokes_magnetostatics",
        title="Stokes sats i magnetostatik",
        short_description="Från Stokes matematiska sats till Ampères lag: cirkulation runt en sluten rand och ström genom ytan.",
    ),
]


THEORY_PAGE_LOOKUP = {page.title: page for page in THEORY_PAGES}


def render_theory_page(page: TheoryPage) -> None:
    """Render one theory page.

    Streamlit tabs execute all tab bodies eagerly, which made the previous version
    feel like several subpages were printed at once. These pages use a radio
    section selector and only build the selected body.
    """
    if page.key == "gauss_flux":
        _render_gauss_page()
    elif page.key == "stokes_magnetostatics":
        _render_stokes_page()
    else:
        import streamlit as st
        st.error("Okänd teorisida.")


# ---------------------------------------------------------------------------
# Gauss flux theorem
# ---------------------------------------------------------------------------


def _render_gauss_page() -> None:
    import streamlit as st

    st.title("Teori: Gauss flödessats")
    st.caption("Målet är att se när flödestanken fungerar, när den inte räcker, och varför ytan måste vara sluten.")

    section = st.radio(
        "Välj del",
        ["Intuition", "Testlabb", "Beräkningsrecept"],
        horizontal=True,
        key="gauss_section",
    )

    if section == "Intuition":
        st.latex(r"\oint_S \mathbf{E}\cdot d\mathbf{A} = \frac{Q_{\mathrm{innesluten}}}{\varepsilon_0}")
        c1, c2 = st.columns([1.1, 1.0])
        with c1:
            st.markdown(
                "### Kärnidé\n"
                "Tänk på den slutna ytan som en **osynlig kontrollvolym**. Varje liten ytdel frågar:\n\n"
                "**Går fältet ut genom mig eller in genom mig?**\n\n"
                "När alla ytdelar summeras försvinner bidrag från laddningar utanför ytan: fältlinjer som går in kommer också ut. "
                "Det enda som ger ett nettoöverskott är laddning som börjar eller slutar inuti ytan."
            )
        with c2:
            st.info(
                "**Det viktiga är inte formen på ytan.**\n\n"
                "En sfär, en deformerad ellipsoid och en kantig sluten yta ger samma totalflöde om de omsluter samma nettoladdning. "
                "Formen påverkar fördelningen av lokalt flöde, men inte totalsumman."
            )
            st.warning(
                "**Vanlig miss:**\n\n"
                "Gauss sats säger inte automatiskt att E är konstant på ytan. Det blir bara sant när symmetrin är stark nog."
            )
        st.markdown(
            "### Vad figuren i testlabbet ska visa\n"
            "- Färgen på ytan visar lokalt \\(\\mathbf{E}\\cdot\\hat{\\mathbf{n}}\\): rött = utåt, blått = inåt.\n"
            "- Totalen jämförs med \\(Q_{\\mathrm{innesluten}}/\\varepsilon_0\\).\n"
            "- Öppna ytor och laddningar på själva ytan markeras som fall där satsen inte kan användas direkt."
        )
        return

    if section == "Testlabb":
        st.markdown("### Flytta strömtuben från insidan till utsidan")
        c1, c2, c3 = st.columns(3)
        with c1:
            scenario = st.selectbox(
                "Scenario",
                [
                    "Stationär fri ström genom ytan",
                    "Inte magnetostatik: laddande kondensator",
                ],
                key="stokes_case",
            )
            current = st.slider("Fri ström I [A]", -5.0, 5.0, 2.0, 0.25, key="stokes_current")
        with c2:
            loop_radius = st.slider("Randradie R [m]", 0.8, 2.0, 1.2, 0.1, key="stokes_loop_radius")
            conductor_radius = st.slider("Strömtubens radie a [m]", 0.12, 0.55, 0.25, 0.01, key="stokes_conductor_radius")
        with c3:
            center_ratio = st.slider(
                "Strömtubens centrum x/R",
                -1.8,
                1.8,
                0.0,
                0.05,
                key="stokes_center_ratio",
                help="Flytta strömtuben tvärs över den valda ytan. |x/R| < 1 betyder att centrum ligger innanför randen.",
            )
            show_h_arrows = st.checkbox("Visa H-pilar längs randen", value=True, key="stokes_h_arrows")
            show_surface_current = st.checkbox("Visa J genom ytan", value=True, key="stokes_j_arrows")

        if scenario == "Inte magnetostatik: laddande kondensator":
            fig, report = _charging_capacitor_figure(current, loop_radius)
        else:
            fig, report = _stokes_magnetostatic_slider_figure(
                current=current,
                loop_radius=loop_radius,
                conductor_radius=conductor_radius,
                center_ratio=center_ratio,
                show_h_arrows=show_h_arrows,
                show_surface_current=show_surface_current,
            )
        st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False})

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Läge", report["case_label"])
        m2.metric("∮ H·dl", report["circulation_text"])
        m3.metric("Fri ström genom S", report["current_through_text"])
        m4.metric("Skillnad", report["difference_text"])

        if report["status"] == "ok":
            st.success(report["message"])
        elif report["status"] == "warning":
            st.warning(report["message"])
        else:
            st.error(report["message"])

        if scenario == "Stationär fri ström genom ytan":
            st.info(
                "Flytta **strömtubens centrum** med slidern. När tuben ligger helt innanför blir hela strömmen innesluten. "
                "När den flyttas mot randen får du ett **delvis genomskuret** fall. När den ligger helt utanför blir strömmen genom ytan noll."
            )

        st.markdown(
            "#### Läs figuren så här\n"
            "- Den gröna skivan är ytan S, och den mörka cirkeln är randen C.\n"
            "- Orange cylinder/pilar visar fri ström J_fri genom ytan.\n"
            "- Blå pilar längs randen visar H-fältets tangentbidrag till randintegralen.\n"
            "- Det som ska jämföras är **cirkulation runt randen** mot **fri ström genom ytan**."
        )
        return

    st.markdown(
        "### Beräkningsrecept för magnetostatik\n"
        "1. Välj en **sluten randkurva** \\(C\\).\n"
        "2. Välj en orienterad yta \\(S\\) vars rand är just \\(C\\).\n"
        "3. Använd högerhandsregeln för att koppla randriktning och normalriktning.\n"
        "4. Beräkna den fria stationära strömmen genom ytan: \\(I_{fri}=\\iint_S\\mathbf{J}_{fri}\\cdot\\hat{\\mathbf{n}}dS\\).\n"
        "5. Sätt \\(\\oint_C\\mathbf{H}\\cdot d\\mathbf{l}=I_{fri}\\). Om symmetrin gör \\(H\\) konstant längs randen kan du lösa ut \\(H\\)."
    )
    st.warning(
        "**När den magnetostatiska formen inte räcker:**\n\n"
        "- Kurvan är inte sluten.\n"
        "- Strömmen är inte stationär.\n"
        "- En vald yta går genom en idealiserad singularitet utan att du hanterar den som ett gränsfall.\n"
        "- Problemet innehåller tidsvarierande elektriska fält, till exempel en laddande kondensator. Då behövs Maxwell–Ampères lag."
    )


# ---------------------------------------------------------------------------
# Gauss helpers
# ---------------------------------------------------------------------------


def _gauss_figure(
    case: str,
    radius: float,
    q_inside_nc: float,
    q_outside_nc: float,
    offset_fraction: float,
    show_field_arrows: bool,
) -> tuple[go.Figure, dict[str, str]]:
    q_inside = q_inside_nc * 1e-9
    q_outside = q_outside_nc * 1e-9

    if case == "Sluten yta: laddning innanför":
        charges = [(q_inside, np.array([offset_fraction * radius, 0.0, 0.0]), "q_in")]
        surface = "closed"
        q_enclosed = q_inside
        status_kind = "ok"
        validity = "Ja"
    elif case == "Sluten yta: laddning utanför":
        charges = [(q_outside, np.array([2.15 * radius, 0.35 * radius, 0.0]), "q_ut")]
        surface = "closed"
        q_enclosed = 0.0
        status_kind = "ok"
        validity = "Ja"
    elif case == "Sluten yta: laddning både inne och ute":
        charges = [
            (q_inside, np.array([offset_fraction * radius, 0.0, 0.0]), "q_in"),
            (q_outside, np.array([2.15 * radius, 0.35 * radius, 0.0]), "q_ut"),
        ]
        surface = "closed"
        q_enclosed = q_inside
        status_kind = "ok"
        validity = "Ja"
    elif case == "Öppen yta: hemisfär utan lock":
        charges = [(q_inside, np.array([0.0, 0.0, 0.0]), "q")]
        surface = "open_hemisphere"
        q_enclosed = math.nan
        status_kind = "warning"
        validity = "Nej"
    else:
        charges = [(q_inside, np.array([radius, 0.0, 0.0]), "q på ytan")]
        surface = "closed"
        q_enclosed = math.nan
        status_kind = "error"
        validity = "Nej"

    X, Y, Z, NX, NY, NZ, dA, theta_range = _sphere_surface(radius, surface)
    pts = np.column_stack([X.ravel(), Y.ravel(), Z.ravel()])
    normals = np.column_stack([NX.ravel(), NY.ravel(), NZ.ravel()])
    E = _electric_field_from_charges(pts, charges, min_distance=0.055 * radius)
    Edotn = np.sum(E * normals, axis=1).reshape(X.shape)

    if status_kind == "error":
        numeric_flux = math.nan
    else:
        numeric_flux = float(np.nansum(Edotn * dA))

    if surface == "closed" and status_kind == "ok":
        gauss_flux = q_enclosed / EPS0
        rel_err = abs(numeric_flux - gauss_flux) / max(abs(gauss_flux), 1.0)
        if abs(gauss_flux) < 1e-20:
            rel_err = abs(numeric_flux)
        message = (
            "Satsen gäller: ytan är sluten och laddningen är inte på ytan. "
            "Den numeriska flödesintegralen följer Gauss förutsägelse inom diskretiseringsfelet."
        )
    elif surface == "open_hemisphere":
        gauss_flux = math.nan
        message = (
            "Detta är en medveten fälla: hemisfären saknar lock och omsluter därför ingen volym ensam. "
            "Flödet genom den öppna ytan kan beräknas, men det är inte Gauss sats i sluten-yta-form. Lägg till locket så blir ytan sluten."
        )
    else:
        gauss_flux = math.nan
        message = (
            "Laddningen ligger på själva ytan. Då är fältet singulärt på integrationsytan och frågan om 'innanför' blir tvetydig. "
            "Flytta laddningen lite inåt eller utåt och ta sedan ett gränsvärde."
        )

    fig = go.Figure()
    finite = Edotn[np.isfinite(Edotn)]
    if finite.size:
        cmax = float(np.nanpercentile(np.abs(finite), 96))
        if cmax <= 0 or not np.isfinite(cmax):
            cmax = 1.0
    else:
        cmax = 1.0

    fig.add_trace(go.Surface(
        x=X, y=Y, z=Z,
        surfacecolor=np.clip(Edotn, -cmax, cmax),
        colorscale="RdBu",
        reversescale=True,
        cmin=-cmax,
        cmax=cmax,
        opacity=0.72 if surface == "open_hemisphere" else 0.62,
        colorbar=dict(title="E·n", len=0.62, x=0.95),
        hovertemplate="E·n=%{surfacecolor:.3e}<extra></extra>",
        showscale=True,
        name="E·n på ytan",
        showlegend=False,
    ))

    if surface == "open_hemisphere":
        _add_open_rim(fig, radius)

    for q, pos, label in charges:
        if abs(q) < 1e-30:
            continue
        color = "#d62728" if q > 0 else "#1f77b4"
        fig.add_trace(go.Scatter3d(
            x=[pos[0]], y=[pos[1]], z=[pos[2]],
            mode="markers+text",
            marker=dict(size=8, color=color),
            text=[label], textposition="top center",
            hovertemplate=f"{label}: {q/1e-9:.2f} nC<extra></extra>",
            showlegend=False,
        ))

    if show_field_arrows:
        _add_gauss_surface_arrows(fig, X, Y, Z, E.reshape(X.shape + (3,)), radius, surface)

    lim = 2.65 * radius
    fig.update_layout(
        title=dict(text="Gauss flödessats: lokalt flöde på ytan", x=0.02),
        scene=dict(
            xaxis=dict(title="x [m]", range=[-lim, lim]),
            yaxis=dict(title="y [m]", range=[-lim, lim]),
            zaxis=dict(title="z [m]", range=[-lim, lim]),
            aspectmode="cube",
            camera=dict(eye=dict(x=1.65, y=1.35, z=1.05)),
        ),
        height=650,
        margin=dict(l=0, r=0, t=42, b=0),
        showlegend=False,
    )

    report = {
        "status": status_kind,
        "validity_short": validity,
        "q_enclosed_text": "—" if not math.isfinite(q_enclosed) else _fmt_eng(q_enclosed, "C"),
        "numeric_flux_text": "odefinierad" if not math.isfinite(numeric_flux) else _fmt_eng(numeric_flux, "V·m"),
        "gauss_flux_text": "gäller ej" if not math.isfinite(gauss_flux) else _fmt_eng(gauss_flux, "V·m"),
        "message": message,
    }
    return fig, report


def _sphere_surface(radius: float, surface: str):
    if surface == "open_hemisphere":
        theta_min, theta_max = 0.0, math.pi / 2
        n_theta = 34
    else:
        theta_min, theta_max = 0.0, math.pi
        n_theta = 58
    n_phi = 96
    theta_edges = np.linspace(theta_min, theta_max, n_theta + 1)
    phi_edges = np.linspace(0.0, 2 * math.pi, n_phi + 1)
    theta = 0.5 * (theta_edges[:-1] + theta_edges[1:])
    phi = 0.5 * (phi_edges[:-1] + phi_edges[1:])
    TH, PH = np.meshgrid(theta, phi, indexing="ij")
    X = radius * np.sin(TH) * np.cos(PH)
    Y = radius * np.sin(TH) * np.sin(PH)
    Z = radius * np.cos(TH)
    NX, NY, NZ = X / radius, Y / radius, Z / radius
    dtheta = theta_edges[1] - theta_edges[0]
    dphi = phi_edges[1] - phi_edges[0]
    dA = radius**2 * np.sin(TH) * dtheta * dphi
    return X, Y, Z, NX, NY, NZ, dA, (theta_min, theta_max)


def _electric_field_from_charges(points: np.ndarray, charges: list[tuple[float, np.ndarray, str]], min_distance: float) -> np.ndarray:
    total = np.zeros_like(points, dtype=float)
    for q, pos, _label in charges:
        if abs(q) < 1e-30:
            continue
        r = points - pos[None, :]
        dist = np.linalg.norm(r, axis=1)
        safe = np.maximum(dist, min_distance)
        total += (q / (4 * math.pi * EPS0)) * r / safe[:, None] ** 3
    return total


def _add_open_rim(fig: go.Figure, radius: float) -> None:
    phi = np.linspace(0, 2 * math.pi, 180)
    fig.add_trace(go.Scatter3d(
        x=radius * np.cos(phi), y=radius * np.sin(phi), z=np.zeros_like(phi),
        mode="lines",
        line=dict(color="#222222", width=6),
        hoverinfo="skip",
        showlegend=False,
    ))
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[0], mode="text",
        text=["öppen kant: inget lock"],
        textposition="bottom center",
        hoverinfo="skip",
        showlegend=False,
    ))


def _add_gauss_surface_arrows(fig: go.Figure, X: np.ndarray, Y: np.ndarray, Z: np.ndarray, E: np.ndarray, radius: float, surface: str) -> None:
    step_theta = 7 if surface == "closed" else 5
    step_phi = 12
    Xs = X[::step_theta, ::step_phi].ravel()
    Ys = Y[::step_theta, ::step_phi].ravel()
    Zs = Z[::step_theta, ::step_phi].ravel()
    Es = E[::step_theta, ::step_phi].reshape(-1, 3)
    mag = np.linalg.norm(Es, axis=1)
    keep = np.isfinite(mag) & (mag > 1e-30)
    if not np.any(keep):
        return
    Es = Es[keep] / mag[keep, None]
    fig.add_trace(go.Cone(
        x=Xs[keep], y=Ys[keep], z=Zs[keep],
        u=Es[:, 0], v=Es[:, 1], w=Es[:, 2],
        anchor="tail",
        sizemode="absolute",
        sizeref=max(0.20 * radius, 1e-6),
        colorscale=[[0.0, "#334155"], [1.0, "#334155"]],
        showscale=False,
        hoverinfo="skip",
        showlegend=False,
    ))


# ---------------------------------------------------------------------------
# Magnetostatic Stokes helpers
# ---------------------------------------------------------------------------


def _stokes_magnetostatic_slider_figure(
    current: float,
    loop_radius: float,
    conductor_radius: float,
    center_ratio: float,
    show_h_arrows: bool,
    show_surface_current: bool,
) -> tuple[go.Figure, dict[str, str]]:
    conductor_offset = center_ratio * loop_radius
    center = np.array([conductor_offset, 0.0])

    overlap_area = _circle_overlap_area(loop_radius, conductor_radius, abs(conductor_offset))
    conductor_area = math.pi * conductor_radius**2
    fraction = 0.0 if conductor_area <= 0 else overlap_area / conductor_area
    current_through = current * fraction
    circulation = _line_integral_H_around_circle(current, conductor_radius, center, loop_radius, closed=True)

    area_tol = 1e-9 * max(loop_radius * loop_radius, 1.0)
    if overlap_area >= conductor_area - area_tol:
        case_label = "helt innanför"
        status = "ok"
        message_prefix = "Hela strömtuben ligger innanför randen, så hela den fria strömmen räknas med."
    elif overlap_area <= area_tol:
        case_label = "helt utanför"
        status = "ok"
        message_prefix = "Strömtuben ligger helt utanför randen, så ingen fri ström går genom den valda ytan."
    else:
        case_label = "delvis genomskuren"
        status = "warning"
        message_prefix = "Strömtuben skär randen. Då är det bara den överlappande delen av strömmen som räknas i Ampères lag."

    fig = go.Figure()
    _add_stokes_disk(fig, loop_radius)
    _add_loop_boundary(fig, loop_radius, closed=True)
    _add_position_axis(fig, loop_radius)
    _add_current_tube(fig, center, conductor_radius, loop_radius, current)

    if show_h_arrows:
        _add_h_arrows_on_boundary(fig, current, conductor_radius, center, loop_radius, closed=True)
    if show_surface_current:
        _add_j_arrows(fig, center, conductor_radius, current, loop_radius)

    fig.add_trace(go.Scatter3d(
        x=[center[0]], y=[center[1]], z=[0.82 * loop_radius],
        mode="markers+text",
        marker=dict(size=5, color="#111827"),
        text=[f"x/R={center_ratio:.2f}"], textposition="top center",
        hoverinfo="skip", showlegend=False,
    ))

    lim = max(2.2 * loop_radius, abs(conductor_offset) + 2.0 * conductor_radius + 0.4)
    fig.update_layout(
        title=dict(text="Stokes/Ampère: flytta strömtuben genom den valda ytan", x=0.02),
        scene=dict(
            xaxis=dict(title="x [m]", range=[-lim, lim]),
            yaxis=dict(title="y [m]", range=[-lim, lim]),
            zaxis=dict(title="z [m]", range=[-0.9 * lim, 0.9 * lim]),
            aspectmode="cube",
            camera=dict(eye=dict(x=1.65, y=1.30, z=1.15)),
        ),
        height=650,
        margin=dict(l=0, r=0, t=42, b=0),
        showlegend=False,
    )

    diff = circulation - current_through
    message = message_prefix + " Den numeriska randintegralen ska följa den fria ström som faktiskt passerar genom ytan."
    report = {
        "status": status,
        "case_label": case_label,
        "circulation_text": _fmt_eng(circulation, "A"),
        "current_through_text": _fmt_eng(current_through, "A"),
        "difference_text": _fmt_eng(diff, "A"),
        "message": message,
    }
    return fig, report


def _add_stokes_disk(fig: go.Figure, radius: float) -> None:
    r = np.linspace(0, radius, 34)
    phi = np.linspace(0, 2 * math.pi, 96)
    R, PH = np.meshgrid(r, phi)
    X = R * np.cos(PH)
    Y = R * np.sin(PH)
    Z = np.zeros_like(X)
    fig.add_trace(go.Surface(
        x=X, y=Y, z=Z,
        surfacecolor=np.zeros_like(X),
        colorscale=[[0.0, "#93c5fd"], [1.0, "#93c5fd"]],
        opacity=0.28,
        showscale=False,
        hoverinfo="skip",
        showlegend=False,
    ))


def _add_loop_boundary(fig: go.Figure, radius: float, closed: bool) -> None:
    if closed:
        phi = np.linspace(0, 2 * math.pi, 220)
    else:
        phi = np.linspace(math.radians(25), math.radians(315), 190)
    fig.add_trace(go.Scatter3d(
        x=radius * np.cos(phi), y=radius * np.sin(phi), z=np.zeros_like(phi) + 0.02,
        mode="lines",
        line=dict(color="#111827", width=8),
        hovertemplate="Rand C<extra></extra>",
        showlegend=False,
    ))
    if not closed:
        endpoints = np.array([[radius * math.cos(phi[0]), radius * math.sin(phi[0]), 0.04], [radius * math.cos(phi[-1]), radius * math.sin(phi[-1]), 0.04]])
        fig.add_trace(go.Scatter3d(
            x=endpoints[:, 0], y=endpoints[:, 1], z=endpoints[:, 2],
            mode="markers+text",
            marker=dict(size=5, color="#b91c1c"),
            text=["start", "slut"], textposition="top center",
            hoverinfo="skip",
            showlegend=False,
        ))


def _add_position_axis(fig: go.Figure, loop_radius: float) -> None:
    axis_len = 1.85 * loop_radius
    fig.add_trace(go.Scatter3d(
        x=[-axis_len, axis_len], y=[0, 0], z=[-0.02, -0.02],
        mode="lines",
        line=dict(color="#64748b", width=4, dash="dash"),
        hoverinfo="skip", showlegend=False,
    ))
    marks = np.array([-loop_radius, 0.0, loop_radius])
    labels = ["-R", "0", "+R"]
    fig.add_trace(go.Scatter3d(
        x=marks, y=np.zeros(3), z=np.full(3, -0.02),
        mode="markers+text",
        marker=dict(size=4, color="#64748b"),
        text=labels, textposition="bottom center",
        hoverinfo="skip", showlegend=False,
    ))


def _add_current_tube(fig: go.Figure, center: np.ndarray, a: float, loop_radius: float, current: float) -> None:
    z = np.linspace(-0.75 * loop_radius, 0.75 * loop_radius, 20)
    phi = np.linspace(0, 2 * math.pi, 48)
    PH, Z = np.meshgrid(phi, z)
    X = center[0] + a * np.cos(PH)
    Y = center[1] + a * np.sin(PH)
    color = "#f97316" if current >= 0 else "#7c3aed"
    fig.add_trace(go.Surface(
        x=X, y=Y, z=Z,
        surfacecolor=np.zeros_like(X),
        colorscale=[[0.0, color], [1.0, color]],
        opacity=0.55,
        showscale=False,
        hovertemplate="strömtub<extra></extra>",
        showlegend=False,
    ))
    z_tip = 0.75 * loop_radius if current >= 0 else -0.75 * loop_radius
    fig.add_trace(go.Cone(
        x=[center[0]], y=[center[1]], z=[0.0],
        u=[0], v=[0], w=[1 if current >= 0 else -1],
        anchor="tail", sizemode="absolute", sizeref=max(0.35 * loop_radius, 1e-6),
        colorscale=[[0.0, color], [1.0, color]],
        showscale=False,
        hovertemplate=f"I={current:.3g} A<extra></extra>",
        showlegend=False,
    ))
    fig.add_trace(go.Scatter3d(
        x=[center[0]], y=[center[1]], z=[z_tip],
        mode="text",
        text=["I"], textposition="top center",
        hoverinfo="skip",
        showlegend=False,
    ))


def _add_j_arrows(fig: go.Figure, center: np.ndarray, a: float, current: float, loop_radius: float) -> None:
    # Show current density only on the part of the current tube that intersects the chosen disk.
    rr = np.linspace(0.0, 0.85 * a, 3)
    pp = np.linspace(0.0, 2 * math.pi, 10, endpoint=False)
    pts = []
    for rho in rr:
        for ph in pp:
            x = center[0] + rho * math.cos(ph)
            y = center[1] + rho * math.sin(ph)
            if x * x + y * y <= loop_radius * loop_radius:
                pts.append((x, y, 0.03))
    if not pts or abs(current) < 1e-12:
        return
    pts = np.array(pts)
    sign = 1 if current >= 0 else -1
    fig.add_trace(go.Cone(
        x=pts[:, 0], y=pts[:, 1], z=pts[:, 2],
        u=np.zeros(len(pts)), v=np.zeros(len(pts)), w=np.full(len(pts), sign),
        anchor="tail", sizemode="absolute", sizeref=max(0.16 * loop_radius, 1e-6),
        colorscale=[[0.0, "#f97316"], [1.0, "#f97316"]],
        showscale=False,
        hoverinfo="skip",
        showlegend=False,
    ))


def _add_h_arrows_on_boundary(fig: go.Figure, current: float, a: float, center: np.ndarray, loop_radius: float, closed: bool) -> None:
    if closed:
        phi = np.linspace(0, 2 * math.pi, 22, endpoint=False)
    else:
        phi = np.linspace(math.radians(35), math.radians(305), 16)
    pts2 = np.column_stack([loop_radius * np.cos(phi), loop_radius * np.sin(phi)])
    H = _H_from_uniform_current_tube(pts2, current, a, center)
    mag = np.linalg.norm(H, axis=1)
    keep = mag > 1e-12
    if not np.any(keep):
        return
    Hdir = H[keep] / mag[keep, None]
    pts2 = pts2[keep]
    fig.add_trace(go.Cone(
        x=pts2[:, 0], y=pts2[:, 1], z=np.full(len(pts2), 0.08),
        u=Hdir[:, 0], v=Hdir[:, 1], w=np.zeros(len(pts2)),
        anchor="tail", sizemode="absolute", sizeref=max(0.16 * loop_radius, 1e-6),
        colorscale=[[0.0, "#2563eb"], [1.0, "#2563eb"]],
        showscale=False,
        hoverinfo="skip",
        showlegend=False,
    ))


def _line_integral_H_around_circle(current: float, a: float, center: np.ndarray, R: float, closed: bool) -> float:
    if closed:
        phi = np.linspace(0, 2 * math.pi, 3000, endpoint=False)
        dphi = 2 * math.pi / len(phi)
    else:
        phi = np.linspace(math.radians(25), math.radians(315), 2200)
        dphi = (phi[-1] - phi[0]) / (len(phi) - 1)
    pts = np.column_stack([R * np.cos(phi), R * np.sin(phi)])
    H = _H_from_uniform_current_tube(pts, current, a, center)
    dl_dphi = np.column_stack([-R * np.sin(phi), R * np.cos(phi)])
    return float(np.sum(np.einsum("ij,ij->i", H, dl_dphi)) * dphi)


def _H_from_uniform_current_tube(points2: np.ndarray, current: float, a: float, center: np.ndarray) -> np.ndarray:
    rel = points2 - center[None, :]
    x = rel[:, 0]
    y = rel[:, 1]
    rho = np.sqrt(x * x + y * y)
    Hphi = np.zeros_like(rho)
    inside = rho < a
    outside = ~inside
    if a > 0:
        Hphi[inside] = current * rho[inside] / (2 * math.pi * a * a)
    Hphi[outside] = current / (2 * math.pi * np.maximum(rho[outside], 1e-12))
    phihat = np.column_stack([-y / np.maximum(rho, 1e-12), x / np.maximum(rho, 1e-12)])
    H = Hphi[:, None] * phihat
    H[rho < 1e-12] = 0.0
    return H


def _circle_overlap_area(R: float, a: float, d: float) -> float:
    # Area common to a disk of radius R centered at origin and a disk of radius a centered d away.
    if d >= R + a:
        return 0.0
    if d <= abs(R - a):
        return math.pi * min(R, a) ** 2
    part1 = R * R * math.acos((d * d + R * R - a * a) / (2 * d * R))
    part2 = a * a * math.acos((d * d + a * a - R * R) / (2 * d * a))
    part3 = 0.5 * math.sqrt(max(0.0, (-d + R + a) * (d + R - a) * (d - R + a) * (d + R + a)))
    return part1 + part2 - part3


def _charging_capacitor_figure(current: float, loop_radius: float) -> tuple[go.Figure, dict[str, str]]:
    fig = go.Figure()
    R = loop_radius
    plate_r = 0.78 * R
    z1, z2 = -0.35 * R, 0.35 * R
    phi = np.linspace(0, 2 * math.pi, 80)
    rr = np.linspace(0, plate_r, 24)
    RR, PH = np.meshgrid(rr, phi)
    X = RR * np.cos(PH)
    Y = RR * np.sin(PH)
    for z, label in [(z1, "platta"), (z2, "platta")]:
        fig.add_trace(go.Surface(
            x=X, y=Y, z=np.full_like(X, z),
            surfacecolor=np.zeros_like(X),
            colorscale=[[0.0, "#94a3b8"], [1.0, "#94a3b8"]],
            opacity=0.48,
            showscale=False,
            hoverinfo="skip",
            showlegend=False,
        ))
    _add_loop_boundary(fig, R, closed=True)

    # H arrows around the loop, caused by total Maxwell current.
    pts_phi = np.linspace(0, 2 * math.pi, 22, endpoint=False)
    sign = 1 if current >= 0 else -1
    fig.add_trace(go.Cone(
        x=R * np.cos(pts_phi), y=R * np.sin(pts_phi), z=np.zeros_like(pts_phi),
        u=-sign * np.sin(pts_phi), v=sign * np.cos(pts_phi), w=np.zeros_like(pts_phi),
        anchor="tail", sizemode="absolute", sizeref=max(0.16 * R, 1e-6),
        colorscale=[[0.0, "#2563eb"], [1.0, "#2563eb"]],
        showscale=False,
        hoverinfo="skip",
        showlegend=False,
    ))
    # Displacement current arrows in the gap.
    grid = []
    for rho in np.linspace(0.0, 0.65 * plate_r, 3):
        for ph in np.linspace(0, 2 * math.pi, 10, endpoint=False):
            grid.append((rho * math.cos(ph), rho * math.sin(ph), -0.12 * R))
    grid = np.array(grid)
    fig.add_trace(go.Cone(
        x=grid[:, 0], y=grid[:, 1], z=grid[:, 2],
        u=np.zeros(len(grid)), v=np.zeros(len(grid)), w=np.full(len(grid), sign),
        anchor="tail", sizemode="absolute", sizeref=max(0.18 * R, 1e-6),
        colorscale=[[0.0, "#22c55e"], [1.0, "#22c55e"]],
        showscale=False,
        hovertemplate="förskjutningsström ∂D/∂t<extra></extra>",
        showlegend=False,
    ))
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[0.58 * R], mode="text",
        text=["laddande kondensator: ∂D/∂t behövs"],
        textposition="top center",
        hoverinfo="skip",
        showlegend=False,
    ))
    lim = 1.65 * R
    fig.update_layout(
        title=dict(text="Inte magnetostatik: Maxwell–Ampère behövs", x=0.02),
        scene=dict(
            xaxis=dict(title="x [m]", range=[-lim, lim]),
            yaxis=dict(title="y [m]", range=[-lim, lim]),
            zaxis=dict(title="z [m]", range=[-lim, lim]),
            aspectmode="cube",
            camera=dict(eye=dict(x=1.55, y=1.25, z=1.15)),
        ),
        height=650,
        margin=dict(l=0, r=0, t=42, b=0),
        showlegend=False,
    )

    report = {
        "status": "error",
        "case_label": "ej magnetostatik",
        "validity_short": "Nej",
        "circulation_text": _fmt_eng(current, "A"),
        "current_through_text": "0 A ledningsström",
        "difference_text": "saknar ∂D/∂t",
        "message": (
            "Detta är inte magnetostatik. Om du väljer en yta mellan kondensatorplattorna går ingen ledningsström genom ytan, "
            "men H-cirkulationen runt randen kan ändå vara icke-noll. Den saknade termen är förskjutningsströmmen ∂D/∂t."
        ),
    }
    return fig, report


# ---------------------------------------------------------------------------
# Shared utilities
# ---------------------------------------------------------------------------


def _fmt_eng(value: float, unit: str) -> str:
    try:
        value = float(value)
    except Exception:
        return f"{value} {unit}".strip()
    if not math.isfinite(value):
        return "—"
    if abs(value) < 5e-15:
        text = "0"
    elif 1e-3 <= abs(value) < 1e4:
        text = f"{value:.4g}"
    else:
        exponent = int(math.floor(math.log10(abs(value))))
        mantissa = value / 10**exponent
        text = f"{mantissa:.3g}×10^{exponent}"
    return f"{text} {unit}".strip()
