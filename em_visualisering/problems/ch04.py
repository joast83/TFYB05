"""Kapitel 4: Energi, kraft och spegelladdning.

Uppgifter i detta kapitel (i menyordning):
    4.1    SphericalShellChargingEnergy
    4.2    ParallelPlateForceDistance
    4.3    CopperFoilLevitationEbonite
    4.5    ThundercloudEnergyEstimate
    4.6    CylindricalCapacitorDielectricPullIn
    4.7    PointChargeConductingPlane
"""

from ..core import *


class SphericalShellChargingEnergy(ProblemBase):
    name = '4.1 Energi vid uppladdning av sfäriskt skal'
    description = 'Arbete som krävs för att ladda upp ett tunt ledande sfäriskt skal till laddningen Q.'
    parameters = [('Q', 'Slutladdning Q [C]', 1e-09), ('a', 'Skalradie a [m]', 0.1)]

    def validate(self, params):
        if params['a'] <= 0:
            return 'a måste vara positiv.'
        return None

    @staticmethod
    def energy(Q, a):
        return Q ** 2 / (8 * math.pi * EPS0 * a)

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        Q, a = (params['Q'], params['a'])
        q = np.linspace(0, max(abs(Q) * 1.3, 1e-12), 400)
        V = q / (4 * math.pi * EPS0 * a)
        W = self.energy(q, a)
        if mode == 'Magnitude':
            ax.plot(q, W)
            ax.set_ylabel('W [J]')
            ax.set_title(f'W(Q) = {self.energy(Q, a):.3e} J')
        else:
            ax.plot(q, V)
            ax.set_ylabel('V [V]')
            ax.set_title('Uppladdningspotential under processen')
        ax.set_xlabel('q [C]')
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        a = params['a']
        ax.add_patch(Circle((0, 0), a, fill=False, linewidth=2))
        ax.text(0, 0, 'ledande skal', ha='center', va='center')
        ax.set_aspect('equal')
        ax.set_xlim(-1.25 * a, 1.25 * a)
        ax.set_ylim(-1.25 * a, 1.25 * a)
        ax.set_title('Geometriskiss')
        ax.set_axis_off()

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        Q, a = (params['Q'], params['a'])
        aa = np.linspace(max(0.1 * a, 1e-06), 2 * a, 60)
        qq = np.linspace(0, max(abs(Q) * 1.5, 1e-12), 60)
        A, QG = np.meshgrid(aa, qq)
        W = self.energy(QG, A)
        ax.plot_surface(A, QG, W, cmap='viridis', alpha=0.9)
        ax.set_xlabel('a [m]')
        ax.set_ylabel('Q [C]')
        ax.set_zlabel('W [J]')
        ax.set_title('Parametersvep för uppladdningsarbete')

class ParallelPlateForceDistance(ProblemBase):
    name = '4.2 Kraft och avstånd i plattkondensator'
    description = 'Bestämmer plattavståndet ur F = ε0 A V²/(2d²) för en luftkondensator.'
    parameters = [('A', 'Plattarea A [m²]', 0.005), ('V', 'Spänning V [V]', 450.0), ('F', 'Kraft F [N]', 0.05)]

    def validate(self, params):
        if params['A'] <= 0 or params['F'] <= 0:
            return 'A och F måste vara positiva.'
        return None

    @staticmethod
    def distance(A, V, F):
        return abs(V) * math.sqrt(EPS0 * A / (2 * F))

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        A, V, F = (params['A'], params['V'], params['F'])
        d0 = self.distance(A, V, F)
        d = np.linspace(max(d0 * 0.2, 1e-06), d0 * 4, 400)
        f = EPS0 * A * V ** 2 / (2 * d ** 2)
        ax.plot(d * 1000.0, f)
        ax.axhline(F, linestyle='--', linewidth=1)
        ax.axvline(d0 * 1000.0, linestyle='--', linewidth=1)
        ax.set_xlabel('d [mm]')
        ax.set_ylabel('F [N]')
        ax.set_title(f'Krävt avstånd d = {d0 * 1000.0:.3g} mm')
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        ax.add_patch(Rectangle((-0.5, 0.2), 1, 0.08, fill=False, linewidth=2))
        ax.add_patch(Rectangle((-0.5, -0.2), 1, 0.08, fill=False, linewidth=2))
        ax.arrow(0.62, 0.2, 0, 0.25, head_width=0.05, length_includes_head=True)
        ax.arrow(0.62, -0.12, 0, -0.25, head_width=0.05, length_includes_head=True)
        ax.text(0, 0, 'luftgap d', ha='center')
        ax.set_xlim(-0.8, 0.8)
        ax.set_ylim(-0.6, 0.6)
        ax.set_aspect('equal')
        ax.set_axis_off()
        ax.set_title('Plattattraktion')

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        A, V, F = (params['A'], params['V'], params['F'])
        d = np.linspace(5e-05, 0.002, 60)
        vv = np.linspace(max(abs(V) * 0.2, 1), abs(V) * 1.5, 60)
        D, VV = np.meshgrid(d, vv)
        FF = EPS0 * A * VV ** 2 / (2 * D ** 2)
        ax.plot_surface(D * 1000.0, VV, FF, cmap='plasma', alpha=0.9)
        ax.set_xlabel('d [mm]')
        ax.set_ylabel('V [V]')
        ax.set_zlabel('F [N]')
        ax.set_title('Kraftyta')

