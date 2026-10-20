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
GAUSS_DEFAULT_CHARGES = {(0.0, 0.0): 5.0}


def _apply_plot_theme(*figures: go.Figure) -> None:
    """Apply one quiet, readable visual style to every theory figure."""
    for figure in figures:
        figure.update_layout(
            template="plotly_white",
            font={"family": "Arial, sans-serif", "size": 14, "color": "#24313b"},
            paper_bgcolor="#ffffff",
            plot_bgcolor="#ffffff",
            legend={
                "orientation": "h",
                "x": 0.5,
                "xanchor": "center",
                "y": -0.22,
                "yanchor": "top",
                "bgcolor": "rgba(255,255,255,0.88)",
            },
            margin={"l": 40, "r": 40, "b": 105, "t": 20},
            height=400,
            hoverlabel={
                "bgcolor": "#ffffff",
                "bordercolor": "#b8c4ce",
                "font": {"size": 13, "color": "#24313b"},
            },
            title_x=0.02,
            title_xanchor="left",
        )
        figure.update_xaxes(fixedrange=True, automargin=True, constrain="domain", tickangle=0)
        figure.update_yaxes(fixedrange=True, automargin=True, constrain="domain")
        if figure.layout.showlegend is False:
            figure.update_layout(margin={"b": 45})
            if figure.layout.xaxis.visible is False:
                figure.update_layout(height=300, margin={"l": 15, "r": 15})
        for trace in figure.data:
            colorbar = None
            if trace.type == "contour":
                colorbar = trace.colorbar
            elif trace.type == "scatter" and trace.marker.showscale:
                colorbar = trace.marker.colorbar
            if colorbar is not None:
                colorbar.update(orientation="h", x=0.5, xanchor="center",
                                y=1.02, yanchor="bottom", len=0.85,
                                thickness=10, title_side="top")
                figure.update_layout(margin={"t": 90})


def _render_plot(figure: go.Figure, **kwargs):
    """Render a responsive chart without shrinking text to fit a phone.

    Streamlit wraps the heading; Plotly retains fixed physical ranges. Disable
    2D drag gestures so a finger scrolls the page, while preserving point taps.
    """
    import streamlit as st

    figure = go.Figure(figure)  # Presentation must not mutate the model figure.
    if figure.layout.title.text:
        st.caption(figure.layout.title.text)
    figure.update_layout(title=None)
    kwargs.setdefault("use_container_width", True)
    return st.plotly_chart(
        figure, theme=None,
        config={"displayModeBar": False, "displaylogo": False,
                "scrollZoom": False, "responsive": True},
        **kwargs,
    )


