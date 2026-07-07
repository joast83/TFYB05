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
            "- Färgen på ytan visar lokalt **E·n̂**: rött = utåt, blått = inåt.\n"
            "- Totalen jämförs med **Q_innesluten/ε₀**.\n"
            "- Öppna ytor och laddningar på själva ytan markeras som fall där satsen inte kan användas direkt."
        )
        return

    if section == "Testlabb":
        st.markdown("### Flytta en laddning genom en Gaussyta")
        st.write(
            "Det här testet använder **en enda laddning**. Dra positionsreglaget från centrum, genom ytan och vidare utanför. "
            "För en sluten yta ska totalflödet hoppa från q/ε₀ till 0 när laddningen passerar ut, medan det lokala flödesmönstret ändras kontinuerligt."
        )

        c1, c2, c3 = st.columns(3)
        with c1:
            q_nc = st.slider("Laddning q [nC]", -10.0, 10.0, 5.0, 0.5, key="gauss_moving_q")
            radius = st.slider("Ytradie R [m]", 0.8, 2.0, 1.1, 0.1, key="gauss_radius")
        with c2:
            position_ratio = st.slider(
                "Laddningens position x/R",
                -0.50,
                2.00,
                0.45,
                0.05,
                key="gauss_position_ratio",
                help="x/R < 1 betyder innanför. x/R = 1 ligger på ytan. x/R > 1 betyder utanför.",
            )
            surface_kind = st.radio(
                "Yta",
                ["Sluten sfär", "Öppen hemisfär utan lock"],
                index=0,
                key="gauss_surface_kind",
            )
        with c3:
            show_field_arrows = st.checkbox("Visa E-pilar på ytan", value=True, key="gauss_arrows")
            show_position_axis = st.checkbox("Visa positionsaxel", value=True, key="gauss_position_axis")

        fig, report = _gauss_figure(
            radius=radius,
            q_nc=q_nc,
            position_ratio=position_ratio,
            surface_kind=surface_kind,
            show_field_arrows=show_field_arrows,
            show_position_axis=show_position_axis,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False})

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Laddningens läge", report["position_text"])
        m2.metric("Q_innesluten", report["q_enclosed_text"])
        m3.metric("Numerisk ∫E·dA", report["numeric_flux_text"])
        m4.metric("Gauss förutsägelse", report["gauss_flux_text"])

        if report["status"] == "ok":
            st.success(report["message"])
        elif report["status"] == "warning":
            st.warning(report["message"])
        else:
            st.error(report["message"])

        st.markdown(
            "#### Läs figuren så här\n"
            "- Färgen på ytan är lokalt **E·n̂**: rött betyder utåt och blått betyder inåt.\n"
            "- När laddningen är **innanför** finns ett nettoöverskott av utgående fält genom den slutna ytan.\n"
            "- När laddningen är **utanför** går fältlinjer in genom vissa delar och ut genom andra; totalen blir noll.\n"
            "- När laddningen ligger **på ytan** är fältet singulärt där, så satsen måste hanteras som ett gränsfall.\n"
            "- Om du byter till **öppen hemisfär** saknas en sluten volym, så Gauss sats i denna form kan inte användas direkt."
        )
        return

    st.markdown(
        "### Beräkningsrecept\n"
        "1. **Välj en sluten yta**. Den måste omsluta en volym.\n"
        "2. **Räkna nettoladdningen innanför**: positiva och negativa laddningar summeras algebraiskt.\n"
        "3. **Skriv flödet** som ∮ₛ E·dA.\n"
        "4. **Använd symmetri bara om den faktiskt finns.** För sfärisk, cylindrisk eller plan symmetri kan E ofta tas ut ur integralen.\n"
        "5. **Kontrollera fallgroparna:** öppen yta, laddning på randen, eller för lite symmetri för att lösa E direkt."
    )
    st.info(
        "**Viktig distinktion:** Gauss sats är alltid en stark kontroll för totalflöde genom en sluten yta. "
        "Men den är bara en enkel metod för att hitta själva fältet när geometrin har tillräcklig symmetri."
    )


# ---------------------------------------------------------------------------
# Stokes theorem for magnetostatics
# ---------------------------------------------------------------------------


