"""Kapitel 6: Biot-Savarts lag.

Uppgifter i detta kapitel (i menyordning):
    6.1    FiniteWireBiotSavart
    6.2    SquareLoopOnAxis
    6.3    RightAngleWireCorner
    6.5    ThinCurrentStripField
    6.8    CircularArcOnAxis
    6.13   RotatingChargedDisk
"""

from ..core import *


class FiniteWireBiotSavart(ProblemBase):
    name = '6.1 Ändlig rak ledare (Biot-Savart)'
    description = "Rak ledare med halvlängd L och ström I längs z-axeln. Visar den azimutala magnetiska flödestätheten Bφ som funktion av avståndet R för valt z. Det andra läget visar en 2-D-färgkarta av |B| i Rz-planet.\nLäget 'Fält' → Bφ-profil. Läget 'Karta' → 2-D-karta av |B|."
    parameters = [('I', 'Ström I [A]', 10.0), ('L', 'Halvlängd L [m]', 0.5), ('z0', 'Fältpunktens axiella position z [m]', 0.0), ('Rmax', 'Största radiella avstånd Rmax [m]', 0.6)]

    def validate(self, params):
        if params['L'] <= 0 or params['Rmax'] <= 0:
            return 'L och Rmax måste vara positiva.'
        return None

    @staticmethod
    def Bphi(I, L, R, z):
        """Azimutalt B vid cylindriska koordinater (R, z) från ledaren −L..+L på z-axeln.
           Resultat i tesla. Jämför uppgift 6.1a i problemhäftet."""
        R = np.maximum(np.abs(R), 1e-12)
        Lm = L - z
        Lp = L + z
        return MU0 * I / (4 * np.pi * R) * (Lm / np.sqrt(Lm ** 2 + R ** 2) + Lp / np.sqrt(Lp ** 2 + R ** 2))

    def plot(self, fig, params, mode):
        fig.clear()
        I = params['I']
        L = params['L']
        z0 = params['z0']
        Rmax = params['Rmax']
        if mode == 'Field':
            ax = fig.add_subplot(111)
            Rmin = max(0.005 * Rmax, 0.0001)
            R = np.geomspace(Rmin, Rmax, 600)
            B = np.abs(self.Bphi(I, L, R, z0))
            B_inf = MU0 * I / (2 * np.pi * R)
            ax.plot(R * 100.0, B * 1000000.0, label='ändlig ledare')
            ax.plot(R * 100.0, B_inf * 1000000.0, '--', alpha=0.6, label='oändlig ledare')
            ax.set_xscale('log')
            ax.set_yscale('log')
            ax.set_xlabel('R [cm]')
            ax.set_ylabel('|Bφ| [µT]')
            ax.set_title(f'Biot-Savart: |Bφ(R)| vid z = {z0:.2f} m  (L = {L:.2f} m)')
            ax.legend(fontsize=8)
            ax.grid(True, which='both', alpha=0.3)
        else:
            ax = fig.add_subplot(111)
            zg = np.linspace(-1.2 * L, 1.2 * L, 300)
            Rg = np.geomspace(max(0.002 * Rmax, 0.0001), Rmax, 260)
            ZZ, RR = np.meshgrid(zg, Rg)
            BB = np.abs(self.Bphi(I, L, RR, ZZ))
            BB_uT = BB * 1000000.0
            im = ax.pcolormesh(zg * 100.0, Rg * 100.0, BB_uT, cmap='plasma', shading='auto', norm=_positive_lognorm(BB_uT))
            fig.colorbar(im, ax=ax).set_label('|Bφ| [µT]')
            ax.plot([-L * 100.0, L * 100.0], [0, 0], linewidth=3, color='cyan', label='tråd')
            ax.axvline(z0 * 100.0, linestyle=':', linewidth=1, color='lime', label=f'z₀ = {z0:.2f} m')
            ax.set_xlabel('z [cm]')
            ax.set_ylabel('R [cm]')
            ax.set_yscale('log')
            ax.set_title('|Bφ|-färgkarta — Rz-planet')
            ax.legend(fontsize=8)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        L = params['L']
        ax.annotate('', xy=(0, L), xytext=(0, -L), arrowprops=dict(arrowstyle='->', lw=2, color='steelblue'))
        ax.text(0.04, 0, 'I ↑', va='center', fontsize=10, color='steelblue')
        ax.plot([0, 0], [-L, L], color='steelblue', linewidth=3)
        ax.axhline(0, linestyle='--', linewidth=0.8, color='grey')
        ax.text(-0.05, L, '+L', va='bottom', ha='right')
        ax.text(-0.05, -L, '−L', va='top', ha='right')
        z0 = params['z0']
        Rmax = params['Rmax']
        ax.annotate('', xy=(Rmax, z0), xytext=(0, z0), arrowprops=dict(arrowstyle='->', lw=1.5, color='coral'))
        ax.text(Rmax / 2, z0 + L * 0.04, 'R', ha='center', color='coral')
        ax.set_xlim(-0.2, params['Rmax'] * 1.2)
        ax.set_ylim(-1.3 * L, 1.3 * L)
        ax.set_aspect('equal')
        ax.set_axis_off()
        ax.set_title('Geometri')

    def draw_3d(self, fig, params, mode):
        """
        Använder en tydligare 3-D-yta över (z, R)-området i stället för att rotera
        den nära-axeln-singulära profilen. Detta är både snabbare och lättare
        att tolka för den ändliga ledargeometrin.
        """
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        I, L, z0, Rmax = (params['I'], params['L'], params['z0'], params['Rmax'])
        nz, nR = (90, 70)
        zg = np.linspace(-1.2 * L, 1.2 * L, nz)
        Rg = np.geomspace(max(0.002 * Rmax, 0.0001), Rmax, nR)
        ZZ, RR = np.meshgrid(zg, Rg)
        BB = np.abs(self.Bphi(I, L, RR, ZZ)) * 1000000.0
        Bpos = BB[BB > 0]
        Bmin = np.min(Bpos) if Bpos.size else 1.0
        Bmax = np.max(BB) if np.size(BB) else 1.0
        if mode == 'Map':
            norm = _positive_lognorm(BB)
            title = '|Bφ(R,z)|-yta — logaritmisk färgskala'
        else:
            norm = Normalize(vmin=0, vmax=Bmax)
            title = '|Bφ(R,z)|-yta'
        surf = ax.plot_surface(ZZ, RR, BB, cmap='plasma', norm=norm, rstride=1, cstride=1, linewidth=0, antialiased=False, alpha=0.9)
        fig.colorbar(surf, ax=ax, shrink=0.55, pad=0.12).set_label('|Bφ| [µT]')
        ax.plot(np.linspace(-L, L, 80), np.zeros(80), np.zeros(80), color='cyan', linewidth=3, label='tråd')
        ax.plot(np.full(2, z0), [Rg[0], Rg[-1]], [0, 0], color='lime', linewidth=2, linestyle=':', label=f'z₀ = {z0:.2f} m')
        ax.set_xlabel('z [m]')
        ax.set_ylabel('R [m]')
        ax.set_zlabel('|Bφ| [µT]')
        ax.set_title(title)
        ax.legend(fontsize=7)

