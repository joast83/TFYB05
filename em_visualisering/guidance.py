"""Progressiv studievägledning för övningsuppgifter i TFYB05.

Målet är att hjälpa studenten att välja rätt fysikalisk idé och matematisk
representation utan att omedelbart visa en fullständig lösning. Ledtrådarna är
ordnade från konceptuell startpunkt till den avgörande uppställningen. Katalogen täcker alla uppgifter från kapitel 2–10 som för närvarande är registrerade i
programmet.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SolutionGuidance:
    """Pedagogiskt stöd för en uppgift, utan fullständig facitlösning."""

    problem_id: str
    learning_goal: str
    concepts: tuple[str, ...]
    start_here: str
    hints: tuple[str, ...]
    self_checks: tuple[str, ...]
    hint_titles: tuple[str, ...]
    common_pitfall: str = ""
    visualization_note: str = ""
    setup_hint: str = ""
    geometry_hint: str = ""


G = SolutionGuidance


GUIDANCE_BY_CLASS: dict[str, SolutionGuidance] = {
    # ------------------------------------------------------------------
    # Kapitel 2 – Coulombs lag, E-fält och potential i vakuum/luft
    # ------------------------------------------------------------------
    'ChargedSpheresSmallAngle': G(
        problem_id='2.1',
        learning_goal='Koppla ihop kraftjämvikt, geometri och småvinkelapproximation i samma härledning.',
        concepts=(
            'Coulombs lag',
            'statisk jämvikt',
            'små vinklar',
        ),
        start_here=r'Skriv först kraftjämvikten $\sum_i\overline F_i=0$ för en kula och Coulombs lag $F_{\mathrm{el}}=\frac{Q^2}{4\pi\varepsilon_0 R^2}$. Identifiera krafterna, avståndet R mellan laddningarna och sambandet mellan trådvinkeln θ och den sökta öppningsvinkeln α.',
        hint_titles=('Rita krafterna', 'Eliminera trådspänningen', 'Använd små vinklar'),
        hints=(
            r'Krafterna är tyngden mg nedåt, trådspänningen T längs tråden och den elektriska repulsionen horisontellt. Sätt $\theta=\alpha/2$. Geometrin ger $R=2\ell\sin\theta$.',
            r"""Projicera kraftjämvikten i horisontell och vertikal riktning:

$$
\begin{aligned}
T\sin\theta &= F_{\mathrm{el}},\\
T\cos\theta &= mg.
\end{aligned}
$$

Dividera ekvationerna och sätt in Coulombkraften med $R=2\ell\sin\theta$.""",
            r"""Du har nu

$$
\tan\theta=\frac{Q^2}{4\pi\varepsilon_0 mg(2\ell\sin\theta)^2}.
$$

Använd $\sin\theta\simeq\theta$ och $\tan\theta\simeq\theta$ i radianer, lös efter $\theta$ och byt sist tillbaka till $\alpha=2\theta$.""",
        ),
        self_checks=(
            r"""Ökar vinkeln när $|Q|$ ökar, och minskar den när m eller $\ell$ ökar? Kontrollera även gränsen $Q\to0$.""",
            r"""Uttrycket för $\alpha$ ska vara dimensionslöst. Sätt in värdena och kontrollera att $\alpha$ verkligen är mycket mindre än 1 radian; annars är småvinkelapproximationen inte tillförlitlig.""",
        ),
        common_pitfall=r"""Att använda $\alpha$ som trådens vinkel mot lodlinjen i stället för $\alpha/2$.""",
        setup_hint=r"""Utgå från $\sum_i\overline F_i=0$ och

$$
F_{\mathrm{el}}=\frac{Q^2}{4\pi\varepsilon_0 R^2}.
$$

Sätt in $R=2\ell\sin\theta$ i

$$
mg\tan\theta=F_{\mathrm{el}}.
$$

Gör småvinkelapproximationen först när denna ekvation är uppställd.""",
        geometry_hint=r"""Rita en lodlinje från upphängningen. Varje kula ligger $\ell\sin\theta$ från lodlinjen, så avståndet mellan kulorna är dubbelt så stort. Vinkeln $\alpha$ är hela öppningsvinkeln.""",
    ),
    'ChargedRingAxis': G(
        problem_id='2.2',
        learning_goal='Bygg upp Coulombintegralen för en kontinuerlig ringladdning från dQ′, r−r′ och |r−r′| innan symmetri används.',
        concepts=('Coulombs lag', 'linjeladdning och parametrisering', 'vektorintegral'),
        start_here=r'Utgå från det allmänna uttrycket $\overline E(\overline r)=\frac{1}{4\pi\varepsilon_0}\int\frac{\overline r-\overline r^{\prime}}{|\overline r-\overline r^{\prime}|^3}\,\mathrm dQ^{\prime}$ över källan. Identifiera först observationspunkten r, källpunkten r′ och laddningselementet dQ′ för hela ringen. Vilken koordinat är lämplig att integrera över?',
        hint_titles=('Laddningen på en liten båge', 'Vektorn från bågen till fältpunkten', 'Integrera ett helt varv'),
        hints=(
            r"""Välj observationspunkten och parametrisera ringens källpunkt:

$$
\begin{aligned}
\overline r&=(0,0,z),\\
\overline r^{\prime}(\phi)&=(a\cos\phi,a\sin\phi,0), \qquad 0\leq\phi\leq2\pi.
\end{aligned}
$$

Med $\rho_\ell=Q/(2\pi a)$ och bågelementet

$$
\mathrm d\ell=a\,\mathrm d\phi
$$

blir laddningselementet

$$
\mathrm dQ^{\prime}=\rho_\ell a\,\mathrm d\phi
=\frac{Q}{2\pi}\,\mathrm d\phi.
$$""",
            r"""Beräkna vektorn från källpunkten till observationspunkten:

$$
\overline r-\overline r^{\prime}
=(-a\cos\phi,-a\sin\phi,z).
$$

Dess belopp är

$$
|\overline r-\overline r^{\prime}|=\sqrt{a^2+z^2}.
$$

Sätt först nu in dessa uttryck tillsammans med $\mathrm dQ^{\prime}$ i den allmänna fältintegralen.""",
            r"""Enhetsvektorn som anger ringens radiella riktning i källplanet är

$$
\hat R(\phi)=\cos\phi\,\hat x+\sin\phi\,\hat y.
$$

Den ändrar riktning runt ringen. Skriv därför bidragen i en fast kartesisk bas innan du integrerar komponenterna. Bidragen med $\cos\phi$ och $\sin\phi$ försvinner över ett helt varv, medan z-komponenten återstår. Kontrollera detta direkt i integralen, utan att ersätta ringen med två punktladdningar.""",
        ),
        self_checks=(
            r'Fältet ska vara noll vid $z=0$ och $E_z$ ska byta tecken när z byter tecken. Rotationssymmetrin kring z-axeln bekräftar att tvärkomponenterna ska försvinna.',
            r"""För $|z|\gg a$ ska fältet närma sig punktladdningsfältet. För $Q>0$ ska det peka bort från ringen på båda sidor.""",
        ),
        common_pitfall=r"""Att glömma bågfaktorn a i

$$
\mathrm dQ^{\prime}=\rho_\ell a\,\mathrm d\phi
$$

eller integrera fältets belopp i stället för dess komponenter. Symmetri kan användas för att kontrollera komponentintegralerna.""",
        visualization_note=r'En axelgraf är användbar först efter härledningen, framför allt för att kontrollera $z=0$ och fjärrfältet.',
        setup_hint=r"""Starta med

$$
\overline E(\overline r)=\frac{1}{4\pi\varepsilon_0}\int\frac{\overline r-\overline r^{\prime}}{|\overline r-\overline r^{\prime}|^3}\,\mathrm dQ^{\prime}.
$$

Använd $\overline r=(0,0,z)$,

$$
\begin{aligned}
\overline r^{\prime}&=(a\cos\phi,a\sin\phi,0),\\
\mathrm dQ^{\prime}&=\frac{Q}{2\pi}\,\mathrm d\phi
\end{aligned}
$$

och integrationsgränserna 0 till $2\pi$; integrera sedan komponentvis.""",
        geometry_hint=r"""$\phi$ beskriver källpunktens position på hela ringen, medan observationspunkten $\overline r=(0,0,z)$ hålls fast. Vektorn $\overline r-\overline r^{\prime}$ pekar från laddningselementet mot observationspunkten och har samma längd för alla $\phi$.""",
    ),
    'FiniteLineCharge2D': G(
        problem_id='2.3',
        learning_goal='Identifiera källkoordinat, laddningselement och separationsvektor i Coulombintegralen för en ändlig tråd.',
        concepts=('linjeladdning', 'vektorintegral', 'gränsvärde'),
        start_here=r'Skriv den allmänna Coulombintegralen $\overline E(\overline r)=\frac{1}{4\pi\varepsilon_0}\int\frac{\overline r-\overline r^{\prime}}{|\overline r-\overline r^{\prime}|^3}\,\mathrm dQ^{\prime}$. Låt sedan r vara den fasta observationspunkten (x,0,0) och låt r′ löpa längs tråden. Bestäm vilka gränser och vilket dQ′ som hör till källan.',
        hint_titles=('Välj källkoordinat och gränser', 'Skriv de två fältkomponenterna', 'Ta gränsen för en lång tråd'),
        hints=(
            r"""Låt källpunkten löpa längs tråden medan observationspunkten hålls fast:

$$
\begin{aligned}
\overline r&=(x,0,0),\\
\overline r^{\prime}&=(0,0,z^{\prime}),\qquad -b\leq z^{\prime}\leq a.
\end{aligned}
$$

Trådens konstanta linjeladdningstäthet ger laddningselementet

$$
\mathrm dQ^{\prime}=\rho_\ell\,\mathrm dz^{\prime}.
$$""",
            r"""Identifiera separationsvektorn

$$
\overline r-\overline r^{\prime}=(x,0,-z^{\prime})
$$

och dess belopp

$$
|\overline r-\overline r^{\prime}|=\sqrt{x^2+(z^{\prime})^2}.
$$

Sätt in dessa uttryck och $\mathrm dQ^{\prime}$ i Coulombintegralen. Dela därefter upp integralen i x- och z-komponenter.""",
            r"""Beräkna de två komponentintegralerna med gränserna

$$
-b\leq z^{\prime}\leq a.
$$

I del (b) låter du därefter $a$ och $b$ gå mot oändligheten oberoende av varandra. Kontrollera att z-komponenten försvinner och att det återstående fältet avtar som $1/|x|$.""",
        ),
        self_checks=(
            r"""Om $a=b$ ska $E_z$ försvinna. Om $a>b$ och $\rho_\ell>0$ ska $E_z$ vara negativ vid (x,0,0), eftersom mer positiv laddning ligger på +z-sidan.""",
            r'I den oändliga gränsen ska $E_z\to0$ och $|E_x|$ avta som $1/|x|$. Fältet ska peka bort från tråden för positiv linjeladdning.',
        ),
        common_pitfall=r"""Att använda cylindersymmetri för den ändliga tråden, eller blanda ihop observationskoordinaten x med integrationsvariabeln $z^{\prime}$.""",
        setup_hint=r"""Sätt $\overline r=(x,0,0)$,

$$
\begin{aligned}
\overline r^{\prime}&=(0,0,z^{\prime}),\\
\mathrm dQ^{\prime}&=\rho_\ell\,\mathrm dz^{\prime}
\end{aligned}
$$

och

$$
\overline r-\overline r^{\prime}=(x,0,-z^{\prime})
$$

i

$$
\overline E(\overline r)=\frac{1}{4\pi\varepsilon_0}\int\frac{\overline r-\overline r^{\prime}}{|\overline r-\overline r^{\prime}|^3}\,\mathrm dQ^{\prime}.
$$

Nämnaren blir $(x^2+z^{\prime2})^{3/2}$; integrera från −b till a.""",
        geometry_hint=r"""Tråden följer z-axeln från −b till a, medan fältpunkten ligger på x-axeln. Vektorn $\overline r-\overline r^{\prime}$ går från källelementet $(0,0,z^{\prime})$ till observationspunkten (x,0,0), så dess z-komponent är $-z^{\prime}$.""",
    ),
    'SemiCircularSurfaceAxis': G(
        problem_id='2.4',
        learning_goal='Bygg upp Coulombintegralen för en halvcirkelskiva och använd först därefter den återstående symmetrin.',
        concepts=('ytladdning', 'polära koordinater', 'komponentsymmetri'),
        start_here=r'Börja med $\overline E(\overline r)=\frac{1}{4\pi\varepsilon_0}\int\frac{\overline r-\overline r^{\prime}}{|\overline r-\overline r^{\prime}|^3}\,\mathrm dQ^{\prime}$ över den laddade ytan. Identifiera observationspunkten, välj två koordinater för källpunkten på halvcirkelskivan och bestäm dQ′ från ytladdningstätheten.',
        hint_titles=('Ytelementet på halvskivan', 'Avstånd och riktning till fältpunkten', 'Vilken komponent försvinner?'),
        hints=(
            r"""Välj observationspunkten och parametrisera källpunkten på halvskivan:

$$
\begin{aligned}
\overline r&=(0,0,z),\\
\overline r^{\prime}&=(R\cos\phi,R\sin\phi,0),\\
0\leq R\leq a,\quad &0\leq\phi\leq\pi.
\end{aligned}
$$

Ytan ligger på sidan $y\geq0$. Det polära ytelementet och laddningselementet är

$$
\mathrm dS^{\prime}=R\,\mathrm dR\,\mathrm d\phi,
\qquad
\mathrm dQ^{\prime}=\rho_s R\,\mathrm dR\,\mathrm d\phi.
$$""",
            r"""Beräkna först vektorn från källpunkten till observationspunkten:

$$
\overline r-\overline r^{\prime}
=(-R\cos\phi,-R\sin\phi,z).
$$

Dess belopp är

$$
|\overline r-\overline r^{\prime}|=\sqrt{R^2+z^2}.
$$

Sätt in dessa uttryck och $\mathrm dQ^{\prime}$ i Coulombintegralen med båda integrationsgränserna.""",
            r"""Skriv källpunktens radiella enhetsvektor i en fast kartesisk bas:

$$
\hat R(\phi)=\cos\phi\,\hat x+\sin\phi\,\hat y.
$$

Integrera sedan över $\phi$. x-komponenten blir noll, men y-komponenten försvinner inte för en halvcirkelskiva. Genomför därefter radialintegralerna.""",
        ),
        self_checks=(
            r"""För $\rho_s>0$ och $z>0$ ska $E_x=0$, $E_y<0$ och $E_z>0$. Kontrollera riktningarna mot den valda halvcirkeln.""",
            r'Långt bort ska den ledande termen vara punktladdningsfältet för $Q=\rho_s\pi a^2/2$; tvärkomponenten avtar snabbare. Punkten $z=0$ ligger på skivans kant och är inte ett vanligt reguljärt kontrollvärde.',
        ),
        common_pitfall=r"""Fick du även $E_y=0$? Kontrollera vinkelgränserna: integralen av $\sin\phi$ från 0 till π försvinner inte. Ett helt varv skulle beskriva en annan yta.""",
        setup_hint=r"""Starta med

$$
\overline E(\overline r)=\frac{1}{4\pi\varepsilon_0}\int\frac{\overline r-\overline r^{\prime}}{|\overline r-\overline r^{\prime}|^3}\,\mathrm dQ^{\prime}.
$$

Använd

$$
\begin{aligned}
\mathrm dQ^{\prime}&=\rho_s R\,\mathrm dR\,\mathrm d\phi,\\
\overline r-\overline r^{\prime}&=(-R\cos\phi,-R\sin\phi,z)
\end{aligned}
$$

och

$$
|\overline r-\overline r^{\prime}|=\sqrt{R^2+z^2},
$$

med $0\leq R\leq a$ och $0\leq\phi\leq\pi$.""",
        geometry_hint=r"""I originalfiguren ligger den laddade halvcirkelskivan i xy-planet med $y\geq0$. $\overline r^{\prime}$ är en rörlig källpunkt på skivan och $\overline r=(0,0,z)$ är den fasta fältpunkten; y-symmetri saknas men x-bidragen tar ut varandra.""",
    ),
    'SphericalShellPotential': G(
        problem_id='2.5',
        learning_goal='Härled skalets potential direkt från den allmänna potentialintegralen med ett korrekt dQ′ och |r−r′|.',
        concepts=('potentialintegral', 'sfärisk symmetri', 'källområde'),
        start_here=r'Utgå från potentialintegralen i originaluppgiften: $V(\overline r)=\frac{1}{4\pi\varepsilon_0}\int\frac{\mathrm dQ^{\prime}}{|\overline r-\overline r^{\prime}|}$ över källområdet. Här är källområdet det laddade sfärskalets yta, inte dess volym. Identifiera dQ′, $\overline r-\overline r^{\prime}$ och $|\overline r-\overline r^{\prime}|$ innan du integrerar.',
        hint_titles=('Laddningselementet på skalet', 'Avståndet till observationspunkten', 'Dela upp svaret vid skalradien'),
        hints=(
            r"""Placera observationspunkten på z-axeln och beskriv källpunkten på sfärskalet:

$$
\begin{aligned}
\overline r&=(0,0,r),\\
\overline r^{\prime}
&=a(\sin\theta\cos\phi,\sin\theta\sin\phi,\cos\theta).
\end{aligned}
$$

För jämn ytladdning är $\rho_s=Q/(4\pi a^2)$, så

$$
\mathrm dQ^{\prime}
=\rho_s a^2\sin\theta\,\mathrm d\theta\,\mathrm d\phi.
$$""",
            r"""Bilda separationsvektorn:

$$
\overline r-\overline r^{\prime}
=(-a\sin\theta\cos\phi,-a\sin\theta\sin\phi,r-a\cos\theta).
$$

Avståndet mellan källan och fältpunkten är

$$
|\overline r-\overline r^{\prime}|
=\sqrt{r^2+a^2-2ar\cos\theta}.
$$

Sätt nu in avståndet och $\mathrm dQ^{\prime}$ i originaluppgiftens potentialintegral.""",
            r"""Integrera först över $\phi$ och använd sedan substitutionen

$$
u=\cos\theta.
$$

Vid integrationsgränserna dyker $r+a$ och $|r-a|$ upp. Behandla därför $r<a$ och $r>a$ var för sig. Fallet $r=0$ kan kontrolleras direkt utan division med $r$.""",
        ),
        self_checks=(
            r'V ska vara kontinuerlig vid $r=a$ och gå mot noll när $r\to\infty$.',
            r'Kontrollera med $E_r=-\mathrm dV/\mathrm dr$: inuti ska fältet vara noll och utanför ska det ha punktladdningens $1/r^2$-beroende. Derivatan får däremot ha ett språng vid den laddade ytan.',
        ),
        common_pitfall='Att ersätta den begärda potentialintegralen med Gauss lag, att integrera över skalets volym eller att blanda ihop observationsradien r och skalradien a.',
        setup_hint=r"""Sätt $\overline r=(0,0,r)$,

$$
\begin{aligned}
\overline r^{\prime}&=a(\sin\theta\cos\phi,\sin\theta\sin\phi,\cos\theta),\\
\mathrm dQ^{\prime}&=\frac{Q}{4\pi a^2}\,a^2\sin\theta\,\mathrm d\theta\,\mathrm d\phi
\end{aligned}
$$

och

$$
|\overline r-\overline r^{\prime}|=\sqrt{r^2+a^2-2ar\cos\theta}
$$

i

$$
V(\overline r)=\frac{1}{4\pi\varepsilon_0}\int\frac{\mathrm dQ^{\prime}}{|\overline r-\overline r^{\prime}|}.
$$""",
        geometry_hint=r"""Välj observationspunkten på z-axeln tack vare sfärisk symmetri. Källpunkten $\overline r^{\prime}$ ligger på sfärytan med fast radie a; vinkeln $\theta$ mäts från z-axeln. Skillnadsvektorns längd fås med cosinussatsen.""",
    ),
    'ConcentricChargedCylinders': G(
        problem_id='2.6',
        learning_goal='Välja rätt Gaussyta och hålla reda på vilken laddning som omsluts i olika radialområden.',
        concepts=(
            'Gauss lag',
            'cylindersymmetri',
            'styckvis fält',
        ),
        start_here=r'Skriv Gauss lag $\oint_S\overline{E}\cdot\mathrm d\overline{S}=\frac{Q_{\mathrm{in}}}{\varepsilon_0}$. Identifiera systemets symmetri, en lämplig sluten yta och vilken laddning den omsluter. Försumma ändeffekter för de långa cylindrarna.',
        hint_titles=('Vilka ytor ger flöde?', 'Vilka cylindrar omsluts?', 'Bestäm fältet områdesvis'),
        hints=(
            r'Cylindersymmetrin ger $\overline E=E_R(R)\,\hat R$. Välj en koaxial Gauss-cylinder med radie R och längd L. På manteln är $\overline E\cdot\hat n=E_R$ och arean $2\pi RL$; på ändytorna är $\overline E\cdot\hat n=0$.',
            r"""Beräkna $Q_{\mathrm{in}}$ från de verkliga laddade ytornas areor:

$$
Q_{\mathrm{in}}=
\begin{cases}
0, & R<a,\\
\rho_{s,a}\,2\pi aL, & a<R<b,\\
\rho_{s,a}\,2\pi aL+\rho_{s,b}\,2\pi bL, & R>b.
\end{cases}
$$

Radierna $a$ och $b$ hör till de laddade ytorna. Gaussytans radie $R$ avgör vilka av dem som ligger innanför.""",
            r"""Sätt in den inneslutna laddningen i Gauss lag för varje radialområde:

$$
E_R\,2\pi RL=\frac{Q_{\mathrm{in}}}{\varepsilon_0}.
$$

Lös efter $E_R$ i respektive område. Multiplicera med $\hat R$ för att få vektorfältet och behåll laddningarnas tecken.""",
        ),
        self_checks=(
            r'För $R<a$ är fältet noll. Utanför båda cylindrarna ska det också bli noll om $a\rho_{s,a}+b\rho_{s,b}=0$, även om vardera cylindern är laddad.',
            r"""Med normalen riktad mot större R ska

$$
E_R^{\mathrm{ut}}-E_R^{\mathrm{in}}=\rho_s/\varepsilon_0
$$

vid varje laddad yta. Kontrollera båda sprången.""",
        ),
        common_pitfall=r'Fick du samma fältuttryck i alla tre områden? Skriv $Q_{\mathrm{in}}$ på nytt för varje radie. Gaussytan kan omsluta noll, en eller två laddade cylinderytor.',
        setup_hint=r'Identifiera vänsterledet som $E_R\,2\pi RL$ och högerledet som $Q_{\mathrm{in}}/\varepsilon_0$. Gör en rad för varje radialområde och sätt in rätt $Q_{\mathrm{in}}$ innan du löser efter $E_R$; den godtyckliga längden L ska förkortas bort.',
        geometry_hint='Gaussytan är en tänkt cylinder vars radie R kan varieras. Laddningen sitter däremot på de verkliga cylindrarna vid a och b, så deras areor ska inte beräknas med R.',
    ),
    'SphericalCapacitorDesign': G(
        problem_id='2.7',
        learning_goal='Göra en fysikalisk optimering där genomslagsfältet sätter en begränsning.',
        concepts=(
            'sfärisk kondensator',
            'fältmaximum',
            'optimering',
        ),
        start_here=r'Skriv Gauss lag $\oint_S\overline{E}\cdot\mathrm d\overline{S}=\frac{Q_{\mathrm{in}}}{\varepsilon_0}$ och potentialskillnaden $V(a)-V(b)=\int_a^b E_r\,\mathrm dr$. Bestäm först E_r i gapet från symmetrin och laddningen; använd därefter kravet $|E|\leq E_{\max}$ för optimeringen.',
        hint_titles=('Fältet i gapet', 'Laddningsgränsen vid ytan', 'Optimera spänningen'),
        hints=(
            r"""Sfärisk symmetri ger $\overline E=E_r(r)\,\hat r$. En sfärisk Gaussyta i $a<r<b$ omsluter innerledarens laddning Q, så

$$
4\pi r^2E_r=Q/\varepsilon_0.
$$

Lös efter $E_r$ innan du söker fältmaximum.""",
            r"""Fältbeloppet avtar som $1/r^2$ och är störst vid $r=a$. Sätt därför

$$
|E(a)|=E_{\max}
$$

och bestäm $|Q|_{\max}(a)$. När $a$ varieras i optimeringen varierar alltså även den tillåtna laddningen.""",
            r"""Sätt in $|Q|_{\max}(a)$ i

$$
U_{\max}(a)=\int_a^b|E_r|\,\mathrm dr.
$$

Derivera med avseende på a med b och $E_{\max}$ konstanta. Lös det stationära villkoret i $0<a<b$ och jämför med randgränserna.""",
        ),
        self_checks=(
            r'Vid genomslagsbegränsad laddning ska den tillåtna spänningen gå mot noll när $a\to0$ och när $a\to b$. Ett inre maximum måste jämföras med dessa gränser.',
            r'Den stationära punkten ska ligga i $0<a<b$ och ha negativ andraderivata. Enheten i spänningsuttrycket ska vara $E_{\max}$ gånger en längd.',
        ),
        common_pitfall=r'Att optimera kondensatorns vanliga spänningsuttryck med Q konstant, trots att Q här begränsas av $E_{\max}$ och därför beror på a.',
        setup_hint=r"""Börja med Gauss lag och bestäm den största tillåtna laddningen vid innerytan:

$$
\begin{aligned}
4\pi r^2E_r&=\frac{Q}{\varepsilon_0},\\
|Q|_{\max}&=4\pi\varepsilon_0a^2E_{\max}.
\end{aligned}
$$

Sätt sedan in laddningsgränsen i spänningsintegralen:

$$
U_{\max}(a)=\int_a^b\frac{|Q|_{\max}(a)}{4\pi\varepsilon_0r^2}\,\mathrm dr.
$$

Utför integralen innan du optimerar. Den tillåtna laddningen beror på $a$ och ska därför inte hållas konstant.""",
        geometry_hint='Rita de två radierna och ett godtyckligt r i gapet. Det minsta tillåtna r i luften är a, vilket är varför det största fältet uppstår där.',
    ),
    'ConcentricSphericalShells': G(
        problem_id='2.8',
        learning_goal='Bestämma ett styckvis fält med Gauss lag, integrera till potentialen och använda ledarvillkor efter sammankoppling.',
        concepts=(
            'Gauss lag och potentialintegral',
            'sfärskal',
            'elektrostatisk ledare',
        ),
        start_here=r'Skriv $\oint_S\overline{E}\cdot\mathrm d\overline{S}=\frac{Q_{\mathrm{in}}}{\varepsilon_0}$ och $V(r)=\int_r^\infty E_r(s)\,\mathrm ds$ med $V(\infty)=0$. Använd sfärisk symmetri och identifiera $Q_{\mathrm{in}}$ i de tre radialområdena innan potentialen beräknas.',
        hint_titles=('Innesluten laddning', 'Integrera genom flera områden', 'När skalen kopplas ihop'),
        hints=(
            r"""Sfärisk symmetri gör fältet radiellt och lika stort över en sfärisk Gaussyta. Gauss lag blir

$$
4\pi r^2 E_r=\frac{Q_{\mathrm{in}}}{\varepsilon_0}.
$$