class CopperFoilLevitationEbonite(ProblemBase):
    name = '4.3 Kopparfolie som lyfts av ebonitplatta'
    description = 'Spänning som behövs för att elektriskt tryck ska balansera kopparfoliens tyngd per area.'
    parameters = [('d', 'Ebonittjocklek d [m]', 0.02), ('eps_r', 'Relativ permittivitet εr', 5.0), ('t', 'Koppartjocklek t [m]', 0.0001), ('rho_Cu', 'Kopparns densitet ρCu [kg/m³]', 8900.0), ('g', 'Tyngdacceleration g [m/s²]', 9.81)]

    def validate(self, params):
        if min(params['d'], params['eps_r'], params['t'], params['rho_Cu'], params['g']) <= 0:
            return 'Alla parametrar måste vara positiva.'
        return None

    @staticmethod
    def voltage(d, eps_r, t, rho_Cu, g):
        return d / eps_r * math.sqrt(2 * t * rho_Cu * g / EPS0)

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        d, e, t, rho, g = (params['d'], params['eps_r'], params['t'], params['rho_Cu'], params['g'])
        U0 = self.voltage(d, e, t, rho, g)
        U = np.linspace(0, max(1.6 * U0, 1), 400)
        p = 0.5 * EPS0 * (e * U / d) ** 2
        w = rho * t * g
        ax.plot(U / 1000.0, p, label='elektriskt tryck')
        ax.axhline(w, linestyle='--', linewidth=1, label='tyngd/area')
        ax.axvline(U0 / 1000.0, linestyle='--', linewidth=1)
        ax.set_xlabel('U [kV]')
        ax.set_ylabel('tryck [N/m²]')
        ax.set_title(f'Levitationens spänning U = {U0 / 1000.0:.3g} kV')
        ax.legend()
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        ax.add_patch(Rectangle((-0.6, 0.1), 1.2, 0.18, alpha=0.25))
        ax.add_patch(Rectangle((-0.6, -0.03), 1.2, 0.04, fill=False, linewidth=2))
        ax.text(0, 0.2, 'metalliserad ebonit', ha='center')
        ax.text(0, -0.12, 'kopparfolie', ha='center')
        ax.arrow(0.4, -0.03, 0, 0.16, head_width=0.04, length_includes_head=True)
        ax.arrow(-0.4, 0.0, 0, -0.16, head_width=0.04, length_includes_head=True)
        ax.set_xlim(-0.8, 0.8)
        ax.set_ylim(-0.35, 0.45)
        ax.set_aspect('equal')
        ax.set_axis_off()
        ax.set_title('Elektriskt tryck mot tyngd')

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        d, t, rho, g = (params['d'], params['t'], params['rho_Cu'], params['g'])
        er = np.linspace(2, 10, 50)
        tt = np.linspace(max(t * 0.2, 1e-06), t * 2, 50)
        ER, TT = np.meshgrid(er, tt)
        U = d / ER * np.sqrt(2 * TT * rho * g / EPS0)
        ax.plot_surface(ER, TT * 1000.0, U / 1000.0, cmap='viridis', alpha=0.9)
        ax.set_xlabel('εr')
        ax.set_ylabel('t [mm]')
        ax.set_zlabel('U [kV]')
        ax.set_title('Levitationens spänning')

