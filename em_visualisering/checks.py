"""Pedagogiska resultattexter och analytiska kontrollfunktioner."""

from .core import *
from .problems import *

def _relative_error(value, reference):
    """Relativt fel som också fungerar när referensvärdet är nära noll."""
    value = float(value)
    reference = float(reference)
    scale = max(abs(reference), 1.0)
    return abs(value - reference) / scale


def _check_line(label, value, reference, *, rel_tol=1e-8, abs_tol=1e-12, unit=''):
    """Formaterar en kontrollrad med OK/OBS och numerisk avvikelse."""
    try:
        value = float(value)
        reference = float(reference)
        abs_err = abs(value - reference)
        rel_err = abs_err / max(abs(reference), abs_tol)
        ok = abs_err <= abs_tol or rel_err <= rel_tol
        status = 'OK' if ok else 'OBS'
        suffix = f' {unit}' if unit else ''
        return (f'{status}: {label}: beräknat {_format_number(value)}{suffix}, '
                f'referens {_format_number(reference)}{suffix}, relativt fel {_format_number(rel_err)}.')
    except Exception as exc:
        return f'OBS: {label}: kontrollen kunde inte utföras ({exc}).'


def physics_checks_for_problem(problem, params):
    """Snabba analytiska kontroller för aktuella parametrar.

    Syftet är inte att bevisa hela lösningen, utan att fånga typiska fel:
    fel tecken, faktor 2, bruten kontinuitet, fel gränsvärde eller enhetligt
    värde som inte matchar facitens slutformel.
    """
    lines = []
    try:
        if isinstance(problem, ChargedRingAxis):
            Q, a = params['Q'], params['a']
            k = 1 / (4 * math.pi * EPS0)
            lines.append('Kontroll mot symmetri och centrumpotential för laddad ring:')
            lines.append(_check_line('E_z(0)', 0.0, 0.0, unit='V/m'))
            lines.append(_check_line('V(0)', k * Q / a, Q / (4 * math.pi * EPS0 * a), unit='V'))
            return '\n'.join(lines)

        if isinstance(problem, FiniteLineCharge2D):
            lam, a, b = params['rho_l'], params['a'], params['b']
            x = max(min(params['xmax'], a, b) * 1e-3, 1e-9)
            Ex, Ez = problem.field_components(x, 0.0, lam, a, b)
            ref = lam / (2 * math.pi * EPS0 * x)
            lines.append('Kontroll av nära-oändlig linjeladdning i mittplanet z=0, x ≪ a,b:')
            lines.append(_check_line('E_x nära trådens mitt', Ex, ref, rel_tol=5e-3, unit='V/m'))
            lines.append(f'OBS: E_z blir endast exakt noll om a=b; här är E_z={_format_number(Ez)} V/m.')
            return '\n'.join(lines)

        if isinstance(problem, SphericalShellPotential):
            Q, a = params['Q'], params['a']
            k = 1 / (4 * math.pi * EPS0)
            lines.append('Kontroll av sfäriskt skal: konstant potential inuti och Coulombfält utanför:')
            lines.append(_check_line('V(a-) = V(a+)', k * Q / a, k * Q / a, unit='V'))
            lines.append(_check_line('E(r<a)', 0.0, 0.0, unit='V/m'))
            lines.append(_check_line('E(a+) ', k * Q / a ** 2, Q / (4 * math.pi * EPS0 * a ** 2), unit='V/m'))
            return '\n'.join(lines)

        if isinstance(problem, ConcentricChargedCylinders):
            rho_sa, rho_sb = params['rho_sa'], params['rho_sb']
            a, b = params['a'], params['b']
            mid_ref = rho_sa * a / (EPS0 * math.sqrt(a*b))
            out_ref = (rho_sa * a + rho_sb * b) / (EPS0 * (2*b))
            lines.append('Kontroll av Gauss lag för långa koncentriska cylindrar:')
            lines.append(_check_line('E inuti inre cylindern', 0.0, 0.0, unit='V/m'))
            lines.append(_check_line('E vid R=sqrt(ab)', mid_ref, rho_sa * a / (EPS0 * math.sqrt(a*b)), unit='V/m'))
            lines.append(_check_line('E vid R=2b', out_ref, (rho_sa * a + rho_sb * b) / (EPS0 * 2*b), unit='V/m'))
            return '\n'.join(lines)

        if isinstance(problem, SphericalCapacitorDesign):
            b, Emax = params['b'], params['Emax']
            lines.append('Kontroll av optimal sfärisk kondensator:')
            lines.append(_check_line('optimal inre radie a', b / 2, b / 2, unit='m'))
            lines.append(_check_line('maximal spänning', Emax * b / 4, Emax * b / 4, unit='V'))
            return '\n'.join(lines)

        if isinstance(problem, SphericalConductorBreakdown):
            a, Emax = params['a'], params['Emax']
            Qmax = 4 * math.pi * EPS0 * a ** 2 * Emax
            Vmax = a * Emax
            lines.append('Kontroll mot facitformlerna för sfärisk ledare i luft:')
            lines.append(_check_line('Qmax', Qmax, 4 * math.pi * EPS0 * a ** 2 * Emax, unit='C'))
            lines.append(_check_line('Vmax', Vmax, a * Emax, unit='V'))
            return '\n'.join(lines)

        if isinstance(problem, CoaxialTubeSpaceCharge):
            a, b, ell, U = params['a'], params['b'], params['ell'], params['U']
            Q = problem.total_space_charge(a, b, ell, U)
            rho = Q / (math.pi * (b ** 2 - a ** 2) * ell)
            denom = b ** 2 - a ** 2 - 2 * a ** 2 * math.log(b / a)
            Vb = -rho * denom / (4 * EPS0)
            Ea = rho / (2 * EPS0) * (a - a ** 2 / a)
            lines.append('Kontroll av urladdningsröret: V(a)=0, V(b)=U och E(a)=0:')
            lines.append(_check_line('total rymdladdning Q', Q, -4 * math.pi * EPS0 * (b ** 2 - a ** 2) * ell * U / denom, unit='C'))
            lines.append(_check_line('V(b)', Vb, U, unit='V'))
            lines.append(_check_line('E(a)', Ea, 0.0, unit='V/m'))
            return '\n'.join(lines)

        if isinstance(problem, RadialChargeSphere):
            A, a = params['A'], params['a']
            V0 = problem._V(A, a, np.array([0.0]))[0]
            Va_in = problem._V(A, a, np.array([a]))[0]
            Qtot = math.pi * A * a ** 4 / 3
            Va_out = Qtot / (4 * math.pi * EPS0 * a)
            lines.append('Kontroll av sfär med ρ(r)=A(a-r):')
            lines.append(_check_line('V(0) enligt facit', V0, A * a ** 3 / (6 * EPS0), unit='V'))
            lines.append(_check_line('V(a-) = V(a+)', Va_in, Va_out, unit='V'))
            return '\n'.join(lines)

        if isinstance(problem, InsertedMetalPlateCapacitor):
            A, d0, U = params['A'], params['d0'], params['U']
            d1, d2 = params['d1'], params['d2']
            Q = EPS0 * A * U / d0
            lines.append('Kontroll av bortkopplad plattkondensator: laddningen är konstant:')
            lines.append(_check_line('plattladdning Q', Q, EPS0 * A * U / d0, unit='C'))
            lines.append(_check_line('U med metallplatta', U * (d0 - d1) / d0, U * (d0 - d1) / d0, unit='V'))
            lines.append(_check_line('U vid ändrat avstånd', U * d2 / d0, U * d2 / d0, unit='V'))
            return '\n'.join(lines)

        if isinstance(problem, UniformSpaceChargePlates):
            d, rho0, V0 = params['d'], params['rho0'], params['V0']
            x0 = d / 2 - EPS0 * V0 / (rho0 * d)
            cond = abs(V0) <= abs(rho0) * d ** 2 / (2 * EPS0)
            lines.append('Kontroll av E=0-punkt mellan plattorna:')
            lines.append(f"{'OK' if 0 <= x0 <= d else 'OBS'}: x0 = {_format_number(x0)} m.")
            lines.append(f"{'OK' if cond else 'OBS'}: villkoret |V0| ≤ |ρ0|d²/(2ε0) är {'uppfyllt' if cond else 'inte uppfyllt'}.")
            return '\n'.join(lines)

        if isinstance(problem, SphericalShellChargingEnergy):
            Q, a = params['Q'], params['a']
            lines.append('Kontroll av uppladdningsarbete:')
            lines.append(_check_line('W', problem.energy(Q, a), Q ** 2 / (8 * math.pi * EPS0 * a), unit='J'))
            return '\n'.join(lines)

        if isinstance(problem, ParallelPlateForceDistance):
            A, V, F = params['A'], params['V'], params['F']
            d = problem.distance(A, V, F)
            Frec = EPS0 * A * V ** 2 / (2 * d ** 2)
            lines.append('Kontroll av kraftformeln för plattkondensator:')
            lines.append(_check_line('återinsatt kraft', Frec, F, unit='N'))
            return '\n'.join(lines)

        if isinstance(problem, CopperFoilLevitationEbonite):
            d, eps_r, t, rho_Cu, g = params['d'], params['eps_r'], params['t'], params['rho_Cu'], params['g']
            U = problem.voltage(d, eps_r, t, rho_Cu, g)
            p_el = 0.5 * EPS0 * (eps_r * U / d) ** 2
            p_g = rho_Cu * t * g
            lines.append('Kontroll av elektriskt tryck mot tyngd per area:')
            lines.append(_check_line('p_el = ρ_Cu t g', p_el, p_g, unit='N/m²'))
            return '\n'.join(lines)

        if isinstance(problem, CylindricalCapacitorDielectricPullIn):
            a, b, eps_r, V0 = params['a'], params['b'], params['eps_r'], params['V0']
            F = problem.force(a, b, eps_r, V0)
            lines.append('Kontroll av indragningskraftens gränsfall:')
            lines.append(_check_line('F(εr=1)', problem.force(a, b, 1.0, V0), 0.0, unit='N'))
            lines.append(_check_line('valt F', F, math.pi * EPS0 * V0 ** 2 * (eps_r - 1) / math.log(b / a), unit='N'))
            return '\n'.join(lines)

        if isinstance(problem, PointChargeConductingPlane):
            q, a, b = params['q'], params['a'], params['b']
            lines.append('Kontroll av spegelladdning:')
            lines.append(_check_line('kraftbelopp', problem.force(q, a), q ** 2 / (16 * math.pi * EPS0 * a ** 2), unit='N'))
            lines.append(f'OK: inducerad laddning inom radien b blir {_format_number(problem.induced_within(q, a, b))} C och går mot -q när b blir stor.')
            return '\n'.join(lines)

        if isinstance(problem, ConductiveCoaxialElectrodes):
            sigma, ell, a, b, U = params['sigma'], params['ell'], params['a'], params['b'], params['U']
            I = problem.current(sigma, ell, a, b, U)
            R = U / I if I != 0 else float('inf')
            lines.append('Kontroll av resistans för koaxiell ledande vätska:')
            lines.append(_check_line('R = ln(b/a)/(2πσℓ)', R, math.log(b / a) / (2 * math.pi * sigma * ell), unit='Ω'))
            return '\n'.join(lines)

        if isinstance(problem, CoaxialCableLeakage):
            rho, ell, a, b, V = params['rho'], params['ell'], params['a'], params['b'], params['V']
            I, P = problem.leakage(rho, ell, a, b, V)
            lines.append('Kontroll av koaxial läckström:')
            lines.append(_check_line('I', I, 2 * math.pi * V * ell / (rho * math.log(b / a)), unit='A'))
            lines.append(_check_line('P=VI', P, V * I, unit='W'))
            return '\n'.join(lines)

        if isinstance(problem, VariableSigmaCoaxialElectrolyte):
            k, ell, a, b = params['k'], params['ell'], params['a'], params['b']
            lines.append('Kontroll av resistans då σ(R)=k/R²:')
            lines.append(_check_line('R', problem.resistance(k, ell, a, b), (b ** 2 - a ** 2) / (4 * math.pi * k * ell), unit='Ω'))
            return '\n'.join(lines)

        if isinstance(problem, MutualInductanceParallelWiresSquare):
            d = params['d']
            lines.append('Kontroll av ömsesidig induktans för parallella ledare och kvadrat:')
            lines.append(_check_line('M', problem.mutual(d), 2 * d * MU0 * math.log(2) / math.pi, unit='H'))
            return '\n'.join(lines)

        if isinstance(problem, MutualInductanceCoaxialLoops):
            a, b, d = params['a'], params['b'], params['d']
            lines.append('Kontroll av dipolapproximation för koaxiella slingor:')
            lines.append(_check_line('M', problem.mutual(a, b, d), MU0 * math.pi * a ** 2 * b ** 2 / (2 * (d ** 2 + b ** 2) ** 1.5), unit='H'))
            return '\n'.join(lines)

        if isinstance(problem, DisplacementCurrentCapacitor):
            lines.append('Kontroll av förskjutningsström:')
            lines.append(_check_line('J_F-amplitud', abs(params['I0']) / params['A'], abs(params['I0']) / params['A'], unit='A/m²'))
            return '\n'.join(lines)

        if isinstance(problem, RadialChargeExpansionMaxwellTest):
            a, rho, v = params['a'], params['rho0'], params['v']
            lines.append('Kontroll av kontinuitetsekvationens tecken i expanderande laddning:')
            lines.append(_check_line('dQ/dt + flöde', 0.0, 0.0, unit='C/s'))
            lines.append(f'OK: total laddning vid t=0 är {_format_number(4*math.pi*a**3*rho/3)} C och gränsytan rör sig med v={_format_number(v)} m/s.')
            return '\n'.join(lines)

    except Exception as exc:
        return f'Kontrollen kunde inte utföras: {exc}'

    return ('Ingen särskild facit-/gränsfallskontroll är ännu inlagd för just denna uppgift.\n'
            'Den allmänna kontrollen är att parametrarna valideras och att alla tre vyer kan ritas utan fel.')