Identifiera först vilken laddning ytan omsluter:

$$
Q_{\mathrm{in}}=
\begin{cases}
0, & r<a,\\
Q_a, & a<r<b,\\
Q_a+Q_b, & r>b.
\end{cases}
$$

Sätt in en rad i taget och lös efter $E_r$. Radien $r$ hör till Gaussytan; $a$ och $b$ är skalens fasta radier.""",
            r"""Välj $V(\infty)=0$ och integrera från observationsradien till oändligheten. I gapet, $a<r<b$, passerar du två områden med olika fältuttryck:

$$
\begin{aligned}
V(r)&=\int_r^b E_{\mathrm{gap}}(s)\,\mathrm ds\\
&\quad+\int_b^\infty E_{\mathrm{yttre}}(s)\,\mathrm ds.
\end{aligned}
$$

Här är $s$ integrationsvariabeln. Sätt in respektive fält från Gauss lag. För $r<a$ tillkommer en sträcka där $E=0$, så potentialen är samma som vid $r=a$. Behåll bidragen från alla passerade områden så att referensen är densamma överallt.""",
            r"""I del (b) betecknas slutladdningarna $q_a$ och $q_b$. Använd laddningsbevarande och samma potential på de sammankopplade skalen:

$$
\begin{aligned}
q_a+q_b&=Q_a+Q_b,\\
V(a)-V(b)&=\int_a^b E_r\,\mathrm dr=0.
\end{aligned}
$$

Sätt in gapfältet med $q_a$ och lös sedan laddningsfördelningen.""",
        ),
        self_checks=(
            'Potentialen ska vara kontinuerlig vid a och b och närma sig noll vid oändligheten. Utanför b beror den bara på den sammanlagda laddningen.',
            'Efter förbindelsen ska laddningen vara bevarad och potentialskillnaden mellan skalen vara noll. I den sfäriskt symmetriska modellen ska resultatet också ge noll fält i gapet.',
        ),
        common_pitfall=r"""Att bevara $Q_a$ och $Q_b$ var för sig efter sammankopplingen, eller anta att ett tomt område alltid har $E=0$. Här måste fältet i gapet följa av potentialvillkoret och geometrin.""",
        setup_hint=r"""Bestäm först fältet områdesvis:

$$
E_r(r)=\frac{Q_{\mathrm{in}}(r)}{4\pi\varepsilon_0r^2}.
$$

I gapet blir potentialintegralen

$$
\begin{aligned}
V(r)&=\int_r^b\frac{Q_a}{4\pi\varepsilon_0s^2}\,\mathrm ds\\
&\quad+\int_b^\infty\frac{Q_a+Q_b}{4\pi\varepsilon_0s^2}\,\mathrm ds.
\end{aligned}
$$

Efter förbindelsen används samma uppställning med de nya laddningarna $q_a$ och $q_b$ och villkoret $V(a)=V(b)$.""",
        geometry_hint='Markera en sfärisk Gaussyta i vart och ett av de tre radialområdena. Kontrollera vilka laddade skal som ligger innanför ytan. Dela sedan integrationsvägen från observationsradien till oändligheten där fältuttrycket ändras.',
    ),
    "AtmosphericChargeDensity": G(
        problem_id="2.9",
        learning_goal=r"""Översätta en observerad fältändring till medelladdning via flödet genom en sluten Gaussyta.""",
        concepts=("Gauss lag", "fältgradient", "teckenkonvention"),
        start_here=r'Skriv Gauss lag $\oint_S\overline{E}\cdot\mathrm d\overline{S}=\frac{Q_{\mathrm{in}}}{\varepsilon_0}$ och medelladdningstätheten $\langle\rho\rangle=Q_{\mathrm{in}}/\text{volym}$. Här är fälten givna och laddningen söks. Identifiera ytornas normaler och fältens signerade komponenter innan de sätts in.',
        hint_titles=('Välj riktning och yta', 'Tecknen på topp och botten', 'Från laddning till medeltäthet'),
        hints=(
            r'Välj z uppåt: $E_z(0)=-300\,\mathrm{V/m}$ och $E_z(h)=-20\,\mathrm{V/m}$, $h=1400\,\mathrm m$. Använd en vertikal cylinder med tvärsnittsarea S och höjd h. Det vertikala fältet ger inget flöde genom manteln.',
            r"""Toppen har utåtnormal $+\hat z$ och botten $-\hat z$. Därför blir flödet

$$
\oint_S\overline E\cdot\mathrm d\overline S
=S E_z(h)-S E_z(0).
$$

Sätt detta lika med $Q_{\mathrm{in}}/\varepsilon_0$.""",
            r"""Lös efter $Q_{\mathrm{in}}$ och dividera med volymen Sh. Du får en medeltäthet; två fältvärden räcker inte för att bestämma den lokala funktionen $\rho(z)$.""",
        ),
        self_checks=(
            r'S ska förkortas bort och $\varepsilon_0\Delta E/h$ ha enheten $\mathrm{C/m^3}$.',
            r'Medeltätheten ska vara positiv eftersom $E_z$ ökar med höjden. Om fälten vore lika skulle medeltätheten vara noll, även om lokal laddning kunde finnas.',
        ),
        common_pitfall="Att subtrahera fältens belopp utan att först ta hänsyn till ytornas normalriktningar.",
        geometry_hint=r'Rita två nedåtpilar, en vid marken och en vid h. Rita sedan utåtnormalerna separat: uppåt på toppen och nedåt på botten. Det är skalärprodukterna $\overline E\cdot\hat n$ som bestämmer flödets tecken.',
        setup_hint=r"""Sätt in flödet och volymen:

$$
S[E_z(h)-E_z(0)]=\frac{\langle\rho\rangle Sh}{\varepsilon_0}.
$$

Förkorta S och lös efter $\langle\rho\rangle$. Använd fältkomponenterna med tecken, inte bara beloppen.""",
    ),
    "OffsetCavitySphereExterior": G(
        problem_id="2.10",
        learning_goal="Använd superposition för att ersätta ett hålrum med en negativ laddningsfördelning.",
        concepts=("superposition", "homogent laddat klot", "förskjutet centrum"),
        start_here=r'Skriv superpositionen $\overline E=\overline E_{\mathrm{stor}}+\overline E_{\text{hål}}$ och Gauss lag $\oint_S\overline{E}\cdot\mathrm d\overline{S}=\frac{Q_{\mathrm{in}}}{\varepsilon_0}$ för varje sfäriskt symmetrisk hjälpfördelning. Identifiera dess laddning och avståndet från dess eget centrum till observationspunkten.',
        hint_titles=('Bygg hålrummet av två klot', 'Fältet från varje klot', 'Mät från rätt centrum'),
        hints=(
            r"""Beskriv materialet som ett helt klot med täthet $\rho$ plus ett mindre klot med täthet $-\rho$ i hålrummet. De två hjälpfördelningarnas laddningar är

$$
\begin{aligned}
Q_{\mathrm{stor}}&=\frac{4\pi\rho b^3}{3},\\
Q_{\text{hål}}&=-\frac{4\pi\rho a^3}{3}.
\end{aligned}
$$""",
            r"""För varje klot ger sfärisk symmetri och en Gaussyta utanför klotet

$$
4\pi s^2 E_s=\frac{Q}{\varepsilon_0},
$$

där s mäts från just det klotets centrum. Punkterna $x>b$ ligger utanför båda hjälpfördelningarna.""",
            r'Hålrummets centrum ligger vid $x=-d$ enligt originalets geometri. Avstånden är x respektive $x+d$ och båda radiella enhetsvektorerna pekar längs $+x$ här. Sätt in dessa i de två fälten och summera deras signerade x-komponenter.',
        ),
        self_checks=(
            r'När $a\to0$ ska hålrummets bidrag försvinna. När $d\to0$ ska resultatet motsvara nettoladdningen i origo.',
            r'Långt bort, $x\gg b,d$, ska den ledande termen vara fältet från nettoladdningen $\frac{4\pi\rho(b^3-a^3)}{3}$. För $\rho>0$ ska $E_x$ vara positivt på den angivna delen av x-axeln.',
        ),
        common_pitfall="Att använda avståndet x till båda sfärernas centrum trots att hålrummets centrum är förskjutet.",
        geometry_hint=r'Markera centrum 0, hålrummets centrum −d och observationspunkten $x>b$ på samma axel. Kontrollera avstånden i din egen skiss: ett hålrum vid $+d$ skulle i stället ge avståndet $x-d$.',
        setup_hint=r"""Bestäm först varje hjälpfält ur

$$
4\pi s^2 E_s=\frac{Q}{\varepsilon_0}.
$$

Sätt sedan

$$
E_x=\frac{1}{4\pi\varepsilon_0}\left(\frac{Q_{\mathrm{stor}}}{x^2}+\frac{Q_{\text{hål}}}{(x+d)^2}\right).
$$

$Q_{\text{hål}}$ innehåller redan minustecknet. En enda Gaussyta kring hela det osymmetriska objektet kan inte ge det lokala fältet på detta sätt.""",
    ),
    "CoaxialCylinderVoltage": G(
        problem_id="2.11",
        learning_goal="Gå från Gauss-lagens koaxialfält till ett givet spänningsfall.",
        concepts=("koaxial geometri", "Gauss lag", "potentialskillnad"),
        start_here=r'Skriv $\oint_S\overline{E}\cdot\mathrm d\overline{S}=\frac{Q_{\mathrm{in}}}{\varepsilon_0}$ och $V(a)-V(b)=\int_a^b E_R\,\mathrm dR$. Cylindersymmetrin bestämmer hur fältet beror på R; den givna spänningen bestämmer därefter dess storlek.',
        hint_titles=('Flöde genom manteln', 'Bestäm konstanten från spänningen', 'Var ligger mittpunkten?'),
        hints=(
            r"""Försumma ändeffekter och välj en koaxial Gauss-cylinder med radie $a<R<b$ och längd L. Inför innerledarens laddning per längd $\rho_\ell$. E är radiellt, så

$$
E_R\,2\pi RL=\rho_\ell L/\varepsilon_0.
$$""",
            r"""Lös efter $E_R$. För fältbeloppet kan du skriva

$$
|E_R|=\frac{K}{R},
\qquad K=\frac{|\rho_\ell|}{2\pi\varepsilon_0}.
$$

Bestäm sedan $K$ ur spänningsintegralen

$$
U=\int_a^b |E_R|\,\mathrm dR=K\ln(b/a).
$$""",
            r"""Mittemellan ytorna är observationsradien

$$
R=a+\frac{b-a}{2}=\frac{a+b}{2}.
$$

Sätt in den först när fältfunktionen är bestämd.""",
        ),
        self_checks=(
            r'Uttrycket ska ha enheten V/m och vara proportionellt mot U. Logaritmens argument $b/a$ ska vara dimensionslöst.',
            r'I ett tunt gap, $b-a\ll a$, ska fältet närma sig plattkondensatorns $U/(b-a)$. Generellt avtar fältbeloppet som $1/R$.',
        ),
        common_pitfall=r"Att anta ett homogent fält $U/(b-a)$, vilket inte gäller för cylindrisk geometri.",
        geometry_hint=r'R mäts från den gemensamma axeln, inte från innerledarens yta. Halva gapbredden $(b-a)/2$ måste därför läggas till a.',
        setup_hint=r"""Identifiera mantelarean $2\pi RL$ och

$$
Q_{\mathrm{in}}=\rho_\ell L
$$

i Gauss lag. Lös sedan

$$
U=\int_a^b\frac{|\rho_\ell|}{2\pi\varepsilon_0R}\,\mathrm dR
$$

efter $|\rho_\ell|$, eller efter

$$
K=|\rho_\ell|/(2\pi\varepsilon_0),
$$

och beräkna fältbeloppet vid $R=\frac{a+b}{2}$.""",
    ),
    "SphericalConductorBreakdown": G(
        problem_id="2.12",
        learning_goal="Koppla luftens genomslagsfält till maximal laddning och potential på en sfärisk ledare.",
        concepts=("ledande sfär", "genomslag", "potential"),
        start_here=r'Skriv $\oint_S\overline{E}\cdot\mathrm d\overline{S}=\frac{Q_{\mathrm{in}}}{\varepsilon_0}$ och $V(a)=\int_a^\infty E_r\,\mathrm dr$. Bestäm fältet från sfärisk symmetri och laddningen Q innan du tillämpar luftens gräns $|E|\leq E_{\max}$.',
        hint_titles=('Fältet utanför sfären', 'Var nås genomslagsgränsen?', 'Potentialen relativt oändligheten'),
        hints=(
            r"""Välj en sfärisk Gaussyta med $r>a$. Fältet är radiellt och konstant över ytan, så

$$
4\pi r^2E_r=\frac{Q}{\varepsilon_0}.
$$

Lös efter $E_r$; inne i metallen är $\overline E=0$.""",
            r"""Det yttre fältbeloppet avtar med $r$ och är störst precis utanför $r=a$. Sätt

$$
\frac{|Q|}{4\pi\varepsilon_0a^2}=E_{\max}
$$

och lös efter den största tillåtna laddningens belopp.""",
            r"""Integrera $E_r$ från $a$ till $\infty$ för att få ytpotentialen med $V(\infty)=0$. Sätt in laddningsgränsen och därefter $a=0{,}10\,\mathrm m$ och

$$
E_{\max}=3\cdot10^6\,\mathrm{V/m}
$$

i del (b).""",
        ),
        self_checks=(
            r'$Q_{\max}$ ska växa som $a^2$, medan den maximala potentialens belopp växer som a. Kontrollera enheterna C respektive V.',
            r'Kvoten $|V(a)|/a$ ska vara $E_{\max}$ vid gränsen. Potentialen har samma tecken som Q, medan genomslagsvillkoret beror på fältets belopp.',
        ),
        common_pitfall="Att sätta genomslagsvillkoret vid någon godtycklig punkt utanför sfären i stället för på ytan.",
        geometry_hint=r'Markera $r=a$ precis på luftsidan av metallytan. Där är det yttre fältet störst; fältet inne i metallen kan inte användas för luftens genomslagsvillkor.',
        setup_hint=r"""Gauss lag ger

$$
E_r=\frac{Q}{4\pi\varepsilon_0 r^2}.
$$

Använd först $|E_r(a)|=E_{\max}$ och därefter

$$
V(a)=\int_a^\infty\frac{Q}{4\pi\varepsilon_0 r^2}\,\mathrm dr.
$$

Genomslagsvillkoret gäller belopp, medan potentialen behåller laddningens tecken.""",
    ),
    "CoaxialTubeSpaceCharge": G(
        problem_id="2.13",
        learning_goal=r"""Använda Gauss lag på ett cylindriskt skal och bestämma rymdladdningen från randvillkoren.""",
        concepts=("rymdladdning", "cylindrisk Gauss lag", "randvillkor"),
        start_here=r"""Skriv Gauss lag $\oint_S\overline E\cdot\mathrm d\overline S=Q_{\mathrm{in}}/\varepsilon_0$. Välj en sluten skalformad yta i gapet mellan radierna $a$ och $R$. Använd $E_R(a)=0$ och därefter $V(b)-V(a)=-\int_a^b E_R\,\mathrm dR=U$.""",
        hint_titles=('Välj en sluten Gaussyta i gapet', 'Använd fältvillkoret vid katoden', 'Bestäm molnets totala laddning'),
        hints=(
            r"""Välj ett cylindriskt skal med längd $L$, innerradie $a$ och ytterradie $R$, där $a<R<b$. Innergränsen tas precis utanför katoden. Cylindersymmetrin ger $\overline E=E_R(R)\hat R$; ändytorna ger inget flöde.

Gauss lag för den slutna skalytan blir

$$
\oint_S\overline E\cdot\mathrm d\overline S
=\frac{Q_{\mathrm{in}}}{\varepsilon_0}.
$$

Den yttre manteln har normal $+\hat R$, den inre $-\hat R$. Därför får du

$$
\begin{aligned}
\oint_S\overline E\cdot\mathrm d\overline S
&=2\pi RL E_R(R)-2\pi aL E_R(a),\\
Q_{\mathrm{in}}&=\rho\pi(R^2-a^2)L.
\end{aligned}
$$

Ytan omsluter bara molnladdningen i skalet, inte katodens metall.""",
            r"""Sätt in randvillkoret $E_R(a)=0$ i flödesekvationen:

$$
2\pi RL E_R(R)=\frac{\rho\pi(R^2-a^2)L}{\varepsilon_0}.
$$

Förkorta $L$ och lös efter $E_R(R)$. Fältet i gapet är nu uttryckt med den ännu okända laddningstätheten $\rho$.""",
            r"""Sätt fältet i

$$
U=-\int_a^b E_R\,\mathrm dR
$$

och lös efter $\rho$. Den totala molnladdningen är sedan $Q=\rho\pi(b^2-a^2)\ell$. Omvandla radier och längd till meter.""",
        ),
        self_checks=(
            r"""Kontrollera både $E_R(a)=0$ och att

$$
-\int_a^b E_R\,\mathrm dR=+300\,\mathrm V.
$$

Med denna spänning ska $\rho$ och molnets totala laddning vara negativa.""",
            r"""För negativ $\rho$ ska $E_R$ peka inåt i gapet, medan kraften på en elektron pekar utåt. Q ska vara proportionell mot $\ell$, och ha enheten C.""",
        ),
        common_pitfall=r"Att använda det laddningsfria koaxialfältet $C/R$ trots att området innehåller konstant rymdladdning.",
        geometry_hint='R löper från katodens radie a till anodens radie b. Molnet fyller ett cylindriskt skal, så dess volym är skillnaden mellan två cylindervolymer. Modellen försummar ändeffekter.',
        setup_hint=r"""Sätt in flödet genom skalytan och dess inneslutna laddning i Gauss lag. Med $E_R(a)=0$ får du

$$
\begin{aligned}
2\pi RL E_R(R)&=\frac{\rho\pi(R^2-a^2)L}{\varepsilon_0},\\
E_R(R)&=\frac{\rho}{2\varepsilon_0}\left(R-\frac{a^2}{R}\right).
\end{aligned}
$$

Bestäm sedan $\rho$ ur potentialskillnaden

$$
U=-\int_a^b E_R\,\mathrm dR.
$$

Molnets hela volym är $\pi(b^2-a^2)\ell$. Hjälpytans längd $L$ är godtycklig; $\ell$ är rörets längd i uppgiften.""",
    ),
    "RadialChargeSphere": G(
        problem_id="2.16",
        learning_goal="Bygga potentialintegralen i centrum från den givna volymladdningen och källkoordinaterna.",
        concepts=("potential", "sfäriska skal", "rymdladdning"),
        start_here=r'Skriv $V(\overline r)=\frac{1}{4\pi\varepsilon_0}\int\frac{\mathrm dQ^{\prime}}{|\overline r-\overline r^{\prime}|}$ med $V(\infty)=0$. Observationspunkten är $\overline r=0$. Identifiera $\mathrm dQ^{\prime}=\rho(\overline r^{\prime})\,\mathrm dV^{\prime}$, separationsvektorn $\overline r-\overline r^{\prime}$ och dess belopp för den givna volymladdningen.',
        hint_titles=('Volymelementet', 'Avståndet till centrum', 'Radialintegralen'),
        hints=(
            r"""Använd sfäriska källkoordinater med

$$
\begin{aligned}
\overline r^{\prime}
&=s(\sin\theta\cos\phi,\sin\theta\sin\phi,\cos\theta),\\
0\leq s\leq a,\quad &0\leq\theta\leq\pi,\quad0\leq\phi\leq2\pi.
\end{aligned}
$$

Laddningselementet blir

$$
\mathrm dQ^{\prime}
=A(a-s)s^2\sin\theta\,\mathrm ds\,\mathrm d\theta\,\mathrm d\phi.
$$""",
            r"""I centrum är

$$
\begin{aligned}
\overline r-\overline r^{\prime}&=-\overline r^{\prime},\\
|\overline r-\overline r^{\prime}|&=s.
\end{aligned}
$$

Sätt in detta och $\mathrm dQ^{\prime}$ i potentialintegralen. Vinkelintegralerna ger $4\pi$ eftersom återstoden är oberoende av vinklarna.""",
            r"""Det återstår

$$
V(0)=\frac{1}{\varepsilon_0}\int_0^a A(a-s)s\,\mathrm ds.
$$

Integrera de två potenstermerna. Utanför a är tätheten noll, så inget ytterligare källbidrag ska adderas.""",
        ),
        self_checks=(
            r"""Efter förenkling är integranden proportionell mot $s(a-s)$; den går mot noll i centrum trots faktorn $1/s$ i potentialkärnan.""",
            r'A har enheten $\mathrm{C/m^4}$. Potentialen ska skala som $Aa^3/\varepsilon_0$ och ha samma tecken som A. Symmetrin ger $\overline E(\overline 0)=0$, men inte $V(0)=0$.',
        ),
        common_pitfall=r'Att sätta $V(0)=0$ för att fältet är noll i centrum, eller ersätta hela fördelningen med en punktladdning när observationspunkten ligger inuti den.',
        geometry_hint=r"""Skilj på observationspunkten $\overline r=0$ och källskalets radie $\overline r^{\prime}$. Avståndet i Coulombpotentialen är $\overline r^{\prime}$; det är inte noll bara för att observationspunkten ligger i origo.""",
        setup_hint=r"""Identifiera

$$
\begin{aligned}
\mathrm dQ^{\prime}&=A(a-s)s^2\sin\theta\,\mathrm ds\,\mathrm d\theta\,\mathrm d\phi,\\
|\overline r-\overline r^{\prime}|&=s
\end{aligned}
$$

vid $\overline r=0$. Potentialkärnans $1/s$ lämnar faktorn s i radialintegralen efter vinkelintegrationen; integrera sedan från 0 till a.""",
    ),
    "InsertedMetalPlateCapacitor": G(
        problem_id="2.18",
        learning_goal="Skilja på vad som hålls konstant före och efter att batteriet kopplats bort.",
        concepts=("plattkondensator", "konstant laddning", "ledare i fält"),
        start_here=r'Skriv Gauss lag $\oint_S\overline{E}\cdot\mathrm d\overline{S}=\frac{Q_{\mathrm{in}}}{\varepsilon_0}$ och potentialskillnaden $\Delta V=-\int\overline E\cdot\mathrm d\overline\ell$. Identifiera plattladdningen, fältets riktning och de delar av gapet där fältet finns. Batteriet kopplas bort efter uppladdningen, så Q är därefter bevarad.',
        hint_titles=('Laddningen före frånkoppling', 'Spänningsfallet med metallplattan', 'Det alternativa försöket'),
        hints=(
            r"""Utan kanteffekter är fältet normalt mot plattorna och homogent i luftgapet. Gauss lag och spänningsintegralen ger, för beloppen,

$$
EA=\frac{Q}{\varepsilon_0},
\qquad U=E\,d_0.
$$

Kombinera ekvationerna för att bestämma $Q$.""",
            r'I del (b) behålls Q från (a), så luftfältet är oförändrat. Inuti den införda metallen är $E=0$. Beräkna spänningsintegralen över de två luftgapen, vars sammanlagda tjocklek är $d_0-d_1$.',
            r"""I del (c) görs ett separat försök utan metallplattan. Behåll samma Q och integrera luftfältet över det nya avståndet $d_2$. Plattorna bär $+Q$ och $-Q$ i alla tre fallen.""",
        ),
        self_checks=(
            r'I del (b) ska spänningen minska med faktorn $(d_0-d_1)/d_0$; i del (c) ska den öka med faktorn $d_2/d_0$. Båda jämförs med ursprungsspänningen.',
            r'Om $d_1\to0$ återfås ursprungsspänningen. Metallplattans placering i gapet ändrar inte resultatet i idealmodellen, så länge den inte vidrör elektroderna och kanteffekter försummas.',
        ),
        common_pitfall=r'Att hålla U konstant efter att batteriet kopplats bort, eller använda $d_2-d_1$ i del (c) trots att metallinsättning och ökat avstånd är alternativa försök.',
        geometry_hint=r"""Rita två separata skisser: (b) två luftgap plus en metallplatta, (c) ett enda luftgap med bredd $d_2$. Inuti metallen är potentialen konstant; bara luftgap bidrar till spänningsfallet.""",
        setup_hint=r'Lös först $EA=Q/\varepsilon_0$ tillsammans med $U=Ed_0$. Använd sedan samma $E=Q/(\varepsilon_0A)$ i $U_b=E(d_0-d_1)$ och $U_c=Ed_2$. Den införda metallens spänningsfall är noll.',
    ),
    "UniformSpaceChargePlates": G(
        problem_id="2.19",
        learning_goal=r"""Kombinera Gauss lag för en sluten box med potentialskillnaden och lokalisera fältets nollställe.""",
        concepts=('Gauss lag', 'plansymmetri', 'randvillkor'),
        start_here=r"""Skriv $\oint_S\overline E\cdot\mathrm d\overline S=Q_{\mathrm{in}}/\varepsilon_0$ och $V(d)-V(0)=-\int_0^d E_x\,\mathrm dx$. Välj $x=0$ vid plattan med potential $V_0$. Använd en sluten box i gapet för att bestämma skillnaden mellan fältet vid två positioner.""",
        hint_titles=('Flödet genom en box i gapet', 'Bestäm fältet vid den första plattan', 'Ligger nollstället i gapet?'),
        hints=(
            r"""Välj en box med tvärsnittsarea $A$ mellan $x=0^+$ och en punkt $x$ i gapet. Låt $C=E_x(0^+)$ vara det okända fältet precis utanför den första plattan. Plansymmetrin gör sidoytornas flöde noll. Gauss lag ger

$$
\begin{aligned}
\oint_S\overline E\cdot\mathrm d\overline S
&=A E_x(x)-AC,\\
Q_{\mathrm{in}}&=\rho_0Ax.
\end{aligned}
$$

Sätt flödet lika med $Q_{\mathrm{in}}/\varepsilon_0$ och lös efter fältet:

$$
E_x(x)=C+\frac{\rho_0x}{\varepsilon_0}.
$$

Boxen ligger i gapet och omsluter inte plattans ytladdning.""",
            r"""Använd potentialerna $V(0)=V_0$ och $V(d)=0$:

$$
\int_0^d E_x(x)\,\mathrm dx=V_0.
$$

Sätt in fältet från Gauss lag och bestäm $C=E_x(0^+)$. Molnets täthet bestämmer fältskillnaden; potentialskillnaden bestämmer också fältets nivå.""",
            r'För $\rho_0\neq0$, lös $E_x(x_0)=0$. Kräv därefter $0<x_0<d$ för ett nollställe strikt mellan plattorna; $x_0=0$ eller d är gränsfall på ytorna. Hantera $\rho_0=0$ separat.',
        ),
        self_checks=(
            r"""$E_x$ ska vara linjärt med lutningen $\rho_0/\varepsilon_0$ och dess integral över gapet ska vara $V_0$. Om $V_0=0$ och $\rho_0\neq0$ ligger nollpunkten mitt i gapet.""",
            r"""Villkoret för en inre nollpunkt blir

$$
|V_0|<\frac{|\rho_0|d^2}{2\varepsilon_0};
$$

