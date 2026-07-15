"""Interactive theory pages used by the Streamlit application.

The theory pages are deliberately independent of the exercise registry.  They explain
Gauss' law and the magnetostatic form of Ampère's law with compact interactive models.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np
import plotly.graph_objects as go

from .core import EPS0, MU0


@dataclass(frozen=True)
class TheoryPage:
    key: str
    title: str
    short_description: str


THEORY_PAGES = [
    TheoryPage(
        key="gauss_flux",
        title="Gauss flödessats",
        short_description=(
            "Slutna ytor, elektriskt flöde och hur innesluten laddning bestämmer "
            "det totala flödet."
        ),
    ),
    TheoryPage(
        key="stokes_magnetostatics",
        title="Stokes sats i magnetostatik",
        short_description=(
            "Kopplingen mellan Stokes sats, Ampères lag, cirkulation och fri ström."
        ),
    ),
]

THEORY_PAGE_LOOKUP = {page.title: page for page in THEORY_PAGES}


def render_theory_page(page: TheoryPage) -> None:
    if page.key == "gauss_flux":
        _render_gauss_page()
    elif page.key == "stokes_magnetostatics":
        _render_stokes_page()
    else:
        import streamlit as st

        st.error("Okänd teorisida.")


def _render_gauss_page() -> None:
    import streamlit as st

    st.title("Teori: Gauss flödessats")
    st.latex(
        r"\oint_S \mathbf{E}\cdot d\mathbf{A}="
        r"\frac{Q_{\mathrm{innesluten}}}{\varepsilon_0}"
    )
    st.write(
        "Gauss sats gäller för varje sluten yta. Symmetri behövs inte för själva "
        "satsen, men stark symmetri behövs ofta för att kunna lösa ut fältstyrkan "
        "direkt ur flödesintegralen."
    )

    section = st.radio(
        "Välj del",
        ["Intuition", "Testlabb", "Beräkningsrecept"],
        horizontal=True,
        key="gauss_section",
    )

    if section == "Intuition":
        left, right = st.columns(2)
        with left:
            st.markdown(
                "### Kärnidé\n"
                "En sluten yta fungerar som en kontrollvolym. Fältlinjer från en "
                "yttre laddning går både in genom och ut genom ytan, så nettobidraget "
                "till flödet tar ut sig. En laddning inuti ger däremot ett nettoflöde."
            )
        with right:
            st.info(
                "Ytans form ändrar den lokala fördelningen av flöde, men inte "
                "totalflödet så länge samma nettoladdning omsluts."
            )
            st.warning(
                "Gauss sats innebär inte automatiskt att E är konstant på ytan. "
                "Det följer endast av lämplig symmetri."
            )
        return

    if section == "Beräkningsrecept":
        st.markdown(
            "### Arbetsgång\n"
            "1. Välj en **sluten** Gaussyta.\n"
            "2. Summera nettoladdningen innanför ytan.\n"
            "3. Bestäm riktningen för ytans utåtriktade normal.\n"
            "4. Utnyttja symmetri när den gör E konstant eller vinkelrät mot ytan.\n"
            "5. Kontrollera enheter och gränsfall."
        )
        st.latex(r"[\Phi_E]=\mathrm{N\,m^2/C}=\mathrm{V\,m}")
        return

    st.markdown("### Flytta en punktladdning genom en sfär")
    c1, c2 = st.columns(2)
    with c1:
        q_nc = st.slider("Laddning q [nC]", -10.0, 10.0, 5.0, 0.5)
        radius = st.slider("Sfärens radie R [m]", 0.5, 2.0, 1.0, 0.1)
    with c2:
        position_ratio = st.slider(
            "Laddningens position x/R",
            -1.5,
            1.5,
            0.2,
            0.05,
            help="|x/R| < 1 betyder att laddningen ligger innanför sfären.",
        )
        show_vectors = st.checkbox("Visa radiella normalpilar", value=True)

    figure = _gauss_sphere_figure(radius, position_ratio, show_vectors)
    st.plotly_chart(figure, use_container_width=True, config={"displaylogo": False})

    q = q_nc * 1e-9
    boundary_tolerance = 1e-9
    if abs(abs(position_ratio) - 1.0) <= boundary_tolerance:
        enclosed = math.nan
        flux_text = "singulärt gränsfall"
        st.warning(
            "Laddningen ligger på ytan. Punktladdningsfältet är då singulärt på "
            "integrationsytan och standardformen kan inte användas direkt."
        )
    elif abs(position_ratio) < 1.0:
        enclosed = q
        flux_text = f"{q / EPS0:.5g} V·m"
        st.success("Laddningen är innesluten: totalflödet är q/ε₀.")
    else:
        enclosed = 0.0
        flux_text = "0 V·m"
        st.info("Laddningen ligger utanför: nettoflödet genom den slutna ytan är noll.")

    m1, m2, m3 = st.columns(3)
    m1.metric("Läge", "innanför" if abs(position_ratio) < 1 else "utanför/på ytan")
    m2.metric(
        "Q innesluten",
        "ej definierat" if math.isnan(enclosed) else f"{enclosed * 1e9:.4g} nC",
    )
    m3.metric("Gauss förutsägelse", flux_text)


def _gauss_sphere_figure(radius: float, position_ratio: float, show_vectors: bool) -> go.Figure:
    theta = np.linspace(0.0, 2.0 * np.pi, 64)
    phi = np.linspace(0.0, np.pi, 32)
    theta_grid, phi_grid = np.meshgrid(theta, phi)
    x = radius * np.sin(phi_grid) * np.cos(theta_grid)
    y = radius * np.sin(phi_grid) * np.sin(theta_grid)
    z = radius * np.cos(phi_grid)

    figure = go.Figure()
    figure.add_trace(
        go.Surface(
            x=x,
            y=y,
            z=z,
            opacity=0.28,
            showscale=False,
            colorscale="Blues",
            hoverinfo="skip",
            name="Gaussyta",
        )
    )
    charge_x = position_ratio * radius
    figure.add_trace(
        go.Scatter3d(
            x=[charge_x],
            y=[0.0],
            z=[0.0],
            mode="markers+text",
            marker={"size": 8},
            text=["q"],
            textposition="top center",
            name="Punktladdning",
        )
    )

    if show_vectors:
        sample_theta = np.linspace(0.0, 2.0 * np.pi, 12, endpoint=False)
        sample_phi = np.linspace(0.25, np.pi - 0.25, 6)
        tt, pp = np.meshgrid(sample_theta, sample_phi)
        sx = radius * np.sin(pp) * np.cos(tt)
        sy = radius * np.sin(pp) * np.sin(tt)
        sz = radius * np.cos(pp)
        figure.add_trace(
            go.Cone(
                x=sx.ravel(),
                y=sy.ravel(),
                z=sz.ravel(),
                u=(sx / radius).ravel(),
                v=(sy / radius).ravel(),
                w=(sz / radius).ravel(),
                sizemode="absolute",
                sizeref=0.12 * radius,
                showscale=False,
                name="Ytnormal",
            )
        )

    extent = 1.65 * radius
    figure.update_layout(
        height=520,
        margin={"l": 0, "r": 0, "t": 35, "b": 0},
        scene={
            "aspectmode": "cube",
            "xaxis": {"range": [-extent, extent], "title": "x [m]"},
            "yaxis": {"range": [-extent, extent], "title": "y [m]"},
            "zaxis": {"range": [-extent, extent], "title": "z [m]"},
        },
        title="Sluten Gaussyta och punktladdning",
    )
    return figure


def _render_stokes_page() -> None:
    import streamlit as st

    st.title("Teori: Stokes sats i magnetostatik")
    st.latex(
        r"\oint_C \mathbf{H}\cdot d\mathbf{l}="
        r"\iint_S (\nabla\times\mathbf{H})\cdot\hat{\mathbf{n}}\,dS="
        r"I_{\mathrm{fri,genom}\,S}"
    )
    st.write(
        "Stokes sats kopplar cirkulationen längs en sluten rand till rotationen "
        "genom en yta. I magnetostatik ger Ampères lag att cirkulationen hos H "
        "bestäms av den fria ström som passerar genom ytan."
    )

    section = st.radio(
        "Välj del",
        ["Intuition", "Testlabb", "Beräkningsrecept"],
        horizontal=True,
        key="stokes_section",
    )
    if section == "Intuition":
        st.info(
            "Högerhandsregeln kopplar randens orientering till ytans normal. Om "
            "normalen vänds, vänds även randintegralens tecken."
        )
        st.warning(
            "Den magnetostatiska formen gäller stationära strömmar. Vid "
            "tidsvarierande elektriska fält måste Maxwells förskjutningsström tas med."
        )
        return

    if section == "Beräkningsrecept":
        st.markdown(
            "### Arbetsgång\n"
            "1. Välj en sluten integrationskurva C.\n"
            "2. Välj en yta S med C som rand.\n"
            "3. Bestäm orienteringen med högerhandsregeln.\n"
            "4. Summera den fria ström som skär ytan med tecken.\n"
            "5. Utnyttja symmetri för att förenkla H·dl."
        )
        st.latex(r"B=\mu_0 H\quad\text{i vakuum}")
        return

    st.markdown("### Ström genom en cirkulär ampereslinga")
    c1, c2 = st.columns(2)
    with c1:
        current = st.slider("Fri ström I [A]", -5.0, 5.0, 2.0, 0.25)
        loop_radius = st.slider("Slingradie R [m]", 0.5, 2.0, 1.0, 0.1)
    with c2:
        offset_ratio = st.slider(
            "Ledningens centrum x/R",
            -1.5,
            1.5,
            0.0,
            0.05,
            help="|x/R| < 1 placerar ledningen innanför integrationsytan.",
        )
        conductor_radius = st.slider("Ledningsradie a/R", 0.05, 0.4, 0.15, 0.01)

    figure = _ampere_figure(loop_radius, offset_ratio, conductor_radius)
    st.plotly_chart(figure, use_container_width=True, config={"displaylogo": False})

    enclosed = current if abs(offset_ratio) + conductor_radius <= 1.0 else 0.0
    if abs(offset_ratio) - conductor_radius < 1.0 < abs(offset_ratio) + conductor_radius:
        st.warning(
            "Ledningen skär randens område. Den enkla allt-eller-inget-modellen är då "
            "otillräcklig; den inneslutna strömdelen måste integreras över överlappet."
        )
        enclosed_text = "delvis innesluten"
        circulation_text = "kräver överlappsintegral"
    else:
        enclosed_text = f"{enclosed:.4g} A"
        circulation_text = f"{enclosed:.4g} A"
        if enclosed != 0:
            st.success("Strömmen är innesluten: ∮H·dl = I.")
        else:
            st.info("Ingen fri ström passerar ytan: cirkulationen är noll.")

    m1, m2, m3 = st.columns(3)
    m1.metric("Fri ström", f"{current:.4g} A")
    m2.metric("Innesluten ström", enclosed_text)
    m3.metric("Förväntad ∮H·dl", circulation_text)
    if loop_radius > 0 and isinstance(enclosed, float):
        h_value = enclosed / (2.0 * math.pi * loop_radius)
        b_value = MU0 * h_value
        st.caption(
            f"Vid full cylindrisk symmetri: H(R) = {h_value:.5g} A/m och "
            f"B(R) = {b_value:.5g} T."
        )


def _ampere_figure(radius: float, offset_ratio: float, conductor_ratio: float) -> go.Figure:
    angle = np.linspace(0.0, 2.0 * np.pi, 240)
    loop_x = radius * np.cos(angle)
    loop_y = radius * np.sin(angle)
    conductor_radius = conductor_ratio * radius
    conductor_x = offset_ratio * radius + conductor_radius * np.cos(angle)
    conductor_y = conductor_radius * np.sin(angle)

    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=loop_x,
            y=loop_y,
            mode="lines",
            line={"width": 4},
            name="Integrationsrand C",
        )
    )
    figure.add_trace(
        go.Scatter(
            x=conductor_x,
            y=conductor_y,
            mode="lines",
            fill="toself",
            opacity=0.45,
            name="Strömledare",
        )
    )
    figure.add_annotation(
        x=offset_ratio * radius,
        y=0.0,
        text="I ⊙",
        showarrow=False,
        font={"size": 18},
    )
    extent = 1.7 * radius
    figure.update_layout(
        height=500,
        margin={"l": 20, "r": 20, "t": 40, "b": 20},
        title="Ampereslinga och fri ström",
        xaxis={"range": [-extent, extent], "title": "x [m]", "scaleanchor": "y"},
        yaxis={"range": [-extent, extent], "title": "y [m]"},
        legend={"orientation": "h"},
    )
    return figure