def _render_stokes_page() -> None:
    import streamlit as st

    st.title("Teori: Stokes sats i magnetostatik")
    st.caption("Här kopplas Stokes sats till Ampères lag för stationära strömmar.")

    section = st.radio(
        "Välj del",
        ["Intuition", "Testlabb", "Beräkningsrecept"],
        horizontal=True,
        key="stokes_section",
    )

    if section == "Intuition":
        st.latex(r"\oint_C \mathbf{H}\cdot d\mathbf{l} = \iint_S (\nabla\times\mathbf{H})\cdot\hat{\mathbf{n}}\,dS")
        st.latex(r"\nabla\times\mathbf{H}=\mathbf{J}_{\mathrm{fri}}\quad\Rightarrow\quad\oint_C \mathbf{H}\cdot d\mathbf{l}=I_{\mathrm{fri, genom}\;S}")
        c1, c2 = st.columns([1.1, 1.0])
        with c1:
            st.markdown(
                "### Magnetostatisk tolkning\n"
                "I magnetostatik är fria strömmar källan till virvling i **H-fältet**. "
                "Stokes sats säger att cirkulationen runt den slutna randen **C** är samma sak som den totala curlen genom ytan **S**. "
                "Med Ampères lokala lag blir denna curl-flux lika med fri ström genom ytan."
            )
        with c2:
            st.info(
                "**Kom ihåg orienteringen:**\n\n"
                "Högerhandsregeln kopplar randens riktning till ytans normal. Om du vänder normalen byter även randintegralens tecken."
            )
            st.warning(
                "**Magnetostatik betyder stationärt.**\n\n"
                "Vid tidsvarierande elektriska fält måste Maxwell-termen ∂D/∂t tas med. Då räcker inte den magnetostatiska Ampèreformen."
            )
        st.markdown(
            "### Vad testlabbet visar\n"
            "- En strömtub genom en vald yta skapar cirkulation hos **H** längs randen.\n"
            "- Om ingen fri ström går genom ytan blir cirkulationen noll.\n"
            "- Om randen skär strömtuben räknas bara den del av strömmen som faktiskt passerar genom ytan.\n"
            "- Öppna kurvor och tidsvarierande kondensatorfält markeras som fall där den använda magnetostatiska formen inte är rätt verktyg."
        )
        return

    if section == "Testlabb":
        st.markdown("### Testa Ampères lag som Stokes sats i magnetostatik")
        c1, c2, c3 = st.columns(3)
        with c1:
            case = st.selectbox(
                "Testfall",
                [
                    "Stationär ström: hela strömtuben omsluts",
                    "Stationär ström: ingen ström omsluts",
                    "Stationär ström: randen skär strömtuben",
                    "Inte Stokes direkt: öppen kurva",
                    "Inte magnetostatik: laddande kondensator",
                ],
                key="stokes_case",
            )
            current = st.slider("Fri ström I [A]", -5.0, 5.0, 2.0, 0.25, key="stokes_current")
        with c2:
            loop_radius = st.slider("Randradie R [m]", 0.8, 2.0, 1.2, 0.1, key="stokes_loop_radius")
            conductor_radius = st.slider("Strömtubens radie a [m]", 0.12, 0.55, 0.25, 0.01, key="stokes_conductor_radius")
        with c3:
            show_h_arrows = st.checkbox("Visa H-pilar längs randen", value=True, key="stokes_h_arrows")
            show_surface_current = st.checkbox("Visa J genom ytan", value=True, key="stokes_j_arrows")

        fig, report = _stokes_magnetostatic_figure(
            case=case,
            current=current,
            loop_radius=loop_radius,
            conductor_radius=conductor_radius,
            show_h_arrows=show_h_arrows,
            show_surface_current=show_surface_current,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False})

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Giltig magnetostatisk användning?", report["validity_short"])
        m2.metric("∮ H·dl", report["circulation_text"])
        m3.metric("Fri ström genom S", report["current_through_text"])
        m4.metric("Skillnad", report["difference_text"])

        if report["status"] == "ok":
            st.success(report["message"])
        elif report["status"] == "warning":
            st.warning(report["message"])
        else:
            st.error(report["message"])

        st.markdown(
            "#### Läs figuren så här\n"
            "- Den gröna skivan är ytan **S**, och den mörka kurvan är randen **C**.\n"
            "- Orange cylinder/pilar visar fri ström **J_fri**.\n"
            "- Blå pilar längs randen visar **H-fältets tangentbidrag** till ∮C H·dl.\n"
            "- När strömtuben bara delvis skär ytan är **I_genom S** inte hela strömmen, utan bara överlappande del."
        )
        return

    st.markdown(
        "### Beräkningsrecept för magnetostatik\n"
        "1. Välj en **sluten randkurva** C.\n"
        "2. Välj en orienterad yta S vars rand är just C.\n"
        "3. Använd högerhandsregeln för att koppla randriktning och normalriktning.\n"
        "4. Beräkna den fria stationära strömmen genom ytan: I_fri = ∬S J_fri·n̂ dS.\n"
        "5. Sätt ∮C H·dl = I_fri. Om symmetrin gör H konstant längs randen kan du lösa ut H."
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
    radius: float,
    q_nc: float,
    position_ratio: float,
    surface_kind: str,
    show_field_arrows: bool,
    show_position_axis: bool,
) -> tuple[go.Figure, dict[str, str]]:
    """Interactive Gauss test with one movable charge.

    The old version separated "inside" and "outside" into different cases, which
    hid the important limiting process. This version keeps the charge and the
    Gaussian surface fixed as concepts, and lets the charge coordinate x/R cross
    the boundary continuously.
    """
    q = q_nc * 1e-9
    charge_pos = np.array([position_ratio * radius, 0.0, 0.0])
    radial_position = abs(position_ratio)
    boundary_tol = 0.025
    is_open = surface_kind == "Öppen hemisfär utan lock"
    on_surface = abs(radial_position - 1.0) <= boundary_tol
    inside_closed_surface = radial_position < 1.0 - boundary_tol
    outside_closed_surface = radial_position > 1.0 + boundary_tol

    surface = "open_hemisphere" if is_open else "closed"
    charges = [(q, charge_pos, "q")]

    if is_open:
        q_enclosed = math.nan
        gauss_flux = math.nan
        status_kind = "warning"
        validity = "Nej"
        if on_surface:
            position_text = "på öppna kanten"
        elif inside_closed_surface:
            position_text = "under hemisfären"
        else:
            position_text = "utanför"
        message = (
            "Den öppna hemisfären är ett viktigt motexempel: flödet genom ytan kan beräknas, "
            "men Gauss sats i formen ∮E·dA = Q_in/ε₀ kräver en sluten yta. Lägg till ett lock i basplanet för att få en Gaussyta."
        )
    elif on_surface:
        q_enclosed = math.nan
        gauss_flux = math.nan
        status_kind = "error"
        validity = "Gränsfall"
        position_text = "på ytan"
        message = (
            "Laddningen ligger på själva integrationsytan. Fältet blir singulärt där och 'innanför' är inte väldefinierat. "
            "Flytta laddningen ett steg inåt eller utåt och jämför gränsvärdena."
        )
    elif inside_closed_surface:
        q_enclosed = q
        gauss_flux = q_enclosed / EPS0
        status_kind = "ok"
        validity = "Ja"
        position_text = "innanför"
        message = (
            "Laddningen är innanför den slutna ytan. Totalflödet ska därför vara q/ε₀, även om laddningen inte ligger i centrum "
            "och färgmönstret på ytan blir osymmetriskt."
        )
    else:
        # Includes the deliberately outside region. A charge outside a closed
        # surface contributes zero net flux: field lines enter and leave.
        q_enclosed = 0.0
        gauss_flux = 0.0
        status_kind = "ok"
        validity = "Ja"
        position_text = "utanför"
        message = (
            "Laddningen är utanför den slutna ytan. Den kan ge starkt lokalt flöde på närmaste sida, "
            "men lika mycket fält går in som ut, så nettot blir noll."
        )

    X, Y, Z, NX, NY, NZ, dA, theta_range = _sphere_surface(radius, surface)
    pts = np.column_stack([X.ravel(), Y.ravel(), Z.ravel()])
    normals = np.column_stack([NX.ravel(), NY.ravel(), NZ.ravel()])
    E = _electric_field_from_charges(pts, charges, min_distance=0.055 * radius)
    Edotn = np.sum(E * normals, axis=1).reshape(X.shape)

    if status_kind == "error":
        numeric_flux = math.nan
    else:
        numeric_flux = float(np.nansum(Edotn * dA))

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

    if show_position_axis:
        _add_gauss_position_axis(fig, radius, max(2.05 * radius, abs(charge_pos[0]) + 0.25 * radius))

    if abs(q) > 1e-30:
        color = "#d62728" if q > 0 else "#1f77b4"
        fig.add_trace(go.Scatter3d(
            x=[charge_pos[0]], y=[charge_pos[1]], z=[charge_pos[2]],
            mode="markers+text",
            marker=dict(size=9, color=color, line=dict(color="#111827", width=1)),
            text=["q"], textposition="top center",
            hovertemplate=f"q={q_nc:.2f} nC<br>x/R={position_ratio:.2f}<extra></extra>",
            showlegend=False,
        ))

    if show_field_arrows:
        _add_gauss_surface_arrows(fig, X, Y, Z, E.reshape(X.shape + (3,)), radius, surface)

    lim = max(2.35 * radius, abs(charge_pos[0]) + 0.65 * radius)
    fig.update_layout(
        title=dict(text="Gauss flödessats: flytta laddningen genom ytan", x=0.02),
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
        "position_text": f"{position_text} (x/R={position_ratio:.2f})",
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


def _add_gauss_position_axis(fig: go.Figure, radius: float, extent: float) -> None:
    """Draw the x-axis used by the moving-charge Gauss experiment."""
    xs = np.linspace(-extent, extent, 80)
    fig.add_trace(go.Scatter3d(
        x=xs,
        y=np.zeros_like(xs),
        z=np.zeros_like(xs),
        mode="lines",
        line=dict(color="#111827", width=3, dash="dash"),
        hoverinfo="skip",
        showlegend=False,
    ))
    fig.add_trace(go.Scatter3d(
        x=[-radius, radius],
        y=[0, 0],
        z=[0, 0],
        mode="markers+text",
        marker=dict(size=5, color="#111827"),
        text=["x/R=-1", "x/R=1"],
        textposition=["bottom center", "bottom center"],
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


def _stokes_magnetostatic_figure(
    case: str,
    current: float,
    loop_radius: float,
    conductor_radius: float,
    show_h_arrows: bool,
    show_surface_current: bool,
) -> tuple[go.Figure, dict[str, str]]:
    if case == "Stationär ström: hela strömtuben omsluts":
        conductor_offset = 0.0
        mode = "closed"
        status = "ok"
        validity = "Ja"
        message_prefix = "Satsen och den magnetostatiska Ampèreformen gäller. Hela den fria strömmen går genom ytan."
    elif case == "Stationär ström: ingen ström omsluts":
        conductor_offset = loop_radius + conductor_radius + 0.45
        mode = "closed"
        status = "ok"
        validity = "Ja"
        message_prefix = "Satsen gäller och ingen fri ström passerar genom ytan. Cirkulationen runt randen blir därför noll."
    elif case == "Stationär ström: randen skär strömtuben":
        conductor_offset = loop_radius - 0.45 * conductor_radius
        mode = "closed"
        status = "warning"
        validity = "Ja"
        message_prefix = "Satsen gäller, men det enkla talet 'hela strömmen' är fel. Bara den del av strömtuben som skär ytan räknas."
    elif case == "Inte Stokes direkt: öppen kurva":
        conductor_offset = 0.0
        mode = "open_arc"
        status = "error"
        validity = "Nej"
        message_prefix = "Kurvan är öppen. Stokes sats kräver en sluten randkurva C. Lägg till en retursträcka eller välj en sluten slinga."
    else:
        return _charging_capacitor_figure(current, loop_radius)

    center = np.array([conductor_offset, 0.0])
    fig = go.Figure()
    _add_stokes_disk(fig, loop_radius)
    _add_current_tube(fig, center, conductor_radius, loop_radius, current)

    if mode == "closed":
        circulation = _line_integral_H_around_circle(current, conductor_radius, center, loop_radius, closed=True)
        current_through = current * _circle_overlap_area(loop_radius, conductor_radius, abs(conductor_offset)) / (math.pi * conductor_radius**2)
        _add_loop_boundary(fig, loop_radius, closed=True)
    else:
        circulation = _line_integral_H_around_circle(current, conductor_radius, center, loop_radius, closed=False)
        current_through = math.nan
        _add_loop_boundary(fig, loop_radius, closed=False)

    if show_h_arrows:
        _add_h_arrows_on_boundary(fig, current, conductor_radius, center, loop_radius, closed=(mode == "closed"))
    if show_surface_current and mode == "closed":
        _add_j_arrows(fig, center, conductor_radius, current, loop_radius)

    lim = max(2.2 * loop_radius, abs(conductor_offset) + 2.0 * conductor_radius + 0.4)
    fig.update_layout(
        title=dict(text="Stokes/Ampère: cirkulation runt C och fri ström genom S", x=0.02),
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

    if mode == "closed":
        diff = circulation - current_through
        message = message_prefix + " Den numeriska randintegralen matchar strömmen genom ytan."
        current_text = _fmt_eng(current_through, "A")
        difference_text = _fmt_eng(diff, "A")
    else:
        message = message_prefix + " Den visade bågintegralen är bara ett kurvbidrag, inte en Stokes-randintegral."
        current_text = "ej definierad"
        difference_text = "ej meningsfull"

    report = {
        "status": status,
        "validity_short": validity,
        "circulation_text": _fmt_eng(circulation, "A") if math.isfinite(circulation) else "ej definierad",
        "current_through_text": current_text,
        "difference_text": difference_text,
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
