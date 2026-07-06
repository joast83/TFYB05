"""Kapitel 3: Dielektriska material.

Uppgifter i detta kapitel (i menyordning):
    3.1    HClDipoleField
    3.3    PorcelainSlabCapacitor
    3.6    GroundedInnerSphereChargeSplit
    3.7    ChargedDielectricShell
    3.9    DielectricFilledSphericalGap
    3.11   MakrofolCapacitorDesign
    3.12   CoaxialTwoDielectricCapacitance
    3.13   BreakdownVoltageCases
    3.14   DielectricSlabCapacitor
    3.18   ElectretCylinderAxis
    3.19   ObliqueConductorDielectricBoundary
"""

from ..core import *


class HClDipoleField(ProblemBase):
    name = '3.1 HCl-molekyl: axel och ekvator'
    description = 'Modellerar H⁺ vid z=+d/2 och Cl⁻ vid z=-d/2 som punktladdningar ±q. Visar fältbelopp eller potential längs positiv z- och y-axel och markerar avståndet r0.'
    parameters = [('q', 'Laddningsbelopp q [C]', 1.602176634e-19), ('d', 'Separation d [m]', 2.18e-11), ('rmin', 'Start för plott rmin [m]', 5e-11), ('rmax', 'Slut för plott rmax [m]', 2e-09), ('r0', 'Markerat avstånd r0 [m]', 1e-09)]

    def validate(self, params):
        q, d = (params['q'], params['d'])
        rmin, rmax, r0 = (params['rmin'], params['rmax'], params['r0'])
        if q <= 0 or d <= 0:
            return 'Kräver q > 0 och d > 0.'
        if rmin <= d / 2:
            return 'Välj rmin > d/2 för att undvika punktladdningarna på z-axeln.'
        if rmax <= rmin:
            return 'Kräver rmax > rmin.'
        if not rmin <= r0 <= rmax:
            return 'r0 måste ligga inom plottområdet.'
        return None

    @staticmethod
    def e_axis(r, q, d):
        k = 1 / (4 * math.pi * EPS0)
        return k * q * (1 / (r - d / 2) ** 2 - 1 / (r + d / 2) ** 2)

    @staticmethod
    def e_equator(r, q, d):
        k = 1 / (4 * math.pi * EPS0)
        return k * q * d / np.power(r ** 2 + (d / 2) ** 2, 1.5)

    @staticmethod
    def v_axis(r, q, d):
        k = 1 / (4 * math.pi * EPS0)
        return k * q * (1 / (r - d / 2) - 1 / (r + d / 2))

    @staticmethod
    def v_equator(r, q, d):
        return np.zeros_like(r)

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        q, d = (params['q'], params['d'])
        rmin, rmax, r0 = (params['rmin'], params['rmax'], params['r0'])
        if mode == 'Map':
            y = np.linspace(-rmax, rmax, 220)
            z = np.linspace(-rmax, rmax, 220)
            Y, Z = np.meshgrid(y, z)
            kq = q / (4 * math.pi * EPS0)
            Rp = np.sqrt(Y ** 2 + (Z - d / 2) ** 2)
            Rm = np.sqrt(Y ** 2 + (Z + d / 2) ** 2)
            Ey = kq * (Y / np.maximum(Rp, 1e-30) ** 3 - Y / np.maximum(Rm, 1e-30) ** 3)
            Ez = kq * ((Z - d / 2) / np.maximum(Rp, 1e-30) ** 3 - (Z + d / 2) / np.maximum(Rm, 1e-30) ** 3)
            Emag = np.sqrt(Ey ** 2 + Ez ** 2)
            mask = (Rp < 0.08 * d) | (Rm < 0.08 * d)
            _show_scalar_map(ax, fig, Y, Z, Emag, title='HCl-modell: |E|-karta i yz-planet', xlabel='y [m]', ylabel='z [m]', cbar_label='|E| [V/m]', scale='log', mask=mask, contours=True)
            _overlay_vector_field(ax, Y, Z, Ey, Ez, mask=mask, max_arrows=23)
            ax.scatter([0, 0], [d / 2, -d / 2], color='white', edgecolors='black', linewidths=0.4, s=[30, 30], zorder=5)
            ax.text(0.05 * rmax, d / 2, '+q', color='white', fontsize=8, va='center')
            ax.text(0.05 * rmax, -d / 2, '−q', color='white', fontsize=8, va='center')
            return
        r = np.linspace(rmin, rmax, 1200)
        if mode == 'Field':
            ez = self.e_axis(r, q, d)
            ey = self.e_equator(r, q, d)
            ax.plot(r, ez, label='|E| på z-axeln')
            ax.plot(r, ey, label='|E| på y-axeln')
            ax.scatter([r0, r0], [self.e_axis(r0, q, d), self.e_equator(r0, q, d)], s=28)
            ax.set_ylabel('|E| [V/m]')
            ax.set_title('HCl-modell: fältbelopp på axel och ekvator')
        else:
            vz = self.v_axis(r, q, d)
            vy = self.v_equator(r, q, d)
            ax.plot(r, vz, label='V på z-axeln')
            ax.plot(r, vy, label='V på y-axeln')
            ax.scatter([r0], [self.v_axis(r0, q, d)], s=28)
            ax.set_ylabel('V [V]')
            ax.set_title('HCl-modell: potential på axel och ekvator')
        ax.axvline(r0, linestyle='--', linewidth=1)
        ax.set_xlabel('Avstånd från molekylens centrum [m]')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=8)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        d = params['d']
        ax.scatter([0, 0], [d / 2, -d / 2], s=[80, 80])
        ax.text(0.02 * d, d / 2, '+q', va='center')
        ax.text(0.02 * d, -d / 2, '-q', va='center')
        ax.plot([0, 0], [-0.9 * d, 0.9 * d], linewidth=1)
        ax.plot([-0.7 * d, 0.7 * d], [0, 0], linewidth=1)
        ax.text(0.08 * d, 0.72 * d, 'z')
        ax.text(0.62 * d, 0.05 * d, 'y')
        ax.set_title('Geometriskiss')
        ax.set_aspect('equal')
        ax.set_xlim(-0.9 * d, 0.9 * d)
        ax.set_ylim(-0.9 * d, 0.9 * d)
        ax.set_axis_off()

    def draw_3d(self, fig, params, mode):
        fig.clear()
        q, d = (params['q'], params['d'])
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter([0, 0], [0, 0], [d / 2, -d / 2], s=[80, 80])
        ax.text(0, 0, d / 2, '+q', fontsize=8)
        ax.text(0, 0, -d / 2, '-q', fontsize=8)
        yy = np.linspace(-8 * d, 8 * d, 7)
        zz = np.linspace(-8 * d, 8 * d, 9)
        Y, Z = np.meshgrid(yy, zz)
        X = np.zeros_like(Y)
        Ry_p = np.sqrt(Y ** 2 + (Z - d / 2) ** 2)
        Ry_m = np.sqrt(Y ** 2 + (Z + d / 2) ** 2)
        kq = q / (4 * math.pi * EPS0)
        Ey = kq * (Y / Ry_p ** 3 - Y / Ry_m ** 3)
        Ez = kq * ((Z - d / 2) / Ry_p ** 3 - (Z + d / 2) / Ry_m ** 3)
        mag = np.sqrt(Ey ** 2 + Ez ** 2) + 1e-30
        scale = 1.5 * d
        ax.quiver(X, Y, Z, np.zeros_like(Ey), scale * Ey / mag, scale * Ez / mag, length=1.0, normalize=False, arrow_length_ratio=0.28)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_title('Dipolfält i yz-planet')