class SquareLoopOnAxis(ProblemBase):
    name = '6.2 Kvadratisk strömslinga på axeln'
    description = "Kvadratisk strömslinga med sidan a centrerad i origo i xy-planet. Visar axiell magnetisk flödestäthet Bz(z). Läget 'Fält' visar exakt axelformel från uppgift 6.2; läget 'Karta' visar numeriskt beräknad Bz-karta i xz-planet."
    parameters = [('I', 'Ström I [A]', 10.0), ('a', 'Sidlängd a [m]', 0.3), ('zmax', 'Halvt axelintervall zmax [m]', 0.6), ('grid_n', 'Kartans rutnätsstorlek N', 91.0)]

    def validate(self, params):
        if params['I'] == 0:
            return 'I får inte vara noll.'
        if params['a'] <= 0 or params['zmax'] <= 0:
            return 'a och zmax måste vara positiva.'
        if params['grid_n'] < 31:
            return 'Använd rutnätsstorlek N >= 31.'
        return None

    @staticmethod
    def _bz_axis(I, a, z):
        z = np.asarray(z, dtype=float)
        return MU0 * I * a ** 2 / (2 * np.pi * (z ** 2 + a ** 2 / 4) * np.sqrt(z ** 2 + a ** 2 / 2))

    @staticmethod
    def _segment_field(P, r1, r2, I):
        """
        Numeriskt Biot-Savartfält från ett rakt ledarsegment r1->r2,
        utvärderat i en eller flera punkter P[...,3].
        """
        P = np.asarray(P, dtype=float)
        nseg = 140
        t = np.linspace(0.0, 1.0, nseg + 1)
        pts = r1 + (r2 - r1)[None, :] * t[:, None]
        mids = 0.5 * (pts[:-1] + pts[1:])
        dl = np.diff(pts, axis=0)
        R = P[..., None, :] - mids
        Rmag = np.linalg.norm(R, axis=-1)
        with np.errstate(divide='ignore', invalid='ignore'):
            cross = np.cross(dl[None, ...], R, axis=-1)
            contrib = cross / np.maximum(Rmag[..., None] ** 3, 1e-18)
        B = MU0 * I / (4 * np.pi) * np.sum(contrib, axis=-2)
        return B

    @classmethod
    def _field_xz(cls, X, Z, I, a):
        P = np.stack([X, np.zeros_like(X), Z], axis=-1)
        half = a / 2
        corners = np.array([[-half, -half, 0.0], [half, -half, 0.0], [half, half, 0.0], [-half, half, 0.0]])
        B = np.zeros(P.shape, dtype=float)
        for i in range(4):
            r1 = corners[i]
            r2 = corners[(i + 1) % 4]
            B += cls._segment_field(P, r1, r2, I)
        return (B[..., 0], B[..., 1], B[..., 2])

    def plot(self, fig, params, mode):
        fig.clear()
        I, a, zmax = (params['I'], params['a'], params['zmax'])
        if mode == 'Field':
            ax = fig.add_subplot(111)
            z = np.linspace(-zmax, zmax, 1000)
            Bz = self._bz_axis(I, a, z)
            B0 = self._bz_axis(I, a, np.array([0.0]))[0]
            ax.plot(z, Bz)
            ax.scatter([0.0], [B0], color='red', zorder=5)
            ax.axvline(0.0, linestyle=':', color='grey', linewidth=0.9)
            ax.set_xlabel('z [m]')
            ax.set_ylabel('Bz [T]')
            ax.set_title('Kvadratisk slinga: exakt fält på z-axeln')
            ax.text(0.02, 0.98, f'Centrumvärde: B(0) = 2√2 μ₀ I / (π a) = {B0:.3e} T', transform=ax.transAxes, va='top', fontsize=9)
            ax.grid(True, alpha=0.3)
        else:
            ax = fig.add_subplot(111)
            n = int(round(params['grid_n']))
            x = np.linspace(-zmax, zmax, n)
            z = np.linspace(-zmax, zmax, n)
            X, Z = np.meshgrid(x, z)
            _, _, Bz = self._field_xz(X, Z, I, a)
            Bz_uT = Bz * 1000000.0
            im = ax.pcolormesh(X, Z, Bz_uT, cmap='coolwarm', shading='auto', norm=_signed_symlognorm(Bz_uT))
            fig.colorbar(im, ax=ax).set_label('Bz [µT]')
            ax.add_patch(Rectangle((-a / 2, -0.015 * a), a, 0.03 * a, fill=True, alpha=0.35, color='steelblue'))
            ax.set_xlabel('x [m]')
            ax.set_ylabel('z [m]')
            ax.set_title('Kvadratisk slinga: Bz-karta i xz-planet')

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        a = params['a']
        half = a / 2
        ax.plot([-half, half, half, -half, -half], [-half, -half, half, half, -half], linewidth=2)
        ax.plot([0, 0], [-0.8 * a, 0.8 * a], linestyle='--', linewidth=1, color='grey')
        ax.plot([-0.8 * a, 0.8 * a], [0, 0], linestyle=':', linewidth=0.8, color='grey')
        ax.text(0.55 * half, -0.75 * half, 'I', fontsize=10)
        ax.set_aspect('equal')
        ax.set_xlim(-0.9 * a, 0.9 * a)
        ax.set_ylim(-0.9 * a, 0.9 * a)
        ax.set_axis_off()
        ax.set_title('Geometri: kvadratisk slinga i xy-planet')

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        I, a, zmax = (params['I'], params['a'], params['zmax'])
        half = a / 2
        ax.plot([-half, half, half, -half, -half], [-half, -half, half, half, -half], [0, 0, 0, 0, 0], color='firebrick', linewidth=2)
        zpts = np.linspace(-0.9 * zmax, 0.9 * zmax, 9)
        Bz = self._bz_axis(I, a, zpts)
        scale = 0.22 * zmax / max(np.max(np.abs(Bz)), 1e-18)
        for zp, bp in zip(zpts, Bz):
            ax.quiver(0, 0, zp, 0, 0, bp * scale, color='steelblue', linewidth=1.2, arrow_length_ratio=0.25)
        lim = max(zmax, 0.75 * a)
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_zlim(-zmax, zmax)
        ax.set_xlabel('x [m]')
        ax.set_ylabel('y [m]')
        ax.set_zlabel('z [m]')
        ax.set_title('Kvadratisk slinga + axiella B-pilar')

