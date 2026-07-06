"""Kapitel 8: Magnetiska material och kretsar.

Uppgifter i detta kapitel (i menyordning):
    8.1    PermanentMagnetAirGapBHCurve
    8.2    NonlinearIronMagneticCircuit
    8.4    MagneticBridgeCircuit
    8.5    CurrentCarryingMagneticTube
    8.6    HorseshoeMagnetAnchorForce
    8.12   PermanentlyMagnetizedCylinderAxis
    8.13   MagnetizationCurrentsCylinder
"""

from ..core import *


class PermanentMagnetAirGapBHCurve(ProblemBase):
    name = '8.1 Permanentmagnetisk ring med luftgap'
    description = 'Löser arbetspunkten som skärningen mellan materialkurva och lastlinje för en permanentmagnetisk ring med litet luftgap, eventuellt med spole.'
    parameters = [('ell', 'Magnetlängd ℓ [m]', 0.2), ('d', 'Luftgap d [m]', 0.001), ('N', 'Spolvarv N', 100.0), ('I', 'Spolström I [A]', 0.0)]
    Btab = np.array([0.0, 0.6, 0.83, 1.0, 1.2])
    Htab = np.array([-5000, -4000, -3000, -2000, 0.0])

    def validate(self, params):
        if params['ell'] <= params['d'] or params['d'] <= 0:
            return 'Kräver ℓ > d > 0.'
        return None

    @classmethod
    def Hmat(cls, B):
        return np.interp(B, cls.Btab, cls.Htab)

    @classmethod
    def solve_B(cls, ell, d, N, I):
        F = N * I
        Bs = np.linspace(cls.Btab[0], cls.Btab[-1], 2001)
        resid = cls.Hmat(Bs) * (ell - d) + Bs * d / MU0 - F
        idx = np.argmin(np.abs(resid))
        return Bs[idx]

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        ell, d, N, I = (params['ell'], params['d'], params['N'], params['I'])
        B = np.linspace(0, 1.2, 400)
        Hload = (N * I - B * d / MU0) / (ell - d)
        B0 = self.solve_B(ell, d, N, I)
        ax.plot(self.Htab, self.Btab, 'o-', label='materialkurva')
        ax.plot(Hload, B, label='lastlinje')
        ax.scatter([self.Hmat(B0)], [B0], zorder=3, label=f'B={B0:.3g} T')
        ax.set_xlabel('H i magneten [A/m]')
        ax.set_ylabel('B [T]')
        ax.set_title('Permanentmagnetens arbetspunkt')
        ax.legend()
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        ax.add_patch(Circle((0, 0), 1, fill=False, linewidth=8, alpha=0.45))
        ax.plot([0.83, 1.15], [0, 0], color='white', linewidth=12)
        ax.text(1.1, 0.15, 'gap d', ha='center')
        ax.text(0, 0, 'magnetring', ha='center')
        ax.set_aspect('equal')
        ax.set_xlim(-1.3, 1.3)
        ax.set_ylim(-1.3, 1.3)
        ax.set_axis_off()
        ax.set_title('Magnetisk krets')

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        ell, d, N = (params['ell'], params['d'], params['N'])
        I = np.linspace(0, 3, 60)
        D = np.linspace(0.2 * d, 3 * d, 60)
        IG, DG = np.meshgrid(I, D)
        B = np.vectorize(self.solve_B)(ell, DG, N, IG)
        ax.plot_surface(IG, DG * 1000.0, B, cmap='viridis', alpha=0.9)
        ax.set_xlabel('I [A]')
        ax.set_ylabel('d [mm]')
        ax.set_zlabel('B [T]')
        ax.set_title('Flödestäthet i gapet')

