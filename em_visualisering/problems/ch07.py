"""Kapitel 7: Magnetiska krafter, moment och flöden.

Uppgifter i detta kapitel (i menyordning):
    7.1    ElectronOrbitDipoleMoment
    7.2    CircularLoopTorqueUniformField
    7.3    DipoleDipoleTorque
    7.5    LoopDipoleApproximationError
    7.6    AntarcticIceFlux
    7.7    CopperWireMagneticLevitation
    7.10   InfiniteWireRectangularLoopFlux
"""

from ..core import *


class ElectronOrbitDipoleMoment(ProblemBase):
    name = '7.1 Elektron i cirkelbana'
    description = "En elektron med laddning -e i cirkelbana med radie a och hastighet v motsvarar en strömslinga. Det magnetiska dipolmomentet är m = -(1/2) e v a ẑ för positiv cirkulation relativt +z. Profilen visar |m| mot hastighet; kartan visar |m|(a, v)."
    parameters = [('v', 'Elektronhastighet v [m/s]', 2000000.0), ('a', 'Banradie a [m]', 5e-11), ('vmax', 'Största plottade hastighet vmax [m/s]', 10000000.0), ('amax', 'Kartans största radie amax [m]', 2e-10)]

    def validate(self, params):
        if params['v'] <= 0 or params['a'] <= 0:
            return 'v och a måste vara positiva.'
        if params['vmax'] < params['v'] or params['amax'] < params['a']:
            return 'Välj vmax >= v och amax >= a.'
        return None

    @staticmethod
    def _moment(v, a):
        return -0.5 * 1.602176634e-19 * np.asarray(v, dtype=float) * np.asarray(a, dtype=float)

    def plot(self, fig, params, mode):
        fig.clear()
        v0, a0, vmax, amax = (params['v'], params['a'], params['vmax'], params['amax'])
        if mode == 'Field':
            ax = fig.add_subplot(111)
            v = np.linspace(0, vmax, 500)
            m = np.abs(self._moment(v, a0))
            m0 = np.abs(self._moment(v0, a0))
            ax.plot(v, m)
            ax.scatter([v0], [m0], color='red', zorder=5)
            ax.set_xlabel('Hastighet v [m/s]')
            ax.set_ylabel('|m| [A·m²]')
            ax.set_title('Elektronbana: magnetiskt dipolmoment mot hastighet')
            ax.text(0.02, 0.98, f'Valt m = {self._moment(v0, a0):.3e} A·m²\nRiktning: -ẑ för positiv omloppsriktning', transform=ax.transAxes, va='top', fontsize=9)
            ax.grid(True, alpha=0.3)
        else:
            ax = fig.add_subplot(111)
            a = np.linspace(0, amax, 220)
            v = np.linspace(0, vmax, 180)
            AA, VV = np.meshgrid(a, v)
            MM = np.abs(self._moment(VV, AA))
            im = ax.pcolormesh(a, v, MM, cmap='viridis', shading='auto')
            fig.colorbar(im, ax=ax).set_label('|m| [A·m²]')
            ax.scatter([a0], [v0], color='red', s=30)
            ax.set_xlabel('Banradie a [m]')
            ax.set_ylabel('Hastighet v [m/s]')
            ax.set_title('Designkarta: |m|(a, v)')

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        t = np.linspace(0, 2 * np.pi, 260)
        ax.plot(np.cos(t), np.sin(t), color='black', linewidth=2)
        for radius, start, end, color in [(1, 0.5, 1.0, 'steelblue'), (1.15, 2.3, 1.8, 'darkorange')]:
            ax.annotate('', xy=(radius*np.cos(end), radius*np.sin(end)), xytext=(radius*np.cos(start), radius*np.sin(start)), arrowprops=dict(arrowstyle='->', lw=2, color=color))
        ax.text(1.15, .6, 'v', color='steelblue')
        ax.text(-.55, 1.15, 'I', color='darkorange')
        ax.text(0, 0, r'$\otimes$', ha='center', va='center', fontsize=26, color='steelblue')
        ax.text(0, -.4, 'm längs −z', ha='center', color='steelblue')
        ax.text(0, -1.35, 'Elektron moturs, ström medurs', ha='center', fontsize=9)
        ax.set(xlim=(-1.5, 1.5), ylim=(-1.5, 1.5), aspect='equal')
        ax.set_axis_off()
        ax.set_title('Elektronbana sedd från +z')

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        v0, a0, vmax, amax = (params['v'], params['a'], params['vmax'], params['amax'])
        a = np.linspace(0, amax, 80)
        v = np.linspace(0, vmax, 80)
        AA, VV = np.meshgrid(a, v)
        MM = np.abs(self._moment(VV, AA))
        surf = ax.plot_surface(AA, VV, MM, cmap='viridis', alpha=0.9, linewidth=0)
        fig.colorbar(surf, ax=ax, shrink=0.55, pad=0.12).set_label('|m| [A·m²]')
        ax.scatter([a0], [v0], [np.abs(self._moment(v0, a0))], color='red', s=35)
        ax.set_xlabel('a [m]')
        ax.set_ylabel('v [m/s]')
        ax.set_zlabel('|m| [A·m²]')
        ax.set_title('Magnetiskt moment för elektronbana')

