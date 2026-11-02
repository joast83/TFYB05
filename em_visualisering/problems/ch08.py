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
    parameters = [('ell', 'Magnetlängd ℓ (exkl. gap) [m]', 0.2), ('d', 'Luftgap d [m]', 0.001), ('N', 'Spolvarv N', 100.0), ('I', 'Spolström I [A]', 0.0)]
    Btab = np.array([0.0, 0.6, 0.83, 1.0, 1.2])
    Htab = np.array([-5000, -4000, -3000, -2000, 0.0])

    def validate(self, params):
        if params['ell'] <= 0 or params['d'] <= 0:
            return 'Kräver ℓ > 0 och d > 0.'
        if params['N'] < 0:
            return 'N måste vara icke-negativt.'
        try:
            self.solve_B(params['ell'], params['d'], params['N'], params['I'])
        except ValueError as error:
            return str(error)
        return None

    @classmethod
    def Hmat(cls, B):
        return np.interp(B, cls.Btab, cls.Htab)

    @classmethod
    def solve_B(cls, ell, d, N, I):
        if ell <= 0 or d <= 0:
            raise ValueError('Kräver ℓ > 0 och d > 0.')
        # On each table segment the magnetic-circuit residual is linear in B.
        required = cls.Htab * ell + cls.Btab * d / MU0
        if not required[0] <= N * I <= required[-1]:
            raise ValueError('Ingen arbetspunkt inom den lagrade B–H-tabellen. Fler materialdata behövs.')
        return float(np.interp(N * I, required, cls.Btab))

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        ell, d, N, I = (params['ell'], params['d'], params['N'], params['I'])
        B = np.linspace(0, 1.2, 400)
        Hload = (N * I - B * d / MU0) / ell
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
        ell, d, N = params['ell'], params['d'], params['N']
        currents = np.linspace(min(0, params['I']), max(3, params['I']), 60)
        gaps = np.linspace(.2*d, 3*d, 60)
        IG, DG = np.meshgrid(currents, gaps)
        B = np.full_like(IG, np.nan)
        for idx in np.ndindex(B.shape):
            try:
                B[idx] = self.solve_B(ell, DG[idx], N, IG[idx])
            except ValueError:
                pass  # No extrapolation outside the material table.
        ax.plot_surface(IG, DG*1000, B, cmap='viridis', alpha=.9)
        ax.set_xlabel('I [A]')
        ax.set_ylabel('d [mm]')
        ax.set_zlabel('B [T]')
        ax.set_title('Gapfält — luckor saknar materialdata')