class NonlinearIronMagneticCircuit(ProblemBase):
    name = '8.2 Ickelinjär magnetisk krets av järn'
    description = 'Magnetisk krets med ett luftgap och ickelinjärt järn enligt B=aH/(b+H).'
    parameters = [('S', 'Tvärsnitt S [m²]', 0.0002), ('ell', 'Järnlängd ℓ [m]', 0.5), ('d', 'Luftgap d [m]', 0.001), ('N', 'Varv N', 100.0), ('I', 'Ström I [A]', 2.0), ('Bsat', 'a-parameter [T]', 2.0), ('H0', 'b-parameter [A/m]', 400.0)]

    def validate(self, params):
        if min(params['S'], params['ell'], params['d'], params['N'], params['Bsat'], params['H0']) <= 0:
            return 'Alla geometri-/materialparametrar måste vara positiva.'
        return None

    @staticmethod
    def solve_B(ell, d, N, I, Bsat, H0):
        lo, hi = (1e-12, Bsat * (1 - 1e-09))

        def f(B):
            H = H0 * B / (Bsat - B)
            return H * ell + B * d / MU0 - N * I
        for _ in range(100):
            mid = (lo + hi) / 2
            if f(mid) > 0:
                hi = mid
            else:
                lo = mid
        return (lo + hi) / 2

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        ell, d, N, I, Bsat, H0 = (params['ell'], params['d'], params['N'], params['I'], params['Bsat'], params['H0'])
        B = np.linspace(1e-06, Bsat * 0.98, 600)
        H = H0 * B / (Bsat - B)
        lhs = H * ell + B * d / MU0
        B0 = self.solve_B(ell, d, N, I, Bsat, H0)
        ax.plot(B, lhs, label='krävda ampervarv')
        ax.axhline(N * I, linestyle='--', linewidth=1, label='NI')
        ax.axvline(B0, linestyle='--', linewidth=1)
        ax.set_xlabel('B [T]')
        ax.set_ylabel('Hℓ + Bd/µ0 [A-turn]')
        ax.set_title(f'Luftgapets B = {B0:.3g} T')
        ax.legend()
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        ax.add_patch(Rectangle((-0.7, -0.5), 1.4, 1, fill=False, linewidth=6, alpha=0.5))
        ax.plot([0.7, 0.9], [0, 0], linewidth=8, color='white')
        ax.text(0.8, 0.12, 'gap', ha='center')
        ax.text(-0.1, 0.55, 'N turns', ha='center')
        ax.set_aspect('equal')
        ax.set_xlim(-1, 1)
        ax.set_ylim(-0.8, 0.8)
        ax.set_axis_off()
        ax.set_title('Järnkrets')

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        ell, d, N, Bsat, H0 = (params['ell'], params['d'], params['N'], params['Bsat'], params['H0'])
        I = np.linspace(0.1, 4, 60)
        D = np.linspace(0.2 * d, 3 * d, 60)
        IG, DG = np.meshgrid(I, D)
        B = np.vectorize(self.solve_B)(ell, DG, N, IG, Bsat, H0)
        ax.plot_surface(IG, DG * 1000.0, B, cmap='plasma', alpha=0.9)
        ax.set_xlabel('I [A]')
        ax.set_ylabel('d [mm]')
        ax.set_zlabel('B [T]')
        ax.set_title('Svep för ickelinjär krets')