likhet placerar nollpunkten på en yta. För $\rho_0=0$ måste fallet behandlas separat: $E_x=V_0/d$ är konstant och är noll överallt endast om $V_0=0$.""",
        ),
        common_pitfall=r'Att blanda ihop vilken platta som ligger vid $x=0$, eller rapportera en algebraisk nollpunkt utanför gapet som en fysisk lösning mellan plattorna.',
        geometry_hint=r"""Markera 0 vid $V_0$-plattan och d vid jord. Om du i stället mäter från den jordade plattan måste du omvandla koordinaten med $x_{\mathrm{ny}}=d-x$; samma fysiska punkt får då ett annat koordinatvärde.""",
        setup_hint=r"""Sätt

$$
E_x=\frac{\rho_0x}{\varepsilon_0}+C
$$

i

$$
\int_0^dE_x\,\mathrm dx=V_0
$$

och lös C. Sätt sedan det färdiga fältuttrycket lika med noll och pröva om lösningen ligger inne i gapet.""",
    ),

    # ------------------------------------------------------------------
    # Kapitel 3 – Dielektriska material
    # ------------------------------------------------------------------
    "HClDipoleField": G(
        problem_id="3.1",
        learning_goal="Se hur två motsatta punktladdningar övergår i dipolfält när observationsavståndet är stort.",
        concepts=("elektrisk dipol", "superposition", "fjärrfältsapproximation"),
        start_here='Skriv Coulombs lag för flera punktladdningar: E(r)=(1/4πε₀)Σ_i q_i(r−r_i)/|r−r_i|³. Identifiera laddningarna, deras positioner och separationsvektorerna för var och en av de två observationspunkterna.',
        hint_titles=('På molekylaxeln', 'Vinkelrätt mot axeln', 'Pröva fjärrfältsgränsen'),
        hints=(
            r"""Placera de två laddningarna på z-axeln:

$$
\begin{aligned}
q_+&=e,&\overline r_+&=(0,0,d/2),\\
q_-&=-e,&\overline r_-&=(0,0,-d/2).
\end{aligned}
$$

För punkten $\overline r=(0,0,r_0)$ är separationsvektorerna $(0,0,r_0-d/2)$ och $(0,0,r_0+d/2)$. Sätt in dem och deras belopp i summan.""",
            r"""För observationspunkten $\overline r=(0,r_0,0)$ blir separationsvektorerna $(0,r_0,-d/2)$ och $(0,r_0,d/2)$, med samma belopp:

$$
|\overline r-\overline r_\pm|=\sqrt{r_0^2+d^2/4}.
$$

Sätt in de signerade laddningarna och summera komponenterna innan du tar fältets belopp.""",
            r"""Beräkna beloppen i de två punkterna. Eftersom $d/r_0\ll1$ kan du även utveckla de exakta uttrycken och behålla första termen som inte försvinner. Omvandla $d=0{,}218\,\text{Å}$ och $r_0=10\,\text{Å}$ till meter före numerisk insättning.""",
        ),
        self_checks=(
            r"""Med dipolmoment $p=ed$ i positiv z-riktning ska fjärrfältet på positiva z-axeln peka längs p och på y-axeln motsatt p.""",
            r"""Båda beloppen ska avta som $1/r_0^3$. Axelfältet blir ungefär dubbelt så stort som ekvatorialfältet; detta är en fjärrfältsrelation, inte en exakt relation nära laddningarna.""",
        ),
        common_pitfall='Att addera de två fältbeloppen på z-axeln trots att bidragen är motriktade, eller anta att nettoladdning noll innebär fält noll.',
        geometry_hint=r"""Rita två separata observationspunkter: $(0,0,r_0)$ och $(0,r_0,0)$. Avståndet $r_0$ mäts från molekylens mittpunkt, inte från någon av jonerna.""",
        setup_hint=r"""Sätt

$$
k=\frac1{4\pi\varepsilon_0}.
$$

På z-axeln ger insättning

$$
E_z=ke\left[\frac1{(r_0-d/2)^2}-\frac1{(r_0+d/2)^2}\right].
$$

På y-axeln används samma vektorsumma med de två lika avstånden; laddningarnas tecken gör att y-bidragen försvinner och z-bidragen adderas.""",
    ),
    "PorcelainSlabCapacitor": G(
        problem_id="3.3",
        learning_goal="Använd randvillkor för D och spänningssumman över två seriekopplade materialskikt.",
        concepts=("D-fält", "dielektrikum", "seriekopplade skikt"),
        start_here='Skriv Gauss lag ∮_S D·n dS=Q_fri,in, materiallagen D=εE och potentialskillnaden ΔV=−∫E·dl. Identifiera materialens permittiviteter, skikttjocklekarna och eventuell fri laddning på gränsen.',
        hint_titles=('Randvillkoret mellan skikten', 'Material och tjocklekar', 'Summera spänningsfallen'),
        hints=(
            r"""Försumma kanteffekter: fälten är normala mot plattorna. En tunn Gaussbox över luft–porslin-gränsen ger

$$
(D_{\mathrm{porslin},n}-D_{\mathrm{luft},n})S=0.
$$

Detta beror på att ingen fri gränsladdning finns. Sätt det gemensamma fältbeloppet till D.""",
            r"""Identifiera

$$
\begin{aligned}
\varepsilon_{\mathrm{luft}}&=\varepsilon_0,\\
\varepsilon_{\mathrm{porslin}}&=6\varepsilon_0
\end{aligned}
$$

och

$$
d_{\mathrm{luft}}=d_{\mathrm{porslin}}=0{,}005\,\mathrm m.
$$

Materiallagen ger fälten i respektive material:

$$
E_{\mathrm{luft}}=\frac D{\varepsilon_0},\qquad
E_{\mathrm{porslin}}=\frac D{6\varepsilon_0}.
$$""",
            r"""Sätt in fälten i spänningsintegralen:

$$
10^4\,\mathrm V=E_{\mathrm{luft}}d_{\mathrm{luft}}+E_{\mathrm{porslin}}d_{\mathrm{porslin}}.
$$

Lös efter D och beräkna därefter båda E-beloppen.""",
        ),
        self_checks=(
            r"""$E_{\mathrm{luft}}/E_{\mathrm{porslin}}$ ska vara 6, medan D är samma i båda skikten. D har enheten C/m² och E har enheten V/m.""",
            r"""Spänningsfallen ska summera till 10 kV. Om $\varepsilon_r$ sätts till 1 ska modellen ge det homogena fältet $U/d$.""",
        ),
        common_pitfall=r"""Att fördela spänningen lika bara för att skikten är lika tjocka, eller kräva kontinuitet för $E_n$ när det är $D_n$ som är kontinuerligt.""",
        geometry_hint='Materialgränsen är parallell med metallplattorna. En väg från den ena plattan till den andra passerar båda materialen; potentialfallen adderas som för seriekopplade skikt.',
        setup_hint=r"""Gaussboxen ger ett gemensamt D. Sätt $E_i=\frac D{\varepsilon_i}$ i $U=\sum_i E_i d_i$, så att

$$
D=\frac U{d_{\mathrm{luft}}/\varepsilon_0+d_{\mathrm{porslin}}/(\varepsilon_0\varepsilon_r)}.
$$

Använd sedan materiallagen för respektive skikt.""",
    ),
    "GroundedInnerSphereChargeSplit": G(
        problem_id="3.6",
        learning_goal="Kombinera Gauss lag, laddningskonservering och ett jordningsvillkor för en flerledargeometri.",
        concepts=("jordad ledare", "sfärisk symmetri", "dielektrikum"),
        start_here='Skriv ∮_S D·n dS=Q_fri,in och V(a)=∫_a^∞ E_r dr=0 för den jordade kulan. Inför laddningarna q på kulan samt q_in och q_ut på skalets sidor. Identifiera innesluten fri laddning och permittivitet i varje radialområde.',
        hint_titles=('Vilka laddningar är bevarade?', 'Fälten innanför och utanför skalet', 'Använd jordningsvillkoret'),
        hints=(
            r"""Sfärisk symmetri ger ett radiellt fält. En Gaussyta inne i skalets metall, där $E=0$, ger

$$
q+q_{\mathrm{in}}=0.
$$

Det isolerade skalets laddning är bevarad:

$$
q_{\mathrm{in}}+q_{\mathrm{ut}}=Q.
$$

Den jordade kulans q är däremot okänd.""",
            r"""I gapet ger $4\pi r^2D_r=q$ och

$$
D=\varepsilon_0\varepsilon_rE.
$$

Utanför skalet ger

$$
4\pi r^2D_r=q+Q=q_{\mathrm{ut}}
$$

och $D=\varepsilon_0E$. Lös efter $E_r$ separat i båda områdena.""",
            r"""Sätt in fälten i jordningsvillkoret

$$
0=\int_a^{3a}E_{\mathrm{gap}}\,\mathrm dr
+\int_{3a}^{\infty}E_{\mathrm{ut}}\,\mathrm dr.
$$

Ersätt q med $-q_{\mathrm{in}}$, lös efter $q_{\mathrm{ut}}/q_{\mathrm{in}}$ och sätt sist $\varepsilon_r=2{,}5$.""",
        ),
        self_checks=(
            'Laddningarna på skalets båda sidor ska summera till Q, och den beräknade potentialen på den inre kulan ska vara noll.',
            r"""Kvoten $q_{\mathrm{ut}}/q_{\mathrm{in}}$ ska vara $2/\varepsilon_r$ för denna geometri, alltså 0,8 vid $\varepsilon_r=2{,}5$. För $Q>0$ är båda skalytorna positivt laddade och den jordade kulan negativ.""",
        ),
        common_pitfall='Att bevara laddningen på den jordade kulan, eller använda en enda permittivitet i en potentialintegral som går genom både dielektrikum och vakuum.',
        geometry_hint='Dela den radiella integrationsvägen vid 3a. Jordningen gäller kulan vid a, inte det yttre skalet. Hålet och tråden försummas enligt uppgiftens antagande om sfärisk symmetri.',
        setup_hint=r"""Identifiera $Q_{\mathrm{fri,in}}=q$ i gapet och $q_{\mathrm{ut}}$ utanför. Efter Gauss lag och potentialintegrationen blir

$$
0=\frac q{4\pi\varepsilon_0\varepsilon_r}\left(\frac1a-\frac1{3a}\right)+\frac{q_{\mathrm{ut}}}{4\pi\varepsilon_0\,3a}.
$$

Kombinera med $q=-q_{\mathrm{in}}$, inte med bevarad laddning på den jordade kulan.""",
    ),
    "ChargedDielectricShell": G(
        problem_id="3.7",
        learning_goal="Lösa E och V styckvis i en sfäriskt symmetrisk geometri med både vakuum och dielektrikum.",
        concepts=("Gauss lag för D", "styckvis medium", "potentialkontinuitet"),
        start_here='Skriv ∮_S D·n dS=Q_fri,in, D=εE och V(r)=∫_r^∞ E_r(s) ds. Identifiera sfärisk symmetri, innesluten laddning och permittivitet för r<a, a<r<b och r>b. Här behandlas ρ0 som fri rymdladdningstäthet, i enlighet med facit.',
        hint_titles=('Innesluten fri laddning', 'Från D till E i varje område', 'Integrera inåt från oändligheten'),
        hints=(
            r"""Tolka $\rho_0$ som fri laddningstäthet enligt facit. Välj en sfärisk Gaussyta. D är radiellt och konstant på ytan, så flödet är

$$
\oint_S\overline D\cdot\mathrm d\overline S=4\pi r^2D_r.
$$

Beräkna

$$
Q_{\mathrm{fri,in}}=\int\rho_0\,\mathrm dV:
$$

den är 0 i hålrummet, $\frac{4\pi\rho_0(r^3-a^3)}3$ i materialet och $\frac{4\pi\rho_0(b^3-a^3)}3$ utanför.""",
            r"""Använd

$$
4\pi r^2D_r=Q_{\mathrm{fri,in}}.
$$

och lös efter $D_r$ i varje område. Sätt sedan

$$
E_r=\frac{D_r}{\varepsilon_0\varepsilon_r}
$$

i materialet och

$$
E_r=\frac{D_r}{\varepsilon_0}
$$

i vakuum.""",
            r"""Integrera fältet med $V(\infty)=0$. Bestäm först V(b) från det yttre fältet och använd sedan

$$
V(r)=V(b)+\int_r^b E_{\mathrm{material}}(s)\,\mathrm ds.
$$

I hålrummet är $E=0$, så V är konstant och lika med V(a).""",
        ),
        self_checks=(
            r"""V ska vara kontinuerlig vid a och b och uppfylla

$$
-\frac{\mathrm dV}{\mathrm dr}=E_r
$$

inom varje område. $E=0$ i hålrummet betyder inte att V där är noll.""",
            r"""Vid b ska

$$
\varepsilon_0\varepsilon_r E_r(b^-)=\varepsilon_0 E_r(b^+).
$$

Utanför är fältet oberoende av $\varepsilon_r$ när den fria laddningen hålls fast; för $\varepsilon_r=1$ försvinner permittivitetssprånget.""",
        ),
        common_pitfall=r"""Att tolka $\rho_0$ som total laddningstäthet samtidigt som Gauss lag för D används, eller sätta potentialens integrationskonstant separat till noll i varje område.""",
        geometry_hint='Rita en sfärisk Gaussyta i varje region. I skalet omsluts bara material mellan a och observationsradien r; vakuumhålet bidrar inte med laddning.',
        setup_hint=r"""Gör en tabell med område, $Q_{\mathrm{fri,in}}$ och $\varepsilon$. Sätt in varje rad i

$$
E_r=\frac{Q_{\mathrm{fri,in}}}{4\pi\varepsilon r^2},
$$

där $\varepsilon$ är områdets absoluta permittivitet. Dela potentialintegralen vid materialgränserna och behåll samma referens $V(\infty)=0$.""",
    ),
    "DielectricFilledSphericalGap": G(
        problem_id="3.9",
        learning_goal="Använd ett gränsvillkor geometriskt: E är tangentiellt mot gränsytan mellan de två dielektrika.",
        concepts=("randvillkor", "E och D", "sfärisk Gaussyta"),
        start_here='Skriv Gauss lag ∮_S D·n dS=Q_fri,in, D_i=ε₀ε_iE_i och randvillkoret E_1t=E_2t. Identifiera hur en sfärisk Gaussyta delas mellan materialen. Uppgiften tillåter att E antas radiellt.',
        hint_titles=('Fältet vid skiljeplanet', 'Flödet genom två halvklot', 'Bestäm fälten i materialen'),
        hints=(
            r"""Materialen fyller var sitt halvklot, inte två radiella lager. Det radiella E-fältet är tangentiellt mot skiljeplanet, så $E_{1r}=E_{2r}=E_r$ vid samma radie. D-beloppen kan däremot vara olika.""",
            r"""En sfärisk Gaussyta i $a<r<b$ omsluter den fria laddningen +Q. Vardera materialet täcker arean $2\pi r^2$, och D är normalt mot Gaussytan. Flödet blir

$$
\Phi_D=2\pi r^2D_{1r}+2\pi r^2D_{2r}.
$$""",
            r"""Använd följande materialrelationer:

$$
D_{1r}=\varepsilon_0\varepsilon_1E_r,\qquad
D_{2r}=\varepsilon_0\varepsilon_2E_r.
$$

Sätt in dem i flödesekvationen och sätt summan lika med $Q$. Lös efter $E_r$ och beräkna sedan D i respektive halva.""",
        ),
        self_checks=(
            r"""När

$$
\varepsilon_1=\varepsilon_2
$$

ska resultatet bli det vanliga fältet i en homogent fylld sfärisk kondensator. $D_{1r}/D_{2r}$ ska vara $\varepsilon_1/\varepsilon_2$.""",
            r"""Det totala D-flödet genom sfären ska vara Q. Utanför det yttre skalet är fältet noll i denna idealmodell eftersom ledarnas totala laddning är $+Q-Q=0$.""",
        ),
        common_pitfall=r"""Att behandla halvorna som två radiella serielager eller sätta $D_{1r}=D_{2r}$. Radialriktningen är tangent till materialgränsen men normal till Gaussytan.""",
        geometry_hint='Rita skiljeplanet genom centrum och en radiell pil längs planet. Jämför med en sfärisk Gaussyta: samma pil har olika relation till normalerna på de två olika ytorna.',
        setup_hint=r"""Använd först $E_{1t}=E_{2t}$ vid skiljeplanet. Gauss lag ger därefter

$$
Q=2\pi r^2\varepsilon_0(\varepsilon_1+\varepsilon_2)E_r.
$$

Arean är $2\pi r^2$ per material; det gemensamma $E_r$ får tas ut ur respektive flödesintegral.""",
    ),
    "MakrofolCapacitorDesign": G(
        problem_id="3.11",
        learning_goal="Dimensionera först mot genomslag och därefter mot önskad kapacitans.",
        concepts=("genomslag", "plattkondensator", "dimensionering"),
        start_here='Skriv C=Q/U, Gauss lag ∮_S D·n dS=Q_fri,in, D=ε₀εrE och ΔV=−∫E·dl. Identifiera total isoleringstjocklek nt och villkoret |E|≤E_genomslag. Först bestäms antalet skikt, sedan arean.',
        hint_titles=('Fältet genom flera skikt', 'Välj ett helt antal skikt', 'Bestäm plattarean'),
        hints=(
            r"""I plattmodellen utan kanteffekter är E homogent och normalt mot plattorna. Spänningsintegralen ger $U=Ent$. För $n$ skikt med tjocklek $t$ krävs

$$
\frac U{nt}\le E_{\mathrm{genomslag}}.
$$

Lös sedan villkoret efter $n$.""",
            r"""Lös

$$
n\geq\frac{U}{E_{\mathrm{genomslag}}t}
$$

och avrunda uppåt till heltal. Sätt $U=50\,\mathrm{kV}$, $t=0{,}10\,\mathrm{mm}$ och

$$
E_{\mathrm{genomslag}}=200\,\mathrm{kV/mm}
$$

i förenliga enheter.""",
            r"""En Gaussbox vid en elektrod ger $DA=Q$ och materiallagen ger

$$
D=\varepsilon_0\varepsilon_rE.
$$

Kombinera med $U=Ent$ och $C=\frac QU$:

$$
C=\frac{\varepsilon_0\varepsilon_r A}{nt}.
$$

Lös A för det valda heltalet n och $C=100\,\mathrm{pF}$.""",
        ),
        self_checks=(
            'Kontrollera att n skikt klarar 50 kV men n−1 inte gör det. Ett avrundat antal får aldrig ge högre fält än genomslagsgränsen.',
            'A ska ha enheten m² och öka med total tjocklek vid given C. Uppgiften söker idealmodellens minimum, utan extra säkerhetsmarginal.',
        ),
        common_pitfall=r"""Att använda den oavrundade minimitjockleken i areaberäkningen, eller förväxla kV/mm med V/m:

$$
1\,\mathrm{kV/mm}=10^6\,\mathrm{V/m}.
$$""",
        geometry_hint='Skikten staplas i fältriktningen mellan samma två elektroder; deras tjocklekar adderas. Hela gapet antas fyllt, så inga luftskikt ska läggas in i modellen.',
        setup_hint=r"""Sätt först in tjockleken nt i

$$
U=\int E\,\mathrm d\ell=Ent
$$

och tillämpa genomslagsvillkoret. När n är valt, använd

$$
Q=\varepsilon_0\varepsilon_r EA
$$

i $C=\frac QU$ för att få

$$
A=\frac{Cnt}{\varepsilon_0\varepsilon_r}.
$$""",
    ),
    "CoaxialTwoDielectricCapacitance": G(
        problem_id="3.12",
        learning_goal="Bygga kapacitansen för två koaxiella dielektriska skikt genom att summera potentialfall.",
        concepts=("koaxial kondensator", "D-fält", "seriekopplade dielektrika"),
        start_here='Skriv ∮_S D·n dS=Q_fri,in, D_i=ε₀ε_iE_i, U=∫_a^c E_R dR och C/L=ρℓ/U. Identifiera cylindersymmetrin, laddningen per längd ρℓ och materialgränsen mellan de två lika tjocka isolationslagren.',
        hint_titles=('Gaussytan och materialgränsen', 'Två potentialintegraler', 'Kapacitans per längd'),
        hints=(
            r"""Lika radiell tjocklek ger $b=\frac{a+c}2$. Välj en koaxial Gauss-cylinder med radie R och längd L. D är radiellt, ändytornas flöde är noll och

$$
Q_{\mathrm{fri,in}}=\rho_\ell L,
$$

så

$$
D_R\,2\pi RL=\rho_\ell L.
$$""",
            r"""Lös efter $D_R$ och använd

$$
E_i=\frac{D_R}{\varepsilon_0\varepsilon_i}.
$$

Sätt upp spänningsintegralen som

$$
U=\int_a^bE_{1R}\,\mathrm dR+
\int_b^cE_{2R}\,\mathrm dR.
$$

varje del ger en logaritm av en radiekvot.""",
            r"""Bilda $\frac CL=\frac{\rho_\ell}U$ med den beräknade spänningen. $\rho_\ell$ ska förkortas bort. Sätt in $a=0{,}020\,\mathrm m$, $c=0{,}050\,\mathrm m$, $\varepsilon_1=4$ och $\varepsilon_2=3$ först när uttrycket är klart.""",
        ),
        self_checks=(
            r"""Om

$$
\varepsilon_1=\varepsilon_2=\varepsilon_r
$$

ska logaritmerna summeras till $\ln(c/a)$, vilket ger den vanliga koaxialkapacitansen per längd.""",
            r"""Svaret ska ha enheten F/m. Vid b är $D_n$ kontinuerligt men

$$
\frac{E_R(b^+)}{E_R(b^-)}=\frac{\varepsilon_1}{\varepsilon_2};
$$

lika tjocka lager behöver inte ha lika spänningsfall.""",
        ),
        common_pitfall=r"""Att förväxla kapacitans C med kapacitans per längdenhet $C/L$, eller använda det geometriska medelvärdet $\sqrt{ac}$ för två lika tjocka lager.""",
        geometry_hint=r"""R mäts från cylinderaxeln. Material 1 fyller $a<R<b$ och material 2 fyller $b<R<c$. Fältet passerar materialen i följd och är normalt mot deras cylindriska gränsyta.""",
        setup_hint=r"""Gauss lag ger

$$
D_R=\frac{\rho_\ell}{2\pi R}.
$$

Insättning i de två potentialintegralerna ger

$$
U=\frac{\rho_\ell}{2\pi\varepsilon_0}\left[\frac{\ln(b/a)}{\varepsilon_1}+\frac{\ln(c/b)}{\varepsilon_2}\right].
$$

Använd sedan definitionen $\frac CL=\frac{\rho_\ell}U$.""",
    ),
    "BreakdownVoltageCases": G(
        problem_id="3.13",
        learning_goal="Skilja mellan homogen isolering och två material i serie när genomslagsfält begränsar spänningen.",
        concepts=("genomslagsfält", "D-kontinuitet", "serielager"),
        start_here='Skriv ΔV=−∫E·dl, D=εE och Gauss lag ∮_S D·n dS=Q_fri,in. Identifiera material och tjocklek i varje fall. Bestäm fälten i lagren innan du tillämpar respektive villkor |E_i|≤E_i,max.',
        hint_titles=('Ett homogent material', 'Två lokala genomslagsvillkor', 'Summera tillåten spänning'),
        hints=(
            r"""Utan kanteffekter är fältet homogent i ett enda material. För (a) och (b) ger spänningsintegralen $U=Ed$ med $d=10\,\mathrm{mm}$. Sätt E lika med genomslagsgränsen för det material som fyller hela gapet.""",
            r"""I (c) ger en Gaussbox över den oladdade materialgränsen samma $D_n$ i båda lagren. Därför är fältrelationerna

$$
E_{\mathrm{luft}}=\frac D{\varepsilon_0},\qquad
E_{\mathrm{plexi}}=\frac D{\varepsilon_0\varepsilon_r}.
$$

Kräv både $D\leq\varepsilon_0E_{\mathrm{luft,max}}$ och $D\leq\varepsilon_0\varepsilon_rE_{\mathrm{plexi,max}}$.""",
            r"""Välj den mindre tillåtna D-nivån, beräkna båda E-beloppen och sätt in dem i

$$
U_{\max}=E_{\mathrm{luft}}\,(1\,\mathrm{mm})+
E_{\mathrm{plexi}}\,(9\,\mathrm{mm}).
$$

Båda fältgränserna måste vara uppfyllda samtidigt.""",
        ),
        self_checks=(
            'Vid den valda spänningen måste båda fältgränserna vara uppfyllda och minst en vara nådd. Med uppgiftens värden begränsar luftgapet.',
            'Om ett material saknas helt används det kvarvarande materialets gräns. Ett mycket tunt men kvarvarande luftgap kan fortfarande begränsa fältet; gränsen när tjockleken går mot noll behöver inte vara värdet när luften helt tagits bort.',
        ),
        common_pitfall='Att addera båda materialens maximala spänningsfall utan att först kontrollera att fälten kan uppfylla D-kontinuitet samtidigt.',
        geometry_hint='Luft och plexiglas ligger efter varandra i fältriktningen. I del (c) återstår bara 1 mm luft, men fältet där är tre gånger fältet i plexiglaset.',
        setup_hint=r"""I ett material används

$$
U_{\max}=E_{\max}d.
$$

I två lager begränsas det gemensamma $D$-beloppet av båda materialen. Beräkna gränserna var för sig:

$$
\begin{aligned}
D_{\mathrm{luft,max}}&=\varepsilon_0E_{\mathrm{luft,max}},\\
D_{\mathrm{plexi,max}}&=\varepsilon_0\varepsilon_rE_{\mathrm{plexi,max}}.
\end{aligned}
$$

Välj den mindre av dem som $D_{\max}$. Beräkna sedan fälten och summera spänningsfallen:

$$
E_i=\frac{D_{\max}}{\varepsilon_i},
\qquad U=\sum_i E_i d_i.
$$

Addera inte två oberoende maxspänningar.""",
    ),
    "DielectricSlabCapacitor": G(
        problem_id="3.14",
        learning_goal="Knyta ihop D-kontinuitet, spänningsfall, fri ytladdning och polarisationsladdning.",
        concepts=("D-fält", "polarisation", "randvillkor"),
        start_here='Skriv ∮_S D·n dS=Q_fri,in, D=εE och ΔV=−∫E·dl. För bundna laddningar behövs dessutom P=ε₀(εr−1)E och ρ_sp=P·n. Identifiera skikten och deras normaler; välj z uppåt från jord till plattan med V0>0.',
        hint_titles=('Fälten i skikten', 'Fri laddning på metallen', 'Bunden laddning på dielektrikumet'),
        hints=(
            r"""I den plana modellen ger en Gaussbox utan fri gränsladdning samma $D_n$ i luft och dielektrikum. Fälten pekar nedåt. För beloppen gäller

$$
\begin{aligned}
E_{\mathrm{luft}}&=\frac D{\varepsilon_0},\\
E_{\mathrm{diel}}&=\frac D{\varepsilon_0\varepsilon_r}.
\end{aligned}
$$

Sätt in tjocklekarna i

$$
V_0=E_{\mathrm{luft}}\,(0{,}2d)+
E_{\mathrm{diel}}\,(0{,}8d).
$$

och lös D.""",
            r"""En Gaussbox från metallens inre till gapet ger

$$
\rho_s=\overline D\cdot\hat n,
$$

