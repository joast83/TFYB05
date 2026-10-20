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
    TheoryPage(
        key="potential_field",
        title="Elektrisk potential och fält",
        short_description="Sambandet mellan potential, ekvipotentialer och elektriskt fält.",
    ),
    TheoryPage(
        key="dielectric_boundary",
        title="Randvillkor mellan dielektrika",
        short_description="Normal- och tangentialkomponenter vid en materialgräns.",
    ),
    TheoryPage(
        key="biot_savart",
        title="Biot–Savarts lag",
        short_description="Hur strömelement bidrar till magnetfältet och adderas vektoriellt.",
    ),
    TheoryPage(
        key="faraday_lenz",
        title="Faradays och Lenz lag",
        short_description="Hur förändrat magnetiskt flöde ger inducerad emk och ström.",
    ),
]

THEORY_PAGE_LOOKUP = {page.title: page for page in THEORY_PAGES}


def render_theory_page(page: TheoryPage) -> None:
    if page.key == "gauss_flux":
        _render_gauss_page()
    elif page.key == "stokes_magnetostatics":
        _render_stokes_page()
    elif page.key == "potential_field":
        _render_potential_page()
    elif page.key == "dielectric_boundary":
        _render_dielectric_page()
    elif page.key == "biot_savart":
        _render_biot_savart_page()
    elif page.key == "faraday_lenz":
        _render_faraday_page()
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


# The following pages use compact models with explicit assumptions.  Each page keeps
# the equations next to one visual that connects the geometry to the predicted result.

def _render_potential_page() -> None:
    import streamlit as st

    st.title("Teori: Elektrisk potential och fält")
    st.latex(r"\mathbf{E}=-\nabla V \qquad V=\sum_i \frac{1}{4\pi\varepsilon_0}\frac{q_i}{r_i}")
    st.write(
        "Potentialen är en skalär som summeras algebraisk. Fältet är en vektor och "
        "fås från potentialens lutning. E-fältet står vinkelrätt mot ekvipotentialerna."
    )
    st.info("Förutsäg först hur ekvipotentialerna ändras när tecknet på en av laddningarna vänds.")
    c1, c2 = st.columns(2)
    with c1:
        q1 = st.slider("Vänster laddning q₁ [nC]", -5.0, 5.0, 2.0, 0.5)
        q2 = st.slider("Höger laddning q₂ [nC]", -5.0, 5.0, -2.0, 0.5)
    with c2:
        separation = st.slider("Laddningsavstånd d [m]", 0.4, 2.0, 1.0, 0.1)
    field_figure, profile_figure = _potential_figures(q1, q2, separation)
    st.plotly_chart(field_figure, use_container_width=True, config={"displaylogo": False})
    st.caption("Pilarnas längder är normaliserade för läsbarhet; deras riktning visar E = −∇V.")
    st.plotly_chart(profile_figure, use_container_width=True, config={"displaylogo": False})