class MagneticBridgeCircuit(ProblemBase):
    name = '8.4 Järnring med magnetisk brygga'
    description = 'Linjär magnetkretsapproximation för flödet genom en brygga över en järnring.'
    parameters = [('D', 'Ringens medeldiameter [m]', 0.15), ('S_ring', 'Ringens tvärsnitt [m²]', 0.00012), ('S_bridge', 'Bryggans tvärsnitt [m²]', 8e-05), ('mu_r', 'Relativ permeabilitet µr', 150.0), ('N', 'Varv N', 160.0), ('I', 'Ström I [A]', 0.002)]

    def validate(self, params):
        if min(params.values()) <= 0:
            return 'Alla parametrar måste vara positiva.'
        return None

    @staticmethod
    def bridge_flux(D, Sr, Sb, mur, N, I):
        mu = MU0 * mur
        Rhalf = math.pi * D / 2 / (mu * Sr)
        Rb = D / (mu * Sb)
        F = N * I
        V = F / Rhalf / (2 / Rhalf + 1 / Rb)
        return V / Rb

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        D, Sr, Sb, mur, N, I = (params['D'], params['S_ring'], params['S_bridge'], params['mu_r'], params['N'], params['I'])
        currents = np.linspace(0, max(3 * I, 1e-06), 300)
        Phi = [self.bridge_flux(D, Sr, Sb, mur, N, ii) for ii in currents]
        ph0 = self.bridge_flux(D, Sr, Sb, mur, N, I)
        ax.plot(currents * 1000.0, Phi)
        ax.scatter([I * 1000.0], [ph0])
        ax.set_xlabel('I [mA]')
        ax.set_ylabel('Φbridge [Wb]')
        ax.set_title(f'Bryggflöde = {ph0:.3e} Wb')
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        ax.add_patch(Circle((0, 0), 1, fill=False, linewidth=8, alpha=0.45))
        ax.plot([0, 0], [-1, 1], linewidth=6, alpha=0.45)
        ax.text(-0.7, 0.55, 'spole', ha='center')
        ax.text(0.15, 0, 'brygga', va='center')
        ax.set_aspect('equal')
        ax.set_xlim(-1.3, 1.3)
        ax.set_ylim(-1.3, 1.3)
        ax.set_axis_off()
        ax.set_title('Ekvivalenta magnetiska grenar')

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        D, Sr, Sb, N, I = (params['D'], params['S_ring'], params['S_bridge'], params['N'], params['I'])
        mur = np.linspace(50, 500, 50)
        cur = np.linspace(0, 0.005, 50)
        MU, CU = np.meshgrid(mur, cur)
        Phi = np.vectorize(self.bridge_flux)(D, Sr, Sb, MU, N, CU)
        ax.plot_surface(MU, CU * 1000.0, Phi, cmap='viridis', alpha=0.9)
        ax.set_xlabel('µr')
        ax.set_ylabel('I [mA]')
        ax.set_zlabel('Φ [Wb]')
        ax.set_title('Svep av bryggflöde')

class CurrentCarryingMagneticTube(ProblemBase):
    name = '8.5 Strömförande magnetiskt rör'
    description = 'H, B och M för ett långt cylindriskt rör med likformigt fördelad axiell ström.'
    parameters = [('I', 'Ström I [A]', 10.0), ('a', 'Inre radie a [m]', 0.02), ('b', 'Yttre radie b [m]', 0.05), ('mu_r', 'Rörets relativa permeabilitet µr', 100.0), ('rmax', 'Största radie [m]', 0.1)]

    def validate(self, params):
        if params['a'] <= 0 or params['b'] <= params['a'] or params['rmax'] <= params['b'] or (params['mu_r'] <= 0):
            return 'Kräver 0 < a < b < rmax och µr > 0.'
        return None

    @staticmethod
    def fields(R, I, a, b, mur):
        H = np.zeros_like(R)
        mask = (R >= a) & (R <= b)
        H[mask] = I * (R[mask] ** 2 - a * a) / (2 * math.pi * R[mask] * (b * b - a * a))
        H[R > b] = I / (2 * math.pi * R[R > b])
        B = MU0 * H.copy()
        M = np.zeros_like(R)
        inside = mask
        B[inside] = MU0 * mur * H[inside]
        M[inside] = (mur - 1) * H[inside]
        return (H, B, M)

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        I, a, b, mur, rmax = (params['I'], params['a'], params['b'], params['mu_r'], params['rmax'])
        R = np.linspace(1e-06, rmax, 800)
        H, B, M = self.fields(R, I, a, b, mur)
        if mode == 'Map':
            ax.plot(R, M, label='Mϕ [A/m]')
            ax.set_ylabel('M [A/m]')
        else:
            ax.plot(R, H, label='Hϕ [A/m]')
            ax.plot(R, B, label='Bϕ [T]')
            ax.set_ylabel('H eller B')
        ax.axvline(a, linestyle='--', linewidth=1)
        ax.axvline(b, linestyle='--', linewidth=1)
        ax.set_xlabel('R [m]')
        ax.legend()
        ax.set_title('Rörfält')
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        a, b = (params['a'], params['b'])
        ax.add_patch(Circle((0, 0), b, fill=False, linewidth=2))
        ax.add_patch(Circle((0, 0), a, fill=False, linewidth=2))
        ax.text(0, 0, 'hål', ha='center')
        ax.text(0.5 * (a + b), 0, 'strömrör', ha='center', fontsize=8)
        ax.set_aspect('equal')
        ax.set_xlim(-1.2 * b, 1.2 * b)
        ax.set_ylim(-1.2 * b, 1.2 * b)
        ax.set_axis_off()
        ax.set_title('Rörets tvärsnitt')

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        I, a, b, mur, rmax = (params['I'], params['a'], params['b'], params['mu_r'], params['rmax'])
        R = np.linspace(1e-06, rmax, 140)
        H, B, M = self.fields(R, I, a, b, mur)
        scalar = M if mode == 'Map' else B
        _surface_of_revolution(ax, 0.04 * b * np.ones_like(R), R, scalar, title='Rörets radiella profil roterad', zlabel='R [m]')

