from __future__ import annotations

import math
from dataclasses import dataclass

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
        short_description="Hur elektriskt flöde genom en sluten yta bara beror på den inneslutna laddningen.",
    ),
    TheoryPage(
        key="stokes",
        title="Stokes sats",
        short_description="Hur cirkulation längs en rand hänger ihop med curl genom ytan som randen omsluter.",
    ),
]


THEORY_PAGE_LOOKUP = {page.title: page for page in THEORY_PAGES}


def render_theory_page(page: TheoryPage) -> None:
    import streamlit as st
    if page.key == "gauss_flux":
        _render_gauss_page()
    elif page.key == "stokes":
        _render_stokes_page()
    else:
        st.error("Okänd teorisida.")


# ---------------------------------------------------------------------------
# Gauss page
# ---------------------------------------------------------------------------


def _render_gauss_page() -> None:
    import streamlit as st
    st.title("Teori: Gauss flödessats")
    st.caption("En konceptsida som ska hjälpa studenter att se skillnaden mellan elektriskt fält lokalt och totalt flöde globalt.")

    with st.expander("Kort idé i en mening", expanded=True):
        st.latex(r"\oint_S \mathbf{E}\cdot d\mathbf{A} = \frac{Q_{\mathrm{innesluten}}}{\varepsilon_0}")
        st.markdown(
            "**Tolkning:** summera hur mycket fältet passerar ut genom varje liten bit av en **sluten yta**. "
            "Summan bryr sig bara om **nettouladdningen innanför ytan** — inte om ytan är stor, liten, rund eller tillplattad."
        )

    tab1, tab2, tab3 = st.tabs(["Översikt", "Interaktiv figur", "Hur använder man satsen?"])

    with tab1:
        left, right = st.columns([1.1, 1.0])
        with left:
            st.markdown(
                "### Vad studenten behöver se\n"
                "1. **Flöde är inte samma sak som fältstyrka.** Ett starkt lokalt fält betyder inte automatiskt stort totalt flöde.\n"
                "2. **Sluten yta krävs.** Gauss sats gäller för en helt omslutande yta.\n"
                "3. **Bara innesluten laddning räknas i totalen.** Yttre laddningar kan vrida och deformera fältet, men ändrar inte totalflödet.\n"
                "4. **Symmetri gör satsen användbar för beräkning.** När fältet är lika stort över stora delar av ytan kan integralen förenklas kraftigt."
            )
        with right:
            st.info(
                "**Bra tumregel:**\n\n"
                "- Fråga först: *Vilken laddning ligger innanför?*\n"
                "- Fråga sedan: *Finns symmetri nog för att göra E konstant på ytan?*\n"
                "- Om ja: använd Gauss sats för att lösa E.\n"
                "- Om nej: använd satsen för förståelse, kontroll eller kvalitativ tolkning."
            )
            st.warning(
                "**Vanlig missuppfattning:** \n"
                "En yttre laddning kan ge starka fältlinjer genom delar av ytan. Men lika mycket går då in som ut, så nettobidraget till totalflödet blir noll."
            )

    with tab2:
        st.markdown("### Utforska en sluten Gaussyta")
        c1, c2, c3 = st.columns(3)
        with c1:
            surface_shape = st.selectbox("Ytans form", ["Sfär", "Ellipsoid"], key="gauss_surface_shape")
            q_inside_nc = st.slider("Inre laddning q_in [nC]", min_value=-10.0, max_value=10.0, value=5.0, step=0.5)
        with c2:
            q_outside_nc = st.slider("Yttre laddning q_ut [nC]", min_value=-10.0, max_value=10.0, value=0.0, step=0.5)
            surface_size = st.slider("Karakteristisk ytstorlek [m]", min_value=0.8, max_value=2.0, value=1.2, step=0.1)
        with c3:
            external_distance = st.slider("Yttre laddningens avstånd [m]", min_value=2.0, max_value=4.0, value=2.6, step=0.1)
            show_normals = st.checkbox("Visa ytans normaler", value=False, key="gauss_normals")

        fig = _gauss_figure(
            surface_shape=surface_shape,
            size=surface_size,
            q_inside_nc=q_inside_nc,
            q_outside_nc=q_outside_nc,
            external_distance=external_distance,
            show_normals=show_normals,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False})

        q_inside_c = q_inside_nc * 1e-9
        q_outside_c = q_outside_nc * 1e-9
        flux_total = q_inside_c / EPS0
        stokes_cols = st.columns(4)
        stokes_cols[0].metric("Innesluten laddning", f"{q_inside_nc:.1f} nC")
        stokes_cols[1].metric("Yttre laddning", f"{q_outside_nc:.1f} nC")
        stokes_cols[2].metric("Förväntat totalflöde", _fmt_eng(flux_total, "V·m"))
        stokes_cols[3].metric("Bidrag från yttre laddning till totalflödet", "0")

        if abs(q_outside_c) > 1e-18:
            st.info(
                "Även när den yttre laddningen slås på förvrängs fältlinjerna nära den sidan av ytan. "
                "Det syns i figuren, men totalflödet bestäms fortfarande enbart av q_in."
            )

        st.markdown(
            "#### Så läser du figuren\n"
            "- **Blå/röd punkt** visar negativ/positiv laddning.\n"
            "- Den genomskinliga kroppen är din **Gaussyta**.\n"
            "- Pilarna visar det lokala elektriska fältet i rummet.\n"
            "- Om du ökar ytstorleken ser du att fältet blir svagare längre ut, men ytan blir samtidigt större. Det är därför totalflödet kan vara oförändrat."
        )

    with tab3:
        st.markdown(
            "### När Gauss sats är extra kraftfull\n"
            "Använd den helst när symmetrin gör att fältet är lätt att beskriva på ytan:\n\n"
            "- **Sfärisk symmetri** → punktladdning, laddat klot, sfärskal.\n"
            "- **Cylindrisk symmetri** → oändlig linjeladdning, koaxial geometri.\n"
            "- **Plan symmetri** → oändligt plan, stora parallellplattor."
        )
        st.success(
            "**Tre-stegsrecept**\n\n"
            "1. Välj en sluten yta som följer symmetrin.\n"
            "2. Bestäm vilken laddning som ligger innanför ytan.\n"
            "3. Skriv flödesintegralen så enkelt som möjligt, ofta som E·A eller 2EA."
        )
        st.markdown(
            "### Kontrollfrågor till studenten\n"
            "- Om du dubblerar sfärens radie runt samma punktladdning — vad händer med flödet?\n"
            "- Vad händer om du flyttar en extra laddning utanför ytan?\n"
            "- Varför är det svårt att använda satsen direkt för en laddning som ligger utanför centrum i en slumpmässig sluten yta?"
        )