class PorcelainSlabCapacitor(ProblemBase):
    name = '3.3 Plattkondensator med porslinsskiva'
    description = "Plattkondensator med en dielektrisk skiva av tjocklek td mellan plattorna. Läget 'Fält' visar E(z); läget 'D / flödestäthet' visar den konstanta elektriska flödestätheten D(z)."
    parameters = [('V0', 'Pålagd spänning V0 [V]', 10000.0), ('d', 'Plattavstånd d [m]', 0.01), ('td', 'Dielektrikets tjocklek td [m]', 0.005), ('eps_r', 'Relativ permittivitet εr [-]', 6.0)]

    def validate(self, params):
        if params['d'] <= 0 or params['td'] <= 0 or params['td'] >= params['d'] or (params['eps_r'] <= 0):
            return 'Kräver d > td > 0 och εr > 0.'
        return None

    @staticmethod
    def _fields(V0, d, td, eps_r):
        D = EPS0 * V0 / (d - td + td / eps_r)
        E_diel = D / (EPS0 * eps_r)
        E_air = D / EPS0
        return (E_diel, E_air, D)

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        V0, d, td, eps_r = (params['V0'], params['d'], params['td'], params['eps_r'])
        E_diel, E_air, D = self._fields(V0, d, td, eps_r)
        if mode == 'Map':
            x = np.linspace(-0.5, 0.5, 180)
            z = np.linspace(0, d, 220)
            X, Z = np.meshgrid(x, z)
            data = np.where(Z <= td, E_diel, E_air)
            _show_scalar_map(ax, fig, X, Z, data, title='Porslinsskiva i kondensator: |E|-karta', xlabel='x', ylabel='z [m]', cbar_label='|E| [V/m]', scale='log')
            ax.axhline(td, color='white', linestyle='--', linewidth=0.9)
            return
        z = np.linspace(0, d, 700)
        y = np.where(z <= td, E_diel if mode == 'Field' else D, E_air if mode == 'Field' else D)
        ax.plot(z, y)
        ax.axvline(td, linestyle='--', linewidth=1)
        ax.text(td, ax.get_ylim()[1] * 0.88 if np.max(np.abs(y)) > 0 else 0.1, '  dielektrikum/luft', va='top')
        ax.set_xlabel('z [m]')
        if mode == 'Field':
            ax.set_ylabel('E [V/m]')
            ax.set_title('Porslinsskiva i kondensator: elektrisk fältstyrka')
        else:
            ax.set_ylabel('D [C/m²]')
            ax.set_title('Porslinsskiva i kondensator: elektrisk flödestäthet')
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        d, td = (params['d'], params['td'])
        ax.plot([-0.6, 0.6], [0, 0], linewidth=3)
        ax.plot([-0.6, 0.6], [d, d], linewidth=3)
        ax.add_patch(Rectangle((-0.5, 0), 1.0, td, fill=True, alpha=0.22))
        ax.add_patch(Rectangle((-0.5, td), 1.0, d - td, fill=False, linewidth=1.5))
        ax.text(0, td / 2, 'porslin', ha='center', va='center')
        ax.text(0, td + (d - td) / 2, 'luft', ha='center', va='center')
        ax.set_title('Geometriskiss')
        ax.set_xlim(-0.8, 0.8)
        ax.set_ylim(-0.1 * d, 1.1 * d)
        ax.set_axis_off()

    def draw_3d(self, fig, params, mode):
        fig.clear()
        V0, d, td, eps_r = (params['V0'], params['d'], params['td'], params['eps_r'])
        E_diel, E_air, D = self._fields(V0, d, td, eps_r)
        W = 1.0
        ax = fig.add_subplot(111, projection='3d')
        _draw_box(ax, -W / 2, W / 2, -W / 2, W / 2, 0, td, 'lightsteelblue', 0.3)
        _draw_box(ax, -W / 2, W / 2, -W / 2, W / 2, td, d, 'lemonchiffon', 0.28)
        _draw_box(ax, -W / 2, W / 2, -W / 2, W / 2, -0.06 * d, 0, 'grey', 0.6)
        _draw_box(ax, -W / 2, W / 2, -W / 2, W / 2, d, 1.06 * d, 'grey', 0.6)
        val_d = E_diel if mode == 'Field' else D
        val_a = E_air if mode == 'Field' else D
        for xi in np.linspace(-W / 3, W / 3, 3):
            for yi in np.linspace(-W / 3, W / 3, 3):
                ax.quiver(xi, yi, td * 0.35, 0, 0, d * 0.26, color='navy', linewidth=1, arrow_length_ratio=0.35)
                ax.quiver(xi, yi, td + (d - td) * 0.25, 0, 0, d * 0.42, color='darkred', linewidth=1, arrow_length_ratio=0.35)
        lbl = 'E' if mode == 'Field' else 'D'
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z [m]')
        ax.set_title(f'Porslinsskiva 3D\nporslin {lbl}={val_d:.2e}, luft {lbl}={val_a:.2e}')
        ax.set_xlim(-W / 2, W / 2)
        ax.set_ylim(-W / 2, W / 2)
        ax.set_zlim(-0.1 * d, 1.1 * d)