class HorseshoeMagnetAnchorForce(ProblemBase):
    name = '8.6 Kraft mellan hästskomagnet och ankare'
    description = 'Kraft mellan en permanentmagnet och ett mjukjärnsankare beräknad från uppmätt magnetiskt flöde.'
    parameters = [('Phi0', 'Magnetiskt flöde Φ0 [Wb]', 0.0003), ('S', 'Tvärsnitt S [m²]', 0.00028)]

    def validate(self, params):
        if params['S'] <= 0:
            return 'S måste vara positivt.'
        return None

    @staticmethod
    def force(Phi, S):
        return Phi ** 2 / (MU0 * S)

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        Phi, S = (params['Phi0'], params['S'])
        ph = np.linspace(0, max(1.5 * abs(Phi), 1e-09), 400)
        F = self.force(ph, S)
        F0 = self.force(Phi, S)
        ax.plot(ph * 10000.0, F)
        ax.scatter([Phi * 10000.0], [F0])
        ax.set_xlabel('Φ [10⁻⁴ Wb]')
        ax.set_ylabel('F [N]')
        ax.set_title(f'Attraktionskraft F = {F0:.3g} N')
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        ax.add_patch(Rectangle((-0.7, -0.2), 1.4, 0.18, fill=False, linewidth=2))
        ax.add_patch(Rectangle((-0.6, 0.0), 0.25, 0.8, fill=False, linewidth=2))
        ax.add_patch(Rectangle((0.35, 0.0), 0.25, 0.8, fill=False, linewidth=2))
        ax.add_patch(Rectangle((-0.6, 0.65), 1.2, 0.18, fill=False, linewidth=2))
        ax.arrow(0, -0.25, 0, 0.18, head_width=0.05, length_includes_head=True)
        ax.set_aspect('equal')
        ax.set_xlim(-0.9, 0.9)
        ax.set_ylim(-0.4, 1.0)
        ax.set_axis_off()
        ax.set_title('Hästsko och ankare')

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        Phi, S = (params['Phi0'], params['S'])
        ph = np.linspace(max(Phi * 0.2, 1e-09), Phi * 2, 60)
        ss = np.linspace(max(S * 0.3, 1e-08), S * 2, 60)
        P, Sg = np.meshgrid(ph, ss)
        F = self.force(P, Sg)
        ax.plot_surface(P * 10000.0, Sg * 10000.0, F, cmap='plasma', alpha=0.9)
        ax.set_xlabel('Φ [10⁻⁴ Wb]')
        ax.set_ylabel('S [cm²]')
        ax.set_zlabel('F [N]')
        ax.set_title('Kraftyta')