class CircularLoopTorqueUniformField(ProblemBase):
    name = '7.2 Kraftmoment på cirkulär slinga i homogent fält'
    description = "En cirkulär strömslinga med radie a ligger i xy-planet i ett homogent magnetfält B = B x̂. Strömmen går positivt relativt +z. Profilen visar fördelat momentbidrag dT_y/dφ och dess kumulativa integral; kartan varierar signerade B och I för totala momentet T = π I B a² ŷ."
    parameters = [('I', 'Slingström I [A]', 2.0), ('B', 'Homogent fält B [T]', 0.3), ('a', 'Slingradie a [m]', 0.12), ('samples', 'Vinkelpunkter', 500), ('Imax', 'Kartans största ström Imax [A]', 6.0), ('Bmax', 'Kartans största fält Bmax [T]', 1.0)]

    def validate(self, params):
        if params['a'] <= 0 or params['samples'] < 60:
            return 'Kräver a > 0 och minst 60 vinkelpunkter.'
        if params['Imax'] <= 0 or params['Bmax'] <= 0:
            return 'Imax och Bmax måste vara positiva.'
        return None

    @staticmethod
    def _torque(I, B, a):
        return math.pi * np.asarray(I, dtype=float) * np.asarray(B, dtype=float) * np.asarray(a, dtype=float) ** 2

    def plot(self, fig, params, mode):
        fig.clear()
        I, B, a = (params['I'], params['B'], params['a'])
        if mode == 'Map':
            ax = fig.add_subplot(111)
            Ivals = np.linspace(-max(params['Imax'], abs(I)), max(params['Imax'], abs(I)), 220)
            Bvals = np.linspace(-max(params['Bmax'], abs(B)), max(params['Bmax'], abs(B)), 220)
            II, BB = np.meshgrid(Ivals, Bvals)
            TT = self._torque(II, BB, a)
            im = ax.pcolormesh(Ivals, Bvals, TT, cmap='RdBu_r', shading='auto')
            fig.colorbar(im, ax=ax).set_label('Ty [N·m]')
            ax.scatter([I], [B], color='red', s=30)
            ax.set_xlabel('Ström I [A]')
            ax.set_ylabel('Fält B [T]')
            ax.set_title('Signerat moment Ty = π I B a²')
            return
        ax = fig.add_subplot(111)
        n = int(round(params['samples']))
        phi = np.linspace(0.0, 2 * np.pi, n)
        dTy_dphi = I * B * a ** 2 * np.cos(phi) ** 2
        cumulative = np.zeros_like(phi)
        cumulative[1:] = np.cumsum(0.5 * (dTy_dphi[1:] + dTy_dphi[:-1]) * np.diff(phi))
        ax.plot(phi, dTy_dphi, label='dT_y/dφ')
        ax.plot(phi, cumulative, label='Kumulativt T_y(0→φ)')
        ax.axhline(self._torque(I, B, a), linestyle='--', color='black', linewidth=1, label=f'$T_y = {self._torque(I, B, a):.3e}$ N·m')
        ax.set_xlabel('Slingvinkel φ [rad]')
        ax.set_ylabel('Momenttäthet / kumulativt moment [N·m]')
        ax.set_title('Cirkulär slinga i homogent B: fördelat moment runt slingan')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=8)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        a, I, B = params['a'], params['I'], params['B']
        t = np.linspace(0, 2*np.pi, 300)
        ax.plot(a*np.cos(t), a*np.sin(t), color='black', lw=2)
        if I:
            t0, t1 = .7 - .2*np.sign(I), .7 + .2*np.sign(I)
            ax.annotate('', xy=(a*np.cos(t1), a*np.sin(t1)), xytext=(a*np.cos(t0), a*np.sin(t0)), arrowprops=dict(arrowstyle='->', lw=2, color='darkorange'))
        if B:
            for y in [-.6*a, 0, .6*a]:
                ax.annotate('', xy=(1.35*a + .3*a*np.sign(B), y), xytext=(1.35*a - .3*a*np.sign(B), y), arrowprops=dict(arrowstyle='->', color='steelblue', lw=2))
        torque = self._torque(I, B, a)
        if torque:
            ax.annotate('', xy=(0, np.sign(torque)*1.25*a), xytext=(0, 0), arrowprops=dict(arrowstyle='->', color='darkgreen', lw=2))
        ax.text(-1.3*a, 1.4*a, f'I = {I:g} A', color='darkorange', fontsize=9)
        ax.text(1.3*a, .85*a, f'Bx = {B:g} T', ha='center', color='steelblue', fontsize=9)
        ax.text(0, -1.65*a, f'Ty = {torque:.2e} N·m', ha='center', color='darkgreen', fontsize=9)
        ax.set(xlim=(-1.5*a, 2*a), ylim=(-1.9*a, 1.8*a), aspect='equal')
        ax.set_axis_off()
        ax.set_title('Sedd från +z: x åt höger, y uppåt')

    def draw_3d(self, fig, params, mode):
        fig.clear()
        I, B, a = (params['I'], params['B'], params['a'])
        ax = fig.add_subplot(111, projection='3d')
        if mode == 'Map':
            Ivals = np.linspace(-max(params['Imax'], abs(I)), max(params['Imax'], abs(I)), 80)
            Bvals = np.linspace(-max(params['Bmax'], abs(B)), max(params['Bmax'], abs(B)), 80)
            II, BB = np.meshgrid(Ivals, Bvals)
            TT = self._torque(II, BB, a)
            surf = ax.plot_surface(II, BB, TT, cmap='RdBu_r', alpha=0.92, linewidth=0)
            fig.colorbar(surf, ax=ax, shrink=0.55, pad=0.1).set_label('Ty [N·m]')
            ax.scatter([I], [B], [self._torque(I, B, a)], color='red', s=35)
            ax.set_xlabel('I [A]')
            ax.set_ylabel('B [T]')
            ax.set_zlabel('Ty [N·m]')
            ax.set_title('Designyta för moment på cirkulär slinga')
            return
        t = np.linspace(0, 2 * np.pi, 300)
        x = a * np.cos(t)
        y = a * np.sin(t)
        z = np.zeros_like(t)
        ax.plot(x, y, z, color='firebrick', linewidth=2.5)
        for y0 in np.linspace(-0.8 * a, 0.8 * a, 5):
            ax.quiver(-1.2 * a, y0, 0.0, np.sign(B) * 0.9 * a, 0.0, 0.0, color='steelblue', linewidth=1.3, arrow_length_ratio=0.15)
        torque = self._torque(I, B, a)
        ax.quiver(0.0, 0.0, 0.0, 0.0, np.sign(torque) * a, 0.0, color='darkgreen', linewidth=2.4, arrow_length_ratio=0.12)
        ax.text(0.0, 1.25 * a, 0.0, f'T = {torque:.2e} ŷ N·m', fontsize=8)
        ax.set_xlim(-1.5 * a, 1.5 * a)
        ax.set_ylim(-1.5 * a, 1.7 * a)
        ax.set_zlim(-1.0 * a, 1.0 * a)
        ax.set_xlabel('x [m]')
        ax.set_ylabel('y [m]')
        ax.set_zlabel('z [m]')
        ax.set_title('Slinga: B längs x, moment längs y (signerade)')