class GroundedInnerSphereChargeSplit(ProblemBase):
    name = '3.6 Jordad inre sfär och laddat yttre skal'
    description = 'Sfäriskt skal med radie 3a och en jordad ledande sfär med radie a i centrum, med dielektrikum εr i mellanrummet. Visar hur laddningen på yttre skalet fördelas på inner- och ytteryta.'
    parameters = [('Q', 'Total laddning på yttre skalet Q [C]', 1e-09), ('a', 'Inre sfärens radie a [m]', 0.1), ('eps_r', 'Relativ permittivitet εr [-]', 2.5)]

    def validate(self, params):
        if params['a'] <= 0 or params['eps_r'] <= 0:
            return 'a och εr måste vara positiva.'
        return None

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        Q, eps_r = (params['Q'], params['eps_r'])
        q_inside = Q / (1 + 2 * eps_r)
        q_outside = Q - q_inside
        ax.bar(['Inneryta', 'Ytteryta'], [q_inside, q_outside])
        ax.set_ylabel('Laddning [C]')
        ax.set_title('Laddningsfördelning på yttre skalet')
        ax.grid(True, axis='y', alpha=0.3)
        ax.text(0.02, 0.98, f'Qoutside / Qinside = {q_outside / q_inside:.3g}', transform=ax.transAxes, va='top')

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        a = params['a']
        outer = 3 * a
        ax.add_patch(Circle((0.0, 0.0), a, fill=False, linewidth=2))
        ax.add_patch(Circle((0.0, 0.0), outer, fill=False, linewidth=2))
        ax.text(0, 0, 'jordad', ha='center', va='center')
        ax.set_title('Geometriskiss')
        ax.set_aspect('equal')
        ax.set_xlim(-1.15 * outer, 1.15 * outer)
        ax.set_ylim(-1.15 * outer, 1.15 * outer)
        ax.set_axis_off()

    def draw_3d(self, fig, params, mode):
        """
        3-D-yta av laddningskvoten Qut/Qin över parameterplanet (Q, εr).
        """
        fig.clear()
        Q_base = params['Q']
        eps_arr = np.linspace(1.0, 10.0, 40)
        Q_arr = np.linspace(0.1 * Q_base, 3 * Q_base, 40)
        EPS, QQ = np.meshgrid(eps_arr, Q_arr)
        q_in = QQ / (1 + 2 * EPS)
        ratio = (QQ - q_in) / q_in
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(EPS, QQ * 1000000000.0, ratio, cmap='coolwarm', alpha=0.85, rstride=1, cstride=1)
        ax.set_xlabel('εr')
        ax.set_ylabel('Q [nC]')
        ax.set_zlabel('Qut / Qin')
        ax.set_title('Laddningskvot mot (εr, Q)')

class ChargedDielectricShell(ProblemBase):
    name = '3.7 Laddat dielektriskt sfäriskt skal'
    description = 'Området a < r < b är fyllt med dielektrikum med relativ permittivitet εr och likformig fri rymdladdningstäthet ρ0. Områdena r < a och r > b är vakuum. Visar radiellt fält eller potential.'
    parameters = [('rho0', 'Rymdladdningstäthet ρ0 [C/m³]', 1e-07), ('a', 'Inre radie a [m]', 0.12), ('b', 'Yttre radie b [m]', 0.28), ('eps_r', 'Relativ permittivitet εr [-]', 3.0), ('rmax', 'Största radie rmax [m]', 0.7)]

    def validate(self, params):
        a, b, eps_r, rmax = (params['a'], params['b'], params['eps_r'], params['rmax'])
        if a <= 0 or b <= a or rmax <= b:
            return 'Kräver 0 < a < b < rmax.'
        if eps_r <= 0:
            return 'εr måste vara positiv.'
        return None

    @staticmethod
    def e_field(r, rho0, a, b, eps_r):
        r = np.asarray(r)
        e = np.zeros_like(r, dtype=float)
        mask_mid = (r >= a) & (r < b)
        mask_out = r >= b
        e[mask_mid] = rho0 * (r[mask_mid] ** 3 - a ** 3) / (3 * EPS0 * eps_r * r[mask_mid] ** 2)
        e[mask_out] = rho0 * (b ** 3 - a ** 3) / (3 * EPS0 * r[mask_out] ** 2)
        return e

    @staticmethod
    def potential(r, rho0, a, b, eps_r):
        r = np.asarray(r)
        v = np.zeros_like(r, dtype=float)
        v_out = rho0 * (b ** 3 - a ** 3) / (3 * EPS0 * np.maximum(r, 1e-30))
        mask_out = r >= b
        v[mask_out] = v_out[mask_out]
        vb = rho0 * (b ** 3 - a ** 3) / (3 * EPS0 * b)
        mask_mid = (r >= a) & (r < b)
        rm = r[mask_mid]
        v[mask_mid] = vb + rho0 / (3 * EPS0 * eps_r) * (0.5 * (b ** 2 - rm ** 2) + a ** 3 * (1 / b - 1 / rm))
        va = vb + rho0 / (3 * EPS0 * eps_r) * (0.5 * (b ** 2 - a ** 2) + a ** 3 * (1 / b - 1 / a))
        v[r < a] = va
        return v

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        rho0, a, b = (params['rho0'], params['a'], params['b'])
        eps_r, rmax = (params['eps_r'], params['rmax'])
        if mode == 'Map':
            X, Z, R = _radial_slice_grid(rmax, n=220)
            Emap = self.e_field(R, rho0, a, b, eps_r)
            _show_scalar_map(ax, fig, X, Z, Emap, title='Laddat dielektriskt skal: |E|-karta', xlabel='x [m]', ylabel='z [m]', cbar_label='|E| [V/m]', scale='log', contours=True)
            for rad in [a, b]:
                ax.add_patch(Circle((0, 0), rad, fill=False, color='white', linewidth=1.0))
            return
        r = np.linspace(0.0001 * a, rmax, 1200)
        if mode == 'Field':
            y = self.e_field(r, rho0, a, b, eps_r)
            ax.plot(r, y)
            ax.set_ylabel('E_r [V/m]')
            ax.set_title('Laddat dielektriskt skal: radiell elektrisk fältstyrka')
        else:
            y = self.potential(r, rho0, a, b, eps_r)
            ax.plot(r, y)
            ax.set_ylabel('V [V]')
            ax.set_title('Laddat dielektriskt skal: potential')
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
        ax.text(0, 0, 'vakuum', ha='center', va='center', fontsize=8)
        ax.text(0, 0.65 * (a + b) / 2, 'ρ0, εr', ha='center', va='center', fontsize=8)
        ax.set_title('Geometriskiss')
        ax.set_aspect('equal')
        ax.set_xlim(-1.15 * b, 1.15 * b)
        ax.set_ylim(-1.15 * b, 1.15 * b)
        ax.set_axis_off()

    def draw_3d(self, fig, params, mode):
        fig.clear()
        rho0, a, b = (params['rho0'], params['a'], params['b'])
        eps_r = params['eps_r']
        r_vals = np.linspace(0.02 * b, b, 140)
        z_vals = np.linspace(0.0, b, 140)
        scalar = self.e_field(r_vals, rho0, a, b, eps_r) if mode == 'Field' else self.potential(r_vals, rho0, a, b, eps_r)
        ax = fig.add_subplot(111, projection='3d')
        _surface_of_revolution(ax, r_vals, z_vals, scalar, n_phi=60, title='Radiell profil (roterad)', zlabel='z [m]')
        phi = np.linspace(0, 2 * np.pi, 200)
        for rad, col in [(a, 'black'), (b, 'red')]:
            ax.plot(rad * np.cos(phi), rad * np.sin(phi), np.zeros_like(phi), color=col, linewidth=1.2)