def _render_problem_guide(instructions: str) -> None:
    """Keep multi-step problem advice available without pushing plots down."""
    import streamlit as st

    with st.expander("Så använder du modellen i en uppgift"):
        st.markdown(instructions)


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
        "satsen, men den hjälper ofta när man vill beräkna fältet direkt."
    )

    section = st.radio(
        "Välj del",
        ["Intuition", "Testlabb", "Beräkningsrecept"],
        horizontal=True,
        key="gauss_section",
    )
    # A centered point charge makes the symmetry behind Gauss' law visible
    # before the learner starts editing the model.
    example_charges = GAUSS_DEFAULT_CHARGES

    if section == "Intuition":
        left, right = st.columns(2)
        with left:
            st.markdown(
                "### Kärnidé\n"
                "En sluten yta fungerar som en kontrollvolym. Fält från yttre "
                "laddningar kan gå in och ut, medan nettoladdningen inuti avgör "
                "det totala flödet."
            )
        with right:
            st.info(
                "Ytans form ändrar det lokala flödet. Den inneslutna laddningen "
                "avgör ändå totalflödet: Φₑ = Q_in/ε₀."
            )
            st.warning(
                "Gauss sats innebär inte automatiskt att E är konstant på ytan. "
                "Det kräver lämplig symmetri."
            )
        _render_plot(
            _gauss_cross_section_figure(1.0, example_charges, True),
            key="gauss_intuition_figure",
        )
        st.caption(
            "En positiv laddning i origo. I testlabbet kan du klicka på rutnätet "
            "för att lägga till eller ta bort laddningar."
        )
        return

    if section == "Beräkningsrecept":
        st.markdown(
            "### Arbetsgång\n"
            "1. Välj en sluten Gaussyta som passar symmetrin i problemet.\n"
            "2. Summera nettoladdningen innanför ytan.\n"
            "3. Bestäm ytans utåtriktade normal.\n"
            "4. Utnyttja symmetri om den förenklar flödesintegralen.\n"
            "5. Kontrollera tecken, enheter och gränsfall."
        )
        st.latex(r"[\Phi_E]=\mathrm{N\,m^2/C}=\mathrm{V\,m}")
        _render_plot(
            _gauss_cross_section_figure(1.0, example_charges, True),
            key="gauss_recipe_figure",
        )
        return

    st.markdown("### Bygg en laddningsfördelning")
    st.info(
        "Startläget är +5 nC i origo. Välj värdet för en ny laddning och klicka "
        "på en rutnätspunkt för att lägga till den. Klicka på en befintlig "
        "laddning för att ta bort den. På pekskärm använder du koordinatkontrollerna nedan."
    )
    # Reset the old dipole default once for people with an existing Streamlit session.
    if st.session_state.get("gauss_model_version", 0) < 2:
        st.session_state.gauss_charges = example_charges.copy()
        st.session_state.gauss_model_version = 2
    if "gauss_chart_version" not in st.session_state:
        st.session_state.gauss_chart_version = 0

    c1, c2 = st.columns(2)
    with c1:
        radius = st.slider("Ytans radie R [m]", 0.5, 2.0, 1.0, 0.25, key="gauss_radius")
    with c2:
        charge_to_add = st.slider(
            "Ny laddning q [nC]", -10.0, 10.0, 5.0, 0.5,
            help="Tecknet och beloppet gäller laddningen som läggs till vid nästa klick.",
            key="gauss_new_charge",
        )
        show_normals = st.checkbox("Visa ytans normaler", value=False, key="gauss_normals")

    clear_col, reset_col = st.columns(2)
    with clear_col:
        if st.button("Töm rutnätet", key="gauss_clear_charges"):
            st.session_state.gauss_charges = {}
            st.session_state.gauss_chart_version += 1
            st.rerun()
    with reset_col:
        if st.button("Återställ startläget", key="gauss_reset_charges"):
            st.session_state.gauss_charges = example_charges.copy()
            st.session_state.gauss_chart_version += 1
            st.rerun()

    with st.expander("Placera med koordinater (mobil / tangentbord)", expanded=True):
        st.caption("Välj x och y i meter. Samma knapp tar bort en befintlig laddning.")
        x_col, y_col = st.columns(2)
        x = x_col.number_input("x [m]", -2.5, 2.5, 0.0, 0.25, key="gauss_x")
        y = y_col.number_input("y [m]", -2.5, 2.5, 0.0, 0.25, key="gauss_y")
        position = (round(x * 4) / 4, round(y * 4) / 4)
        occupied = position in st.session_state.gauss_charges
        label = "Ta bort laddning" if occupied else "Lägg till laddning"
        st.caption(f"Rutnätspunkt: ({position[0]:g}, {position[1]:g}) m")
        if st.button(label, key="gauss_coordinate_toggle", disabled=not occupied and charge_to_add == 0):
            st.session_state.gauss_charges = _toggle_gauss_charge(
                st.session_state.gauss_charges, position, charge_to_add
            )
            st.session_state.gauss_chart_version += 1
            st.rerun()

    charges = st.session_state.gauss_charges
    figure = _gauss_cross_section_figure(radius, charges, show_normals, show_grid=True)
    chart_key = f"gauss_charge_grid_{st.session_state.gauss_chart_version}"
    selection = _render_plot(
        figure,
        key=chart_key,
        on_select="rerun",
        selection_mode="points",
    )
    selected = _selection_points(selection)
    grid_index = _gauss_grid_index_from_selection(selected, len(figure.data) - 1)
    if grid_index is not None:
        charge_position = _gauss_grid_position(grid_index)
        st.session_state.gauss_charges = _toggle_gauss_charge(
            charges, charge_position, charge_to_add
        )
        st.session_state.gauss_chart_version += 1
        st.rerun()

    st.caption(
        "Med mus: klicka på en rutnätspunkt för att lägga till eller ta bort en laddning. "
        "På pekskärm: använd koordinaterna ovan; tryck i figuren visar punktinformation. "
        "Axlarna och färgskalan (±120 N/C) är fasta; färgen klipps utanför intervallet. "
        "Pilarna visar fältets riktning "
        "med komprimerad längdskala; färgen visar E·n på ytan. "
        "Rutnätet har 0,25 m mellan punkterna."
    )
    enclosed, on_surface = _gauss_enclosed_charge(radius, charges)
    total_charge = sum(charges.values())
    m1, m2, m3 = st.columns(3)
    m1.metric("Punktladdningar", str(len(charges)))
    m2.metric(
        "Q innesluten",
        "singulärt gränsfall" if on_surface else f"{enclosed:.4g} nC",
    )
    m3.metric(
        "Gauss förutsägelse Φₑ",
        "ej definierad" if on_surface else f"{enclosed * 1e-9 / EPS0:.4g} V·m",
    )
    if on_surface:
        st.warning(
            "En punktladdning ligger på Gaussytan. Fältet är singulärt där, så "
            "flödet genom ytan är inte definierat i denna idealisering. Flytta "
            "laddningen till en annan rutnätspunkt."
        )
    else:
        st.info(
            f"Summan av alla placerade laddningar är {total_charge:.4g} nC. "
            "Endast laddningarna innanför den sfäriska ytan bidrar till nettoflödet. "
            "Ytans form påverkar var flödet går, medan den inneslutna laddningen "
            "bestämmer totalflödet."
        )


def _selection_points(selection) -> list[dict]:
    """Read selected Plotly points across Streamlit's object and mapping forms."""
    if selection is None:
        return []
    try:
        selected = selection["selection"] if isinstance(selection, dict) else selection.selection
        points = selected["points"] if isinstance(selected, dict) else selected.points
    except (KeyError, AttributeError, TypeError):
        return []
    return list(points or [])


def _gauss_grid_index_from_selection(points, grid_trace_index: int) -> int | None:
    """Return the selected grid marker index, tolerating Plotly event variants."""
    for point in points:
        if not isinstance(point, dict):
            continue
        curve = point.get("curve_number", point.get("curveNumber"))
        if curve is not None:
            try:
                if int(curve) != grid_trace_index:
                    continue
            except (TypeError, ValueError):
                continue
        raw_index = point.get("point_index", point.get("point_number", point.get("pointNumber")))
        if raw_index is None and curve is not None:
            raw_index = point.get("customdata")
        # Plotly may serialize a point's customdata as a one-item sequence.
        if isinstance(raw_index, (list, tuple, np.ndarray)):
            if not len(raw_index):
                continue
            raw_index = raw_index[0]
        try:
            index = int(raw_index)
        except (TypeError, ValueError):
            continue
        if 0 <= index < 441:
            return index
    return None


