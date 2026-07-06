"""Kapitel 10: Förskjutningsström.

Uppgifter i detta kapitel (i menyordning):
    10.2   DisplacementCurrentCapacitor
    10.3   RadialChargeExpansionMaxwellTest
"""

from ..core import *


class DisplacementCurrentCapacitor(ProblemBase):
    name = '10.2 Förskjutningsström i driven kondensator'
    description = 'För i(t)=I0 sin(ωt) är förskjutningsströmtätheten JF=I0 sin(ωt)/A.'
    parameters = [('I0', 'Strömamplitud I0 [A]', 1.0), ('omega', 'Vinkelfrekvens ω [rad/s]', 2 * math.pi * 50), ('A', 'Plattarea A [m²]', 0.01)]

    def validate(self, params):
        if params['omega'] <= 0 or params['A'] <= 0:
            return 'ω och A måste vara positiva.'
        return None

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        I0, w, A = (params['I0'], params['omega'], params['A'])
        T = 2 * math.pi / w
        t = np.linspace(0, 2 * T, 600)
        J = I0 * np.sin(w * t) / A
        ax.plot(t * 1000.0, J)
        ax.set_xlabel('t [ms]')
        ax.set_ylabel('JF [A/m²]')
        ax.set_title(f'JF-amplitud = {abs(I0) / A:.3g} A/m²')
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        ax.add_patch(Rectangle((-0.5, 0.15), 1, 0.06, fill=False, linewidth=2))
        ax.add_patch(Rectangle((-0.5, -0.15), 1, 0.06, fill=False, linewidth=2))
        ax.arrow(0, -0.06, 0, 0.14, head_width=0.05, length_includes_head=True)
        ax.text(0.1, 0, 'JF', va='center')
        ax.set_xlim(-0.8, 0.8)
        ax.set_ylim(-0.4, 0.4)
        ax.set_aspect('equal')
        ax.set_axis_off()
        ax.set_title('Förskjutningsström genom gapet')

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        I0, w, A = (params['I0'], params['omega'], params['A'])
        t = np.linspace(0, 2 * math.pi / w, 100)
        area = np.linspace(0.2 * A, 2 * A, 50)
        T, AR = np.meshgrid(t, area)
        J = I0 * np.sin(w * T) / AR
        ax.plot_surface(T * 1000.0, AR, J, cmap='coolwarm', alpha=0.9)
        ax.set_xlabel('t [ms]')
        ax.set_ylabel('A [m²]')
        ax.set_zlabel('JF [A/m²]')
        ax.set_title('JF(t,A)')

class RadialChargeExpansionMaxwellTest(ProblemBase):
    name = '10.3 Radiellt expanderande laddning – Maxwelltest'
    description = 'Exempel på radiellt symmetriskt expanderande laddningsmoln: JF = −J och B=0 uppfyller Maxwells ekvationer.'
    parameters = [('rho0', 'Ursprunglig central densitet ρ0 [C/m³]', 1e-06), ('s0', 'Ursprunglig bredd s0 [m]', 0.1), ('v', 'Expansionshastighet ds/dt [m/s]', 0.05), ('t', 'Tid t [s]', 1.0), ('rmax', 'Största radie [m]', 0.6)]

    def validate(self, params):
        if params['s0'] <= 0 or params['rmax'] <= 0:
            return 's0 och rmax måste vara positiva.'
        return None

    @staticmethod
    def profiles(r, rho0, s0, v, t):
        s = s0 + v * t
        rho = rho0 * (s0 / s) ** 3 * np.exp(-(r / s) ** 2)
        drhodt = rho * v * (-3 / s + 2 * r * r / s ** 3)
        integrand = drhodt * r * r
        integ = np.zeros_like(r)
        if len(r) > 1:
            integ[1:] = np.cumsum(0.5 * (integrand[1:] + integrand[:-1]) * np.diff(r))
        J = -integ / np.maximum(r * r, 1e-30)
        J[0] = 0.0
        return (rho, J, -J)

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        rho0, s0, v, t, rmax = (params['rho0'], params['s0'], params['v'], params['t'], params['rmax'])
        r = np.linspace(0, rmax, 800)
        rho, J, JF = self.profiles(r, rho0, s0, v, t)
        if mode == 'Map':
            ax.plot(r, J, label='J_r')
            ax.plot(r, JF, '--', label='JF,r = -J_r')
            ax.set_ylabel('strömtäthet [A/m²]')
            ax.legend()
        else:
            ax.plot(r, rho)
            ax.set_ylabel('ρ(r,t) [C/m³]')
        ax.set_xlabel('r [m]')
        ax.set_title('Radiell symmetri tillåter B = 0 trots att J ≠ 0')
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        rmax = params['rmax']
        for rad in np.linspace(0.2 * rmax, rmax, 5):
            ax.add_patch(Circle((0, 0), rad, fill=False, alpha=0.25))
        for th in np.linspace(0, 2 * np.pi, 8, endpoint=False):
            ax.arrow(0, 0, 0.8 * rmax * math.cos(th), 0.8 * rmax * math.sin(th), head_width=0.04 * rmax, length_includes_head=True, alpha=0.5)
        ax.set_aspect('equal')
        ax.set_xlim(-1.1 * rmax, 1.1 * rmax)
        ax.set_ylim(-1.1 * rmax, 1.1 * rmax)
        ax.set_axis_off()
        ax.set_title('Rent radiell ström: ingen utvald B-riktning')

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        rho0, s0, v, t, rmax = (params['rho0'], params['s0'], params['v'], params['t'], params['rmax'])
        r = np.linspace(0, rmax, 120)
        rho, J, JF = self.profiles(r, rho0, s0, v, t)
        scalar = J if mode == 'Map' else rho
        _surface_of_revolution(ax, 0.04 * rmax * np.ones_like(r), r, scalar, title='Radiell profil roterad', zlabel='r [m]')