class DielectricFilledSphericalGap(ProblemBase):
    name = '3.9 Sfäriska skal med två dielektrika'
    description = 'Koncentriska ledande sfärer där mellanrummet är uppdelat i två hemisfäriska dielektrika. Visar radiellt E tillsammans med styckvis D-belopp i respektive halvrum.'
    parameters = [('Q', 'Inre sfärens laddning Q [C]', 1e-09), ('a', 'Inre radie a [m]', 0.15), ('b', 'Yttre radie b [m]', 0.35), ('eps1', 'Relativ permittivitet ε1 [-]', 4.0), ('eps2', 'Relativ permittivitet ε2 [-]', 2.0), ('rmax', 'Största radie rmax [m]', 0.7)]

    def validate(self, params):
        if params['a'] <= 0 or params['b'] <= params['a']:
            return 'Kräver 0 < a < b.'
        if params['eps1'] <= 0 or params['eps2'] <= 0:
            return 'ε1 och ε2 måste vara positiva.'
        if params['rmax'] <= params['b']:
            return 'rmax måste vara större än b.'
        return None

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        Q, a, b = (params['Q'], params['a'], params['b'])
        eps1, eps2, rmax = (params['eps1'], params['eps2'], params['rmax'])
        if mode == 'Map':
            X, Z, R = _radial_slice_grid(rmax, n=220)
            e_gap = np.abs(Q) / (2 * math.pi * EPS0 * (eps1 + eps2) * np.maximum(R, 1e-30) ** 2)
            e_out = np.abs(Q) / (4 * math.pi * EPS0 * np.maximum(R, 1e-30) ** 2)
            Emap = np.where((R >= a) & (R < b), e_gap, np.where(R >= b, e_out, 0.0))
            _show_scalar_map(ax, fig, X, Z, Emap, title='Sfäriskt gap med två dielektrika: |E|-karta', xlabel='x [m]', ylabel='z [m]', cbar_label='|E| [V/m]', scale='log', contours=True)
            for rad in [a, b]:
                ax.add_patch(Circle((0, 0), rad, fill=False, color='white', linewidth=1.0))
            ax.axvline(0.0, color='white', linestyle=':', linewidth=0.8)
            return
        r = np.linspace(a, rmax, 1000)
        e_gap = Q / (2 * math.pi * EPS0 * (eps1 + eps2) * r ** 2)
        d1_gap = eps1 * Q / ((eps1 + eps2) * 2 * math.pi * r ** 2)
        d2_gap = eps2 * Q / ((eps1 + eps2) * 2 * math.pi * r ** 2)
        e_out = Q / (4 * math.pi * EPS0 * r ** 2)
        if mode == 'Field':
            ax.plot(r, np.where(r < b, e_gap, e_out), label='|E_r|')
            ax.set_ylabel('Fält [V/m]')
            ax.set_title('Sfäriskt gap med två dielektrika: elektrisk fältstyrka')
        else:
            ax.plot(r, np.where(r < b, d1_gap, np.nan), label='|D| i ε1-området')
            ax.plot(r, np.where(r < b, d2_gap, np.nan), label='|D| i ε2-området')
            ax.set_ylabel('D [C/m²]')
            ax.set_title('Sfäriskt gap med två dielektrika: elektrisk flödestäthet')
        ax.legend()
        ax.axvline(a, linestyle='--', linewidth=1)
        ax.axvline(b, linestyle='--', linewidth=1)
        ax.set_xlabel('r [m]')
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        a, b = (params['a'], params['b'])
        ax.add_patch(Circle((0.0, 0.0), a, fill=False, linewidth=2))
        t1 = np.linspace(-np.pi / 2, np.pi / 2, 200)
        t2 = np.linspace(np.pi / 2, 3 * np.pi / 2, 200)
        ax.plot(b * np.cos(t1), b * np.sin(t1), linewidth=2)
        ax.plot(b * np.cos(t2), b * np.sin(t2), linewidth=2, linestyle='--')
        ax.plot([0, 0], [-b, b], linewidth=1)
        ax.set_title('Geometriskiss')
        ax.set_aspect('equal')
        ax.set_xlim(-1.15 * b, 1.15 * b)
        ax.set_ylim(-1.15 * b, 1.15 * b)
        ax.set_axis_off()

    def draw_3d(self, fig, params, mode):
        """
        Två halvklotskal i mitten av gapet, färgade blått (ε1) och rött (ε2),
        med annoterade fält-/D-värden.
        """
        fig.clear()
        Q, a, b = (params['Q'], params['a'], params['b'])
        eps1, eps2 = (params['eps1'], params['eps2'])
        r_mid = (a + b) / 2
        e_mid = Q / (2 * math.pi * EPS0 * (eps1 + eps2) * r_mid ** 2)
        d1_mid = eps1 * Q / ((eps1 + eps2) * 2 * math.pi * r_mid ** 2)
        d2_mid = eps2 * Q / ((eps1 + eps2) * 2 * math.pi * r_mid ** 2)
        theta = np.linspace(0, np.pi, 50)
        phi_h1 = np.linspace(0, np.pi, 60)
        phi_h2 = np.linspace(np.pi, 2 * np.pi, 60)
        ax = fig.add_subplot(111, projection='3d')
        for r_s, alpha in [(a, 0.3), (r_mid, 0.55), (b, 0.3)]:
            for ph, col in [(phi_h1, 'steelblue'), (phi_h2, 'coral')]:
                T, P = np.meshgrid(theta, ph)
                X = r_s * np.sin(T) * np.cos(P)
                Y = r_s * np.sin(T) * np.sin(P)
                Z = r_s * np.cos(T)
                ax.plot_surface(X, Y, Z, color=col, alpha=alpha, shade=True)
        if mode == 'Field':
            ax.text(r_mid * 0.7, 0, 0, f'E={e_mid:.2e}', fontsize=7, color='navy')
        else:
            ax.text(r_mid * 0.7, 0, 0, f'D1={d1_mid:.2e}', fontsize=7, color='steelblue')
            ax.text(-r_mid * 0.7, 0, 0, f'D2={d2_mid:.2e}', fontsize=7, color='coral')
        ax.set_xlabel('x [m]')
        ax.set_ylabel('y [m]')
        ax.set_zlabel('z [m]')
        ax.set_title('Tvådielektriskt gap (blå=ε1, röd=ε2)')

