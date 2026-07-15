"""Visualiseringsprogram för elektromagnetism — interaktiv Tkinter/Matplotlib-app.

Varje uppgift är en subklass av ProblemBase. Lägg till nya uppgifter genom att skapa
en subklass till ProblemBase i rätt kapitelmodul under problems/ (t.ex. problems/ch06.py
för kapitel 6) och lägga in en instans i PROBLEMS-listan i registry.py.

Layout: [2-D-graf] [geometriskiss] [3-D-vy]
3-D-vyn är en roterbar Axes3D-panel vars innehåll väljs uppgiftsvis för bästa fysikaliska översikt:
  - Axialsymmetriska uppgifter → rotationsyta färgsatt efter fält/potential
  - Skikt/kondensatorer       → 3-D-tvärsnitt med skuggade lager och fältpilar
  - Ändlig linjeladdning      → 3-D-quiverfält i xz-planet utsträckt i y-led
  - Design-/stapeldiagram     → 3-D-parameterstudie
"""
import math
import numpy as np
from matplotlib import colormaps
from matplotlib.cm import ScalarMappable
from matplotlib.colors import LogNorm, Normalize, SymLogNorm
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, Ellipse, Rectangle
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from .parameters import (
    ParameterSpec,
    ValidationIssue,
    normalize_parameter_specs,
    validate_parameter_values,
)
EPS0 = 8.854187817e-12
MU0 = 4e-07 * math.pi

def _surface_of_revolution(ax3d, r_vals, z_vals, scalar_vals, n_phi=60, title='', zlabel='', cmap='plasma'):
    """
    Roterar kurvan (r_vals, z_vals) kring z-axeln och färgsätter med scalar_vals.
    """
    phi = np.linspace(0, 2 * np.pi, n_phi)
    R, PHI = np.meshgrid(r_vals, phi)
    Z = np.tile(z_vals, (n_phi, 1))
    S = np.tile(scalar_vals, (n_phi, 1))
    X = R * np.cos(PHI)
    Y = R * np.sin(PHI)
    finite = S[np.isfinite(S)]
    if finite.size == 0:
        vmin, vmax = 0.0, 1.0
    else:
        vmin, vmax = float(np.nanmin(finite)), float(np.nanmax(finite))
        if not np.isfinite(vmin) or not np.isfinite(vmax) or vmax <= vmin:
            vmax = vmin + 1.0
    norm = Normalize(vmin=vmin, vmax=vmax)
    fc = colormaps[cmap](norm(S))
    if getattr(ax3d, 'plotly_bridge', False):
        ax3d.plot_surface(
            X, Y, Z, surfacecolor=S, cmap=cmap, cmin=vmin, cmax=vmax,
            rstride=1, cstride=1, antialiased=False, shade=False
        )
    else:
        ax3d.plot_surface(X, Y, Z, facecolors=fc, rstride=1, cstride=1, antialiased=False, shade=False)
    ax3d.set_xlabel('x [m]')
    ax3d.set_ylabel('y [m]')
    ax3d.set_zlabel(zlabel)
    ax3d.set_title(title)
    sm = ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    ax3d.get_figure().colorbar(sm, ax=ax3d, shrink=0.5, pad=0.1)