där n pekar från metallen ut i gapet. Använd det beräknade D-fältet: den övre plattans fria laddning är positiv och den undres negativ.""",
            r"""Beräkna $\overline P$ som vektor i dielektrikumet och använd sambandet

$$
\rho_{sp}=\overline P\cdot\hat n.
$$

Normalen pekar ut ur just dielektrikumet. Dess övre normal är $+\hat z$ och den undre $-\hat z$. Använd inte metallens normal i detta steg.""",
        ),
        self_checks=(
            r"""För $\varepsilon_r=1$ ska $E=\frac{V_0}d$ i hela gapet och den bundna laddningen försvinna. D är kontinuerligt genom materialgränsen även när E har ett språng.""",
            r"""För $\varepsilon_r>1$ blir den bundna laddningen negativ på dielektrikumets övre yta och positiv på dess undre; de summerar till noll. De fria elektrodladdningarna har motsatta tecken.""",
        ),
        common_pitfall='Att använda metallens normal när du räknar dielektrikumets bundna laddning, eller blanda ihop fältbelopp med den negativa z-komponenten.',
        geometry_hint=r"""Dielektrikumet fyller $0<z<0{,}8d$. Dess övre normal är $+\hat z$ och dess undre $-\hat z$. På den övre metallplattans undersida är normalriktningen i stället $-\hat z$.""",
        setup_hint=r"""Lös D ur

$$
V_0=Dd\left[\frac{0{,}2}{\varepsilon_0}+\frac{0{,}8}{\varepsilon_0\varepsilon_r}\right].
$$

Sätt $E_z=-E$ och

$$
P_z=-\varepsilon_0(\varepsilon_r-1)E_{\mathrm{diel}}.
$$

Beräkna sedan

$$
\rho_s=\overline D\cdot\hat n
$$

på metallen och

$$
\rho_{sp}=\overline P\cdot\hat n
$$

på dielektrikumet med respektive utåtnormal.""",
    ),
    "ElectretCylinderAxis": G(
        problem_id="3.18",
        learning_goal="Ersätta en homogen polarisation med dess bundna laddningar och sedan använda superposition.",
        concepts=("elektret", "bunden laddning", "fält från skiva"),
        start_here=r"""Bestäm den bundna laddningen med $Q_{p,\mathrm{in}}=-\oint_S\overline P\cdot\mathrm d\overline S$ och ytladdningen med $\rho_{sp}=\overline P\cdot\hat n$. För homogen polarisation ger varje sluten yta helt inne i materialet noll nettoflöde. Använd sedan Coulombintegralen för ändytornas laddningar och $\overline D=\varepsilon_0\overline E+\overline P$.""",
        hint_titles=('Vilka ytor bär laddning?', 'Parametrisera varje skiva', 'Addera de axiella fälten', 'Jämför elektret och fria laddningar'),
        hints=(
            r"""För en sluten yta helt inne i det homogent polariserade materialet gäller

$$
Q_{p,\mathrm{in}}=-\oint_S\overline P\cdot\mathrm d\overline S=0.
$$

Konstant $\overline P$ ger lika stora, motriktade flödesbidrag. Eftersom detta gäller varje sådan delvolym finns ingen bunden volymladdning. Vid materialets ytor används

$$
\rho_{sp}=\overline P\cdot\hat n.
$$

Manteln har noll ytladdning. Botten vid $z=0$ har normal $-\hat z$ och $\rho_{sp}=-P$; toppen vid $z=h$ har normal $+\hat z$ och $\rho_{sp}=+P$.""",
            r"""För vardera skivan vid $z_0=0$ eller $h$: välj $\overline r=(0,0,z)$ och

$$
\overline r'=(R\cos\phi,R\sin\phi,z_0).
$$

Laddningselementet är

$$
\mathrm dQ^{\prime}=\rho_{sp}R\,\mathrm dR\,\mathrm d\phi
$$

Då är

$$
\begin{aligned}
\overline r-\overline r^{\prime}&=(-R\cos\phi,-R\sin\phi,z-z_0),\\
|\overline r-\overline r^{\prime}|&=\sqrt{R^2+(z-z_0)^2}.
\end{aligned}
$$

Integrera över $0\leq R\leq a$ och $0\leq\phi\leq2\pi$ och addera skivbidragen.""",
            r"""Vinkelintegrationen tar bort tvärkomponenterna. Radialintegralen ger följande fält utanför skivytan:

$$
E_{\mathrm{skiva},z}=
\frac{\rho_{sp}}{2\varepsilon_0}
\left[
\operatorname{sgn}(z-z_0)
-\frac{z-z_0}{\sqrt{(z-z_0)^2+a^2}}
\right].
$$

Summera med rätt $\rho_{sp}$ och $z_0$; skriv resultatet i områdena $z<0$, $0<z<h$ och $z>h$.""",
            r"""Använd

$$
\overline D=\varepsilon_0\overline E+P\hat z
$$

inne i elektreten och $D=\varepsilon_0E$ utanför. Ta därefter den plana gränsen $a\gg h$ nära ändytornas centrala delar. I del (d) är $\pm P$ fria skivladdningar, inte materialpolarisation, så där används $D=\varepsilon_0E$ överallt.""",
        ),
        self_checks=(
            r"""$E_z$ ska ha rätt språng $\rho_{sp}/\varepsilon_0$ över varje ändyta, medan $D_z$ är kontinuerligt eftersom det inte finns fri ytladdning. Använd ensidiga gränsvärden på ytorna.""",
            r"""I den plana gränsen är

$$
\overline E\approx-\frac P{\varepsilon_0}\hat z
$$

inne och ungefär noll utanför, medan $\overline D\approx0$ för elektreten. Fria skivladdningar ger samma E men

$$
\overline D=\varepsilon_0\overline E,
$$

alltså $\overline D\approx-P\hat z$ mellan skivorna.""",
        ),
        common_pitfall=r"""Att anta $\overline D=0$ bara för att fri laddning saknas. Gauss lag ger då $\oint_S\overline D\cdot\mathrm d\overline S=0$: nettoflödet är noll, men fältet behöver inte vara noll. Den plana approximationen gäller inte godtyckligt långt från en ändlig cylinder.""",
        geometry_hint=r"""Rita utåtnormal $-\hat z$ på botten och $+\hat z$ på toppen. Vid $z=0$ och h är E diskontinuerligt, så ange vilken sida du menar. Villkoret $a\gg h$ gör centralområdet ungefär plant, men långt bort måste den ändliga kroppens fält avta.""",
        setup_hint=r"""Beräkna först den bundna ytladdningen på varje ändyta:

$$
\rho_{sp}=\overline P\cdot\hat n.
$$

För en skiva vid $z_0$ är bidraget

$$
E_{z_0,z}(z)=\frac{\rho_{sp}(z_0)}{2\varepsilon_0}
\int_0^a\frac{R(z-z_0)}{[R^2+(z-z_0)^2]^{3/2}}\,\mathrm dR.
$$

Summera de två skivbidragen innan du bestämmer $\overline D$:

$$
\begin{aligned}
E_z(z)&=E_{0,z}(z)+E_{h,z}(z),\\
\overline D&=\varepsilon_0\overline E+\overline P.
\end{aligned}
$$

Använd den lokala polarisationen i rätt område. Vid ändytorna används ensidiga gränsvärden.""",
    ),
    "ObliqueConductorDielectricBoundary": G(
        problem_id="3.19",
        learning_goal="Bestäm fältets riktning från ledarrandvillkoret och geometrin hos ett snett plan.",
        concepts=("ledarrandvillkor", "ytladdning", "normalvektor"),
        start_here='Skriv randvillkoren n·(D_2−D_1)=ρs och E_2t=E_1t tillsammans med D_2=ε₀εrE_2. I ledaren är E_1=0; en Gaussbox ger då D_2·n=ρs. Identifiera enhetsnormalen från ledaren mot dielektrikumet innan du sätter in uppgiftens geometri.',
        hint_titles=('Bestäm enhetsnormalen', 'Fältets tillåtna komponenter', 'Sätt in den signerade ytladdningen'),
        hints=(
            r"""Planet beskrivs av

$$
f(x,y)=\frac xa+\frac yb-1=0.
$$

Ledaren innehåller origo, alltså sidan $f<0$. Normalen mot medium 2 är

$$
\hat n=\frac{\nabla f}{|\nabla f|}=\frac{(b,a,0)}{\sqrt{a^2+b^2}},
$$

eftersom $a,b>0$.""",
            r"""Tangentialvillkoret ger $E_{2t}=0$. I det isotropa dielektrikumet är $\overline D_2$ parallellt med $\overline E_2$, så skriv $\overline D_2=D_n\hat n$. Gaussboxen ger $D_n=\rho_s$.""",
            r"""Sätt in normalen i $\overline D_2=\rho_s\hat n$ och använd sedan

$$
\overline E_2=\frac{\overline D_2}{\varepsilon_0\varepsilon_r}.
$$

Behåll tecknet på den fria ytladdningen; negativ $\rho_s$ vänder båda vektorerna.""",
        ),
        self_checks=(
            'Enhetsnormalen ska ha längd 1 och vara vinkelrät mot tangenten (a,−b,0). Ingen z-komponent ska finnas.',
            r"""För $a=b$ ska normalens x- och y-komponenter vara lika. D har belopp $|\rho_s|$; vid given fri ytladdning minskar E med ökande $\varepsilon_r$.""",
        ),
        common_pitfall='Att använda skärningsvektorn (a,b,0) som normal, glömma normaliseringen eller anta att den fria ytladdningen är noll eftersom dielektrikumets volymladdning är noll.',
        geometry_hint='Punkterna (a,0) och (0,b) ligger på linjen i xy-snittet; linjen är parallell med vektorn (a,−b). Ledaren innehåller origo, vilket avgör vilken av de två normalriktningarna som ska väljas.',
        setup_hint=r"""Identifiera först normalen

$$
\hat n=\frac{(b,a,0)}{\sqrt{a^2+b^2}}.
$$

Sätt $\overline D_2=D_n\hat n$ i

$$
\overline D_2\cdot\hat n=\rho_s
$$

och använd $\hat n\cdot\hat n=1$. Materiallagen ger sedan $\overline E_2$; $\rho_s$ är fri ytladdning även om fri volymladdning saknas.""",
    ),
    # ------------------------------------------------------------------
    # Kapitel 4 – Energi, kraft och spegelladdning
    # ------------------------------------------------------------------
    "SphericalShellChargingEnergy": G(
        problem_id="4.1",
        learning_goal="Förstå uppladdningsarbete som en successiv process där potentialen ändras medan laddningen byggs upp.",
        concepts=("elektrostatisk energi", "potential", "uppladdningsarbete"),
        start_here=(
            'Skriv uppladdningsarbetet W=∫ V(q) dq, med potentialreferens vid oändligheten. Identifiera den föränderliga laddningen q och potentialen som den skapar. Bygg upp laddningen från ett neutralt skal. När en liten laddning dq förs in från oändligheten är skalets laddning q, inte redan slutladdningen Q.'
        ),
        hint_titles=('Potentialen under uppladdning', 'Arbetet för nästa laddningselement', 'Integrera över laddningen'),
        hints=(
            r"""Med $V(\infty)=0$ har det ledande skalet potentialen

$$
V(q)=\frac q{4\pi\varepsilon_0a}.
$$

Den är konstant över skalytan men ökar i belopp under uppladdningen.""",
            r"""Det yttre arbetet för nästa lilla laddning är

$$
\mathrm dW=V(q)\,\mathrm dq.
$$

vid långsam uppladdning. Summan av dessa bidrag blir en integral från $q=0$ till $q=Q$.""",
            r"""Integrera q-beroendet och jämför med

$$
W=\frac{Q^2}{2C},\qquad C=4\pi\varepsilon_0a.
$$

En ensam sfär har $C=4\pi\varepsilon_0a$. Alternativt kan du integrera fältenergitätheten $\frac{\varepsilon_0E^2}2$ utanför skalet.""",
        ),
        self_checks=(
            r"""Arbetet ska vara positivt för både positiv och negativ slutladdning och vara proportionellt mot $Q^2$. För $Q=0$ är arbetet noll.""",
            r"""Vid fast Q minskar arbetet när a ökar. Kontrollera också

$$
\frac{\mathrm dW}{\mathrm dQ}=V(Q);
$$

faktorn 1/2 hör till det totala arbetet, inte till det sista lilla laddningssteget.""",
        ),
        common_pitfall=r"""Att använda slutpotentialen för hela laddningen och skriva $W=QV(Q)$, vilket räknar allt arbete som om skalet redan var fulladdat.""",
        geometry_hint=r"""Skalet är en ensam sfär med radie a, med potentialreferens vid oändligheten. Fältet är noll inuti och finns för $r>a$; blanda inte ihop skalradien a med integrationsradien r i en alternativ fältenergiberäkning.""",
        setup_hint=r"""Skriv

$$
W=\int_0^Q\frac q{4\pi\varepsilon_0a}\,\mathrm dq.
$$

Håll radien konstant och låt q vara integrationsvariabel. För $Q<0$ är både potentialen och laddningsstegen negativa, men arbetet blir fortfarande positivt.""",
    ),
    "ParallelPlateForceDistance": G(
        problem_id="4.2",
        learning_goal="Koppla den elektriska fältenergin eller det elektriska trycket till den mekaniska kraften mellan kondensatorplattor.",
        concepts=("elektriskt tryck", "plattkondensator", "kraft"),
        start_here='Skriv kraftbalansen ΣF=0 och det elektrostatiska trycket p=ε₀E²/2 vid en metallyta i luft. Identifiera arean i F=pA och bestäm gapfältet från ΔV=−∫E·dl, utan kanteffekter. Betrakta den givna kraften som beloppet av den yttre kraft som balanserar plattornas attraktion. Använd fältet i luftgapet för att bestämma det elektriska trycket.',
        hint_titles=('Fältet från spänningen', 'Från tryck till kraft', 'Lös efter avståndet'),
        hints=(
            r"""I plattkondensatorapproximationen, utan kanteffekter, är fältbeloppet $E=\frac{|V|}d$. Spänningen 450 V avser potentialskillnaden mellan plattorna.""",
            r"""Det elektriska trycket är

$$
p=\frac{\varepsilon_0E^2}{2}.
$$

Multiplicera med A för kraften. Faktorn 1/2 kan förstås genom att en platta påverkas av den andra plattans fält, inte av sitt eget.""",
            r"""Sätt kraftbeloppet lika med $0{,}05\,\mathrm N$ och lös efter det positiva avståndet d. Omvandla $50\,\mathrm{cm^2}$ till $0{,}005\,\mathrm{m^2}$ innan du sätter in talen.""",
        ),
        self_checks=(
            r"""Sätt tillbaka ditt d i $\frac{\varepsilon_0AV^2}{2d^2}$ och kontrollera att kraften blir den givna. Attraktionen ändras inte om spänningens tecken vänds.""",
            r"""Vid given V och A ska större efterfrågad kraft ge mindre d, med d proportionellt mot $1/\sqrt F$. Avståndet bör vara litet jämfört med plattornas sidomått för att kanteffekter ska kunna försummas.""",
        ),
        common_pitfall=r"""Att skriva $F=QE$ med hela gapfältet och därmed få dubbla kraften, eller derivera enbart fältenergin vid konstant V utan att räkna med spänningskällans energiutbyte.""",
        geometry_hint='Markera en pil inåt för den elektriska kraften på varje platta och en lika stor pil utåt för den kraft som håller dem isär. d är vinkelrätt avstånd mellan plattorna; A är en plattas yta, inte summan av bådas.',
        setup_hint=r"""Skriv

$$
F=\frac{\varepsilon_0A}2\left(\frac Vd\right)^2
$$

och isolera $d^2$ innan du tar den positiva roten. Tryckmetoden gäller för det aktuella tillståndet utan att du behöver anta hur en strömkälla kopplas vid en senare förflyttning.""",
    ),
    "CopperFoilLevitationEbonite": G(
        problem_id="4.3",
        learning_goal="Använd randvillkor mellan luft och dielektrikum för att koppla elektriskt tryck till tyngdkraft.",
        concepts=("dielektrikum", "elektriskt tryck", "kraftjämvikt"),
        start_here=(
            'Utgå från ΣF=0, elektriskt tryck p=ε₀E_luft²/2 och randvillkoret D_luft,n=D_diel,n utan fri gränsladdning. Identifiera tyngden per area och vilket fält som verkar på metallen. Skriv kraftbalansen per area för kopparblecket: elektriskt tryck uppåt ska balansera tyngden ρ_Cu t g nedåt. Då förkortas den okända plattarean bort.'
        ),
        hint_titles=('Trycket på blecket', 'Koppla samman fälten', 'Använd kraftbalansen'),
        hints=(
            r"""Kraften på blecket bestäms av luftfältet precis utanför metallen:

$$
p_{\mathrm{el}}=\frac{\varepsilon_0E_{\mathrm{luft}}^2}2.
$$

Det infinitesimala luftgapet är därför viktigt även om dess spänningsfall är försumbart.""",
            r"""Utan fri laddning på luft–ebonitgränsen är $D_n$ kontinuerligt. Därmed gäller

$$
\varepsilon_0E_{\mathrm{luft}}
=\varepsilon_0\varepsilon_rE_{\mathrm{ebonit}}.
$$""",
            r"""När luftgapets tjocklek går mot noll blir $U\approx E_{\mathrm{ebonit}}d$. Kombinera detta med

$$
p_{\mathrm{el}}=\rho_{\mathrm{Cu}}tg.
$$

och lös efter minsta spänningsbelopp som balanserar tyngden.""",
        ),
        self_checks=(
            r"""Sätt in ditt U och kontrollera att

$$
\frac{\varepsilon_0}2\left(\frac{\varepsilon_rU}d\right)^2=\rho_{\mathrm{Cu}}tg.
$$

Båda leden ska ha enheten N/m².""",
            r"""Större t eller $\rho_{\mathrm{Cu}}$ ska kräva större spänning, proportionellt mot kvadratroten. Kraftbalansen visar att folien kan hållas uppe i idealmodellen, inte att en fritt svävande jämvikt är stabil.""",
        ),
        common_pitfall=r"""Att använda $U/d$ som luftfält eller ta bort luftgapet innan kraften bestämts. $U/d$ är ebonitfältet i gränsen av ett mycket tunt luftgap.""",
        geometry_hint='Rita i ordning: övre metallbelägg, ebonit med tjocklek d, ett mycket tunt luftgap och kopparfolie med tjocklek t. Det är luftfältet vid foliens övre yta som ger trycket; d och t har olika roller.',
        setup_hint=r"""Lös först $E_{\mathrm{luft}}$ ur

$$
\frac{\varepsilon_0E_{\mathrm{luft}}^2}2=\rho_{\mathrm{Cu}}tg
$$

och använd sedan

$$
U\approx\frac{dE_{\mathrm{luft}}}{\varepsilon_r}.
$$

Sätt $d=0{,}02\,\mathrm m$, $t=10^{-4}\,\mathrm m$ och

$$
\rho_{\mathrm{Cu}}=8{,}9\times10^3\,\mathrm{kg/m^3}.
$$""",
    ),
    "ThundercloudEnergyEstimate": G(
        problem_id="4.5",
        learning_goal="Göra en ordningsstorleksmodell av ett åskmoln som en plattkondensator och koppla genomslagsfält till laddning och energi.",
        concepts=("plattkondensator", "genomslagsfält", "fältenergi"),
        start_here='Skriv ∮E·n dS=Q_in/ε₀ och W_e=∫ ε₀E²/2 dV. Identifiera laddningsytans area, gapets volym och det givna genomslagsfältet i plattmodellen. Följ uppgiftens modell med negativ molnbas och positiv mark som två stora plattor. Låt Q beteckna laddningsbeloppet, så att molnets signerade laddning är −Q.',
        hint_titles=('Laddningen från gapfältet', 'Omvandla de givna enheterna', 'Från energitäthet till energi'),
        hints=(
            r"""I plattmodellen är E normalt mot ytorna och homogent i gapet. En Gaussbox från markens ledande inre till gapet ger

$$
EA=\frac Q{\varepsilon_0}.
$$

Lös efter laddningsbeloppet Q med $E=E_{\max}$.""",
            r"""Omvandla först $A=1\,\mathrm{km^2}$ till $10^6\,\mathrm{m^2}$ och

$$
E_{\max}=20\,000\,\mathrm{V/cm}
$$

till $2\times10^6\,\mathrm{V/m}$. Bestäm sedan Q från fältet.""",
            r"""Beräkna energin med

$$
W_e=\frac{\varepsilon_0E_{\max}^2Ah}{2}.
$$

Kontrollera genom $C=\frac{\varepsilon_0A}h$, spänningsbelopp $U=E_{\max}h$ och

$$
W_e=\frac{CU^2}2=\frac{QU}2.
$$""",
        ),
        self_checks=(
            r"""De två energiberäkningarna ska stämma och ge joule. Energin är positiv även om molnets laddning är negativ; använd laddnings- och spänningsbelopp i $QU/2$.""",
            r"""Vid fast $E_{\max}$ och area är Q oberoende av h, medan U och $W_e$ växer linjärt med h. Detta är en idealiserad kondensatoruppskattning, inte en detaljerad modell av ett verkligt åskmoln.""",
        ),
        common_pitfall=r"""Att missa faktorn 100 när V/cm omvandlas till V/m, eller använda ensamplattans

$$
E=\frac{\rho_s}{2\varepsilon_0}
$$

när båda plattornas fält bidrar.""",
        geometry_hint=r"""Marken är vid $z=0$ och molnbasen vid $z=h$. Fältet pekar uppåt från markens +Q till molnets −Q, medan potentialen minskar uppåt. A är en ytas area och ska inte dubbleras.""",
        setup_hint=r"""Skriv $Q=\varepsilon_0AE_{\max}$ och

$$
W_e=\frac{\varepsilon_0E_{\max}^2}2Ah.
$$

Skilj energitätheten i J/m³ från den totala energin i J; volymen i modellen är Ah.""",
    ),
    "CylindricalCapacitorDielectricPullIn": G(
        problem_id="4.6",
        learning_goal="Beräkna en dielektrisk indragningskraft genom hur kapacitansen ändras med inskjutningslängden.",
        concepts=("energimetod", "kapacitans", "dielektrisk kraft"),
        start_here=(
            'Skriv energibalansen dW_källa=dW_fält+F_x dx, med dW_källa=V0 dQ, W_fält=CV0²/2 och Q=CV0. Identifiera vilken geometrisk storhet som ändrar C och vad spänningskällan håller konstant. Låt x öka när hålcylindern dras in längs metallrörens axel. Spänningskällan är ansluten och håller V0 konstant; både kondensatorns laddning och dess fältenergi kan därför ändras.'
        ),
        hint_titles=('Dela upp den aktiva längden', 'Kapacitansens ändring', 'Källans arbete och kraften'),
        hints=(
            r"""Dela upp en aktiv längd L i en fylld del x och en luftfylld del $L-x$. Delarna har samma spänning mellan samma elektroder och deras kapacitanser adderas parallellt.""",
            r"""Kapacitansen per längd för den fyllda respektive tomma delen är

$$
\frac{2\pi\varepsilon_0\varepsilon_r}{\ln(b/a)}
\qquad\text{och}\qquad
\frac{2\pi\varepsilon_0}{\ln(b/a)}.
$$

Skriv C(x) och beräkna $\frac{\mathrm dC}{\mathrm dx}$.""",
            r"""Vid konstant $V_0$ tillför källan

$$
\mathrm dW_{\text{källa}}=V_0\,\mathrm dQ=V_0^2\,\mathrm dC.
$$

Fältenergin ökar med

$$
\mathrm dW_{\text{fält}}=\frac{V_0^2}2\,\mathrm dC.
$$

Resten blir mekaniskt arbete $F_x\,\mathrm dx$; använd detta för att få kraften och dess riktning.""",
        ),
        self_checks=(
            r"""För $\varepsilon_r>1$ ska kraften peka inåt, mot större x och större C. Den ska försvinna när $\varepsilon_r=1$ eller $V_0=0$ och vara oförändrad om spänningens tecken vänds.""",
            'Kraften blir oberoende av x medan både fylld och tom del finns och kapacitansen kan approximeras som linjär i x. Nära full inskjutning eller långt utanför gäller inte denna konstanta kraftmodell.',
        ),
        common_pitfall=r"""Att använda

$$
F_x=-\frac{\mathrm d}{\mathrm dx}\left(\frac{CV_0^2}2\right)
$$

vid konstant spänning och få fel tecken. Fältenergin ensam är inte den mekaniska potentialenergin när källan utbyter energi med systemet.""",
        geometry_hint=r"""Hålcylindern fyller hela radialgapet $a<r<b$ men bara en del av längden. Rörelsen är axiell, inte radiell. Kraften verkar vid övergången till fylld del; energimetoden ger nettokraften utan att fransfältet behöver lösas i detalj.""",
        setup_hint=r"""Skriv

$$
C(x)=\frac{2\pi\varepsilon_0[L+(\varepsilon_r-1)x]}{\ln(b/a)}.
$$

Kombinera $\frac{\mathrm dC}{\mathrm dx}$ med

$$
F_x=\frac{V_0^2}2\frac{\mathrm dC}{\mathrm dx}.
$$

L försvinner ur kraften; logaritmens argument $b/a$ är dimensionslöst.""",
    ),
    "PointChargeConductingPlane": G(
        problem_id="4.7",
        learning_goal="Använd spegelladdningsmetoden både för inducerad ytladdning och för kraften på en punktladdning.",
        concepts=("spegelladdning", "ledarvillkor", "inducerad ytladdning"),
        start_here=(
            'Skriv V(r)=Σ_i q_i/(4πε₀|r−r_i|), E=−∇V och ρ_s=ε₀E_n omedelbart utanför ledaren. Identifiera en hjälpladdning som gör V=0 på planet; därefter kan ytladdningen integreras och kraften beräknas. Välj planet z=0 och den verkliga laddningen q vid z=a. Använd den idealisering med ett oändligt plan på noll potential som ligger bakom appens modell och facit; spegelladdningen är ett hjälpmedel utanför det fysiska området.'
        ),
        hint_titles=('Placera spegelladdningen', 'Bestäm integrationsradien', 'Integrera laddningen och bestäm kraften'),
        hints=(
            r"""Placera −q vid $z=-a$. Potentialbidragen tar ut varandra på $z=0$. Fältet i det övre halvrummet är då den sökta lösningen, men fältet inne i den verkliga ledaren är noll.""",
            r"""För del (a): b mäts från kulan, inte från dess lodräta projektion på planet. Punkter i planet på avstånd högst b från kulan bildar en skiva med radie

$$
R_{\max}=\sqrt{b^2-a^2}.
$$

Bestäm

$$
\rho_s(R)=\varepsilon_0E_z(R,0^+)
$$

med normal $+\hat z$.""",
            r"""Integrera den inducerade laddningen med ringelement

$$
\mathrm dS=2\pi R\,\mathrm dR.
$$