class MakrofolCapacitorDesign(ProblemBase):
    name = '3.11 Makrofol-kondensator'
    description = 'Designverktyg för en plattkondensator byggd av staplade Makrofol-skivor. Beräknar minsta antal skivor för att tåla spänningen och den plattarea som krävs för önskad kapacitans.'
    parameters = [('C_target', 'Önskad kapacitans C [F]', 1e-10), ('U', 'Krävd spänning U [V]', 50000.0), ('t_sheet', 'Skivtjocklek [m]', 0.0001), ('eps_r', 'Relativ permittivitet εr [-]', 3.0), ('E_break', 'Genomslagsfält [V/m]', 200000000.0), ('nmax', 'Max antal skivor i svepet', 40)]

    def validate(self, params):
        if any((params[k] <= 0 for k in ['C_target', 'U', 't_sheet', 'eps_r', 'E_break'])):
            return 'Alla fysikaliska parametrar måste vara positiva.'
        if params['nmax'] < 5:
            return 'Använd minst 5 skivor i svepet.'
        return None

    @staticmethod
    def _area_needed(C, n, t_sheet, eps_r):
        d = n * t_sheet
        return C * d / (EPS0 * eps_r)

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        C = params['C_target']
        U = params['U']
        t_sheet = params['t_sheet']
        eps_r = params['eps_r']
        E_break = params['E_break']
        nmax = int(round(params['nmax']))
        n_min = max(1, math.ceil(U / (E_break * t_sheet)))
        n = np.arange(1, nmax + 1)
        if mode == 'Field':
            E = U / (n * t_sheet)
            ax.plot(n, E)
            ax.axhline(E_break, linestyle='--', linewidth=1)
            ax.axvline(n_min, linestyle='--', linewidth=1)
            ax.set_ylabel('Fält i dielektrikum [V/m]')
            ax.set_title('Makrofolstapel: fält mot antal skivor')
        else:
            Areq = self._area_needed(C, n, t_sheet, eps_r)
            ax.plot(n, Areq)
            ax.axvline(n_min, linestyle='--', linewidth=1)
            ax.set_ylabel('Krävd plattarea [m²]')
            ax.set_title('Makrofolstapel: krävd area mot antal skivor')
            ax.text(0.02, 0.98, f'Minsta antal skivor = {n_min}\nArea vid n_min = {self._area_needed(C, n_min, t_sheet, eps_r):.3e} m²', transform=ax.transAxes, va='top')
        ax.set_xlabel('Antal skivor')
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        n_show = min(8, max(2, int(math.ceil(params['U'] / (params['E_break'] * params['t_sheet'])))))
        h = 1.0 / n_show
        for i in range(n_show):
            ax.add_patch(Rectangle((-0.45, i * h), 0.9, 0.8 * h, fill=True, alpha=0.15))
        ax.plot([-0.6, 0.6], [0, 0], linewidth=3)
        ax.plot([-0.6, 0.6], [1.0, 1.0], linewidth=3)
        ax.text(0, 0.5, f'{n_show} representativa\nMakrofol-skivor', ha='center', va='center')
        ax.set_xlim(-0.8, 0.8)
        ax.set_ylim(-0.05, 1.05)
        ax.set_title('Geometriskiss')
        ax.set_axis_off()

    def draw_3d(self, fig, params, mode):
        fig.clear()
        C = params['C_target']
        t_sheet = params['t_sheet']
        eps_r = params['eps_r']
        E_break = params['E_break']
        Umax = params['U'] * 1.8
        nmax = int(round(params['nmax']))
        N = np.arange(1, nmax + 1)
        U = np.linspace(0.1 * params['U'], Umax, 45)
        NN, UU = np.meshgrid(N, U)
        if mode == 'Field':
            Z = UU / (NN * t_sheet)
            zlabel = 'Fält [V/m]'
        else:
            n_eff = np.maximum(1, np.ceil(UU / (E_break * t_sheet)))
            Z = self._area_needed(C, n_eff, t_sheet, eps_r)
            zlabel = 'Krävd area [m²]'
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(NN, UU / 1000.0, Z, cmap='viridis', alpha=0.85, rstride=1, cstride=1)
        ax.set_xlabel('Antal skivor n')
        ax.set_ylabel('Spänning [kV]')
        ax.set_zlabel(zlabel)
        ax.set_title('Makrofol-designsvep')

class CoaxialTwoDielectricCapacitance(ProblemBase):
    name = '3.12 Koaxiell kondensator med två dielektriska skikt'
    description = 'Koaxiell kondensator med två dielektriska skikt av lika tjocklek. Visar C/L och radiellt E- eller D-fält för pålagd spänning U.'
    parameters = [('a', 'Inre radie a [m]', 0.02), ('c', 'Yttre radie c [m]', 0.05), ('eps1', 'Inre relativ permittivitet ε1', 4.0), ('eps2', 'Yttre relativ permittivitet ε2', 3.0), ('U', 'Pålagd spänning U [V]', 100.0)]

    def validate(self, params):
        if params['a'] <= 0 or params['c'] <= params['a']:
            return 'Kräver 0 < a < c.'
        if params['eps1'] <= 0 or params['eps2'] <= 0:
            return 'Relativa permittiviteter måste vara positiva.'
        return None

    @staticmethod
    def c_per_length(a, c, eps1, eps2):
        b = 0.5 * (a + c)
        return 2 * math.pi * EPS0 / (math.log(b / a) / eps1 + math.log(c / b) / eps2)

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        a, c, e1, e2, U = (params['a'], params['c'], params['eps1'], params['eps2'], params['U'])
        b = 0.5 * (a + c)
        C = self.c_per_length(a, c, e1, e2)
        lam = C * U
        R = np.linspace(a, c, 700)
        epsr = np.where(R <= b, e1, e2)
        D = lam / (2 * math.pi * R)
        E = D / (EPS0 * epsr)
        if mode == 'D':
            ax.plot(R, D)
            ax.set_ylabel('D_R [C/m²]')
            ax.set_title(f'C/L = {C * 1000000000.0:.3g} nF/m')
        else:
            ax.plot(R, E)
            ax.set_ylabel('E_R [V/m]')
            ax.set_title('Radiellt elektriskt fält i två dielektriska skikt')
        ax.axvline(b, linestyle='--', linewidth=1)
        ax.text(b, ax.get_ylim()[1] * 0.9, '  interface', va='top')
        ax.set_xlabel('R [m]')
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        a, c = (params['a'], params['c'])
        b = 0.5 * (a + c)
        ax.add_patch(Circle((0, 0), c, fill=False, linewidth=2))
        ax.add_patch(Circle((0, 0), b, fill=False, linestyle='--'))
        ax.add_patch(Circle((0, 0), a, fill=False, linewidth=2))
        ax.text(0, 0, 'ledare', ha='center', va='center', fontsize=8)
        ax.text(0.5 * (a + b), 0, 'ε1', ha='center', fontsize=9)
        ax.text(0.5 * (b + c), 0, 'ε2', ha='center', fontsize=9)
        ax.set_aspect('equal')
        ax.set_xlim(-1.2 * c, 1.2 * c)
        ax.set_ylim(-1.2 * c, 1.2 * c)
        ax.set_title('Koaxiella skikt')
        ax.set_axis_off()

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        a, c, e1, e2, U = (params['a'], params['c'], params['eps1'], params['eps2'], params['U'])
        b = 0.5 * (a + c)
        C = self.c_per_length(a, c, e1, e2)
        lam = C * U
        R = np.linspace(a, c, 100)
        D = lam / (2 * math.pi * R)
        epsr = np.where(R <= b, e1, e2)
        scalar = D / (EPS0 * epsr) if mode == 'Field' else D
        _surface_of_revolution(ax, 0.03 * c * np.ones_like(R), R, scalar, title='Radiell profil roterad', zlabel='R [m]')