class RightAngleWireCorner(ProblemBase):
    name = '6.3 Ledare böjd i rät vinkel'
    description = "Lång tunn strömförande ledare böjd 90° i horisontalplanet. På höjden h rakt ovanför hörnet pekar fältet längs vinkelbisektrisen. Läget 'Fält' visar |B| mot höjd h; läget 'Karta' visar designytan |B|(I, h)."
    parameters = [('I', 'Ström I [A]', 5.0), ('h', 'Höjd över hörnet h [m]', 0.05), ('hmax', 'Största plottade höjd hmax [m]', 0.2)]

    def validate(self, params):
        if params['I'] == 0:
            return 'I får inte vara noll.'
        if params['h'] <= 0 or params['hmax'] <= 0:
            return 'h och hmax måste vara positiva.'
        if params['hmax'] < params['h']:
            return 'Välj hmax >= h.'
        return None

    @staticmethod
    def _bmag(I, h):
        h = np.asarray(h, dtype=float)
        return MU0 * I / (2 * np.sqrt(2) * np.pi * np.maximum(h, 1e-18))

    def plot(self, fig, params, mode):
        fig.clear()
        I, h0, hmax = (params['I'], params['h'], params['hmax'])
        if mode == 'Field':
            ax = fig.add_subplot(111)
            h = np.linspace(max(0.01 * hmax, 0.0001), hmax, 700)
            B = self._bmag(I, h)
            B0 = self._bmag(I, h0)
            ax.plot(h * 100.0, B * 1000000.0)
            ax.scatter([h0 * 100.0], [B0 * 1000000.0], color='red', zorder=5)
            ax.set_xlabel('Höjd över hörnet h [cm]')
            ax.set_ylabel('|B| [µT]')
            ax.set_title('Rätvinklig ledare: fält ovanför böjen')
            ax.text(0.02, 0.98, f'Riktning: längs vinkelbisektrisen\nValt värde: {B0:.3e} T', transform=ax.transAxes, va='top', fontsize=9)
            ax.grid(True, alpha=0.3)
        else:
            ax = fig.add_subplot(111)
            Ivals = np.linspace(0.2 * abs(I), 3.0 * abs(I), 220)
            hvals = np.linspace(max(0.01 * hmax, 0.0001), hmax, 180)
            II, HH = np.meshgrid(Ivals, hvals)
            BB = self._bmag(II, HH)
            BB_uT = BB * 1000000.0
            im = ax.pcolormesh(Ivals, hvals * 100.0, BB_uT, cmap='viridis', shading='auto', norm=_positive_lognorm(BB_uT))
            fig.colorbar(im, ax=ax).set_label('|B| [µT]')
            ax.scatter([abs(I)], [h0 * 100.0], color='red', s=30)
            ax.set_xlabel('Ström I [A]')
            ax.set_ylabel('Höjd h [cm]')
            ax.set_title('Designkarta: |B|(I, h)')

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        span = max(1.4 * params['h'], 0.08)
        ax.plot([-span, 0], [0, 0], color='sienna', linewidth=3)
        ax.plot([0, 0], [0, span], color='sienna', linewidth=3)
        ax.text(-0.75 * span, 0.08 * span, 'I', color='sienna')
        ax.text(0.06 * span, 0.75 * span, 'I', color='sienna')
        ax.text(0.1 * span, 0.1 * span, 'hörn', fontsize=9)
        ax.set_xlim(-1.1 * span, 1.1 * span)
        ax.set_ylim(-0.6 * span, 1.1 * span)
        ax.set_aspect('equal')
        ax.set_axis_off()
        ax.set_title('Geometri: böjd ledare (ovanifrån)')

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        I, h = (params['I'], params['h'])
        span = max(1.4 * h, 0.08)
        ax.plot([-span, 0], [0, 0], [0, 0], color='sienna', linewidth=3)
        ax.plot([0, 0], [0, span], [0, 0], color='sienna', linewidth=3)
        ax.scatter([0], [0], [h], color='crimson', s=30)
        bmag = self._bmag(I, h)
        vec = np.array([1.0, -1.0, 0.0]) / np.sqrt(2)
        ax.quiver(0, 0, h, *vec * span * 0.45, color='steelblue', linewidth=2, arrow_length_ratio=0.15)
        ax.text(0.35 * span, -0.35 * span, h, f'|B|={bmag:.2e} T', fontsize=8)
        ax.set_xlim(-span, span)
        ax.set_ylim(-span, span)
        ax.set_zlim(0, max(1.5 * h, 0.06))
        ax.set_xlabel('x [m]')
        ax.set_ylabel('y [m]')
        ax.set_zlabel('z [m]')
        ax.set_title('Böjd ledare + fältvektor ovanför hörnet')