från 0 till $R_{\max}$. Låt sedan $b\to\infty$ för del (b). I del (c) används enbart spegelladdningens fält vid q, med avståndet 2a.""",
        ),
        self_checks=(
            r"""När $b\to a^+$ ska den integrerade laddningen gå mot noll, eftersom skivan krymper till en punkt. När $b\to\infty$ ska den gå mot −q.""",
            r"""Den inducerade laddningen har motsatt tecken mot q. Kraften är riktad nedåt och dess belopp är proportionellt mot $q^2/a^2$, oberoende av avståndsgränsen b.""",
        ),
        common_pitfall='Att integrera till radien b i planet, vilket motsvarar ett annat område än uppgiften frågar efter. Förväxla inte heller kraften med energin: kraften fås direkt från bilden, men bildparets fulla Coulombenergi är inte systemets verkliga energi.',
        visualization_note="Här kan en geometrisk bild av verklig laddning, spegelladdning och fältlinjer vara mer pedagogisk än en generell fältkarta.",
        geometry_hint='Rita en rätvinklig triangel med höjden a, sträckan R i planet och hypotenusan b från kulan till skivans kant. Skivan ligger i planet; i ett vertikalt snitt syns den som en sträcka, inte som en cirkel runt origo.',
        setup_hint=r"""Fältets normaldel ger

$$
\rho_s(R)=-\frac{qa}{2\pi(R^2+a^2)^{3/2}}.
$$

Skriv

$$
Q_{\mathrm{ind}}=\int_0^{\sqrt{b^2-a^2}}\rho_s(R)\,2\pi R\,\mathrm dR
$$

och använd $u=R^2+a^2$. För kraften: använd Coulombs lag mellan q och −q på avstånd 2a, utan extra faktor 2.""",
    ),

    # ------------------------------------------------------------------
    # Kapitel 5 – Strömmar och strömtäthet
    # ------------------------------------------------------------------
    "ConductiveCoaxialElectrodes": G(
        problem_id="5.1",
        learning_goal="Översätta det välkända koaxiala E-fältet till stationär ström genom ett ledande medium.",
        concepts=("Ohms lag i punktform", "koaxial geometri", "ström"),
        start_here='Skriv I=∫J·n dS, J=σE och ΔV=−∫E·dl. Identifiera strömmens riktning, tvärsnittsarean vid varje radie och integrationsgränserna. Välj U=V(a)−V(b) och positiv ström radiellt utåt. I stationärt tillstånd passerar samma ström varje cylindrisk yta mellan elektroderna; ändeffekter försummas.',
        hint_titles=('Arean som strömmen passerar', 'Integrera det radiella fältet', 'Lös efter strömmen'),
        hints=(
            r"""En strömyta med radie R och längd $\ell$ har arean $2\pi R\ell$. Strömkonservering ger därför

$$
J_R=\frac I{2\pi R\ell}.
$$

strömtätheten är inte konstant i gapet.""",
            r"""Använd $E_R=\frac{J_R}{\sigma}$ och skriv

$$
U=\int_a^bE_R\,\mathrm dR.
$$

Den radiella integralen ger $\ln(b/a)$.""",
            r"""Lös ut I och jämför med $I=\frac U{R_{\mathrm{el}}}$. Konduktivitet $\sigma$ mäts i S/m och är inversen till resistiviteten; blanda inte ihop dessa materialstorheter.""",
        ),
        self_checks=(
            r"""Produkten $2\pi R\ell J_R$ ska vara samma för varje R. Vid $U>0$ pekar både E och J utåt; negativ U vänder riktningen.""",
            r"""Resistansen ska vara positiv och oberoende av U. Vid $U=0$ är strömmen noll men resistansen fortfarande ändlig. En längre cylinder ger större ledande yta och därmed större ström vid samma spänning.""",
        ),
        common_pitfall='Att behandla strömmen som om den gick längs cylinderns längd eller använda samma tvärsnittsarea över hela radialgapet. I den resistiva vätskan kan E vara skilt från noll även när strömmen är stationär.',
        geometry_hint=r"""Rita två koncentriska cirklar och en radiell strömpil från inner- till ytterledare för $U>0$. Den strömyta du använder är cylinderns mantelyta $2\pi R\ell$, inte ändytan $\pi R^2$.""",
        setup_hint=r"""Sätt

$$
U=I\int_a^b\frac{\mathrm dR}{2\pi\sigma\ell R}
$$

och lös efter I. Håll isär radialkoordinaten R och resistansen $R_{\mathrm{el}}$. Om U definieras tvärtom måste den signerade strömriktningen ändras.""",
    ),
    "CoaxialCableLeakage": G(
        problem_id="5.2",
        learning_goal="Beräkna läckström och effektförlust genom ett resistivt koaxialt isolationsskikt.",
        concepts=("resistivitet", "koaxial resistans", "Joulevärme"),
        start_here='Skriv dR_el=ρ dℓ/S, I=V/R_el och P=VI. Identifiera strömvägens längdelement och den area som strömmen passerar vid varje radie. Läckströmmen går genom isolationen från innerledare till skärm, alltså radiellt. Modellera varje tunt radiellt skikt som en resistans i serie med nästa.',
        hint_titles=('Ett tunt resistivt skikt', 'Gränser från diametrarna', 'Läckström och effekt'),
        hints=(
            r"""För ett skikt på radie R med tjocklek dR är strömvägens längd dR och tvärsnittsarean $2\pi R\ell$. Skriv

$$
\mathrm dR_{\mathrm{el}}=\frac{\rho\,\mathrm dR}{2\pi R\ell}.
$$

där $\rho$ här är resistivitet i Ω m.""",
            r"""Uppgiften anger diametrarna a och b. Integrera från $a/2$ till $b/2$; logaritmen blir

$$
\ln\!\left(\frac{b/2}{a/2}\right)=\ln(b/a).
$$

Om du senare beräknar lokala fält måste du ändå använda faktiska radier.""",
            r"""Med resistansen bestämd fås $I=\frac V{R_{\mathrm{el}}}$ och

$$
P=VI=\frac{V^2}{R_{\mathrm{el}}}.
$$

Sätt $\ell=1{,}50\,\mathrm m$, $V=120\,\mathrm V$ och

$$
\rho=5{,}0\times10^6\,\Omega\,\mathrm m;
$$

avrunda först i slutet.""",
        ),
        self_checks=(
            'Läckströmmen ska bli ungefär 0,16 mA och effekten ungefär 20 mW. P har enheten watt, inte energi i joule.',
            'Om V byter tecken byter I tecken men P är oförändrad och icke-negativ. Dubbel kabellängd ger dubbel läckström och effekt, eftersom fler strömvägar kopplas parallellt.',
        ),
        common_pitfall=r"""Att använda kabelns längd som strömvägens längd i $\rho\ell/A$, eller dubblera/halvera bara den ena diametern i logaritmen.""",
        geometry_hint=r"""Rita ett tvärsnitt med innerledarradie $a/2$ och skärmens innerradie $b/2$. Radialskikten ligger i serie; olika bitar längs kabeln erbjuder däremot parallella läckvägar mellan samma två ledare.""",
        setup_hint=r"""Skriv

$$
R_{\mathrm{el}}=\frac{\rho\ln(b/a)}{2\pi\ell}.
$$

Använd sedan samma $R_{\mathrm{el}}$ i både $I=\frac V{R_{\mathrm{el}}}$ och

$$
P=\frac{V^2}{R_{\mathrm{el}}}.
$$

Resistiviteten $\rho$ i detta problem är inte en laddningstäthet.""",
    ),
    "VariableSigmaCoaxialElectrolyte": G(
        problem_id="5.7",
        learning_goal=r"""Hantera stationär ström vid varierande konduktivitet och bestämma fri rymdladdning från Gauss lag.""",
        concepts=("kontinuitet", "variabel konduktivitet", "Gauss lag"),
        start_here=r"""Skriv $I=\int_S\overline J\cdot\mathrm d\overline S$, $\overline J=\sigma(R)\overline E$ och $\oint_S\overline D\cdot\mathrm d\overline S=Q_{\mathrm{fri,in}}$. Samma stationära ström passerar varje koaxial cylinderyta. Välj $U=V(a)-V(b)$ och bestäm först fältet från strömmen och potentialintegralen. Använd sedan en sluten skalformad Gaussyta inne i elektrolyten.""",
        hint_titles=('Hur varierar J och E med radien?', 'Bestäm resistansen', 'Laddningen i ett cylindriskt skal'),
        hints=(
            r"""Samma I passerar varje cylindrisk yta: $J_R=\frac I{2\pi R\ell}$. Sätt därefter

$$
E_R=\frac{J_R}{\sigma(R)},\qquad
\sigma(R)=\frac{k}{R^2}.
$$

Fältet blir proportionellt mot R även om strömtätheten avtar som $1/R$.""",
            r"""Integrera

$$
U=\int_a^b E_R\,\mathrm dR
$$

och identifiera $R_{\mathrm{el}}=\frac UI$. Du kan också integrera

$$
\mathrm dR_{\mathrm{el}}=\frac{\mathrm dR}{\sigma(R)2\pi R\ell}.
$$""",
            r"""För del (b), välj ett slutet cylindriskt skal med radier $R_1,R_2$ helt inne i elektrolyten och längd $L$. Med $\varepsilon=\varepsilon_0\varepsilon_r$ ger Gauss lag

$$
\begin{aligned}
Q_{\mathrm{fri,in}}
&=\oint_S\overline D\cdot\mathrm d\overline S\\
&=2\pi L\varepsilon\left[R_2E_R(R_2)-R_1E_R(R_1)\right].
\end{aligned}
$$

Ändytorna ger inget flöde. Sätt in fältet från (a) och dividera laddningen med skalvolymen $\pi(R_2^2-R_1^2)L$. Om kvoten är densamma för alla skal är den också den lokala laddningstätheten.""",
        ),
        self_checks=(
            r"""Strömmen $2\pi R\ell J_R$ ska vara densamma vid varje radie. Kontrollera också att laddningen från Gauss lag är proportionell mot skalvolymen, så att den fria volymladdningstätheten är konstant.""",
            r"""Med den valda definitionen är $\rho_{\mathrm{fri}}$ positiv för $U>0$ och byter tecken när U vänds. Vid fast U är $\rho_{\mathrm{fri}}$ oberoende av k, medan I är proportionell mot k. k har enheten S·m.""",
        ),
        common_pitfall=r"""Att sätta laddningstätheten till noll för att strömmen är stationär, eller glömma flödet genom skalets inre mantel. Dess utåtnormal är $-\hat R$, så det bidraget ska subtraheras.""",
        geometry_hint=r"""Observationsradien R löper genom elektrolyten $a<R<b$. Föreställ dig två cylindriska strömytor: den större har större area och därför lägre $J_R$, samtidigt som dess lägre $\sigma$ kräver ett större $E_R$.""",
        setup_hint=r"""Sätt in fältet från potentialintegralen,

$$
E_R(R)=\frac{2UR}{b^2-a^2},
$$

i Gauss lag för skalet:

$$
Q_{\mathrm{fri,in}}=
\frac{4\pi\varepsilon_0\varepsilon_rUL}{b^2-a^2}(R_2^2-R_1^2).
$$

Dividera med $\pi(R_2^2-R_1^2)L$. Resultatet är oberoende av skalets radier. Stationaritet betyder att lika mycket ström går in som ut ur varje sluten volym, inte att volymen saknar laddning.""",
        visualization_note='Jämför de separata vyerna för E_R, J_R och fri laddningstäthet. Försök förklara hur σ(R)=k/R² kan ge olika radialberoenden för E och J samtidigt som totalströmmen är densamma genom varje cylinderyta.',
    ),
    "SemicylindricalRingResistor": G(
        problem_id="5.10",
        learning_goal="Beräkna resistans i en geometri där strömvägens längd beror på radien och olika radiala skikt ligger parallellt.",
        concepts=("cylindriska koordinater", "strömfördelning", "parallella strömvägar"),
        start_here='Skriv dG=σ dS/ℓ_bana och R_el=1/G. Identifiera längden och tvärsnittet för en strömbana och avgör vilka banor som har samma potentialskillnad. Betrakta en tunn halvcirkelformad strömbana mellan radierna R och R+dR. Alla sådana banor går mellan samma kontaktytor A och B och ligger elektriskt parallellt.',
        hint_titles=('Längd och tvärsnitt för en bana', 'Summera konduktanser', 'Kontrollera med strömflödet'),
        hints=(
            r"""Banans längd är $\pi R$ och dess tvärsnittsarea vinkelrätt mot strömmen är $h\,\mathrm dR$. Skriv dess konduktans

$$
\mathrm dG=\frac{\sigma h}{\pi R}\,\mathrm dR.
$$

så att parallellkopplingen blir enkel.""",
            'Integrera dG från a till b och invertera först den totala konduktansen för att få resistansen. Radierna beskriver vilka banor som finns, inte strömmens riktning.',
            r"""Som alternativ kontroll: sätt $V(A)-V(B)=U$ och låt vinkeln öka från A till B. Då är

$$
E_\phi=\frac{U}{\pi R}.
$$

Integrera $J_\phi=\sigma E_\phi$ över en radiell snittyta med areaelement $h\,\mathrm dR$ för att få I.""",
        ),
        self_checks=(
            r"""Större $\sigma$ eller h ska minska resistansen. När $b\to a^+$ går den ledande tvärsnittsarean mot noll och resistansen mot oändligheten.""",
            r"""För en tunn ring, $b-a\ll a$, ska resultatet närma sig $\frac{\pi a}{\sigma h(b-a)}$, alltså längd delat med konduktivitet gånger tvärsnittsarea. Den inre banan har större J än den yttre vid samma U.""",
        ),
        common_pitfall='Att addera banornas resistanser som om de låg i serie, eller behandla strömmen som radiell mellan inner- och ytterytan. Här går den längs halvcirklarna mellan A och B.',
        visualization_note="En enkel tvärsnittsskiss med flera parallella halvcirkelformade strömvägar är mer informativ än en färgkarta över J.",
        geometry_hint='I tvärsnittet är A och B de två raka radialytorna vid halvringens ändar. Rita flera halvcirklar mellan dem. h är höjden vinkelrätt mot denna bild och ingår i varje banas tvärsnittsarea.',
        setup_hint=r"""Skriv

$$
G=\int_a^b\frac{\sigma h}{\pi R}\,\mathrm dR
$$

och sedan $R_{\mathrm{el}}=1/G$. Skilj konduktans G i siemens från materialets konduktivitet $\sigma$ i S/m.""",
    ),
    "SteadyCurrentInterfaceCharge": G(
        problem_id="5.15",
        learning_goal="Kombinera stationär strömkontinuitet med elektrostatikens randvillkor för att hitta fri ytladdning i ett materialgränsskikt.",
        concepts=("randvillkor", "J=σE", "ytladdning"),
        start_here='Skriv J_1n=J_2n, E_1t=E_2t, J_i=σ_iE_i och ρ_s=n·(D_2−D_1). Identifiera normalen, de givna strömkomponenterna och materialkonstanterna. Välj normalen n=+x̂ från medium 1 (x<0) till medium 2 (x>0). Dela J1=αx̂+βŷ i normal och tangentiell del innan du använder randvillkoren.',
        hint_titles=('Normal strömkomponent', 'Tangentiell fältkomponent', 'Ytladdningen från D'),
        hints=(
            r"""Stationärt tillstånd innebär att ingen ytterligare ytladdning ansamlas:

$$
J_{2x}=J_{1x}=\alpha.
$$

Det utesluter inte en redan etablerad, tidsoberoende ytladdning. Ohms lag ger

$$
\begin{aligned}
E_{1x}&=\frac\alpha{\sigma_1},\\
E_{2x}&=\frac\alpha{\sigma_2}.
\end{aligned}
$$""",
            r"""Det stationära elektriska fältets tangentiella komponent är kontinuerlig:

$$
E_{2y}=E_{1y}=\frac\beta{\sigma_1}.
$$

Därför är

$$
J_{2y}=\frac{\sigma_2\beta}{\sigma_1};
$$

hela J-vektorn behöver inte vara kontinuerlig.""",
            r"""Använd Gauss randvillkor

$$
\rho_s=D_{2x}-D_{1x}
=\varepsilon_0(\varepsilon_2E_{2x}-\varepsilon_1E_{1x}).
$$

För del (b), sök materialvillkoret som gör detta noll även när en normal ström passerar gränsen.""",
        ),
        self_checks=(
            r"""Ytladdningen ska vara oberoende av $\beta$ och ha enheten C/m². Den byter tecken om $\alpha$ byter tecken med samma normalriktning.""",
            r"""För $\alpha\ne0$ krävs

$$
\frac{\varepsilon_1}{\sigma_1}=\frac{\varepsilon_2}{\sigma_2}
$$

för noll ytladdning. Om $\alpha=0$ är ytladdningen noll oavsett materialkvoterna; identiska material är ett annat enkelt kontrollfall.""",
        ),
        common_pitfall=r"""Att kräva kontinuitet för $E_n$ eller hela J. Här är $J_n$ och $E_t$ kontinuerliga, medan språnget i $D_n$ bestämmer den fria ytladdningen.""",
        geometry_hint=r"""Gränsen är yz-planet: x är normalriktning och y är tangentriktning. En liten Gaussbox ger D-språnget över gränsen, medan en tunn rektangulär slinga ger kontinuitet för $E_y$.""",
        setup_hint=r"""Skriv

$$
\begin{aligned}
\overline E_1&=\left(\frac\alpha{\sigma_1},\frac\beta{\sigma_1},0\right),\\
\overline E_2&=\left(\frac\alpha{\sigma_2},\frac\beta{\sigma_1},0\right).
\end{aligned}
$$

Sätt endast x-komponenterna i

$$
\rho_s=\varepsilon_0(\varepsilon_2E_{2x}-\varepsilon_1E_{1x}).
$$

$\varepsilon_1$ och $\varepsilon_2$ används här som relativa permittiviteter, som i appen och facit.""",
    ),

    # ------------------------------------------------------------------
    # Kapitel 6 – Biot–Savarts lag
    # ------------------------------------------------------------------
    "FiniteWireBiotSavart": G(
        problem_id="6.1",
        learning_goal="Härleda fältet från en ändlig rak ledare och se hur Biot–Savart, vektorpotential och Ampères lag hänger ihop.",
        concepts=("Biot–Savarts lag", "vektorpotential", "Ampères lag"),
        start_here='Skriv Biot–Savarts lag B(r)=μ₀I/(4π)∫ dℓ′×(r−r′)/|r−r′|³. Identifiera dℓ′, separationsvektorn, dess belopp och gränserna. För potentialvägen används A(r)=μ₀I/(4π)∫dℓ′/|r−r′| och B=∇×A. Beräkna bidraget från det raka segmentet −L<z′<L, med ström i +z-riktningen. Uppgiften anger att segmentet är en del av en sluten krets; returledningens bidrag ingår inte här.',
        hint_titles=(
            r"""Del (a) · Identifiera integralens delar""",
            r"""Del (a) · Integrera och ta gränsvärdet""",
            r"""Del (b) · Beräkna först vektorpotentialen""",
            r"""Del (b) · Ta rotationen av det beräknade fältet""",
            r"""Del (c) · Välj Ampereslingan""",
            r"""Del (c) · Förenkla cirkulationsintegralen""",
        ),
        hints=(
            r"""Utgå från Biot–Savarts integral i startlagen. Låt källpunkten löpa längs segmentet i strömriktningen:

$$
\begin{aligned}
\overline r'&=z'\hat z,\qquad -L\leq z'\leq L,\\
\mathrm d\overline\ell'&=\mathrm dz'\,\hat z,\\
\overline r-\overline r'&=R\hat R+(z-z')\hat z,\\
|\overline r-\overline r'|&=\sqrt{R^2+(z-z')^2}.
\end{aligned}
$$