class NonlinearIronMagneticCircuit(ProblemBase):
    name = '8.2 Ickelinjär magnetisk krets av järn'
    description = 'Magnetisk krets med ett luftgap och ickelinjärt järn enligt B=aH/(b+H).'
    parameters = [('S', 'Tvärsnitt S [m²]', 0.0002), ('ell', 'Järnlängd ℓ [m]', 0.5), ('d', 'Luftgap d [m]', 0.001), ('N', 'Varv N', 100.0), ('I', 'Ström I [A]', 2.0), ('Bsat', 'a-parameter [T]', 2.0), ('H0', 'b-parameter [A/m]', 400.0)]

    def validate(self, params):
        if min(params['S'], params['ell'], params['d'], params['N'], params['Bsat'], params['H0']) <= 0:
            return 'Alla geometri-/materialparametrar måste vara positiva.'
        if params['I'] < 0:
            return 'Materiallagen gäller för H > 0; välj I ≥ 0 (noll som gränsfall).'
        return None

    @staticmethod
    def solve_B(ell, d, N, I, Bsat, H0):
        if I < 0:
            raise ValueError('Materiallagen gäller för H > 0.')
        if I == 0:
            return 0.0
        lo, hi = (0.0, np.nextafter(float(Bsat), 0.0))

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
        B = np.linspace(0, min(Bsat*.999, max(.1*Bsat, 1.5*self.solve_B(ell, d, N, I, Bsat, H0))), 600)
        H = H0 * B / (Bsat - B)
        lhs = H * ell + B * d / MU0
        B0 = self.solve_B(ell, d, N, I, Bsat, H0)
        ax.plot(B, lhs, label='krävda ampervarv')
        ax.axhline(N * I, linestyle='--', linewidth=1, label='NI')
        ax.axvline(B0, linestyle='--', linewidth=1)
        ax.set_xlabel('B [T]')
        ax.set_ylabel('Hℓ + Bd/µ0 [ampervarv]')
        ax.set_title(f'B = {B0:.3g} T; Φ = {B0*params["S"]:.3g} Wb')
        ax.legend()
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        ax.add_patch(Rectangle((-0.7, -0.5), 1.4, 1, fill=False, linewidth=6, alpha=0.5))
        ax.plot([0.7, 0.9], [0, 0], linewidth=8, color='white')
        ax.text(0.8, 0.12, 'gap', ha='center')
        ax.text(-0.1, 0.55, 'N varv', ha='center')
        ax.set_aspect('equal')
        ax.set_xlim(-1, 1)
        ax.set_ylim(-0.8, 0.8)
        ax.set_axis_off()
        ax.set_title('Järnkrets')

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        ell, d, N, Bsat, H0 = (params['ell'], params['d'], params['N'], params['Bsat'], params['H0'])
        I = np.linspace(0, max(4, 1.5*params['I']), 60)
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
        if min(value for key, value in params.items() if key != 'I') <= 0:
            return 'Geometri, permeabilitet och varvtal måste vara positiva.'
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
        currents = np.linspace(-max(3 * abs(I), 1e-6), max(3 * abs(I), 1e-6), 300)
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
        mur = np.linspace(.5*params['mu_r'], 2*params['mu_r'], 50)
        cur = np.linspace(-max(.005, 2*abs(I)), max(.005, 2*abs(I)), 50)
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
        R = np.asarray(R, dtype=float)
        H = np.zeros_like(R)
        mask = (R >= a) & (R <= b)
        H[mask] = I * (R[mask] ** 2 - a * a) / (2 * math.pi * R[mask] * (b * b - a * a))
        H[R > b] = I / (2 * math.pi * R[R > b])
        B = np.where(mask, MU0*mur*H, MU0*H)
        M = np.where(mask, (mur-1)*H, 0.0)
        return (H, B, M)

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        I, a, b, mur, rmax = (params[k] for k in ['I', 'a', 'b', 'mu_r', 'rmax'])
        index, label = {'Field': (0, 'Hφ [A/m]'), 'Potential': (1, 'Bφ [T]'), 'Map': (2, 'Mφ [A/m]')}[mode]
        regions = [np.linspace(0, a, 120), np.linspace(a, b, 300), np.linspace(np.nextafter(b, np.inf), rmax, 250)]
        for j, R in enumerate(regions):
            values = self.fields(R, I, a, b, mur)[index]
            ax.plot(R, values, color='steelblue', label=label if j == 0 else None)
        ax.axvspan(a, b, color='grey', alpha=.12, label='rörmaterial')
        for boundary in [a, b]:
            ax.axvline(boundary, ls=':', color='black', lw=.8)
        ax.set_xlabel('R [m]')
        ax.set_ylabel(label)
        ax.set_title('Radiell profil — positiva värden längs +φ')
        ax.grid(True, alpha=.3)
        ax.legend(fontsize=8)

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
        ax.set_title(f"Tvärsnitt: I = {params['I']:g} A längs +z")

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        I, a, b, mur, rmax = (params[k] for k in ['I', 'a', 'b', 'mu_r', 'rmax'])
        index, label = {'Field': (0, 'Hφ [A/m]'), 'Potential': (1, 'Bφ [T]'), 'Map': (2, 'Mφ [A/m]')}[mode]
        for R in [np.linspace(0, a, 40), np.linspace(a, b, 80), np.linspace(np.nextafter(b, np.inf), rmax, 80)]:
            scalar = self.fields(R, I, a, b, mur)[index]
            ax.plot(R, np.zeros_like(R), scalar, color='steelblue')
        ax.set_xlabel('R [m]')
        ax.set_ylabel('Profilplan')
        ax.set_zlabel(label)
        ax.set_title('Radiell funktionsgraf (inte rumsligt fält)')

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
        ax.scatter([abs(Phi) * 10000.0], [F0])
        ax.set_xlabel('|Φ| [10⁻⁴ Wb]')
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
        ph = np.linspace(0, max(abs(Phi)*2, 1e-9), 60)
        ss = np.linspace(S*.3, S*2, 60)
        P, Sg = np.meshgrid(ph, ss)
        F = self.force(P, Sg)
        ax.plot_surface(P * 10000.0, Sg * 10000.0, F, cmap='plasma', alpha=0.9)
        ax.set_xlabel('|Φ| [10⁻⁴ Wb]')
        ax.set_ylabel('S [cm²]')
        ax.set_zlabel('F [N]')
        ax.set_title('Kraftyta')

