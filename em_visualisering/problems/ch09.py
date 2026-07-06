"""Kapitel 9: Induktans och induktion.

Uppgifter i detta kapitel (i menyordning):
    9.2    MutualInductanceParallelWiresSquare
    9.4    MutualInductanceCoaxialLoops
    9.6    OpenSecondaryTransformerVoltage
    9.13   MovingLoopFieldWork
    9.14   MovingLoopDipoleEmf
"""

from ..core import *


class MutualInductanceParallelWiresSquare(ProblemBase):
    name = '9.2 Ömsesidig induktans: parallella ledare och kvadrat'
    description = 'Ömsesidig induktans mellan en tvåledarslinga och en kvadratisk slinga tangent till båda ledarna.'
    parameters = [('d', 'Ledarseparation d [m]', 0.1)]

    def validate(self, params):
        if params['d'] <= 0:
            return 'd måste vara positivt.'
        return None

    @staticmethod
    def mutual(d):
        return 2 * d * MU0 * math.log(2) / math.pi

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        d = params['d']
        D = np.linspace(0, 3 * d, 300)
        M = self.mutual(D)
        ax.plot(D, M * 1000000000.0)
        ax.scatter([d], [self.mutual(d) * 1000000000.0])
        ax.set_xlabel('d [m]')
        ax.set_ylabel('M [nH]')
        ax.set_title(f'M = {self.mutual(d):.3e} H')
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        d = params['d']
        s = d / math.sqrt(2)
        ax.plot([-0.2 * d, 1.2 * d], [0, 0], linewidth=2)
        ax.plot([-0.2 * d, 1.2 * d], [d, d], linewidth=2)
        diamond = np.array([[d / 2, 0], [d, d / 2], [d / 2, d], [0, d / 2], [d / 2, 0]])
        ax.plot(diamond[:, 0], diamond[:, 1], linewidth=2)
        ax.set_aspect('equal')
        ax.set_xlim(-0.2 * d, 1.2 * d)
        ax.set_ylim(-0.2 * d, 1.2 * d)
        ax.set_axis_off()
        ax.set_title('Tvåledarslinga och kvadratisk slinga')

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        d = params['d']
        x = np.linspace(-0.2 * d, 1.2 * d, 2)
        ax.plot(x, 0 * x, 0 * x)
        ax.plot(x, 0 * x + d, 0 * x)
        diamond = np.array([[d / 2, 0, 0], [d, d / 2, 0], [d / 2, d, 0], [0, d / 2, 0], [d / 2, 0, 0]])
        ax.plot(diamond[:, 0], diamond[:, 1], diamond[:, 2])
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_title('Slingor i samma plan')

class MutualInductanceCoaxialLoops(ProblemBase):
    name = '9.4 Ömsesidig induktans för koaxiella cirkulära slingor'
    description = 'Approximerad ömsesidig induktans för två koaxiella slingor då a≪b och d≫a.'
    parameters = [('a', 'Lilla slingans radie a [m]', 0.02), ('b', 'Stora slingans radie b [m]', 0.1), ('d', 'Axiellt avstånd d [m]', 0.3)]

    def validate(self, params):
        if min(params['a'], params['b'], params['d']) <= 0:
            return 'a, b och d måste vara positiva.'
        return None

    @staticmethod
    def mutual(a, b, d):
        return MU0 * math.pi * a * a * b * b / (2 * (d * d + b * b) ** 1.5)

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        a, b, d = (params['a'], params['b'], params['d'])
        dd = np.linspace(0.02 * b, 5 * max(d, b), 500)
        M = self.mutual(a, b, dd)
        ax.plot(dd, M * 1000000000.0)
        ax.axvline(d, linestyle='--', linewidth=1)
        ax.set_xlabel('d [m]')
        ax.set_ylabel('M [nH]')
        ax.set_title(f'M = {self.mutual(a, b, d):.3e} H')
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        a, b, d = (params['a'], params['b'], params['d'])
        ax.add_patch(Circle((0, 0), b, fill=False, linewidth=2))
        ax.add_patch(Circle((d, 0), a, fill=False, linewidth=2))
        ax.plot([0, d], [0, 0], linestyle='--')
        ax.text(d / 2, 0.08 * max(b, d), 'd', ha='center')
        ax.set_aspect('equal')
        ax.set_xlim(-1.2 * b, d + 1.5 * a)
        ax.set_ylim(-1.2 * b, 1.2 * b)
        ax.set_axis_off()
        ax.set_title('Tvärsnitt av koaxiella slingor')

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        a, b, d = (params['a'], params['b'], params['d'])
        th = np.linspace(0, 2 * np.pi, 200)
        ax.plot(b * np.cos(th), b * np.sin(th), np.zeros_like(th))
        ax.plot(a * np.cos(th), a * np.sin(th), np.full_like(th, d))
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_title('Koaxiella slingor')

