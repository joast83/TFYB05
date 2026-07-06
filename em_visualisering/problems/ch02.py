"""Kapitel 2: Elektrostatik i vakuum/luft.

Uppgifter i detta kapitel (i menyordning):
    2.1    ChargedSpheresSmallAngle
    2.2    ChargedRingAxis
    2.3    FiniteLineCharge2D
    2.4    SemiCircularSurfaceAxis
    2.5    SphericalShellPotential
    2.6    ConcentricChargedCylinders
    2.7    SphericalCapacitorDesign
    2.8    ConcentricSphericalShells
    2.9    AtmosphericChargeDensity
    2.10   OffsetCavitySphereExterior
    2.11   CoaxialCylinderVoltage
    2.12   SphericalConductorBreakdown
    2.13   CoaxialTubeSpaceCharge
    2.16   RadialChargeSphere
    2.18   InsertedMetalPlateCapacitor
    2.19   UniformSpaceChargePlates
"""

from ..core import *


class ChargedSpheresSmallAngle(ProblemBase):
    name = '2.1 Laddade kulor upphängda i trådar, liten vinkel'
    description = 'Två lika laddade kulor upphängda från samma punkt. Använder småvinkelformeln α = (Q²/(2π ε0 m g ℓ²))^(1/3).'
    parameters = [('Q', 'Laddning på vardera kulan Q [C]', 3e-08), ('m', 'Massa hos vardera kulan m [kg]', 0.001), ('ell', 'Trådlängd ℓ [m]', 0.5), ('g', 'Tyngdacceleration g [m/s²]', 9.81)]

    def validate(self, params):
        if params['m'] <= 0 or params['ell'] <= 0 or params['g'] <= 0:
            return 'm, ℓ och g måste vara positiva.'
        return None

    @staticmethod
    def alpha(Q, m, ell, g):
        return np.cbrt(Q ** 2 / (2 * math.pi * EPS0 * m * g * ell ** 2))

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        Q, m, ell, g = (params['Q'], params['m'], params['ell'], params['g'])
        qmax = max(abs(Q) * 2.5, 1e-12)
        q = np.linspace(0, qmax, 400)
        alpha = self.alpha(q, m, ell, g)
        ax.plot(q * 1000000000.0, np.degrees(alpha))
        a0 = float(self.alpha(abs(Q), m, ell, g))
        ax.scatter([abs(Q) * 1000000000.0], [math.degrees(a0)], zorder=3)
        ax.set_xlabel('|Q| [nC]')
        ax.set_ylabel('α [grader]')
        ax.set_title(f'Småvinkeljämvikt: α = {math.degrees(a0):.3g}°')
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        Q, m, ell, g = (params['Q'], params['m'], params['ell'], params['g'])
        alpha = float(self.alpha(abs(Q), m, ell, g))
        theta = alpha / 2
        x = ell * math.sin(theta)
        y = -ell * math.cos(theta)
        ax.plot([0, -x], [0, y], linewidth=2)
        ax.plot([0, x], [0, y], linewidth=2)
        ax.add_patch(Circle((-x, y), 0.05 * ell, fill=False, linewidth=2))
        ax.add_patch(Circle((x, y), 0.05 * ell, fill=False, linewidth=2))
        ax.text(0, 0.05 * ell, f'α = {math.degrees(alpha):.2f}°', ha='center')
        ax.set_aspect('equal')
        ax.set_xlim(-0.45 * ell, 0.45 * ell)
        ax.set_ylim(-1.1 * ell, 0.15 * ell)
        ax.set_title('Geometriskiss')
        ax.set_axis_off()

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        Q0, m0, ell, g = (params['Q'], params['m'], params['ell'], params['g'])
        q = np.linspace(max(abs(Q0) * 0.1, 1e-12), max(abs(Q0) * 2.0, 2e-12), 60)
        m = np.linspace(max(m0 * 0.25, 1e-06), m0 * 2.0, 60)
        Qg, Mg = np.meshgrid(q, m)
        A = np.degrees(self.alpha(Qg, Mg, ell, g))
        ax.plot_surface(Qg * 1000000000.0, Mg * 1000.0, A, cmap='viridis', alpha=0.88)
        ax.set_xlabel('|Q| [nC]')
        ax.set_ylabel('m [g]')
        ax.set_zlabel('α [grader]')
        ax.set_title('α som funktion av laddning och massa')

class ChargedRingAxis(ProblemBase):
    name = '2.2 Laddad ring på axel'
    description = 'Tunn metalltråd böjd till en ring med radie a i xy-planet och jämnt fördelad laddning Q. Visar elektrisk fältstyrka och potential längs z-axeln.'
    parameters = [('Q', 'Total laddning Q [C]', 1e-09), ('a', 'Ringradie a [m]', 0.15), ('zmax', 'Halvt axelintervall zmax [m]', 0.5)]

    def validate(self, params):
        if params['a'] <= 0 or params['zmax'] <= 0:
            return 'a och zmax måste vara positiva.'
        return None

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        Q, a, zmax = (params['Q'], params['a'], params['zmax'])
        if mode == 'Map':
            X, Z, R = _radial_slice_grid(zmax, n=181)
            k = Q / (4 * math.pi * EPS0)
            rho2 = X ** 2 + Z ** 2
            common = np.power(rho2 + a ** 2, 2.5)
            Ex = k * 3 * a ** 2 * X * Z / np.maximum(common, 1e-30)
            Ez_map = k * Z * (2 * Z ** 2 - 3 * X ** 2 - a ** 2) / np.maximum(common, 1e-30)
            field_mag = np.sqrt(Ex ** 2 + Ez_map ** 2)
            _show_scalar_map(ax, fig, X, Z, field_mag, title='Laddad ring: |E|-karta i xz-planet', xlabel='x [m]', ylabel='z [m]', cbar_label='|E| [V/m]', scale='log', contours=True)
            _overlay_vector_field(ax, X, Z, Ex, Ez_map, max_arrows=21)
            ax.scatter([-a, a], [0.0, 0.0], color='white', edgecolors='black', linewidths=0.4, s=28, zorder=5)
            ax.axhline(0.0, color='white', linestyle=':', linewidth=0.8, alpha=0.75)
            ax.text(0.02 * zmax, 0.04 * zmax, 'pilar: fältriktning', color='white', fontsize=8, alpha=0.9)
            return
        z = np.linspace(-zmax, zmax, 800)
        Ez = Q / (4 * math.pi * EPS0) * z / np.power(z ** 2 + a ** 2, 1.5)
        V = Q / (4 * math.pi * EPS0) / np.sqrt(z ** 2 + a ** 2)
        if mode == 'Field':
            ax.plot(z, Ez)
            ax.set_ylabel('E_z [V/m]')
            ax.set_title('Laddad ring: elektrisk fältstyrka på z-axeln')
        else:
            ax.plot(z, V)
            ax.set_ylabel('V [V]')
            ax.set_title('Laddad ring: potential på z-axeln')
        ax.axvline(0.0, linestyle='--', linewidth=1)
        ax.set_xlabel('z [m]')
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        a = params['a']
        ax.add_patch(Circle((0.0, 0.0), a, fill=False, linewidth=2))
        ax.plot([-1.2 * a, 1.2 * a], [0, 0], linewidth=1)
        ax.plot([0, 0], [-1.2 * a, 1.2 * a], linewidth=1, linestyle='--')
        ax.set_title('Geometriskiss')
        ax.set_aspect('equal')
        ax.set_xlim(-1.35 * a, 1.35 * a)
        ax.set_ylim(-1.35 * a, 1.35 * a)
        ax.set_axis_off()

    def draw_3d(self, fig, params, mode):
        """
        Rotationsyta: roterar ett tunt band vid r=0,05a kring z-axeln,
        färgsatt efter E_z eller V längs den axiella profilen. Ringen ritas röd.
        """
        fig.clear()
        Q, a, zmax = (params['Q'], params['a'], params['zmax'])
        z = np.linspace(-zmax, zmax, 120)
        Ez = Q / (4 * math.pi * EPS0) * z / np.power(z ** 2 + a ** 2, 1.5)
        V = Q / (4 * math.pi * EPS0) / np.sqrt(z ** 2 + a ** 2)
        scalar = Ez if mode == 'Field' else V
        label = 'E_z [V/m]' if mode == 'Field' else 'V [V]'
        r_vals = 0.05 * a * np.ones_like(z)
        ax = fig.add_subplot(111, projection='3d')
        _surface_of_revolution(ax, r_vals, z, scalar, n_phi=60, title='Axiell profil (roterad)', zlabel='z [m]')
        phi = np.linspace(0, 2 * np.pi, 200)
        ax.plot(a * np.cos(phi), a * np.sin(phi), np.zeros(200), color='red', linewidth=2, label='ring')
        ax.legend(fontsize=7)

