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
        st.plotly_chart(
            _gauss_cross_section_figure(1.0, 0.35, True, 1.0),
            use_container_width=True,
            config={"displaylogo": False},
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
        st.plotly_chart(
            _gauss_cross_section_figure(1.0, 0.35, True, 1.0),
            use_container_width=True,
            config={"displaylogo": False},
        )
        return

    st.markdown("### Flytta en punktladdning genom en sfär")
    st.info("Förutsäg först: blir det lokala flödet lika stort över hela ytan när laddningen flyttas?")
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
        show_vectors = st.checkbox("Visa ytans normalpilar", value=True)

    figure = _gauss_cross_section_figure(radius, position_ratio, show_vectors, q_nc)
    st.plotly_chart(figure, use_container_width=True, config={"displaylogo": False})
    st.caption(
        "2D-snitt av det tredimensionella fältet. Markörerna visar tecken och "
        "relativ storlek på E·n lokalt; totalflödet bestäms av innesluten laddning."
    )

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




def _gauss_cross_section_figure(radius: float, position_ratio: float, show_normals: bool, charge_nc: float = 1.0) -> go.Figure:
    """Qualitative 2D slice: field direction and relative local E dot n."""
    qsign=float(np.sign(charge_nc)); qx=position_ratio*radius; fig=go.Figure()
    if qsign:
        for x in np.linspace(-1.45*radius,1.45*radius,9):
            for y in np.linspace(-1.45*radius,1.45*radius,9):
                dx,dy=x-qx,y; r=math.hypot(dx,dy)
                if r<.16*radius: continue
                length=.095*radius
                fig.add_annotation(x=x+length*qsign*dx/r,y=y+length*qsign*dy/r,ax=x,ay=y,
                    xref="x",yref="y",axref="x",ayref="y",showarrow=True,arrowhead=2,
                    arrowsize=1,arrowwidth=1.2,arrowcolor="rgba(35,87,125,0.55)")
    a=np.linspace(0,2*np.pi,240)
    fig.add_trace(go.Scatter(x=radius*np.cos(a),y=radius*np.sin(a),mode="lines",
        line={"color":"#1f4e79","width":3},name="Gaussyta (snitt)"))
    a=np.linspace(0,2*np.pi,32,endpoint=False)
    px,py=radius*np.cos(a),radius*np.sin(a); dx,dy=px-qx,py; r2=dx*dx+dy*dy
    en=np.full_like(r2,np.nan,dtype=float); ok=r2>1e-14*radius*radius
    en[ok]=qsign*(dx[ok]*np.cos(a[ok])+dy[ok]*np.sin(a[ok]))/(r2[ok]**1.5)
    fig.add_trace(go.Scatter(x=px,y=py,mode="markers",
        marker={"size":9,"color":en,"colorscale":"RdBu","cmid":0,"showscale":True,
                "colorbar":{"title":"E·n<br>(relativt)","thickness":12}},
        customdata=en,hovertemplate="E·n (relativt) = %{customdata:.3g}<extra></extra>",
        name="Lokalt E·n på ytan"))
    if show_normals:
        for t in np.linspace(0,2*np.pi,12,endpoint=False):
            x0,y0=radius*np.cos(t),radius*np.sin(t); length=.18*radius
            fig.add_annotation(x=x0+length*np.cos(t),y=y0+length*np.sin(t),ax=x0,ay=y0,
                xref="x",yref="y",axref="x",ayref="y",showarrow=True,arrowhead=3,
                arrowsize=1,arrowwidth=1.4,arrowcolor="#c66a17")
    fig.add_trace(go.Scatter(x=[qx],y=[0],mode="markers+text",
        marker={"size":13,"color":"#b22222"},text=["q"],textposition="top center",
        name="Punktladdning"))
    e=1.65*radius
    fig.update_layout(height=540,margin={"l":25,"r":25,"t":45,"b":25},
        title="Elektriskt fält och Gaussyta: 2D-snitt",
        xaxis={"range":[-e,e],"title":"x [m]","scaleanchor":"y"},
        yaxis={"range":[-e,e],"title":"y [m]"},legend={"orientation":"h","y":-0.15})
    return fig


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
        st.markdown("### Randens riktning bestämmer tecknet")
        st.plotly_chart(_ampere_figure(1.0, 0.0, 0.16, 1, 1.0),
            use_container_width=True, config={"displaylogo": False})
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
        st.caption("Kontrollera att randens orientering och ytans normal följer högerhandsregeln.")
        st.plotly_chart(_ampere_figure(1.0, 0.0, 0.16, 1, 1.0),
            use_container_width=True, config={"displaylogo": False})
        return

    st.markdown("### Ström genom en cirkulär ampereslinga")
    st.info("Förutsäg först tecknet på ∮H·dl när du vänder integrationsriktningen.")
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
        orientation_label = st.radio("Orientering av C enligt högerhandsregeln",
            ["Moturs (+z-normal)", "Medurs (−z-normal)"], horizontal=True)
    orientation = 1 if orientation_label.startswith("Moturs") else -1
    figure = _ampere_figure(loop_radius, offset_ratio, conductor_radius, orientation, current)
    st.plotly_chart(figure, use_container_width=True, config={"displaylogo": False})

    fraction = _circle_overlap_fraction(
        loop_radius,
        abs(offset_ratio) * loop_radius,
        conductor_radius * loop_radius,
    )
    enclosed = current*fraction*orientation
    if 1e-8 < fraction < 1-1e-8:
        st.info(
            f"Delvis innesluten ledare ({fraction:.1%}). Vid jämn strömtäthet "
            f"blir I_innesluten = {enclosed:.4g} A."
        )
    elif fraction >= 1-1e-8:
        st.success("Hela strömmen passerar ytan: ∮H·dl = I, med tecken enligt orienteringen.")
    else:
        st.info("Ingen fri ström passerar ytan: cirkulationen är noll.")
    m1,m2,m3=st.columns(3)
    m1.metric("Fri ström I",f"{current:.4g} A")
    m2.metric("Innesluten ström (tecken)",f"{enclosed:.4g} A")
    m3.metric("Förväntad ∮H·dl",f"{enclosed:.4g} A")
    if abs(offset_ratio)<1e-10 and fraction>=1-1e-8:
        h=current/(2*math.pi*loop_radius)
        st.caption(
            f"För centrerad cirkelsymmetri: H(R) = {h:.5g} A/m och "
            f"B(R) = {MU0 * h:.5g} T. För en förskjuten slinga är H inte "
            "konstant längs C, trots att cirkulationen fortfarande bestäms "
            "av innesluten ström."
        )



def _circle_overlap_fraction(
    loop_radius: float, center_distance: float, conductor_radius: float
) -> float:
    """Fraction of uniformly distributed wire current inside the Amperian circle."""
    loop_r = loop_radius
    wire_r = conductor_radius
    distance = center_distance

    if distance >= loop_r + wire_r:
        return 0.0
    if distance <= abs(loop_r - wire_r):
        return (loop_r / wire_r) ** 2 if loop_r < wire_r else 1.0

    radicand = max(
        0.0,
        (-distance + loop_r + wire_r)
        * (distance + loop_r - wire_r)
        * (distance - loop_r + wire_r)
        * (distance + loop_r + wire_r),
    )
    loop_angle = math.acos(
        max(-1.0, min(1.0, (distance**2 + loop_r**2 - wire_r**2) / (2 * distance * loop_r)))
    )
    wire_angle = math.acos(
        max(-1.0, min(1.0, (distance**2 + wire_r**2 - loop_r**2) / (2 * distance * wire_r)))
    )
    overlap_area = (
        loop_r**2 * loop_angle
        + wire_r**2 * wire_angle
        - 0.5 * math.sqrt(radicand)
    )
    return max(0.0, min(1.0, overlap_area / (math.pi * wire_r**2)))


def _ampere_figure(
    radius: float,
    offset_ratio: float,
    conductor_ratio: float,
    orientation: int = 1,
    current: float = 1.0,
) -> go.Figure:
    angle = np.linspace(0.0, 2.0 * np.pi, 240)
    loop_x = radius * np.cos(angle)
    loop_y = radius * np.sin(angle)
    conductor_radius = conductor_ratio * radius
    wire_x = offset_ratio * radius + conductor_radius * np.cos(angle)
    wire_y = conductor_radius * np.sin(angle)

    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=loop_x,
            y=loop_y,
            mode="lines",
            line={"width": 4, "color": "#1f4e79"},
            name="Integrationsrand C",
        )
    )
    figure.add_trace(
        go.Scatter(
            x=wire_x,
            y=wire_y,
            mode="lines",
            fill="toself",
            fillcolor="rgba(224,126,40,0.28)",
            line={"color": "#d77824", "width": 2},
            name="Ledarens tvärsnitt",
        )
    )

    for angle_at in (0.45, 2.0, 3.55, 5.1):
        x0 = radius * np.cos(angle_at)
        y0 = radius * np.sin(angle_at)
        arrow_length = 0.16 * radius
        figure.add_annotation(
            x=x0 - arrow_length * np.sin(angle_at) * orientation,
            y=y0 + arrow_length * np.cos(angle_at) * orientation,
            ax=x0,
            ay=y0,
            xref="x",
            yref="y",
            axref="x",
            ayref="y",
            showarrow=True,
            arrowhead=3,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="#245b35",
        )

    current_symbol = "⊙" if current >= 0 else "⊗"
    normal_symbol = "⊙" if orientation > 0 else "⊗"
    figure.add_annotation(
        x=offset_ratio * radius,
        y=0.0,
        text=f"I {current_symbol}<br>n {normal_symbol}",
        showarrow=False,
        font={"size": 15},
        bgcolor="rgba(255,255,255,0.8)",
    )
    extent = 1.7 * radius
    figure.update_layout(
        height=500,
        margin={"l": 20, "r": 20, "t": 40, "b": 20},
        title="Randkurva, orientering och ström genom ytan",
        xaxis={"range": [-extent, extent], "title": "x [m]", "scaleanchor": "y"},
        yaxis={"range": [-extent, extent], "title": "y [m]"},
        legend={"orientation": "h"},
    )
    return figure