class OpenSecondaryTransformerVoltage(ProblemBase):
    name = '9.6 Tomgångsspänning i transformatorns sekundärlindning'
    description = 'Tomgångsspänning i sekundärlindningen inducerad av i1(t)=I0 cos(ωt) i en linjär järnkärna.'
    parameters = [('N1', 'Primärvarv N1', 100.0), ('N2', 'Sekundärvarv N2', 800.0), ('I0', 'Primärströmmens amplitud I0 [A]', 1.0), ('omega', 'Vinkelfrekvens ω [rad/s]', 2 * math.pi * 50), ('ell', 'Magnetisk väglängd ℓ [m]', 0.4), ('S', 'Kärnans tvärsnitt S [m²]', 0.00063), ('mu_r', 'Relativ permeabilitet µr', 2000.0)]

    def validate(self, params):
        if min(params['N1'], params['N2'], params['omega'], params['ell'], params['S'], params['mu_r']) <= 0:
            return 'Varvtal, ω, ℓ, S och µr måste vara positiva.'
        return None

    @staticmethod
    def amp(N1, N2, I0, omega, ell, S, mur):
        return MU0 * mur * N1 * N2 * S * I0 * omega / ell

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        N1, N2, I0, w, L, S, mur = (params['N1'], params['N2'], params['I0'], params['omega'], params['ell'], params['S'], params['mu_r'])
        T = 2 * math.pi / w
        t = np.linspace(0, 2 * T, 600)
        u = self.amp(N1, N2, I0, w, L, S, mur) * np.sin(w * t)
        ax.plot(t * 1000.0, u)
        ax.set_xlabel('t [ms]')
        ax.set_ylabel('u2 [V]')
        ax.set_title(f'Spänningsamplitud = {np.max(np.abs(u)):.3g} V')
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        ax.add_patch(Rectangle((-0.7, -0.45), 1.4, 0.9, fill=False, linewidth=6, alpha=0.45))
        ax.text(-0.55, 0, 'N1', ha='center')
        ax.text(0.55, 0, 'N2 öppen', ha='center')
        ax.set_aspect('equal')
        ax.set_xlim(-1, 1)
        ax.set_ylim(-0.7, 0.7)
        ax.set_axis_off()
        ax.set_title('Ideal magnetisk krets')

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        N1, N2, I0, w, L, S = (params['N1'], params['N2'], params['I0'], params['omega'], params['ell'], params['S'])
        mur = np.linspace(100, 3000, 50)
        freq = np.linspace(10, 200, 50)
        MU, F = np.meshgrid(mur, freq)
        U = self.amp(N1, N2, I0, 2 * math.pi * F, L, S, MU)
        ax.plot_surface(MU, F, U, cmap='viridis', alpha=0.9)
        ax.set_xlabel('µr')
        ax.set_ylabel('f [Hz]')
        ax.set_zlabel('Uamp [V]')
        ax.set_title('Sekundärspänningens amplitud')