class FiniteLineCharge2D(ProblemBase):
    name = '2.3 Ändlig linjeladdning (2-D-snitt)'
    description = 'Smal rak tråd med konstant linjeladdningstäthet längs z-axeln från z=-b till z=+a. Visar antingen en 2-D-fältkarta i xz-planet eller potential/equipotentialer.'
    parameters = [('rho_l', 'Linjeladdningstäthet λ [C/m]', 1e-09), ('a', 'Höger längd a [m]', 0.4), ('b', 'Vänster längd b [m]', 0.3), ('xmax', 'x-utsträckning [m]', 0.4), ('zmax', 'z-utsträckning [m]', 0.5), ('grid_n', 'Rutnätsstorlek N', 81)]

    def validate(self, params):
        if params['a'] <= 0 or params['b'] <= 0 or params['xmax'] <= 0 or (params['zmax'] <= 0):
            return 'a, b, xmax och zmax måste vara positiva.'
        if params['grid_n'] < 21:
            return 'Rutnätsstorleken N bör vara minst 21.'
        return None

    @staticmethod
    def field_components(x, z, rho_l, a, b):
        # Fält från ett ändligt linjesegment på z-axeln: z' ∈ [-b, a].
        # Uttrycket beror på observationspunktens z-koordinat, inte bara på x.
        x = np.asarray(x, dtype=float)
        z = np.asarray(z, dtype=float)
        xp = np.maximum(np.abs(x), 1e-09)
        upper = a - z
        lower = b + z
        k = rho_l / (4 * math.pi * EPS0)
        ex_abs = k / xp * (upper / np.sqrt(upper ** 2 + xp ** 2) + lower / np.sqrt(lower ** 2 + xp ** 2))
        ez = k * (1 / np.sqrt(upper ** 2 + xp ** 2) - 1 / np.sqrt(lower ** 2 + xp ** 2))
        return (np.sign(x) * ex_abs, ez)

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        rho_l = params['rho_l']
        a, b = (params['a'], params['b'])
        xmax, zmax = (params['xmax'], params['zmax'])
        n = int(round(params['grid_n']))
        x = np.linspace(-xmax, xmax, n)
        z = np.linspace(-zmax, zmax, n)
        X, Z = np.meshgrid(x, z)
        Ex, Ez = self.field_components(X, Z, rho_l, a, b)
        mask = np.abs(X) < 0.015 * xmax
        Emag = np.sqrt(Ex ** 2 + Ez ** 2)
        if mode == 'Field':
            _show_scalar_map(ax, fig, X, Z, Emag, title='Ändlig linjeladdning: |E|-karta i xz-planet', xlabel='x [m]', ylabel='z [m]', cbar_label='|E| [V/m]', scale='log', mask=mask, contours=True)
            _overlay_vector_field(ax, X, Z, Ex, Ez, mask=mask, max_arrows=22)
            ax.text(-0.96 * xmax, 0.88 * zmax, 'pilar: fältriktning', color='white', fontsize=8, alpha=0.9)
        else:
            potential = np.zeros_like(X)
            zs = np.linspace(-b, a, 800)
            dz = zs[1] - zs[0]
            for zz in zs:
                potential += dz / np.sqrt(X ** 2 + (Z - zz) ** 2 + 1e-18)
            potential *= rho_l / (4 * math.pi * EPS0)
            cs = ax.contour(X, Z, potential, levels=18)
            ax.clabel(cs, inline=True, fontsize=8)
            ax.set_title('Ändlig linjeladdning: ekvipotentiallinjer i xz-planet')
        ax.plot([0, 0], [-b, a], linewidth=4)
        ax.set_xlabel('x [m]')
        ax.set_ylabel('z [m]')
        ax.grid(True, alpha=0.2)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        a, b = (params['a'], params['b'])
        xmax = params['xmax']
        ax.plot([0, 0], [-b, a], linewidth=4)
        ax.set_title('Geometriskiss')
        ax.set_aspect('equal')
        ax.set_xlim(-xmax, xmax)
        ax.set_ylim(-b * 1.2, a * 1.2)
        ax.set_axis_off()

    def draw_3d(self, fig, params, mode):
        """
        3-D-quiverdiagram av hela E-vektorfältet på ett glest xyz-rutnät.
        """
        fig.clear()
        rho_l = params['rho_l']
        a, b = (params['a'], params['b'])
        xmax, zmax = (params['xmax'], params['zmax'])
        n3 = 9
        xg = np.linspace(-xmax * 0.9, xmax * 0.9, n3)
        yg = np.linspace(-xmax * 0.9, xmax * 0.9, n3)
        zg = np.linspace(-zmax * 0.9, zmax * 0.9, n3)
        X3, Y3, Z3 = np.meshgrid(xg, yg, zg)
        Rcyl = np.sqrt(X3 ** 2 + Y3 ** 2)
        xp = np.maximum(Rcyl, 1e-09)
        k = rho_l / (4 * math.pi * EPS0)
        upper = a - Z3
        lower = b + Z3
        Er = k / xp * (upper / np.sqrt(upper ** 2 + xp ** 2) + lower / np.sqrt(lower ** 2 + xp ** 2))
        with np.errstate(invalid='ignore', divide='ignore'):
            Ex3 = np.where(Rcyl > 1e-12, Er * X3 / Rcyl, 0.0)
            Ey3 = np.where(Rcyl > 1e-12, Er * Y3 / Rcyl, 0.0)
        Ez3 = k * (1 / np.sqrt(upper ** 2 + xp ** 2) - 1 / np.sqrt(lower ** 2 + xp ** 2))
        mag = np.sqrt(Ex3 ** 2 + Ey3 ** 2 + Ez3 ** 2)
        mag = np.where(mag == 0, 1, mag)
        scale = xmax * 0.18
        ax = fig.add_subplot(111, projection='3d')
        valid = Rcyl > max(0.06 * xmax, 1e-12)
        ax.quiver(X3[valid], Y3[valid], Z3[valid], (Ex3 / mag)[valid], (Ey3 / mag)[valid], (Ez3 / mag)[valid], length=scale, normalize=False, color='steelblue', linewidth=0.7, alpha=0.7)
        ax.plot([0, 0], [0, 0], [-b, a], color='red', linewidth=3, label='tråd')
        ax.set_xlabel('x [m]')
        ax.set_ylabel('y [m]')
        ax.set_zlabel('z [m]')
        ax.set_title('Ändlig linjeladdning: 3-D E-fält')
        ax.legend(fontsize=7)

