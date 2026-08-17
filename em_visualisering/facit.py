"""Slutresultat från den tryckta problemsamlingens facit.

Detta är avsiktligt ett facit, inte en fullständig lösningssamling. Formuleringarna
följer problemsamlingens slutresultat för de uppgifter som är registrerade i appen.
"""

from __future__ import annotations

from .study_content import problem_id_from_name


FACIT_BY_ID: dict[str, str] = {
    # ------------------------------------------------------------------
    # Kapitel 2
    # ------------------------------------------------------------------
    "2.1": r"""
$$
\alpha=\left(\frac{Q^2}{2\pi\varepsilon_0mg\ell^2}\right)^{1/3}.
$$
""",
    "2.2": r"""
$$
\mathbf E=
\frac{Q}{4\pi\varepsilon_0}
\frac{z}{(z^2+a^2)^{3/2}}\,\hat{\mathbf z}.
$$
""",
    "2.3": r"""
**(a)**
$$
\mathbf E=\frac{\rho_\ell}{4\pi\varepsilon_0}
\left\{
\frac{1}{x}\left[
\frac{a}{\sqrt{a^2+x^2}}+
\frac{b}{\sqrt{b^2+x^2}}
\right]\hat{\mathbf x}
+
\left[
\frac{1}{\sqrt{a^2+x^2}}-
\frac{1}{\sqrt{b^2+x^2}}
\right]\hat{\mathbf z}
\right\}.
$$

**(b)**
$$
\mathbf E=\frac{\rho_\ell}{2\pi x\varepsilon_0}\,\hat{\mathbf x}.
$$
""",
    "2.4": r"""
$$
\mathbf E=\frac{\rho_s}{2\varepsilon_0}
\left\{
-\frac{1}{\pi}
\left[
\ln\left|
\frac{\sqrt{a^2+z^2}+a}{z}
\right|
-\frac{a}{\sqrt{a^2+z^2}}
\right]\hat{\mathbf y}
+
\frac12\left[
\frac{z}{|z|}-\frac{z}{\sqrt{a^2+z^2}}
\right]\hat{\mathbf z}
\right\}.
$$

$x$-komponenten är noll.
""",
    "2.5": r"""
$$
V(r)=
\begin{cases}
\dfrac{Q}{4\pi\varepsilon_0a}, & r\le a,\\[6pt]
\dfrac{Q}{4\pi\varepsilon_0r}, & r>a.
\end{cases}
$$
""",
    "2.6": r"""
$$
\mathbf E=
\begin{cases}
0, & R<a,\\[4pt]
\dfrac{\rho_{sa}a}{\varepsilon_0R}\,\hat{\mathbf R}, & a<R<b,\\[8pt]
\dfrac{\rho_{sa}a+\rho_{sb}b}{\varepsilon_0R}\,\hat{\mathbf R}, & R>b.
\end{cases}
$$
""",
    "2.7": r"""
$$
a=\frac b2=0.50\ \mathrm{m},
\qquad
V_{\max}=\frac{bE_{\max}}4=5.0\times10^5\ \mathrm{V}.
$$
""",
    "2.8": r"""
**(a)**
$$
V(r)=\frac{1}{4\pi\varepsilon_0}
\begin{cases}
\dfrac{Q_a}{a}+\dfrac{Q_b}{b}, & r\le a,\\[7pt]
\dfrac{Q_a}{r}+\dfrac{Q_b}{b}, & a\le r\le b,\\[7pt]
\dfrac{Q_a+Q_b}{r}, & r\ge b.
\end{cases}
$$

**(b)** Efter den ledande förbindelsen ligger all laddning på det yttre skalet.
""",
    "2.9": r"""
$$
\langle\rho\rangle=1.8\times10^{-12}\ \mathrm{C/m^3}.
$$

Facit anger Gauss sats som metod.
""",
    "2.10": r"""
$$
\mathbf E=
\frac{\rho}{3\varepsilon_0}
\left[
\frac{b^3}{x^2}
-
\frac{a^3}{(x+d)^2}
\right]\hat{\mathbf x}.
$$
""",
    "2.11": r"""
$$
|\mathbf E|=
\frac{2}{a+b}\,
\frac{U}{\ln(b/a)}.
$$
""",
    "2.12": r"""
**(a)**
$$
Q_{\max}=4\pi\varepsilon_0a^2E_{\max},
\qquad
V_{\max}=aE_{\max}.
$$

**(b)**
$$
Q_{\max}=0.33\times10^{-5}\ \mathrm C,
\qquad
V_{\max}=3\times10^5\ \mathrm V.
$$
""",
    "2.13": r"""
$$
Q=
-\frac{
4\pi\varepsilon_0(b^2-a^2)\ell U
}{
(b^2-a^2)-2a^2\ln(b/a)
}
=-1.6\times10^{-9}\ \mathrm C.
$$
""",
    "2.16": r"""
$$
V(0)=\frac{Aa^3}{6\varepsilon_0}.
$$
""",
    "2.18": r"""
**(a)**
$$
Q=\frac{\varepsilon_0AU}{d_0}=8.9\times10^{-9}\ \mathrm C.
$$

**(b)**
$$
U'=\frac{d_0-d_1}{d_0}U=80\ \mathrm V.
$$

**(c)**
$$
U''=\frac{d_2}{d_0}U=600\ \mathrm V.
$$
""",
    "2.19": r"""
**(a)**
$$
x=\frac d2-\frac{\varepsilon_0V_0}{\rho_0d},
$$
där $x$ är avståndet från plattan med potential $V_0$.

**(b)**
$$
|V_0|\le \frac{\rho_0d^2}{2\varepsilon_0}.
$$
""",

    # ------------------------------------------------------------------
    # Kapitel 3
    # ------------------------------------------------------------------
    "3.1": r"""
Längs $z$-axeln respektive $y$-axeln:
$$
6.2\times10^7\ \mathrm{V/m},
\qquad
3.1\times10^7\ \mathrm{V/m}.
$$

För $r_0\gg d$ anges approximationerna
$$
\frac{ed}{2\pi\varepsilon_0r_0^3},
\qquad
\frac{ed}{4\pi\varepsilon_0r_0^3},
$$
där $e$ är elementarladdningen.
""",
    "3.3": r"""
$$
E_p=0.29\times10^6\ \mathrm{V/m},
\qquad
E_\ell=1.7\times10^6\ \mathrm{V/m},
$$
$$
D_p=D_\ell=1.5\times10^{-5}\ \mathrm{C/m^2}.
$$
""",
    "3.6": r"""
$$
\frac{Q_{\mathrm{utsida}}}{Q_{\mathrm{insida}}}=0.8.
$$
""",
    "3.7": r"""
För $r>b$:
$$
\mathbf E(r)=\frac{\rho_0(b^3-a^3)}{3\varepsilon_0r^2}\hat{\mathbf r},
\qquad
V(r)=\frac{\rho_0(b^3-a^3)}{3\varepsilon_0r}.
$$

För $a<r<b$:
$$
\mathbf E(r)=
\frac{\rho_0(r^3-a^3)}{3\varepsilon_0\varepsilon_rr^2}\hat{\mathbf r},
$$
$$
V(r)=\frac{\rho_0}{3\varepsilon_0\varepsilon_r}
\left[
b^2\left(\varepsilon_r+\frac12\right)
+\frac{a^3}{b}(1-\varepsilon_r)
-\frac{r^2}{2}
-\frac{a^3}{r}
\right].
$$

För $0\le r<a$:
$$
\mathbf E=0,
$$
$$
V(r)=\frac{\rho_0}{3\varepsilon_0\varepsilon_r}
\left[
b^2\left(\varepsilon_r+\frac12\right)
+\frac{a^3}{b}(1-\varepsilon_r)
-\frac32a^2
\right].
$$
""",
    "3.9": r"""
$$
\mathbf E=
\frac{Q}{2\pi\varepsilon_0(\varepsilon_1+\varepsilon_2)}
\frac{\hat{\mathbf r}}{r^2}.
$$

I den högra halvan:
$$
\mathbf D=
\frac{\varepsilon_1}{\varepsilon_1+\varepsilon_2}
\frac{Q\hat{\mathbf r}}{2\pi r^2}.
$$

I den vänstra halvan:
$$
\mathbf D=
\frac{\varepsilon_2}{\varepsilon_1+\varepsilon_2}
\frac{Q\hat{\mathbf r}}{2\pi r^2}.
$$
""",
    "3.11": r"""
**(a)** Tre skikt makrofol krävs.

**(b)** Arean måste vara
$$
11\ \mathrm{cm^2}.
$$
""",
    "3.12": r"""
Med $b=(a+c)/2$:
$$
\frac CL=
2\pi\varepsilon_0
\left[
\frac1{\varepsilon_1}\ln\left(\frac ba\right)
+
\frac1{\varepsilon_2}\ln\left(\frac cb\right)
\right]^{-1}
=0.21\ \mathrm{nF/m}.
$$
""",
    "3.13": r"""
**(a)** $30\ \mathrm{kV}$

**(b)** $200\ \mathrm{kV}$

**(c)** $12\ \mathrm{kV}$
""",
    "3.14": r"""
**(a)**
$$
E_{\mathrm{diel}}=
\frac{V_0}{(0.2\varepsilon_r+0.8)d},
\qquad
E_{\mathrm{luft}}=
\frac{\varepsilon_rV_0}{(0.2\varepsilon_r+0.8)d},
$$
$$
D_{\mathrm{diel}}=D_{\mathrm{luft}}=
\frac{\varepsilon_0\varepsilon_rV_0}{(0.2\varepsilon_r+0.8)d}.
$$

**(b)**
$$
\rho_s=
\pm\frac{\varepsilon_0\varepsilon_rV_0}{(0.2\varepsilon_r+0.8)d},
$$
med positivt tecken på den övre plattan.

**(c)**
$$
\rho_{sp}=
\mp\frac{\varepsilon_0(\varepsilon_r-1)V_0}{(0.2\varepsilon_r+0.8)d},
$$
med negativt tecken på dielektrikumets övre yta.
""",
    "3.18": r"""
**(a)** För $z<0$ och $z>h$:
$$
\mathbf E=
\frac{P}{2\varepsilon_0}
\left[
\frac{z}{\sqrt{a^2+z^2}}
-
\frac{z-h}{\sqrt{a^2+(z-h)^2}}
\right]\hat{\mathbf z}.
$$
För $0<z<h$:
$$
\mathbf E=
\frac{P}{2\varepsilon_0}
\left[
-2+
\frac{z}{\sqrt{a^2+z^2}}
-
\frac{z-h}{\sqrt{a^2+(z-h)^2}}
\right]\hat{\mathbf z}.
$$

**(b)** För alla $z$:
$$
\mathbf D=
\frac{P}{2}
\left[
\frac{z}{\sqrt{a^2+z^2}}
-
\frac{z-h}{\sqrt{a^2+(z-h)^2}}
\right]\hat{\mathbf z}.
$$
$D$ är kontinuerligt.

**(c)** När $a\gg h$:
$$
\mathbf E=-\frac{P}{\varepsilon_0}\hat{\mathbf z},
\qquad
\mathbf D=0
\quad (0<z<h),
$$
och utanför är $E=D=0$.

**(d)** För fria ytladdningar blir
$$
\mathbf D=-P\hat{\mathbf z}
\quad (0<z<h).
$$
För övrigt är $E$ och $D$ som för elektreten.
""",
    "3.19": r"""
$$
\mathbf D=
\rho_s\,
\frac{b\hat{\mathbf x}+a\hat{\mathbf y}}{\sqrt{a^2+b^2}},
\qquad
\mathbf E=\frac{\mathbf D}{\varepsilon_0\varepsilon_r}.
$$
""",

    # ------------------------------------------------------------------
    # Kapitel 4
    # ------------------------------------------------------------------
    "4.1": r"""
$$
W=\frac{Q^2}{8\pi\varepsilon_0a}.
$$
""",
    "4.2": r"""
$$
d=
V\sqrt{\frac{\varepsilon_0A}{2F}}
=0.3\ \mathrm{mm}.
$$
""",
    "4.3": r"""
$$
U=
\frac{d}{\varepsilon_r}
\sqrt{\frac{2t\rho_{\mathrm{Cu}}g}{\varepsilon_0}}
=5.6\ \mathrm{kV}.
$$
""",
    "4.5": r"""
**(a)**
$$
Q=18\ \mathrm C.
$$

**(b)**
$$
W_e=3.5\times10^9\ \mathrm J.
$$
""",
    "4.6": r"""
$$
F=
\frac{\pi\varepsilon_0V_0^2}{\ln(b/a)}(\varepsilon_r-1)
=3.8\times10^{-4}\ \mathrm N.
$$
""",
    "4.7": r"""
**(a)**
$$
Q(b)=-q\left(1-\frac ab\right).
$$

**(b)**
$$
Q_{\mathrm{tot}}=-q.
$$

**(c)**
$$
F=\frac{q^2}{16\pi\varepsilon_0a^2},
$$
riktad rakt ned mot planet.
""",

    # ------------------------------------------------------------------
    # Kapitel 5
    # ------------------------------------------------------------------
    "5.1": r"""
$$
I=\frac{2\pi\sigma\ell U}{\ln(b/a)}.
$$
""",
    "5.2": r"""
**(a)**
$$
I=\frac{2\pi V\ell}{\rho\ln(b/a)}
=0.16\ \mathrm{mA}.
$$

**(b)**
$$
P=\frac{2\pi V^2\ell}{\rho\ln(b/a)}
=20\ \mathrm{mW}.
$$
""",
    "5.7": r"""
**(a)**
$$
R=\frac{b^2-a^2}{4\pi k\ell}.
$$

**(b)**
$$
\rho=
\frac{4\varepsilon_0\varepsilon_rU}{b^2-a^2}.
$$

Tecknet på laddningstätheten beror på hur $U$ definieras.
""",
    "5.10": r"""
$$
R=\frac{\pi}{\sigma h\ln(b/a)}.
$$
""",
    "5.15": r"""
**(a)**
$$
\rho_s=
\alpha\varepsilon_0
\left(
\frac{\varepsilon_2}{\sigma_2}
-
\frac{\varepsilon_1}{\sigma_1}
\right).
$$

**(b)** Ingen fri ytladdning fås om
$$
\frac{\sigma_2}{\varepsilon_2}
=
\frac{\sigma_1}{\varepsilon_1}.
$$
""",

    # ------------------------------------------------------------------
    # Kapitel 6
    # ------------------------------------------------------------------
    "6.1": r"""
**(a)**
$$
\mathbf B=
\frac{\mu_0I}{4\pi R}
\left[
\frac{L-z}{\sqrt{(L-z)^2+R^2}}
+
\frac{L+z}{\sqrt{(L+z)^2+R^2}}
\right]\hat{\boldsymbol\phi}.
$$
När $L\to\infty$:
$$
\mathbf B\to
\frac{\mu_0I}{2\pi R}\hat{\boldsymbol\phi}.
$$

**(b)** För $z=0$:
$$
\mathbf B=
\frac{\mu_0I}{2\pi R}
\frac{L}{\sqrt{L^2+R^2}}
\hat{\boldsymbol\phi}.
$$

**(c)**
$$
\mathbf B=
\frac{\mu_0I}{2\pi R}\hat{\boldsymbol\phi}.
$$
""",
    "6.2": r"""
**(a)**
$$
\mathbf B=
\frac{\mu_0Ia^2}
{2\pi\left(z^2+a^2/4\right)\sqrt{z^2+a^2/2}}
\,\hat{\mathbf z}.
$$

**(b)**
$$
B(0)=\frac{2\sqrt2\,\mu_0I}{\pi a}
=3.8\times10^{-6}\ \mathrm{T}.
$$
""",
    "6.3": r"""
$$
B=1.4\times10^{-5}\ \mathrm T,
$$
riktad längs bisektrisen till den räta vinkeln.
""",
    "6.5": r"""
**(a)**
$$
B=\frac{\mu_0I}{4\pi a}\ln 3.
$$

**(b)**
$$
B=\frac{\mu_0I}{2\pi a}\arctan\left(\frac12\right).
$$
""",
    "6.8": r"""
**(a)**
$$
\mathbf B=
\frac{\mu_0I}{4\pi}
\frac{a}{(a^2+z^2)^{3/2}}
\left(
z\hat{\mathbf x}
+
z\hat{\mathbf y}
+
\frac{a\pi}{2}\hat{\mathbf z}
\right).
$$

**(b)**
$$
\mathbf B=
\frac{\mu_0I}{2}
\frac{a^2}{(a^2+z^2)^{3/2}}
\hat{\mathbf z}.
$$
""",
    "6.13": r"""
$$
\mathbf B=
\frac{\mu_0\rho_s\omega}{2}
\left[
\frac{a^2+2z^2}{\sqrt{a^2+z^2}}
-2|z|
\right]\hat{\mathbf z}.
$$
""",

    # ------------------------------------------------------------------
    # Kapitel 7
    # ------------------------------------------------------------------
    "7.1": r"""
Om elektronens rörelse sker i positiv omloppsriktning relativt $\hat{\mathbf z}$:
$$
\mathbf m=-\frac12eva\,\hat{\mathbf z}.
$$
""",
    "7.2": r"""
**(a)**
$$
\mathbf T=\pi IBa^2\,\hat{\mathbf y}.
$$

**(b)** Samma resultat fås från $\mathbf T=\mathbf m\times\mathbf B$.

**(c)** Riktningen stämmer med magnetnålsbilden.
""",
    "7.3": r"""
$$
T=
\frac{3\mu_0m^2}{8\pi r^3}\sin(2\theta)
=1.5\times10^{-7}\ \mathrm{Nm}.
$$
""",
    "7.5": r"""
Dipolapproximationen avviker med mindre än $1\%$ på symmetriaxeln från ungefär
$$
z=12.2\,a.
$$
""",
    "7.6": r"""
$$
\Phi=
\frac{\mu_0m}{2r_J}\sin^2\theta_{\max}
=9.5\times10^8\ \mathrm{Wb},
$$
där $\theta_{\max}=20^\circ$.
""",
    "7.7": r"""
$$
B=\frac{\rho_{\mathrm{Cu}}g}{J}
=29\times10^{-3}\ \mathrm T.
$$
""",
    "7.10": r"""
$$
\Phi=
\frac{\mu_0Ia}{4\pi}
\ln\left(\frac{b^2+c^2}{c^2}\right).
$$
""",

    # ------------------------------------------------------------------
    # Kapitel 8
    # ------------------------------------------------------------------
    "8.1": r"""
**(a)** $B=0.8\ \mathrm T$

**(b)** $B=0.9\ \mathrm T$
""",
    "8.2": r"""
Den fysikaliskt tillåtna lösningen ger
$$
B\approx0.22\ \mathrm T.
$$

Den andra algebraiska roten ger negativ flödestäthet i järnmaterialet och förkastas i facit.
""",
    "8.4": r"""
$$
\Phi=1.1\times10^{-8}\ \mathrm{Wb}.
$$
""",
    "8.5": r"""
För både koppar och järn bestäms $H$ av den fria strömmen:
$$
\mathbf H=
\begin{cases}
0, & R<a,\\[4pt]
\dfrac{I(R^2-a^2)}{2\pi R(b^2-a^2)}\,\hat{\boldsymbol\phi},
& a<R<b,\\[8pt]
\dfrac{I}{2\pi R}\,\hat{\boldsymbol\phi},
& R>b.
\end{cases}
$$

**(a) Koppar**
$$
\mathbf B=\mu_0\mathbf H,\qquad \mathbf M=0
$$
för alla $R$.

**(b) Järn**

För $a<R<b$:
$$
\mathbf B=\mu_0\mu_r\mathbf H,
\qquad
\mathbf M=(\mu_r-1)\mathbf H.
$$
För $R<a$ och $R>b$:
$$
\mathbf B=\mu_0\mathbf H,\qquad \mathbf M=0.
$$
""",
    "8.6": r"""
$$
F=\frac{\Phi_0^2}{\mu_0S}=260\ \mathrm N.
$$
""",
    "8.12": r"""
**(a)**
$$
\mathbf B=
\frac{\mu_0M}{2}
\left[
\frac{z}{\sqrt{a^2+z^2}}
-
\frac{z-h}{\sqrt{a^2+(z-h)^2}}
\right]\hat{\mathbf z}.
$$

**(b)**
$$
\mathbf H=
\begin{cases}
\mathbf B/\mu_0-M\hat{\mathbf z}, & 0<z<h,\\
\mathbf B/\mu_0, & \text{annars}.
\end{cases}
$$

**(c)** När $a$ är mycket stor:
$$
\mathbf H=-M\hat{\mathbf z}\quad (0<z<h),
$$
och för övrigt är alla fält noll; även $B=0$.
""",
    "8.13": r"""
**(a)**
$$
\mathbf J_m=
\frac{I}{\pi a^2}(\mu_r-1)\hat{\mathbf z}
\qquad (R<a),
$$
$$
\mathbf J_{sm}=
-\frac{I}{2\pi a}(\mu_r-1)\hat{\mathbf z}
\qquad (R=a).
$$

**(b)** Den tryckta facitdelen anger inget separat nytt uttryck för del (b). Deluppgiften
är att visa att volym- och ytbidragen tillsammans ger total magnetiseringsström
$noll$ i $z$-riktningen.
""",

    # ------------------------------------------------------------------
    # Kapitel 9
    # ------------------------------------------------------------------
    "9.2": r"""
$$
M=\frac{2d\mu_0\ln2}{\pi}.
$$
""",
    "9.4": r"""
Båda metoderna ger
$$
M=
\frac{\mu_0\pi a^2b^2}
{2(d^2+b^2)^{3/2}}.
$$
""",
    "9.6": r"""
$$
u_2(t)=
\frac{\mu_0\mu_rN_1N_2SI_0\omega}{\ell}
\sin(\omega t).
$$
""",
    "9.13": r"""
$$
W=
\frac{2B^2a^3v}{R_\Omega}
=0.40\ \mathrm J.
$$
""",
    "9.14": r"""
Båda beskrivningssätten ger samma elektromotoriska spänning:
$$
\mathcal E=
\frac{3\mu_0ma^2v}{2z^4}.
$$
""",

    # ------------------------------------------------------------------
    # Kapitel 10
    # ------------------------------------------------------------------
    "10.2": r"""
$$
\mathbf J_F\equiv\frac{\partial\mathbf D}{\partial t}
=
\frac{I_0}{A}\sin(\omega t).
$$
""",
    "10.3": r"""
$$
\mathbf J(r,t)=
-\frac{1}{r^2}
\left[
\int_0^r
\frac{\partial\rho(r',t)}{\partial t}(r')^2\,dr'
\right]\hat{\mathbf r},
$$
$$
\mathbf J_F\equiv\frac{\partial\mathbf D}{\partial t}=-\mathbf J.
$$

Därför är
$$
\mathbf B=0
$$
en lösning trots att $\mathbf J\ne0$.
""",
}


def facit_for_problem(problem) -> str | None:
    """Returnera tryckt facit för en registrerad uppgift."""
    return FACIT_BY_ID.get(problem_id_from_name(problem.name))