class ThinCurrentStripField(ProblemBase):
    name = '6.5 Tunt strömband'
    description = 'Magnetiskt fält från ett långt tunt band med bredd 2a och likformigt fördelad ström I.'
    parameters = [('I', 'Ström I [A]', 10.0), ('a', 'Halvbredd a [m]', 0.02)]

    def validate(self, params):
        if params['a'] <= 0:
            return 'a måste vara positiv.'
        return None

    @staticmethod
    def B_in_plane(I, a, x):
        return MU0 * I / (4 * math.pi * a) * np.log(np.abs((x + a) / (x - a)))

    @staticmethod
    def B_normal_plane(I, a, y):
        return MU0 * I / (2 * math.pi * a) * np.arctan(a / y)

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        I, a = (params['I'], params['a'])
        if mode == 'Map':
            y = np.linspace(0.05 * a, 6 * a, 400)
            B = self.B_normal_plane(I, a, y)
            ax.plot(y / a, B)
            ax.axvline(2, linestyle='--', linewidth=1)
            ax.set_xlabel('avstånd/a')
            ax.set_ylabel('B [T]')
            ax.set_title(f'Perpendicular plane: B(2a) = {self.B_normal_plane(I, a, 2 * a):.3e} T')
        else:
            x = np.linspace(1.05 * a, 6 * a, 400)
            B = self.B_in_plane(I, a, x)
            ax.plot(x / a, B)
            ax.axvline(2, linestyle='--', linewidth=1)
            ax.set_xlabel('avstånd/a')
            ax.set_ylabel('B [T]')
            ax.set_title(f'In strip plane: B(2a) = {self.B_in_plane(I, a, 2 * a):.3e} T')
        ax.grid(True, alpha=0.3)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        a = params['a']
        ax.add_patch(Rectangle((-a, -0.15 * a), 2 * a, 0.3 * a, alpha=0.25))
        ax.arrow(-0.7 * a, 0, 1.4 * a, 0, head_width=0.08 * a, length_includes_head=True)
        ax.text(0, 0.28 * a, 'ström in/ut ur sidan längs bandet', ha='center')
        ax.scatter([2 * a], [0], label='i planet')
        ax.scatter([0], [2 * a], label='normalplan')
        ax.legend(fontsize=7)
        ax.set_aspect('equal')
        ax.set_xlim(-1.4 * a, 2.6 * a)
        ax.set_ylim(-0.5 * a, 2.6 * a)
        ax.set_axis_off()
        ax.set_title('Bandets tvärsnitt')

    def draw_3d(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        I, a = (params['I'], params['a'])
        x = np.linspace(1.05 * a, 5 * a, 60)
        y = np.linspace(0.05 * a, 5 * a, 60)
        X, Y = np.meshgrid(x, y)
        u = np.linspace(-a, a, 300)
        du = u[1] - u[0]
        B = np.zeros_like(X)
        for uu in u:
            R2 = (X - uu) ** 2 + Y ** 2
            B += MU0 * (I / (2 * a)) * du / (2 * math.pi * np.sqrt(R2))
        ax.plot_surface(X / a, Y / a, B, cmap='viridis', alpha=0.9)
        ax.set_xlabel('x/a')
        ax.set_ylabel('y/a')
        ax.set_zlabel('B [T]')
        ax.set_title('Fältbelopp nära bandet')

class CircularArcOnAxis(ProblemBase):
    name = '6.8 Cirkulär strömbåge på axeln'
    description = 'Magnetisk flödestäthet på z-axeln från en strömförande cirkelbåge i xy-planet. Använder kvartscirkelresultatet från 6.8(a) och kan även visa helcirkelresultatet från 6.8(b).'
    parameters = [('I', 'Ström I [A]', 10.0), ('a', 'Bågradie a [m]', 0.15), ('zmax', 'Halvt axelintervall zmax [m]', 0.5), ('loop', '1=kvartsbåge, 2=hel slinga', 1.0)]

    def validate(self, params):
        if params['a'] <= 0 or params['zmax'] <= 0:
            return 'a och zmax måste vara positiva.'
        if round(params['loop']) not in (1, 2):
            return 'slingvärdet måste vara 1 (kvartsbåge) eller 2 (hel slinga).'
        return None

    @staticmethod
    def _quarter_components(I, a, z):
        coeff = MU0 * I / (4 * np.pi) * a / np.power(a ** 2 + z ** 2, 1.5)
        Bx = coeff * z
        By = coeff * z
        Bz = coeff * (a * np.pi / 2)
        return (Bx, By, Bz)

    @staticmethod
    def _full_loop_Bz(I, a, z):
        return MU0 * I * a ** 2 / (2 * np.power(a ** 2 + z ** 2, 1.5))

    def plot(self, fig, params, mode):
        fig.clear()
        ax = fig.add_subplot(111)
        I, a, zmax = (params['I'], params['a'], params['zmax'])
        loop = int(round(params['loop']))
        z = np.linspace(-zmax, zmax, 1000)
        if loop == 1:
            Bx, By, Bz = self._quarter_components(I, a, z)
            if mode == 'Field':
                ax.plot(z, Bx, label='Bx')
                ax.plot(z, By, label='By')
                ax.plot(z, Bz, label='Bz')
                ax.set_ylabel('B components [T]')
                ax.set_title('Kvartscirkelbåge: fältkomponenter på z-axeln')
            else:
                Bmag = np.sqrt(Bx ** 2 + By ** 2 + Bz ** 2)
                ax.plot(z, Bmag)
                ax.set_ylabel('|B| [T]')
                ax.set_title('Kvartscirkelbåge: |B| på z-axeln')
        else:
            Bz = self._full_loop_Bz(I, a, z)
            ax.plot(z, Bz)
            ax.set_ylabel('B_z [T]')
            ax.set_title('Hel cirkelslinga: axiellt fält')
        ax.set_xlabel('z [m]')
        ax.grid(True, alpha=0.3)
        if loop == 1 and mode == 'Field':
            ax.legend(fontsize=8)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        a = params['a']
        loop = int(round(params['loop']))
        if loop == 1:
            t = np.linspace(0, np.pi / 2, 160)
            ax.plot(a * np.cos(t), a * np.sin(t), linewidth=2)
            ax.plot([a, 1.35 * a], [0, 0], linewidth=2)
            ax.plot([0, 0], [a, 1.35 * a], linewidth=2)
            ax.text(0.75 * a, 0.12 * a, 'I', fontsize=10)
            ax.text(0.1 * a, 0.82 * a, 'I', fontsize=10)
            ax.set_title('Kvartsbåge + tangentiella ledare')
        else:
            t = np.linspace(0, 2 * np.pi, 220)
            ax.plot(a * np.cos(t), a * np.sin(t), linewidth=2)
            ax.set_title('Hel cirkelslinga')
        ax.set_aspect('equal')
        ax.set_xlim(-1.5 * a, 1.5 * a)
        ax.set_ylim(-1.5 * a, 1.5 * a)
        ax.set_axis_off()

    def draw_3d(self, fig, params, mode):
        """
        3-D-vy: ritar strömgeometrin (kvartsbåge + anslutande ledare, eller hel slinga)
        i xy-planet och visar B-fältpilar längs z-axeln.
        För hel slinga är fältet rent axiellt (Bz); för kvartsbågen visas
        alla tre komponenter som separata färgpilar.
        """
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        I, a, zmax = (params['I'], params['a'], params['zmax'])
        loop = int(round(params['loop']))
        z = np.linspace(-zmax, zmax, 200)
        if loop == 2:
            t = np.linspace(0, 2 * np.pi, 240)
            ax.plot(a * np.cos(t), a * np.sin(t), np.zeros(240), color='firebrick', linewidth=2.5, label='slinga (I)')
            Bz = self._full_loop_Bz(I, a, z)
            Bpeak = np.max(np.abs(Bz))
            scale = 0.3 * zmax / max(Bpeak, 1e-30)
            z_pts = np.linspace(-zmax * 0.85, zmax * 0.85, 10)
            Bz_pts = self._full_loop_Bz(I, a, z_pts)
            for zp, Bp in zip(z_pts, Bz_pts):
                col = 'steelblue' if Bp >= 0 else 'tomato'
                ax.quiver(0, 0, zp, 0, 0, Bp * scale, color=col, linewidth=1.5, arrow_length_ratio=0.3)
            ax.plot([0, 0], [0, 0], [-zmax, zmax], color='grey', linewidth=0.8, linestyle=':')
            ax.set_title('Hel slinga: Bz(z)-pilar på axeln')
        else:
            t = np.linspace(0, np.pi / 2, 120)
            ax.plot(a * np.cos(t), a * np.sin(t), np.zeros(120), color='firebrick', linewidth=2.5, label='båge (I)')
            lead = 0.45 * a
            ax.plot([a, a + lead], [0, 0], [0, 0], color='firebrick', linewidth=2.0)
            ax.plot([0, 0], [a, a + lead], [0, 0], color='firebrick', linewidth=2.0)
            z_pts = np.linspace(-zmax * 0.85, zmax * 0.85, 9)
            Bx_pts, By_pts, Bz_pts = self._quarter_components(I, a, z_pts)
            Bpeak = max(np.max(np.abs(Bx_pts)), np.max(np.abs(By_pts)), np.max(np.abs(Bz_pts)), 1e-30)
            scale = 0.25 * zmax / Bpeak
            for zp, bx, by, bz in zip(z_pts, Bx_pts, By_pts, Bz_pts):
                ax.quiver(0, 0, zp, bx * scale, 0, 0, color='tomato', linewidth=1.2, arrow_length_ratio=0.3)
                ax.quiver(0, 0, zp, 0, by * scale, 0, color='darkorange', linewidth=1.2, arrow_length_ratio=0.3)
                ax.quiver(0, 0, zp, 0, 0, bz * scale, color='steelblue', linewidth=1.2, arrow_length_ratio=0.3)
            proxies = [Line2D([0], [0], color='tomato', linewidth=2, label='Bx'), Line2D([0], [0], color='darkorange', linewidth=2, label='By'), Line2D([0], [0], color='steelblue', linewidth=2, label='Bz'), Line2D([0], [0], color='firebrick', linewidth=2, label='båge (I)')]
            ax.legend(handles=proxies, fontsize=7, loc='upper right')
            ax.plot([0, 0], [0, 0], [-zmax, zmax], color='grey', linewidth=0.8, linestyle=':')
            ax.set_title('Kvartsbåge: B-komponenter på z-axeln')
        ax.set_xlabel('x [m]')
        ax.set_ylabel('y [m]')
        ax.set_zlabel('z [m]')
        ax.set_xlim(-1.1 * a, 1.1 * a)
        ax.set_ylim(-1.1 * a, 1.1 * a)
        ax.set_zlim(-zmax, zmax)

class RotatingChargedDisk(ProblemBase):
    name = '6.13 Roterande laddad skiva'
    description = "Isolerande skiva med radie a och likformig ytladdningstäthet ρs som roterar med vinkelhastighet ω kring sin axel. Varje ringelement motsvarar en cirkulär strömslinga; totalt axiellt B fås genom integration över ringarna.\nLäget 'Fält' → B_z(z) på axeln. Läget 'Karta' → 2-D-färgkarta Bz mot (R, z)."
    parameters = [('rho_s', 'Ytladdningstäthet ρs [C/m²]', 0.0005), ('a', 'Skivradie a [m]', 0.15), ('omega', 'Vinkelhastighet ω [rad/s]', 500.0), ('zmax', 'Halvt axelintervall zmax [m]', 0.4)]

    def validate(self, params):
        if params['a'] <= 0 or params['zmax'] <= 0 or params['omega'] <= 0:
            return 'a, omega och zmax måste vara positiva.'
        return None

    @staticmethod
    def _Bz_axis(rho_s, omega, a, z_arr, n_rings=400):
        """
        Integrerar Biot-Savarts lag över ringelement.
        Varje ring med radie r har ström dI = ρs * ω * r * dr / (2π) × 2π = ρs ω r dr.
        B_z från en ring på höjden z över ringen: µ0 dI r² / (2(r²+z²)^{3/2}).
        """
        r_rings = np.linspace(1e-06 * a, a, n_rings)
        dr = r_rings[1] - r_rings[0]
        dI = rho_s * omega * r_rings * dr
        z_arr = np.asarray(z_arr)
        z2D = z_arr[:, None]
        r2D = r_rings[None, :]
        dB = MU0 / 2.0 * dI * r2D ** 2 / np.power(r2D ** 2 + z2D ** 2, 1.5)
        return dB.sum(axis=1)

    @staticmethod
    def _analytic_Bz(rho_s, omega, a, z):
        """
        Slutet uttryck från facit till uppgift 6.13:
        B_z = (µ0 ρs ω / 2) * ( (a² + 2z²)/√(a²+z²) − 2|z| )
        """
        z = np.asarray(z, dtype=float)
        root = np.sqrt(a ** 2 + z ** 2)
        return MU0 * rho_s * omega / 2.0 * ((a ** 2 + 2 * z ** 2) / root - 2 * np.abs(z))

    @staticmethod
    def _Bz_offaxis(rho_s, omega, a, R_arr, z_arr, n_rings=200):
        """
        Beräknar Bz i godtycklig punkt (R, z) genom att integrera Biot-Savart
        över ringelement. Varje ring med skivradie r har ström
        dI = rho_s * omega * r * dr och bidrar i fältpunkten (R, z) med:
            dBz = (mu0 * dI / (4*pi)) * integral_0^{2pi}
                    (r - R*cos(phi)) / (r^2 + R^2 - 2rR cos(phi) + z^2)^{3/2} r dphi
        Beräkningen görs här approximativt med tät phi-kvadratur.
        R_arr och z_arr är 2-D-arrayer med samma form (meshgrid).
        Returnerar en Bz-array med samma form.
        """
        r_rings = np.linspace(1e-06 * a, a, n_rings)
        dr = r_rings[1] - r_rings[0]
        dI = rho_s * omega * r_rings * dr
        n_phi = 60
        phi = np.linspace(0, 2 * np.pi, n_phi, endpoint=False)
        dphi = 2 * np.pi / n_phi
        R4 = R_arr[:, :, np.newaxis, np.newaxis]
        Z4 = z_arr[:, :, np.newaxis, np.newaxis]
        r4 = r_rings[np.newaxis, np.newaxis, :, np.newaxis]
        p4 = phi[np.newaxis, np.newaxis, np.newaxis, :]
        dI4 = dI[np.newaxis, np.newaxis, :, np.newaxis]
        dist2 = r4 ** 2 + R4 ** 2 - 2 * r4 * R4 * np.cos(p4) + Z4 ** 2
        dist3 = np.power(np.maximum(dist2, 1e-30), 1.5)
        integrand = (r4 - R4 * np.cos(p4)) / dist3
        Bz = MU0 / (4 * np.pi) * np.sum(dI4 * r4 * integrand * dphi, axis=(2, 3))
        return Bz

    def plot(self, fig, params, mode):
        fig.clear()
        rho_s = params['rho_s']
        a = params['a']
        omega = params['omega']
        zmax = params['zmax']
        if mode == 'Field':
            ax = fig.add_subplot(111)
            z = np.linspace(-zmax, zmax, 600)
            Bz_num = self._Bz_axis(rho_s, omega, a, z)
            Bz_ana = self._analytic_Bz(rho_s, omega, a, z)
            ax.plot(z * 100.0, Bz_num * 1000000.0, label='numeriskt (ringar)')
            ax.plot(z * 100.0, Bz_ana * 1000000.0, '--', alpha=0.6, label='analytiskt (facit)')
            ax.axvline(0, linestyle=':', linewidth=0.9, color='grey')
            ax.set_xlabel('z [cm]')
            ax.set_ylabel('Bz [µT]')
            ax.set_title('Roterande laddad skiva: axiellt B-fält')
            ax.legend(fontsize=8)
            ax.grid(True, alpha=0.3)
        else:
            ax = fig.add_subplot(111)
            nR, nZ = (55, 80)
            Rg = np.linspace(0, 1.5 * a, nR)
            Zg = np.linspace(-zmax, zmax, nZ)
            ZZ, RR = np.meshgrid(Zg, Rg)
            Bmap = self._Bz_offaxis(rho_s, omega, a, RR, ZZ, n_rings=150)
            Bmap_uT = np.abs(Bmap) * 1000000.0
            im = ax.pcolormesh(Zg * 100.0, Rg * 100.0, Bmap_uT, cmap='magma', shading='auto', norm=_positive_lognorm(Bmap_uT))
            fig.colorbar(im, ax=ax).set_label('|Bz| [µT] (Biot-Savart)')
            ax.axvline(0, color='cyan', linewidth=2, label='skivplan')
            ax.axhline(a * 100.0, color='white', linewidth=1, linestyle='--', label=f'r = a = {a * 100.0:.1f} cm')
            ax.set_xlabel('z [cm]')
            ax.set_ylabel('R [cm]')
            ax.set_title('|Bz|-färgkarta utanför axeln (Biot-Savart-integration)')
            ax.legend(fontsize=8)

    def draw_geometry(self, fig, params):
        fig.clear()
        ax = fig.add_subplot(111)
        a = params['a']
        disk = Ellipse((0, 0), 2 * a, 0.45 * a, fill=True, facecolor='steelblue', alpha=0.35, edgecolor='steelblue', linewidth=2)
        ax.add_patch(disk)
        theta = np.linspace(0.15 * np.pi, 0.85 * np.pi, 60)
        ax.plot(a * 0.6 * np.cos(theta), a * 0.22 * np.sin(theta), color='darkorange', linewidth=2)
        ax.annotate('ω', xy=(a * 0.6 * np.cos(0.85 * np.pi), a * 0.22 * np.sin(0.85 * np.pi)), fontsize=12, color='darkorange', xytext=(-a * 0.7, a * 0.18), ha='center')
        ax.annotate('', xy=(0, a), xytext=(0, -a * 0.3), arrowprops=dict(arrowstyle='->', lw=1.5, color='grey'))
        ax.text(0.04 * a, a * 0.85, 'z-axel', fontsize=9, color='grey')
        ax.set_xlim(-1.2 * a, 1.2 * a)
        ax.set_ylim(-0.5 * a, 1.2 * a)
        ax.set_aspect('equal')
        ax.set_axis_off()
        ax.set_title('Geometri')

    def draw_3d(self, fig, params, mode):
        """
        3-D-vy: skivan visas som en plan färgyta färgsatt efter
        effektiv strömtäthet (ρs·ω·r), plus axiella B-pilar.
        """
        fig.clear()
        ax = fig.add_subplot(111, projection='3d')
        rho_s = params['rho_s']
        a = params['a']
        omega = params['omega']
        zmax = params['zmax']
        r1d = np.linspace(0, a, 50)
        phi1d = np.linspace(0, 2 * np.pi, 60)
        R2D, PHI2D = np.meshgrid(r1d, phi1d)
        Xd = R2D * np.cos(PHI2D)
        Yd = R2D * np.sin(PHI2D)
        Zd = np.zeros_like(Xd)
        Js = rho_s * omega * R2D
        norm_Js = Normalize(vmin=0, vmax=np.max(Js))
        fc = colormaps['YlOrRd'](norm_Js(Js))
        ax.plot_surface(Xd, Yd, Zd, facecolors=fc, rstride=1, cstride=1, antialiased=False, shade=False, alpha=0.85)
        sm = ScalarMappable(cmap='YlOrRd', norm=norm_Js)
        sm.set_array([])
        fig.colorbar(sm, ax=ax, shrink=0.45, pad=0.1).set_label('Js [A/m]')
        z_pts = np.linspace(-zmax * 0.85, zmax * 0.85, 8)
        Bz_pts = self._analytic_Bz(rho_s, omega, a, z_pts)
        B_scale = zmax * 0.25 / max(np.max(np.abs(Bz_pts)), 1e-30)
        for zp, Bp in zip(z_pts, Bz_pts):
            ax.quiver(0, 0, zp, 0, 0, Bp * B_scale, color='steelblue', linewidth=1.5, arrow_length_ratio=0.3)
        ax.set_xlabel('x [m]')
        ax.set_ylabel('y [m]')
        ax.set_zlabel('z [m]')
        ax.set_title('Roterande skiva: ytström (färg)\n+ axiella B-pilar')
        ax.set_zlim(-zmax, zmax)