class SemiCircularSurfaceAxis(ProblemBase):
    name = '2.4 Halvcirkelformad laddad yta'
    description = 'Halvcirkelformad isolerande yta med radie a och konstant ytladdningstäthet ρs. Visar fältkomponenterna längs z-axeln ovanför cirkelns medelpunkt.'
    parameters = [('rho_s', 'Ytladdningstäthet ρs [C/m²]', 1e-09), ('a', 'Radie a [m]', 0.25), ('zmax', 'Halvt axelintervall zmax [m]', 0.8)]

    def validate(self, params):
        if params['a'] <= 0 or params['zmax'] <= 0:
            return 'a och zmax måste vara positiva.'
        return None

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        rho_s, a, zmax = (params['rho_s'], params['a'], params['zmax'])
        z = np.linspace(-zmax, zmax, 1200)
        root = np.sqrt(a ** 2 + z ** 2)
        Ey = rho_s / (2 * EPS0) * (-(1 / math.pi) * (np.log(np.abs((root + a) / np.maximum(np.abs(z), 1e-18))) - a / root))
        Ez = rho_s / (2 * EPS0) * 0.5 * (np.sign(z) - z / root)
        if mode == 'Field':
            ax.plot(z, Ey, label='E_y')
            ax.plot(z, Ez, label='E_z')
            ax.set_ylabel('Fält [V/m]')
            ax.set_title('Halvcirkelformad laddad yta: axiella fältkomponenter')
            ax.legend()
        else:
            ax.plot(z, np.sqrt(Ey ** 2 + Ez ** 2))
            ax.set_ylabel('|E| [V/m]')
            ax.set_title('Halvcirkelformad laddad yta: fältbelopp på axeln')
        ax.axvline(0.0, linestyle='--', linewidth=1)
        ax.set_xlabel('z [m]')
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        a = params['a']
        theta = np.linspace(0, np.pi, 300)
        ax.plot(a * np.cos(theta), a * np.sin(theta), linewidth=2)
        ax.plot([-a, a], [0, 0], linewidth=1)
        ax.plot([0, 0], [-0.1 * a, 1.2 * a], linewidth=1, linestyle='--')
        ax.set_title('Geometriskiss')
        ax.set_aspect('equal')
        ax.set_xlim(-1.2 * a, 1.2 * a)
        ax.set_ylim(-0.2 * a, 1.25 * a)
        ax.set_axis_off()

    def draw_3d(self, fig, params, mode):
        """
        Yta för |E| över planet (y-förskjutning, z), med halvcirkeln
        ritad som en 3-D-kurva.
        """
        fig.clear()
        rho_s, a, zmax = (params['rho_s'], params['a'], params['zmax'])
        nz, ny = (60, 40)
        z1 = np.linspace(-zmax, zmax, nz)
        y1 = np.linspace(-1.2 * a, 1.2 * a, ny)
        Z2, Y2 = np.meshgrid(z1, y1)
        root = np.sqrt(a ** 2 + Z2 ** 2 + Y2 ** 2)
        Ey2 = rho_s / (2 * EPS0) * (-(1 / math.pi) * (np.log(np.abs((root + a) / np.maximum(np.abs(Z2), 1e-18))) - a / root))
        Ez2 = rho_s / (2 * EPS0) * 0.5 * (np.sign(Z2) - Z2 / root)
        Emag2 = np.sqrt(Ey2 ** 2 + Ez2 ** 2)
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(Y2, Z2, Emag2, cmap='viridis', alpha=0.85, rstride=1, cstride=1)
        theta = np.linspace(0, np.pi, 200)
        ax.plot(a * np.sin(theta), np.zeros(200), a * np.cos(theta), color='red', linewidth=2)
        ax.set_xlabel('y [m]')
        ax.set_ylabel('z [m]')
        ax.set_zlabel('|E| [V/m]')
        ax.set_title('Halvcirkelformad yta: |E| över yz-planet')

class SphericalShellPotential(ProblemBase):
    name = '2.5 Sfäriskt laddat skal'
    description = 'Sfäriskt skal med radie a och laddning Q jämnt fördelad över ytan. Visar radiell elektrisk fältstyrka och potential.'
    parameters = [('Q', 'Total laddning Q [C]', 1e-09), ('a', 'Skalradie a [m]', 0.2), ('rmax', 'Största radie rmax [m]', 0.8)]

    def validate(self, params):
        if params['a'] <= 0 or params['rmax'] <= params['a']:
            return 'Kräver a > 0 och rmax > a.'
        return None

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        Q, a, rmax = (params['Q'], params['a'], params['rmax'])
        k = Q / (4 * math.pi * EPS0)
        if mode == 'Map':
            X, Z, R = _radial_slice_grid(rmax, n=220)
            Emap = np.where(R < a, 0.0, k / np.maximum(R, 1e-30) ** 2)
            _show_scalar_map(ax, fig, X, Z, Emap, title='Sfäriskt skal: |E|-karta', xlabel='x [m]', ylabel='z [m]', cbar_label='|E| [V/m]', scale='log', contours=True)
            ax.add_patch(Circle((0, 0), a, fill=False, color='white', linewidth=1.0))
            return
        r = np.linspace(1e-05, rmax, 1000)
        E = np.where(r < a, 0.0, k / r ** 2)
        V = np.where(r < a, k / a, k / r)
        if mode == 'Field':
            ax.plot(r, E)
            ax.set_ylabel('|E_r| [V/m]')
            ax.set_title('Sfäriskt skal: radiell elektrisk fältstyrka')
        else:
            ax.plot(r, V)
            ax.set_ylabel('V [V]')
            ax.set_title('Sfäriskt skal: potential')
        ax.axvline(a, linestyle='--', linewidth=1)
        ax.text(a, ax.get_ylim()[1] * 0.9, '  r=a', va='top')
        ax.set_xlabel('r [m]')
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        a = params['a']
        ax.add_patch(Circle((0.0, 0.0), a, fill=False, linewidth=2))
        ax.set_title('Geometriskiss')
        ax.set_aspect('equal')
        ax.set_xlim(-1.25 * a, 1.25 * a)
        ax.set_ylim(-1.25 * a, 1.25 * a)
        ax.set_axis_off()

    def draw_3d(self, fig, params, mode):
        """
        Genomskuren övre hemisfär som visar inre zon (E=0/V=konstant) och yttre zon.
        """
        fig.clear()
        Q, a, rmax = (params['Q'], params['a'], params['rmax'])
        k = Q / (4 * math.pi * EPS0)
        theta = np.linspace(0, np.pi / 2, 50)
        phi = np.linspace(0, 2 * np.pi, 70)
        T, P = np.meshgrid(theta, phi)
        ax = fig.add_subplot(111, projection='3d')
        for r_s, color, alpha, label in [(a * 0.5, 'steelblue', 0.35, 'insida'), (rmax * 0.75, 'coral', 0.4, 'utsida')]:
            val = 0.0 if mode == 'Field' and r_s < a else k / a if mode != 'Field' and r_s < a else k / r_s ** 2 if mode == 'Field' else k / r_s
            X = r_s * np.sin(T) * np.cos(P)
            Y = r_s * np.sin(T) * np.sin(P)
            Z = r_s * np.cos(T)
            ax.plot_surface(X, Y, Z, color=color, alpha=alpha, shade=True)
            ax.text(0, 0, r_s * 0.9, f"{('E' if mode == 'Field' else 'V')}={val:.2e}", fontsize=7, ha='center')
        ax.set_xlabel('x [m]')
        ax.set_ylabel('y [m]')
        ax.set_zlabel('z [m]')
        ax.set_title('Sfäriskt skal (övre hemisfär, genomskuret)')