class PermanentlyMagnetizedCylinderAxis(ProblemBase):
    name = '8.12 Permanentmagnetiserad cylinder på axeln'
    description = "En cylinder med radie a och höjd h har likformig magnetisering M = M ẑ. Längs z-axeln gäller B_z = (μ0 M / 2) [ z/sqrt(a²+z²) − (z−h)/sqrt(a²+(z−h)²) ]. Läget 'B-fält' visar B_z; läget 'H-fält' visar H_z, lika med B/μ0 − M inne i magneten och B/μ0 utanför."
    parameters = [('M', 'Magnetisering M [A/m]', 800000.0), ('a', 'Cylinderradie a [m]', 0.05), ('h', 'Cylinderhöjd h [m]', 0.12), ('zmax', 'Största plottade z [m]', 0.25), ('amax', 'Kartans största radie amax [m]', 0.2)]

    def validate(self, params):
        if params['M'] == 0:
            return 'M får inte vara noll.'
        if params['a'] <= 0 or params['h'] <= 0 or params['zmax'] <= 0 or (params['amax'] <= 0):
            return 'a, h, zmax och amax måste vara positiva.'
        return None

    @staticmethod
    def _Bz(M, a, h, z):
        z = np.asarray(z, dtype=float)
        return 0.5 * MU0 * np.asarray(M, dtype=float) * (z / np.sqrt(a ** 2 + z ** 2) - (z - h) / np.sqrt(a ** 2 + (z - h) ** 2))

    @classmethod
    def _Hz(cls, M, a, h, z):
        z = np.asarray(z, dtype=float)
        Bz = cls._Bz(M, a, h, z)
        inside = (z > 0) & (z < h)
        return Bz / MU0 - np.where(inside, M, 0.0)

    def plot(self, fig, params, mode):
        fig.clear()
        M, a, h, zmax = (params['M'], params['a'], params['h'], params['zmax'])
        if mode == 'Map':
            ax = fig.add_subplot(111)
            z = np.linspace(-0.3 * h, zmax, 260)
            a_vals = np.linspace(0.02 * params['amax'], params['amax'], 220)
            ZZ, AA = np.meshgrid(z, a_vals)
            BB = self._Bz(M, AA, h, ZZ)
            im = ax.pcolormesh(z, a_vals, BB, cmap='coolwarm', shading='auto')
            fig.colorbar(im, ax=ax).set_label('B_z [T]')
            ax.scatter([0.5 * h], [a], color='black', s=22)
            ax.set_xlabel('Axelkoordinat z [m]')
            ax.set_ylabel('Cylinderradie a [m]')
            ax.set_title('B_z på axeln mot cylinderradie')
            return
        ax = fig.add_subplot(111)
        z = np.linspace(-0.4 * h, zmax, 1000)
        if mode == 'Field':
            y = self._Bz(M, a, h, z)
            ylabel = 'B_z [T]'
            title = 'Likformigt magnetiserad cylinder: B_z på axeln'
        else:
            y = self._Hz(M, a, h, z)
            ylabel = 'H_z [A/m]'
            title = 'Likformigt magnetiserad cylinder: H_z på axeln'
        ax.plot(z, y)
        ax.axvspan(0.0, h, color='grey', alpha=0.12, label='magnet')
        ax.axvline(0.0, linestyle='--', linewidth=1, color='grey')
        ax.axvline(h, linestyle='--', linewidth=1, color='grey')
        ax.set_xlabel('z [m]')
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=8)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        a, h = (params['a'], params['h'])
        ax.add_patch(Rectangle((-a, 0.0), 2 * a, h, fill=False, linewidth=2, color='firebrick'))
        for z0 in np.linspace(0.15 * h, 0.85 * h, 5):
            ax.annotate('', xy=(0.0, z0 + 0.12 * h), xytext=(0.0, z0 - 0.12 * h), arrowprops=dict(arrowstyle='->', linewidth=1.7, color='steelblue'))
        ax.text(0.08 * a, 0.5 * h, 'M', color='steelblue')
        ax.plot([0, 0], [-0.15 * h, 1.15 * h], color='black', linestyle=':', linewidth=1)
        ax.text(0.05 * a, 1.08 * h, 'z-axel')
        ax.set_xlim(-1.4 * a, 1.4 * a)
        ax.set_ylim(-0.18 * h, 1.18 * h)
        ax.set_aspect('equal')
        ax.set_axis_off()
        ax.set_title('Geometri: cylindrisk permanentmagnet')

    def draw_3d(self, fig, params, mode):
        fig.clear()
        M, a, h, zmax = (params['M'], params['a'], params['h'], params['zmax'])
        z = np.linspace(-0.3 * h, zmax, 180)
        scalar = self._Bz(M, a, h, z) if mode == 'Field' else self._Hz(M, a, h, z)
        ribbon_r = 0.08 * a * np.ones_like(z)
        ax = fig.add_subplot(111, projection='3d')
        _surface_of_revolution(ax, ribbon_r, z, scalar, n_phi=60, title='B_z-profil roterad' if mode == 'Field' else 'H_z-profil roterad', zlabel='z [m]', cmap='coolwarm')
        phi = np.linspace(0, 2 * np.pi, 120)
        for z0 in [0.0, h]:
            ax.plot(a * np.cos(phi), a * np.sin(phi), z0 * np.ones_like(phi), color='black', linewidth=1.8)
        ax.plot(a * np.cos(phi), a * np.sin(phi), np.linspace(0, h, phi.size), alpha=0)
        for ang in [0, np.pi / 2, np.pi, 3 * np.pi / 2]:
            ax.plot([a * np.cos(ang), a * np.cos(ang)], [a * np.sin(ang), a * np.sin(ang)], [0, h], color='black', linewidth=1.0, alpha=0.8)