# ---------------------------------------------------------------------------
# Stokes page
# ---------------------------------------------------------------------------


def _render_stokes_page() -> None:
    import streamlit as st
    st.title("Teori: Stokes sats")
    st.caption("En konceptsida som kopplar samman lokal rotation i ett vektorfält med cirkulation längs randkurvan.")

    with st.expander("Kort idé i en mening", expanded=True):
        st.latex(r"\oint_C \mathbf{F}\cdot d\mathbf{l} = \iint_S (\nabla \times \mathbf{F})\cdot \hat{\mathbf{n}}\, dS")
        st.markdown(
            "**Tolkning:** det du får om du går ett varv runt randen och summerar fältets tangentiella bidrag, "
            "är samma sak som den totala mängden **rotation (curl)** som passerar genom ytan innanför randen."
        )

    tab1, tab2, tab3 = st.tabs(["Översikt", "Interaktiv figur", "Hur använder man satsen?"])

    with tab1:
        lcol, rcol = st.columns([1.05, 1.0])
        with lcol:
            st.markdown(
                "### Intuition\n"
                "Tänk att små paddelhjul ligger utspridda i fältet:\n"
                "- Om hjulet vill börja snurra finns **curl**.\n"
                "- Om många sådana små rotationer pekar genom en yta får du ett totalt bidrag genom ytan.\n"
                "- Det totala bidraget måste balansera mot vad du mäter när du går runt yttre kanten."
            )
        with rcol:
            st.info(
                "**Bra tumregel:**\n\n"
                "- **Randintegral** = vad fältet gör *längs kanten*.\n"
                "- **Ytintegral av curl** = hur mycket fältet *virvlar genom ytan*.\n"
                "- Samma rand kan ha många olika ytor, men båda sidor ger ändå samma värde — så länge randen är densamma och fältet är välbeteende."
            )
            st.warning(
                "**Vanlig missuppfattning:**\n"
                "Ett stort fält betyder inte automatiskt stor cirkulation. Det är den tangentiella komponenten längs randen, och den lokala rotationen (curl), som avgör."
            )

    with tab2:
        st.markdown("### Utforska rand och yta")
        c1, c2, c3 = st.columns(3)
        with c1:
            field_name = st.selectbox(
                "Vektorfält",
                [
                    "Roterande fält F = (-ωy, ωx, 0)",
                    "Virvelfritt gradientfält F = (x, y, 0)",
                ],
                key="stokes_field",
            )
            omega = st.slider("Skalfaktor ω", min_value=0.5, max_value=2.5, value=1.0, step=0.1)
        with c2:
            radius = st.slider("Randens radie R [m]", min_value=0.5, max_value=2.0, value=1.1, step=0.1)
            tilt_deg = st.slider("Ytans lutning [grader]", min_value=0, max_value=80, value=25, step=5)
        with c3:
            show_boundary_tangent = st.checkbox("Visa tangentvektorer längs randen", value=True, key="stokes_tangent")
            show_curl = st.checkbox("Visa curl-vektorer genom ytan", value=True, key="stokes_curl")

        fig, circulation, curl_flux, narrative = _stokes_figure(
            field_name=field_name,
            omega=omega,
            radius=radius,
            tilt_deg=tilt_deg,
            show_boundary_tangent=show_boundary_tangent,
            show_curl=show_curl,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False})

        cols = st.columns(3)
        cols[0].metric("Cirkulation ∮ F·dl", _fmt_eng(circulation, ""))
        cols[1].metric("Curl-flöde ∬ (∇×F)·n dS", _fmt_eng(curl_flux, ""))
        cols[2].metric("Skillnad", f"{abs(circulation - curl_flux):.2e}")

        st.info(narrative)
        st.markdown(
            "#### Så läser du figuren\n"
            "- Den **genomskinliga skivan** är ytan S.\n"
            "- Den **mörka cirkeln** är randkurvan C.\n"
            "- **Blå pilar** visar vektorfältet på ytan.\n"
            "- **Orange pilar** längs kanten visar tangentens orientering runt randen.\n"
            "- **Gröna pilar** genom ytan visar curlens riktning och storlek."
        )

    with tab3:
        st.markdown(
            "### När Stokes sats är extra användbar\n"
            "- När randintegralen är jobbig men curlen är enkel.\n"
            "- När du vill byta mellan **lokal rotation** och **global cirkulation**.\n"
            "- När du arbetar med Ampères lag eller vill förstå varför ett fält orsakar virvling runt en slinga."
        )
        st.success(
            "**Tre-stegsrecept**\n\n"
            "1. Identifiera randkurvan C och välj en yta S med samma rand.\n"
            "2. Beräkna eller tolka curl = ∇×F.\n"
            "3. Jämför randintegralen med ytintegralen av curl genom ytan."
        )
        st.markdown(
            "### Kontrollfrågor till studenten\n"
            "- Vad händer med båda sidor om du lutar ytan mer i det roterande fältet?\n"
            "- Varför blir båda sidor noll för gradientfältet?\n"
            "- Varför spelar randens orientering roll för tecknet?"
        )