class ConcentricChargedCylinders(ProblemBase):
    name = '2.6 Långa koncentriska laddade cylindrar'
    description = 'Två långa koncentriska cylindriska skal med radier a och b och ytladdningstätheter ρsa respektive ρsb. Visar radiellt fält och logaritmisk potential med V(rmax)=0 som referens.'
    parameters = [('rho_sa', 'Inre ytladdningstäthet ρsa [C/m²]', 1e-09), ('rho_sb', 'Yttre ytladdningstäthet ρsb [C/m²]', -4e-10), ('a', 'Inre radie a [m]', 0.08), ('b', 'Yttre radie b [m]', 0.22), ('rmax', 'Största radie rmax [m]', 0.6)]

    def validate(self, params):
        if params['a'] <= 0 or params['b'] <= params['a'] or params['rmax'] <= params['b']:
            return 'Kräver 0 < a < b < rmax.'
        return None

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        rho_sa, rho_sb = (params['rho_sa'], params['rho_sb'])
        a, b, rmax = (params['a'], params['b'], params['rmax'])
        c_mid = rho_sa * a / EPS0
        c_out = (rho_sa * a + rho_sb * b) / EPS0
        if mode == 'Map':
            X, Z, R = _radial_slice_grid(rmax, n=220)
            Emap = np.piecewise(R, [R < a, (R >= a) & (R < b), R >= b], [0.0, lambda rr: np.abs(c_mid) / np.maximum(rr, 1e-30), lambda rr: np.abs(c_out) / np.maximum(rr, 1e-30)])
            _show_scalar_map(ax, fig, X, Z, Emap, title='Koncentriska cylindrar: |E|-karta', xlabel='x [m]', ylabel='z [m]', cbar_label='|E| [V/m]', scale='log', contours=True)
            for rad in [a, b]:
                ax.add_patch(Circle((0, 0), rad, fill=False, color='white', linewidth=1.0))
            return
        r = np.linspace(1e-05, rmax, 1200)
        E = np.piecewise(r, [r < a, (r >= a) & (r < b), r >= b], [0.0, lambda rr: c_mid / rr, lambda rr: c_out / rr])
        V = np.piecewise(r, [r < a, (r >= a) & (r < b), r >= b], [lambda rr: c_out * np.log(rmax / b) + c_mid * np.log(b / a), lambda rr: c_out * np.log(rmax / b) + c_mid * np.log(b / rr), lambda rr: c_out * np.log(rmax / rr)])
        if mode == 'Field':
            ax.plot(r, E)
            ax.set_ylabel('E_R [V/m]')
            ax.set_title('Långa koncentriska cylindrar: radiellt elektriskt fält')
        else:
            ax.plot(r, V)
            ax.set_ylabel('V [V] (referens vid r=rmax)')
            ax.set_title('Långa koncentriska cylindrar: potential')
        ax.axvline(a, linestyle='--', linewidth=1)
        ax.axvline(b, linestyle='--', linewidth=1)
        ax.set_xlabel('R [m]')
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        a, b = (params['a'], params['b'])
        ax.add_patch(Circle((0.0, 0.0), a, fill=False, linewidth=2))
        ax.add_patch(Circle((0.0, 0.0), b, fill=False, linewidth=2))
        ax.set_title('Geometriskiss')
        ax.set_aspect('equal')
        ax.set_xlim(-1.25 * b, 1.25 * b)
        ax.set_ylim(-1.25 * b, 1.25 * b)
        ax.set_axis_off()

    def draw_3d(self, fig, params, mode):
        fig.clear()
        rho_sa, rho_sb = (params['rho_sa'], params['rho_sb'])
        a, b, rmax = (params['a'], params['b'], params['rmax'])
        r = np.linspace(0.03 * a, rmax, 180)
        if mode == 'Field':
            scalar = np.piecewise(r, [r < a, (r >= a) & (r < b), r >= b], [0.0, lambda rr: rho_sa * a / EPS0 / rr, lambda rr: (rho_sa * a + rho_sb * b) / EPS0 / rr])
            title = 'Koncentriska cylindrar: E(R) roterad'
            zlabel = 'R [m]'
        else:
            c_mid = rho_sa * a / EPS0
            c_out = (rho_sa * a + rho_sb * b) / EPS0
            scalar = np.piecewise(r, [r < a, (r >= a) & (r < b), r >= b], [lambda rr: c_out * np.log(rmax / b) + c_mid * np.log(b / a), lambda rr: c_out * np.log(rmax / b) + c_mid * np.log(b / rr), lambda rr: c_out * np.log(rmax / rr)])
            title = 'Koncentriska cylindrar: V(R) roterad'
            zlabel = 'R [m]'
        z = r.copy()
        ribbon_r = 0.06 * b * np.ones_like(r)
        ax = fig.add_subplot(111, projection='3d')
        _surface_of_revolution(ax, ribbon_r, z, scalar, n_phi=60, title=title, zlabel=zlabel)
        phi = np.linspace(0, 2 * np.pi, 200)
        for rad, color in [(a, 'red'), (b, 'black')]:
            ax.plot(rad * np.cos(phi), rad * np.sin(phi), np.zeros_like(phi), color=color, linewidth=2)

class SphericalCapacitorDesign(ProblemBase):
    name = '2.7 Sfärisk kondensator – största spänning'
    description = 'Designvy för sfärisk kondensator. Varierar den inre radien a och visar största tillåtna spänning när fältet inte får överstiga Emax.'
    parameters = [('b', 'Yttre radie b [m]', 1.0), ('Emax', 'Genomslagsfält Emax [V/m]', 2000000.0), ('samples', 'Antal sveppunkter', 300)]

    def validate(self, params):
        if params['b'] <= 0 or params['Emax'] <= 0:
            return 'b och Emax måste vara positiva.'
        if params['samples'] < 50:
            return 'Använd minst 50 sveppunkter.'
        return None

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        b, Emax = (params['b'], params['Emax'])
        samples = int(round(params['samples']))
        a = np.linspace(0.05 * b, 0.95 * b, samples)
        vmax = Emax * a * (b - a) / b
        a_opt = b / 2
        vmax_opt = Emax * a_opt * (b - a_opt) / b
        if mode == 'Field':
            ax.plot(a, Emax * np.ones_like(a))
            ax.set_ylabel('Största tillåtna fält vid inre sfären [V/m]')
            ax.set_title('Designvillkor för sfärisk kondensator')
        else:
            ax.plot(a, vmax)
            ax.axvline(a_opt, linestyle='--', linewidth=1)
            ax.set_ylabel('Största spänning [V]')
            ax.set_title('Sfärisk kondensator: maxspänning mot inre radie')
            ax.text(0.02, 0.98, f'Optimal a = {a_opt:.3g} m, Vmax = {vmax_opt:.3e} V', transform=ax.transAxes, va='top')
        ax.set_xlabel('Inre radie a [m]')
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        b = params['b']
        ax.add_patch(Circle((0.0, 0.0), b, fill=False, linewidth=2))
        ax.text(0, 0, 'designsvep', ha='center', va='center')
        ax.set_title('Geometriskiss')
        ax.set_aspect('equal')
        ax.set_xlim(-1.15 * b, 1.15 * b)
        ax.set_ylim(-1.15 * b, 1.15 * b)
        ax.set_axis_off()

    def draw_3d(self, fig, params, mode):
        """
        2-D-designlandskap: Vmax(a/b, Emax-skala) där den optimala
        åsen a/b = 0,5 markeras.
        """
        fig.clear()
        b, Emax_base = (params['b'], params['Emax'])
        a_frac = np.linspace(0.05, 0.95, 50)
        emax_frac = np.linspace(0.5, 2.0, 40)
        AF, EF = np.meshgrid(a_frac, emax_frac)
        VMAX = EF * Emax_base * AF * b * (b - AF * b) / b
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(AF, EF, VMAX, cmap='viridis', alpha=0.85, rstride=1, cstride=1)
        opt_v = emax_frac * Emax_base * 0.25 * b
        ax.plot(np.full_like(emax_frac, 0.5), emax_frac, opt_v, color='red', linewidth=2, label='optimalt a=b/2')
        ax.legend(fontsize=7)
        ax.set_xlabel('a/b')
        ax.set_ylabel('Emax / Emax_base')
        ax.set_zlabel('Vmax [V]')
        ax.set_title('Designlandskap: Vmax(a, Emax)')

class ConcentricSphericalShells(ProblemBase):
    name = '2.8 Koncentriska sfäriska metallskal'
    description = 'Två koncentriska ledande sfäriska skal med radier a och b och laddningar Qa respektive Qb. Visar radiell elektrisk fältstyrka eller potential.'
    parameters = [('Qa', 'Inre skalets laddning Qa [C]', 1e-09), ('Qb', 'Yttre skalets laddning Qb [C]', -4e-10), ('a', 'Inre radie a [m]', 0.15), ('b', 'Yttre radie b [m]', 0.35), ('rmax', 'Största radie rmax [m]', 0.8)]

    def validate(self, params):
        if params['a'] <= 0 or params['b'] <= params['a'] or params['rmax'] <= params['b']:
            return 'Kräver 0 < a < b < rmax.'
        return None

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        Qa, Qb = (params['Qa'], params['Qb'])
        a, b, rmax = (params['a'], params['b'], params['rmax'])
        k = 1 / (4 * math.pi * EPS0)
        if mode == 'Map':
            X, Z, R = _radial_slice_grid(rmax, n=220)
            Emap = np.piecewise(R, [R < a, (R >= a) & (R < b), R >= b], [0.0, lambda rr: np.abs(k * Qa) / np.maximum(rr, 1e-30) ** 2, lambda rr: np.abs(k * (Qa + Qb)) / np.maximum(rr, 1e-30) ** 2])
            _show_scalar_map(ax, fig, X, Z, Emap, title='Koncentriska sfäriska skal: |E|-karta', xlabel='x [m]', ylabel='z [m]', cbar_label='|E| [V/m]', scale='log', contours=True)
            for rad in [a, b]:
                ax.add_patch(Circle((0, 0), rad, fill=False, color='white', linewidth=1.0))
            return
        r = np.linspace(1e-05, rmax, 1200)
        E = np.piecewise(r, [r < a, (r >= a) & (r < b), r >= b], [0.0, lambda rr: k * Qa / rr ** 2, lambda rr: k * (Qa + Qb) / rr ** 2])
        V = np.piecewise(r, [r < a, (r >= a) & (r < b), r >= b], [lambda rr: k * (Qa / a + Qb / b), lambda rr: k * (Qa / rr + Qb / b), lambda rr: k * (Qa + Qb) / rr])
        if mode == 'Field':
            ax.plot(r, E)
            ax.set_ylabel('E_r [V/m]')
            ax.set_title('Koncentriska sfäriska skal: radiellt elektriskt fält')
        else:
            ax.plot(r, V)
            ax.set_ylabel('V [V]')
            ax.set_title('Koncentriska sfäriska skal: potential')
        ax.axvline(a, linestyle='--', linewidth=1)
        ax.axvline(b, linestyle='--', linewidth=1)
        ax.set_xlabel('r [m]')
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        a, b = (params['a'], params['b'])
        ax.add_patch(Circle((0.0, 0.0), a, fill=False, linewidth=2))
        ax.add_patch(Circle((0.0, 0.0), b, fill=False, linewidth=2))
        ax.set_title('Geometriskiss')
        ax.set_aspect('equal')
        ax.set_xlim(-1.2 * b, 1.2 * b)
        ax.set_ylim(-1.2 * b, 1.2 * b)
        ax.set_axis_off()

    def draw_3d(self, fig, params, mode):
        """
        Genomskuren övre hemisfär med tre radiella zoner (inre, gap, yttre),
        färgsatta och annoterade med respektive fält-/potentialvärde.
        """
        fig.clear()
        Qa, Qb = (params['Qa'], params['Qb'])
        a, b, rmax = (params['a'], params['b'], params['rmax'])
        k = 1 / (4 * math.pi * EPS0)
        theta = np.linspace(0, np.pi / 2, 50)
        phi = np.linspace(0, 2 * np.pi, 70)
        T, P = np.meshgrid(theta, phi)
        ax = fig.add_subplot(111, projection='3d')
        zones = [(a * 0.5, 'steelblue', 0.3), ((a + b) / 2, 'coral', 0.45), ((b + rmax) / 2, 'mediumseagreen', 0.4)]
        for r_m, color, alpha in zones:
            if mode == 'Field':
                val = 0.0 if r_m < a else k * Qa / r_m ** 2 if r_m < b else k * (Qa + Qb) / r_m ** 2
            else:
                val = k * (Qa / a + Qb / b) if r_m < a else k * (Qa / r_m + Qb / b) if r_m < b else k * (Qa + Qb) / r_m
            X = r_m * np.sin(T) * np.cos(P)
            Y = r_m * np.sin(T) * np.sin(P)
            Z = r_m * np.cos(T)
            ax.plot_surface(X, Y, Z, color=color, alpha=alpha, shade=True)
            ax.text(0, 0, r_m * 0.95, f'{val:.2e}', fontsize=7, ha='center', color=color)
        ax.set_xlabel('x [m]')
        ax.set_ylabel('y [m]')
        ax.set_zlabel('z [m]')
        ax.set_title('Koncentriska skal (genomskurna, värde per zon)')