class ThundercloudEnergyEstimate(ProblemBase):
    name = '4.5 Åskmoln som kondensator'
    description = 'Approximerar ett åskmoln och marken som en plattkondensator. Använder luftens genomslagsfält för att uppskatta molnets laddning och lagrad elektrostatisk energi.'
    parameters = [('A', 'Moln-/markarea A [m²]', 1000000.0), ('h', 'Molnbasens höjd h [m]', 200.0), ('Emax', 'Genomslagsfält Emax [V/m]', 2000000.0)]

    def validate(self, params):
        if params['A'] <= 0 or params['h'] <= 0 or params['Emax'] <= 0:
            return 'A, h och Emax måste vara positiva.'
        return None

    @staticmethod
    def charge_and_energy(A, h, Emax):
        Q = EPS0 * A * Emax
        We = 0.5 * EPS0 * Emax ** 2 * A * h
        V = Emax * h
        sigma = EPS0 * Emax
        C = EPS0 * A / h
        return (Q, We, V, sigma, C)

    def plot(self, fig, params, mode):
        fig.clear()
        A, h, Emax = (params['A'], params['h'], params['Emax'])
        Q, We, V, sigma, C = self.charge_and_energy(A, h, Emax)
        if mode == 'Map':
            ax = fig.add_subplot(111)
            side = math.sqrt(A)
            x = np.linspace(-0.6 * side, 0.6 * side, 180)
            z = np.linspace(-0.15 * h, 1.15 * h, 220)
            X, Z = np.meshgrid(x, z)
            data = np.where((Z >= 0) & (Z <= h), Emax, 1e-12 * Emax)
            _show_scalar_map(ax, fig, X, Z, data, title='Åskmoln som kondensator: |E|-karta', xlabel='horisontellt läge [m]', ylabel='höjd z [m]', cbar_label='|E| [V/m]', scale='log')
            ax.axhline(0, color='white', linewidth=1.0)
            ax.axhline(h, color='white', linewidth=1.0)
            return
        if mode == 'Field':
            ax = fig.add_subplot(111)
            z = np.linspace(-0.15 * h, 1.15 * h, 800)
            E = np.where((z >= 0) & (z <= h), Emax, 0.0)
            ax.plot(z, E * 0.001, linewidth=2, color='steelblue', label=f'E = {Emax:.2e} V/m inside gap')
            ax.axhline(Emax * 0.001, linestyle='--', linewidth=1, color='tomato', label='genomslagsfält Emax')
            ax.fill_between(z, E * 0.001, alpha=0.15, color='steelblue')
            ax.axvline(0, linestyle=':', linewidth=0.9, color='grey')
            ax.axvline(h, linestyle=':', linewidth=0.9, color='grey')
            ax.set_xlabel('Höjd z [m]  (mark = 0, molnbas = h)')
            ax.set_ylabel('E [kV/m]')
            ax.set_title('Åskmolnsmodell: elektriskt fält i gapet')
            ax.text(0.02, 0.98, f'|Q| = {Q:.3g} C\nσ = {sigma:.3e} C/m²\nC = {C:.3e} F', transform=ax.transAxes, va='top', fontsize=9)
            ax.legend(fontsize=8)
            ax.grid(True, alpha=0.3)
        else:
            ax = fig.add_subplot(111)
            h_arr = np.linspace(10, 3 * h, 400)
            We_arr = 0.5 * EPS0 * Emax ** 2 * A * h_arr
            w_density = 0.5 * EPS0 * Emax ** 2
            ax2 = ax.twinx()
            ax.plot(h_arr, We_arr * 1e-09, color='darkorange', linewidth=2, label='Lagrad energi Wₑ')
            ax.axvline(h, linestyle='--', linewidth=1, color='grey')
            ax.scatter([h], [We * 1e-09], color='red', zorder=5, label=f'Aktuellt: Wₑ = {We:.3g} J')
            ax2.axhline(w_density * 0.001, linestyle=':', color='steelblue', linewidth=1.5, label=f'w = {w_density * 0.001:.2e} kJ/m³')
            ax.set_xlabel('Molnbasens höjd h [m]')
            ax.set_ylabel('Lagrad energi Wₑ [GJ]', color='darkorange')
            ax2.set_ylabel('Energitäthet w [kJ/m³]', color='steelblue')
            ax.set_title('Åskmolnsuppskattning: lagrad energi mot gaphöjd')
            lines1, lab1 = ax.get_legend_handles_labels()
            lines2, lab2 = ax2.get_legend_handles_labels()
            ax.legend(lines1 + lines2, lab1 + lab2, fontsize=8)
            ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        A, h = (params['A'], params['h'])
        side = math.sqrt(A)
        half = 0.5 * side
        ax.add_patch(Rectangle((-half, 0), side, 3, fill=True, alpha=0.35))
        ax.add_patch(Rectangle((-half, h), side, 3, fill=True, alpha=0.35))
        ax.annotate('', xy=(half * 0.82, h), xytext=(half * 0.82, 0), arrowprops=dict(arrowstyle='<->', linewidth=1.5))
        ax.text(half * 0.88, 0.5 * h, f'h = {h:g} m', rotation=90, va='center')
        ax.text(0, h + 10, 'molnbas (−Q)', ha='center', va='bottom')
        ax.text(0, -10, 'mark (+Q)', ha='center', va='top')
        ax.text(0, 0.5 * h, f'motsvarande kvadratisk sida ≈ {side:.0f} m', ha='center', va='center')
        ax.set_title('Geometriskiss')
        ax.set_xlim(-0.65 * side, 0.65 * side)
        ax.set_ylim(-0.15 * h, 1.2 * h)
        ax.set_axis_off()

    def draw_3d(self, fig, params, mode):
        fig.clear()
        A0, h, E0 = (params['A'], params['h'], params['Emax'])
        area = np.linspace(0.25 * A0, 2.0 * A0, 45)
        field = np.linspace(0.25 * E0, 1.5 * E0, 45)
        AREA, FIELD = np.meshgrid(area, field)
        Q = EPS0 * AREA * FIELD
        WE = 0.5 * EPS0 * FIELD ** 2 * AREA * h
        Z = Q if mode == 'Field' else WE
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(AREA / 1000000.0, FIELD / 100000.0, Z, cmap='viridis', alpha=0.85, rstride=1, cstride=1)
        ax.scatter([A0 / 1000000.0], [E0 / 100000.0], [EPS0 * A0 * E0 if mode == 'Field' else 0.5 * EPS0 * E0 ** 2 * A0 * h], color='red', s=35)
        ax.set_xlabel('Area [km²]')
        ax.set_ylabel('Emax [kV/cm]')
        ax.set_zlabel('|Q| [C]' if mode == 'Field' else 'Wₑ [J]')
        ax.set_title('Designyta för åskmolnsuppskattning')