# ---------------------------------------------------------------------------
# 3D figure helpers
# ---------------------------------------------------------------------------


def _gauss_figure(surface_shape: str, size: float, q_inside_nc: float, q_outside_nc: float, external_distance: float, show_normals: bool) -> go.Figure:
    q_inside = q_inside_nc * 1e-9
    q_outside = q_outside_nc * 1e-9
    inside_pos = np.array([0.0, 0.0, 0.0])
    outside_pos = np.array([external_distance, 0.3 * size, 0.0])

    if surface_shape == "Sfär":
        a, b, c = size, size, size
    else:
        a, b, c = 1.35 * size, 0.95 * size, 0.70 * size

    theta = np.linspace(0.0, np.pi, 36)
    phi = np.linspace(0.0, 2 * np.pi, 64)
    TH, PH = np.meshgrid(theta, phi)
    X = a * np.sin(TH) * np.cos(PH)
    Y = b * np.sin(TH) * np.sin(PH)
    Z = c * np.cos(TH)

    fig = go.Figure()
    fig.add_trace(
        go.Surface(
            x=X,
            y=Y,
            z=Z,
            opacity=0.22,
            surfacecolor=np.zeros_like(X),
            colorscale=[[0.0, "#7aa6ff"], [1.0, "#7aa6ff"]],
            showscale=False,
            hoverinfo="skip",
            name="Gaussyta",
        )
    )

    normals_x = X / max(a, 1e-12)
    normals_y = Y / max(b, 1e-12)
    normals_z = Z / max(c, 1e-12)
    normal_len = np.sqrt(normals_x**2 + normals_y**2 + normals_z**2)
    normals_x /= normal_len
    normals_y /= normal_len
    normals_z /= normal_len

    # Sample field arrows in a sparse grid around the surface.
    xs = np.linspace(-1.6 * a, 1.6 * a, 6)
    ys = np.linspace(-1.6 * b, 1.6 * b, 6)
    zs = np.linspace(-1.4 * c, 1.4 * c, 5)
    pts = np.array(np.meshgrid(xs, ys, zs, indexing="ij")).reshape(3, -1).T
    mask = np.linalg.norm(pts / np.array([a, b, c]), axis=1) < 0.82
    pts = pts[~mask]

    E = _point_charge_field(pts, q_inside, inside_pos) + _point_charge_field(pts, q_outside, outside_pos)
    E_mag = np.linalg.norm(E, axis=1)
    keep = np.isfinite(E_mag) & (E_mag > 1e-30)
    pts = pts[keep]
    E = E[keep]
    E_mag = E_mag[keep]
    if pts.shape[0] > 90:
        idx = np.linspace(0, pts.shape[0] - 1, 90).astype(int)
        pts = pts[idx]
        E = E[idx]
        E_mag = E_mag[idx]
    if E_mag.size:
        E_dir = E / E_mag[:, None]
        arrow_scale = 0.35 * size
        fig.add_trace(
            go.Cone(
                x=pts[:, 0], y=pts[:, 1], z=pts[:, 2],
                u=E_dir[:, 0], v=E_dir[:, 1], w=E_dir[:, 2],
                sizemode="absolute",
                sizeref=max(arrow_scale * 0.55, 1e-6),
                anchor="tail",
                colorscale="Blues",
                showscale=False,
                name="E-fält",
                hovertemplate="E-riktning<extra></extra>",
            )
        )

    if show_normals:
        step_phi = slice(None, None, 8)
        step_theta = slice(4, -4, 8)
        Xs = X[step_phi, step_theta].ravel()
        Ys = Y[step_phi, step_theta].ravel()
        Zs = Z[step_phi, step_theta].ravel()
        NX = normals_x[step_phi, step_theta].ravel()
        NY = normals_y[step_phi, step_theta].ravel()
        NZ = normals_z[step_phi, step_theta].ravel()
        fig.add_trace(
            go.Cone(
                x=Xs, y=Ys, z=Zs,
                u=NX, v=NY, w=NZ,
                sizemode="absolute",
                sizeref=max(size * 0.28, 1e-6),
                anchor="tail",
                colorscale=[[0.0, "#4caf50"], [1.0, "#4caf50"]],
                showscale=False,
                name="Normaler",
                hoverinfo="skip",
            )
        )

    if abs(q_inside) > 1e-18:
        fig.add_trace(go.Scatter3d(
            x=[inside_pos[0]], y=[inside_pos[1]], z=[inside_pos[2]],
            mode="markers+text",
            marker=dict(size=8, color="#d62728" if q_inside > 0 else "#1f77b4"),
            text=["q_in"], textposition="top center",
            name="Inre laddning",
            hovertemplate=f"q_in={q_inside_nc:.1f} nC<extra></extra>",
        ))

    if abs(q_outside) > 1e-18:
        fig.add_trace(go.Scatter3d(
            x=[outside_pos[0]], y=[outside_pos[1]], z=[outside_pos[2]],
            mode="markers+text",
            marker=dict(size=8, color="#d62728" if q_outside > 0 else "#1f77b4"),
            text=["q_ut"], textposition="top center",
            name="Yttre laddning",
            hovertemplate=f"q_ut={q_outside_nc:.1f} nC<extra></extra>",
        ))

    lim = max(external_distance + 0.6, 1.8 * size)
    fig.update_layout(
        scene=dict(
            xaxis=dict(title="x [m]", range=[-1.8 * lim, 1.8 * lim]),
            yaxis=dict(title="y [m]", range=[-1.4 * lim, 1.4 * lim]),
            zaxis=dict(title="z [m]", range=[-1.4 * lim, 1.4 * lim]),
            aspectmode="cube",
            camera=dict(eye=dict(x=1.55, y=1.35, z=1.05)),
        ),
        margin=dict(l=0, r=0, t=40, b=0),
        height=650,
        title=dict(text="Elektriskt flöde genom en sluten yta", x=0.02),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )
    return fig