class AtmosphericChargeDensity(ProblemBase):
    name = '2.9 Genomsnittlig luftelektrisk laddningstäthet'
    description = 'Beräknar genomsnittlig rymdladdningstäthet från hur det vertikala luftelektriska fältet ändras med höjden, med Gauss lag.'
    parameters = [('E_ground', 'Nedåtriktat fält vid marken [V/m]', 300.0), ('E_top', 'Nedåtriktat fält på höjden h [V/m]', 20.0), ('h', 'Höjd h [m]', 1400.0)]

    def validate(self, params):
        if params['h'] <= 0:
            return 'h måste vara positiv.'
        return None

    @staticmethod
    def rho_mean(E_ground, E_top, h):
        return EPS0 * (E_ground - E_top) / h

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        Eg, Et, h = (params['E_ground'], params['E_top'], params['h'])
        z = np.linspace(0, h, 300)
        E_down = Eg + (Et - Eg) * z / h
        rho = self.rho_mean(Eg, Et, h)
        if mode == 'Potential':
            ax.axhline(rho, linewidth=2)
            ax.set_ylabel('⟨ρ⟩ [C/m³]')
            ax.set_title(f'Genomsnittlig laddningstäthet: {rho:.3e} C/m³')
        else:
            ax.plot(z, E_down)
            ax.set_ylabel('Nedåtriktat |E| [V/m]')
            ax.set_title('Antagen linjär fältprofil mellan två höjder')
        ax.set_xlabel('z [m]')
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        h = params['h']
        ax.plot([-0.8, 0.8], [0, 0], linewidth=3)
        ax.plot([-0.8, 0.8], [h, h], linestyle='--')
        for zz, txt in [(0, 'mark'), (h, 'h')]:
            ax.text(0.9, zz, txt, va='center')
        for zz in np.linspace(0.1 * h, 0.9 * h, 5):
            ax.arrow(0, zz + 0.07 * h, 0, -0.05 * h, head_width=0.06, length_includes_head=True)
        ax.set_ylim(-0.1 * h, 1.1 * h)
        ax.set_xlim(-1, 1.4)
        ax.set_title('Gaussisk pillbox i vertikalled')
        ax.set_axis_off()

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        Eg, Et, h = (params['E_ground'], params['E_top'], params['h'])
        z = np.linspace(0, h, 40)
        r = np.linspace(0, 1, 12)
        R, Z = np.meshgrid(r, z)
        Phi = np.linspace(0, 2 * np.pi, 40)
        X = np.cos(Phi)[None, :] * np.ones((len(z), 1))
        Y = np.sin(Phi)[None, :] * np.ones((len(z), 1))
        Zsurf = z[:, None] * np.ones_like(X)
        ax.plot_surface(X, Y, Zsurf, alpha=0.18, color='steelblue')
        rho = self.rho_mean(Eg, Et, h)
        ax.text(0, 0, 0.5 * h, f'⟨ρ⟩={rho:.2e} C/m³', ha='center')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z [m]')
        ax.set_title('Gaussisk kolonn')

class OffsetCavitySphereExterior(ProblemBase):
    name = '2.10 Laddat klot med hålrum (x > b)'
    description = 'Isolerande material format till ett klot med radie b och ett sfäriskt hålrum med radie a vars centrum ligger förskjutet. Superposition används för att visa fält eller potential på +x-axeln för x > b.'
    parameters = [('rho', 'Rymdladdningstäthet ρ [C/m³]', 1e-06), ('a', 'Hålrummets radie a [m]', 0.1), ('b', 'Yttre klotradie b [m]', 0.3), ('d', 'Hålrummets förskjutning d [m]', 0.12), ('xmin', 'Start för plott xmin [m]', 0.32), ('xmax', 'Slut för plott xmax [m]', 1.2)]

    def validate(self, params):
        a, b, d = (params['a'], params['b'], params['d'])
        xmin, xmax = (params['xmin'], params['xmax'])
        if a <= 0 or b <= 0 or d < 0:
            return 'Kräver a > 0, b > 0 och d ≥ 0.'
        if b <= a + d:
            return 'Kräver b > a + d så att hålrummet ligger inne i klotet.'
        if xmin <= b or xmax <= xmin:
            return 'Kräver xmin > b och xmax > xmin.'
        return None

    @staticmethod
    def ex_field(x, rho, a, b, d):
        return rho / (3 * EPS0) * (b ** 3 / x ** 2 - a ** 3 / (x + d) ** 2)

    @staticmethod
    def potential(x, rho, a, b, d):
        return rho / (3 * EPS0) * (b ** 3 / x - a ** 3 / (x + d))

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        rho, a, b, d = (params['rho'], params['a'], params['b'], params['d'])
        xmin, xmax = (params['xmin'], params['xmax'])
        x = np.linspace(xmin, xmax, 900)
        if mode == 'Field':
            y = self.ex_field(x, rho, a, b, d)
            ax.plot(x, y)
            ax.set_ylabel('E_x [V/m]')
            ax.set_title('Laddat klot med hålrum: yttre fält på +x-axeln')
        else:
            y = self.potential(x, rho, a, b, d)
            ax.plot(x, y)
            ax.set_ylabel('V [V]')
            ax.set_title('Laddat klot med hålrum: yttre potential på +x-axeln')
        ax.axvline(b, linestyle='--', linewidth=1)
        ax.set_xlabel('x [m]')
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        a, b, d = (params['a'], params['b'], params['d'])
        ax.add_patch(Circle((0.0, 0.0), b, fill=False, linewidth=2))
        ax.add_patch(Circle((-d, 0.0), a, fill=False, linewidth=2, linestyle='--'))
        ax.plot([-1.2 * b, 1.35 * b], [0, 0], linewidth=1)
        ax.text(0.45 * b, 0.07 * b, '+x', fontsize=8)
        ax.text(-d, 0, 'hålrum', ha='center', va='center', fontsize=8)
        ax.set_title('Geometriskiss')
        ax.set_aspect('equal')
        ax.set_xlim(-1.25 * b, 1.45 * b)
        ax.set_ylim(-1.25 * b, 1.25 * b)
        ax.set_axis_off()

    def draw_3d(self, fig, params, mode):
        fig.clear()
        rho, a, b, d = (params['rho'], params['a'], params['b'], params['d'])
        x = np.linspace(params['xmin'], params['xmax'], 120)
        scalar = self.ex_field(x, rho, a, b, d) if mode == 'Field' else self.potential(x, rho, a, b, d)
        label = 'E_x [V/m]' if mode == 'Field' else 'V [V]'
        r_vals = 0.08 * b * np.ones_like(x)
        ax = fig.add_subplot(111, projection='3d')
        _surface_of_revolution(ax, r_vals, x, scalar, n_phi=60, title='Yttre x-axelprofil (roterad)', zlabel='x [m]')
        theta = np.linspace(0, np.pi, 40)
        phi = np.linspace(0, 2 * np.pi, 55)
        T, P = np.meshgrid(theta, phi)
        for xc, rad, col, alp in [(0.0, b, 'lightgrey', 0.18), (-d, a, 'white', 0.45)]:
            X = xc + rad * np.sin(T) * np.cos(P)
            Y = rad * np.sin(T) * np.sin(P)
            Z = rad * np.cos(T)
            ax.plot_surface(X, Y, Z, color=col, alpha=alp, shade=True)
        ax.text(0, 0, 1.15 * b, label, fontsize=7)