class CylindricalCapacitorDielectricPullIn(ProblemBase):
    name = '4.6 Dielektrikum dras in i cylindrisk kondensator'
    description = 'Kraften som drar in ett koaxiellt dielektriskt hölje i en spänningsmatad cylindrisk kondensator.'
    parameters = [('a', 'Inre radie a [m]', 0.03), ('b', 'Yttre radie b [m]', 0.05), ('eps_r', 'Relativ permittivitet εr', 8.0), ('V0', 'Spänning V0 [V]', 1000.0)]

    def validate(self, params):
        if params['a'] <= 0 or params['b'] <= params['a'] or params['eps_r'] <= 0:
            return 'Kräver 0 < a < b och εr > 0.'
        return None

    @staticmethod
    def force(a, b, eps_r, V0):
        return math.pi * EPS0 * V0 ** 2 * (eps_r - 1) / math.log(b / a)

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        a, b, e, V = (params['a'], params['b'], params['eps_r'], params['V0'])
        eps = np.linspace(1, max(e * 1.8, 2), 400)
        F = math.pi * EPS0 * V ** 2 * (eps - 1) / math.log(b / a)
        F0 = self.force(a, b, e, V)
        ax.plot(eps, F)
        ax.scatter([e], [F0])
        ax.set_xlabel('εr')
        ax.set_ylabel('F [N]')
        ax.set_title(f'Indragningskraft F = {F0:.3e} N')
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        a, b = (params['a'], params['b'])
        ax.add_patch(Circle((0, 0), b, fill=False, linewidth=2))
        ax.add_patch(Circle((0, 0), a, fill=False, linewidth=2))
        ax.arrow(-1.5 * b, 0, 0.6 * b, 0, head_width=0.07 * b, length_includes_head=True)
        ax.text(-1.55 * b, 0.13 * b, 'dielektriskt hölje', ha='left')
        ax.set_aspect('equal')
        ax.set_xlim(-1.8 * b, 1.2 * b)
        ax.set_ylim(-1.2 * b, 1.2 * b)
        ax.set_axis_off()
        ax.set_title('Koaxiellt gap')

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        a, b, V = (params['a'], params['b'], params['V0'])
        er = np.linspace(1, 12, 60)
        vv = np.linspace(max(0.1 * abs(V), 1), 1.5 * abs(V), 60)
        ER, VV = np.meshgrid(er, vv)
        F = math.pi * EPS0 * VV ** 2 * (ER - 1) / math.log(b / a)
        ax.plot_surface(ER, VV / 1000.0, F, cmap='plasma', alpha=0.9)
        ax.set_xlabel('εr')
        ax.set_ylabel('V [kV]')
        ax.set_zlabel('F [N]')
        ax.set_title('Kraftyta')