class BreakdownVoltageCases(ProblemBase):
    name = '3.13 Genomslagsspänning för plattkondensatorer'
    description = "Jämför största tillåtna spänning för tre plattkondensatorfall: enbart luft, enbart plexiglas och blandning luft/plexiglas. Läget 'Fältprofil' visar begränsande fältprofil; läget 'Umax-svep' visar Umax mot dielektrikets tjocklek."
    parameters = [('d', 'Totalt plattavstånd d [m]', 0.01), ('t_plexi', 'Plexiglastjocklek i blandfallet [m]', 0.009), ('E_air_max', 'Luftens genomslagsfält [V/m]', 3000000.0), ('E_plexi_max', 'Plexiglasets genomslagsfält [V/m]', 20000000.0), ('eps_r', 'Plexiglasets relativa permittivitet εr [-]', 3.0)]

    def validate(self, params):
        if params['d'] <= 0 or params['t_plexi'] < 0 or params['t_plexi'] > params['d']:
            return 'Kräver d > 0 och 0 ≤ t_plexi ≤ d.'
        if params['E_air_max'] <= 0 or params['E_plexi_max'] <= 0 or params['eps_r'] <= 0:
            return 'Genomslagsfält och εr måste vara positiva.'
        return None

    @staticmethod
    def _mixed_case(d, t_plexi, E_air_max, E_plexi_max, eps_r):
        d_air = d - t_plexi
        E_air = min(E_air_max, eps_r * E_plexi_max)
        E_plexi = E_air / eps_r
        Umax = E_air * d_air + E_plexi * t_plexi
        limiting = 'luft' if E_air_max <= eps_r * E_plexi_max else 'plexiglas'
        return (d_air, E_air, E_plexi, Umax, limiting)

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        d = params['d']
        t_plexi = params['t_plexi']
        E_air_max = params['E_air_max']
        E_plexi_max = params['E_plexi_max']
        eps_r = params['eps_r']
        d_air, E_air, E_plexi, U_mixed, limiting = self._mixed_case(d, t_plexi, E_air_max, E_plexi_max, eps_r)
        U_air = E_air_max * d
        U_plexi = E_plexi_max * d
        if mode == 'Field':
            z = np.linspace(0, d, 700)
            field = np.where(z <= t_plexi, E_plexi, E_air)
            ax.plot(z, field)
            if 0 < t_plexi < d:
                ax.axvline(t_plexi, linestyle='--', linewidth=1)
            ax.set_xlabel('z [m]')
            ax.set_ylabel('E [V/m]')
            ax.set_title(f'Blandad stapel vid Umax={U_mixed:.2e} V (begränsad av {limiting})')
            ax.grid(True, alpha=0.3)
        else:
            t = np.linspace(0, d, 300)
            U_curve = np.empty_like(t)
            for i, tt in enumerate(t):
                _, _, _, Uv, _ = self._mixed_case(d, tt, E_air_max, E_plexi_max, eps_r)
                U_curve[i] = Uv
            ax.plot(t, U_curve, label='blandad stapel')
            ax.axhline(U_air, linestyle='--', linewidth=1, label='endast luft')
            ax.axhline(U_plexi, linestyle='--', linewidth=1, label='endast plexiglas')
            ax.axvline(t_plexi, linestyle=':', linewidth=1)
            ax.set_xlabel('Plexiglastjocklek [m]')
            ax.set_ylabel('Umax [V]')
            ax.set_title('Genomslagsbegränsad spänning mot dielektrikets tjocklek')
            ax.legend(fontsize=8)
            ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        d, t_plexi = (params['d'], params['t_plexi'])
        d_air = d - t_plexi
        ax.plot([-0.6, 0.6], [0, 0], linewidth=3)
        ax.plot([-0.6, 0.6], [d, d], linewidth=3)
        if t_plexi > 0:
            ax.add_patch(Rectangle((-0.5, 0), 1.0, t_plexi, fill=True, alpha=0.22))
            ax.text(0, t_plexi / 2, 'plexiglas', ha='center', va='center')
        if d_air > 0:
            ax.add_patch(Rectangle((-0.5, t_plexi), 1.0, d_air, fill=False, linewidth=1.5))
            ax.text(0, t_plexi + d_air / 2, 'luft', ha='center', va='center')
        ax.set_title('Geometriskiss (blandfallet)')
        ax.set_xlim(-0.8, 0.8)
        ax.set_ylim(-0.1 * d, 1.1 * d)
        ax.set_axis_off()

    def draw_3d(self, fig, params, mode):
        fig.clear()
        d = params['d']
        E_air_max = params['E_air_max']
        E_plexi_max = params['E_plexi_max']
        eps_r = params['eps_r']
        t = np.linspace(0, d, 80)
        er = np.linspace(max(1.2, 0.6 * eps_r), max(6.0, 1.8 * eps_r), 80)
        T, ER = np.meshgrid(t, er)
        Eair_lim = np.minimum(E_air_max, ER * E_plexi_max)
        Umax = Eair_lim * (d - T) + Eair_lim / ER * T
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(T, ER, Umax, cmap='viridis', alpha=0.88, rstride=1, cstride=1)
        ax.set_xlabel('plexiglas thickness [m]')
        ax.set_ylabel('εr')
        ax.set_zlabel('Umax [V]')
        ax.set_title('Genomslagsbegränsad designyta')