class CoaxialCylinderVoltage(ProblemBase):
    name = '2.11 Koaxiella cylindrar med pålagd spänning'
    description = 'Två långa koaxiella cylindriska ledare med radier a och b. Den inre ledaren ligger på 0 V och den yttre på U. Visar E(R) och V(R) samt markerar fältet mittemellan skalen.'
    parameters = [('U', 'Pålagd spänning U [V]', 300.0), ('a', 'Inre radie a [m]', 0.01), ('b', 'Yttre radie b [m]', 0.04), ('rmax', 'Plottad radie rmax [m]', 0.06)]

    def validate(self, params):
        if params['U'] <= 0 or params['a'] <= 0 or params['b'] <= params['a'] or (params['rmax'] <= params['b']):
            return 'Kräver U > 0 och 0 < a < b < rmax.'
        return None

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        U, a, b, rmax = (params['U'], params['a'], params['b'], params['rmax'])
        if mode == 'Map':
            X, Z, R = _radial_slice_grid(rmax, n=220)
            Emap = np.where((R >= a) & (R <= b), U / (np.maximum(R, 1e-30) * np.log(b / a)), 0.0)
            _show_scalar_map(ax, fig, X, Z, Emap, title='Koaxiella cylindrar: |E|-karta', xlabel='x [m]', ylabel='z [m]', cbar_label='|E| [V/m]', scale='log', contours=True)
            for rad in [a, b]:
                ax.add_patch(Circle((0, 0), rad, fill=False, color='white', linewidth=1.0))
            return
        r = np.linspace(a, b, 1200)
        E = U / (r * np.log(b / a))
        V = U * np.log(r / a) / np.log(b / a)
        r_mid = 0.5 * (a + b)
        E_mid = U / (r_mid * np.log(b / a))
        if mode == 'Field':
            ax.plot(r, E)
            ax.scatter([r_mid], [E_mid], s=35)
            ax.annotate(f'mittpunkt = {E_mid:.2e} V/m', (r_mid, E_mid), textcoords='offset points', xytext=(8, 8), fontsize=8)
            ax.set_ylabel('|E_R| [V/m]')
            ax.set_title('Koaxiella cylindrar: radiell elektrisk fältstyrka')
        else:
            ax.plot(r, V)
            ax.set_ylabel('V [V]')
            ax.set_title('Koaxiella cylindrar: potential')
        ax.axvline(a, linestyle='--', linewidth=1)
        ax.axvline(b, linestyle='--', linewidth=1)
        ax.set_xlabel('R [m]')
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        a, b = (params['a'], params['b'])
        ax.add_patch(Circle((0.0, 0.0), a, fill=False, linewidth=2))
        ax.add_patch(Circle((0.0, 0.0), b, fill=False, linewidth=2))
        ax.text(0, 0, '0 V', ha='center', va='center')
        ax.text(0, 0.72 * b, 'U', ha='center', va='center')
        ax.set_title('Geometriskiss')
        ax.set_aspect('equal')
        ax.set_xlim(-1.2 * b, 1.2 * b)
        ax.set_ylim(-1.2 * b, 1.2 * b)
        ax.set_axis_off()

    def draw_3d(self, fig, params, mode):
        fig.clear()
        U, a, b = (params['U'], params['a'], params['b'])
        z = np.linspace(0.0, 1.0, 140)
        if mode == 'Field':
            scalar = U / (np.linspace(a, b, 140) * np.log(b / a))
            title = 'Koaxiella cylindrar: E(R) roterad'
        else:
            rr = np.linspace(a, b, 140)
            scalar = U * np.log(rr / a) / np.log(b / a)
            title = 'Koaxiella cylindrar: V(R) roterad'
        r_vals = np.linspace(a, b, 140)
        ax = fig.add_subplot(111, projection='3d')
        _surface_of_revolution(ax, r_vals, z, scalar, n_phi=64, title=title, zlabel='z')

class SphericalConductorBreakdown(ProblemBase):
    name = '2.12 Sfärisk ledare i luft'
    description = 'Sfärisk ledare med radie a i luft. Fältet vid ytan får inte överstiga genomslagsfältet Emax. Visar radiellt fält/potential för vald laddning och anger begränsande laddning och potential.'
    parameters = [('a', 'Sfärradie a [m]', 0.1), ('Emax', 'Genomslagsfält Emax [V/m]', 3000000.0), ('Q', 'Laddning Q [C]', 2e-06), ('rmax', 'Största radie rmax [m]', 0.6)]

    def validate(self, params):
        if params['a'] <= 0 or params['Emax'] <= 0 or params['rmax'] <= params['a']:
            return 'Kräver a > 0, Emax > 0 och rmax > a.'
        return None

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        a, Emax, Q, rmax = (params['a'], params['Emax'], params['Q'], params['rmax'])
        k = 1 / (4 * math.pi * EPS0)
        r = np.linspace(a, rmax, 900)
        E = k * Q / r ** 2
        V = k * Q / r
        Qmax = 4 * math.pi * EPS0 * a ** 2 * Emax
        Vmax = a * Emax
        if mode == 'Field':
            ax.plot(r, E, label='Valt fält')
            ax.axhline(Emax, linestyle='--', linewidth=1, label='Emax')
            ax.set_ylabel('E_r [V/m]')
            ax.set_title('Sfärisk ledare: radiellt fält i luft')
        else:
            ax.plot(r, V, label='Vald potential')
            ax.set_ylabel('V [V]')
            ax.set_title('Sfärisk ledare: potential')
            ax.text(0.02, 0.98, f'Qmax = {Qmax:.3e} C\nVmax = {Vmax:.3e} V\nfält vid ytan = {k * Q / a ** 2:.3e} V/m', transform=ax.transAxes, va='top')
        ax.axvline(a, linestyle='--', linewidth=1)
        ax.set_xlabel('r [m]')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=8)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        a = params['a']
        ax.add_patch(Circle((0.0, 0.0), a, fill=False, linewidth=2))
        ax.text(0, 0, 'ledare', ha='center', va='center')
        ax.set_title('Geometriskiss')
        ax.set_aspect('equal')
        ax.set_xlim(-1.3 * a, 1.3 * a)
        ax.set_ylim(-1.3 * a, 1.3 * a)
        ax.set_axis_off()

    def draw_3d(self, fig, params, mode):
        fig.clear()
        a, Emax, Q, rmax = (params['a'], params['Emax'], params['Q'], params['rmax'])
        k = 1 / (4 * math.pi * EPS0)
        r = np.linspace(a, rmax, 140)
        scalar = k * Q / r ** 2 if mode == 'Field' else k * Q / r
        ax = fig.add_subplot(111, projection='3d')
        _surface_of_revolution(ax, r, np.zeros_like(r), scalar, title='Radiell profil roterad till sfäriskt skal', zlabel='E_r [V/m]' if mode == 'Field' else 'V [V]')
        phi = np.linspace(0, 2 * np.pi, 200)
        ax.plot(a * np.cos(phi), a * np.sin(phi), np.full_like(phi, np.min(scalar)), color='red', linewidth=2)
        qsurf = 4 * math.pi * EPS0 * a ** 2 * Emax
        ax.text(0, 0, np.max(scalar), f'Qmax={qsurf:.2e} C', fontsize=7)