class PointChargeConductingPlane(ProblemBase):
    name = '4.7 Punktladdning ovanför ledande plan'
    description = 'Spegelladdningslösning för inducerad laddning och attraktionskraft på en laddning ovanför ett ledande plan.'
    parameters = [('q', 'Laddning q [C]', 1e-09), ('a', 'Höjd över planet a [m]', 0.1), ('b', 'Avståndsgräns b från laddningen [m]', 0.3)]

    def validate(self, params):
        if params['a'] <= 0 or params['b'] <= params['a']:
            return 'Kräver b > a > 0.'
        return None

    @staticmethod
    def induced_within(q, a, b):
        return -q * (1 - a / b)

    @staticmethod
    def force(q, a):
        return q ** 2 / (16 * math.pi * EPS0 * a ** 2)

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        q, a, b = (params['q'], params['a'], params['b'])
        bb = np.linspace(a * 1.001, max(3 * b, 1.01 * a), 500)
        Qind = self.induced_within(q, a, bb)
        if mode == 'Magnitude':
            aa = np.linspace(0.2 * a, 3 * a, 400)
            F = self.force(q, aa)
            ax.plot(aa, F)
            ax.scatter([a], [self.force(q, a)])
            ax.set_xlabel('a [m]')
            ax.set_ylabel('|F| [N]')
            ax.set_title(f'Attraktionskraft = {self.force(q, a):.3e} N nedåt')
        else:
            ax.plot(bb, Qind / q if q != 0 else Qind)
            ax.axvline(b, linestyle='--', linewidth=1)
            ax.set_xlabel('b [m]')
            ax.set_ylabel('Qind/q')
            ax.set_title(f'Inducerad laddning inom b: {self.induced_within(q, a, b):.3e} C')
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        a, b = (params['a'], params['b'])
        r = math.sqrt(max(b * b - a * a, 0))
        ax.plot([-1.2 * r, 1.2 * r], [0, 0], linewidth=2)
        ax.add_patch(Circle((0, a), 0.05 * a, fill=False, linewidth=2))
        ax.add_patch(Circle((0, -a), 0.05 * a, fill=False, linestyle='--'))
        ax.add_patch(Circle((0, 0), r, fill=False, linestyle=':'))
        ax.plot([0, r], [a, 0], linestyle='--', linewidth=1)
        ax.text(0.5 * r, 0.5 * a, 'b', ha='left')
        ax.text(0, a * 1.15, 'q', ha='center')
        ax.text(0, -a * 1.2, 'spegelladdning -q', ha='center')
        ax.set_aspect('equal')
        ax.set_xlim(-1.25 * max(r, a), 1.25 * max(r, a))
        ax.set_ylim(-1.4 * a, 1.5 * a)
        ax.set_axis_off()
        ax.set_title('Spegelladdningsgeometri')

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        a, b = (params['a'], params['b'])
        r = math.sqrt(max(b * b - a * a, 0))
        theta = np.linspace(0, 2 * np.pi, 80)
        rr = np.linspace(0, r, 30)
        R, T = np.meshgrid(rr, theta)
        X = R * np.cos(T)
        Y = R * np.sin(T)
        Z = np.zeros_like(X)
        ax.plot_surface(X, Y, Z, alpha=0.25, color='grey')
        ax.scatter([0], [0], [a], s=50)
        ax.scatter([0], [0], [-a], s=35, alpha=0.5)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_title('Planskiva motsvarande avstånd b')