class MagnetizationCurrentsCylinder(ProblemBase):
    name = '8.13 Magnetiseringsströmmar i permeabel ledare'
    description = 'Volym- och ytmagnetiseringsströmmar i en lång permeabel cylindrisk ledare.'
    parameters = [('I', 'Transportström I [A]', 10.0), ('a', 'Radie a [m]', 0.02), ('mu_r', 'Relativ permeabilitet µr', 100.0)]

    def validate(self, params):
        if params['a'] <= 0 or params['mu_r'] <= 0:
            return 'a och µr måste vara positiva.'
        return None

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        I, a, mur = (params['I'], params['a'], params['mu_r'])
        R = np.linspace(0, 2 * a, 500)
        Jm = np.where(R < a, I * (mur - 1) / (math.pi * a * a), 0.0)
        K = -I * (mur - 1) / (2 * math.pi * a)
        ax.plot(R, Jm, label='Jm,z [A/m²]')
        ax.axvline(a, linestyle='--', linewidth=1, label=f'ytström Km={K:.2e} A/m')
        ax.set_xlabel('R [m]')
        ax.set_ylabel('magnetiseringsströmtäthet')
        ax.set_title('Nettomagnetiseringsströmmen i z-riktningen är noll')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        a = params['a']
        ax.add_patch(Circle((0, 0), a, fill=False, linewidth=2))
        ax.text(0, 0, 'Jm längs +z', ha='center')
        ax.text(0, -1.25 * a, 'ytström längs -z', ha='center')
        ax.set_aspect('equal')
        ax.set_xlim(-1.4 * a, 1.4 * a)
        ax.set_ylim(-1.5 * a, 1.4 * a)
        ax.set_axis_off()
        ax.set_title('Strömriktningar')

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        a = params['a']
        theta = np.linspace(0, 2 * np.pi, 50)
        z = np.linspace(-a, a, 20)
        T, Z = np.meshgrid(theta, z)
        X = a * np.cos(T)
        Y = a * np.sin(T)
        ax.plot_surface(X, Y, Z, alpha=0.25, color='steelblue')
        ax.quiver([0], [0], [-0.8 * a], [0], [0], [1], length=1.6 * a)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_title('Volym- och ytströmmar tar ut varandra totalt')