class CoaxialTubeSpaceCharge(ProblemBase):
    name = '2.13 Koaxiellt urladdningsrör med rymdladdning'
    description = 'Koaxiell katod-anod-geometri med likformig rymdladdning mellan cylindrarna. Visar radiell elektrisk fältstyrka eller elektrostatisk potential.'
    parameters = [('a', 'Katodradie a [m]', 0.001), ('b', 'Anodradie b [m]', 0.004), ('U', 'Anodspänning U [V]', 300.0), ('ell', 'Längd ℓ [m]', 0.04), ('rmax', 'Största radie rmax [m]', 0.006)]

    def validate(self, params):
        if params['a'] <= 0 or params['b'] <= params['a'] or params['ell'] <= 0:
            return 'Kräver 0 < a < b och ℓ > 0.'
        if params['rmax'] <= params['b']:
            return 'rmax måste vara större än b.'
        return None

    @staticmethod
    def total_space_charge(a, b, ell, U):
        denom = b ** 2 - a ** 2 - 2 * a ** 2 * np.log(b / a)
        return -4 * math.pi * EPS0 * (b ** 2 - a ** 2) * ell * U / denom

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        a, b, U = (params['a'], params['b'], params['U'])
        ell, rmax = (params['ell'], params['rmax'])
        Q = self.total_space_charge(a, b, ell, U)
        rho = Q / (math.pi * (b ** 2 - a ** 2) * ell)
        r = np.linspace(a, rmax, 1200)
        # Med V(a)=0 och V(b)=U blir rho negativ för ett elektronmoln.
        # E_R = -dV/dR = rho/(2 eps0) * (R - a^2/R), alltså riktat inåt.
        E_gap = rho / (2 * EPS0) * (r - a ** 2 / r)
        E = np.where(r <= b, E_gap, 0.0)
        V_gap = -rho / (4 * EPS0) * (r ** 2 - a ** 2 - 2 * a ** 2 * np.log(r / a))
        V = np.where(r <= b, V_gap, U)
        if mode == 'Field':
            ax.plot(r, E)
            ax.set_ylabel('E_r [V/m]')
            ax.set_title('Koaxiellt rör med likformig rymdladdning: radiellt fält')
        else:
            ax.plot(r, V)
            ax.set_ylabel('V [V]')
            ax.set_title('Koaxiellt rör med likformig rymdladdning: potential')
        ax.axvline(a, linestyle='--', linewidth=1)
        ax.axvline(b, linestyle='--', linewidth=1)
        ax.set_xlabel('r [m]')
        ax.grid(True, alpha=0.3)
        ax.text(0.02, 0.98, f'Total rymdladdning Q = {Q:.3e} C', transform=ax.transAxes, va='top')

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        a, b = (params['a'], params['b'])
        ax.add_patch(Circle((0.0, 0.0), a, fill=False, linewidth=2))
        ax.add_patch(Circle((0.0, 0.0), b, fill=False, linewidth=2))
        ax.set_title('Geometriskiss')
        ax.set_aspect('equal')
        ax.set_xlim(-1.15 * b, 1.15 * b)
        ax.set_ylim(-1.15 * b, 1.15 * b)
        ax.set_axis_off()

    def draw_3d(self, fig, params, mode):
        """
        Roterar E_r(r) eller V(r) kring z-axeln och använder skalarvärdet
        som z-höjd. Det ger en tratt-/skålform som tydliggör den radiella profilen.
        Katod- och anodcylindrar läggs ovanpå som ringar.
        """
        fig.clear()
        a, b, U = (params['a'], params['b'], params['U'])
        ell, rmax = (params['ell'], params['rmax'])
        Q = self.total_space_charge(a, b, ell, U)
        rho = Q / (math.pi * (b ** 2 - a ** 2) * ell)
        r = np.linspace(a, rmax, 80)
        # Med V(a)=0 och V(b)=U blir rho negativ för ett elektronmoln.
        # E_R = -dV/dR = rho/(2 eps0) * (R - a^2/R), alltså riktat inåt.
        E_gap = rho / (2 * EPS0) * (r - a ** 2 / r)
        E = np.where(r <= b, E_gap, 0.0)
        V_gap = -rho / (4 * EPS0) * (r ** 2 - a ** 2 - 2 * a ** 2 * np.log(r / a))
        V = np.where(r <= b, V_gap, U)
        scalar = E if mode == 'Field' else V
        label = 'E_r [V/m]' if mode == 'Field' else 'V [V]'
        phi = np.linspace(0, 2 * np.pi, 60)
        R2, PHI = np.meshgrid(r, phi)
        S2 = np.tile(scalar, (60, 1))
        X2 = R2 * np.cos(PHI)
        Y2 = R2 * np.sin(PHI)
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X2, Y2, S2, cmap='plasma', alpha=0.85, rstride=1, cstride=1)
        z0, z1 = (np.min(scalar), np.max(scalar))
        for radius, col in [(a, 'steelblue'), (b, 'coral')]:
            xs = radius * np.cos(phi)
            ys = radius * np.sin(phi)
            ax.plot(xs, ys, np.full_like(phi, z0), color=col, linewidth=2)
            ax.plot(xs, ys, np.full_like(phi, z1), color=col, linewidth=2)
        ax.set_xlabel('x [m]')
        ax.set_ylabel('y [m]')
        ax.set_zlabel(label)
        ax.set_title(f'Koaxiellt: roterad {label}')

class RadialChargeSphere(ProblemBase):
    name = '2.16 Sfär med ρ(r)=A(a-r)'
    description = 'Sfäriskt symmetrisk rymdladdningstäthet ρ(r)=A(a-r) för r<a och ρ=0 utanför. Visar radiellt fält eller potential och anger potentialen i centrum.'
    parameters = [('A', 'Konstant A [C/m^4]', 1e-06), ('a', 'Sfärradie a [m]', 0.2), ('rmax', 'Största radie rmax [m]', 0.8)]

    def validate(self, params):
        if params['A'] == 0:
            return 'Använd A ≠ 0 så att graferna blir meningsfulla.'
        if params['a'] <= 0 or params['rmax'] <= params['a']:
            return 'Kräver a > 0 och rmax > a.'
        return None

    @staticmethod
    def _Qenc(A, a, r):
        r = np.asarray(r)
        return 4 * np.pi * A * (a * r ** 3 / 3 - r ** 4 / 4)

    @staticmethod
    def _E(A, a, r):
        r = np.asarray(r)
        E_in = A / EPS0 * (a * r / 3 - r ** 2 / 4)
        Qtot = 4 * np.pi * A * a ** 4 / 12
        E_out = Qtot / (4 * np.pi * EPS0 * np.maximum(r, 1e-300) ** 2)
        return np.where(r <= a, E_in, E_out)

    @staticmethod
    def _V(A, a, r):
        r = np.asarray(r)
        Qtot = 4 * np.pi * A * a ** 4 / 12
        V_out = Qtot / (4 * np.pi * EPS0 * np.maximum(r, 1e-300))
        V_in = A / EPS0 * (a ** 3 / 6 - a * r ** 2 / 6 + r ** 3 / 12)
        return np.where(r <= a, V_in, V_out)

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        A, a, rmax = (params['A'], params['a'], params['rmax'])
        r = np.linspace(1e-05 * a, rmax, 1000)
        if mode == 'Field':
            ax.plot(r, self._E(A, a, r))
            ax.set_ylabel('E_r [V/m]')
            ax.set_title('Sfär med ρ(r)=A(a-r): radiellt fält')
        else:
            ax.plot(r, self._V(A, a, r))
            ax.set_ylabel('V [V]')
            ax.set_title('Sfär med ρ(r)=A(a-r): potential')
            ax.text(0.02, 0.98, f'V(0) = {A * a ** 3 / (6 * EPS0):.3e} V', transform=ax.transAxes, va='top')
        ax.axvline(a, linestyle='--', linewidth=1)
        ax.set_xlabel('r [m]')
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        a = params['a']
        ax.add_patch(Circle((0, 0), a, fill=True, alpha=0.15))
        ax.add_patch(Circle((0, 0), a, fill=False, linewidth=2))
        ax.text(0, 0, 'ρ=A(a-r)', ha='center', va='center')
        ax.set_title('Geometriskiss')
        ax.set_aspect('equal')
        ax.set_xlim(-1.25 * a, 1.25 * a)
        ax.set_ylim(-1.25 * a, 1.25 * a)
        ax.set_axis_off()

    def draw_3d(self, fig, params, mode):
        fig.clear()
        A, a, rmax = (params['A'], params['a'], params['rmax'])
        r = np.linspace(0.0001 * a, rmax, 160)
        scalar = self._E(A, a, r) if mode == 'Field' else self._V(A, a, r)
        ax = fig.add_subplot(111, projection='3d')
        _surface_of_revolution(ax, r, np.zeros_like(r), scalar, title='Sfärisk radiell profil (roterad)', zlabel='E_r [V/m]' if mode == 'Field' else 'V [V]')
        phi = np.linspace(0, 2 * np.pi, 200)
        ax.plot(a * np.cos(phi), a * np.sin(phi), np.full_like(phi, np.min(scalar)), color='black', linewidth=1.6)