class MovingLoopFieldWork(ProblemBase):
    name = '9.13 Arbete då kvadratisk slinga dras genom B-fält'
    description = 'Arbete som krävs för att dra en resistiv kvadratisk slinga med konstant hastighet genom ett ändligt homogent B-fältsområde.'
    parameters = [('B', 'Magnetisk flödestäthet B [T]', 1.0), ('a', 'Slingans sida a [m]', 0.1), ('v', 'Hastighet v [m/s]', 10.0), ('R_ohm', 'Slingans resistans RΩ [Ω]', 0.05), ('ell', 'Fältområdets bredd ℓ [m]', 0.3)]

    def validate(self, params):
        if min(params['a'], params['v'], params['R_ohm'], params['ell']) <= 0:
            return 'a, v, RΩ och ℓ måste vara positiva.'
        return None

    @staticmethod
    def work(B, a, v, R):
        return 2 * B * B * a ** 3 * v / R

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        B, a, v, R, L = (params['B'], params['a'], params['v'], params['R_ohm'], params['ell'])
        x = np.linspace(-a, L + a, 800)
        overlap = np.clip(x + a, 0, a) - np.clip(x - L, 0, a)
        P = np.where((x > -a) & (x < 0) | (x > L - a) & (x < L), (B * a * v) ** 2 / R, 0.0)
        Wcum = np.cumsum(P) * (x[1] - x[0]) / v
        if mode == 'Map':
            ax.plot(x, Wcum)
            ax.set_ylabel('kumulativt W [J]')
        else:
            ax.plot(x, P)
            ax.set_ylabel('mekanisk effekt [W]')
        ax.set_xlabel('främre kantens läge x [m]')
        ax.set_title(f'Totalt arbete W = {self.work(B, a, v, R):.3g} J')
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        a, L = (params['a'], params['ell'])
        ax.add_patch(Rectangle((0, -0.6 * a), L, 1.2 * a, alpha=0.2))
        ax.add_patch(Rectangle((-1.2 * a, -0.5 * a), a, a, fill=False, linewidth=2))
        ax.arrow(-0.1 * a, 0, 0.5 * a, 0, head_width=0.05 * a, length_includes_head=True)
        ax.text(0.5 * L, 0.65 * a, 'B-område', ha='center')
        ax.set_aspect('equal')
        ax.set_xlim(-1.5 * a, L + 0.5 * a)
        ax.set_ylim(-0.8 * a, 0.9 * a)
        ax.set_axis_off()
        ax.set_title('Slinga går in i/ut ur fältet')

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        B, a, v, R = (params['B'], params['a'], params['v'], params['R_ohm'])
        bb = np.linspace(0, 2 * max(B, 0.1), 50)
        vv = np.linspace(0.1, 2 * v, 50)
        BB, VV = np.meshgrid(bb, vv)
        W = self.work(BB, a, VV, R)
        ax.plot_surface(BB, VV, W, cmap='plasma', alpha=0.9)
        ax.set_xlabel('B [T]')
        ax.set_ylabel('v [m/s]')
        ax.set_zlabel('W [J]')
        ax.set_title('Arbetets skalning')

class MovingLoopDipoleEmf(ProblemBase):
    name = '9.14 EMS i rörlig slinga nära magnetisk dipol'
    description = 'Elektromotorisk spänning i en liten slinga som rör sig längs axeln till en magnetisk dipol: ε = 3µ0 m a² v/(2z⁴).'
    parameters = [('m', 'Dipolmoment m [A m²]', 1.0), ('a', 'Slingradie a [m]', 0.01), ('v', 'Hastighet v [m/s]', 1.0), ('zmin', 'Minsta z [m]', 0.1), ('zmax', 'Största z [m]', 1.0)]

    def validate(self, params):
        if min(params['a'], params['zmin'], params['zmax']) <= 0 or params['zmax'] <= params['zmin']:
            return 'Kräver positiva a, zmin och zmax med zmax > zmin.'
        return None

    @staticmethod
    def emf(m, a, v, z):
        return MU0 * m * a * a * 3 * v / (2 * z ** 4)

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        m, a, v, z0, z1 = (params['m'], params['a'], params['v'], params['zmin'], params['zmax'])
        z = np.linspace(z0, z1, 500)
        eps = self.emf(m, a, v, z)
        ax.plot(z, eps)
        ax.set_xlabel('z [m]')
        ax.set_ylabel('εemf [V]')
        ax.set_title('Rörelse- och transformatorberäkning ger samma EMS')
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        z0, z1, a = (params['zmin'], params['zmax'], params['a'])
        ax.arrow(0, 0, 0, 0.3 * z1, head_width=0.04 * z1, length_includes_head=True)
        ax.text(0.03 * z1, 0.15 * z1, 'm', va='center')
        ax.add_patch(Circle((0, z0), 3 * a, fill=False))
        ax.arrow(0, z0, 0, 0.2 * (z1 - z0), head_width=0.03 * z1, length_includes_head=True)
        ax.text(0.05 * z1, z0, 'loop', va='center')
        ax.set_aspect('equal')
        ax.set_xlim(-0.2 * z1, 0.3 * z1)
        ax.set_ylim(-0.1 * z1, 1.1 * z1)
        ax.set_axis_off()
        ax.set_title('Dipolaxel')

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        m, a, v, z0, z1 = (params['m'], params['a'], params['v'], params['zmin'], params['zmax'])
        z = np.linspace(z0, z1, 100)
        eps = self.emf(m, a, v, z)
        _surface_of_revolution(ax, 0.2 * a * np.ones_like(z), z, eps, title='EMS mot axiellt läge', zlabel='z [m]')