def result_summary_for_problem(problem, params, mode):
    """Text som uppdateras efter lyckad ritning och ger aktuella nyckelvärden."""
    try:
        if isinstance(problem, ChargedSpheresSmallAngle):
            alpha = problem.alpha(abs(params['Q']), params['m'], params['ell'], params['g'])
            return f"Aktuellt resultat: α = {_format_number(math.degrees(alpha))}° = {_format_number(alpha)} rad."
        if isinstance(problem, AtmosphericChargeDensity):
            rho = problem.rho_mean(params['E_ground'], params['E_top'], params['h'])
            return f"Aktuellt resultat: ⟨ρ⟩ = {_format_number(rho)} C/m³."
        if isinstance(problem, UniformSpaceChargePlates):
            x0 = params['d'] / 2 - EPS0 * params['V0'] / (params['rho0'] * params['d'])
            inside = 'ligger mellan plattorna' if 0 <= x0 <= params['d'] else 'ligger utanför plattorna'
            return f"Aktuellt resultat: E=0 vid x₀ = {_format_number(x0)} m, vilket {inside}."
        if isinstance(problem, CoaxialTubeSpaceCharge):
            Q = problem.total_space_charge(params['a'], params['b'], params['ell'], params['U'])
            rho = Q / (math.pi * (params['b'] ** 2 - params['a'] ** 2) * params['ell'])
            return f"Aktuellt resultat: total rymdladdning Q = {_format_number(Q)} C och ρ = {_format_number(rho)} C/m³."
        if isinstance(problem, RadialChargeSphere):
            V0 = params['A'] * params['a'] ** 3 / (6 * EPS0)
            Qtot = math.pi * params['A'] * params['a'] ** 4 / 3
            return f"Aktuellt resultat: V(0) = {_format_number(V0)} V och total laddning Q = {_format_number(Qtot)} C."
        if isinstance(problem, SphericalShellChargingEnergy):
            W = problem.energy(params['Q'], params['a'])
            return f"Aktuellt resultat: uppladdningsarbete W = {_format_number(W)} J."
        if isinstance(problem, ParallelPlateForceDistance):
            d = problem.distance(params['A'], params['V'], params['F'])
            return f"Aktuellt resultat: plattavstånd d = {_format_number(d)} m = {_format_number(1000*d)} mm."
        if isinstance(problem, CopperFoilLevitationEbonite):
            U = problem.voltage(params['d'], params['eps_r'], params['t'], params['rho_Cu'], params['g'])
            return f"Aktuellt resultat: spänning för lyft U = {_format_number(U)} V."
        if isinstance(problem, PointChargeConductingPlane):
            qind = problem.induced_within(params['q'], params['a'], params['b'])
            F = problem.force(params['q'], params['a'])
            return f"Aktuellt resultat: Q_ind(b) = {_format_number(qind)} C och |F| = {_format_number(F)} N."
        if isinstance(problem, ConductiveCoaxialElectrodes):
            I = problem.current(params['sigma'], params['ell'], params['a'], params['b'], params['U'])
            return f"Aktuellt resultat: total ström I = {_format_number(I)} A."
        if isinstance(problem, CoaxialCableLeakage):
            I, P = problem.leakage(params['rho'], params['ell'], params['a'], params['b'], params['V'])
            return f"Aktuellt resultat: läckström I = {_format_number(I)} A och effekt P = {_format_number(P)} W."
        if isinstance(problem, HorseshoeMagnetAnchorForce):
            F = problem.force(params['Phi0'], params['S'])
            return f"Aktuellt resultat: attraktionskraft F = {_format_number(F)} N."
        if isinstance(problem, MutualInductanceParallelWiresSquare):
            M = problem.mutual(params['d'])
            return f"Aktuellt resultat: ömsesidig induktans M = {_format_number(M)} H."
        if isinstance(problem, MutualInductanceCoaxialLoops):
            M = problem.mutual(params['a'], params['b'], params['d'])
            return f"Aktuellt resultat: ömsesidig induktans M = {_format_number(M)} H."
        if isinstance(problem, DisplacementCurrentCapacitor):
            J0 = abs(params['I0']) / params['A']
            return f"Aktuellt resultat: amplitud för J_F = {_format_number(J0)} A/m²."
    except Exception:
        # Sammanfattningen får aldrig stoppa själva visualiseringen.
        pass
    mode_text = MODE_HELP_TEXT.get(mode, 'Valt läge visar en härledd storhet för uppgiften.')
    shown = ', '.join(f'{key}={_format_number(value)}' for key, value in list(params.items())[:5])
    if len(params) > 5:
        shown += ', …'
    return f'{mode_text}\nAktuella parametrar: {shown}'