class DipoleDipoleTorque(ProblemBase):
    name = '7.3 Kraftmoment mellan två magnetiska dipoler'
    description = "Två små spolar har lika magnetiska dipolmoment m = m ẑ. Separationsvektorn har längd r och bildar vinkeln θ med +z. Momentets y-komponent i xz-geometrin är Ty = (3 μ0 m² / (8π r³)) sin(2θ); beloppet är |Ty|. Profilen visar signerat moment mot vinkel; kartan visar momentbelopp mot r och θ."
    parameters = [('m', 'Dipolmoment m [A·m²]', 1.0), ('r', 'Avstånd r [m]', 1.0), ('theta_deg', 'Vinkel θ [grad]', 45.0), ('rmax', 'Kartans största avstånd rmax [m]', 3.0)]

    def validate(self, params):
        if params['m'] == 0:
            return 'm får inte vara noll.'
        if params['r'] <= 0 or params['rmax'] <= 0:
            return 'r och rmax måste vara positiva.'
        if not 0 <= params['theta_deg'] <= 180:
            return 'θ måste ligga mellan 0 och 180 grader.'
        return None

    @staticmethod
    def _torque(m, r, theta_rad):
        return 3 * MU0 * np.asarray(m, dtype=float) ** 2 / (8 * np.pi * np.asarray(r, dtype=float) ** 3) * np.sin(2 * np.asarray(theta_rad, dtype=float))

    def plot(self, fig, params, mode):
        fig.clear()
        m, r = (params['m'], params['r'])
        theta_deg = params['theta_deg']
        theta = math.radians(theta_deg)
        T0 = self._torque(m, r, theta)
        if mode == 'Map':
            ax = fig.add_subplot(111)
            theta_vals = np.linspace(0.0, 180.0, 220)
            r_vals = np.geomspace(min(0.08 * params['rmax'], r), max(params['rmax'], r), 220)
            TT, RR = np.meshgrid(np.radians(theta_vals), r_vals)
            torque = np.abs(self._torque(m, RR, TT))
            im = ax.pcolormesh(theta_vals, r_vals, torque, cmap='viridis', shading='auto')
            fig.colorbar(im, ax=ax).set_label('|T| [N·m]')
            ax.scatter([theta_deg], [r], color='red', s=35)
            ax.set_xlabel('Vinkel θ [grad]')
            ax.set_ylabel('Avstånd r [m]')
            ax.set_title('Dipol–dipol-momentkarta')
            return
        ax = fig.add_subplot(111)
        theta_vals = np.linspace(0.0, 180.0, 500)
        torque = self._torque(m, r, np.radians(theta_vals))
        ax.plot(theta_vals, torque)
        ax.scatter([theta_deg], [T0], color='red', s=35)
        ax.axvline(45.0, linestyle='--', linewidth=1, color='grey', label='Max vid 45°')
        ax.set_xlabel('Vinkel θ [grad]')
        ax.axhline(0, color='black', lw=.8)
        ax.set_ylabel('Signerat moment Ty [N·m]')
        ax.set_title('Moment på ena dipolen från den andra')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=8)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        theta = math.radians(params['theta_deg'])
        p1 = np.array([math.sin(theta), math.cos(theta)])
        ax.plot([0, p1[0]], [0, p1[1]], '--', color='grey')
        for pos in [np.zeros(2), p1]:
            ax.scatter([pos[0]], [pos[1]], color='black', s=25)
            ax.annotate('', xy=pos + [0, .45*np.sign(params['m'])], xytext=pos, arrowprops=dict(arrowstyle='->', color='steelblue', lw=2))
        arc = np.linspace(0, theta, 100)
        ax.plot(.25*np.sin(arc), .25*np.cos(arc), color='darkorange')
        ax.text(.35*math.sin(theta/2), .35*math.cos(theta/2), 'θ', color='darkorange')
        ax.text(.5*p1[0]+.08, .5*p1[1], 'r')
        ax.axvline(0, color='grey', lw=.6)
        ax.text(-.35, 1.4, '+z ↑', fontsize=9)
        torque = self._torque(params['m'], params['r'], theta)
        ax.text(.45, -1.45, f'Ty = {torque:.2e} N·m', ha='center', fontsize=9)
        ax.set(xlim=(-.5, 1.6), ylim=(-1.6, 1.6), aspect='equal')
        ax.set_axis_off()
        ax.set_title('xz-planet: moment kring ±y')

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        m, r = (params['m'], params['r'])
        theta = math.radians(params['theta_deg'])
        p1 = np.array([r * math.sin(theta), 0.0, r * math.cos(theta)])
        ax.scatter([0, p1[0]], [0, p1[1]], [0, p1[2]], color=['black', 'firebrick'], s=40)
        ax.plot([0, p1[0]], [0, p1[1]], [0, p1[2]], color='grey', linestyle='--')
        ax.quiver(0, 0, 0, 0, 0, np.sign(m) * 0.7 * r, color='steelblue', linewidth=2, arrow_length_ratio=0.15)
        ax.quiver(p1[0], p1[1], p1[2], 0, 0, np.sign(m) * 0.7 * r, color='steelblue', linewidth=2, arrow_length_ratio=0.15)
        torque = self._torque(m, r, theta)
        Tmag = abs(torque)
        direction = 0 if abs(np.sin(2*theta)) < 1e-14 else np.sign(torque)
        ax.quiver(p1[0], p1[1], p1[2], 0, direction * 0.4 * r, 0, color='darkgreen', linewidth=2, arrow_length_ratio=0.2)
        ax.text(p1[0], p1[1], p1[2] + 0.15 * r, f'|T|={Tmag:.2e} N·m', fontsize=8)
        lim = 1.25 * max(r, 1e-06)
        ax.set_xlim(-0.3 * lim, lim)
        ax.set_ylim(-0.6 * lim, 0.6 * lim)
        ax.set_zlim(-1.8 * r, 1.8 * r)
        ax.set_xlabel('x [m]')
        ax.set_ylabel('y [m]')
        ax.set_zlabel('z [m]')
        ax.set_title('3-D-dipolgeometri och momentriktning')