def _stokes_figure(field_name: str, omega: float, radius: float, tilt_deg: float, show_boundary_tangent: bool, show_curl: bool):
    tilt = math.radians(tilt_deg)
    ex = np.array([1.0, 0.0, 0.0])
    e1 = ex
    e2 = np.array([0.0, math.cos(tilt), math.sin(tilt)])
    n = np.cross(e1, e2)
    n = n / np.linalg.norm(n)

    # Disk surface in the tilted plane.
    r = np.linspace(0.0, radius, 26)
    phi = np.linspace(0.0, 2 * math.pi, 72)
    R, PHI = np.meshgrid(r, phi)
    pts = np.outer((R * np.cos(PHI)).ravel(), e1) + np.outer((R * np.sin(PHI)).ravel(), e2)
    X = pts[:, 0].reshape(R.shape)
    Y = pts[:, 1].reshape(R.shape)
    Z = pts[:, 2].reshape(R.shape)

    boundary_phi = np.linspace(0.0, 2 * math.pi, 160)
    boundary = np.outer(radius * np.cos(boundary_phi), e1) + np.outer(radius * np.sin(boundary_phi), e2)
    tangent = np.outer(-radius * np.sin(boundary_phi), e1) + np.outer(radius * np.cos(boundary_phi), e2)
    tangent = tangent / np.linalg.norm(tangent, axis=1)[:, None]

    if field_name.startswith("Roterande"):
        def F(p):
            return np.column_stack((-omega * p[:, 1], omega * p[:, 0], np.zeros(len(p))))
        curl = np.array([0.0, 0.0, 2 * omega])
        circulation = 2 * omega * math.cos(tilt) * math.pi * radius**2
        narrative = (
            "Här skapar fältet en tydlig virvel runt z-axeln. När du lutar ytan minskar den del av curl som går genom ytan, "
            "och därför minskar både randintegralen och ytintegralen lika mycket."
        )
    else:
        def F(p):
            return np.column_stack((p[:, 0], p[:, 1], np.zeros(len(p))))
        curl = np.array([0.0, 0.0, 0.0])
        circulation = 0.0
        narrative = (
            "Detta är ett gradientfält. Små paddelhjul vill inte snurra, alltså är curl = 0. Därför blir även cirkulationen runt den slutna randen noll."
        )

    curl_flux = float(np.dot(curl, n) * math.pi * radius**2)

    fig = go.Figure()
    fig.add_trace(go.Surface(
        x=X, y=Y, z=Z,
        opacity=0.28,
        surfacecolor=np.zeros_like(X),
        colorscale=[[0.0, "#8fd19e"], [1.0, "#8fd19e"]],
        showscale=False,
        hoverinfo="skip",
        name="Yta S",
    ))
    fig.add_trace(go.Scatter3d(
        x=boundary[:, 0], y=boundary[:, 1], z=boundary[:, 2],
        mode="lines",
        line=dict(color="#222222", width=7),
        name="Rand C",
        hovertemplate="Rand C<extra></extra>",
    ))

    # Vector field arrows on the surface.
    rr = np.linspace(0.15 * radius, 0.9 * radius, 4)
    pp = np.linspace(0.0, 2 * math.pi, 12, endpoint=False)
    sample = np.array([rho * math.cos(ph) * e1 + rho * math.sin(ph) * e2 for rho in rr for ph in pp])
    field = F(sample)
    mag = np.linalg.norm(field, axis=1)
    keep = mag > 1e-12
    sample = sample[keep]
    field = field[keep]
    mag = mag[keep]
    if sample.size:
        field_dir = field / np.maximum(mag[:, None], 1e-12)
        fig.add_trace(go.Cone(
            x=sample[:, 0], y=sample[:, 1], z=sample[:, 2],
            u=field_dir[:, 0], v=field_dir[:, 1], w=field_dir[:, 2],
            anchor="tail", sizemode="absolute", sizeref=max(radius * 0.18, 1e-6),
            colorscale=[[0.0, "#3b82f6"], [1.0, "#3b82f6"]], showscale=False,
            name="Fält F",
            hoverinfo="skip",
        ))

    if show_boundary_tangent:
        idx = np.arange(0, len(boundary_phi) - 1, 20)
        fig.add_trace(go.Cone(
            x=boundary[idx, 0], y=boundary[idx, 1], z=boundary[idx, 2],
            u=tangent[idx, 0], v=tangent[idx, 1], w=tangent[idx, 2],
            anchor="tail", sizemode="absolute", sizeref=max(radius * 0.15, 1e-6),
            colorscale=[[0.0, "#f59e0b"], [1.0, "#f59e0b"]], showscale=False,
            name="Tangent längs C",
            hoverinfo="skip",
        ))

    if show_curl and np.linalg.norm(curl) > 1e-12:
        centers = np.array([0.35 * radius * math.cos(ph) * e1 + 0.35 * radius * math.sin(ph) * e2 for ph in np.linspace(0, 2*math.pi, 6, endpoint=False)])
        curl_dir = np.tile(curl / np.linalg.norm(curl), (len(centers), 1))
        fig.add_trace(go.Cone(
            x=centers[:, 0], y=centers[:, 1], z=centers[:, 2],
            u=curl_dir[:, 0], v=curl_dir[:, 1], w=curl_dir[:, 2],
            anchor="tail", sizemode="absolute", sizeref=max(radius * 0.18, 1e-6),
            colorscale=[[0.0, "#22c55e"], [1.0, "#22c55e"]], showscale=False,
            name="Curl",
            hovertemplate=f"curl = ({curl[0]:.2f}, {curl[1]:.2f}, {curl[2]:.2f})<extra></extra>",
        ))

    lim = 1.45 * radius
    fig.update_layout(
        scene=dict(
            xaxis=dict(title="x", range=[-lim, lim]),
            yaxis=dict(title="y", range=[-lim, lim]),
            zaxis=dict(title="z", range=[-lim, lim]),
            aspectmode="cube",
            camera=dict(eye=dict(x=1.55, y=1.30, z=1.15)),
        ),
        margin=dict(l=0, r=0, t=40, b=0),
        height=650,
        title=dict(text="Randcirkulation och curl genom en yta", x=0.02),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )
    return fig, circulation, curl_flux, narrative


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def _point_charge_field(points: np.ndarray, q: float, pos: np.ndarray) -> np.ndarray:
    if abs(q) < 1e-30:
        return np.zeros_like(points)
    r = points - pos[None, :]
    dist = np.linalg.norm(r, axis=1)
    safe = np.maximum(dist, 0.18)
    return (q / (4 * math.pi * EPS0)) * r / safe[:, None]**3


def _fmt_eng(value: float, unit: str) -> str:
    try:
        value = float(value)
    except Exception:
        return f"{value} {unit}".strip()
    if not math.isfinite(value):
        return f"{value} {unit}".strip()
    abs_value = abs(value)
    if abs_value == 0:
        text = "0"
    elif 1e-3 <= abs_value < 1e4:
        text = f"{value:.4g}"
    else:
        exponent = int(math.floor(math.log10(abs_value)))
        mantissa = value / 10**exponent
        text = f"{mantissa:.3g}×10^{exponent}"
    return f"{text} {unit}".strip()
