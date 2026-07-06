"""Kapitel 5: Stationära strömmar.

Uppgifter i detta kapitel (i menyordning):
    5.1    ConductiveCoaxialElectrodes
    5.2    CoaxialCableLeakage
    5.7    VariableSigmaCoaxialElectrolyte
    5.10   SemicylindricalRingResistor
    5.15   SteadyCurrentInterfaceCharge
"""

from ..core import *


class ConductiveCoaxialElectrodes(ProblemBase):
    name = '5.1 Ledande vätska mellan koaxiella elektroder'
    description = 'Likström genom en ledande vätska mellan långa koaxiella cylindrar.'
    parameters = [('sigma', 'Konduktivitet σ [S/m]', 1.0), ('ell', 'Längd ℓ [m]', 1.0), ('a', 'Inre radie a [m]', 0.01), ('b', 'Yttre radie b [m]', 0.05), ('U', 'Spänning U [V]', 10.0)]

    def validate(self, params):
        if params['sigma'] <= 0 or params['ell'] <= 0 or params['a'] <= 0 or (params['b'] <= params['a']):
            return 'Kräver σ, ℓ och a positiva samt b > a.'
        return None

    @staticmethod
    def current(sigma, ell, a, b, U):
        return 2 * math.pi * sigma * ell * U / math.log(b / a)

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        s, L, a, b, U = (params['sigma'], params['ell'], params['a'], params['b'], params['U'])
        R = np.linspace(a, b, 500)
        E = U / (R * math.log(b / a))
        J = s * E
        if mode == 'Magnitude':
            ax.plot(R, J)
            ax.set_ylabel('J_R [A/m²]')
            ax.set_title(f'Total ström I = {self.current(s, L, a, b, U):.3e} A')
        else:
            ax.plot(R, E)
            ax.set_ylabel('E_R [V/m]')
            ax.set_title('Radiellt elektriskt fält')
        ax.set_xlabel('R [m]')
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        a, b = (params['a'], params['b'])
        ax.add_patch(Circle((0, 0), b, fill=False, linewidth=2))
        ax.add_patch(Circle((0, 0), a, fill=False, linewidth=2))
        ax.text(0, 0, 'vätska', ha='center')
        ax.set_aspect('equal')
        ax.set_xlim(-1.2 * b, 1.2 * b)
        ax.set_ylim(-1.2 * b, 1.2 * b)
        ax.set_axis_off()
        ax.set_title('Ledande ringområde')

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        s, L, a, b, U = (params['sigma'], params['ell'], params['a'], params['b'], params['U'])
        aa = np.linspace(max(a * 0.4, 0.0001), a * 2, 50)
        bb = np.linspace(max(b * 0.6, a * 2.1), b * 1.6, 50)
        A, B = np.meshgrid(aa, bb)
        I = 2 * math.pi * s * L * U / np.log(B / A)
        I = np.where(B > A, I, np.nan)
        ax.plot_surface(A, B, I, cmap='viridis', alpha=0.9)
        ax.set_xlabel('a [m]')
        ax.set_ylabel('b [m]')
        ax.set_zlabel('I [A]')
        ax.set_title('Ström mot radier')