Observationskoordinaterna $R,z$ hålls fasta; $z'$ är integrationsvariabeln.""",
            r"""Beräkna korsprodukten innan du integrerar:

$$
\mathrm d\overline\ell'\times(\overline r-\overline r')
=R\,\mathrm dz'\,\hat\phi.
$$

Biot–Savart ger därför segmentbidraget

$$
B_\phi(R,z)=\frac{\mu_0IR}{4\pi}
\int_{-L}^L\frac{\mathrm dz'}{[R^2+(z-z')^2]^{3/2}}.
$$

Använd exempelvis $u=z'-z$ och sätt in båda gränserna. Ta först därefter $L\to\infty$, som också efterfrågas i del (a).""",
            r"""Börja om från vektorpotentialens källintegral:

$$
\overline A(\overline r)=\frac{\mu_0I}{4\pi}
\int\frac{\mathrm d\overline\ell'}{|\overline r-\overline r'|}.
$$

Återanvänd linjeelementet och avståndet från (a). Alla linjeelement pekar i $z$-riktningen, så segmentet ger bara $A_z$:

$$
A_z(R,z)=\frac{\mu_0I}{4\pi}
\int_{-L}^L\frac{\mathrm dz'}{\sqrt{R^2+(z-z')^2}}.
$$

Beräkna integralen först. I (b) får du sätta $z=0$, men behåll $R$ som variabel eftersom nästa steg kräver dess radialberoende.""",
            r"""När $\overline A$ är beräknat används metodens andra steg:

$$
\overline B=\nabla\times\overline A.
$$

Här är $A_R=A_\phi=0$ och $A_z$ oberoende av $\phi$. Rotationen i cylindriska koordinater reduceras därför till

$$
\overline B=-\frac{\partial A_z}{\partial R}\,\hat\phi.
$$

Derivera ditt färdiga uttryck för $A_z(R,0)$ och jämför med Biot–Savartresultatet vid $z=0$. Rotationssteget är sambandet som gör om den beräknade vektorpotentialen till magnetfält.""",
            r"""I (c) är ledaren oändligt lång redan från början. Utgå från

$$
\oint_C\overline B\cdot\mathrm d\overline\ell=\mu_0I_{\mathrm{in}}.
$$

Välj en cirkel med radie $R$ kring ledaren. Den oändliga ledarens symmetri gör fältet azimutalt och dess komponent $B_\phi$ lika stor över hela cirkeln. Den omslutna strömmen är $I$.""",
            r"""Skriv linjeelementet på cirkeln som $\mathrm d\overline\ell=R\,\mathrm d\phi\,\hat\phi$. Då blir

$$
\int_0^{2\pi}B_\phi(R)R\,\mathrm d\phi
=2\pi R B_\phi(R)=\mu_0I.
$$

Lös efter $B_\phi$ och jämför med gränsvärdet i (a). Ampères lag gäller det fullständiga stationära strömsystemets fält. För ett ändligt segment kan du inte tillskriva enbart segmentbidraget hela den omslutna strömmen och bortse från returledningen.""",
        ),
        self_checks=(
            r"""Vid $z=0$ ska de två ändpunktsbidragen vara lika. För $L\gg R,|z|$ ska resultatet närma sig $\frac{\mu_0I}{2\pi R}$; vid $I=0$ blir fältet noll.""",
            r"""Segmentets $B_\phi$ är oberoende av azimutvinkeln även när L är ändlig. Tecknet vänds om I vänds. $A_z$ kan få en divergent additiv konstant när $L\to\infty$, trots att B förblir ändligt.""",
        ),
        common_pitfall='Att förklara Ampèreproblemet med att ett ändligt segment saknar rotationssymmetri. Segmentbidraget har sådan symmetri, men Ampères magnetostatiska lag gäller den fullständiga stationära strömkretsens fält, inte ett öppet segment isolerat.',
        geometry_hint=r"""R är vinkelrätt avstånd till z-axeln och z är observationspunktens höjd; $z^{\prime}$ är källkoordinat. Markera båda ändarna ±L. Hela ledarens längd är 2L.""",
        setup_hint=r"""Välj den del du arbetar med:

**(a) Biot–Savart:** Sätt in linjeelement, separationsvektor och gränser i fältintegralen; korsprodukten ger riktningen före integrationen.

**(b) Vektorpotential:** Beräkna först $A_z$ från källintegralen. Ta sedan rotationen av det färdiga uttrycket. Här återstår $B_\phi=-\partial A_z/\partial R$.

**(c) Ampère:** Använd den oändliga ledarens symmetri för att förenkla cirkulationsintegralen. Kontrollera resultatet mot gränsen $L\to\infty$ i (a).""",
    ),
    "SquareLoopOnAxis": G(
        problem_id="6.2",
        learning_goal="Summera magnetfält från flera räta ledarsegment och utnyttja symmetri för att eliminera tvärkomponenter.",
        concepts=("superposition", "ändlig rak ledare", "symmetri"),
        start_here='Skriv B(r)=μ₀I/(4π)∮ dℓ′×(r−r′)/|r−r′|³. Identifiera källpunkt och riktat linjeelement för var och en av kvadratens fyra sidor innan komponenterna summeras. Välj först strömriktning uttryckligt. Appens positiva I går moturs sedd från +z och ger B_z>0, i samma teckenkonvention som det lagrade facit. Uppgiftstextens formulering medurs är inte entydigt förenlig med detta; om du menar medurs sedd från +z ska vektorsvaret få motsatt tecken.',
        hint_titles=('Parametrisera en sida', 'Vilka komponenter ska adderas?', 'Sätt fältpunkten i centrum'),
        hints=(
            r"""Placera hörnen vid $(\pm a/2,\pm a/2,0)$. Medurs sedd från +z är uppgiftens riktning; det tryckta facit använder motsatt tecken. För att jämföra med facit väljer vi här moturs. För nederkanten använder du

$$
\overline r^{\prime}=(x^{\prime},-a/2,0),
\qquad
\mathrm d\overline\ell^{\prime}=\mathrm dx^{\prime}\,\hat x,
\qquad
-a/2\leq x^{\prime}\leq a/2.
$$

Med $\overline r=(0,0,z)$ blir

$$
\begin{aligned}
\overline r-\overline r^{\prime}&=(-x^{\prime},a/2,z),\\
|\overline r-\overline r^{\prime}|&=\sqrt{x^{\prime2}+a^2/4+z^2}.
\end{aligned}
$$""",
            'Integrera en sidas Biot–Savartbidrag och ta dess z-komponent. Vid summering över fyra sidor tar tvärkomponenterna ut varandra, men z-komponenterna adderas.',
            r"""Använd det allmänna uttrycket längs axeln och sätt sedan $z=0$ i del (b). Där ska $a=3{,}0\,\mathrm m$ och $I=10\,\mathrm A$ användas, oavsett vilka utforskningsparametrar som valts i appen.""",
        ),
        self_checks=(
            r"""$B_z$ ska vara jämn i z: på båda sidor om slingan pekar axelfältet åt samma håll för en given strömriktning. Om strömmen vänds byter $B_z$ tecken.""",
            r"""Långt bort ska $B_z$ närma sig $\frac{\mu_0m_z}{2\pi|z|^3}$, där $|m_z|=|I|a^2$. Centrumfältets belopp med uppgiftens tal är cirka 3,8 µT.""",
        ),
        common_pitfall=r"""Att multiplicera hela fältvektorn från en sida med fyra, eller förväxla sidlängden a med halva sidlängden $a/2$. Bestäm strömriktningen innan tecknet jämförs med facit.""",
        geometry_hint='Se slingan från +z och rita en strömpil på varje sida. Höger tumme ger slingans axelfält. Positivt I i appens modell betyder moturs sedd från +z; ett negativt I vänder pilar och fält.',
        setup_hint=r"""För sidan $y=-a/2$ med ström i +x blir

$$
\mathrm dB_z=\frac{\mu_0I(a/2)\,\mathrm dx^{\prime}}{4\pi(x^{\prime2}+a^2/4+z^2)^{3/2}}.
$$

Integrera $x^{\prime}$ från $-a/2$ till $a/2$ och multiplicera z-komponenten med fyra.""",
    ),
    "RightAngleWireCorner": G(
        problem_id="6.3",
        learning_goal="Superponera fält från två halv-oändliga räta ledare med olika riktningar.",
        concepts=("Biot–Savart", "superposition", "vektorriktning"),
        start_here='Skriv B(r)=μ₀I/(4π)∫ dℓ′×(r−r′)/|r−r′|³ för vardera ledardelen. Identifiera deras separata parametriseringar och integrationsgränser; addera vektorerna efter integrationen. Dela ledaren i två halv-oändliga raka delar. I appens koordinater går positiv ström längs +x från negativa x-axeln till hörnet och sedan vidare längs +y. Punkten är (0,0,h).',
        hint_titles=('Två parametriseringar', 'Korsprodukternas riktningar', 'Summera vektorerna'),
        hints=(
            r"""För den inkommande delen är källpunkten och dess bidrag

$$
\begin{aligned}
\overline r^{\prime}&=(x^{\prime},0,0),
&&-\infty<x^{\prime}\leq0,\\
\mathrm d\overline\ell^{\prime}&=\mathrm dx^{\prime}\hat x,
&&\overline r-\overline r^{\prime}=(-x^{\prime},0,h).
\end{aligned}
$$

För utgående delen:

$$
\overline r^{\prime}=(0,y^{\prime},0),
$$

$0\leq y^{\prime}<\infty$,

$$
\begin{aligned}
\mathrm d\overline\ell^{\prime}&=\mathrm dy^{\prime}\,\hat y,\\
\overline r-\overline r^{\prime}&=(0,-y^{\prime},h).
\end{aligned}
$$""",
            r"""Korsprodukterna för de två delarna blir

$$
-h\,\mathrm dx^{\prime}\hat y
\qquad\text{respektive}\qquad
h\,\mathrm dy^{\prime}\hat x.
$$

Avstånden är $\sqrt{x^{\prime2}+h^2}$ respektive $\sqrt{y^{\prime2}+h^2}$. Sätt in dessa i varsin Biot–Savartintegral och integrera över respektive halvlinje.""",
            r"""För $h>0$ ger vardera integral faktorn $1/h$ efter att h i täljaren räknats med. Summera vektorerna och beräkna sedan beloppet från komponenternas kvadratsumma. Sätt $h=0{,}050\,\mathrm m$ och $I=5\,\mathrm A$ sist.""",
        ),
        self_checks=(
            r"""Det numeriska beloppet ska bli ungefär $1{,}4\times10^{-5}\,\mathrm T$. Fältet har ingen z-komponent ovanför hörnet i denna geometri.""",
            r"""Beloppet ska skala som $|I|/h$. Negativ I vänder vektorn men ger samma positiva belopp; en punkt under planet vänder också båda horisontella komponenterna.""",
        ),
        common_pitfall='Att addera de två beloppen direkt eller ange bisektrisen utan att välja dess riktning. Högerhandsregeln måste tillämpas på vart och ett av segmenten.',
        geometry_hint='Rita ett xy-snitt ovanifrån med ett inkommande segment på negativa x-axeln och ett utgående på positiva y-axeln. Observationspunkten ligger på höjden h över hörnet, inte i samma plan som ledaren.',
        setup_hint=r"""Skriv de två Biot–Savartbidragen var för sig:

$$
\begin{aligned}
B_y&=-\frac{\mu_0I}{4\pi}\int_{-\infty}^0
\frac{h\,\mathrm dx^{\prime}}{(x^{\prime2}+h^2)^{3/2}},\\
B_x&=\frac{\mu_0I}{4\pi}\int_0^\infty
\frac{h\,\mathrm dy^{\prime}}{(y^{\prime2}+h^2)^{3/2}}.
\end{aligned}
$$

Utför integralerna var för sig och beräkna sedan beloppet:

$$
|\overline B|=\sqrt{B_x^2+B_y^2}.
$$""",
    ),
    "ThinCurrentStripField": G(
        problem_id="6.5",
        learning_goal="Ersätta ett brett strömförande band med en kontinuerlig samling parallella linjeströmmar.",
        concepts=("superposition", "ytström", "oändlig rak ledare"),
        start_here='Skriv superpositionen B=∫dB med dB=μ₀ dI φ̂/(2πs) för en oändlig rak deltråd. Identifiera delströmmen dI, avståndet s och riktningen φ̂ för varje källäge; komponenterna måste uttryckas i samma bas. Välj ström i +z och bandbredd längs x från −a till a. Betrakta tvärsnittet i xy-planet; uppgiftens två punkter kan då väljas som (2a,0) och (0,2a).',
        hint_titles=('Strömmen i en smal remsa', 'Punkten bredvid bandet', 'Punkten ovanför bandet'),
        hints=(
            r"""En remsa med bredd $\mathrm dx^{\prime}$ bär

$$
\mathrm dI=\frac{I}{2a}\,\mathrm dx^{\prime}.
$$

Fältet från varje lång tråd har belopp

$$
\frac{\mu_0\,\mathrm dI}{2\pi s},
$$

men riktningen beror på observationspunkten.""",
            r"""I punkten (2a,0) pekar alla bidrag i +y för $I>0$. Integrera $\frac1{2a-x^{\prime}}$ från −a till a; detta ger en logaritm.""",
            r"""I punkten (0,2a) tar y-komponenterna ut varandra för $x^{\prime}$ och −$x^{\prime}$. X-komponenterna adderas i −x. Projektionen ger en integral med nämnaren $x^{\prime2}+(2a)^2$ och därmed en arctan.""",
        ),
        self_checks=(
            'Vid fast observationsavstånd mycket större än a ska bandet likna en linjeström med total ström I. Håll avståndet fast när denna gräns tas, inte punkten 2a.',
            r"""Ovanför mittlinjen ska $B_y=0$ och $B_x<0$ för $I>0$. I bandets plan till höger om kanten är $B_y>0$; ett byte av strömriktning vänder båda fälten.""",
        ),
        common_pitfall='Att summera trådarnas fältbelopp i normalplanet utan att projicera vektorerna. Olika remsors fält pekar åt olika håll och vissa komponenter tar ut varandra.',
        geometry_hint=r"""I tvärsnittet är strömmen ut ur bilden för $I>0$, markerad med ⊙. Den går längs bandet, inte tvärs över bredden 2a. Punkten i del (a) ligger utanför bandet, inte inne i metallremsan.""",
        setup_hint=r"""Använd

$$
\mathrm d\overline B=\frac{\mu_0\,\mathrm dI}{2\pi[(x-x^{\prime})^2+y^2]}\left[-y\hat x+(x-x^{\prime})\hat y\right].
$$

Sätt in respektive observationspunkt och integrera $x^{\prime}$ över bandbredden.""",
    ),
    "CircularArcOnAxis": G(
        problem_id="6.8",
        learning_goal="Genomföra Biot–Savart-integralen för en cirkelbåge där symmetrin inte räcker för att eliminera alla komponenter.",
        concepts=("cirkelbåge", "Biot–Savart", "vektorintegral"),
        start_here='Skriv Biot–Savarts lag B(r)=μ₀I/(4π)∫ dℓ′×(r−r′)/|r−r′|³. Identifiera bågens parametrisering, det riktade linjeelementet och vinkelgränserna före korsprodukten. Beräkna bara den krökta delens bidrag i del (a). Appens båge ligger i första kvadranten med φ från 0 till π/2 och positiv I i riktning mot ökande φ, vilket ger det lagrade facits komponenter.',
        hint_titles=('Bågens variabla tangent', 'Integrera en kvartsbåge', 'Jämför med ett helt varv'),
        hints=(
            r"""Parametrisera bågen och separationsvektorn:

$$
\begin{aligned}
\overline r^{\prime}&=(a\cos\phi,a\sin\phi,0),\\
\mathrm d\overline\ell^{\prime}&=a(-\sin\phi,\cos\phi,0)\,\mathrm d\phi,\\
\overline s&=(-a\cos\phi,-a\sin\phi,z).
\end{aligned}
$$

Alla element har avståndet $\sqrt{a^2+z^2}$ till fältpunkten.""",
            r"""Korsprodukten blir

$$
\mathrm d\overline\ell^{\prime}\times\overline s
=(az\cos\phi,az\sin\phi,a^2)\,\mathrm d\phi.
$$

Integrera komponenterna separat över $0\leq\phi\leq\pi/2$; en kvartsbåge saknar helcirkelns möjlighet att släcka alla tvärkomponenter.""",
            r"""För del (b), integrera samma uttryck över $0\leq\phi\leq2\pi$. Sinus- och cosinustermerna försvinner, medan z-komponenten summeras över hela varvet.""",
        ),
        self_checks=(
            r"""I centrum $z=0$ är båda tvärkomponenterna exakt noll och kvartsbågens fält är en fjärdedel av helcirkelns centrumfält.""",
            r"""$B_x$ och $B_y$ är udda i z, medan $B_z$ är jämn. För helcirkeln är $B_x=B_y=0$ över hela axeln. Negativ I vänder alla komponenter.""",
        ),
        common_pitfall='Att ta en fjärdedel av helcirkelns hela fältvektor för alla z. Det ger rätt z-komponent men missar kvartsbågens tvärfält. Lägg inte heller till de raka ledarnas bidrag när frågan gäller bågen ensam.',
        geometry_hint='Rita bågen från (a,0) till (0,a) och observationspunkten (0,0,z). Kontrollera hur din kursfigur orienterar bågen: om koordinater eller strömriktning ändras måste även komponenterna ändras.',
        setup_hint=r"""Sätt den gemensamma nämnaren $(a^2+z^2)^{3/2}$ utanför integralen. Integrera $az\cos\phi$, $az\sin\phi$ och $a^2$ var för sig. På så sätt kan tecken och symmetri kontrolleras innan beloppet beräknas.""",
    ),
    "RotatingChargedDisk": G(
        problem_id="6.13",
        learning_goal="Omvandla en roterande ytladdning till en kontinuerlig fördelning av cirkulära strömslingor.",
        concepts=("ytladdning", "konvektionsström", "strömslinga"),
        start_here='Skriv Biot–Savarts lag och definitionen dI=dQ/τ för en roterande laddningsring, med τ=2π/|ω| för periodens belopp. Identifiera ringens laddningselement, radie och signerade strömriktning innan ringbidragen integreras. Dela skivan i tunna ringar. Använd signerad ytladdning ρs och låt ω vara positiv för rotation moturs sedd från +z; då följer den konventionella strömmens tecken av produkten ρsω.',
        hint_titles=('Från ringladdning till ringström', 'Summera ringarnas fält', 'Radialintegralens undre gräns'),
        hints=(
            r"""En ring med radie r och bredd dr har

$$
\mathrm dq=\rho_s\,2\pi r\,\mathrm dr.
$$

Den signerade ringströmmen är

$$
\mathrm dI=\frac{\omega\,\mathrm dq}{2\pi}
=\rho_s\omega r\,\mathrm dr.
$$

För negativ laddning går strömmen motsatt rörelsen.""",
            r"""Varje ring ger

$$
\mathrm dB_z=\frac{\mu_0\,\mathrm dI\,r^2}{2(r^2+z^2)^{3/2}}.
$$

Summera genom att integrera r från 0 till a, utan att ersätta hela skivan med en enda kantström.""",
            r"""Integrera $\frac{r^3}{(r^2+z^2)^{3/2}}$, exempelvis med $u=\sqrt{r^2+z^2}$. Den undre gränsen blir $|z|$. Det slutliga axelfältet ska därför gälla på båda sidor om skivan.""",
        ),
        self_checks=(
            r"""Vid $z=0$ ska

$$
B_z=\frac{\mu_0\rho_s\omega a}2.
$$

$B_z$ är jämn i z och byter tecken när antingen laddning eller rotation vänds; noll laddning eller noll rotation ger noll fält.""",
            r"""Långt bort blir

$$
\begin{aligned}
m_z&=\frac{\pi\rho_s\omega a^4}4,\\
&B_z\approx\frac{\mu_0m_z}{2\pi|z|^3}.
\end{aligned}
$$

Ett isolerat ringelement får inte användas som modell för hela skivans dipolmoment.""",
        ),
        common_pitfall=r"""Att lägga till en extra faktor $2\pi$ i ringströmmen eller använda z i stället för $|z|$ vid den undre integrationsgränsen. Positiv rotationsriktning och positiv konventionell ström är inte samma sak för negativ laddning.""",
        geometry_hint='r är källringens radie och z observationspunktens höjd; a är skivans ytterradie. Alla ringar har samma vinkelhastighet, men hastigheten ωr och ringarnas laddning varierar med r.',
        setup_hint=r"""Skriv

$$
B_z=\frac{\mu_0\rho_s\omega}2\int_0^a\frac{r^3}{(r^2+z^2)^{3/2}}\,\mathrm dr.
$$

Med $u=\sqrt{r^2+z^2}$ blir integranden $1-\frac{z^2}{u^2}$ och en primitiv funktion $u+\frac{z^2}u$; hantera centrumgränsen kontinuerligt.""",
    ),

    # ------------------------------------------------------------------
    # Kapitel 7 – Kraft, moment och magnetiskt flöde
    # ------------------------------------------------------------------
    "ElectronOrbitDipoleMoment": G(
        problem_id="7.1",
        learning_goal="Koppla en laddnings periodiska rörelse till en ekvivalent ström och ett magnetiskt dipolmoment.",
        concepts=("magnetiskt moment", "ekvivalent ström", "elektronladdning"),
        start_here='Skriv I=q/τ och m=I A n för en plan strömslinga. Identifiera laddningens tecken, omloppstiden och den orienterade arean. Välj elektronens omloppsriktning innan du bestämmer tecknet. Appen antar moturs rörelse sedd från +z; den konventionella strömmen går då medurs eftersom elektronens laddning är −e.',
        hint_titles=('Period och signerad ström', 'Välj areanormal', 'Bestäm momentets riktning'),
        hints=(
            r"""Beräkna omloppstiden $\tau$ från banans omkrets och farten v. En laddning −e passerar ett valt snitt per varv, så den signerade strömmen relativt moturs riktning är $I=-\frac e\tau$.""",
            r"""Använd det magnetiska dipolmomentet för vald positiv omloppsriktning:

$$
\overline m=IA\,\hat n,\qquad A=\pi a^2,\quad\hat n=\hat z
$$

Blanda inte ihop banradien med arean.""",
            r"""Sätt in $\tau=\frac{2\pi a}v$ och förenkla. Högerhandsregeln ska tillämpas på konventionell ström: momentet är motsatt elektronens rörelsemängdsmoment.""",
        ),
        self_checks=(
            r"""Enheten $e\,v\,a$ är

$$
\mathrm{C\,m^2/s}=\mathrm{A\,m^2}.
$$

Om v eller a fördubblas vid fast värde på den andra parametern fördubblas |m|.""",
            'En positiv laddning med samma rörelse får motsatt moment. Om elektronens omloppsriktning vänds byter även m riktning.',
        ),
        common_pitfall='Att rita m som en pil i banplanet. Dipolmomentet är vinkelrätt mot planet, och för den valda elektronrörelsen pekar det in i bilden när du ser från +z.',
        setup_hint=r"""Skriv $I=q/\tau$ och $m_z=I\pi a^2$. Behåll $q=-e$ tills den sista förenklingen så att minustecknet inte tappas bort.""",
        geometry_hint='Se xy-planet från +z. Rita elektronens rörelse moturs och strömmen medurs. Symbolen ⊗ i centrum betyder m längs −z, in i bilden; det är ingen radiell vektor.',
    ),
    "CircularLoopTorqueUniformField": G(
        problem_id="7.2",
        learning_goal="Se hur det lokala kraftbidraget på en strömslinga summeras till det globala momentet m×B.",
        concepts=("Lorentzkraft på ledare", "kraftmoment", "magnetiskt moment"),
        start_here='Skriv dF=I dℓ×B och T=∮r×dF. Identifiera linjeelement, hävarm och det givna fältet innan korsprodukterna beräknas. Beräkna först kraften på ett litet strömelement och sedan dess moment kring centrum. Håll isär dℓ, kraften dF och hävarmen r; de är tre olika vektorer.',
        hint_titles=(
            r"""Del (a) · Kraften på linjeelementet""",
            r"""Del (a) · Integrera kraftmomentet""",
            r"""Del (b–c) · Dipolmoment och vridningsriktning""",
        ),
        hints=(
            r"""Parametrisera

$$
\begin{aligned}
\overline r&=a(\cos\phi,\sin\phi,0),\\
\mathrm d\overline\ell&=a(-\sin\phi,\cos\phi,0)\,\mathrm d\phi.
\end{aligned}
$$

Med $\overline B=B\hat x$ ger kraften från strömelementet

$$
\mathrm d\overline F=I\,\mathrm d\overline\ell\times\overline B
$$

en kraft i z-led vars tecken beror på $\cos\phi$.""",
            r"""Ta

$$
\mathrm d\overline T=\overline r\times\mathrm d\overline F
$$

komponentvis. Då fås

$$
\begin{aligned}
\mathrm dT_x&=-IBa^2\sin\phi\cos\phi\,\mathrm d\phi,\\
\mathrm dT_y&=IBa^2\cos^2\phi\,\mathrm d\phi.
\end{aligned}
$$

Integrera över ett helt varv: x-bidraget tar ut sig.""",
            r"""I (b) börjar du från dipolmetodens allmänna samband:

$$
\overline m=IA\hat n,\qquad \overline T=\overline m\times\overline B.
$$

Identifiera $A=\pi a^2$ och $\hat n=\hat z$ för den givna positiva strömriktningen. Beräkna korsprodukten med $\overline B=B\hat x$ och jämför med integralresultatet i (a).

I (c) tolkar du riktningen: positivt moment kring $y$ vrider $\overline m$ från $+z$ mot $+x$, alltså mot fältet.""",
        ),
        self_checks=(
            r"""Nettokraften

$$
\oint\mathrm d\overline F
$$

ska vara noll i det homogena fältet trots att nettomomentet inte är noll. Integralen av $\cos^2\phi$ över ett varv är π.""",
            r"""Vid $\phi=\pi/2$ är dℓ parallell med B och både dF och dT är noll. Vid $I=0$ eller $B=0$ försvinner momentet; om endast ett av tecknen vänds byter T riktning.""",
        ),
        common_pitfall='Att byta ordning på en korsprodukt eller använda samma riktning för kraft och moment. Här är kraften lokal i ±z medan det sammanlagda momentet ligger i y-led.',
        setup_hint=r"""Gör de två korsprodukterna i ordning:

$$
\mathrm d\overline F=I\,\mathrm d\overline\ell\times\overline B,
$$

sedan

$$
\mathrm d\overline T=\overline r\times\mathrm d\overline F.
$$

Integrera varje momentkomponent över $0\leq\phi\leq2\pi$ innan du jämför med $\overline m\times\overline B$.""",
        geometry_hint=r"""B ligger i slingans plan längs x. På motsatta sidor $x=\pm a$ är krafterna motsatta i z men bildar ett kraftpar kring y. Positiv I går moturs sedd från +z.""",
    ),
    "DipoleDipoleTorque": G(
        problem_id="7.3",
        learning_goal="Beräkna momentet på en magnetisk dipol i det icke-homogena fältet från en annan dipol.",
        concepts=("dipolfält", "magnetiskt moment", "vektorgeometri"),
        start_here='Skriv B₁=μ₀[3(m₁·r̂)r̂−m₁]/(4πr³) och T₂=m₂×B₁. Identifiera dipolmomenten och separationsvektorn innan du tar komponenter. Bestäm fältet från den första dipolen i den andra spolens centrum. Dipolapproximationen förutsätter att spolarna är små jämfört med avståndet r. Välj separationsvektorn i xz-planet.',
        hint_titles=('Fältet vid andra dipolen', 'Vilken komponent ger moment?', 'Skilj belopp från tecken'),
        hints=(
            r"""Skriv

$$
\hat r=\sin\theta\,\hat x+\cos\theta\,\hat z
$$

och använd dipolfältet:

$$
\overline B_1=\frac{\mu_0}{4\pi r^3}
\left[3(\overline m_1\cdot\hat r)\hat r-\overline m_1\right].
$$

Båda momenten är $m\hat z$.""",
            r"""Endast fältets x-komponent bidrar till

$$
\overline T_2=\overline m_2\times\overline B_1.
$$

Z-komponenten är parallell med m₂ och ger inget kraftmoment.""",
            r"""Korsprodukten ger en signerad y-komponent proportionell mot $\sin\theta\cos\theta$. Ta absolutbelopp först när uppgiftens momentbelopp efterfrågas; sätt därefter $m=1\,\mathrm{A\,m^2}$, $r=1\,\mathrm m$ och $\theta=45^\circ$.""",
        ),
        self_checks=(
            r"""Momentet försvinner vid $\theta=0^\circ$, 90° och 180°. Beloppet är störst vid 45° och 135°, men riktningen är motsatt i de två fallen.""",
            r"""Vid uppgiftens värden ska beloppet bli $1{,}5\times10^{-7}\,\mathrm{N\,m}$. Fördubbling av r minskar det med en faktor åtta; samtidig vändning av båda dipolerna ändrar inte momentet.""",
        ),
        common_pitfall=r"""Att kalla $\sin(2\theta)$-uttrycket ett belopp för alla vinklar. Det är den signerade y-komponenten i den valda geometrin; beloppet innehåller $|\sin(2\theta)|$.""",
        setup_hint=r"""Beräkna

$$
B_{1x}=\frac{3\mu_0m\sin\theta\cos\theta}{4\pi r^3}
$$

och därefter $T_{2y}=mB_{1x}$. Använd sedan $|T_{2y}|$ för det efterfrågade beloppet.""",
        geometry_hint=r"""Båda dipolerna är parallella med z, medan $\hat r$ lutar mot x. T är vinkelrätt mot xz-planet, längs ±y. $\theta$ är vinkeln mellan separationen och z, inte mellan de två dipolmomenten.""",
    ),
    "LoopDipoleApproximationError": G(
        problem_id="7.5",
        learning_goal="Kvantifiera när fjärrfältsapproximationen av en strömslinga som magnetisk dipol faktiskt är tillräckligt noggrann.",
        concepts=("dipolapproximation", "relativt fel", "gränsfall"),
        start_here='Skriv relativfelet δ=|B_dip−B_exakt|/|B_exakt| och kravet δ<0,01. Identifiera samma observationspunkt och samma ström och radie i båda fältuttrycken. Jämför exakt axelfält och dipolfält vid samma punkt och för samma slingmoment m=Iπa². Definiera relativfelet med det exakta fältets belopp i nämnaren.',
        hint_titles=('Två fält vid samma punkt', 'Bilda en dimensionslös kvot', 'Lös felvillkoret'),
        hints=(
            r"""För $z\neq0$, jämför fältbeloppen:

$$
B_{\mathrm{exakt}}=\frac{\mu_0Ia^2}{2(a^2+z^2)^{3/2}},
\qquad B_{\mathrm{dip}}=\frac{\mu_0Ia^2}{2|z|^3}.
$$

Formlerna har samma riktning på båda sidor om slingan.""",
            r"""Inför $x=|z|/a$ och bilda kvoten. För $I\ne0$ blir

$$
\frac{B_{\mathrm{dip}}}{B_{\mathrm{exakt}}}
=(1+x^{-2})^{3/2}.
$$

så ström och enheter försvinner.""",
            r"""Lös $(1+x^{-2})^{3/2}-1<0{,}01$ efter x. Använd det exakta olikhetsvillkoret; serieutvecklingen $\frac3{2x^2}$ kan användas som rimlighetskontroll.""",
        ),
        self_checks=(
            r"""Gränsen ligger vid ungefär $|z|=12{,}26a$. Strikt mindre än 1 % kräver ett avstånd större än denna gräns; det avrundade facitvärdet är ungefärligt.""",
            r"""Felet går mot noll långt bort och är oberoende av strömmens storlek och tecken. Vid $I=0$ är båda fälten noll och ett uppmätt relativfel 0/0 odefinierat; grafen visar då samma geometriska gränsvärde som för $I\ne0$.""",
        ),
        common_pitfall=r"""Att använda det approximativa fältet som nämnare, eller anta att dipolmodellen fungerar nära centrum. Den divergerar vid $z=0$ medan slingans exakta fält är ändligt.""",
        visualization_note="En graf över relativfelet mot z/a kan här faktiskt hjälpa studenten att se var dipolapproximationen blir användbar.",
        setup_hint=r"""Isolera först $x^{-2}$: det ska vara mindre än $(1+\mathrm{tol})^{2/3}-1$. Invertera därefter olikheten med hänsyn till att alla storheter är positiva.""",
        geometry_hint='z mäts från slingans centrum vinkelrätt mot dess plan. Rita gärna ett sidoperspektiv med slingans plan och normalaxel. Den sökta tröskelpunkten ligger på normalaxeln.',
    ),
    "AntarcticIceFlux": G(
        problem_id="7.6",
        learning_goal=r"""Använda noll nettoflöde av magnetfältet genom en sluten yta för att byta till en enklare flödesyta.""",
        concepts=("magnetiskt flöde", "Gauss lag för B", "jordens dipolfält"),
        start_here=(
            'Skriv Φ=∫_S B·n dS och ∮_sluten B·n dS=0. Identifiera den efterfrågade öppna ytan och en kompletterande yta med känd normal och enklare fält. Slut isvolymen med bottenytan mot jorden. Det efterfrågade flödet genom hela is–luft-gränsen omfattar både ovansida och lodrät rand; använd ∮B·dS=0 för att ersätta dessa med bottenytan.'
        ),
        hint_titles=('Slut ytan', 'Fältet på bottenkalotten', 'Integrera med rätt normal'),
        hints=(
            r"""Den slutna isvolymens utåtnormal vid botten pekar in mot jorden. Därför är

$$
\Phi_{\mathrm{luft}}=-\Phi_{\mathrm{botten}}.
$$

Jordens moment pekar söderut, så fältet vid sydpolen går från jorden in i isen.""",
            r"""Mät polvinkeln $\theta$ från sydpolen, alltså från momentets riktning. Vid 70° sydlig bredd blir $\theta_{\max}=20^\circ$. På $r=r_J$ är

$$
B_r=\frac{\mu_0 m\cos\theta}{2\pi r_J^3}.
$$

positivt radiellt utåt.""",
            r"""Integrera $B_r r_J^2\sin\theta\,\mathrm d\theta\,\mathrm d\phi$ över bottenkalotten med radialnormal utåt från jorden. Detta är $-\Phi_{\mathrm{botten}}$ och därmed det sökta flödet till luften.""",
        ),
        self_checks=(
            r"""Med

$$
\begin{aligned}
m&=0{,}824\times10^{23}\,\mathrm{A\,m^2},\\
r_J&=637\,\mathrm{mil}=6{,}37\times10^6\,\mathrm m
\end{aligned}
$$

blir flödet cirka $9{,}5\times10^8\,\mathrm{Wb}$. När kalotten krymper till sydpolen går flödet mot noll.""",
            'Istjockleken 1000 m faller bort när bottenkalotten är fixerad: ändrad tjocklek omfördelar flödet mellan ovansida och rand men ändrar inte deras summa. Flödet genom hela den slutna isvolymen är fortfarande noll.',
        ),
        common_pitfall=r"""Att bara räkna isens ovansida och glömma randytan, eller välja fel bottennormal. Gauss lag för magnetfältet är $\oint_S\overline B\cdot\mathrm d\overline S=0$. Nettoflödet genom hela den slutna ytan är noll; flödet genom en enskild del kan vara skilt från noll.""",
        setup_hint=r"""Skriv

$$
\Phi_{\mathrm{luft}}=\int_0^{2\pi}\int_0^{\theta_{\max}}\frac{\mu_0m\cos\theta}{2\pi r_J^3}\,r_J^2\sin\theta\,\mathrm d\theta\,\mathrm d\phi.
$$

Håll isvolymens inåtriktade bottennormal skild från jordens radiella normal.""",
        geometry_hint=r"""$\theta$ mäts från sydpolen och är komplementet till sydlig bredd. Höjden h är istjockleken ovanpå jordytan, inte avståndet från latitudcirkeln till polen. Skissen överdriver tjockleken för läsbarhet.""",
    ),
    "CopperWireMagneticLevitation": G(
        problem_id="7.7",
        learning_goal="Jämföra magnetisk krafttäthet J×B med tyngdkraft per volym.",
        concepts=("krafttäthet", "J×B", "kraftjämvikt"),
        start_here='Skriv kraftbalansen J×B+ρg=0 per volym. Identifiera strömriktningen, massdensiteten och den fältriktning som ger en uppåtriktad kraft. Arbeta med kraft per volym. Både magnetisk kraft och tyngdkraft är proportionella mot trådens volym, så den okända längden och tvärsnittsarean behövs inte.',
        hint_titles=('Krafternas riktningar', 'Vertikal kraftbalans', 'Enheter före insättning'),
        hints=(
            r"""Skriv magnetisk krafttäthet

$$
\overline f_{\mathrm{mag}}=\overline J\times\overline B.
$$

Med $\overline J=J\hat x$ och $\overline B=B\hat y$ blir den $JB\hat z$; tyngdkrafttätheten är $-\rho g\hat z$.""",
            r"""Kraftbalansen för de vertikala krafttätheterna ger

$$
JB-\rho g=0.
$$

Detta är ett kraftbalansvillkor, inte i sig ett bevis för stabil svävning.""",
            r"""Omvandla $J=3{,}0\,\mathrm{A/mm^2}$ till $3{,}0\times10^6\,\mathrm{A/m^2}$ och

$$
\rho=8{,}9\,\mathrm{g/cm^3}
$$

till $8{,}9\times10^3\,\mathrm{kg/m^3}$ innan du löser ut och beräknar B.""",
        ),
        self_checks=(
            r"""Med $g=9{,}81\,\mathrm{m/s^2}$ blir $B\approx0{,}0291\,\mathrm T$, alltså 29 mT. Vid mindre B är nettokraften nedåt och vid större B uppåt.""",
            'Fördubbling av J halverar det erforderliga B. Om bara strömmen eller bara fältet vänds blir den magnetiska kraften nedåt och kan inte balansera tyngden.',
        ),
        common_pitfall='Att blanda kraft per längd med kraft per volym, eller glömma faktorn 10⁶ vid omvandlingen från A/mm². Kraftbalans i ett homogent fält ger ingen återställande kraft vid en höjdförskjutning.',
        setup_hint=r"""Du kan även skriva $I=JA$ för en bit med längd $\ell$: $F_{\mathrm{mag}}=JA\ell B$ och $F_g=\rho A\ell g$. Förkorta Aℓ först och lös därefter balansvillkoret.""",
        geometry_hint=r"""Välj x åt höger och z uppåt. Strömmen går längs +x och lyftkraften längs +z. Då måste B peka längs +y enligt $\hat x\times\hat y=\hat z$; B och $\overline J\times\overline B$ är vinkelräta.""",
    ),
    "InfiniteWireRectangularLoopFlux": G(
        problem_id="7.10",
        learning_goal="Beräkna magnetiskt flöde genom en plan yta när B både varierar i belopp och lutar relativt ytans normal.",
        concepts=("magnetiskt flöde", "fält från rak ledare", "projektion"),
        start_here='Skriv Φ=∫_S B·n dS och B=μ₀I φ̂/(2πR) för den oändliga ledaren. Identifiera avståndet till ledaraxeln, fältets riktning och slingans normal innan flödet integreras. Välj slingans normal till +z och beräkna ledarens fält i punkten (x,y,c). Fältet cirkulerar runt x-axeln och är inte vinkelrätt mot hela slingytan.',
        hint_titles=('Ledarfältets riktning', 'Projicera på ytans normal', 'Integrera över rektangeln'),
        hints=(
            r"""Avståndet till ledaren är $R=\sqrt{y^2+c^2}$. För ström i +x ger högerhandsregeln

$$
\overline B=\frac{\mu_0I}{2\pi(y^2+c^2)}
(-c\hat y+y\hat z).
$$""",
            r"""Ytelementet är

$$
\mathrm d\overline S=\hat z\,\mathrm dx\,\mathrm dy.
$$

så bara $B_z$ bidrar. Vid närmaste kanten $y=0$ är $B_z=0$ trots att hela magnetfältet där är ändligt.""",
            r"""$B_z$ är oberoende av x. X-integralen ger a, och y-integralen från 0 till b innehåller $\frac y{y^2+c^2}$, vars primitiva funktion är en halv logaritm.""",
        ),
        self_checks=(
            r"""Flödet ska vara proportionellt mot I och a och byta tecken när strömmen eller vald ytnormal vänds. Vid $b\to0$ försvinner flödet.""",
            r"""För $c\gg b$ ska

$$
\Phi\approx\frac{\mu_0Iab^2}{4\pi c^2}.
$$

När $c\to0$ vid fast b divergerar idealmodellens flöde logaritmiskt; en verklig ledares ändliga radie sätter gränser för modellen.""",
        ),
        common_pitfall=r"""Att integrera fältbeloppet $\frac{\mu_0I}{2\pi R}$ utan projektion eller behandla hela slingytan som om den hade samma avstånd till ledaren.""",
        setup_hint=r"""Skriv

$$
\Phi=\frac{a\mu_0I}{2\pi}\int_0^b\frac y{y^2+c^2}\,\mathrm dy.
$$

Logaritmens slutliga argument måste vara dimensionslöst; använd kvoten av värdena vid de båda gränserna.""",
        geometry_hint=r"""Slingan ligger i $z=c$, med $0\leq x\leq a$ och $0\leq y\leq b$. I ett yz-snitt syns ledaren som en punkt vid origo och slingan som en sträcka på höjden c; normalen pekar uppåt längs z.""",
    ),

    # ------------------------------------------------------------------
    # Kapitel 8 – Magnetiska material och magnetiska kretsar
    # ------------------------------------------------------------------
    "PermanentMagnetAirGapBHCurve": G(
        problem_id="8.1",
        learning_goal="Bestäm arbetspunkten för en permanentmagnet genom skärningen mellan materialets B–H-kurva och magnetkretsens lastlinje.",
        concepts=("B–H-kurva", "magnetisk krets", "luftgap"),
        start_here='Skriv ∮H·dl=NI och ∮B·n dS=0. Identifiera magnetlängd, gaplängd, gemensam area och materialets tabellerade H(B); summera de två delarnas cirkulation. Börja med flödeskontinuitet och Ampères lag. Utan läckage och med samma tvärsnitt är B samma i magnet och gap, men H är olika. Kursoriginalets fullständiga B–H-tabell och spolström i del (b) finns nu i uppgiftstexten.',
        hint_titles=('Materialkurvan och gapfältet', 'Arbetspunkt utan spole', 'Arbetspunkt med spole'),
        hints=(
            r"""I luftgapet gäller

$$
H_g=\frac B{\mu_0}.
$$

Använd materialtabellen för $H_m(B)$. Magnetens H kan vara negativt även när B är positivt.""",
            r"""Utan spolström gäller

$$
H_m\ell_m+\frac{Bd}{\mu_0}=0.
$$

Rita lastlinjen

$$
H_m=-\frac{Bd}{\mu_0\ell_m}
$$

och sök skärningen med materialkurvan.""",
            'Med spole ersätts högerledet av NI. Positiv I i appen förstärker gapfältet. Interpolera mellan tabellpunkter; utanför den givna materialkurvan kan arbetspunkten inte bestämmas utan fler data.',
        ),
        self_checks=(
            r"""Vid $I=0$ ska magnetens negativa H-bidrag balansera gapets positiva bidrag. Kontrollera residualen $H_m\ell_m+\frac{Bd}{\mu_0}-NI$, inte bara hur nära kurvorna ser ut att ligga.""",
            'Ökad förstärkande NI höjer B inom tabellens giltiga intervall. En tabelländpunkt är inte automatiskt en lösning om lastlinjen missar kurvan.',
        ),
        common_pitfall=r"""Att använda en konstant permeabilitet för permanentmagneten eller extrapolera den tabellerade grenen utan stöd. Originalets $\ell$ är magnetens längd, medan luftgapet d tillkommer.""",
        visualization_note="Just här är en B–H-graf med lastlinje pedagogiskt relevant eftersom lösningen bokstavligen är deras skärningspunkt.",
        setup_hint=r"""Originaluppgiften definierar $\ell$ som permanentmagnetens längd, alltså $\ell_m=\ell$. Använd

$$
H_m(B)\ell+\frac{Bd}{\mu_0}=NI
$$

där d är luftgapet, utan att dra av d från $\ell$.""",
        geometry_hint='Följ en sluten medellinje genom magnet och luftgap. Samma flöde passerar båda; gapet är en seriedel. Spolens tecken bestäms av om dess magnetomotoriska spänning hjälper eller motverkar magneten.',
    ),
    "NonlinearIronMagneticCircuit": G(
        problem_id="8.2",
        learning_goal="Lösa en magnetisk krets där järnets materiallag är icke-linjär men flödet är gemensamt med luftgapet.",
        concepts=("icke-linjär B–H-lag", "Ampères lag", "luftgap"),
        start_here='Skriv ∮H·dl=NI, flödeskontinuitet och den givna materiallagen B=aH/(b+H). Identifiera järnets och gapets längder samt materiallagens giltiga gren. Använd ett gemensamt B i järn och gap eftersom tvärsnittet är samma och läckage försummas. Invertera den givna materiallagen innan Ampères lag ställs upp.',
        hint_titles=('Invertera materiallagen', 'Summera cirkulationen', 'Pröva den fysikaliska roten'),
        hints=(
            r"""Från $B=\frac{aH}{b+H}$ fås

$$
H=\frac{bB}{a-B}.
$$

Materiallagen gäller för $H>0$, vilket begränsar den fysiska lösningen till $0<B<a$.""",
            r"""Skriv magnetkretsens balans:

$$
H_{\text{järn}}\ell+\frac{Bd}{\mu_0}=NI.
$$

Här är $\ell$ järnets medellängd. Tvärsnittet S förkortas bort när samma B gäller i hela kretsen; flödet är däremot $\Phi=BS$.""",
            r"""Lös den monotona ekvationen i intervallet $0<B<a$. Om du multiplicerar bort nämnaren och använder en andragradsekvation måste varje rot återinsättas i både materiallagen och balansvillkoret.""",
        ),
        self_checks=(
            r"""Med uppgiftens värden ska B bli cirka 0,22 T och ligga under $a=2\,\mathrm T$. Den andra algebraiska roten ligger över a och ger $H<0$, trots att B där är positivt.""",
            r"""Ökad positiv ström höjer B mot mättnadsgränsen a. Vid $I\to0^+$ går $B\to0$. Appen tillåter noll som gränsfall men extrapolerar inte den givna $H>0$-lagen till negativ ström.""",
        ),
        common_pitfall=r"""Att godta en rot enbart för att B är positivt. Även $B<a$ och $H>0$ måste gälla. Arean behövs för flödet men påverkar inte B i denna idealisering.""",
        setup_hint=r"""Sätt

$$
\frac{bB\ell}{a-B}+\frac{Bd}{\mu_0}=NI.
$$

I kontrollerna heter materialkonstanterna $B_{\mathrm{sat}}$ och $H_0$ för att skilja dem från geometriska längder. Summan av järnets och gapets ampervarv ska bli NI.""",
        geometry_hint='Järn och luftgap ligger i serie och har samma area S. Summera H gånger respektive delsträcka, inte B gånger hela längden med en enda permeabilitet.',
    ),
    "MagneticBridgeCircuit": G(
        problem_id="8.4",
        learning_goal="Översätta en förgrenad järngeometri till ett nätverk av magnetiska reluktanser och hitta flödet i en bestämd gren.",
        concepts=("reluktans", "magnetisk krets", "flödesdelning"),
        start_here='Skriv ∮H·dl=NI, Φ_in=ΣΦ_ut vid en förgrening och ℜ=ℓ/(μS) för varje homogen del. Identifiera delarnas längder, areor och vilka flöden som är gemensamma. Rita vänster ringhalva som en seriedel med spolen. Mellan ringens två förgreningspunkter ligger bryggan och höger ringhalva parallellt.',
        hint_titles=('Beräkna delarnas reluktanser', 'Fördela flödet', 'Lös för bryggan'),
        hints=(
            r"""Varje ringhalva har längd $\pi D/2$ och area $S_{\mathrm{ring}}$. Bryggan har längd D och area $S_{\mathrm{brygga}}$. Beräkna reluktansen för varje del:

$$
\mathcal R=\frac{\ell}{\mu_0\mu_rS}.
$$

Använd respektive längd och tvärsnittsarea.""",
            r"""Låt $U_m$ vara den magnetiska potentialskillnaden mellan förgreningspunkterna. Då är

$$
\begin{aligned}
\Phi_b&=\frac{U_m}{\mathcal R_b},\\
\Phi_h&=\frac{U_m}{\mathcal R_h}
\end{aligned}
$$

medan vänsterflödet är $\Phi_v=\Phi_b+\Phi_h$.""",
            r"""Spolens NI används både i vänstra ringhalvan och över parallellgrenarna:

$$
NI=\mathcal R_v(\Phi_b+\Phi_h)+U_m.
$$

Lös först $U_m$ och sedan det efterfrågade bryggflödet.""",
        ),
        self_checks=(
            r"""Med uppgiftens värden blir bryggflödet cirka $1{,}1\times10^{-8}\,\mathrm{Wb}$. Om $S_{\mathrm{brygga}}\to0$ ska bryggflödet gå mot noll.""",
            r"""Vänsterflödet är summan av de två grenflödena. En större grenreluktans ger mindre grenflöde vid samma $U_m$; vänd strömmen och alla flöden byter tecken.""",
        ),
        common_pitfall='Att lägga alla tre delarna i serie eller dela flödet lika utan att jämföra reluktanserna. Samma material innebär inte samma reluktans när längder och areor skiljer sig.',
        visualization_note="Ett reluktansnät bredvid den geometriska skissen är sannolikt mer lärorikt än en 3-D-fältbild för denna uppgift.",
        setup_hint=r"""Skriv

$$
\begin{aligned}
\mathcal R_v&=\mathcal R_h=\frac{\pi D}{2\mu_0\mu_rS_{\mathrm{ring}}},\\
\mathcal R_b&=\frac D{\mu_0\mu_rS_{\mathrm{brygga}}}.
\end{aligned}
$$

Eliminera $\Phi_b$ och $\Phi_h$ ur

$$
NI=\mathcal R_v(\Phi_b+\Phi_h)+U_m.
$$""",
        geometry_hint='De två ringhalvorna möts vid bryggans ändar. Det finns en gemensam inkommande gren och två returvägar. Spolen sitter på bara den ena ringhalvan.',
    ),
    "CurrentCarryingMagneticTube": G(
        problem_id="8.5",
        learning_goal="Hålla isär H, B och M när ett fritt strömförande material kan vara magnetiskt.",
        concepts=("Ampères lag för H", "magnetisering", "styckvis fält"),
        start_here='Skriv ∮H·dl=I_fri,in, B=μ₀(H+M) och M=(μr−1)H i materialet. Identifiera cylindersymmetrin och den fria ström som omsluts i varje radialområde. Bestäm H från den fria strömmen innan du räknar B och M. Strömmen antas likformigt fördelad i rörmaterialets area π(b²−a²), inte i hela cirkelskivan.',
        hint_titles=('Innesluten fri ström', 'Cirkulation längs en cirkel', 'Från H till B och M'),
        hints=(
            r"""Dela upp rummet i $R<a$, $a<R<b$ och $R>b$. Den omslutna fria strömmen är respektive 0, $\frac{I(R^2-a^2)}{b^2-a^2}$ och I.""",
            r"""En cirkulär Ampereslinga ger

$$
2\pi R H_\phi=I_{\mathrm{fri,innesluten}}.
$$

Högerhandsregeln kring +z ger positiv $\phi$-riktning för $I>0$.""",
            r"""I kopparmodellen $\mu_r=1$ är $M=0$ och

$$
\overline B=\mu_0\overline H.
$$

I järnmaterialet gäller

$$
\overline M=(\mu_r-1)\overline H,\qquad
\overline B=\mu_0\mu_r\overline H.
$$

I hålet och utanför används vakuumrelationen.""",
        ),
        self_checks=(
            r"""H är oberoende av $\mu_r$ och kontinuerligt vid a och b eftersom ingen fri ytström införts. Vid $R=a$ är $H=0$.""",
            r"""Vid b är $H_\phi$ kontinuerligt men $B_\phi$ och $M_\phi$ kan hoppa. B är tangentiellt mot denna gränsyta, så kravet på kontinuerligt normalt B förbjuder inte hoppet.""",
        ),
        common_pitfall=r"""Att blanda H [A/m] och B [T] på samma numeriska skala eller lägga $\mu_r$ i Ampères lag för H. Separata graflägen gör det möjligt att jämföra rätt storhet och enhet.""",
        setup_hint=r"""Beräkna först $I_{\mathrm{fri,in}}$ från areakvoten. Använd därefter

$$
H_\phi=\frac{I_{\mathrm{fri,in}}}{2\pi R},
$$

med $H=0$ i hålet även på axeln. Applicera materialrelationerna bara för $a<R<b$.""",
        geometry_hint=r"""Strömmen går längs rörets axel, medan H, B och M går runt axeln. R är avstånd från axeln; a och b är de två materialgränserna. Ställ $\mu_r=1$ för del (a).""",
    ),
    "HorseshoeMagnetAnchorForce": G(
        problem_id="8.6",
        learning_goal="Beräkna attraktionskraft från uppmätt magnetiskt flöde med hjälp av magnetiskt tryck i luftgap.",
        concepts=("magnetiskt tryck", "magnetiskt flöde", "kraft"),
        start_here='Skriv Φ=∫B·n dS och magnetiskt tryck p=B²/(2μ₀) i luftgapet. Identifiera arean för varje pol och summera krafterna pS på ankaret. Utgå från det uppmätta flödet i magnetkretsen. Samma flöde går genom båda polerna i serie; Φ0 ska inte delas i två.',
        hint_titles=('Fältet vid varje pol', 'Trycket i gapet', 'Summera polernas krafter'),
        hints=(
            r"""Med försumbart läckage och ungefär jämnt fält är

$$
B\simeq\frac{\Phi_0}{S}.
$$

vid varje pol. Omvandla $S=2{,}8\,\mathrm{cm^2}$ till $2{,}8\times10^{-4}\,\mathrm{m^2}$.""",
            r"""Det magnetiska trycket i ett mycket litet luftgap är

$$
p=\frac{B^2}{2\mu_0}.
$$

Varje pol bidrar med kraften pS mot ankaret.""",
            'Det finns två polytor med area S vardera. Addera deras krafter och sätt först därefter in flödet och arean.',
        ),
        self_checks=(
            'Resultatet blir cirka 256 N, avrundat 260 N i facit. En enda pol ger hälften av hela kraften.',
            r"""Kraften är attraktiv och beror på $\Phi_0^2$. Om flödets riktning vänds ändras inte kraftbeloppet; dubbelt flöde ger fyra gånger större kraft.""",
        ),
        common_pitfall='Att dela flödet mellan de två polerna eller missa faktorn två i kraftsumman. Sambandet vid fast uppmätt flöde ska inte tolkas som att flödet förblir konstant om magnetens verkliga geometri ändras.',
        setup_hint=r"""Skriv

$$
F_{\mathrm{tot}}=2\frac{B^2}{2\mu_0}S
$$

och använd $B=\frac{\Phi_0}S$. Kontrollera att S är arean för en pol, inte summan av båda polytorna.""",
        geometry_hint='Fältet går ut genom den ena polen och in genom den andra, men båda polerna drar ankaret mot magneten. Skissens två kontaktområden motsvarar två kraftbidrag.',
    ),
    "PermanentlyMagnetizedCylinderAxis": G(
        problem_id="8.12",
        learning_goal="Ersätta en homogen magnetisering med bundna magnetiseringsströmmar och därefter skilja mellan B och H.",
        concepts=("magnetisering", "magnetiseringsström", "B och H"),
        start_here=r"""Skriv $I_{m,S}=\oint_C\overline M\cdot\mathrm d\overline\ell$, där $C$ begränsar en yta $S$ helt inne i materialet. Använd sedan $\overline J_{sm}=\overline M\times\hat n$ på materialets rand. För konstant $\overline M=M\hat z$ finns ingen bunden volymström, men mantelns ytström ger ett fält som beräknas med Biot–Savarts lag. Bestäm till sist $\overline H=\overline B/\mu_0-\overline M$.""",
        hint_titles=('Vilka bundna strömmar finns?', 'Manteln som strömslingor', 'Från B till H'),
        hints=(
            r"""Välj en sluten kurva $C$ helt inne i materialet och en uppspänd yta $S$ där. Den bundna strömmen genom ytan är

$$
I_{m,S}=\oint_C\overline M\cdot\mathrm d\overline\ell=0.
$$

En konstant vektor $\overline M$ ger noll cirkulation runt varje sluten kurva, så det finns ingen bunden volymström. På manteln gäller däremot

$$
\overline J_{sm}=\overline M\times\hat R=M\hat\phi.
$$

Ändytorna har normal $\pm\hat z$ och därför ingen bunden ytström.""",
            r"""En mantelremsa med höjd $\mathrm dz^{\prime}$ motsvarar en cirkulär slinga med

$$
\mathrm dI=M\,\mathrm dz^{\prime}.
$$

Integrera dess axelfält över $0<z^{\prime}<h$ med avståndet $z-z^{\prime}$ till observationspunkten.""",
            r"""Använd

$$
\overline H=\frac{\overline B}{\mu_0}-M\hat z
$$

inuti och

$$
\overline H=\frac{\overline B}{\mu_0}
$$

utanför. För del (c), låt a växa vid fast h och fast observationspunkt z; då fås gränsen för en oändligt utbredd skiva.""",
        ),
        self_checks=(
            r"""$B_z$ är kontinuerligt över ändytorna på axeln och symmetriskt kring $z=h/2$. $H_z$ hoppar med −M när du går in vid $z=0$ och med +M när du går ut vid $z=h$.""",
            r"""Vid $a\to\infty$ och fast h,z går $B\to0$. Inuti går $H\to-M$ och utanför $H\to0$. För en lång smal cylinder långt från ändarna är i stället $B\approx\mu_0M$ och $H\approx0$.""",
        ),
        common_pitfall=r"""Att använda $B=\mu_0M$ utan avmagnetiserande H eller förväxla en mycket bred cylinder med en mycket lång. På idealiserade gränsytor ska H jämföras genom sina ensidiga gränsvärden.""",
        setup_hint=r"""Skriv

$$
B_z=\frac{\mu_0M}2\int_0^h\frac{a^2}{[a^2+(z-z^{\prime})^2]^{3/2}}\,\mathrm dz^{\prime}.
$$

Efter integrationen bestäms H med den lokala magnetiseringen, som är noll utanför $0<z<h$.""",
        geometry_hint=r"""Cylinderns botten ligger vid $z=0$ och toppen vid $z=h$, inte vid $\pm h/2$. Mantelströmmen går moturs sedd från +z för $M>0$. Radie-kartan är en parameterstudie av axelfältet, inte ett rumsligt fält utanför axeln.""",
    ),
    "MagnetizationCurrentsCylinder": G(
        problem_id="8.13",
        learning_goal="Härleda både volym- och ytmagnetiseringsströmmar från ett linjärt magnetiserat strömförande material och visa att deras nettoström tar ut sig.",
        concepts=("magnetiseringsström", "M=(μr−1)H", "cylindriska koordinater"),
        start_here=r"""Utgå från Ampères lag $\oint_C\overline H\cdot\mathrm d\overline\ell=I_{\mathrm{fri,in}}$ och $\overline M=(\mu_r-1)\overline H$. Beräkna sedan bunden ström genom en tvärsnittsskiva med $I_{m,S}=\oint_C\overline M\cdot\mathrm d\overline\ell$. På materialets mantel används $\overline J_{sm}=\overline M\times\hat n$. Håll isär volymström och ytström.""",
        hint_titles=('Magnetiseringen inne i ledaren', 'Volymström och ytström', 'Jämför de integrerade strömmarna'),
        hints=(
            r"""För $R<a$ är

$$
\begin{aligned}
I_{\mathrm{fri,in}}&=\frac{IR^2}{a^2},\\
H_\phi&=\frac{IR}{2\pi a^2}.
\end{aligned}
$$

Därför är $M_\phi$ linjär i R.""",
            r"""Välj en cirkel med radie $R<a$, positiv omloppsriktning moturs sedd från $+z$. Magnetiseringens cirkulation ger den bundna strömmen genom skivan:

$$
\begin{aligned}
I_{m,S}(R)&=\oint_C\overline M\cdot\mathrm d\overline\ell\\
&=2\pi R M_\phi(R).
\end{aligned}
$$

Sätt in $M_\phi$ från föregående steg. Strömmen är proportionell mot $R^2$, så varje ringskikt har samma ström per tvärsnittsarea. Dividera med $\pi R^2$ för att få den konstanta $J_{m,z}$.

På manteln används

$$
\overline J_{sm}=\overline M\times\hat R.
$$

Eftersom $\hat\phi\times\hat R=-\hat z$ är ytströmmen motsatt volymströmmen när $I(\mu_r-1)>0$.""",
            r"""Integrera $\overline J_m$ över tvärsnittet och $\overline J_{sm}$ över mantelytans skärning med tvärsnittet:

$$
\begin{aligned}
I_{\mathrm{m,vol}}&=J_{m,z}\pi a^2,\\
I_{\mathrm{m,yta}}&=J_{sm,z}\,2\pi a.
\end{aligned}
$$

Addera först dessa strömmar i ampere.""",
        ),
        self_checks=(
            r"""Volym- och ytbidragen blir ($\mu_r-1$)I respektive −($\mu_r-1$)I. Deras summa är noll, men den fria transportströmmen I finns fortfarande kvar.""",
            r"""Vid $\mu_r=1$ eller $I=0$ försvinner båda magnetiseringsströmmarna. Om I eller tecknet på $\mu_r-1$ ändras vänder båda riktningarna.""",
        ),
        common_pitfall=r"""Att addera $\overline J_m$ [A/m²] direkt till $\overline J_{sm}$ [A/m], eller tolka noll nettomagnetiseringsström som att strömmarna och deras fält är noll överallt.""",
        setup_hint=r"""Sätt in magnetiseringen i cirkulationsintegralen för en cirkel inne i ledaren:

$$
\begin{aligned}
M_\phi(R)&=\frac{(\mu_r-1)IR}{2\pi a^2},\\
I_{m,S}(R)&=2\pi R M_\phi(R)
=\frac{(\mu_r-1)IR^2}{a^2}.
\end{aligned}
$$

Strömmen per skivarea är konstant. Därför är $J_{m,z}=I_{m,S}(R)/(\pi R^2)$ för $0<R<a$, med samma ändliga gränsvärde på axeln. Beräkna ytströmmen separat från $\overline J_{sm}=\overline M\times\hat R$ precis innanför $R=a$.""",
        geometry_hint=r"""Både volym- och ytström går axiellt, men i motsatta riktningar. Ytströmmen finns på manteln $R=a$; den är inte en azimutal ström runt tvärsnittets rand.""",
    ),

    # ------------------------------------------------------------------
    # Kapitel 9 – Induktans, induktion och elektromotorisk spänning
    # ------------------------------------------------------------------
    "MutualInductanceParallelWiresSquare": G(
        problem_id="9.2",
        learning_goal="Beräkna ömsesidig induktans genom att integrera magnetiskt flöde från två motriktade oändliga ledare genom en snedställd kvadrat.",
        concepts=("ömsesidig induktans", "magnetiskt flöde", "geometri"),
        start_here='Skriv M=Φ₂/I₁ och Φ₂=∫_S₂ B₁·n₂ dS. Identifiera bidragen från båda raka ledarna, mottagarytans normal och dess varierande bredd. Välj båda slingornas orientering innan du bestämmer tecknet på M. Välj koordinater så att de raka ledarna ligger längs x vid y=0 och y=d, med ström i +x respektive −x; mellan dem pekar B i +z.',
        hint_titles=('Ledarnas sammanlagda fält', 'Remsans varierande bredd', 'Från flöde till induktans'),
        hints=(
            r"""Välj ledarna längs x vid $y=0$ och $y=d$, med ström i +x respektive −x. Välj slingnormal +z och låt $u=y$ vara avståndet från den nedre ledaren. Mellan ledarna adderas fälten:

$$
B_z=\frac{\mu_0 I}{2\pi}
\left(\frac1u+\frac1{d-u}\right).
$$

Returledaren ska inte subtraheras eftersom dess strömriktning redan är omvänd.""",
            r"""Kvadratens diagonal över mellanrummet är d och sidan $d/\sqrt2$. En remsa på höjden $u$ har bredden

$$
w(u)=
\begin{cases}
2u,&0<u<d/2,\\
2(d-u),&d/2<u<d.
\end{cases}
$$""",
            r"""Integrera $B_z$ gånger remsans area, använd spegelsymmetri kring $u=d/2$ och dividera flödet med I. Behåll båda ledarnas bidrag även när du utnyttjar symmetrin.""",
        ),
        self_checks=(
            r"""M ska vara proportionell mot $\mu_0d$ och ha enheten henry. Om alla längder fördubblas fördubblas M.""",
            'B divergerar vid en ideal linjeledare, men kvadratens lokala bredd går samtidigt mot noll. Flödesintegralen är därför ändlig. Vänd mottagarslingans normal och tecknet på M vänds.',
        ),
        common_pitfall='Att använda hela arean gånger centrumfältet eller anta konstant remsbredd. Kvadratens hörn tangerar ledarna geometriskt utan att slingorna ska vara elektriskt förbundna.',
        visualization_note="En skiss som visar den lokala kvadratbredden som funktion av x gör integraluppställningen betydligt lättare att förstå.",
        setup_hint=r"""Med normal +z skriv

$$
\Phi=2\int_0^{d/2}\frac{\mu_0I}{2\pi}\left(\frac1u+\frac1{d-u}\right)2u\,\mathrm du.
$$

Förenkla produkten innan ändpunkten $u=0$ behandlas.""",
        geometry_hint=r"""x går längs ledarna och $u=y$ tvärs mellan dem. Detta är en roterad kvadrat, inte en rektangel med konstant bredd. Skissens strömpilar ger positivt flöde genom normal +z.""",
    ),
    "MutualInductanceCoaxialLoops": G(
        problem_id="9.4",
        learning_goal="Se reciprociteten i ömsesidig induktans genom två olika approximativa flödesberäkningar.",
        concepts=("ömsesidig induktans", "dipolapproximation", "reciprocitet"),
        start_here='Skriv M=Φ_mottagare/I_källa och Φ=∫B·n dS. Identifiera vilken slinga som är källa i varje del och var de givna småparameterantagandena får användas. Uppgiften antar a≪b och a≪d. Använd två olika källslingor i del (a) och (b), men håll mottagarens normal och strömriktning konsekventa så att M kan jämföras.',
        hint_titles=(
            r"""Del (a) · Dipolfältet från den lilla slingan""",
            r"""Del (a) · Integrera över den stora skivan""",
            r"""Del (b) · Bestäm den stora slingans fält""",
            r"""Del (b) · Flöde genom den lilla slingan""",
        ),
        hints=(
            r"""I (a) börjar du med flödesintegralen i startlagen och identifierar den lilla slingan som källa. Dess dipolmoment är $\overline m=I_{\mathrm{liten}}\pi a^2\hat z$. Använd det allmänna dipolfältet:

$$
\overline B(\overline r)=\frac{\mu_0}{4\pi r^3}
\left[3(\overline m\cdot\hat r)\hat r-\overline m\right].
$$

På den stora skivan är $\overline r=R\hat R+d\hat z$ och $r=\sqrt{R^2+d^2}$. Projektera på skivans normal $\hat z$. Det ger

$$
B_z(R)=\frac{\mu_0m(2d^2-R^2)}{4\pi(R^2+d^2)^{5/2}}.
$$""",
            r"""Integrera flödesbidraget

$$
\mathrm d\Phi=B_z(R)\,2\pi R\,\mathrm dR
$$

från 0 till b. Använd inte bara dipolfältets axelvärde över hela den stora arean; både belopp och tecken på $B_z$ kan variera. Dividera sedan flödet med källströmmen $I_{\mathrm{liten}}$ för att få $M$.""",
            r"""I (b) byter du källa och mottagare. Börja från Biot–Savarts integral för den stora slingan:

$$
\overline B=\frac{\mu_0I_{\mathrm{stor}}}{4\pi}
\oint\frac{\mathrm d\overline\ell'\times(\overline r-\overline r')}{|\overline r-\overline r'|^3}.
$$

På axeln väljs $\overline r=d\hat z$, medan $\overline r'=b\hat R(\phi)$ och $\mathrm d\overline\ell'=b\,\mathrm d\phi\,\hat\phi$. Integrera ett helt varv; tvärkomponenterna tar ut varandra. Du kan också använda ringfältet som redan härletts i 6.8(b).""",
            r"""Använd den lilla slingans normal och area i flödesintegralen:

$$
\begin{aligned}
\Phi_{\mathrm{liten}}&=\int_{S_{\mathrm{liten}}}\overline B_{\mathrm{stor}}\cdot\mathrm d\overline S\\
&\approx B_z(d)\pi a^2,\\
M&=\frac{\Phi_{\mathrm{liten}}}{I_{\mathrm{stor}}}.
\end{aligned}
$$

Här får fältet tas ut ur integralen eftersom $a\ll b$ och $a\ll d$. Detta antagande gällde inte över den stora mottagarskivan i (a). Jämför de två resultaten med samma orientering.""",
        ),
        self_checks=(
            r"""För $d\gg b$ ska M avta som $d^{-3}$. M är proportionell mot den lilla slingans area och är positiv för de samriktade normaler som appen använder.""",
            r"""Reciprocitet betyder $M_{12}=M_{21}$ för samma geometri. Den asymmetriskt skrivna approximationen får inte användas med a och b utbytta utan att kraven på vilken slinga som är liten fortfarande gäller.""",
        ),
        common_pitfall=r"""Att förväxla reciprocitet med tillåtelse att använda en approximation utanför dess giltighetsområde. Kontrollera $a/b$ och $a/d$ före tolkningen av ett numeriskt resultat.""",
        setup_hint=r"""Del (a): skriv

$$
M=\frac{\Phi_{\mathrm{stor}}}{I_{\mathrm{liten}}}
$$

och integrera dipolfältets normalkomponent över skivan. Del (b): skriv

$$
M=\frac{\mu_0I_{\mathrm{stor}}b^2}{2(b^2+d^2)^{3/2}}\frac{\pi a^2}{I_{\mathrm{stor}}}.
$$""",
        geometry_hint='Slingornas plan är parallella och deras gemensamma axel går genom båda centrum. I ett snitt genom axeln syns slingorna som två kantställda sträckor, inte två cirklar bredvid varandra i samma plan.',
    ),
    "OpenSecondaryTransformerVoltage": G(
        problem_id="9.6",
        learning_goal="Koppla en tidsvarierande primärström till sekundärspänning via järnkärnans flöde och Faradays lag.",
        concepts=("Faradays lag", "transformator", "flödeskoppling"),
        start_here='Skriv ∮H·dl=N1 i1, B=μ₀μrH, Φ=∫B·n dS och emk₂=−N2 dΦ/dt. Identifiera kärnans längd och area samt den givna tidsberoende strömmen. Sekundärlindningen är öppen: den bär ingen ström men kan ha en inducerad spänning. Bestäm först kärnflödet från den givna primärströmmen, inte från ett antaget spänningsförhållande.',
        hint_titles=('Kärnfältet från primärströmmen', 'Flöde och flödeskoppling', 'Tidsderivata och tecken'),
        hints=(
            r"""Försumma läckage och anta linjär kärna med konstant $\mu_r$. Ampères lag ger

$$
H\ell=N_1i_1(t),\qquad B=\mu_0\mu_rH.
$$""",
            r"""Flödet per varv är $\Phi=BS$. Sekundärens flödeskoppling är $N_2\Phi$, vilket ger ännu en varvtalsfaktor utöver $N_1$ i fältet.""",
            r"""Använd Faradays lag med vald positiv omloppsriktning:

$$
u_2=-N_2\frac{\mathrm d\Phi}{\mathrm dt}.
$$

När $i_1=I_0\cos(\omega t)$ ger derivatan $-\omega I_0\sin(\omega t)$, så spänningen blir positiv sinus i facits konvention.""",
        ),
        self_checks=(
            r"""Vid $t=0$ är ström och flöde maximala men spänningen noll eftersom flödesderivatan är noll. Vid en fjärdedels period är den positiva spänningen maximal i den valda konventionen.""",
            r"""Vid $\omega=0$ eller $I_0=0$ är den inducerade spänningen noll. Amplituden skalar med $N_1N_2$, $\mu_r$, S och $\omega$, och om polaritetsreferensen vänds byter hela kurvan tecken.""",
        ),
        common_pitfall=r"""Att sätta sekundärspänningen till noll för att kretsen är öppen, eller glömma $N_2$ i flödeskopplingen. Linjär $\mu_r$ är en modellförutsättning, inte en beskrivning av mättnad och hysteres.""",
        setup_hint=r"""Skriv

$$
\Phi(t)=\frac{\mu_0\mu_rN_1SI_0\cos(\omega t)}\ell
$$

och derivera $N_2\Phi$. Håll isär vinkelfrekvens $\omega$ [rad/s] och frekvens $f=\frac\omega{2\pi}$ [Hz].""",
        geometry_hint='Båda lindningarna länkar samma kärnflöde i idealmodellen. Spänningens tecken kräver en vald lindnings- och mätorientering; facits plus framför sinus är knutet till den konventionen.',
    ),
    "MovingLoopFieldWork": G(
        problem_id="9.13",
        learning_goal="Koppla mekaniskt arbete vid rörelse genom ett magnetfält till inducerad ström och resistiv värme.",
        concepts=("rörelse-emk", "Lenz lag", "energibalans"),
        start_here='Skriv Φ=∫B·n dS, ε_ems=−dΦ/dt, I=ε_ems/RΩ och W=∫I²RΩ dt för konstant fart och försumbar självinduktans. Identifiera den överlappande arean som funktion av läget innan du deriverar. Följ flödet genom slingan när dess främre kant flyttas åt +x. Fältområdet är 0<x<ℓ och slingan sträcker sig från x−a till x. Uppgiftens ℓ=30 cm är större än a=10 cm.',
        hint_titles=('När ändras arean?', 'Från inducerad ström till effekt', 'Integrera arbetet över tiden'),
        hints=(
            r"""När $\ell\geq a$ finns en inträdesfas, en fas med hela slingan inne och en utträdesfas. Endast under in- och utträde ändras överlappningsarean; då är

$$
\left|\frac{\mathrm dA}{\mathrm dt}\right|=av.
$$""",
            r"""Om slingans självinduktans försummas blir

$$
i=\frac{\varepsilon_{\mathrm{ems}}}{R_\Omega},
\qquad \varepsilon_{\mathrm{ems}}=-\frac{\mathrm d\Phi}{\mathrm dt}.
$$

Lenz lag ger en bromskraft i båda övergångarna. Vid konstant hastighet är den yttre mekaniska effekten lika med $i^2R_\Omega$.""",
            r"""Varje övergång i uppgiftens geometri varar $a/v$. Integrera effekten under båda övergångarna. Om du utforskar $\ell<a$ varar de i stället $\ell/v$; när hela fältremsan ligger inuti slingan är flödet åter konstant.""",
        ),
        self_checks=(
            r"""Med $B=1\,\mathrm T$, $a=0{,}10\,\mathrm m$, $v=10\,\mathrm{m/s}$ och $R_\Omega=0{,}05\,\Omega$ blir arbetet 0,40 J. Effekten är aldrig negativ även om emk och ström byter tecken mellan in- och utträde.""",
            r"""Vid $\ell\geq a$ är arbetet oberoende av $\ell$. För ett smalare fältområde minskar arbetet proportionellt mot $\ell$. Vid $B=0$ blir både effekt och arbete noll.""",
        ),
        common_pitfall='Att räkna bromsarbete under hela förflyttningen eller använda samma strömriktning vid in- och utträde. Resultatet förutsätter konstant fart och försumbar självinduktans; magnetkraften motverkar rörelsen.',
        visualization_note="En enkel animation av överlappningsarean A(t) kan vara mycket pedagogisk här, eftersom den direkt visar när dΦ/dt är noll respektive icke-noll.",
        setup_hint=r"""Sätt $P=\frac{(Bav)^2}{R_\Omega}$ i de två intervall där överlappningen ändras och $P=0$ annars. Använd

$$
\mathrm dt=\frac{\mathrm dx}v.
$$

För hela passagen blir övergångarnas sammanlagda längd $2\min(a,\ell)$.""",
        geometry_hint=r"""x betecknar främre kanten, inte slingans centrum eller bakre kant. Inträdet börjar vid $x=0$ och passagen är färdig vid $x=\ell+a$. För $\ell\geq a$ ligger slingan helt inne när $a\leq x\leq\ell$.""",
    ),
    "MovingLoopDipoleEmf": G(
        problem_id="9.14",
        learning_goal="Visa att tidsvarierande flöde i ett medföljande system och rörelse-emk i ett fast system beskriver samma inducerade spänning.",
        concepts=("Faradays lag", "rörelse-emk", "dipolfält"),
        start_here='Skriv ε_ems=−dΦ/dt med Φ=∫B·n dS, eller ε_ems=∮(v×B)·dℓ för den rörliga slingan i det stationära fältet. Identifiera samma orientering, hastighet och fältkomponenter i båda metoderna. Välj slingnormal +z och positiv omloppsriktning moturs sedd från +z. Slingan befinner sig vid z>0 och v=dz/dt är signerad. Approximationen kräver a≪z.',
        hint_titles=(
            r"""Del (a) · Bestäm flödet""",
            r"""Del (a) · Flödets tidsändring""",
            r"""Del (b) · Identifiera rörelseintegralens delar""",
            r"""Del (b) · Integrera och jämför""",
        ),
        hints=(
            r"""I (a) börjar du med

$$
\varepsilon_{\mathrm{ems}}=-\frac{\mathrm d\Phi}{\mathrm dt},
\qquad \Phi=\int_S\overline B\cdot\mathrm d\overline S.
$$

Välj normal $+\hat z$ och positiv omloppsriktning enligt högerhandsregeln. Eftersom $a\ll z$ är dipolfältet ungefär konstant över slingan:

$$
\Phi(z)\approx\pi a^2B_z(z),\qquad
B_z(z)=\frac{\mu_0m}{2\pi z^3}.
$$""",
            r"""Avståndet till dipolen ändras med $\mathrm dz/\mathrm dt=v$. Använd kedjeregeln på flödet du just beräknat:

$$
\varepsilon_{\mathrm{ems}}=-\frac{\mathrm d\Phi}{\mathrm dz}\,v.
$$

Behåll minustecknet från Faradays lag. För $m>0$ och $v>0$ minskar det positiva flödet, så den positiva emk:n försöker bevara det enligt Lenz lag.""",
            r"""I (b) börjar du från rörelse-emk:n i dipolens stillastående system:

$$
\varepsilon_{\mathrm{ems}}=\oint_C(\overline v\times\overline B)\cdot\mathrm d\overline\ell.
$$

På slingans rand är $\overline v=v\hat z$, $\mathrm d\overline\ell=a\,\mathrm d\phi\,\hat\phi$ och $\overline B=B_R\hat R+B_z\hat z$. Det axiella fältet ger ingen korsprodukt med hastigheten. Bestäm i stället dipolfältets radiella komponent vid $R=a$:

$$
B_R\approx\frac{3\mu_0ma}{4\pi z^4}.
$$""",
            r"""Använd $\hat z\times\hat R=\hat\phi$. Med samma positiva omloppsriktning som i (a) blir

$$
\varepsilon_{\mathrm{ems}}=\int_0^{2\pi}vB_R a\,\mathrm d\phi.
$$

Fältkomponenten $B_R$ är densamma längs randen. Utför integralen och jämför både belopp och tecken med (a). De två metoderna ger samma spänning; bidragen ska inte adderas.""",
        ),
        self_checks=(
            r"""Vid $v=0$ är emk noll. Byt tecken på antingen m eller v och emk:n byter tecken. Fördubblat z minskar beloppet med en faktor 16 i approximationen.""",
            r"""Båda beräkningssätten ska ge samma spänning med samma orientering. Den axiala komponenten ensam ger

$$
\overline v\times(B_z\hat z)=0
$$

och kan därför inte förklara rörelse-emk:n.""",
        ),
        common_pitfall='Att kasta bort det radiella fältet innan rörelseintegralen beräknas eller lägga ihop de två beskrivningssätten som två separata spänningskällor. De beskriver samma fysik.',
        setup_hint=r"""Flödesvägen: derivera $\frac{\mu_0ma^2}{2z^3}$ med

$$
\frac{\mathrm dz}{\mathrm dt}=v
$$

och använd minustecknet i Faradays lag. Rörelsevägen: multiplicera $vB_R$ vid $R=a$ med $2\pi a$.""",
        geometry_hint='Dipolen ligger i origo och slingan i ett plan vinkelrätt mot z-axeln. Positiv v betyder rörelse bort från dipolen; negativ v betyder rörelse mot den. Farten och magnetmomentet kan vändas oberoende.',
    ),

    # ------------------------------------------------------------------
    # Kapitel 10 – Förskjutningsströmmar
    # ------------------------------------------------------------------
    "DisplacementCurrentCapacitor": G(
        problem_id="10.2",
        setup_hint=r"""Välj normalen från den positivt laddade plattan mot den negativa. Skriv $D_n=\frac QA$ och

$$
i=\frac{\mathrm dQ}{\mathrm dt}
$$

med samma teckenkonvention. Derivera vid fast A: $J_{F,n}=\frac iA$. En konstant begynnelseladdning bidrar inte till tidsderivatan.""",
        geometry_hint=r"""Förskjutningsströmmen går normalt genom hela plattarean. I vakuum passerar inga fria laddningar genom gapet; $\overline J_F$ beskriver det föränderliga elektriska fältet. Avståndet d påverkar spänningen men förkortas bort ur $\overline J_F$ vid given tillförd ström.""",
        learning_goal="Se varför en tidsvarierande kondensatorström motsvaras av samma förskjutningsström genom gapet.",
        concepts=("förskjutningsström", "D-fält", "laddningskontinuitet"),
        start_here=r'Skriv $I_F=\frac{\mathrm d}{\mathrm dt}\int_S\overline D\cdot\mathrm d\overline S$ för en fast yta genom gapet. Använd Gauss lag för att koppla D-flödet till plattladdningen och $i=\mathrm dQ/\mathrm dt$ för den tillförda strömmen. För homogent fält ger division med plattarean förskjutningsströmtätheten.',
        hint_titles=('Ström och plattladdning', 'Bestäm D i gapet', 'Flödets tidsändring per area'),
        hints=(
            r"""Strömmen till en platta ges av

$$
i(t)=\frac{\mathrm dQ}{\mathrm dt}.
$$

Tecknet bestäms av den valda riktningen.""",
            r"""Utan randeffekter är D normalt mot plattorna och homogent. En Gaussbox från metallens inre till gapet ger $D_nA=Q$. Lös efter $D_n$ med samma normal som används för strömmen.""",
            r"""Förskjutningsströmmen genom den fasta plattarean är

$$
I_F=\frac{\mathrm d}{\mathrm dt}\int_S\overline D\cdot\mathrm d\overline S
=\frac{\mathrm dQ}{\mathrm dt}=i(t).
$$

Fältet är homogent, så $J_{F,n}=I_F/A$. Lägg märke till att plattavståndet $d$ inte behövs för just denna storhet.""",
        ),
        self_checks=(
            r"""Integralen av $\overline J_F$ över plattarean ska exakt ge den ledningsström i(t) som kommer fram i ledaren.""",
            r"""$\overline J_F$ ska ha samma sinusform och fas som den givna strömmen i(t), inte som plattspänningen i allmänhet.""",
        ),
        common_pitfall=r"""Att först integrera strömmen till Q(t) och sedan tappa bort att tidsderivatan i $\overline J_F$ tar tillbaka den ursprungliga strömfunktionen.""",
    ),
    "RadialChargeExpansionMaxwellTest": G(
        problem_id="10.3",
        setup_hint=r"""Använd samma inneslutna laddning i laddningsbevarande och Gauss lag:

$$
\begin{aligned}
Q_{\mathrm{in}}(r,t)&=\int_0^r\rho(s,t)\,4\pi s^2\,\mathrm ds,\\
4\pi r^2J_r&=-\frac{\mathrm dQ_{\mathrm{in}}}{\mathrm dt},\\
4\pi r^2D_r&=Q_{\mathrm{in}}.
\end{aligned}
$$

Tidsändringen av D-flödet ger $4\pi r^2J_{F,r}=\mathrm dQ_{\mathrm{in}}/\mathrm dt$. Strömtätheterna tar därför ut varandra för $r>0$. I centrum används deras reguljära gränsvärden. Tidsderivatan tas vid fast observationsradie, inte längs en laddnings bana.""",
        geometry_hint=r"""Rita en sfär med centrum i laddningsmolnet. J och $\overline J_F$ är radiella och motriktade. Symmetrin gäller hela fördelningen, inte bara en enskild laddning. Appens expanderande Gaussprofil är ett exempel med bevarad total laddning, inte en lösning för partiklarnas Coulombdrivna rörelse.""",
        learning_goal="Använd sfärisk symmetri och kontinuitet för att förstå hur ledningsström och förskjutningsström kan ta ut varandra i Ampère–Maxwells lag.",
        concepts=("sfärisk symmetri", "kontinuitetsekvationen", "Ampère–Maxwells lag"),
        start_here=(
            r"""Börja med $\oint_S\overline B\cdot\mathrm d\overline S=0$ på en sfär. Sfärisk symmetri tillåter bara ett radiellt fält, vilket då måste vara noll. För del (b), kombinera laddningsbevarande $\oint_S\overline J\cdot\mathrm d\overline S=-\mathrm dQ_{\mathrm{in}}/\mathrm dt$ med Gauss lag $\oint_S\overline D\cdot\mathrm d\overline S=Q_{\mathrm{in}}$ på samma fasta sfär."""
        ),
        hint_titles=('Strömmen ut ur en sluten sfär', 'D från laddningen innanför sfären', 'Jämför strömmarna i Ampère–Maxwells lag'),
        hints=(
            r"""För del (b), välj en fast sfär med radie $r>0$. Laddningsbevarande säger att utåtriktad ström minskar laddningen innanför:

$$
\oint_S\overline J\cdot\mathrm d\overline S
=-\frac{\mathrm dQ_{\mathrm{in}}(r,t)}{\mathrm dt}.
$$

Sfärisk symmetri ger därför

$$
4\pi r^2J_r(r,t)=-\frac{\mathrm dQ_{\mathrm{in}}(r,t)}{\mathrm dt}.
$$

Bestäm $Q_{\mathrm{in}}$ genom att integrera laddningstätheten från centrum till $r$. Håll sfärens radie fast när tiden varierar.""",
            r"""Gauss lag ger $D_r(r,t)$ från den inneslutna laddningen:

$$
4\pi r^2D_r=\int_0^r\rho(r^{\prime},t)\,4\pi(r^{\prime})^2\,\mathrm dr^{\prime}.
$$""",
            r"""Gauss lag på samma fasta sfär ger $4\pi r^2D_r=Q_{\mathrm{in}}$. Tidsändringen av D-flödet är förskjutningsströmmen:

$$
4\pi r^2J_{F,r}=\frac{\mathrm dQ_{\mathrm{in}}}{\mathrm dt}.
$$

Jämför med strömmen i första steget: $J_r+J_{F,r}=0$ vid varje radie. Ampère–Maxwells lag i integralform är

$$
\oint_C\overline H\cdot\mathrm d\overline\ell
=\int_S\overline J\cdot\mathrm d\overline S
+\frac{\mathrm d}{\mathrm dt}\int_S\overline D\cdot\mathrm d\overline S.
$$

Här är $S$ en fast yta med rand $C$. De två högerleden tar ut varandra. Det är förenligt med $B=0$, som redan följer av sfärisk symmetri och noll B-flöde genom en sluten sfär.""",
        ),
        self_checks=(
            r"""Trots att de verkliga laddningarna rör sig kan $B=0$ vara en lösning eftersom förskjutningsströmmen exakt kompenserar den radiella ledningsströmmen i Ampère–Maxwells lag.""",
            "Resultatet får inte bryta sfärisk symmetri genom att välja någon särskild axel eller azimutal riktning.",
        ),
        common_pitfall=r"Att resonera 'rörliga laddningar ger alltid $B\ne0$' utan att först kontrollera vad full sfärisk symmetri och Maxwells förskjutningsström tillåter.",
        visualization_note="Det mest värdefulla här är ett konceptdiagram som visar J och J_F som lika stora och motriktade radiella fält, snarare än en vanlig B-fältgraf.",
    ),
}


def guidance_for_problem(problem) -> SolutionGuidance | None:
    """Returnera progressiv vägledning för en ProblemBase-instans om den finns."""

    return GUIDANCE_BY_CLASS.get(problem.__class__.__name__)


def guidance_for_class_name(class_name: str) -> SolutionGuidance | None:
    """Liten hjälpfunktion för tester och andra gränssnitt."""

    return GUIDANCE_BY_CLASS.get(class_name)


__all__ = [
    "SolutionGuidance",
    "GUIDANCE_BY_CLASS",
    "guidance_for_problem",
    "guidance_for_class_name",
]