class DielectricSlabCapacitor(ProblemBase):
    name = '3.14 Plattkondensator med dielektrisk skiva'
    description = 'Plattkondensator med plattavstånd d. En dielektrisk skiva med tjocklek 0,8d ligger mot den undre plattan och resterande 0,2d är luft. Visar styckvis profil för E eller D mot höjd.'
    parameters = [('V0', 'Pålagd spänning V0 [V]', 1000.0), ('d', 'Plattavstånd d [m]', 0.01), ('eps_r', 'Relativ permittivitet εr [-]', 4.0)]

    def validate(self, params):
        if params['d'] <= 0 or params['eps_r'] <= 0:
            return 'd och εr måste vara positiva.'
        return None

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        V0, d, eps_r = (params['V0'], params['d'], params['eps_r'])
        d_diel = 0.8 * d
        E_diel = V0 / ((0.2 * eps_r + 0.8) * d)
        E_air = eps_r * V0 / ((0.2 * eps_r + 0.8) * d)
        D = EPS0 * eps_r * E_diel
        if mode == 'Map':
            x = np.linspace(-0.5, 0.5, 180)
            z = np.linspace(0, d, 220)
            X, Z = np.meshgrid(x, z)
            data = np.where(Z <= d_diel, E_diel, E_air)
            _show_scalar_map(ax, fig, X, Z, data, title='Plattkondensator med dielektrisk skiva: |E|-karta', xlabel='x', ylabel='z [m]', cbar_label='|E| [V/m]', scale='log')
            ax.axhline(d_diel, color='white', linestyle='--', linewidth=0.9)
            return
        z = np.linspace(0, d, 600)
        y = np.where(z <= d_diel, E_diel if mode == 'Field' else D, E_air if mode == 'Field' else D)
        ax.plot(z, y)
        ax.axvline(d_diel, linestyle='--', linewidth=1)
        ax.text(d_diel, ax.get_ylim()[1] * 0.9 if np.max(y) != 0 else 0.1, '  dielektrikum/luft', va='top')
        ax.set_xlabel('z [m] (undre platta vid z=0)')
        ax.set_ylabel('E [V/m]' if mode == 'Field' else 'D [C/m²]')
        ax.set_title('Plattkondensator med dielektrisk skiva')
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        d = params['d']
        d_diel = 0.8 * d
        ax.plot([-0.6, 0.6], [0, 0], linewidth=3)
        ax.plot([-0.6, 0.6], [d, d], linewidth=3)
        ax.add_patch(Rectangle((-0.5, 0), 1.0, d_diel, fill=True, alpha=0.2))
        ax.add_patch(Rectangle((-0.5, d_diel), 1.0, d - d_diel, fill=False, linewidth=1.5))
        ax.text(0, d_diel / 2, 'dielektrikum', ha='center', va='center')
        ax.text(0, d_diel + (d - d_diel) / 2, 'luft', ha='center', va='center')
        ax.set_title('Geometriskiss')
        ax.set_xlim(-0.8, 0.8)
        ax.set_ylim(-0.1 * d, 1.1 * d)
        ax.set_axis_off()

    def draw_3d(self, fig, params, mode):
        """
        Två staplade kuboidlager (dielektrikum blått, luft gult) med
        homogena fältpilar i varje område.
        """
        fig.clear()
        V0, d, eps_r = (params['V0'], params['d'], params['eps_r'])
        d_diel = 0.8 * d
        E_diel = V0 / ((0.2 * eps_r + 0.8) * d)
        E_air = eps_r * V0 / ((0.2 * eps_r + 0.8) * d)
        D = EPS0 * eps_r * E_diel
        W = 1.0
        ax = fig.add_subplot(111, projection='3d')
        _draw_box(ax, -W / 2, W / 2, -W / 2, W / 2, 0, d_diel, 'steelblue', 0.25)
        _draw_box(ax, -W / 2, W / 2, -W / 2, W / 2, d_diel, d, 'lightyellow', 0.25)
        _draw_box(ax, -W / 2, W / 2, -W / 2, W / 2, -d * 0.06, 0, 'grey', 0.6)
        _draw_box(ax, -W / 2, W / 2, -W / 2, W / 2, d, d * 1.06, 'grey', 0.6)
        val_d = E_diel if mode == 'Field' else D
        val_a = E_air if mode == 'Field' else D
        scale = d * 0.35
        for xi in np.linspace(-W / 3, W / 3, 3):
            for yi in np.linspace(-W / 3, W / 3, 3):
                ax.quiver(xi, yi, d_diel * 0.35, 0, 0, scale, color='navy', linewidth=1, arrow_length_ratio=0.35)
                ax.quiver(xi, yi, d_diel + (d - d_diel) * 0.3, 0, 0, scale * 0.6, color='darkred', linewidth=1, arrow_length_ratio=0.35)
        lbl = 'E' if mode == 'Field' else 'D'
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z [m]')
        ax.set_title(f'Dielektrisk skiva 3D\ndiel. {lbl}={val_d:.2e}, luft {lbl}={val_a:.2e}')
        ax.set_xlim(-W / 2, W / 2)
        ax.set_ylim(-W / 2, W / 2)
        ax.set_zlim(-d * 0.1, d * 1.1)