def _potential_figures(q1_nc: float, q2_nc: float, separation: float) -> tuple[go.Figure, go.Figure]:
    k = 1.0 / (4.0 * math.pi * EPS0)
    positions = (-0.5 * separation, 0.5 * separation)
    charges = (q1_nc * 1e-9, q2_nc * 1e-9)
    x = np.linspace(-1.5 * separation, 1.5 * separation, 81)
    y = np.linspace(-1.2 * separation, 1.2 * separation, 65)
    xx, yy = np.meshgrid(x, y)
    potential = np.zeros_like(xx)
    ex = np.zeros_like(xx)
    ey = np.zeros_like(xx)
    for charge, x0 in zip(charges, positions):
        dx, dy = xx - x0, yy
        r2 = dx * dx + dy * dy
        safe = np.maximum(r2, (0.035 * separation) ** 2)
        r = np.sqrt(safe)
        potential += k * charge / r
        ex += k * charge * dx / (safe * r)
        ey += k * charge * dy / (safe * r)
        potential[r2 < (0.035 * separation) ** 2] = np.nan

    field = go.Figure()
    field.add_trace(go.Contour(
        x=x, y=y, z=potential, colorscale="RdBu", zmid=0,
        contours={"coloring": "lines", "showlabels": True},
        colorbar={"title": "V [V]"}, name="Ekvipotentialer",
    ))
    for gx in np.linspace(-1.3 * separation, 1.3 * separation, 9):
        for gy in np.linspace(-1.0 * separation, 1.0 * separation, 7):
            ix = int(np.abs(x - gx).argmin())
            iy = int(np.abs(y - gy).argmin())
            magnitude = math.hypot(ex[iy, ix], ey[iy, ix])
            if not math.isfinite(magnitude) or magnitude == 0:
                continue
            length = 0.075 * separation
            field.add_annotation(
                x=gx + length * ex[iy, ix] / magnitude,
                y=gy + length * ey[iy, ix] / magnitude,
                ax=gx, ay=gy, xref="x", yref="y", axref="x", ayref="y",
                showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=1.2,
                arrowcolor="rgba(25,55,80,0.7)",
            )
    for charge, x0, label in zip(charges, positions, ("q₁", "q₂")):
        field.add_trace(go.Scatter(
            x=[x0], y=[0], mode="markers+text",
            marker={
                "size": 13,
                "color": "#888888" if charge == 0 else ("#b22222" if charge > 0 else "#245b9e"),
                "symbol": "x" if charge == 0 else ("circle" if charge > 0 else "circle-open"),
            },
            text=[label], textposition="top center", name=label,
        ))
    field.update_layout(
        height=560, title="Ekvipotentialer och elektriskt fält i planet",
        xaxis={"title": "x [m]", "scaleanchor": "y"}, yaxis={"title": "y [m]"},
        margin={"l": 20, "r": 25, "t": 55, "b": 20},
    )

    line_x = np.linspace(-1.5 * separation, 1.5 * separation, 500)
    line_v = np.zeros_like(line_x)
    line_ex = np.zeros_like(line_x)
    for charge, x0 in zip(charges, positions):
        dx = line_x - x0
        r = np.maximum(np.abs(dx), 0.025 * separation)
        line_v += k * charge / r
        line_ex += k * charge * dx / (r**3)
    profile = go.Figure()
    profile.add_trace(go.Scatter(x=line_x, y=line_v, mode="lines", name="V(x, 0) [V]"))
    profile.add_trace(go.Scatter(
        x=line_x, y=line_ex, mode="lines", name="Eₓ(x, 0) [V/m]", yaxis="y2",
        line={"dash": "dash", "color": "#d77824"},
    ))
    profile.update_layout(
        height=330, title="Potentialens lutning längs x-axeln",
        xaxis={"title": "x [m]"}, yaxis={"title": "V [V]"},
        yaxis2={"title": "Eₓ [V/m]", "overlaying": "y", "side": "right"},
        legend={"orientation": "h", "y": 1.12}, margin={"l": 20, "r": 45, "t": 60, "b": 30},
    )
    return field, profile


def _render_dielectric_page() -> None:
    import streamlit as st

    st.title("Teori: Randvillkor mellan dielektrika")
    st.latex(r"E_{1t}=E_{2t} \qquad D_{2n}-D_{1n}=\sigma_{\mathrm f}")
    st.write(
        "Vid en plan gränsyta i elektrostatik är den tangentiella komponenten av E "
        "kontinuerlig. Språnget i D:s normalkomponent bestäms av den fria ytladdningen."
    )
    st.info("Förutsäg hur E₂ ändras ifall εᵣ₂ ökar medan εᵣ₁, E₁ och σf hålls fasta.")
    c1, c2 = st.columns(2)
    with c1:
        eps1 = st.slider("Relativ permittivitet εᵣ₁", 1.0, 12.0, 2.0, 0.5)
        eps2 = st.slider("Relativ permittivitet εᵣ₂", 1.0, 12.0, 5.0, 0.5)
        e1_kvm = st.slider("Fält E₁ [kV/m]", 0.5, 10.0, 4.0, 0.5)
    with c2:
        angle_deg = st.slider("E₁-vinkel från normalen [°]", -75, 75, 35, 1)
        sigma_nc_m2 = st.slider("Fri ytladdning σf [nC/m²]", -50.0, 50.0, 0.0, 2.0)
    e1n, e1t, e2n, e2t = _dielectric_boundary_fields(
        eps1, eps2, e1_kvm, angle_deg, sigma_nc_m2
    )
    st.plotly_chart(_dielectric_figure(e1n, e1t, e2n, e2t, eps1, eps2),
        use_container_width=True, config={"displaylogo": False})
    m1, m2, m3 = st.columns(3)
    m1.metric("E₁t", f"{e1t:.3g} kV/m")
    m2.metric("E₂t", f"{e2t:.3g} kV/m")
    m3.metric("E₂n", f"{e2n:.3g} kV/m")
    st.caption("Normalen pekar från material 1 till material 2. E-pilarna är ritade med en gemensam skalfaktor.")