class CoaxialCableLeakage(ProblemBase):
    name = '5.2 Läckström i koaxialkabel'
    description = 'Läckström och effektförlust genom isolation med ändlig resistivitet i en koaxialkabel.'
    parameters = [('rho', 'Resistivitet ρ [Ω m]', 5000000.0), ('ell', 'Kabellängd ℓ [m]', 1.5), ('a', 'Innerledarens diameter a [m]', 0.001), ('b', 'Ytterledarens inre diameter b [m]', 0.004), ('V', 'Spänning V [V]', 120.0)]

    def validate(self, params):
        if params['rho'] <= 0 or params['ell'] <= 0 or params['a'] <= 0 or (params['b'] <= params['a']):
            return 'Kräver ρ, ℓ och a positiva samt b > a.'
        return None

    @staticmethod
    def leakage(rho, ell, a_diam, b_diam, V):
        I = 2 * math.pi * V * ell / (rho * math.log(b_diam / a_diam))
        P = V * I
        return (I, P)

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        rho, L, a, b, V = (params['rho'], params['ell'], params['a'], params['b'], params['V'])
        I, P = self.leakage(rho, L, a, b, V)
        rr = np.logspace(math.log10(rho / 20), math.log10(rho * 20), 400)
        II, PP = self.leakage(rr, L, a, b, V)
        if mode == 'Magnitude':
            ax.loglog(rr, PP)
            ax.set_ylabel('P [W]')
            ax.set_title(f'P = {P * 1000.0:.3g} mW')
        else:
            ax.loglog(rr, II)
            ax.set_ylabel('I [A]')
            ax.set_title(f'Läckström I = {I * 1000.0:.3g} mA')
        ax.axvline(rho, linestyle='--', linewidth=1)
        ax.set_xlabel('ρ [Ω m]')
        ax.grid(True, which='both', alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        a, b = (params['a'], params['b'])
        ax.add_patch(Circle((0, 0), b / 2, fill=False, linewidth=2))
        ax.add_patch(Circle((0, 0), a / 2, fill=True, alpha=0.25))
        ax.text(0, 0, 'isolering', ha='center', va='bottom')
        ax.set_aspect('equal')
        ax.set_xlim(-0.6 * b, 0.6 * b)
        ax.set_ylim(-0.6 * b, 0.6 * b)
        ax.set_axis_off()
        ax.set_title('Koaxialkabelns tvärsnitt')

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        rho, L, a, b, V = (params['rho'], params['ell'], params['a'], params['b'], params['V'])
        rr = np.logspace(math.log10(rho / 10), math.log10(rho * 10), 50)
        vv = np.linspace(0, 1.5 * abs(V), 50)
        R, VV = np.meshgrid(rr, vv)
        I = 2 * math.pi * VV * L / (R * math.log(b / a))
        P = VV * I
        ax.plot_surface(np.log10(R), VV, P, cmap='plasma', alpha=0.9)
        ax.set_xlabel('log10 ρ')
        ax.set_ylabel('V [V]')
        ax.set_zlabel('P [W]')
        ax.set_title('Effektförlustyta')

class VariableSigmaCoaxialElectrolyte(ProblemBase):
    name = '5.7 Koaxiell elektrolyt med σ(R)=k/R²'
    description = 'Resistans och fri laddningstäthet för en koaxiell elektrolyt vars konduktivitet varierar som k/R².'
    parameters = [('k', 'Konduktivitetskoefficient k [S·m]', 0.0001), ('eps_r', 'Relativ permittivitet εr', 80.0), ('ell', 'Längd ℓ [m]', 1.0), ('a', 'Inre radie a [m]', 0.01), ('b', 'Yttre radie b [m]', 0.05), ('U', 'Potentialskillnad U [V]', 1.0)]

    def validate(self, params):
        if params['k'] <= 0 or params['eps_r'] <= 0 or params['ell'] <= 0 or (params['a'] <= 0) or (params['b'] <= params['a']):
            return 'Kräver k, εr, ℓ och a positiva samt b > a.'
        return None

    @staticmethod
    def resistance(k, ell, a, b):
        return (b * b - a * a) / (4 * math.pi * k * ell)

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        k, er, L, a, b, U = (params['k'], params['eps_r'], params['ell'], params['a'], params['b'], params['U'])
        R = np.linspace(a, b, 500)
        E = 2 * U * R / (b * b - a * a)
        sig = k / R ** 2
        J = sig * E
        rho = 4 * EPS0 * er * U / (b * b - a * a)
        if mode == 'D':
            ax.plot(R, np.full_like(R, rho))
            ax.set_ylabel('ρfree [C/m³]')
            ax.set_title(f'ρfree = {rho:.3e} C/m³')
        else:
            ax.plot(R, E, label='E_R [V/m]')
            ax.plot(R, J, label='J_R [A/m²]')
            ax.legend()
            ax.set_ylabel('fält / strömtäthet')
            ax.set_title(f'R = {self.resistance(k, L, a, b):.3e} Ω')
        ax.set_xlabel('R [m]')
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        a, b = (params['a'], params['b'])
        ax.add_patch(Circle((0, 0), b, fill=False, linewidth=2))
        ax.add_patch(Circle((0, 0), a, fill=False, linewidth=2))
        ax.text(0, 0, 'σ=k/R²', ha='center')
        ax.set_aspect('equal')
        ax.set_xlim(-1.2 * b, 1.2 * b)
        ax.set_ylim(-1.2 * b, 1.2 * b)
        ax.set_axis_off()
        ax.set_title('Elektrolytiskt ringområde')

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        k, L, a, b = (params['k'], params['ell'], params['a'], params['b'])
        aa = np.linspace(max(0.3 * a, 0.0001), a * 2, 50)
        bb = np.linspace(max(1.2 * b, 2.2 * a), b * 2, 50)
        A, B = np.meshgrid(aa, bb)
        R = (B * B - A * A) / (4 * math.pi * k * L)
        R = np.where(B > A, R, np.nan)
        ax.plot_surface(A, B, R, cmap='viridis', alpha=0.9)
        ax.set_xlabel('a [m]')
        ax.set_ylabel('b [m]')
        ax.set_zlabel('R [Ω]')
        ax.set_title('Resistans mot geometri')

class SemicylindricalRingResistor(ProblemBase):
    name = '5.10 Halvcylindrisk ringresistor'
    description = 'Approximerad resistans mellan radialytorna i en halvringformad cylindrisk resistor.'
    parameters = [('sigma', 'Konduktivitet σ [S/m]', 1.0), ('h', 'Höjd h [m]', 0.02), ('a', 'Inre radie a [m]', 0.01), ('b', 'Yttre radie b [m]', 0.05)]

    def validate(self, params):
        if params['sigma'] <= 0 or params['h'] <= 0 or params['a'] <= 0 or (params['b'] <= params['a']):
            return 'Kräver σ, h och a positiva samt b > a.'
        return None

    @staticmethod
    def resistance(sigma, h, a, b):
        return math.pi / (sigma * h * math.log(b / a))

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        s, h, a, b = (params['sigma'], params['h'], params['a'], params['b'])
        bb = np.linspace(a * 1.05, max(b * 2, a * 1.1), 400)
        R = math.pi / (s * h * np.log(bb / a))
        ax.plot(bb, R)
        ax.axvline(b, linestyle='--', linewidth=1)
        ax.set_xlabel('b [m]')
        ax.set_ylabel('R [Ω]')
        ax.set_title(f'R = {self.resistance(s, h, a, b):.3g} Ω')
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        a, b = (params['a'], params['b'])
        th = np.linspace(0, math.pi, 200)
        ax.plot(a * np.cos(th), a * np.sin(th), linewidth=2)
        ax.plot(b * np.cos(th), b * np.sin(th), linewidth=2)
        ax.plot([a, b], [0, 0], linewidth=2)
        ax.plot([-a, -b], [0, 0], linewidth=2)
        ax.text(b * 0.85, 0.05 * b, 'A', ha='center')
        ax.text(-b * 0.85, 0.05 * b, 'B', ha='center')
        ax.set_aspect('equal')
        ax.set_xlim(-1.15 * b, 1.15 * b)
        ax.set_ylim(-0.15 * b, 1.15 * b)
        ax.set_axis_off()
        ax.set_title('Halvring')

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        s, h, a, b = (params['sigma'], params['h'], params['a'], params['b'])
        aa = np.linspace(max(0.3 * a, 0.0001), a * 2, 50)
        bb = np.linspace(max(1.2 * b, 2.2 * a), b * 2, 50)
        A, B = np.meshgrid(aa, bb)
        R = math.pi / (s * h * np.log(B / A))
        R = np.where(B > A, R, np.nan)
        ax.plot_surface(A, B, R, cmap='plasma', alpha=0.9)
        ax.set_xlabel('a [m]')
        ax.set_ylabel('b [m]')
        ax.set_zlabel('R [Ω]')
        ax.set_title('Resistansyta')

class SteadyCurrentInterfaceCharge(ProblemBase):
    name = '5.15 Ytladdning vid gränsyta i stationär ström'
    description = 'Fri ytladdning vid en stationär strömgränsyta mellan förlustbringande dielektrika.'
    parameters = [('alpha', 'Normal J-koefficient α [A/m²]', 1.0), ('beta', 'Tangentiell J-koefficient β [A/m²]', 0.5), ('eps1', 'Relativ permittivitet ε1', 2.0), ('eps2', 'Relativ permittivitet ε2', 5.0), ('sigma1', 'Konduktivitet σ1 [S/m]', 1.0), ('sigma2', 'Konduktivitet σ2 [S/m]', 4.0)]

    def validate(self, params):
        if min(params['eps1'], params['eps2'], params['sigma1'], params['sigma2']) <= 0:
            return 'Permittiviteter och konduktiviteter måste vara positiva.'
        return None

    @staticmethod
    def rho_s(alpha, eps1, eps2, sigma1, sigma2):
        return alpha * EPS0 * (eps2 / sigma2 - eps1 / sigma1)

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        alpha, beta, e1, e2, s1, s2 = (params['alpha'], params['beta'], params['eps1'], params['eps2'], params['sigma1'], params['sigma2'])
        s2vals = np.logspace(math.log10(s2 / 20), math.log10(s2 * 20), 400)
        rho = self.rho_s(alpha, e1, e2, s1, s2vals)
        ax.semilogx(s2vals, rho)
        ax.axhline(0, linewidth=1)
        ax.axvline(s2, linestyle='--', linewidth=1)
        ax.set_xlabel('σ2 [S/m]')
        ax.set_ylabel('ρs [C/m²]')
        ax.set_title(f'ρs = {self.rho_s(alpha, e1, e2, s1, s2):.3e} C/m²; zero if σ2/ε2 = σ1/ε1')
        ax.grid(True, which='both', alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        ax.plot([0, 0], [-1, 1], linewidth=2)
        ax.text(-0.5, 0.8, 'medium 1', ha='center')
        ax.text(0.5, 0.8, 'medium 2', ha='center')
        alpha, beta = (params['alpha'], params['beta'])
        norm = max(math.hypot(alpha, beta), 1e-30)
        ax.arrow(-0.7, -0.5, 0.5 * alpha / norm, 0.5 * beta / norm, head_width=0.05, length_includes_head=True)
        ax.text(-0.7, -0.6, 'J1', ha='center')
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.set_aspect('equal')
        ax.set_axis_off()
        ax.set_title('yz-gränsyta vid x=0')

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        alpha, e1, s1 = (params['alpha'], params['eps1'], params['sigma1'])
        e2 = np.linspace(1, 10, 50)
        s2 = np.logspace(-1, 1, 50)
        E2, S2 = np.meshgrid(e2, s2)
        R = self.rho_s(alpha, e1, E2, s1, S2)
        ax.plot_surface(E2, np.log10(S2), R, cmap='coolwarm', alpha=0.9)
        ax.set_xlabel('ε2')
        ax.set_ylabel('log10 σ2')
        ax.set_zlabel('ρs [C/m²]')
        ax.set_title('Ytladdningsyta vid gräns')