def _gauss_grid_position(index: int) -> tuple[float, float]:
    """Map a row-major 21×21 plot point index to its displayed coordinates."""
    if not 0 <= index < 441:
        raise ValueError("Gauss grid index must be between 0 and 440")
    values = np.arange(-2.5, 2.5001, 0.25)
    return round(float(values[index % 21]), 2), round(float(values[index // 21]), 2)


def _toggle_gauss_charge(
    charges: dict[tuple[float, float], float],
    position: tuple[float, float],
    charge_to_add: float,
) -> dict[tuple[float, float], float]:
    """Remove an occupied grid point or add the selected charge at an empty one."""
    updated = charges.copy()
    if position in updated:
        del updated[position]
    elif charge_to_add != 0:
        updated[position] = float(charge_to_add)
    return updated


def _gauss_enclosed_charge(
    radius: float, charges: dict[tuple[float, float], float]
) -> tuple[float, bool]:
    """Return enclosed charge in nC and whether any point charge is on the surface."""
    tolerance = 1e-9
    enclosed = 0.0
    on_surface = False
    for (x, y), charge in charges.items():
        distance = math.hypot(x, y)
        on_surface |= math.isclose(distance, radius, rel_tol=0.0, abs_tol=tolerance)
        inside = distance < radius - tolerance
        if inside:
            enclosed += charge
    return enclosed, on_surface


def _electric_field_at(
    x: float, y: float, charges: dict[tuple[float, float], float]
) -> tuple[float, float]:
    k = 1.0 / (4.0 * math.pi * EPS0)
    ex = ey = 0.0
    for (charge_x, charge_y), charge_nc in charges.items():
        dx, dy = x - charge_x, y - charge_y
        r2 = dx * dx + dy * dy
        if r2 < 1e-12:
            continue
        scale = k * charge_nc * 1e-9 / (r2 * math.sqrt(r2))
        ex += scale * dx
        ey += scale * dy
    return ex, ey


def _gauss_cross_section_figure(
    radius: float,
    charges: dict[tuple[float, float], float],
    show_normals: bool,
    show_grid: bool = False,
) -> go.Figure:
    """Show E directions and E·n on a spherical Gaussian surface slice."""
    fig = go.Figure()
    grid_values = np.arange(-2.5, 2.5001, 0.25)
    grid_x, grid_y = np.meshgrid(grid_values, grid_values)
    flat_x, flat_y = grid_x.ravel(), grid_y.ravel()
    # Fixed axes and color limits keep the reference scale stable as the model changes.
    field_color_reference = 120.0  # N/C, fixed colorbar reference.
    arrow_x = np.arange(-2.25, 2.251, 0.5)
    arrow_y = np.arange(-2.0, 2.001, 0.5)
    arrow_length_max = 0.34
    for x in arrow_x:
        for y in arrow_y:
            ex, ey = _electric_field_at(float(x), float(y), charges)
            magnitude = math.hypot(ex, ey)
            if magnitude < 1e-9:
                continue
            # A compressed scale keeps weak far-field arrows visible while
            # preserving clear differences near the charges.
            length = 0.20 + 0.14 * min(magnitude / 220.0, 1.0)
            length = min(arrow_length_max, length)
            fig.add_annotation(
                x=x + length * ex / magnitude,
                y=y + length * ey / magnitude,
                ax=x, ay=y, xref="x", yref="y", axref="x", ayref="y",
                showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=1.3,
                arrowcolor="rgba(30,65,92,0.72)",
            )

    angle = np.linspace(0, 2 * np.pi, 240)
    boundary_x, boundary_y = radius * np.cos(angle), radius * np.sin(angle)
    fig.add_trace(go.Scatter(
        x=boundary_x, y=boundary_y, mode="lines", fill="toself",
        fillcolor="rgba(80,150,210,0.10)",
        line={"color": "#1f4e79", "width": 3}, name="Sfär (snitt)",
    ))
    sample_angle = np.linspace(0, 2 * np.pi, 40, endpoint=False)
    normal_x, normal_y = np.cos(sample_angle), np.sin(sample_angle)
    surface_x, surface_y = radius * normal_x, radius * normal_y

    normal_field = []
    for x, y, nx, ny in zip(surface_x, surface_y, normal_x, normal_y):
        if any(math.hypot(x - charge_x, y - charge_y) < 1e-9
               for charge_x, charge_y in charges):
            normal_field.append(float("nan"))
            continue
        ex, ey = _electric_field_at(float(x), float(y), charges)
        normal_field.append(ex * nx + ey * ny)
    fig.add_trace(go.Scatter(
        x=surface_x, y=surface_y, mode="markers",
        marker={
            "size": 6, "color": normal_field, "colorscale": "RdBu_r",
            "cmin": -field_color_reference, "cmax": field_color_reference, "cauto": False,
            "showscale": True,
            "colorbar": {
                "title": "E·n [N/C]", "tickvals": [-field_color_reference, 0, field_color_reference],
                "ticktext": ["−120", "0", "+120"], "thickness": 14,
            },
        },
        customdata=normal_field,
        hovertemplate="E·n = %{customdata:.3g} N/C<extra></extra>",
        name="Lokalt flöde E·n",
    ))
    if show_normals:
        normal_length = 0.14
        normal_angles = np.arange(8) * (2 * np.pi / 8) + np.pi / 8
        for angle in normal_angles:
            nx, ny = math.cos(angle), math.sin(angle)
            x, y = radius * nx, radius * ny
            fig.add_annotation(
                x=x + normal_length * nx, y=y + normal_length * ny,
                ax=x, ay=y, xref="x", yref="y", axref="x", ayref="y",
                showarrow=True, arrowhead=3, arrowsize=1, arrowwidth=1.2,
                arrowcolor="#c66a17",
            )

    if charges and not show_grid:
        charge_positions = list(charges)
        charge_values = [charges[pos] for pos in charge_positions]
        fig.add_trace(go.Scatter(
            x=[pos[0] for pos in charge_positions], y=[pos[1] for pos in charge_positions],
            mode="markers+text",
            marker={
                "size": 15,
                "color": ["#c0392b" if q > 0 else "#245b9e" if q < 0 else "#808080"
                          for q in charge_values],
                "symbol": ["circle" if q > 0 else "circle-open" if q < 0 else "x"
                           for q in charge_values],
                "line": {"width": 2},
            },
            text=[f"{q:+g} nC" for q in charge_values], textposition="top center",
            customdata=charge_values,
            hovertemplate="q = %{customdata:+.3g} nC<extra></extra>",
            name="Punktladdningar",
        ))
    if show_grid:
        # Draw the hit targets last so surface markers never intercept a click.
        grid_charge_values = [
            charges.get((round(float(x), 2), round(float(y), 2)))
            for x, y in zip(flat_x, flat_y)
        ]
        fig.add_trace(go.Scatter(
            x=flat_x, y=flat_y, mode="markers+text",
            text=["" if q is None else f"{q:+g} nC" for q in grid_charge_values],
            textposition="top center", customdata=np.arange(len(flat_x)),
            marker={
                "size": [4 if q is None else 16 for q in grid_charge_values],
                "color": [
                    "#75808a" if q is None else "#c0392b" if q > 0 else "#245b9e"
                    for q in grid_charge_values
                ],
                "symbol": [
                    "circle" if q is None or q > 0 else "circle-open"
                    for q in grid_charge_values
                ],
                "opacity": [0.3 if q is None else 1.0 for q in grid_charge_values],
                "line": {"width": 2},
            },
            hovertemplate=("(%{x:.2f}, %{y:.2f}) m<br>"
                           "Klicka för att lägga till/ta bort en laddning<extra></extra>"),
            showlegend=False, name="Laddningsrutnät",
        ))
    fig.update_layout(
        height=540,
        title="Fält och lokalt flöde på en sfärisk Gaussyta",
        xaxis={"range": [-3, 3], "tick0": -3, "dtick": 1, "title": "x [m]",
               "scaleanchor": "y", "constrain": "domain"},
        yaxis={"range": [-3, 3], "tick0": -3, "dtick": 1, "title": "y [m]"},
        margin={"l": 25, "r": 25, "t": 55, "b": 30},
        legend={"orientation": "h", "y": 1.02},
        clickmode="event+select",
        dragmode="pan" if show_grid else False,
        uirevision="gauss-fixed-axes",
    )
    _apply_plot_theme(fig)
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
        _render_plot(_ampere_figure(1.0, 0.0, 0.16, 1, 1.0))
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
        _render_plot(_ampere_figure(1.0, 0.0, 0.16, 1, 1.0))
        return

    st.markdown("### Ström genom en cirkulär ampereslinga")
    st.info("Förutsäg först tecknet på ∮H·dl när du vänder integrationsriktningen.")
    with st.expander("Inställningar", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            current = st.slider("Fri ström I [A]", -5.0, 5.0, 2.0, 0.25)
            loop_radius = st.slider("Slingradie R [m]", 0.5, 1.25, 1.0, 0.05)
        with c2:
            offset_ratio = st.slider(
                "Ledningens centrum x/R",
                -1.4,
                1.4,
                0.0,
                0.05,
                help="|x/R| < 1 placerar ledningen innanför integrationsytan.",
            )
            conductor_radius = st.slider("Ledningsradie a/R", 0.05, 0.35, 0.15, 0.01)
            orientation_label = st.radio("Orientering av C enligt högerhandsregeln",
                ["Moturs (+z-normal)", "Medurs (−z-normal)"], horizontal=True)
    orientation = 1 if orientation_label.startswith("Moturs") else -1
    figure = _ampere_figure(loop_radius, offset_ratio, conductor_radius, orientation, current)
    _render_plot(figure)
    st.caption(
        "Axlarna har fast skala. Slingradie och ledarens läge visas i meter; "
        "symbolen anger strömriktning och textstorleken följer |I|."
    )

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

    current_symbol = "⊙" if current > 0 else "⊗" if current < 0 else "0"
    normal_symbol = "⊙" if orientation > 0 else "⊗"
    figure.add_annotation(
        x=offset_ratio * radius,
        y=0.0,
        text=f"I={abs(current):g} A {current_symbol}<br>n {normal_symbol}",
        showarrow=False,
        font={"size": 12 + round(8 * min(abs(current), 5.0) / 5.0)},
        bgcolor="rgba(255,255,255,0.8)",
    )
    extent = 2.4
    figure.update_layout(
        height=500,
        margin={"l": 20, "r": 20, "t": 40, "b": 20},
        title="Randkurva, orientering och ström genom ytan",
        xaxis={"range": [-extent, extent], "title": "x [m]", "scaleanchor": "y"},
        yaxis={"range": [-extent, extent], "title": "y [m]"},
        legend={"orientation": "h"},
    )
    _apply_plot_theme(figure)
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
    _render_problem_guide(
        "1. Ställ in laddningarnas tecken, belopp och avstånd enligt uppgiften.\n"
        "2. Läs V från ekvipotentialerna eller använd profilen längs x-axeln.\n"
        "3. Använd Eₓ = −dV/dx: brantare lutning betyder starkare fält.\n"
        "4. Kontrollera riktningen med pilarna och laddningarnas tecken."
    )
    st.caption("Prova att vända tecknet på en laddning och följ hur fältet och potentialen ändras.")
    with st.expander("Inställningar", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            q1 = st.slider("Vänster laddning q₁ [nC]", -5.0, 5.0, 2.0, 0.5)
            q2 = st.slider("Höger laddning q₂ [nC]", -5.0, 5.0, -2.0, 0.5)
        with c2:
            separation = st.slider("Laddningsavstånd d [m]", 0.4, 2.0, 1.0, 0.1)
    field_figure, profile_figure = _potential_figures(q1, q2, separation)
    field_tab, profile_tab = st.tabs(["Fältkarta", "Profil längs x"])
    with field_tab:
        _render_plot(field_figure)
        st.caption(
            "Färgskalan är fast (±50 V); värden utanför intervallet mättas. "
            "Axlarna är fasta. Pilarna visar "
            "E = −∇V med komprimerad längdskala, så även svagare fält syns."
        )
    with profile_tab:
        _render_plot(profile_figure)
        st.caption("V och Eₓ har varsin fast skala; använd lutningen på V-kurvan för att kontrollera Eₓ.")


def _potential_figures(q1_nc: float, q2_nc: float, separation: float) -> tuple[go.Figure, go.Figure]:
    k = 1.0 / (4.0 * math.pi * EPS0)
    positions = (-0.5 * separation, 0.5 * separation)
    charges = (q1_nc * 1e-9, q2_nc * 1e-9)
    x = np.linspace(-3.0, 3.0, 121)
    y = np.linspace(-3.0, 3.0, 121)
    xx, yy = np.meshgrid(x, y)
    potential = np.zeros_like(xx)
    for charge, x0 in zip(charges, positions):
        if charge == 0:
            continue
        dx, dy = xx - x0, yy
        r2 = dx * dx + dy * dy
        safe = np.maximum(r2, 0.08**2)
        r = np.sqrt(safe)
        potential += k * charge / r
        potential[r2 < 0.08**2] = np.nan

    field = go.Figure()
    field.add_trace(go.Contour(
        x=x, y=y, z=potential, colorscale="RdBu_r", zmin=-50, zmax=50,
        autocontour=False,
        contours={"start": -50, "end": 50, "size": 5,
                  "coloring": "heatmap", "showlabels": False},
        colorbar={"title": "V [V]", "tickvals": [-50, 0, 50]},
        name="Ekvipotentialer",
    ))
    for gx in np.linspace(-2.5, 2.5, 9):
        for gy in np.linspace(-2.5, 2.5, 9):
            field_x = field_y = 0.0
            near_charge = False
            for charge, x0 in zip(charges, positions):
                if charge == 0:
                    continue
                dx, dy = gx - x0, gy
                r2 = dx * dx + dy * dy
                if r2 < 0.08**2:
                    near_charge = True
                    break
                field_scale = k * charge / (r2 * math.sqrt(r2))
                field_x += field_scale * dx
                field_y += field_scale * dy
            magnitude = math.hypot(field_x, field_y)
            if near_charge or magnitude == 0:
                continue
            length = 0.18 + 0.16 * min(magnitude / 300.0, 1.0)
            field.add_annotation(
                x=gx + length * field_x / magnitude,
                y=gy + length * field_y / magnitude,
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
        height=520, title="Ekvipotentialer och elektriskt fält i planet",
        xaxis={"range": [-3, 3], "dtick": 1, "title": "x [m]", "scaleanchor": "y"},
        yaxis={"range": [-3, 3], "dtick": 1, "title": "y [m]"},
        margin={"l": 20, "r": 25, "t": 55, "b": 20},
        uirevision="potential-fixed-reference",
    )

    line_x = np.linspace(-3.0, 3.0, 800)
    line_v = np.zeros_like(line_x)
    line_ex = np.zeros_like(line_x)
    for charge, x0 in zip(charges, positions):
        if charge == 0:
            continue
        dx = line_x - x0
        r = np.maximum(np.abs(dx), 0.08)
        line_v += k * charge / r
        line_ex += k * charge * dx / (r**3)
    for charge, x0 in zip(charges, positions):
        if charge == 0:
            continue
        line_v[np.abs(line_x - x0) < 0.08] = np.nan
        line_ex[np.abs(line_x - x0) < 0.08] = np.nan
    profile = go.Figure()
    profile.add_trace(go.Scatter(x=line_x, y=line_v, mode="lines", name="V(x, 0) [V]"))
    profile.add_trace(go.Scatter(
        x=line_x, y=line_ex, mode="lines", name="Eₓ(x, 0) [V/m]", yaxis="y2",
        line={"dash": "dash", "color": "#d77824"},
    ))
    profile.update_layout(
        height=370, title="Potentialens lutning längs x-axeln",
        xaxis={"range": [-3, 3], "dtick": 2, "title": "x [m]"},
        yaxis={"range": [-1000, 1000], "title": "V [V]"},
        yaxis2={"range": [-10000, 10000], "title": "Eₓ [V/m]", "overlaying": "y", "side": "right"},
        legend={"orientation": "h", "y": 1.12}, margin={"l": 20, "r": 45, "t": 60, "b": 30},
        uirevision="potential-profile-fixed-reference",
    )
    _apply_plot_theme(field, profile)
    return field, profile


def _render_dielectric_page() -> None:
    import streamlit as st

    st.title("Teori: Randvillkor mellan dielektrika")
    st.latex(r"E_{1t}=E_{2t} \qquad D_{2n}-D_{1n}=\sigma_{\mathrm f}")
    st.write(
        "Vid en plan gränsyta i elektrostatik är den tangentiella komponenten av E "
        "kontinuerlig. Språnget i D:s normalkomponent bestäms av den fria ytladdningen."
    )
    _render_problem_guide(
        "1. Dela upp E₁ i normal- och tangentialkomponenter med vinkeln.\n"
        "2. Sätt E₂t = E₁t.\n"
        "3. Beräkna E₂n från ε₀εᵣ₂E₂n − ε₀εᵣ₁E₁n = σf.\n"
        "4. Kombinera komponenterna för E₂. Om σf = 0 är D:s normalkomponent kontinuerlig."
    )
    st.caption("Ändra ett värde i taget och följ hur E₂:s normal- och tangentialdel reagerar.")
    with st.expander("Inställningar", expanded=False):
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
    _render_plot(_dielectric_figure(e1n, e1t, e2n, e2t, eps1, eps2))
    m1, m2, m3 = st.columns(3)
    m1.metric("E₁t", f"{e1t:.3g} kV/m")
    m2.metric("E₂t", f"{e2t:.3g} kV/m")
    m3.metric("E₂n", f"{e2n:.3g} kV/m")
    st.caption(
        "Normalen pekar från material 1 till 2. Pilarna visar riktningen med "
        "komprimerade, begränsade längder; läs fältstyrkan i siffrorna. "
        "Jämför E₁t och E₂t för kontinuitet och använd ε₀εᵣEₙ för D:s språng."
    )



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
    for x0, en, et, color, label in [(-0.8, e1n, e1t, "#1f77b4", "E₁"),
                                      (0.8, e2n, e2t, "#d95f02", "E₂")]:
        magnitude = math.hypot(en, et)
        length = min(0.65, 0.08 + 0.045 * magnitude) if magnitude else 0.0
        dx, dy = (length * en / magnitude, length * et / magnitude) if magnitude else (0.0, 0.0)
        fig.add_annotation(x=x0+dx, y=dy, ax=x0, ay=0, xref="x", yref="y",
            axref="x", ayref="y", showarrow=True, arrowhead=3, arrowsize=1,
            arrowwidth=3, arrowcolor=color)
        fig.add_annotation(x=x0, y=-0.65, text=f"{label}<br>{magnitude:.2g} kV/m", showarrow=False,
            font={"size": 16, "color": color})
    fig.add_annotation(x=-0.85, y=1.05, text=f"Material 1<br>εᵣ₁={eps1:g}", showarrow=False)
    fig.add_annotation(x=0.85, y=1.05, text=f"Material 2<br>εᵣ₂={eps2:g}", showarrow=False)
    fig.add_annotation(x=0.08, y=-1.15, text="n →", showarrow=False)
    fig.update_layout(height=420, title="Fältkomponenter vid en plan gränsyta",
        xaxis={"range": [-1.7, 1.7], "visible": False, "scaleanchor": "y"},
        yaxis={"range": [-1.35, 1.35], "visible": False},
        margin={"l": 10, "r": 10, "t": 50, "b": 10}, showlegend=False)
    _apply_plot_theme(fig)
    return fig


def _render_biot_savart_page() -> None:
    import streamlit as st

    st.title("Teori: Biot–Savarts lag")
    st.latex(r"d\mathbf{B}=\frac{\mu_0}{4\pi}\frac{I\,d\boldsymbol{\ell}\times\hat{\mathbf r}}{r^2}")
    st.write(
        "Varje strömelement bidrar med ett magnetfält. Bidragen adderas som vektorer; "
        "symmetri gör att många komponenter tar ut varandra."
    )
    _render_problem_guide(
        "1. Ställ in strömmens riktning, slingradie och observationspunkt.\n"
        "2. Använd högerhandsregeln för riktningen på B längs axeln.\n"
        "3. Jämför de 16 lika stora axialbidragen med summan Bᶻ(z).\n"
        "Modellen visar en tunn cirkulär ledare i vakuum; formeln gäller på axeln."
    )
    st.caption("Vänd strömmens tecken för att se hur alla bidrag och Bᶻ byter riktning.")
    with st.expander("Inställningar", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            current = st.slider("Ström I [A]", -5.0, 5.0, 3.0, 0.25)
            radius = st.slider("Loopradie a [m]", 0.5, 1.0, 0.75, 0.05)
        with c2:
            z = st.slider("Observationspunkt z [m]", -1.5, 1.5, 0.5, 0.05)
    geometry, contributions, profile = _biot_savart_figures(current, radius, z)
    m1, m2, m3 = st.columns(3)
    m1.metric("Bᶻ vid vald punkt", f"{_loop_axis_field(current, radius, z) * 1e6:.3g} µT")
    m2.metric("Bidrag från ett segment", f"{_loop_axis_field(current, radius, z) * 1e6 / 16:.3g} µT")
    m3.metric("Segment", "16")
    section_tab, geometry_tab, contributions_tab, profile_tab = st.tabs(
        ["Snitt", "3D", "Bidrag", "Axelfält"]
    )
    with section_tab:
        _render_plot(_biot_savart_section(current, radius, z))
        st.caption("Snitt genom xz-planet. ⊙ är ström ut ur skärmen (−y); ⊗ är ström in (+y). "
                   "B-pilen visar riktningen; läs storleken i mätvärdet ovan. "
                   "Krök högerhandens fingrar med strömmen: tummen visar B på axeln.")
    with geometry_tab:
        _render_plot(geometry)
        st.caption("Axlarna är fasta i meter. Följ den blå strömpilen och orange B-pil med högerhandsregeln.")
    with contributions_tab:
        _render_plot(contributions)
        st.caption("På loopens axel är alla 16 axialkomponenter lika stora; summan visas ovanför staplarna.")
    with profile_tab:
        _render_plot(profile)
        st.caption("Den orange markören är den valda punkten på den blå Bᶻ(z)-kurvan.")


def _loop_axis_field(current: float, radius: float, z: float) -> float:
    return MU0 * current * radius**2 / (2.0 * (radius**2 + z**2) ** 1.5)


def _biot_savart_section(current: float, radius: float, z: float) -> go.Figure:
    """Touch-friendly xz cross-section; +y points into the screen."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[-radius, radius], y=[0, 0], mode="markers+text",
        marker={"size": 18, "color": "#1f77b4"},
        text=["⊙" if current > 0 else "⊗" if current < 0 else "0",
              "⊗" if current > 0 else "⊙" if current < 0 else "0"],
        textfont={"color": "white", "size": 16}, textposition="middle center",
        name="Ledare", hovertemplate="Ledaren: x=%{x:.2f} m<extra></extra>"))
    fig.add_trace(go.Scatter(x=[0], y=[z], mode="markers+text",
        marker={"size": 10, "color": "#d95f02"}, text=["P"],
        textposition="middle right", name="Fältpunkt"))
    if current:
        fig.add_annotation(x=0, y=z + math.copysign(0.28, current), ax=0, ay=z,
            xref="x", yref="y", axref="x", ayref="y", showarrow=True,
            arrowhead=3, arrowwidth=3, arrowcolor="#d95f02")
    fig.update_layout(title="Slingans snitt och B-riktning", showlegend=False,
        xaxis={"range": [-1.3, 1.3], "title": "x [m]", "scaleanchor": "y", "dtick": 0.5},
        yaxis={"range": [-1.9, 1.9], "title": "z [m]", "dtick": 1})
    _apply_plot_theme(fig)
    return fig


def _biot_savart_figures(current: float, radius: float, z: float) -> tuple[go.Figure, go.Figure, go.Figure]:
    n = 16
    angle = np.linspace(0.0, 2.0*np.pi, n+1)
    loop = go.Figure()
    loop.add_trace(go.Scatter3d(x=radius*np.cos(angle), y=radius*np.sin(angle), z=np.zeros_like(angle),
        mode="lines", line={"color":"#1f77b4","width":6}, name="Strömslinga"))
    loop.add_trace(go.Scatter3d(x=[0], y=[0], z=[z], mode="markers+text",
        marker={"size":6,"color":"#d95f02"}, text=["P"], textposition="top center", name="Fältpunkt"))
    selected_field = abs(_loop_axis_field(current, radius, z))
    current_cone_size = 0.18 * radius * (0.15 + 0.85 * min(abs(current) / 5.0, 1.0))
    field_cone_size = 0.28 * radius * (0.15 + 0.85 * min(selected_field / 6.3e-6, 1.0))
    if current != 0:
        loop.add_trace(go.Cone(x=[radius],y=[0],z=[0],u=[0],v=[np.sign(current)],w=[0],
            sizemode="absolute",sizeref=current_cone_size,
            colorscale=[[0,"#1f77b4"],[1,"#1f77b4"]], showscale=False,name="I-riktning"))
        loop.add_trace(go.Cone(x=[0],y=[0],z=[z],u=[0],v=[0],w=[np.sign(current)],
            sizemode="absolute",sizeref=field_cone_size,
            colorscale=[[0,"#d95f02"],[1,"#d95f02"]], showscale=False,name="B på axeln"))
    loop.update_layout(height=470,title="Cirkulär slinga och fältpunkt på axeln",
        scene={"aspectmode":"data","xaxis":{"title":"x [m]","range":[-1.8,1.8]},
               "yaxis":{"title":"y [m]","range":[-1.8,1.8]},
               "zaxis":{"title":"z [m]","range":[-1.8,1.8]}},
        margin={"l":0,"r":0,"t":45,"b":0},uirevision="biot-geometry-fixed-reference")

    dphi=2.0*np.pi/n
    dBz=np.full(n,(MU0 / (4 * np.pi))*current*radius**2*dphi/(radius**2+z**2)**1.5)*1e6
    bars=go.Figure(go.Bar(x=np.arange(1,n+1),y=dBz,marker_color="#4c78a8",name="dBz"))
    bars.add_annotation(
        x=0.98, y=0.98, xref="paper", yref="paper", xanchor="right", yanchor="top",
        text=f"Σ dBz = {_loop_axis_field(current, radius, z) * 1e6:.3g} µT",
        showarrow=False, font={"color": "#d95f02"},
    )
    bars.update_layout(height=370,title="Axialt fältbidrag från varje segment",
        xaxis_title="Segment",yaxis={"title":"dBᶻ [µT]","range":[-0.5,0.5]},showlegend=False,
        margin={"l":20,"r":20,"t":50,"b":25})

    zz=np.linspace(-2.5,2.5,500)
    bz=np.array([_loop_axis_field(current,radius,value) for value in zz])*1e6
    profile=go.Figure(go.Scatter(x=zz,y=bz,mode="lines",line={"color":"#1f77b4","width":2},name="Bz(z)"))
    profile.add_trace(go.Scatter(x=[z],y=[_loop_axis_field(current,radius,z)*1e6],mode="markers",
        marker={"size":9,"color":"#d95f02"},name="Vald punkt"))
    profile.update_layout(height=370,title="Axialfält längs z-axeln",xaxis_title="z [m]",
        yaxis={"title":"Bᶻ [µT]","range":[-7,7]},
        xaxis={"title":"z [m]","range":[-2.5,2.5]},
        margin={"l":20,"r":15,"t":50,"b":25},uirevision="biot-fixed-reference")
    _apply_plot_theme(loop, bars, profile)
    return loop,bars,profile


def _render_faraday_page() -> None:
    import streamlit as st

    st.title("Teori: Faradays och Lenz lag")
    st.latex(r"\mathcal{E}=-N\frac{d\Phi_B}{dt} \qquad \Phi_B=BA\cos\theta")
    st.write(
        "En förändring av det magnetiska flödet ger en inducerad emk. Lenz lag anger "
        "att den inducerade strömmen skapar ett fält som motverkar förändringen av flödet."
    )
    _render_problem_guide(
        "1. Bestäm flödet Φ = BA cos θ genom ett varv.\n"
        "2. Beräkna emk = −N dΦ/dt.\n"
        "3. Emk-tecknet anger riktningen relativt spolens normal n.\n"
        "4. Lenz lag säger att det inducerade fältet motverkar **förändringen** "
        "av det signerade flödet: om dΦ/dt är positiv pekar det längs −n, "
        "vid negativ derivata längs +n och vid noll ingen inducerad emk. Detta gäller en sluten resistiv krets när självinduktion försummas."
    )
    st.caption("Här varierar B sinusformigt. När θ = 0 pekar spolens normal n längs +z.")
    with st.expander("Inställningar", expanded=False):
        c1,c2=st.columns(2)
        with c1:
            b0_mt=st.slider("Fältamplitud B₀ [mT]",0.1,20.0,20.0,0.1)
            frequency=st.slider("Frekvens f [Hz]",0.1,5.0,4.5,0.1)
        with c2:
            turns=st.slider("Varvtal N",1,500,450,1)
            area_cm2=st.slider("Spolarea A [cm²]",1.0,500.0,450.0,1.0)
            angle_deg=st.slider("Vinkel θ mellan B och spolnormal [°]",0,180,0,1)
    phase=st.slider("Tidpunkt t/T",0.0,1.0,0.1,0.005)
    b0=b0_mt*1e-3
    area=area_cm2*1e-4
    time=phase/frequency
    b, flux, emf = _faraday_state(b0, frequency, turns, area, time, angle_deg)
    graph,schematic=_faraday_figures(b0,frequency,turns,area,phase,angle_deg,emf)
    waveform_tab, direction_tab = st.tabs(["Tidskurvor", "Riktning"])
    with waveform_tab:
        _render_plot(graph)
        st.caption("Den streckade linjen visar vald tidpunkt; jämför B med emk och dess tecken.")
    m1,m2,m3=st.columns(3)
    m1.metric("Bext(t)",f"{b*1e3:.4g} mT")
    m2.metric("Flödeskoppling NΦ",f"{turns*flux:.4g} Wb-turn")
    m3.metric("Inducerad emk",f"{emf:.4g} V")
    with direction_tab:
        _render_plot(schematic)
        st.caption(f"Vald tid är t = {time:.4g} s. Emk-tecknet anger inducerat fält längs +n eller −n.")
    st.caption(
        "Fasta axlar: B mellan −22 och +22 mT, emk mellan −17 och +17 V. "
        "Vinkeln påverkar flödet genom faktorn cos θ."
    )



def _faraday_state(
    b0: float, frequency: float, turns: int, area: float, time: float,
    angle_deg: float = 0.0,
) -> tuple[float, float, float]:
    """Return applied B, flux per turn, and induced emf for B=B0 sin(2πft)."""
    omega = 2.0 * math.pi * frequency
    magnetic_field = b0 * math.sin(omega * time)
    normal_component = math.cos(math.radians(angle_deg))
    flux = magnetic_field * area * normal_component
    emf = -turns * area * omega * b0 * normal_component * math.cos(omega * time)
    return magnetic_field, flux, emf

def _faraday_figures(b0: float, frequency: float, turns: int, area: float,
                     selected_phase: float, angle_deg: float,
                     induced_emf: float) -> tuple[go.Figure, go.Figure]:
    phase=np.linspace(0.0,2.0,600)
    omega=2*np.pi*frequency
    b=b0*np.sin(2*np.pi*phase)
    emf=-turns*area*omega*b0*math.cos(math.radians(angle_deg))*np.cos(2*np.pi*phase)
    graph=go.Figure()
    graph.add_trace(go.Scatter(x=phase,y=b*1e3,mode="lines",name="Bext [mT]",line={"color":"#1f77b4"}))
    graph.add_trace(go.Scatter(x=phase,y=emf,mode="lines",name="Inducerad emk [V]",yaxis="y2",line={"color":"#d95f02"}))
    graph.add_vline(x=selected_phase,line_dash="dash",line_color="#333")
    graph.update_layout(height=470,title="Yttre fält och inducerad emk",xaxis={"title":"Tid t/T","range":[0,2],"dtick":0.5,"tickangle":0},
        yaxis={"title":"Bext [mT]","range":[-22,22]},
        yaxis2={"title":"emk [V]","range":[-17,17],"overlaying":"y","side":"right"},
        legend={"orientation":"h","y":1.12},margin={"l":45,"r":55,"t":60,"b":40},
        uirevision="faraday-fixed-reference")
    schematic=go.Figure()
    theta=np.linspace(0,2*np.pi,200)
    schematic.add_trace(go.Scatter(x=np.cos(theta),y=np.sin(theta),mode="lines",
        line={"width":4,"color":"#555"},name="Spole"))
    if abs(induced_emf) > 1e-12:
        induced_sign=np.sign(induced_emf)
        symbol="⊙" if induced_sign>0 else "⊗"
        label="Bind längs +n" if induced_sign>0 else "Bind längs −n"
        font_size=16
        schematic.add_annotation(x=0,y=0,text=f"{symbol}<br>{label}<br>|emk|={abs(induced_emf):.3g} V",
            showarrow=False,font={"size":font_size})
    else:
        schematic.add_annotation(x=0,y=0,text="emk = 0",showarrow=False,font={"size":17})
    schematic.update_layout(height=300,title="Inducerat fälts riktning relativt spolnormalen n",
        xaxis={"range":[-1.3,1.3],"visible":False,"scaleanchor":"y"},
        yaxis={"range":[-1.3,1.3],"visible":False},showlegend=False,
        margin={"l":10,"r":10,"t":45,"b":10})
    _apply_plot_theme(graph, schematic)
    return graph,schematic