class InsertedMetalPlateCapacitor(ProblemBase):
    name = '2.18 Kondensator med införd metallplatta'
    description = 'Plattkondensator som först laddas upp och kopplas bort. Jämför ursprungligt fall med införd oladdad metallplatta eller ändrat plattavstånd.'
    parameters = [('A', 'Plattarea A [m²]', 0.05), ('d0', 'Ursprungligt avstånd d0 [m]', 0.01), ('U', 'Ursprunglig spänning U [V]', 200.0), ('d1', 'Införd metalltjocklek d1 [m]', 0.006), ('d2', 'Alternativt avstånd d2 [m]', 0.03)]

    def validate(self, params):
        if params['A'] <= 0 or params['d0'] <= 0 or params['U'] <= 0:
            return 'A, d0 och U måste vara positiva.'
        if params['d1'] <= 0 or params['d1'] >= params['d0']:
            return 'Kräver 0 < d1 < d0.'
        if params['d2'] <= 0:
            return 'd2 måste vara positivt.'
        return None

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        A, d0, U = (params['A'], params['d0'], params['U'])
        d1, d2 = (params['d1'], params['d2'])
        Q = EPS0 * A * U / d0
        E0 = U / d0
        U_inserted = U * (d0 - d1) / d0
        E_inserted = U_inserted / (d0 - d1)
        U_wider = U * d2 / d0
        E_wider = U_wider / d2
        labels = ['Ursprungligt fall', 'Med metallplatta', 'Större avstånd']
        values = [U, U_inserted, U_wider] if mode != 'Field' else [E0, E_inserted, E_wider]
        ax.bar(labels, values)
        ax.set_ylabel('Spänning [V]' if mode != 'Field' else 'Fält [V/m]')
        ax.set_title('Jämförelse för bortkopplad kondensator')
        ax.grid(True, axis='y', alpha=0.3)
        ax.text(0.02, 0.98, f'Lagrad laddning på varje platta: {Q:.3e} C', transform=ax.transAxes, va='top')

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        d0, d1 = (params['d0'], params['d1'])
        ax.plot([-0.7, 0.7], [0, 0], linewidth=3)
        ax.plot([-0.7, 0.7], [d0, d0], linewidth=3)
        ax.add_patch(Rectangle((-0.5, 0.5 * (d0 - d1)), 1.0, d1, fill=True, alpha=0.25))
        ax.set_title('Geometriskiss')
        ax.set_xlim(-0.9, 0.9)
        ax.set_ylim(-0.1 * d0, 1.1 * d0)
        ax.set_axis_off()

    def draw_3d(self, fig, params, mode):
        """
        3-D-yta: E eller V som funktion i designrummet (d1/d0, d2/d0).
        """
        fig.clear()
        d0, U = (params['d0'], params['U'])
        d1_arr = np.linspace(0.05 * d0, 0.95 * d0, 40)
        d2_arr = np.linspace(d0, 5 * d0, 40)
        D1, D2 = np.meshgrid(d1_arr, d2_arr)
        U_ins = U * (d0 - D1) / d0
        U_wid = U * D2 / d0
        E_ins = U / d0 * np.ones_like(D1)
        E_wid = U / d0 * np.ones_like(D2)
        ax = fig.add_subplot(111, projection='3d')
        if mode == 'Field':
            ax.plot_surface(D1 / d0, D2 / d0, E_ins, cmap='Blues', alpha=0.7, rstride=1, cstride=1, label='insert')
            ax.set_zlabel('E [V/m]')
            ax.set_title('Fält mot metallinlägg och avstånd')
        else:
            ax.plot_surface(D1 / d0, D2 / d0, U_ins, cmap='Blues', alpha=0.7, rstride=1, cstride=1)
            ax.plot_surface(D1 / d0, D2 / d0, U_wid, cmap='Oranges', alpha=0.5, rstride=1, cstride=1)
            ax.set_zlabel('V [V]')
            ax.set_title('Spänningslandskap\n(blå=inlägg, orange=större avstånd)')
        ax.set_xlabel('d1/d0')
        ax.set_ylabel('d2/d0')

class UniformSpaceChargePlates(ProblemBase):
    name = '2.19 Likformig rymdladdning mellan plattor'
    description = 'Två kondensatorplattor på avstånd d med likformigt fördelad rymdladdning ρ0 mellan sig. Ena plattan är jordad och den andra har potentialen V0.'
    parameters = [('rho0', 'Rymdladdningstäthet ρ0 [C/m³]', 1e-08), ('V0', 'Vänstra plattans potential V0 [V]', 50.0), ('d', 'Plattavstånd d [m]', 0.1)]

    def validate(self, params):
        if params['d'] <= 0 or abs(params['rho0']) < 1e-30:
            return 'd måste vara positivt och ρ0 får inte vara noll.'
        return None

    @staticmethod
    def profiles(x, rho0, V0, d):
        V = V0 + (-V0 / d + rho0 * d / (2 * EPS0)) * x - rho0 * x ** 2 / (2 * EPS0)
        E = V0 / d - rho0 * d / (2 * EPS0) + rho0 * x / EPS0
        return (E, V)

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        rho0, V0, d = (params['rho0'], params['V0'], params['d'])
        x = np.linspace(0, d, 600)
        E, V = self.profiles(x, rho0, V0, d)
        x0 = d / 2 - EPS0 * V0 / (rho0 * d)
        if mode == 'Map':
            X, Y = np.meshgrid(np.linspace(0, d, 240), np.linspace(-0.5 * d, 0.5 * d, 80))
            Em, _ = self.profiles(X, rho0, V0, d)
            _show_scalar_map(ax, fig, X, Y, Em, title='E_x mellan plattorna', xlabel='x [m]', ylabel='tvärkoordinat [m]', cbar_label='E_x [V/m]', scale='symlog', contours=True)
        elif mode == 'Potential':
            ax.plot(x, V)
            ax.set_ylabel('V [V]')
            ax.set_title('Potential mellan plattorna')
        else:
            ax.plot(x, E)
            ax.axhline(0, linewidth=1)
            if 0 <= x0 <= d:
                ax.axvline(x0, linestyle='--', linewidth=1)
                ax.text(x0, 0, '  E=0', va='bottom')
            ax.set_ylabel('E_x [V/m]')
            ax.set_title(f'Punkt där fältet är noll, x₀ = {x0:.3g} m')
        ax.set_xlabel('x från V0-plattan [m]')
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        d = params['d']
        ax.add_patch(Rectangle((0, -0.45 * d), 0.03 * d, 0.9 * d, fill=False, linewidth=2))
        ax.add_patch(Rectangle((d, -0.45 * d), 0.03 * d, 0.9 * d, fill=False, linewidth=2))
        ax.text(0, 0.55 * d, 'V0', ha='center')
        ax.text(d, 0.55 * d, '0 V', ha='center')
        ax.text(0.5 * d, -0.62 * d, 'likformig ρ0', ha='center')
        ax.set_xlim(-0.15 * d, 1.15 * d)
        ax.set_ylim(-0.75 * d, 0.75 * d)
        ax.set_aspect('equal')
        ax.set_title('Geometriskiss')
        ax.set_axis_off()

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        rho0, V0, d = (params['rho0'], params['V0'], params['d'])
        x = np.linspace(0, d, 90)
        y = np.linspace(-0.35 * d, 0.35 * d, 25)
        X, Y = np.meshgrid(x, y)
        E, V = self.profiles(X, rho0, V0, d)
        Z = E if mode == 'Field' else V
        ax.plot_surface(X, Y, Z, cmap='plasma', alpha=0.88)
        ax.set_xlabel('x [m]')
        ax.set_ylabel('y [m]')
        ax.set_zlabel('E_x [V/m]' if mode == 'Field' else 'V [V]')
        ax.set_title('Plattprofil som yta')