class ElectretCylinderAxis(ProblemBase):
    name = '3.18 Elektretcylinder på axeln'
    description = 'Cylinder med radie a och höjd h med likformig polarisation P längs +z. Visar axiellt E- eller D-fält.'
    parameters = [('P', 'Polarisation P [C/m²]', 1e-08), ('a', 'Cylinderradie a [m]', 0.1), ('h', 'Cylinderhöjd h [m]', 0.05), ('zmin', 'z min [m]', -0.2), ('zmax', 'z max [m]', 0.25)]

    def validate(self, params):
        if params['a'] <= 0 or params['h'] <= 0 or params['zmax'] <= params['zmin']:
            return 'Kräver a > 0, h > 0 och zmax > zmin.'
        return None

    @staticmethod
    def e_field(z, P, a, h):
        root1 = np.sqrt(a ** 2 + z ** 2)
        root2 = np.sqrt(a ** 2 + (z - h) ** 2)
        base = P / (2 * EPS0) * (z / root1 - (z - h) / root2)
        base = np.where((z > 0) & (z < h), base - P / EPS0, base)
        return base

    @staticmethod
    def d_field(z, P, a, h):
        root1 = np.sqrt(a ** 2 + z ** 2)
        root2 = np.sqrt(a ** 2 + (z - h) ** 2)
        return P / 2.0 * (z / root1 - (z - h) / root2)

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        P, a, h = (params['P'], params['a'], params['h'])
        zmin, zmax = (params['zmin'], params['zmax'])
        if mode == 'Map':
            x = np.linspace(-1.4 * a, 1.4 * a, 180)
            z = np.linspace(zmin, zmax, 220)
            X, Z = np.meshgrid(x, z)
            data = np.abs(self.e_field(Z, P, a, h))
            _show_scalar_map(ax, fig, X, Z, data, title='Elektretcylinder: axiellt snitt, |E|-karta', xlabel='x [m]', ylabel='z [m]', cbar_label='|E_z| [V/m]', scale='log', contours=True)
            ax.add_patch(Rectangle((-a, 0), 2 * a, h, fill=False, edgecolor='white', linewidth=1.0))
            return
        z = np.linspace(zmin, zmax, 1200)
        if mode == 'Field':
            y = self.e_field(z, P, a, h)
            ax.set_ylabel('E_z [V/m]')
            ax.set_title('Elektretcylinder: axiell elektrisk fältstyrka')
        else:
            y = self.d_field(z, P, a, h)
            ax.set_ylabel('D_z [C/m²]')
            ax.set_title('Elektretcylinder: axiell elektrisk flödestäthet')
        ax.plot(z, y)
        ax.axvline(0.0, linestyle='--', linewidth=1)
        ax.axvline(h, linestyle='--', linewidth=1)
        ax.set_xlabel('z [m]')
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        a, h = (params['a'], params['h'])
        ax.add_patch(Rectangle((-a, 0), 2 * a, h, fill=False, linewidth=2))
        ax.arrow(0, 0.15 * h, 0, 0.55 * h, width=max(0.015 * a, 1e-06), head_width=0.18 * a, head_length=0.08 * h, length_includes_head=True)
        ax.text(0.15 * a, 0.5 * h, 'P')
        ax.set_title('Geometriskiss')
        ax.set_xlim(-1.4 * a, 1.4 * a)
        ax.set_ylim(-0.15 * h, 1.15 * h)
        ax.set_aspect('equal')
        ax.set_axis_off()

    def draw_3d(self, fig, params, mode):
        """
        3-D-vy: roterar fältprofilen på axeln kring z-axeln som ett
        tunt band, färgsatt efter E_z eller D_z. Elektretcylindern ritas som
        wireframe och fältpilar ovanför/under ändytorna visar fransfältets riktning.
        """
        fig.clear()
        P, a, h = (params['P'], params['a'], params['h'])
        zmin, zmax_p = (params['zmin'], params['zmax'])
        ax = fig.add_subplot(111, projection='3d')
        z = np.linspace(zmin, zmax_p, 200)
        scalar = self.e_field(z, P, a, h) if mode == 'Field' else self.d_field(z, P, a, h)
        zlabel = 'E_z [V/m]' if mode == 'Field' else 'D_z [C/m²]'
        _surface_of_revolution(ax, 0.04 * a * np.ones_like(z), z, scalar, n_phi=60, title='Profil på axeln (roterad)', zlabel='z [m]', cmap='RdBu_r')
        phi = np.linspace(0, 2 * np.pi, 80)
        for zc in [0.0, h]:
            ax.plot(a * np.cos(phi), a * np.sin(phi), np.full_like(phi, zc), color='dimgrey', linewidth=1.2)
        for angle in [0, np.pi / 2, np.pi, 3 * np.pi / 2]:
            ax.plot([a * np.cos(angle), a * np.cos(angle)], [a * np.sin(angle), a * np.sin(angle)], [0.0, h], color='dimgrey', linewidth=1.0)
        Fbot = self.e_field(zmin * 0.5, P, a, h) if mode == 'Field' else self.d_field(zmin * 0.5, P, a, h)
        Ftop = self.e_field(zmax_p * 0.5, P, a, h) if mode == 'Field' else self.d_field(zmax_p * 0.5, P, a, h)
        fscale = 0.25 * (zmax_p - zmin) / (max(abs(Fbot), abs(Ftop), 1e-30) / max(abs(Fbot), abs(Ftop), 1e-30))
        for zp, Fp in [(zmin * 0.55, Fbot), (zmax_p * 0.55, Ftop)]:
            sign = 1 if Fp >= 0 else -1
            ax.quiver(0, 0, zp, 0, 0, sign * 0.18 * (zmax_p - zmin), color='steelblue' if sign > 0 else 'tomato', linewidth=1.8, arrow_length_ratio=0.35)
        ax.set_xlabel('x [m]')
        ax.set_ylabel('y [m]')
        ax.set_zlabel('z [m]')
        ax.set_title(f'Elektretcylinder\npå axeln {zlabel} (roterad)')

class ObliqueConductorDielectricBoundary(ProblemBase):
    name = '3.19 Sned gränsyta ledare–dielektrikum'
    description = 'Plan gränsyta x/a + y/b = 1. Området som innehåller origo är en perfekt ledare; precis utanför är D_n lika med den fria ytladdningstätheten.'
    parameters = [('a', 'x-skärning a [m]', 0.3), ('b', 'y-skärning b [m]', 0.2), ('rho_s', 'Fri ytladdningstäthet ρs [C/m²]', 1e-08), ('eps_r', 'Dielektrikets relativa permittivitet εr', 2.5)]

    def validate(self, params):
        if params['a'] <= 0 or params['b'] <= 0 or params['eps_r'] <= 0:
            return 'a, b och εr måste vara positiva.'
        return None

    @staticmethod
    def normal(a, b):
        n = np.array([1 / a, 1 / b, 0.0], dtype=float)
        return n / np.linalg.norm(n)

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        a, b, rho_s, eps_r = (params['a'], params['b'], params['rho_s'], params['eps_r'])
        n = self.normal(a, b)
        D = rho_s * n
        E = D / (EPS0 * eps_r)
        xs = np.linspace(-0.1 * a, 1.25 * a, 100)
        ys = b * (1 - xs / a)
        ax.plot(xs, ys, linewidth=2, label='gränsyta')
        ax.fill_between(xs, np.minimum(ys, 1.25 * b), 1.25 * b, alpha=0.15, label='dielektrikum')
        p = np.array([0.5 * a, 0.5 * b])
        vec = E[:2] if mode == 'Field' else D[:2]
        scale = max(np.linalg.norm(vec), 1e-30)
        ax.arrow(p[0], p[1], 0.25 * a * vec[0] / scale, 0.25 * a * vec[1] / scale, head_width=0.03 * max(a, b), length_includes_head=True)
        ax.text(p[0], p[1], '  E' if mode == 'Field' else '  D', va='bottom')
        ax.set_aspect('equal')
        ax.set_xlim(-0.1 * a, 1.25 * a)
        ax.set_ylim(-0.1 * b, 1.25 * b)
        ax.set_xlabel('x [m]')
        ax.set_ylabel('y [m]')
        if mode == 'Field':
            ax.set_title(f'E = {np.linalg.norm(E):.3e} n̂ V/m')
        else:
            ax.set_title(f'D = {rho_s:.3e} n̂ C/m²')
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        a, b = (params['a'], params['b'])
        ax.plot([0, a], [b, 0], linewidth=2)
        ax.text(0.1 * a, 0.1 * b, 'ledare', ha='left')
        ax.text(0.8 * a, 0.8 * b, 'dielektrikum', ha='center')
        ax.set_aspect('equal')
        ax.set_xlim(-0.1 * a, 1.2 * a)
        ax.set_ylim(-0.1 * b, 1.2 * b)
        ax.set_title('Tvärsnitt av gränsytan')
        ax.set_axis_off()

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        a, b = (params['a'], params['b'])
        xx = np.linspace(0, a, 2)
        zz = np.linspace(-0.3 * a, 0.3 * a, 2)
        X, Z = np.meshgrid(xx, zz)
        Y = b * (1 - X / a)
        ax.plot_surface(X, Y, Z, alpha=0.35, color='steelblue')
        n = self.normal(a, b)
        p = np.array([0.5 * a, 0.5 * b, 0])
        ax.quiver([p[0]], [p[1]], [p[2]], [n[0]], [n[1]], [n[2]], length=0.25 * max(a, b))
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_title('3-D-gränsyta och utåtriktad normal')