def _dielectric_boundary_fields(
    eps1: float, eps2: float, e1_kvm: float, angle_deg: float, sigma_nc_m2: float
) -> tuple[float, float, float, float]:
    """Return E1n, E1t, E2n, E2t in kV/m for a planar interface."""
    e1n = e1_kvm * math.cos(math.radians(angle_deg))
    e1t = e1_kvm * math.sin(math.radians(angle_deg))
    sigma = sigma_nc_m2 * 1e-9
    e2n = (EPS0 * eps1 * e1n * 1000 + sigma) / (EPS0 * eps2) / 1000
    return e1n, e1t, e2n, e1t

def _dielectric_figure(e1n: float, e1t: float, e2n: float, e2t: float,
                       eps1: float, eps2: float) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[0, 0], y=[-1.4, 1.4], mode="lines",
        line={"color": "#444", "width": 3}, name="Gränsyta"))
    maximum = max(math.hypot(e1n, e1t), math.hypot(e2n, e2t), 1e-9)
    scale = 1.0 / maximum
    for x0, en, et, color, label in [(-0.7, e1n, e1t, "#1f77b4", "E₁"),
                                      (0.7, e2n, e2t, "#d95f02", "E₂")]:
        dx, dy = en * scale, et * scale
        fig.add_annotation(x=x0+dx, y=dy, ax=x0, ay=0, xref="x", yref="y",
            axref="x", ayref="y", showarrow=True, arrowhead=3, arrowsize=1,
            arrowwidth=3, arrowcolor=color)
        fig.add_annotation(x=x0+dx, y=dy+0.12, text=label, showarrow=False,
            font={"size": 16, "color": color})
    fig.add_annotation(x=-1.25, y=1.05, text=f"Material 1<br>εᵣ₁={eps1:g}", showarrow=False)
    fig.add_annotation(x=1.25, y=1.05, text=f"Material 2<br>εᵣ₂={eps2:g}", showarrow=False)
    fig.add_annotation(x=0.08, y=-1.15, text="n →", showarrow=False)
    fig.update_layout(height=420, title="Fältkomponenter vid en plan gränsyta",
        xaxis={"range": [-1.7, 1.7], "visible": False, "scaleanchor": "y"},
        yaxis={"range": [-1.35, 1.35], "visible": False},
        margin={"l": 10, "r": 10, "t": 50, "b": 10}, showlegend=False)
    return fig


def _render_biot_savart_page() -> None:
    import streamlit as st

    st.title("Teori: Biot–Savarts lag")
    st.latex(r"d\mathbf{B}=\frac{\mu_0}{4\pi}\frac{I\,d\boldsymbol{\ell}\times\hat{\mathbf r}}{r^2}")
    st.write(
        "Varje strömelement bidrar med ett magnetfält. Bidragen adderas som vektorer; "
        "symmetri gör att många komponenter tar ut varandra."
    )
    st.info("Förutsäg riktningen på B längs loopens axel innan du ändrar strömmens riktning.")
    c1, c2 = st.columns(2)
    with c1:
        current = st.slider("Ström I [A]", -5.0, 5.0, 2.0, 0.25)
        radius = st.slider("Loopradie a [m]", 0.1, 1.0, 0.5, 0.05)
    with c2:
        z = st.slider("Observationspunkt z [m]", -1.5, 1.5, 0.5, 0.05)
    geometry, contributions, profile = _biot_savart_figures(current, radius, z)
    st.plotly_chart(geometry, use_container_width=True, config={"displaylogo": False})
    left, right = st.columns(2)
    with left:
        st.plotly_chart(contributions, use_container_width=True, config={"displaylogo": False})
    with right:
        st.metric("Bz på axeln", f"{_loop_axis_field(current, radius, z) * 1e6:.4g} µT")
        st.plotly_chart(profile, use_container_width=True, config={"displaylogo": False})
    st.caption("Slingan ligger i xy-planet; de visade segmentvisa dBz-bidragen summerar till det analytiska axelfältet.")