class PermanentlyMagnetizedCylinderAxis(ProblemBase):
    name = '8.12 Permanentmagnetiserad cylinder på axeln'
    description = "En cylinder med radie a och höjd h har likformig magnetisering M = M ẑ. Längs z-axeln gäller B_z = (μ0 M / 2) [ z/sqrt(a²+z²) − (z−h)/sqrt(a²+(z−h)²) ]. Läget 'B-fält' visar B_z; läget 'H-fält' visar H_z, lika med B/μ0 − M inne i magneten och B/μ0 utanför."
    parameters = [('M', 'Magnetisering M [A/m]', 800000.0), ('a', 'Cylinderradie a [m]', 0.05), ('h', 'Cylinderhöjd h [m]', 0.12), ('zmax', 'Största plottade z [m]', 0.25), ('amax', 'Kartans största radie amax [m]', 0.2)]

    def validate(self, params):
        if params['a'] <= 0 or params['h'] <= 0 or params['zmax'] <= 0 or (params['amax'] <= 0):
            return 'a, h, zmax och amax måste vara positiva.'
        return None

    @staticmethod
    def _Bz(M, a, h, z):
        z = np.asarray(z, dtype=float)
        a = np.asarray(a, dtype=float)
        w = z - h
        rz, rw = np.hypot(a, z), np.hypot(a, w)
        difference = z/rz - w/rw
        # Rationalize outside the end faces to avoid far-field cancellation.
        denominator = rz*rw*(z*rw + w*rz)
        stable = np.divide(a*a*h*(z+w), denominator, out=np.zeros_like(difference), where=denominator != 0)
        difference = np.where(z*w > 0, stable, difference)
        return .5*MU0*np.asarray(M, dtype=float)*difference

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
            z = np.linspace(-.3*h, max(zmax, 1.3*h), 260)
            a_vals = np.linspace(min(.02*params['amax'], a), max(params['amax'], a), 220)
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
        z = np.linspace(-.4*h, max(zmax, 1.4*h), 1000)
        if mode == 'Field':
            y = self._Bz(M, a, h, z)
            ylabel = 'B_z [T]'
            title = 'Likformigt magnetiserad cylinder: B_z på axeln'
        else:
            y = self._Hz(M, a, h, z)
            ylabel = 'H_z [A/m]'
            title = 'Likformigt magnetiserad cylinder: H_z på axeln'
        if mode == 'Field':
            ax.plot(z, y)
        else:
            for lo, hi in [(-.4*h, np.nextafter(0., -np.inf)), (np.nextafter(0., np.inf), np.nextafter(h, 0.)), (np.nextafter(h, np.inf), max(zmax, 1.4*h))]:
                segment = np.linspace(lo, hi, 350)
                ax.plot(segment, self._Hz(M, a, h, segment), color='steelblue')
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
            ax.annotate('', xy=(0.0, z0 + np.sign(params['M']) * 0.12 * h), xytext=(0.0, z0 - np.sign(params['M']) * 0.12 * h), arrowprops=dict(arrowstyle='->', linewidth=1.7, color='steelblue'))
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
        ax = fig.add_subplot(111, projection='3d')
        M, a, h, zmax = (params[k] for k in ['M', 'a', 'h', 'zmax'])
        if mode == 'Map':
            z = np.linspace(-.4*h, max(zmax, 1.4*h), 80)
            radii = np.linspace(min(.02*params['amax'], a), max(params['amax'], a), 60)
            ZZ, AA = np.meshgrid(z, radii)
            ax.plot_surface(ZZ, AA, self._Bz(M, AA, h, ZZ), cmap='viridis')
            ax.set_xlabel('z [m]')
            ax.set_ylabel('Cylinderradie a [m]')
            ax.set_zlabel('Bz [T]')
            ax.set_title('Parameterstudie av axelfältet')
        else:
            for lo, hi in [(-.4*h, np.nextafter(0., -np.inf)), (np.nextafter(0., np.inf), np.nextafter(h, 0.)), (np.nextafter(h, np.inf), max(zmax, 1.4*h))]:
                z = np.linspace(lo, hi, 100)
                scalar = self._Bz(M, a, h, z) if mode == 'Field' else self._Hz(M, a, h, z)
                ax.plot(z, np.zeros_like(z), scalar, color='steelblue')
            ax.set_xlabel('Axelkoordinat z [m]')
            ax.set_ylabel('Profilplan')
            ax.set_zlabel('Bz [T]' if mode == 'Field' else 'Hz [A/m]')
            ax.set_title('Axelprofil (inte ett fält utanför axeln)')

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
        ax.set_ylabel('Jm,z [A/m²]')
        ax.set_title('Magnetiseringsström: volym + mantel = 0')
        ax.text(.03, .08, f'I_vol = {I*(mur-1):.3g} A; I_yta = {-I*(mur-1):.3g} A', transform=ax.transAxes, fontsize=9, bbox=dict(facecolor='white', edgecolor='none', alpha=.8))
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        a = params['a']
        signed = params['I']*(params['mu_r']-1)
        symbol = lambda value: r'$\odot$' if value > 0 else r'$\otimes$' if value < 0 else '0'
        ax.add_patch(Circle((0, 0), a, fill=False, lw=2))
        ax.text(0, 0, symbol(signed), ha='center', va='center', fontsize=24, color='steelblue')
        ax.text(0, -.4*a, 'volymström', ha='center', fontsize=9)
        for angle in np.linspace(0, 2*np.pi, 5)[:-1]:
            ax.text(a*np.cos(angle), a*np.sin(angle), symbol(-signed), ha='center', va='center', fontsize=20, color='darkorange')
        ax.text(0, -1.4*a, 'Mantelström: motsatt riktning', ha='center', fontsize=9)
        ax.set(xlim=(-1.7*a, 1.7*a), ylim=(-1.7*a, 1.4*a), aspect='equal')
        ax.set_axis_off()
        ax.set_title('Sedd från +z: ⊙ ut, ⊗ in')

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
        direction = np.sign(params['I']*(params['mu_r']-1))
        ax.quiver(0, 0, -direction*.8*a, 0, 0, direction*1.6*a, color='steelblue')
        for angle in [0, np.pi/2, np.pi, 3*np.pi/2]:
            ax.quiver(a*np.cos(angle), a*np.sin(angle), direction*.8*a, 0, 0, -direction*1.6*a, color='darkorange')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_title('Volym- och ytströmmar tar ut varandra totalt')