class LoopDipoleApproximationError(ProblemBase):
    name = '7.5 Fel i dipolapproximation för slinga på axeln'
    description = 'Jämför exakt B på axeln för en cirkulär slinga med fjärrfältsapproximationen som magnetisk dipol.'
    parameters = [('a', 'Slingradie a [m]', 0.1), ('I', 'Ström I [A]', 1.0), ('tol', 'Feltolerans', 0.01)]

    def validate(self, params):
        if params['a'] <= 0 or params['tol'] <= 0:
            return 'a och tolerans måste vara positiva.'
        return None

    @staticmethod
    def z_for_tol(a, tol):
        return a / math.sqrt(math.expm1((2 / 3) * math.log1p(tol)))

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        a, I, tol = (params['a'], params['I'], params['tol'])
        ztol = self.z_for_tol(a, tol)
        z = np.geomspace(a, max(30*a, 1.3*ztol), 700)
        exact = MU0 * I * a * a / (2 * (z * z + a * a) ** 1.5)
        dip = MU0 * I * a * a / (2 * z ** 3)
        err = np.expm1(1.5 * np.log1p((a / z) ** 2))
        ztol = self.z_for_tol(a, tol)
        if mode == 'Map':
            ax.plot(z / a, exact, label='exakt')
            ax.plot(z / a, dip, '--', label='dipol')
            ax.set_ylabel('B_z [T]')
            ax.legend()
        else:
            ax.semilogy(z / a, err)
            ax.axhline(tol, linestyle='--', linewidth=1)
            ax.axvline(ztol / a, linestyle='--', linewidth=1)
            ax.set_ylabel('relativt fel')
        ax.set_xscale('log')
        ax.set_xlabel('|z|/a')
        ax.set_title(f'Fel < {tol:.3g} för |z| > {ztol / a:.2f} a')
        if I == 0:
            ax.text(.03, .04, 'I = 0: fälten är noll; felet visas som gränsvärde.', transform=ax.transAxes, fontsize=8)
        ax.grid(True, which='both', alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        ratio = self.z_for_tol(params['a'], params['tol']) / params['a']
        # Schematic side view: use a labelled break rather than clip distant thresholds.
        ax.plot([-1, 1], [0, 0], color='steelblue', lw=4)
        ax.plot([0, 0], [0, 2.5], '--', color='grey')
        ax.scatter([0], [2.5], color='black')
        ax.text(.15, 2.5, f'|z| = {ratio:.2f} a', va='center')
        ax.text(.15, 1.2, '⋯', fontsize=18)
        ax.text(0, -.3, 'Slinga sedd från sidan (bredd 2a)', ha='center', fontsize=9)
        ax.set(xlim=(-1.5, 2.5), ylim=(-.6, 3.1), aspect='equal')
        ax.set_axis_off()
        ax.set_title('Normalaxeln — schematisk avståndsskala')

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        a = params['a']
        th = np.linspace(0, 2 * np.pi, 200)
        ax.plot(a * np.cos(th), a * np.sin(th), np.zeros_like(th), linewidth=2)
        z = np.linspace(a, 15 * a, 80)
        ax.plot(np.zeros_like(z), np.zeros_like(z), z, label='axel')
        ax.scatter(np.zeros(10), np.zeros(10), z[::8], s=15, c=((1 + (a / z)**2)**1.5)[::8])
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_title('Axelpunkter färgade med Bdip/Bexakt')

class AntarcticIceFlux(ProblemBase):
    name = '7.6 Magnetiskt flöde genom Antarktis iskalott'
    description = "Söder om latitud 70°S antas ett 1000 m tjockt islager med vertikal yttervägg. Med jordens dipolmoment m fås flödet ut ur isen till luften: Φ = (μ0 m / (2 r_J)) sin²(θ_max), där θ_max = 90° − latitud. Profilen visar flöde mot latitudgräns; kartan varierar dipolmoment och latitud. Istjockleken påverkar inte summan av flödena genom ovansida och rand."
    parameters = [('m', 'Jordens dipolmoment m [A·m²]', 8.24e+22), ('rJ', 'Jordradie rJ [m]', 6370000.0), ('latitude_deg', 'Latitudgräns syd [grad]', 70.0), ('mmax', 'Kartans största dipolmoment [A·m²]', 1.4e+23)]

    def validate(self, params):
        if params['m'] <= 0 or params['rJ'] <= 0 or (params['mmax'] <= 0):
            return 'm, rJ och mmax måste vara positiva.'
        if not 0 <= params['latitude_deg'] <= 90:
            return 'latitud måste ligga mellan 0 och 90 grader syd, inklusive ändpunkterna.'
        return None

    @staticmethod
    def _theta_max_deg(latitude_deg):
        return 90.0 - np.asarray(latitude_deg, dtype=float)

    @staticmethod
    def _flux(m, rJ, latitude_deg):
        theta = np.radians(90.0 - np.asarray(latitude_deg, dtype=float))
        return MU0 * np.asarray(m, dtype=float) / (2 * np.asarray(rJ, dtype=float)) * np.sin(theta) ** 2

    def plot(self, fig, params, mode):
        fig.clear()
        m, rJ, lat = (params['m'], params['rJ'], params['latitude_deg'])
        phi0 = self._flux(m, rJ, lat)
        if mode == 'Map':
            ax = fig.add_subplot(111)
            lats = np.linspace(0.0, 90.0, 220)
            mvals = np.linspace(0, max(params['mmax'], m), 220)
            LL, MM = np.meshgrid(lats, mvals)
            Phi = self._flux(MM, rJ, LL)
            im = ax.pcolormesh(lats, mvals / 1e+23, Phi, cmap='viridis', shading='auto')
            fig.colorbar(im, ax=ax).set_label('Flöde Φ [Wb]')
            ax.scatter([lat], [m / 1e+23], color='red', s=35)
            ax.set_xlabel('Latitudgräns syd [grad]')
            ax.set_ylabel('Dipolmoment m [10²³ A·m²]')
            ax.set_title('Flöde från isen ut i luften')
            return
        ax = fig.add_subplot(111)
        lats = np.linspace(0.0, 90.0, 500)
        Phi = self._flux(m, rJ, lats)
        ax.plot(lats, Phi)
        ax.scatter([lat], [phi0], color='red', s=35)
        ax.axvline(lat, linestyle='--', color='grey', linewidth=1)
        ax.set_xlabel('Latitudgräns syd [grad]')
        ax.set_ylabel('Flöde Φ [Wb]')
        ax.set_title('Ackumulerat dipolflöde genom polariskalott')
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        theta = math.radians(90 - params['latitude_deg'])
        t = np.linspace(-theta, theta, 160)
        outer = 1.08  # Deliberately exaggerated thickness, not the cap height.
        x, z = np.sin(t), -np.cos(t)
        xo, zo = outer*x, outer*z
        ax.fill(np.r_[x, xo[::-1]], np.r_[z, zo[::-1]], color='lightskyblue', alpha=.6)
        ax.plot(x, z, color='black', lw=2, label='Botten mot jorden')
        ax.plot(xo, zo, color='steelblue', lw=2, label='Is–luft: ovansida + rand')
        for j in [0, -1]:
            ax.plot([x[j], xo[j]], [z[j], zo[j]], color='steelblue', lw=2)
            ax.plot([0, x[j]], [0, z[j]], ':', color='grey')
        ax.annotate('', xy=(0, -outer), xytext=(0, -1), arrowprops=dict(arrowstyle='<->', color='black'))
        ax.text(.04, -1.04, 'h (överdriven)', fontsize=9, va='center')
        ax.annotate('', xy=(0, -.65), xytext=(0, -.2), arrowprops=dict(arrowstyle='->', color='darkorange', lw=2))
        ax.text(.05, -.45, 'm mot syd', color='darkorange', fontsize=9)
        ax.text(-.65, -.18, f'θmax = {90-params["latitude_deg"]:g}°', fontsize=9)
        ax.set(xlim=(-1.2, 1.2), ylim=(-1.2, .05), aspect='equal')
        ax.set_axis_off()
        ax.legend(loc='upper right', fontsize=8)
        ax.set_title('Isvolym: botten + ovansida + rand')

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        lat = params['latitude_deg']
        m, rJ = (params['m'], params['rJ'])
        phi0 = self._flux(m, rJ, lat)
        theta_cap = math.radians(90.0 - lat)
        theta = np.linspace(np.pi - theta_cap, np.pi, 45)
        phi = np.linspace(0, 2 * np.pi, 70)
        T, P = np.meshgrid(theta, phi)
        X = np.sin(T) * np.cos(P)
        Y = np.sin(T) * np.sin(P)
        Z = np.cos(T)
        ax.plot_surface(X, Y, Z, color='lightskyblue', alpha=0.75, linewidth=0)
        ax.quiver(0, 0, 0, 0, 0, -1.2, color='steelblue', linewidth=2.5, arrow_length_ratio=0.12)
        ax.text(0, 0, -1.28, 'm', color='steelblue', ha='center')
        ax.text(0.1, 0.0, -0.15, f'Φ={phi0:.2e} Wb', fontsize=8)
        ax.set_xlim(-1.1, 1.1)
        ax.set_ylim(-1.1, 1.1)
        ax.set_zlim(-1.4, 0.2)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_title('Sydpolskalott och dipolriktning')

class CopperWireMagneticLevitation(ProblemBase):
    name = '7.7 Kraftbalans för koppartråd'
    description = "En horisontell koppartråd har likformig strömtäthet J = J x̂ i ett homogent fält B = B ŷ. Den magnetiska krafttätheten J×B pekar i +z och kan balansera tyngden ρg. Profilen visar krafttätheter mot B; kartan varierar J och ρ och visar B_req = ρg/J. Kraftbalans innebär inte automatiskt stabil svävning."
    parameters = [('J', 'Strömtäthet J [A/m²]', 3000000.0), ('rho_cu', 'Masstäthet ρ [kg/m³]', 8900.0), ('g', 'Tyngdacceleration g [m/s²]', 9.81), ('Bmax', 'Största plottade fält Bmax [T]', 0.08), ('Jmax', 'Kartans största strömtäthet Jmax [A/m²]', 8000000.0), ('rhomax', 'Kartans största densitet ρmax [kg/m³]', 12000.0)]

    def validate(self, params):
        if params['J'] <= 0 or params['rho_cu'] <= 0 or params['g'] <= 0:
            return 'J, ρ och g måste vara positiva.'
        if params['Bmax'] <= 0 or params['Jmax'] <= 0 or params['rhomax'] <= 0:
            return 'Bmax, Jmax och ρmax måste vara positiva.'
        return None

    @staticmethod
    def _required_B(J, rho_cu, g):
        return np.asarray(rho_cu, dtype=float) * np.asarray(g, dtype=float) / np.asarray(J, dtype=float)

    def plot(self, fig, params, mode):
        fig.clear()
        J, rho_cu, g = (params['J'], params['rho_cu'], params['g'])
        Breq = self._required_B(J, rho_cu, g)
        if mode == 'Map':
            ax = fig.add_subplot(111)
            Jvals = np.geomspace(min(.025*params['Jmax'], J), max(params['Jmax'], J), 220)
            rhos = np.linspace(0, max(params['rhomax'], rho_cu), 220)
            JJ, RR = np.meshgrid(Jvals, rhos)
            BB = self._required_B(JJ, RR, g)
            im = ax.pcolormesh(Jvals / 1000000.0, rhos, BB, cmap='viridis', shading='auto')
            fig.colorbar(im, ax=ax).set_label('Krävt B [T]')
            ax.scatter([J / 1000000.0], [rho_cu], color='red', s=30)
            ax.set_xlabel('Strömtäthet J [A/mm²]')
            ax.set_ylabel('Masstäthet ρ [kg/m³]')
            ax.set_title('Krävt B för magnetisk levitation: B = ρg/J')
            return
        ax = fig.add_subplot(111)
        B = np.linspace(0.0, max(params['Bmax'], 1.2*Breq), 500)
        f_mag = J * B
        f_grav = rho_cu * g * np.ones_like(B)
        f_net = f_mag - f_grav
        ax.plot(B, f_mag, label='Magnetisk krafttäthet JB')
        ax.plot(B, f_grav, label='Tyngdtäthet ρg')
        ax.plot(B, f_net, label='Netto vertikal krafttäthet')
        ax.axvline(Breq, linestyle='--', color='black', linewidth=1, label=f'Balans vid B = {Breq:.3e} T')
        ax.set_xlabel('Magnetisk flödestäthet B [T]')
        ax.set_ylabel('Krafttäthet [N/m³]')
        ax.set_title('Kraftbalans för koppartråd i homogent magnetfält')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=8)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        ax.add_patch(Rectangle((-1.2, -.15), 2.4, .3, fill=False, lw=2))
        ax.annotate('', xy=(.9, 0), xytext=(-.9, 0), arrowprops=dict(arrowstyle='->', lw=2, color='darkorange'))
        ax.text(-.9, .25, 'J längs +x', color='darkorange', fontsize=9)
        ax.text(0, .65, r'$\otimes$ B längs +y', color='steelblue', ha='center', fontsize=12)
        ax.annotate('', xy=(1.4, 1), xytext=(1.4, 0), arrowprops=dict(arrowstyle='->', lw=2, color='steelblue'))
        ax.text(1.4, 1.1, 'J×B', ha='center', color='steelblue')
        ax.annotate('', xy=(-1.4, -1), xytext=(-1.4, 0), arrowprops=dict(arrowstyle='->', lw=2, color='black'))
        ax.text(-1.4, -1.2, 'ρg', ha='center')
        ax.set(xlim=(-1.9, 1.9), ylim=(-1.4, 1.4), aspect='equal')
        ax.set_axis_off()
        ax.set_title('xz-planet: +z uppåt, +y in i bilden')

    def draw_3d(self, fig, params, mode):
        fig.clear()
        J, rho_cu, g = (params['J'], params['rho_cu'], params['g'])
        Breq = self._required_B(J, rho_cu, g)
        ax = fig.add_subplot(111, projection='3d')
        if mode == 'Map':
            Jvals = np.geomspace(min(.025*params['Jmax'], J), max(params['Jmax'], J), 80)
            rhos = np.linspace(0, max(params['rhomax'], rho_cu), 80)
            JJ, RR = np.meshgrid(Jvals, rhos)
            BB = self._required_B(JJ, RR, g)
            surf = ax.plot_surface(JJ / 1000000.0, RR, BB, cmap='viridis', alpha=0.92, linewidth=0)
            fig.colorbar(surf, ax=ax, shrink=0.55, pad=0.1).set_label('Krävt B [T]')
            ax.scatter([J / 1000000.0], [rho_cu], [Breq], color='red', s=35)
            ax.set_xlabel('J [A/mm²]')
            ax.set_ylabel('ρ [kg/m³]')
            ax.set_zlabel('B [T]')
            ax.set_title('Designyta för trådlevitation')
            return
        _draw_box(ax, -0.8, 0.8, -0.08, 0.08, -0.08, 0.08, color='peru', alpha=0.8)
        ax.quiver(-0.7, 0.0, 0.0, 1.2, 0.0, 0.0, color='firebrick', linewidth=2, arrow_length_ratio=0.12)
        ax.quiver(0.0, -0.7, 0.0, 0.0, 1.2, 0.0, color='steelblue', linewidth=2, arrow_length_ratio=0.12)
        ax.quiver(0.55, 0.0, 0.0, 0.0, 0.0, 0.9, color='darkgreen', linewidth=2.4, arrow_length_ratio=0.12)
        ax.quiver(-0.55, 0.0, 0.0, 0.0, 0.0, -0.9, color='black', linewidth=2.4, arrow_length_ratio=0.12)
        ax.text(0.15, 0.0, 0.12, f'B_req = {Breq:.3e} T', fontsize=8)
        ax.set_xlim(-1.0, 1.0)
        ax.set_ylim(-1.0, 1.0)
        ax.set_zlim(-1.0, 1.0)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_title('3-D-kraftbalans på koppartråd')