def _loop_axis_field(current: float, radius: float, z: float) -> float:
    return MU0 * current * radius**2 / (2.0 * (radius**2 + z**2) ** 1.5)


def _biot_savart_figures(current: float, radius: float, z: float) -> tuple[go.Figure, go.Figure, go.Figure]:
    n = 16
    angle = np.linspace(0.0, 2.0*np.pi, n+1)
    loop = go.Figure()
    loop.add_trace(go.Scatter3d(x=radius*np.cos(angle), y=radius*np.sin(angle), z=np.zeros_like(angle),
        mode="lines", line={"color":"#1f77b4","width":6}, name="Strömslinga"))
    loop.add_trace(go.Scatter3d(x=[0], y=[0], z=[z], mode="markers+text",
        marker={"size":6,"color":"#d95f02"}, text=["P"], textposition="top center", name="Fältpunkt"))
    if current != 0:
        loop.add_trace(go.Cone(x=[radius],y=[0],z=[0],u=[0],v=[np.sign(current)],w=[0],
            sizemode="absolute",sizeref=0.18*radius,showscale=False,name="I-riktning"))
        loop.add_trace(go.Cone(x=[0],y=[0],z=[z],u=[0],v=[0],w=[np.sign(current)],
            sizemode="absolute",sizeref=0.28*radius,showscale=False,name="B på axeln"))
    extent=max(1.3*radius,abs(z)+0.5*radius)
    loop.update_layout(height=450,title="Strömslinga och axial fältpunkt",
        scene={"aspectmode":"data","xaxis":{"title":"x [m]","range":[-extent,extent]},
               "yaxis":{"title":"y [m]","range":[-extent,extent]},
               "zaxis":{"title":"z [m]","range":[-extent,extent]}},
        margin={"l":0,"r":0,"t":45,"b":0})

    dphi=2.0*np.pi/n
    dBz=np.full(n,1e-7*current*radius**2*dphi/(radius**2+z**2)**1.5)*1e6
    bars=go.Figure(go.Bar(x=np.arange(1,n+1),y=dBz,marker_color="#4c78a8",name="dBz"))
    bars.add_hline(y=float(np.sum(dBz)),line_dash="dash",line_color="#d95f02",
        annotation_text=f"Summa = {np.sum(dBz):.3g} µT")
    bars.update_layout(height=330,title="Axialt bidrag från varje strömelement",
        xaxis_title="Strömelement",yaxis_title="dBz [µT]",showlegend=False,
        margin={"l":20,"r":20,"t":50,"b":25})

    zz=np.linspace(-2*radius,2*radius,300)
    bz=np.array([_loop_axis_field(current,radius,value) for value in zz])*1e6
    profile=go.Figure(go.Scatter(x=zz,y=bz,mode="lines",line={"color":"#1f77b4","width":2},name="Bz(z)"))
    profile.add_trace(go.Scatter(x=[z],y=[_loop_axis_field(current,radius,z)*1e6],mode="markers",
        marker={"size":9,"color":"#d95f02"},name="Vald punkt"))
    profile.update_layout(height=330,title="Magnetfält längs loopens axel",xaxis_title="z [m]",
        yaxis_title="Bz [µT]",margin={"l":20,"r":15,"t":50,"b":25})
    return loop,bars,profile