def _draw_box(ax, x0, x1, y0, y1, z0, z1, color, alpha):
    """Ritar ett enfärgat rätblock med Poly3DCollection."""
    verts = [[(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)], [(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], [(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)], [(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], [(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)], [(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)]]
    poly = Poly3DCollection(verts, alpha=alpha, facecolor=color, edgecolor='grey', linewidth=0.5)
    ax.add_collection3d(poly)

def _finite_values(values, *, positive_only=False):
    """Returnerar finita, omaskerade värden ur vanliga arrayer eller masked arrays."""
    arr = np.ma.masked_invalid(values)
    vals = arr.compressed() if np.ma.isMaskedArray(arr) else np.asarray(arr, dtype=float).ravel()
    vals = vals[np.isfinite(vals)]
    if positive_only:
        vals = vals[vals > 0]
    return vals


def _robust_limits(values, *, positive_only=False, lower=1.0, upper=99.0):
    """Percentilbaserade gränser som inte domineras av singulariteter eller enstaka extremvärden."""
    vals = _finite_values(values, positive_only=positive_only)
    if vals.size == 0:
        return None
    if vals.size < 4:
        return (float(np.min(vals)), float(np.max(vals)))
    lo, hi = np.nanpercentile(vals, [lower, upper])
    if not np.isfinite(lo) or not np.isfinite(hi) or hi <= lo:
        lo, hi = float(np.min(vals)), float(np.max(vals))
    if hi <= lo:
        hi = lo + 1.0
    return (float(lo), float(hi))


def _positive_lognorm(values, floor_fraction=0.001, floor_abs=1e-18, robust=True):
    """Logaritmisk färgnormalisering för icke-negativa skalarfält."""
    positive = _finite_values(values, positive_only=True)
    if positive.size == 0:
        return LogNorm(vmin=1.0, vmax=10.0)
    if robust:
        limits = _robust_limits(values, positive_only=True, lower=1.0, upper=99.5)
        vmin_data, vmax = limits if limits is not None else (float(np.min(positive)), float(np.max(positive)))
    else:
        vmin_data, vmax = float(np.min(positive)), float(np.max(positive))
    vmin = max(vmin_data, vmax * floor_fraction, floor_abs)
    if not np.isfinite(vmax) or vmax <= vmin:
        vmax = max(vmin * 10.0, 10.0)
    return LogNorm(vmin=vmin, vmax=vmax)


def _signed_symlognorm(values, linthresh_fraction=0.001, linscale=1.0, floor_abs=1e-18, robust=True):
    """Symmetrisk logaritmisk normalisering för fält som kan byta tecken."""
    finite = _finite_values(values)
    if finite.size == 0:
        return Normalize(vmin=-1.0, vmax=1.0)
    abs_vals = np.abs(finite)
    vmax = float(np.nanpercentile(abs_vals, 99.5)) if robust and abs_vals.size >= 4 else float(np.max(abs_vals))
    if not np.isfinite(vmax) or vmax <= floor_abs:
        return Normalize(vmin=-1.0, vmax=1.0)
    linthresh = max(vmax * linthresh_fraction, floor_abs)
    return SymLogNorm(linthresh=linthresh, linscale=linscale, vmin=-vmax, vmax=vmax, base=10)


def _show_scalar_map(ax, fig, X, Y, data, *, title, xlabel, ylabel, cbar_label, cmap='plasma', scale='linear', mask=None, contours=False, contour_levels=14, robust=True, equal_aspect=True):
    """Ritar en 2-D-skalarfältkarta med valbar linjär/log/symlog-skala.

    Färggränserna är percentilbaserade som standard. Det gör att punktladdningar,
    trådar och andra matematiska singulariteter inte trycker ihop nästan hela
    färgskalan till en enda färg.
    """
    arr = np.ma.masked_invalid(data).astype(float)
    if mask is not None:
        arr = np.ma.array(arr, mask=np.asarray(mask, dtype=bool) | np.ma.getmaskarray(arr))
    if scale == 'log':
        norm = _positive_lognorm(arr, robust=robust)
    elif scale == 'symlog':
        norm = _signed_symlognorm(arr, robust=robust)
    else:
        limits = _robust_limits(arr, lower=1.0, upper=99.0) if robust else None
        finite = _finite_values(arr)
        if finite.size == 0:
            norm = Normalize(vmin=0.0, vmax=1.0)
        else:
            vmin, vmax = limits if limits is not None else (float(np.nanmin(finite)), float(np.nanmax(finite)))
            if not np.isfinite(vmin) or not np.isfinite(vmax) or vmax <= vmin:
                vmax = vmin + 1.0
            norm = Normalize(vmin=vmin, vmax=vmax)
    cmap_obj = colormaps[cmap].copy() if isinstance(cmap, str) else cmap
    try:
        cmap_obj.set_bad(alpha=0.0)
    except Exception:
        pass
    im = ax.imshow(arr, extent=[np.min(X), np.max(X), np.min(Y), np.max(Y)], origin='lower', aspect='auto', cmap=cmap_obj, norm=norm)
    fig.colorbar(im, ax=ax).set_label(cbar_label)
    if contours:
        try:
            contour_data = np.ma.array(np.asarray(data, dtype=float), mask=np.ma.getmaskarray(arr))
            contour_vals = _finite_values(contour_data, positive_only=(scale == 'log'))
            if contour_vals.size > 2:
                if scale == 'log':
                    lo, hi = _robust_limits(contour_data, positive_only=True, lower=5.0, upper=95.0)
                    levels = np.geomspace(max(lo, 1e-300), hi, contour_levels)
                else:
                    lo, hi = _robust_limits(contour_data, lower=5.0, upper=95.0)
                    levels = np.linspace(lo, hi, contour_levels)
                ax.contour(X, Y, contour_data, levels=levels, colors='white', linewidths=0.4, alpha=0.45)
        except Exception:
            pass
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if equal_aspect:
        try:
            ax.set_aspect('equal', adjustable='box')
        except Exception:
            pass
    ax.grid(True, alpha=0.15)
    return im


def _overlay_vector_field(ax, X, Y, U, V, *, mask=None, max_arrows=23, color='white', alpha=0.78, min_rel_magnitude=1e-4):
    """Lägger normaliserade riktningspilar ovanpå en 2-D-karta."""
    X = np.asarray(X)
    Y = np.asarray(Y)
    U = np.asarray(U, dtype=float)
    V = np.asarray(V, dtype=float)
    mag = np.sqrt(U ** 2 + V ** 2)
    valid = np.isfinite(mag) & np.isfinite(U) & np.isfinite(V)
    if mask is not None:
        valid &= ~np.asarray(mask, dtype=bool)
    finite_mag = mag[valid]
    if finite_mag.size == 0:
        return None
    threshold = max(float(np.nanmax(finite_mag)) * min_rel_magnitude, 1e-300)
    valid &= mag >= threshold
    step = max(1, int(math.ceil(max(X.shape) / max_arrows)))
    valid_s = valid[::step, ::step]
    if not np.any(valid_s):
        return None
    mag_safe = np.where(mag == 0, 1.0, mag)
    Us = np.ma.array(U / mag_safe, mask=~valid)[::step, ::step]
    Vs = np.ma.array(V / mag_safe, mask=~valid)[::step, ::step]
    return ax.quiver(X[::step, ::step], Y[::step, ::step], Us, Vs, pivot='mid', color=color, alpha=alpha, linewidth=0.35, width=0.0032)


def _radial_slice_grid(rmax, n=220):
    x = np.linspace(-rmax, rmax, n)
    z = np.linspace(-rmax, rmax, n)
    X, Z = np.meshgrid(x, z)
    R = np.sqrt(X ** 2 + Z ** 2)
    return (X, Z, R)


MODE_HELP_TEXT = {
    'Field': 'Fältläge: fokuserar på den elektriska eller magnetiska fältstorheten.',
    'Potential': 'Potentialläge: visar potential, spänning eller en motsvarande integrerad storhet.',
    'D': 'D-läge: visar elektrisk flödestäthet eller en närliggande materialstorhet.',
    'Magnitude': 'Resultatläge: visar belopp, dimensioneringsresultat eller härledd storhet.',
    'Map': 'Kartläge: visar ett tvådimensionellt snitt eller en parameterstudie.',
}

CHAPTER_NOTES = {
    '2': 'Elektrostatik i vakuum eller luft: bygg upp E från Coulombs lag eller använd Gauss lag när symmetrin tillåter det. Potentialen fås genom linjeintegral av fältet eller direkt laddningsintegral.',
    '3': 'Dielektriska material: skilj på E, D och polarisation. Randvillkoren för normal/tangentiell komponent och seriekopplade fältskikt är ofta den viktigaste idén.',
    '4': 'Energi, kraft och spegelladdning: kraft kan ofta fås från energimetoden eller från fälttryck. Vid ledande plan ersätts randvillkoret ofta med en lämplig spegelladdning.',
    '5': 'Stationära strömmar: använd J = σE, I = ∫J·dS och kontinuitet. Potentialen spelar samma matematiska roll som i elektrostatiken, men med konduktivitet i stället för permittivitet.',
    '6': 'Biot–Savarts lag: summera bidrag från strömelement. Symmetri avgör riktningen och visualiseringen visar oftast B-fältets belopp eller riktning.',
    '7': 'Magnetiska krafter, moment och flöden: använd dF = I dℓ × B, m = IA n̂ och Φ = ∫B·dS. För stora avstånd jämförs ofta exakt fält med dipolapproximation.',
    '8': 'Magnetiska material och kretsar: håll isär B, H och M. I magnetkretsar motsvarar magnetomotorisk spänning, reluktans och flöde ungefär spänning, resistans och ström.',
    '9': 'Induktans och induktion: flödeskoppling ger L och M, och inducerad ems följer av Faradays lag ε = −dΦ/dt. Tecknet visar motverkan enligt Lenz lag.',
    '10': 'Förskjutningsström: Maxwells korrektion gör Ampères lag konsistent även när E-fältet varierar i tiden, exempelvis i kondensatorgap.',
}

SPECIFIC_NOTES = {
    'ChargedSpheresSmallAngle': 'Kärnidé: de två laddade kulorna är i statisk jämvikt. Småvinkelapproximationen ger α = (Q²/(2π ε0 m g ℓ²))^(1/3). Figuren visar hur vinkeln växer med |Q|.',
    'ChargedRingAxis': 'Kärnidé: alla laddningselement på ringen har samma avstånd till en punkt på z-axeln. Tvärkomponenterna tar ut varandra, så endast E_z återstår.',
    'FiniteLineCharge2D': 'Kärnidé: fältet är summan av bidrag från en ändlig linjeladdning. När observationspunkten ligger nära en mycket lång tråd närmar sig resultatet det oändliga linjeladdningsfallet.',
    'SphericalShellPotential': 'Kärnidé: ett jämnt laddat sfäriskt skal ger E=0 innanför skalet och samma yttre fält som en punktladdning i centrum. Potentialen är konstant inuti.',
    'ConcentricChargedCylinders': 'Kärnidé: Gaussytor i form av koaxiella cylindrar visar vilka laddningar som bidrar i varje radialt område.',
    'SphericalCapacitorDesign': 'Kärnidé: den sfäriska kondensatorns största fält uppstår vid den inre sfären. Optimum för största tillåtna spänning fås när inre radien är ungefär halva yttre radien.',
    'AtmosphericChargeDensity': 'Kärnidé: med Gauss lag kopplas ändringen i vertikalt E-fält till genomsnittlig rymdladdningstäthet i luftvolymen.',
    'UniformSpaceChargePlates': 'Kärnidé: Poissons ekvation ger en parabolisk potential och ett linjärt E-fält mellan plattorna. Punkten E=0 finns bara om den hamnar inom intervallet.',
    'HClDipoleField': 'Kärnidé: molekylen modelleras som två punktladdningar. Långt bort bör fältet likna ett dipolfält, med olika uttryck på axel och ekvator.',
    'ObliqueConductorDielectricBoundary': 'Kärnidé: vid ledarytan är tangentiella E-komponenten noll. Normalfältet bestämmer fri ytladdning via D_n = ρ_s.',
    'SphericalShellChargingEnergy': 'Kärnidé: uppladdningsarbetet fås genom att integrera potentialen under laddningsprocessen: dW = V(q)dq.',
    'PointChargeConductingPlane': 'Kärnidé: det jordade ledande planet ersätts av en spegelladdning med motsatt tecken på andra sidan planet.',
    'ConductiveCoaxialElectrodes': 'Kärnidé: samma radiella geometri som en koaxial kondensator, men strömmen bestäms av konduktivitet och potentialfall.',
    'FiniteWireBiotSavart': 'Kärnidé: Biot–Savarts lag integreras över en ändlig rak ledare. Oändligt lång ledare fås som gränsfall när längden blir stor.',
    'ThinCurrentStripField': 'Kärnidé: strömbandet kan ses som många parallella trådar vars fält summeras över bandets bredd.',
    'LoopDipoleApproximationError': 'Kärnidé: jämför exakt axelfält från en cirkulär slinga med dipolapproximationen. Relativfelet visar när fjärrfältsmodellen är rimlig.',
    'PermanentMagnetAirGapBHCurve': 'Kärnidé: arbetspunkten bestäms av skärningen mellan magnetens materialkurva och magnetkretsens lastlinje.',
    'NonlinearIronMagneticCircuit': 'Kärnidé: luftgapet och det ickelinjära järnet delar den magnetomotoriska spänningen. Lösningen kräver att samma flöde går genom båda delarna.',
    'MutualInductanceParallelWiresSquare': 'Kärnidé: ömsesidig induktans beräknas från flödet genom den ena slingan per ström i den andra.',
    'MovingLoopFieldWork': 'Kärnidé: när slingan dras genom ett B-fält uppstår inducerad ström. Det mekaniska arbetet blir värmeförlust i resistansen.',
    'DisplacementCurrentCapacitor': 'Kärnidé: förskjutningsströmmen i gapet ersätter ledningsströmmen i Ampères lag när kondensatorn laddas och urladdas.',
}


def _format_number(value):
    """Kompakt talformat för status- och resultattexter."""
    try:
        value = float(value)
    except (TypeError, ValueError):
        return str(value)
    if not math.isfinite(value):
        return str(value)
    if value == 0:
        return '0'
    abs_value = abs(value)
    if 1e-3 <= abs_value < 1e4:
        return f'{value:.4g}'
    return f'{value:.3e}'


def _chapter_number(problem):
    """Hämtar kapitelnummer ur uppgiftsnamn som börjar med t.ex. '2.3'."""
    first = problem.name.split(maxsplit=1)[0]
    if '.' in first:
        return first.split('.', 1)[0]
    return ''


def pedagogical_note_for_problem(problem):
    """Kort didaktisk hjälptext som följer uppgiftens fysikaliska huvudidé."""
    specific = SPECIFIC_NOTES.get(problem.__class__.__name__)
    chapter = CHAPTER_NOTES.get(_chapter_number(problem), '')
    if specific and chapter:
        return f'{specific}\n\nKapitelkontext: {chapter}'
    if specific:
        return specific
    if chapter:
        return chapter
    return 'Använd parametrarna för att variera geometrin eller materialdata. Jämför huvudgrafen med geometriskissen och 3-D-vyn för att tolka resultatet.'


class ProblemBase:
    name = 'Basuppgift'
    description = ''
    parameters = []

    def parameter_specs(self):
        """Return structured parameter metadata with legacy tuple compatibility."""
        return normalize_parameter_specs(self.parameters)

    def defaults(self):
        return {spec.key: spec.default_si for spec in self.parameter_specs()}

    def validate(self, params):
        """Problem-specific validation hook retained for existing subclasses."""
        return None

    def validation_issues(self, params):
        """Combine generic metadata validation with the problem's own checks."""
        issues = validate_parameter_values(self.parameter_specs(), params)
        if any(issue.severity == 'error' for issue in issues):
            return issues
        try:
            problem_error = self.validate(params)
        except Exception as exc:
            issues.append(ValidationIssue('error', f'Valideringen misslyckades: {exc}'))
            return issues
        if problem_error:
            issues.append(ValidationIssue('error', str(problem_error)))
        return issues

    def validate_all(self, params):
        """Compatibility alias used by the user interfaces and tests."""
        return self.validation_issues(params)

    def plot(self, fig, params, mode):
        raise NotImplementedError

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, 'Ingen geometriskiss', ha='center', va='center')
        ax.set_axis_off()

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        ax.text(0.5, 0.5, 0.5, 'Ingen 3-D-vy', ha='center', va='center')
        ax.set_axis_off()

    def pedagogical_note(self):
        return pedagogical_note_for_problem(self)

    def result_summary(self, params, mode):
        # Importeras sent för att undvika cirkulära beroenden mellan
        # basklassen, uppgiftsklasserna och kontrollfunktionerna.
        from .checks import result_summary_for_problem
        return result_summary_for_problem(self, params, mode)

    def physics_check(self, params):
        # Importeras sent av samma skäl som result_summary.
        from .checks import physics_checks_for_problem
        return physics_checks_for_problem(self, params)


# Gör även interna hjälpfunktioner som börjar med _ tillgängliga för problems.py.
__all__ = [name for name in globals() if not name.startswith('__')]