class InfiniteWireRectangularLoopFlux(ProblemBase):
    name = '7.10 Flöde genom rektangulär slinga nära oändlig ledare'
    description = 'Magnetiskt flöde genom en rektangulär slinga i planet z=c från en oändlig ledare längs x.'
    parameters = [('I', 'Ledningsström I [A]', 10.0), ('a', 'Slingans längd i x-led, a [m]', 0.2), ('b', 'Slingans bredd i y-led, b [m]', 0.1), ('c', 'Höjd z=c [m]', 0.05)]

    def validate(self, params):
        if params['a'] <= 0 or params['b'] <= 0 or params['c'] <= 0:
            return 'a, b och c måste vara positiva.'
        return None

    @staticmethod
    def flux(I, a, b, c):
        return MU0 * I * a / (4 * math.pi) * math.log1p((b / c) ** 2)

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        I, a, b, c = (params['I'], params['a'], params['b'], params['c'])
        y = np.linspace(0, b, 400)
        Bz = MU0 * I * y / (2 * math.pi * (y * y + c * c))
        if mode == 'Map':
            X, Y = np.meshgrid(np.linspace(0, a, 100), y)
            B = MU0 * I * Y / (2 * math.pi * (Y * Y + c * c))
            _show_scalar_map(ax, fig, X, Y, B, title='B_z över slingan', xlabel='x [m]', ylabel='y [m]', cbar_label='B_z [T]', scale='linear', contours=True)
        else:
            ax.plot(y, Bz)
            ax.set_xlabel('y [m]')
            ax.set_ylabel('B_z [T]')
            ax.set_title(f'Flöde Φ = {self.flux(I, a, b, c):.3e} Wb')
            ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        b, c, I = params['b'], params['c'], params['I']
        span = max(b, c)
        ax.plot([0, b], [c, c], color='steelblue', lw=3, label='Slinga i z=c (längd a längs x)')
        symbol = r'$\odot$' if I > 0 else r'$\otimes$' if I < 0 else '0'
        ax.text(0, 0, symbol, ha='center', va='center', fontsize=22)
        ax.text(.12*span, 0, 'Ledare längs x', va='center', fontsize=9)
        ax.plot([0, 0], [0, c], ':', color='grey')
        ax.annotate('', xy=(.5*b, c+.3*span), xytext=(.5*b, c), arrowprops=dict(arrowstyle='->', lw=2))
        ax.text(.5*b+.06*span, c+.25*span, 'n = +z', fontsize=9)
        ax.set(xlim=(-.25*span, b+.3*span), ylim=(-.2*span, c+.5*span), aspect='equal', xlabel='y [m]', ylabel='z [m]')
        ax.legend(loc='upper left', fontsize=8)
        ax.set_title('yz-snitt: x ut ur bilden')

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        a, b, c = (params['a'], params['b'], params['c'])
        ax.plot([0, a, a, 0, 0], [0, 0, b, b, 0], [c, c, c, c, c], linewidth=2)
        ax.plot([-0.2 * a, 1.2 * a], [0, 0], [0, 0], linewidth=3)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_title('Ledare och upphöjd slinga')