def _render_faraday_page() -> None:
    import streamlit as st

    st.title("Teori: Faradays och Lenz lag")
    st.latex(r"\mathcal{E}=-N\frac{d\Phi_B}{dt} \qquad \Phi_B=BA\cos\theta")
    st.write(
        "En förändring av det magnetiska flödet ger en inducerad emk. Lenz lag anger "
        "att den inducerade strömmen skapar ett fält som motverkar förändringen av flödet."
    )
    st.info("Förutsäg riktningen på det inducerade fältet: det motverkar B självt eller dess förändring?")
    c1,c2=st.columns(2)
    with c1:
        b0_mt=st.slider("Fältamplitud B₀ [mT]",0.1,20.0,5.0,0.1)
        frequency=st.slider("Frekvens f [Hz]",0.1,5.0,1.0,0.1)
    with c2:
        turns=st.slider("Varvtal N",1,500,100,1)
        area_cm2=st.slider("Spolarea A [cm²]",1.0,500.0,100.0,1.0)
    phase=st.slider("Tidpunkt t/T",0.0,1.0,0.125,0.005)
    b0=b0_mt*1e-3
    area=area_cm2*1e-4
    omega=2*np.pi*frequency
    time=phase/frequency
    b, flux, emf = _faraday_state(b0, frequency, turns, area, time)
    emf_scale = turns * area * 2.0 * math.pi * frequency * b0
    induced_sign = 0.0 if abs(emf) <= 1e-10 * emf_scale else float(np.sign(emf))
    graph,schematic=_faraday_figures(b0,frequency,turns,area,time,induced_sign)
    st.plotly_chart(graph,use_container_width=True,config={"displaylogo":False})
    m1,m2,m3=st.columns(3)
    m1.metric("Bext(t)",f"{b*1e3:.4g} mT")
    m2.metric("Flödeskoppling NΦ",f"{turns*flux:.4g} Wb-turn")
    m3.metric("Inducerad emk",f"{emf:.4g} V")
    st.plotly_chart(schematic,use_container_width=True,config={"displaylogo":False})
    st.caption("Spolens positiva normal är +z. Ekvationen visar att Bind följer −dBext/dt, även när Bext passerar noll.")



def _faraday_state(
    b0: float, frequency: float, turns: int, area: float, time: float
) -> tuple[float, float, float]:
    """Return applied B, flux per turn, and induced emf for B=B0 sin(2πft)."""
    omega = 2.0 * math.pi * frequency
    magnetic_field = b0 * math.sin(omega * time)
    flux = magnetic_field * area
    emf = -turns * area * omega * b0 * math.cos(omega * time)
    return magnetic_field, flux, emf

def _faraday_figures(b0: float, frequency: float, turns: int, area: float,
                     selected_time: float, induced_sign: float) -> tuple[go.Figure, go.Figure]:
    time=np.linspace(0.0,2.0/frequency,500)
    omega=2*np.pi*frequency
    b=b0*np.sin(omega*time)
    emf=-turns*area*omega*b0*np.cos(omega*time)
    graph=go.Figure()
    graph.add_trace(go.Scatter(x=time,y=b*1e3,mode="lines",name="Bext [mT]",line={"color":"#1f77b4"}))
    graph.add_trace(go.Scatter(x=time,y=emf,mode="lines",name="Inducerad emk [V]",yaxis="y2",line={"color":"#d95f02"}))
    graph.add_vline(x=selected_time,line_dash="dash",line_color="#333")
    graph.update_layout(height=400,title="Tidsvariation av fält och inducerad emk",xaxis_title="t [s]",
        yaxis={"title":"Bext [mT]"},yaxis2={"title":"emk [V]","overlaying":"y","side":"right"},
        legend={"orientation":"h","y":1.12},margin={"l":20,"r":45,"t":60,"b":30})
    schematic=go.Figure()
    theta=np.linspace(0,2*np.pi,200)
    schematic.add_trace(go.Scatter(x=np.cos(theta),y=np.sin(theta),mode="lines",
        line={"width":4,"color":"#555"},name="Spole"))
    if induced_sign:
        symbol="⊙" if induced_sign>0 else "⊗"
        label="Bind längs +z" if induced_sign>0 else "Bind längs −z"
        schematic.add_annotation(x=0,y=0,text=f"{symbol}<br>{label}",showarrow=False,font={"size":17})
    else:
        schematic.add_annotation(x=0,y=0,text="emk = 0",showarrow=False,font={"size":17})
    schematic.update_layout(height=300,title="Inducerat fälts riktning (normal +z)",
        xaxis={"range":[-1.3,1.3],"visible":False,"scaleanchor":"y"},
        yaxis={"range":[-1.3,1.3],"visible":False},showlegend=False,
        margin={"l":10,"r":10,"t":45,"b":10})
    return graph,schematic

