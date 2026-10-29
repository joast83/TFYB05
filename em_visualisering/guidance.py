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
        start_here='Rita krafterna på en kula: tyngdkraft, trådspänning och elektrisk kraft. Inför θ=α/2 som trådens vinkel mot lodlinjen och välj horisontell och vertikal riktning.',
        hints=(
            'Skriv T sinθ=F_el och T cosθ=mg. Dividera ekvationerna så att den okända trådspänningen T försvinner.',
            'Kulornas avstånd är R=2ℓ sinθ. Sätt in detta i Coulombs lag F_el=Q²/(4πε₀R²); R är avståndet mellan kulorna, inte trådlängden.',
            'Använd sinθ≈θ och tanθ≈θ med θ i radianer. Kombinera kraftjämvikten med Coulombs lag, samla potenserna av θ och byt sist tillbaka till α=2θ.',
        ),
        self_checks=(
            'Ökar vinkeln när |Q| ökar, och minskar den när m eller ℓ ökar? Kontrollera även gränsen Q→0.',
            'Uttrycket för α ska vara dimensionslöst. Sätt in värdena och kontrollera att α verkligen är mycket mindre än 1 radian; annars är småvinkelapproximationen inte tillförlitlig.',
        ),
        common_pitfall='Att använda α som trådens vinkel mot lodlinjen i stället för α/2.',
        setup_hint='Eliminera T genom att dividera den horisontella jämviktsekvationen med den vertikala. Då återstår en ekvation för θ med F_el/(mg) i högerledet.',
        geometry_hint='Rita en lodlinje från upphängningen. Varje kula ligger ℓ sinθ från lodlinjen, så avståndet mellan kulorna är dubbelt så stort. Vinkeln α är hela öppningsvinkeln.',
    ),
    'ChargedRingAxis': G(
        problem_id='2.2',
        learning_goal='Använd symmetri för att reducera en vektorintegral till en enda komponent.',
        concepts=(
            'Coulombs lag',
            'superposition',
            'symmetri',
        ),
        start_here='Para ihop två laddningselement på motsatta sidor av ringen. Vilka komponenter av deras fält tar ut varandra vid punkten (0,0,z)?',
        hints=(
            'Tvärkomponenterna tar ut varandra. Alla källelement har samma avstånd R=√(a²+z²) till fältpunkten, men bara projektionen på z-axeln ska summeras.',
            'Parametrisera ringen med φ: dQ=λa dφ, där λ=Q/(2πa). Den signerade z-projektionen av separationsvektorn är z.',
            'Skriv dE_z=z dQ/(4πε₀R³). Faktorn framför dQ är konstant runt ringen; integrera dQ över hela ringen utan att ersätta z med |z|.',
        ),
        self_checks=(
            'Fältet ska vara noll vid z=0 och E_z ska byta tecken när z byter tecken.',
            'För |z|≫a ska fältet närma sig punktladdningsfältet. För Q>0 ska det peka bort från ringen på båda sidor.',
        ),
        common_pitfall='Att integrera fältets belopp och glömma att dE är en vektor.',
        visualization_note='En axelgraf är användbar först efter härledningen, framför allt för att kontrollera z=0 och fjärrfältet.',
        setup_hint='Börja med vektorformen dE=dQ R⃗/(4πε₀|R⃗|³). Ta z-komponenten innan du integrerar; då återstår endast en konstant geometrifaktor gånger ∫dQ.',
        geometry_hint='Källpunkten är (a cosφ,a sinφ,0) och fältpunkten är (0,0,z). Rita vektorn från källpunkten till fältpunkten och jämför med det diametralt motsatta elementet.',
    ),
    'FiniteLineCharge2D': G(
        problem_id='2.3',
        learning_goal='Sätt upp Coulombintegralen för en ändlig linjeladdning och tolka gränsen mot en oändlig tråd.',
        concepts=(
            'linjeladdning',
            'vektorintegral',
            'gränsvärde',
        ),
        start_here='Låt källkoordinaten vara z′ på tråden, från −b till a. Skriv vektorn från (0,0,z′) till fältpunkten (x,0,0) innan du väljer komponenter.',
        hints=(
            'Separationsvektorn är x x̂−z′ ẑ och dess längd är √(x²+z′²). Använd dQ=ρℓ dz′.',
            'Sätt upp separata integraler för E_x och E_z med samma nämnare (x²+z′²)^(3/2). I E_z-integralen hjälper substitutionen u=x²+z′²; i E_x kan du använda z′=|x|tanθ.',
            'För del (b), låt båda ändpunkterna gå långt bort medan x hålls fixerat och skilt från noll. Undersök gränsvärdet av varje ändpunktsterm; a och b behöver inte vara lika.',
        ),
        self_checks=(
            'Om a=b ska E_z försvinna. Om a>b och ρℓ>0 ska E_z vara negativ vid (x,0,0), eftersom mer positiv laddning ligger på +z-sidan.',
            'I den oändliga gränsen ska E_z→0 och |E_x| avta som 1/|x|. Fältet ska peka bort från tråden för positiv linjeladdning.',
        ),
        common_pitfall='Att anta cylindersymmetri redan i del (a), trots att tråden där är ändlig och kan vara osymmetrisk kring origo.',
        setup_hint='Integralerna har täljarna x respektive −z′. Behåll x konstant under integrationen och sätt in gränserna −b och a först efter att du har hittat primitiva funktioner.',
        geometry_hint='Använd olika symboler för källpunkten z′ och fältpunkten x. Vektorn går från laddningen till observationspunkten, så dess z-komponent är −z′ även om x är positivt.',
    ),
    'SemiCircularSurfaceAxis': G(
        problem_id='2.4',
        learning_goal='Hantera en ytladdningsintegral där endast en del av symmetrin finns kvar.',
        concepts=(
            'ytladdning',
            'polära koordinater',
            'komponentsymmetri',
        ),
        start_here='I appens skiss ligger halvcirkelskivan i xy-planet på sidan y≥0. Para ihop källpunkter med motsatta x-koordinater och avgör vilken fältkomponent som försvinner vid (0,0,z).',
        hints=(
            'Använd källpunkten (R cosφ,R sinφ,0), med 0≤R≤a och 0≤φ≤π. Ytelementet är dS=R dR dφ och dQ=ρs dS.',
            'Separationsvektorn är −R cosφ x̂−R sinφ ŷ+z ẑ och dess längd är √(R²+z²). Integrera vinkelberoendet i varje komponent innan du gör radialintegralen.',
            'Integralen av cosφ över halvcirkeln är noll, medan integralen av sinφ inte är det. För z-komponenten är vinkelintegralen bara π. Behandla därefter de två återstående radialintegralerna var för sig.',
        ),
        self_checks=(
            'För ρs>0 och z>0 ska E_x=0, E_y<0 och E_z>0. Kontrollera riktningarna mot den valda halvcirkeln.',
            'Långt bort ska den ledande termen vara punktladdningsfältet för Q=ρsπa²/2; tvärkomponenten avtar snabbare. Punkten z=0 ligger på skivans kant och är inte ett vanligt reguljärt kontrollvärde.',
        ),
        common_pitfall='Att låna symmetrin från en hel skiva och därför sätta alla tvärkomponenter till noll.',
        setup_hint='Sätt in dS och separationsvektorn i dE=ρs R⃗ dS/(4πε₀|R⃗|³). Skilj på den radiella källkoordinaten R och avståndet |R⃗| till fältpunkten.',
        geometry_hint='Halvcirkeln är spegelsymmetrisk under x→−x men inte under y→−y. Det räcker för att eliminera E_x, men ger inget skäl att sätta E_y till noll.',
    ),
    'SphericalShellPotential': G(
        problem_id='2.5',
        learning_goal='Beräkna potential direkt från en laddningsintegral och förstå varför resultatet blir styckvis.',
        concepts=(
            'potentialintegral',
            'sfärisk symmetri',
            'källområde',
        ),
        start_here='Använd potentialintegralen som uppgiften efterfrågar. Sfärisk symmetri gör att du kan placera observationspunkten på z-axeln på avståndet r från centrum.',
        hints=(
            'Ytladdningstätheten är ρs=Q/(4πa²) och dS=a²sinθ dθ dφ. Avståndet från källelementet till fältpunkten är √(r²+a²−2ar cosθ).',
            'Integrera först över φ och använd sedan u=cosθ. För r>0 kan du nu integrera en funktion av formen 1/√(r²+a²−2aru).',
            'Vid integrationsgränserna får du r+a och |r−a|. Dela därför upp r<a och r>a innan du förenklar. Vid r=0 kan du använda att alla källelement ligger på avståndet a, utan att dividera med r.',
        ),
        self_checks=(
            'V ska vara kontinuerlig vid r=a och gå mot noll när r→∞.',
            'Kontrollera med E_r=−dV/dr: inuti ska fältet vara noll och utanför ska det ha punktladdningens 1/r²-beroende. Derivatan får däremot ha ett språng vid den laddade ytan.',
        ),
        common_pitfall='Att försöka använda E-fältets Gauss-lösning när uppgiften uttryckligen vill att potentialintegralen genomförs.',
        setup_hint='Integrera över sfärens yta, inte dess volym. Integralen över φ ger 2π; θ-integralen innehåller sinθ dθ, vilket gör u=cosθ till ett naturligt variabelbyte.',
        geometry_hint='Skilj observationsradien r från skalets fasta radie a. Cosinussatsen för triangeln mellan centrum, källpunkten och fältpunkten ger avståndet i nämnaren.',
    ),
    'ConcentricChargedCylinders': G(
        problem_id='2.6',
        learning_goal='Välja rätt Gaussyta och hålla reda på vilken laddning som omsluts i olika radialområden.',
        concepts=(
            'Gauss lag',
            'cylindersymmetri',
            'styckvis fält',
        ),
        start_here='Försumma ändeffekter för de långa cylindrarna. Dela upp rummet i R<a, a<R<b och R>b och rita en koaxial Gauss-cylinder i varje område.',
        hints=(
            'Symmetrin ger ett radiellt E som är konstant på Gauss-cylinderns mantel. Flödet genom ändytorna är noll och mantelytans area är 2πRL.',
            'Skilj på Gaussytans radie R och de laddade ytornas radier a och b. Deras laddningar per längd L är ρsa·2πaL respektive ρsb·2πbL.',
            'Summera bara de laddade ytor som ligger innanför respektive Gaussyta. Sätt sedan E_R·2πRL=Q_in/ε₀ och låt E_R behålla sitt tecken.',
        ),
        self_checks=(
            'För R<a är fältet noll. Utanför båda cylindrarna ska det också bli noll om aρsa+bρsb=0, även om vardera cylindern är laddad.',
            'Med normalen riktad mot större R ska E_R(utanför)−E_R(innanför)=ρs/ε₀ vid varje laddad yta. Kontrollera båda sprången.',
        ),
        common_pitfall='Att använda samma inneslutna laddning i alla tre radialområden.',
        setup_hint='Gör en tabell med de tre radialområdena och Q_in i varje rad. Samma flödesuttryck gäller i alla rader; det är den inneslutna laddningen som ändras.',
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
        start_here='Ytterradien b och det tillåtna fältet Emax är givna. Bestäm först var i gapet |E(r)| är störst; där begränsas den tillåtna laddningen.',
        hints=(
            'Använd en sfärisk Gaussyta i a<r<b. Fältets belopp avtar som 1/r², så gränsen sätts precis utanför den inre ledaren.',
            'För varje vald radie a kan laddningens belopp ökas tills |E(a)|=Emax. Uttryck därför |Q|max som funktion av a; laddningen är inte konstant i optimeringen.',
            'Integrera fältet från a till b för att få spänningens belopp och sätt in |Q|max(a). Derivera funktionen av a med b och Emax konstanta och kontrollera både den stationära punkten och randgränserna.',
        ),
        self_checks=(
            'Vid genomslagsbegränsad laddning ska den tillåtna spänningen gå mot noll när a→0 och när a→b. Ett inre maximum måste jämföras med dessa gränser.',
            'Den stationära punkten ska ligga i 0<a<b och ha negativ andraderivata. Enheten i spänningsuttrycket ska vara Emax gånger en längd.',
        ),
        common_pitfall='Att optimera kondensatorns vanliga spänningsuttryck med Q konstant, trots att Q här begränsas av Emax och därför beror på a.',
        setup_hint='Skriv först U_max(a)=∫_a^b |E(r;Q_max(a))| dr. Först efter att Q_max uttryckts med a är det rätt funktion att derivera.',
        geometry_hint='Rita de två radierna och ett godtyckligt r i gapet. Det minsta tillåtna r i luften är a, vilket är varför det största fältet uppstår där.',
    ),
    'ConcentricSphericalShells': G(
        problem_id='2.8',
        learning_goal='Bygga en styckvis potential genom superposition och använda ledarvillkor efter sammankoppling.',
        concepts=(
            'superposition',
            'sfärskal',
            'elektrostatisk ledare',
        ),
        start_here='I del (a) är Qa och Qb givna. Bygg potentialen genom att lägga ihop bidragen från två jämnt laddade sfärskal med samma referens V(∞)=0.',
        hints=(
            'Ett skals potential är konstant innanför skalet och motsvarar en punktladdnings potential utanför. Skriv bidragen separat i r<a, a<r<b och r>b.',
            'Summera sedan de två bidragen i varje område. Kontrollera att samma potential nås från båda sidor av varje skal innan du går vidare till del (b).',
            'I del (b), kalla de nya laddningarna qa och qb. Använd både qa+qb=Qa+Qb och V(a)=V(b) under förbindelsen. Sätt in potentialerna från del (a) med de nya laddningarna och lös dessa två villkor.',
        ),
        self_checks=(
            'Potentialen ska vara kontinuerlig vid a och b och närma sig noll vid oändligheten. Utanför b beror den bara på den sammanlagda laddningen.',
            'Efter förbindelsen ska laddningen vara bevarad och potentialskillnaden mellan skalen vara noll. I den sfäriskt symmetriska modellen ska resultatet också ge noll fält i gapet.',
        ),
        common_pitfall='Att bevara Qa och Qb var för sig efter sammankopplingen, eller anta att ett tomt område alltid har E=0. Här måste fältet i gapet följa av potentialvillkoret och geometrin.',
        setup_hint='För del (b): byt namn på de okända slutladdningarna och skriv två oberoende ekvationer, en för bevarad total laddning och en för lika potential. Använd inte de ursprungliga laddningarna som om de vore låsta.',
        geometry_hint='Markera ett observationsläge i vart och ett av de tre radialområdena. För varje skal, fråga om punkten ligger innanför eller utanför just det skalet innan du skriver dess potentialbidrag.',
    ),
    "AtmosphericChargeDensity": G(
        problem_id="2.9",
        learning_goal="Översätta en observerad fältändring till medelladdning via Gauss lag/divergens.",
        concepts=("Gauss lag", "fältgradient", "teckenkonvention"),
        start_here="Välj z uppåt och skriv de givna vertikala fälten som signerade z-komponenter innan du använder några belopp.",
        hints=(
            'Välj z uppåt: E_z(0)=−300 V/m och E_z(h)=−20 V/m, där h=1400 m. Betrakta en vertikal cylinder med tvärsnittsarea S; fältet har inget flöde genom mantelytan i denna modell.',
            'På ovansidan är normalen +ẑ, på undersidan −ẑ. Det totala utåtriktade flödet blir därför S[E_z(h)−E_z(0)], trots att båda fälten pekar nedåt.',
            'Använd Q_inne=ε0Φ och dividera med volymen Sh. Detta ger medeltätheten; två fältvärden räcker inte för att bestämma hur laddningen varierar med höjden.',
        ),
        self_checks=(
            'S ska förkortas bort och ε0ΔE/h ha enheten C/m³.',
            'Medeltätheten ska vara positiv eftersom E_z ökar med höjden. Om fälten vore lika skulle medeltätheten vara noll, även om lokal laddning kunde finnas.',
        ),
        common_pitfall="Att subtrahera fältens belopp utan att först ta hänsyn till ytornas normalriktningar.",
        geometry_hint='Rita två nedåtpilar, en vid marken och en vid h. Rita sedan utåtnormalerna separat: uppåt på toppen och nedåt på botten. Det är skalärprodukterna E·n som bestämmer flödets tecken.',
        setup_hint='Skriv ⟨ρ⟩Sh=ε0S[E_z(h)−E_z(0)]. Sätt in signerade fältkomponenter innan du förenklar; anta inte att ρ(z) är konstant.',
    ),
    "OffsetCavitySphereExterior": G(
        problem_id="2.10",
        learning_goal="Använd superposition för att ersätta ett hålrum med en negativ laddningsfördelning.",
        concepts=("superposition", "homogent laddat klot", "förskjutet centrum"),
        start_here="Tänk det verkliga objektet som ett helt laddat klot plus ett mindre klot med laddningstäthet −ρ där hålrummet finns.",
        hints=(
            'Fyll först hålrummet med samma täthet ρ som resten. Lägg därefter till ett mindre klot med täthet −ρ för att återställa hålrummet. Dess laddning är negativ när ρ>0.',
            'För x>b ligger punkten utanför båda kloten. Använd därför deras laddningar Q_stor=4πρb³/3 och Q_hål=−4πρa³/3 som punktladdningar i respektive centrum.',
            'I appens skiss ligger hålrummets centrum vid x=−d. Avstånden till punkten x är alltså x och x+d. Summera de signerade x-komponenterna av Coulombfälten.',
        ),
        self_checks=(
            'När a→0 ska hålrummets bidrag försvinna. När d→0 ska resultatet motsvara nettoladdningen i origo.',
            'Långt bort, x≫b,d, ska den ledande termen vara fältet från nettoladdningen 4πρ(b³−a³)/3. För ρ>0 ska E_x vara positivt på den angivna delen av x-axeln.',
        ),
        common_pitfall="Att använda avståndet x till båda sfärernas centrum trots att hålrummets centrum är förskjutet.",
        geometry_hint='Markera centrum 0, hålrummets centrum −d och observationspunkten x>b på samma axel. Kontrollera avstånden i din egen skiss: ett hålrum vid +d skulle i stället ge avståndet x−d.',
        setup_hint='Skriv E_x=k[Q_stor/x²+Q_hål/(x+d)²], med k=1/(4πε0). Tecknet från den negativa hjälpladdningen ingår redan i Q_hål; lägg inte in ännu ett minustecken.',
    ),
    "CoaxialCylinderVoltage": G(
        problem_id="2.11",
        learning_goal="Gå från Gauss-lagens koaxialfält till ett givet spänningsfall.",
        concepts=("koaxial geometri", "Gauss lag", "potentialskillnad"),
        start_here="Bestäm först den allmänna formen E(R)=C/R mellan cylindrarna; bestäm sedan konstanten från spänningen U.",
        hints=(
            'En cylindrisk Gaussyta mellan skalen ger |E_R|=K/R. Ändeffekter försummas eftersom cylindrarna är långa.',
            'Integrera fältbeloppet genom gapet: U=∫_a^b K/R dR=K ln(b/a). Bestäm K från den givna spänningen, utan att behöva beräkna laddningen separat.',
            'Mittemellan ytorna är R=a+(b−a)/2. Sätt in denna radie i fältuttrycket först när K är bestämd.',
        ),
        self_checks=(
            'Uttrycket ska ha enheten V/m och vara proportionellt mot U. Logaritmens argument b/a ska vara dimensionslöst.',
            'I ett tunt gap, b−a≪a, ska fältet närma sig plattkondensatorns U/(b−a). Generellt avtar fältbeloppet som 1/R.',
        ),
        common_pitfall="Att anta ett homogent fält U/(b−a), vilket inte gäller för cylindrisk geometri.",
        geometry_hint='R mäts från den gemensamma axeln, inte från innerledarens yta. Halva gapbredden (b−a)/2 måste därför läggas till a.',
        setup_hint='Skriv U=K ln(b/a) och lös ut K innan du använder R=(a+b)/2. Uppgiften efterfrågar ett belopp; fältriktningen kräver dessutom att du anger vilken ledare som har högre potential.',
    ),
    "SphericalConductorBreakdown": G(
        problem_id="2.12",
        learning_goal="Koppla luftens genomslagsfält till maximal laddning och potential på en sfärisk ledare.",
        concepts=("ledande sfär", "genomslag", "potential"),
        start_here="Var är fältet från en laddad ledande sfär störst? Applicera Emax just där.",
        hints=(
            'För en ensam sfärisk ledare är fältet noll inne i metallen. Strax utanför ytan är beloppet |Q|/(4πε0a²), och längre bort avtar det som 1/r².',
            'Sätt fältbeloppet vid r=a lika med Emax och lös ut den största tillåtna laddningens belopp. Villkoret gäller både positiv och negativ laddning.',
            'Med V(∞)=0 är ytpotentialen Q/(4πε0a). Använd laddningsgränsen från förra steget och sätt sedan in a=0,10 m samt Emax=3·10⁶ V/m i del (b).',
        ),
        self_checks=(
            'Qmax ska växa som a², medan den maximala potentialens belopp växer som a. Kontrollera enheterna C respektive V.',
            'Kvoten |V(a)|/a ska vara Emax vid gränsen. Potentialen har samma tecken som Q, medan genomslagsvillkoret beror på fältets belopp.',
        ),
        common_pitfall="Att sätta genomslagsvillkoret vid någon godtycklig punkt utanför sfären i stället för på ytan.",
        geometry_hint='Markera r=a precis på luftsidan av metallytan. Där är det yttre fältet störst; fältet inne i metallen kan inte användas för luftens genomslagsvillkor.',
        setup_hint='Börja med |Q|/(4πε0a²)≤Emax. Lös laddningsgränsen först och använd sedan V(a)=Q/(4πε0a); byt inte ut a mot en godtycklig observationsradie.',
    ),
    "CoaxialTubeSpaceCharge": G(
        problem_id="2.13",
        learning_goal="Lösa Poisson/Gauss-problemet i cylindrisk geometri när det finns en konstant rymdladdning.",
        concepts=("rymdladdning", "cylindrisk Gauss lag", "randvillkor"),
        start_here="Anta E=E(R) R̂. Använd först Gauss lag i differential- eller integralform för att hitta den allmänna radialformen när ρ är konstant.",
        hints=(
            'I gapet gäller (1/R)d(RE_R)/dR=ρ/ε0. Integrera till E_R=ρR/(2ε0)+C/R; fältet är inte enbart proportionellt mot 1/R eftersom gapet innehåller laddning.',
            'Använd E_R(a)=0 för att bestämma C. Därmed återstår bara ρ som okänd i E_R(R).',
            'Skriv U=V(b)−V(a)=−∫_a^b E_R dR och bestäm ρ. Multiplicera sedan med elektronmolnets volym π(b²−a²)ℓ för att få dess totala laddning, inte laddningen per längdenhet.',
        ),
        self_checks=(
            'Kontrollera både E_R(a)=0 och att −∫_a^b E_R dR=+300 V. Med denna spänning ska ρ och molnets totala laddning vara negativa.',
            'För negativ ρ ska E_R peka inåt i gapet, medan kraften på en elektron pekar utåt. Q ska vara proportionell mot ℓ, och ha enheten C.',
        ),
        common_pitfall="Att använda det laddningsfria koaxialfältet C/R trots att området innehåller konstant rymdladdning.",
        geometry_hint='R löper från katodens radie a till anodens radie b. Molnet fyller ett cylindriskt skal, så dess volym är skillnaden mellan två cylindervolymer. Modellen försummar ändeffekter.',
        setup_hint='Efter villkoret vid a får du E_R=ρ(R−a²/R)/(2ε0). Integrera detta med minustecknet i U=−∫E_R dR. Använd meter för a, b och ℓ.',
    ),
    "RadialChargeSphere": G(
        problem_id="2.16",
        learning_goal="Välja den kortaste vägen till potentialen i centrum för en sfäriskt symmetrisk laddningsfördelning.",
        concepts=("potential", "sfäriska skal", "rymdladdning"),
        start_here="För just V(0) är det enklare att summera potentialbidrag från tunna sfäriska skal än att först bestämma E(r) överallt.",
        hints=(
            'Välj källradien r′ för ett tunt sfäriskt skal: dQ=4πr′²A(a−r′)dr′. Observationspunkten är hela tiden centrum.',
            'Alla delar av detta skal ligger lika långt, r′, från centrum. Potentialbidragen adderas som skalärer: dV=dQ/(4πε0r′).',
            'Integrera från r′=0 till a. V(∞)=0 är inbyggt i Coulombpotentialen. Det finns inget bidrag från r′>a eftersom tätheten är noll där.',
        ),
        self_checks=(
            'Efter förenkling är integranden proportionell mot r′(a−r′); den går mot noll i centrum trots faktorn 1/r′ i potentialkärnan.',
            'A har enheten C/m⁴. Potentialen ska skala som Aa³/ε0 och ha samma tecken som A. Symmetrin ger E(0)=0, men inte V(0)=0.',
        ),
        common_pitfall='Att sätta V(0)=0 för att fältet är noll i centrum, eller ersätta hela fördelningen med en punktladdning när observationspunkten ligger inuti den.',
        geometry_hint='Skilj på observationspunkten r=0 och källskalets radie r′. Avståndet i Coulombpotentialen är r′; det är inte noll bara för att observationspunkten ligger i origo.',
        setup_hint='Skriv V(0)=(1/ε0)∫₀ᵃ A(a−r′)r′ dr′. Faktorn r′ kommer från skalets area r′² dividerad med avståndet r′. Integrera de två potenstermerna var för sig.',
    ),
    "InsertedMetalPlateCapacitor": G(
        problem_id="2.18",
        learning_goal="Skilja på vad som hålls konstant före och efter att batteriet kopplats bort.",
        concepts=("plattkondensator", "konstant laddning", "ledare i fält"),
        start_here="Markera tidsordningen: kondensatorn laddas med batteriet anslutet, sedan kopplas batteriet bort. Vad är därför bevarat i del (b) och (c)?",
        hints=(
            'I del (a) bestäms laddningsbeloppet av Q=(ε0A/d0)U. Plattorna bär +Q respektive −Q. Omvandla 500 cm² till m² och alla avstånd till meter.',
            'I del (b) är Q bevarad efter att batteriet kopplats bort. En metallplatta som inte vidrör elektroderna har E=0 inuti. Spänningsfallet ligger därför bara över luftgapens sammanlagda tjocklek d0−d1.',
            'Del (c) är ett alternativ till del (b): ingen metallplatta är införd. Behåll laddningen från del (a), använd E=Q/(ε0A) och det nya avståndet d2.',
        ),
        self_checks=(
            'I del (b) ska spänningen minska med faktorn (d0−d1)/d0; i del (c) ska den öka med faktorn d2/d0. Båda jämförs med ursprungsspänningen.',
            'Om d1→0 återfås ursprungsspänningen. Metallplattans placering i gapet ändrar inte resultatet i idealmodellen, så länge den inte vidrör elektroderna och kanteffekter försummas.',
        ),
        common_pitfall='Att hålla U konstant efter att batteriet kopplats bort, eller använda d2−d1 i del (c) trots att metallinsättning och ökat avstånd är alternativa försök.',
        geometry_hint='Rita två separata skisser: (b) två luftgap plus en metallplatta, (c) ett enda luftgap med bredd d2. Inuti metallen är potentialen konstant; bara luftgap bidrar till spänningsfallet.',
        setup_hint='Beräkna Q en gång i del (a). Skriv sedan U_b=Q(d0−d1)/(ε0A) och U_c=Qd2/(ε0A). Fråga i varje steg vad som är låst: här är det laddningen, inte spänningen.',
    ),
    "UniformSpaceChargePlates": G(
        problem_id="2.19",
        learning_goal="Kombinera Poissons ekvation med en föreskriven potentialskillnad och sedan lokalisera E=0.",
        concepts=("Poissons ekvation", "1D-fält", "randvillkor"),
        start_here='Använd samma koordinat som i appens skiss: x=0 vid plattan med V0 och x=d vid den jordade plattan. Då är V(0)=V0 och V(d)=0.',
        hints=(
            'Med konstant ρ0 ger Gauss lag dE_x/dx=ρ0/ε0. Integrera till E_x=ρ0x/ε0+C; konstanten bestäms inte av laddningstätheten ensam.',
            'Använd V(d)−V(0)=−V0=−∫₀ᵈ E_x dx. Detta bestämmer C. Kontrollera minustecknet med E_x=−dV/dx.',
            'För ρ0≠0: lös E_x(x0)=0 och kräv sedan 0<x0<d för en nollpunkt inne i gapet. Gränsfallen x0=0 och x0=d ligger på plattornas ytor, inte strikt mellan dem.',
        ),
        self_checks=(
            'E_x ska vara linjärt med lutningen ρ0/ε0 och dess integral över gapet ska vara V0. Om V0=0 och ρ0≠0 ligger nollpunkten mitt i gapet.',
            'Villkoret för en inre nollpunkt blir |V0|<|ρ0|d²/(2ε0); likhet placerar nollpunkten på en yta. För ρ0=0 måste fallet behandlas separat: E_x=V0/d är konstant och är noll överallt endast om V0=0.',
        ),
        common_pitfall='Att blanda ihop vilken platta som ligger vid x=0, eller rapportera en algebraisk nollpunkt utanför gapet som en fysisk lösning mellan plattorna.',
        geometry_hint='Markera 0 vid V0-plattan och d vid jord. Om du i stället mäter från den jordade plattan måste du omvandla koordinaten med x_ny=d−x; samma fysiska punkt får då ett annat koordinatvärde.',
        setup_hint='Skriv ∫₀ᵈ(ρ0x/ε0+C)dx=V0. Bestäm C innan du löser E_x=0. Dividera inte med ρ0 utan att först ange antagandet ρ0≠0.',
    ),

    # ------------------------------------------------------------------
    # Kapitel 3 – Dielektriska material
    # ------------------------------------------------------------------
    "HClDipoleField": G(
        problem_id="3.1",
        learning_goal="Se hur två motsatta punktladdningar övergår i dipolfält när observationsavståndet är stort.",
        concepts=("elektrisk dipol", "superposition", "fjärrfältsapproximation"),
        start_here='Rita H⁺ vid z=d/2 och Cl⁻ vid z=−d/2. Skriv först riktningen för varje laddnings fält i observationspunkten; summera komponenter innan du tar belopp.',
        hints=(
            'På positiva z-axeln utanför molekylen pekar bidragen åt motsatta håll. Avstånden är r0−d/2 till H⁺ och r0+d/2 till Cl⁻; den närmare positiva laddningen ger det större bidraget.',
            'På y-axeln är avstånden lika, √(r0²+d²/4). Y-komponenterna tar ut varandra och z-komponenterna adderas i negativ z-riktning.',
            'Använd d/r0≪1 för att utveckla det exakta uttrycket. Behåll första termen som inte tar ut sig. Sätt in e, d=0,218 Å och r0=10 Å först efter att avstånden omvandlats till meter.',
        ),
        self_checks=(
            'Med dipolmoment p=ed i positiv z-riktning ska fjärrfältet på positiva z-axeln peka längs p och på y-axeln motsatt p.',
            'Båda beloppen ska avta som 1/r0³. Axelfältet blir ungefär dubbelt så stort som ekvatorialfältet; detta är en fjärrfältsrelation, inte en exakt relation nära laddningarna.',
        ),
        common_pitfall='Att addera de två fältbeloppen på z-axeln trots att bidragen är motriktade, eller anta att nettoladdning noll innebär fält noll.',
        geometry_hint='Rita två separata observationspunkter: (0,0,r0) och (0,r0,0). Avståndet r0 mäts från molekylens mittpunkt, inte från någon av jonerna.',
        setup_hint='Sätt k=1/(4πε0). På positiva z-axeln: E_z=ke[(r0−d/2)⁻²−(r0+d/2)⁻²]. På y-axeln: projicera varje Coulombfält på z innan du summerar. Ta belopp sist.',
    ),
    "PorcelainSlabCapacitor": G(
        problem_id="3.3",
        learning_goal="Använd randvillkor för D och spänningssumman över två seriekopplade materialskikt.",
        concepts=("D-fält", "dielektrikum", "seriekopplade skikt"),
        start_here='Rita porslin och luft som två skikt efter varandra mellan plattorna. Fältet är normalt mot materialgränsen; ingen fri laddning finns på denna gräns.',
        hints=(
            'En tunn Gaussbox över materialgränsen ger D_n,luft=D_n,porslin. Sätt det gemensamma beloppet till D. Detta innebär inte att E är lika i skikten.',
            'Använd E_luft=D/ε0 och E_porslin=D/(6ε0). De två skikten är vardera 0,005 m tjocka.',
            'Summera spänningsfallen: 10⁴ V=E_luft d_luft+E_porslin d_porslin. Bestäm D ur denna ekvation och beräkna sedan båda E-fälten.',
        ),
        self_checks=(
            'E_luft/E_porslin ska vara 6, medan D är samma i båda skikten. D har enheten C/m² och E har enheten V/m.',
            'Spänningsfallen ska summera till 10 kV. Om εr sätts till 1 ska modellen ge det homogena fältet U/d.',
        ),
        common_pitfall='Att fördela spänningen lika bara för att skikten är lika tjocka, eller kräva kontinuitet för E_n när det är D_n som är kontinuerligt.',
        geometry_hint='Materialgränsen är parallell med metallplattorna. En väg från den ena plattan till den andra passerar båda materialen; potentialfallen adderas som för seriekopplade skikt.',
        setup_hint='Skriv D=U/[d_luft/ε0+d_porslin/(ε0εr)]. Använd hela plattavståndet för att bestämma d_luft=d−d_porslin, inte d som luftgapets tjocklek.',
    ),
    "GroundedInnerSphereChargeSplit": G(
        problem_id="3.6",
        learning_goal="Kombinera Gauss lag, laddningskonservering och ett jordningsvillkor för en flerledargeometri.",
        concepts=("jordad ledare", "sfärisk symmetri", "dielektrikum"),
        start_here='Inför fria laddningar q på den jordade kulan, q_in på plåtskalets insida och q_ut på dess utsida. Bara det yttre skalets totala laddning är låst till Q; den jordade kulan kan utbyta laddning med jorden.',
        hints=(
            'En Gaussyta inne i skalets metall ger q+q_in=0. Det isolerade yttre skalet ger dessutom q_in+q_ut=Q.',
            'I gapet a<r<3a är E_r=q/(4πε0εr r²). Utanför skalet är nettoladdningen q+Q=q_ut och mediet vakuum. Integrera dessa två fält med rätt permittivitet.',
            'Jordningen ger V(a)=∫_a^(3a) E_gap dr+∫_(3a)^∞ E_ut dr=0. Ersätt q med −q_in och lös relationen mellan q_ut och q_in innan du sätter εr=2,5.',
        ),
        self_checks=(
            'Laddningarna på skalets båda sidor ska summera till Q, och den beräknade potentialen på den inre kulan ska vara noll.',
            'Kvoten q_ut/q_in ska vara 2/εr för denna geometri, alltså 0,8 vid εr=2,5. För Q>0 är båda skalytorna positivt laddade och den jordade kulan negativ.',
        ),
        common_pitfall='Att bevara laddningen på den jordade kulan, eller använda en enda permittivitet i en potentialintegral som går genom både dielektrikum och vakuum.',
        geometry_hint='Dela den radiella integrationsvägen vid 3a. Jordningen gäller kulan vid a, inte det yttre skalet. Hålet och tråden försummas enligt uppgiftens antagande om sfärisk symmetri.',
        setup_hint='Skriv 0=q(1/a−1/(3a))/(4πε0εr)+q_ut/(4πε0·3a). Tillsammans med q=−q_in bestämmer detta kvoten; använd sedan q_in+q_ut=Q om enskilda laddningar behövs.',
    ),
    "ChargedDielectricShell": G(
        problem_id="3.7",
        learning_goal="Lösa E och V styckvis i en sfäriskt symmetrisk geometri med både vakuum och dielektrikum.",
        concepts=("Gauss lag för D", "styckvis medium", "potentialkontinuitet"),
        start_here='Dela radien i tre områden: hålrummet r<a, materialet a<r<b och vakuumet r>b. Här behandlas ρ0 som fri rymdladdningstäthet, som i appens modell och facit.',
        hints=(
            'Använd 4πr²D_r=Q_fri,in. Den inneslutna laddningen är noll i hålrummet, 4πρ0(r³−a³)/3 i materialet och 4πρ0(b³−a³)/3 utanför.',
            'Omvandla D till E med ε0εr i materialet och ε0 i vakuum. Eftersom ingen fri ytladdning anges är D_n kontinuerligt vid materialgränserna; E_n behöver inte vara det.',
            'Sätt V(∞)=0. Bestäm först V(b) från det yttre fältet, sedan V(r)=V(b)+∫_r^b E_material(s)ds i skalet. Inne i hålrummet är V konstant och lika med V(a).',
        ),
        self_checks=(
            'V ska vara kontinuerlig vid a och b och uppfylla −dV/dr=E_r inom varje område. E=0 i hålrummet betyder inte att V där är noll.',
            'Vid b ska ε0εr E_r(b⁻)=ε0E_r(b⁺). Utanför är fältet oberoende av εr när den fria laddningen hålls fast; för εr=1 försvinner permittivitetssprånget.',
        ),
        common_pitfall='Att tolka ρ0 som total laddningstäthet samtidigt som Gauss lag för D används, eller sätta potentialens integrationskonstant separat till noll i varje område.',
        geometry_hint='Rita en sfärisk Gaussyta i varje region. I skalet omsluts bara material mellan a och observationsradien r; vakuumhålet bidrar inte med laddning.',
        setup_hint='Beräkna Q_fri,in med skalvolymen, inte med hela klotvolymen. Behåll V(b) som randvärde när du integrerar inåt; detta undviker tre oberoende och felaktiga potentialreferenser.',
    ),
    "DielectricFilledSphericalGap": G(
        problem_id="3.9",
        learning_goal="Använd ett gränsvillkor geometriskt: E är tangentiellt mot gränsytan mellan de två dielektrika.",
        concepts=("randvillkor", "E och D", "sfärisk Gaussyta"),
        start_here='Materialen fyller var sitt halvklot i gapet, inte två radiella skikt. Använd uppgiftens antagande att E är radiellt och studera dess riktning vid planet mellan materialen.',
        hints=(
            'Det radiella fältet ligger tangentiellt mot skiljeplanet. Kontinuitet för E_t ger därför samma E_r(r) i båda materialen vid samma radie.',
            'D skiljer sig: D1=ε0ε1E och D2=ε0ε2E. En sfärisk Gaussyta med a<r<b har area 2πr² i vardera materialet.',
            'Summera flödena: 2πr²(D1_r+D2_r)=Q. Lös först E_r och använd sedan respektive permittivitet för att få D i varje halva.',
        ),
        self_checks=(
            'När ε1=ε2 ska resultatet bli det vanliga fältet i en homogent fylld sfärisk kondensator. D1_r/D2_r ska vara ε1/ε2.',
            'Det totala D-flödet genom sfären ska vara Q. Utanför det yttre skalet är fältet noll i denna idealmodell eftersom ledarnas totala laddning är +Q−Q=0.',
        ),
        common_pitfall='Att behandla halvorna som två radiella serielager eller sätta D1_r=D2_r. Radialriktningen är tangent till materialgränsen men normal till Gaussytan.',
        geometry_hint='Rita skiljeplanet genom centrum och en radiell pil längs planet. Jämför med en sfärisk Gaussyta: samma pil har olika relation till normalerna på de två olika ytorna.',
        setup_hint='Skriv Q=2πr²ε0(ε1+ε2)E_r. Faktorn 2π kommer från vardera halvklotets area; använd inte 4π för båda bidragen var för sig.',
    ),
    "MakrofolCapacitorDesign": G(
        problem_id="3.11",
        learning_goal="Dimensionera först mot genomslag och därefter mot önskad kapacitans.",
        concepts=("genomslag", "plattkondensator", "dimensionering"),
        start_here='Bestäm först hur tjock isoleringen måste vara för att tåla spänningen. Därefter kan du bestämma arean som ger önskad kapacitans med ett helt antal skikt.',
        hints=(
            'För n lika skikt utan luftgap är total tjocklek nt och E=U/(nt). Kräv E≤E_genomslag; εr ingår inte i detta fältvillkor vid given spänning och tjocklek.',
            'Lös n≥U/(E_genomslag t) och avrunda uppåt till heltal. Här är t=0,10 mm och E_genomslag=200 kV/mm; håll enheterna konsekventa.',
            'Använd det valda heltalet i C=ε0εrA/(nt). Lös ut A för C=100 pF och omvandla m² till cm² först i sista steget.',
        ),
        self_checks=(
            'Kontrollera att n skikt klarar 50 kV men n−1 inte gör det. Ett avrundat antal får aldrig ge högre fält än genomslagsgränsen.',
            'A ska ha enheten m² och öka med total tjocklek vid given C. Uppgiften söker idealmodellens minimum, utan extra säkerhetsmarginal.',
        ),
        common_pitfall='Att använda den oavrundade minimitjockleken i areaberäkningen, eller förväxla kV/mm med V/m: 1 kV/mm=10⁶ V/m.',
        geometry_hint='Skikten staplas i fältriktningen mellan samma två elektroder; deras tjocklekar adderas. Hela gapet antas fyllt, så inga luftskikt ska läggas in i modellen.',
        setup_hint='Beräkna först U/(E_genomslag t), välj nästa heltal och sätt därefter A=C nt/(ε0εr). 100 pF=10⁻¹⁰ F och 1 m²=10⁴ cm².',
    ),
    "CoaxialTwoDielectricCapacitance": G(
        problem_id="3.12",
        learning_goal="Bygga kapacitansen för två koaxiella dielektriska skikt genom att summera potentialfall.",
        concepts=("koaxial kondensator", "D-fält", "seriekopplade dielektrika"),
        start_here='Rita två radiella isolationslager mellan a och c. Lika tjocklek betyder att materialgränsen ligger vid b=(a+c)/2, inte att lagren har samma volym.',
        hints=(
            'Inför fri laddning per längd λ på innerledaren. En cylindrisk Gaussyta ger D_R=λ/(2πR) i båda materialen; D_R varierar med R men har inget språng vid b.',
            'Använd E_i=D/(ε0ε_i) och integrera det inre lagret från a till b samt det yttre från b till c. Varje integral ger en logaritm av en radiekvot.',
            'Addera spänningsfallen till U och bilda C/L=λ/U. Den införda λ ska förkortas bort; kapacitansen bestäms av geometri och material.',
        ),
        self_checks=(
            'Om ε1=ε2=εr ska logaritmerna summeras till ln(c/a), vilket ger den vanliga koaxialkapacitansen per längd.',
            'Svaret ska ha enheten F/m. Vid b är D_n kontinuerligt men E_R(b⁺)/E_R(b⁻)=ε1/ε2; lika tjocka lager behöver inte ha lika spänningsfall.',
        ),
        common_pitfall='Att förväxla kapacitans C med kapacitans per längdenhet C/L, eller använda det geometriska medelvärdet √(ac) för två lika tjocka lager.',
        geometry_hint='R mäts från cylinderaxeln. Material 1 fyller a<R<b och material 2 fyller b<R<c. Fältet passerar materialen i följd och är normalt mot deras cylindriska gränsyta.',
        setup_hint='Skriv U=λ[ln(b/a)/ε1+ln(c/b)/ε2]/(2πε0). Lös sedan λ/U och använd meter för radierna om du också beräknar fält eller laddning per längd.',
    ),
    "BreakdownVoltageCases": G(
        problem_id="3.13",
        learning_goal="Skilja mellan homogen isolering och två material i serie när genomslagsfält begränsar spänningen.",
        concepts=("genomslagsfält", "D-kontinuitet", "serielager"),
        start_here='Behandla de tre fallen separat. I ett enda homogent material används U=Ed. I blandfallet måste båda materialens lokala fält hålla sig under respektive genomslagsgräns.',
        hints=(
            'För (a) och (b): multiplicera genomslagsfältet för det enda materialet med hela avståndet 10 mm. Relativ permittivitet är ingen extra faktor i U=Ed.',
            'För (c) ger avsaknad av fri gränsladdning E_luft=εr E_plexi. Jämför därför de två gränserna D≤ε0 E_luft,max och D≤ε0εr E_plexi,max.',
            'Välj den mindre tillåtna D-nivån. Beräkna båda fälten och summera Umax=E_luft·1 mm+E_plexi·9 mm. Att ett material når sin gräns betyder inte att det andra också gör det.',
        ),
        self_checks=(
            'Vid den valda spänningen måste båda fältgränserna vara uppfyllda och minst en vara nådd. Med uppgiftens värden begränsar luftgapet.',
            'Om ett material saknas helt används det kvarvarande materialets gräns. Ett mycket tunt men kvarvarande luftgap kan fortfarande begränsa fältet; gränsen när tjockleken går mot noll behöver inte vara värdet när luften helt tagits bort.',
        ),
        common_pitfall='Att addera båda materialens maximala spänningsfall utan att först kontrollera att fälten kan uppfylla D-kontinuitet samtidigt.',
        geometry_hint='Luft och plexiglas ligger efter varandra i fältriktningen. I del (c) återstår bara 1 mm luft, men fältet där är tre gånger fältet i plexiglaset.',
        setup_hint='Sätt Dmax=min(ε0 E_luft,max, ε0εr E_plexi,max) när båda lagren finns. Beräkna E_luft=Dmax/ε0 och E_plexi=Dmax/(ε0εr), sedan deras spänningsfall.',
    ),
    "DielectricSlabCapacitor": G(
        problem_id="3.14",
        learning_goal="Knyta ihop D-kontinuitet, spänningsfall, fri ytladdning och polarisationsladdning.",
        concepts=("D-fält", "polarisation", "randvillkor"),
        start_here='Välj z uppåt från den jordade undre plattan till den övre med V0>0. Fältet pekar nedåt. Beräkna först beloppen och sätt sedan ut tecknen på laddningarna.',
        hints=(
            'Utan fri gränsladdning är D-beloppet gemensamt. Skriv E_luft=D/ε0 och E_diel=D/(ε0εr). Spänningsbeloppet är V0=E_luft·0,2d+E_diel·0,8d.',
            'De fria ytladdningarna på elektrodernas inre ytor har belopp D: positivt på den övre plattan och negativt på den undre. Använd normal från metallen ut i gapet på respektive platta.',
            'I dielektrikumet är P=ε0(εr−1)E som vektor. Beräkna bunden ytladdning med σ_b=P·n där n nu är utåtnormal från dielektrikumet. För εr>1 pekar P nedåt.',
        ),
        self_checks=(
            'För εr=1 ska E=V0/d i hela gapet och den bundna laddningen försvinna. D är kontinuerligt genom materialgränsen även när E har ett språng.',
            'För εr>1 blir den bundna laddningen negativ på dielektrikumets övre yta och positiv på dess undre; de summerar till noll. De fria elektrodladdningarna har motsatta tecken.',
        ),
        common_pitfall='Att använda metallens normal när du räknar dielektrikumets bundna laddning, eller blanda ihop fältbelopp med den negativa z-komponenten.',
        geometry_hint='Dielektrikumet fyller 0<z<0,8d. Dess övre normal är +ẑ och dess undre −ẑ. På den övre metallplattans undersida är normalriktningen i stället −ẑ.',
        setup_hint='Lös D ur V0=Dd[0,2/ε0+0,8/(ε0εr)]. Skriv sedan E_z=−E och P_z=−ε0(εr−1)E_diel innan du bildar P·n.',
    ),
    "ElectretCylinderAxis": G(
        problem_id="3.18",
        learning_goal="Ersätta en homogen polarisation med dess bundna laddningar och sedan använda superposition.",
        concepts=("elektret", "bunden laddning", "fält från skiva"),
        start_here='Börja med de bundna laddningarna från den föreskrivna polarisationen P=Pẑ. Cylindern sträcker sig från z=0 till z=h; omgivningen är vakuum.',
        hints=(
            'Konstant P ger ρ_b=−∇·P=0 inne i volymen. Manteln har σ_b=0, botten σ_b=−P och toppen σ_b=+P eftersom σ_b=P·n.',
            'Summera fälten från de två laddade skivorna. För en skiva vid z0 kan ringintegralen skrivas E_z=σ[sgn(z−z0)−(z−z0)/√((z−z0)²+a²)]/(2ε0), utanför själva skivytan. Använd σ=−P vid 0 och +P vid h.',
            'Beräkna D=ε0E+Pẑ inne i cylindern och D=ε0E utanför. För a≫h, nära skivornas centrala delar, används den plana gränsen. I del (d) är P bara ett betecknat laddningsbelopp: ingen materialpolarisation ska adderas för de fria laddningsskivorna.',
        ),
        self_checks=(
            'E_z ska ha rätt språng σ_b/ε0 över varje ändyta, medan D_z är kontinuerligt eftersom det inte finns fri ytladdning. Använd ensidiga gränsvärden på ytorna.',
            'I den plana gränsen är E≈−Pẑ/ε0 inne och ungefär noll utanför, medan D≈0 för elektreten. Fria skivladdningar ger samma E men D=ε0E, alltså D≈−Pẑ mellan skivorna.',
        ),
        common_pitfall='Att anta D=0 överallt för en ändlig elektret bara för att fri laddning saknas. ∇·D=0 innebär inte att D är noll; den plana approximationen gäller inte godtyckligt långt från en ändlig cylinder.',
        geometry_hint='Rita utåtnormal −ẑ på botten och +ẑ på toppen. Vid z=0 och h är E diskontinuerligt, så ange vilken sida du menar. Villkoret a≫h gör centralområdet ungefär plant, men långt bort måste den ändliga kroppens fält avta.',
        setup_hint='Skriv E_z=E_skiva(z;h,+P)+E_skiva(z;0,−P) och förenkla separat för z<0, 0<z<h och z>h. Lägg sedan till P endast i det inre området när D beräknas.',
    ),
    "ObliqueConductorDielectricBoundary": G(
        problem_id="3.19",
        learning_goal="Bestäm fältets riktning från ledarrandvillkoret och geometrin hos ett snett plan.",
        concepts=("ledarrandvillkor", "ytladdning", "normalvektor"),
        start_here='Skriv gränsen som f(x,y)=x/a+y/b−1=0. Origo ligger på ledarsidan f<0, så normalen mot dielektrikumet pekar mot ökande f.',
        hints=(
            'Gradienten ∇f=(1/a,1/b,0) är normal mot planet. Normalisera den; eftersom a,b>0 kan enhetsnormalen skrivas (b,a,0)/√(a²+b²).',
            'I elektrostatisk jämvikt är E=0 i ledaren och E_t=0 precis utanför. I det isotropa dielektrikumet är därför både E och D normala mot ytan.',
            'En Gaussbox över metallytan ger D·n=ρs, där ρs är den fria ytladdningen. Skriv D=ρs n och använd E=D/(ε0εr). Negativ ρs vänder båda fältens riktning.',
        ),
        self_checks=(
            'Enhetsnormalen ska ha längd 1 och vara vinkelrät mot tangenten (a,−b,0). Ingen z-komponent ska finnas.',
            'För a=b ska normalens x- och y-komponenter vara lika. D har belopp |ρs|; vid given fri ytladdning minskar E med ökande εr.',
        ),
        common_pitfall='Att använda skärningsvektorn (a,b,0) som normal, glömma normaliseringen eller anta att den fria ytladdningen är noll eftersom dielektrikumets volymladdning är noll.',
        geometry_hint='Punkterna (a,0) och (0,b) ligger på linjen i xy-snittet; linjen är parallell med vektorn (a,−b). Ledaren innehåller origo, vilket avgör vilken av de två normalriktningarna som ska väljas.',
        setup_hint='Beräkna först n=∇f/|∇f|. Multiplicera med den signerade ρs för D och dividera med ε0εr för E. Randvillkoret gäller omedelbart utanför metallen.',
    ),
    # ------------------------------------------------------------------
    # Kapitel 4 – Energi, kraft och spegelladdning
    # ------------------------------------------------------------------
    "SphericalShellChargingEnergy": G(
        problem_id="4.1",
        learning_goal="Förstå uppladdningsarbete som en successiv process där potentialen ändras medan laddningen byggs upp.",
        concepts=("elektrostatisk energi", "potential", "uppladdningsarbete"),
        start_here=(
            'Bygg upp laddningen från ett neutralt skal. När en liten laddning dq förs in från oändligheten är skalets laddning q, inte redan slutladdningen Q.'
        ),
        hints=(
            'Med V(∞)=0 har det ledande skalet potentialen V(q)=q/(4πε0a). Den är konstant över skalytan men ökar i belopp under uppladdningen.',
            'Det yttre arbetet för nästa lilla laddning är dW=V(q)dq vid långsam uppladdning. Summan av dessa bidrag blir en integral från q=0 till q=Q.',
            'Integrera q-beroendet och jämför med W=Q²/(2C), där en ensam sfär har C=4πε0a. Alternativt kan du integrera fältenergitätheten ε0E²/2 utanför skalet.',
        ),
        self_checks=(
            'Arbetet ska vara positivt för både positiv och negativ slutladdning och vara proportionellt mot Q². För Q=0 är arbetet noll.',
            'Vid fast Q minskar arbetet när a ökar. Kontrollera också dW/dQ=V(Q); faktorn 1/2 hör till det totala arbetet, inte till det sista lilla laddningssteget.',
        ),
        common_pitfall='Att använda slutpotentialen för hela laddningen och skriva W=QV(Q), vilket räknar allt arbete som om skalet redan var fulladdat.',
        geometry_hint='Skalet är en ensam sfär med radie a, med potentialreferens vid oändligheten. Fältet är noll inuti och finns för r>a; blanda inte ihop skalradien a med integrationsradien r i en alternativ fältenergiberäkning.',
        setup_hint='Skriv W=∫₀^Q q/(4πε0a) dq. Håll radien konstant och låt q vara integrationsvariabel. För Q<0 är både potentialen och laddningsstegen negativa, men arbetet blir fortfarande positivt.',
    ),
    "ParallelPlateForceDistance": G(
        problem_id="4.2",
        learning_goal="Koppla den elektriska fältenergin eller det elektriska trycket till den mekaniska kraften mellan kondensatorplattor.",
        concepts=("elektriskt tryck", "plattkondensator", "kraft"),
        start_here='Betrakta den givna kraften som beloppet av den yttre kraft som balanserar plattornas attraktion. Använd fältet i luftgapet för att bestämma det elektriska trycket.',
        hints=(
            'I plattkondensatorapproximationen, utan kanteffekter, är fältbeloppet E=|V|/d. Spänningen 450 V avser potentialskillnaden mellan plattorna.',
            'Det elektriska trycket är p=ε0E²/2. Multiplicera med A för kraften. Faktorn 1/2 kan förstås genom att en platta påverkas av den andra plattans fält, inte av sitt eget.',
            'Sätt kraftbeloppet lika med 0,05 N och lös efter det positiva avståndet d. Omvandla 50 cm² till 0,005 m² innan du sätter in talen.',
        ),
        self_checks=(
            'Sätt tillbaka ditt d i ε0A V²/(2d²) och kontrollera att kraften blir den givna. Attraktionen ändras inte om spänningens tecken vänds.',
            'Vid given V och A ska större efterfrågad kraft ge mindre d, med d proportionellt mot 1/√F. Avståndet bör vara litet jämfört med plattornas sidomått för att kanteffekter ska kunna försummas.',
        ),
        common_pitfall='Att skriva F=QE med hela gapfältet och därmed få dubbla kraften, eller derivera enbart fältenergin vid konstant V utan att räkna med spänningskällans energiutbyte.',
        geometry_hint='Markera en pil inåt för den elektriska kraften på varje platta och en lika stor pil utåt för den kraft som håller dem isär. d är vinkelrätt avstånd mellan plattorna; A är en plattas yta, inte summan av bådas.',
        setup_hint='Skriv F=(ε0A/2)(V/d)² och isolera d² innan du tar den positiva roten. Tryckmetoden gäller för det aktuella tillståndet utan att du behöver anta hur en strömkälla kopplas vid en senare förflyttning.',
    ),
    "CopperFoilLevitationEbonite": G(
        problem_id="4.3",
        learning_goal="Använd randvillkor mellan luft och dielektrikum för att koppla elektriskt tryck till tyngdkraft.",
        concepts=("dielektrikum", "elektriskt tryck", "kraftjämvikt"),
        start_here=(
            'Skriv kraftbalansen per area för kopparblecket: elektriskt tryck uppåt ska balansera tyngden ρ_Cu t g nedåt. Då förkortas den okända plattarean bort.'
        ),
        hints=(
            'Kraften på blecket bestäms av luftfältet precis utanför metallen: p_el=ε0E_luft²/2. Det infinitesimala luftgapet är därför viktigt även om dess spänningsfall är försumbart.',
            'Utan fri laddning på luft–ebonitgränsen är D_n kontinuerligt. Därmed gäller ε0E_luft=ε0εrE_ebonit.',
            'När luftgapets tjocklek går mot noll blir U≈E_ebonit d. Kombinera detta med p_el=ρ_Cu t g och lös efter minsta spänningsbelopp som balanserar tyngden.',
        ),
        self_checks=(
            'Sätt in ditt U och kontrollera att ε0(εrU/d)²/2=ρ_Cu t g. Båda leden ska ha enheten N/m².',
            'Större t eller ρ_Cu ska kräva större spänning, proportionellt mot kvadratroten. Kraftbalansen visar att folien kan hållas uppe i idealmodellen, inte att en fritt svävande jämvikt är stabil.',
        ),
        common_pitfall='Att använda U/d som luftfält eller ta bort luftgapet innan kraften bestämts. U/d är ebonitfältet i gränsen av ett mycket tunt luftgap.',
        geometry_hint='Rita i ordning: övre metallbelägg, ebonit med tjocklek d, ett mycket tunt luftgap och kopparfolie med tjocklek t. Det är luftfältet vid foliens övre yta som ger trycket; d och t har olika roller.',
        setup_hint='Lös först E_luft ur ε0E_luft²/2=ρ_Cu t g och använd sedan U≈d E_luft/εr. Sätt d=0,02 m, t=10⁻⁴ m och ρ_Cu=8,9·10³ kg/m³.',
    ),
    "ThundercloudEnergyEstimate": G(
        problem_id="4.5",
        learning_goal="Göra en ordningsstorleksmodell av ett åskmoln som en plattkondensator och koppla genomslagsfält till laddning och energi.",
        concepts=("plattkondensator", "genomslagsfält", "fältenergi"),
        start_here='Följ uppgiftens modell med negativ molnbas och positiv mark som två stora plattor. Låt Q beteckna laddningsbeloppet, så att molnets signerade laddning är −Q.',
        hints=(
            'Fälten från de två motsatt laddade ytorna adderas i gapet. Sätt E=Q/(ε0A) lika med det angivna Emax för denna uppskattning.',
            'Omvandla först A=1 km² till 10⁶ m² och Emax=20 000 V/cm till 2·10⁶ V/m. Bestäm sedan Q från fältet.',
            'Beräkna energin med W_e=ε0Emax²Ah/2. Kontrollera genom C=ε0A/h, spänningsbelopp U=Emax h och W_e=CU²/2=QU/2.',
        ),
        self_checks=(
            'De två energiberäkningarna ska stämma och ge joule. Energin är positiv även om molnets laddning är negativ; använd laddnings- och spänningsbelopp i QU/2.',
            'Vid fast Emax och area är Q oberoende av h, medan U och W_e växer linjärt med h. Detta är en idealiserad kondensatoruppskattning, inte en detaljerad modell av ett verkligt åskmoln.',
        ),
        common_pitfall='Att missa faktorn 100 när V/cm omvandlas till V/m, eller använda ensamplattans E=σ/(2ε0) när båda plattornas fält bidrar.',
        geometry_hint='Marken är vid z=0 och molnbasen vid z=h. Fältet pekar uppåt från markens +Q till molnets −Q, medan potentialen minskar uppåt. A är en ytas area och ska inte dubbleras.',
        setup_hint='Skriv Q=ε0A Emax och W_e=(ε0Emax²/2)Ah. Skilj energitätheten i J/m³ från den totala energin i J; volymen i modellen är Ah.',
    ),
    "CylindricalCapacitorDielectricPullIn": G(
        problem_id="4.6",
        learning_goal="Beräkna en dielektrisk indragningskraft genom hur kapacitansen ändras med inskjutningslängden.",
        concepts=("energimetod", "kapacitans", "dielektrisk kraft"),
        start_here=(
            'Låt x öka när hålcylindern dras in längs metallrörens axel. Spänningskällan är ansluten och håller V0 konstant; både kondensatorns laddning och dess fältenergi kan därför ändras.'
        ),
        hints=(
            'Dela upp en aktiv längd L i en fylld del x och en luftfylld del L−x. Delarna har samma spänning mellan samma elektroder och deras kapacitanser adderas parallellt.',
            'Kapacitans per längd är 2πε0εr/ln(b/a) i den fyllda delen och 2πε0/ln(b/a) i den tomma. Skriv C(x) och beräkna dC/dx.',
            'Vid konstant V0 tillför källan dW_källa=V0 dQ=V0²dC. Fältenergin ökar med dW_fält=V0²dC/2. Resten blir mekaniskt arbete F_x dx; använd detta för att få kraften och dess riktning.',
        ),
        self_checks=(
            'För εr>1 ska kraften peka inåt, mot större x och större C. Den ska försvinna när εr=1 eller V0=0 och vara oförändrad om spänningens tecken vänds.',
            'Kraften blir oberoende av x medan både fylld och tom del finns och kapacitansen kan approximeras som linjär i x. Nära full inskjutning eller långt utanför gäller inte denna konstanta kraftmodell.',
        ),
        common_pitfall='Att använda F_x=−d(CV0²/2)/dx vid konstant spänning och få fel tecken. Fältenergin ensam är inte den mekaniska potentialenergin när källan utbyter energi med systemet.',
        geometry_hint='Hålcylindern fyller hela radialgapet a<r<b men bara en del av längden. Rörelsen är axiell, inte radiell. Kraften verkar vid övergången till fylld del; energimetoden ger nettokraften utan att fransfältet behöver lösas i detalj.',
        setup_hint='Skriv C(x)=2πε0[L+(εr−1)x]/ln(b/a). Kombinera dC/dx med F_x=V0²(dC/dx)/2. L försvinner ur kraften; logaritmens argument b/a är dimensionslöst.',
    ),
    "PointChargeConductingPlane": G(
        problem_id="4.7",
        learning_goal="Använd spegelladdningsmetoden både för inducerad ytladdning och för kraften på en punktladdning.",
        concepts=("spegelladdning", "ledarvillkor", "inducerad ytladdning"),
        start_here=(
            'Välj planet z=0 och den verkliga laddningen q vid z=a. Använd den idealisering med ett oändligt plan på noll potential som ligger bakom appens modell och facit; spegelladdningen är ett hjälpmedel utanför det fysiska området.'
        ),
        hints=(
            'Placera −q vid z=−a. Potentialbidragen tar ut varandra på z=0. Fältet i det övre halvrummet är då den sökta lösningen, men fältet inne i den verkliga ledaren är noll.',
            'För del (a): b mäts från kulan, inte från dess lodräta projektion på planet. Punkter i planet på avstånd högst b från kulan bildar en skiva med radie R_max=√(b²−a²). Bestäm σ(R)=ε0E_z(R,0⁺) med normal +ẑ.',
            'Integrera den inducerade laddningen med ringelement dS=2πR dR från 0 till R_max. Låt sedan b→∞ för del (b). I del (c) används enbart spegelladdningens fält vid q, med avståndet 2a.',
        ),
        self_checks=(
            'När b→a⁺ ska den integrerade laddningen gå mot noll, eftersom skivan krymper till en punkt. När b→∞ ska den gå mot −q.',
            'Den inducerade laddningen har motsatt tecken mot q. Kraften är riktad nedåt och dess belopp är proportionellt mot q²/a², oberoende av avståndsgränsen b.',
        ),
        common_pitfall='Att integrera till radien b i planet, vilket motsvarar ett annat område än uppgiften frågar efter. Förväxla inte heller kraften med energin: kraften fås direkt från bilden, men bildparets fulla Coulombenergi är inte systemets verkliga energi.',
        visualization_note="Här kan en geometrisk bild av verklig laddning, spegelladdning och fältlinjer vara mer pedagogisk än en generell fältkarta.",
        geometry_hint='Rita en rätvinklig triangel med höjden a, sträckan R i planet och hypotenusan b från kulan till skivans kant. Skivan ligger i planet; i ett vertikalt snitt syns den som en sträcka, inte som en cirkel runt origo.',
        setup_hint='Fältets normaldel ger σ(R)=−qa/[2π(R²+a²)^(3/2)]. Skriv Q_ind=∫₀^√(b²−a²) σ(R)2πR dR och använd u=R²+a². För kraften: använd Coulombs lag mellan q och −q på avstånd 2a, utan extra faktor 2.',
    ),

    # ------------------------------------------------------------------
    # Kapitel 5 – Strömmar och strömtäthet
    # ------------------------------------------------------------------
    "ConductiveCoaxialElectrodes": G(
        problem_id="5.1",
        learning_goal="Översätta det välkända koaxiala E-fältet till stationär ström genom ett ledande medium.",
        concepts=("Ohms lag i punktform", "koaxial geometri", "ström"),
        start_here='Välj U=V(a)−V(b) och positiv ström radiellt utåt. I stationärt tillstånd passerar samma ström varje cylindrisk yta mellan elektroderna; ändeffekter försummas.',
        hints=(
            'En strömyta med radie R och längd ℓ har arean 2πRℓ. Strömkonservering ger därför J_R=I/(2πRℓ); strömtätheten är inte konstant i gapet.',
            'Använd E_R=J_R/σ och skriv U=∫_a^b E_R dR. Den radiella integralen ger ln(b/a).',
            'Lös ut I och jämför med I=U/R_el. Konduktivitet σ mäts i S/m och är inversen till resistiviteten; blanda inte ihop dessa materialstorheter.',
        ),
        self_checks=(
            'Produkten 2πRℓJ_R ska vara samma för varje R. Vid U>0 pekar både E och J utåt; negativ U vänder riktningen.',
            'Resistansen ska vara positiv och oberoende av U. Vid U=0 är strömmen noll men resistansen fortfarande ändlig. En längre cylinder ger större ledande yta och därmed större ström vid samma spänning.',
        ),
        common_pitfall='Att behandla strömmen som om den gick längs cylinderns längd eller använda samma tvärsnittsarea över hela radialgapet. I den resistiva vätskan kan E vara skilt från noll även när strömmen är stationär.',
        geometry_hint='Rita två koncentriska cirklar och en radiell strömpil från inner- till ytterledare för U>0. Den strömyta du använder är cylinderns mantelyta 2πRℓ, inte ändytan πR².',
        setup_hint='Sätt U=I∫_a^b dR/(2πσℓR) och lös efter I. Håll isär radialkoordinaten R och resistansen R_el. Om U definieras tvärtom måste den signerade strömriktningen ändras.',
    ),
    "CoaxialCableLeakage": G(
        problem_id="5.2",
        learning_goal="Beräkna läckström och effektförlust genom ett resistivt koaxialt isolationsskikt.",
        concepts=("resistivitet", "koaxial resistans", "Joulevärme"),
        start_here='Läckströmmen går genom isolationen från innerledare till skärm, alltså radiellt. Modellera varje tunt radiellt skikt som en resistans i serie med nästa.',
        hints=(
            'För ett skikt på radie R med tjocklek dR är strömvägens längd dR och tvärsnittsarean 2πRℓ. Skriv dR_el=ρ dR/(2πRℓ), där ρ här är resistivitet i Ω m.',
            'Uppgiften anger diametrarna a och b. Integrera från a/2 till b/2; logaritmen blir ln[(b/2)/(a/2)]=ln(b/a). Om du senare beräknar lokala fält måste du ändå använda faktiska radier.',
            'Med resistansen bestämd fås I=V/R_el och P=VI=V²/R_el. Sätt ℓ=1,50 m, V=120 V och ρ=5,0·10⁶ Ω m; avrunda först i slutet.',
        ),
        self_checks=(
            'Läckströmmen ska bli ungefär 0,16 mA och effekten ungefär 20 mW. P har enheten watt, inte energi i joule.',
            'Om V byter tecken byter I tecken men P är oförändrad och icke-negativ. Dubbel kabellängd ger dubbel läckström och effekt, eftersom fler strömvägar kopplas parallellt.',
        ),
        common_pitfall='Att använda kabelns längd som strömvägens längd i ρℓ/A, eller dubblera/halvera bara den ena diametern i logaritmen.',
        geometry_hint='Rita ett tvärsnitt med innerledarradie a/2 och skärmens innerradie b/2. Radialskikten ligger i serie; olika bitar längs kabeln erbjuder däremot parallella läckvägar mellan samma två ledare.',
        setup_hint='Skriv R_el=ρ ln(b/a)/(2πℓ). Använd sedan samma R_el i både I=V/R_el och P=V²/R_el. Resistiviteten ρ i detta problem är inte en laddningstäthet.',
    ),
    "VariableSigmaCoaxialElectrolyte": G(
        problem_id="5.7",
        learning_goal="Hantera stationär ström när konduktiviteten varierar i rummet och koppla fältets divergens till fri rymdladdning.",
        concepts=("kontinuitet", "variabel konduktivitet", "Gauss lag"),
        start_here='Börja med stationär strömkonservering. Välj U=V(a)−V(b) och positiv ström utåt, så att tecknet på den fria laddningstätheten kan följas genom beräkningen.',
        hints=(
            'Samma I passerar varje cylindrisk yta: J_R=I/(2πRℓ). Sätt därefter E_R=J_R/σ(R) med σ(R)=k/R². Fältet blir proportionellt mot R även om strömtätheten avtar som 1/R.',
            'Integrera U=∫_a^b E_R dR och identifiera R_el=U/I. Du kan också integrera dR_el=dR/[σ(R)2πRℓ].',
            'För del (b) använder du den konstanta permittiviteten ε=ε0εr och ρ_fri=∇·D=ε(1/R)d(RE_R)/dR. Sätt in E_R uttryckt med U innan du deriverar.',
        ),
        self_checks=(
            'Strömflödet 2πRℓJ_R ska vara konstant. Den fria volymladdningstätheten blir också konstant här, men av en annan anledning: cylindrisk divergens av ett fält proportionellt mot R.',
            'Med den valda definitionen är ρ_fri positiv för U>0 och byter tecken när U vänds. Vid fast U är ρ_fri oberoende av k, medan I är proportionell mot k. k har enheten S·m.',
        ),
        common_pitfall='Att sätta laddningstätheten till noll bara för att strömmen är stationär, eller använda dE_R/dR i stället för den cylindriska divergensen (1/R)d(RE_R)/dR.',
        geometry_hint='Observationsradien R löper genom elektrolyten a<R<b. Föreställ dig två cylindriska strömytor: den större har större area och därför lägre J_R, samtidigt som dess lägre σ kräver ett större E_R.',
        setup_hint='Efter integrationen får du E_R=2UR/(b²−a²). Använd detta i ρ_fri=ε0εr(1/R)d(RE_R)/dR. Stationaritet betyder ∂ρ_fri/∂t=0 och ∇·J=0, inte att ρ_fri måste vara noll.',
        visualization_note='Jämför de separata vyerna för E_R, J_R och fri laddningstäthet. Försök förklara hur σ(R)=k/R² kan ge olika radialberoenden för E och J samtidigt som totalströmmen är densamma genom varje cylinderyta.',
    ),
    "SemicylindricalRingResistor": G(
        problem_id="5.10",
        learning_goal="Beräkna resistans i en geometri där strömvägens längd beror på radien och olika radiala skikt ligger parallellt.",
        concepts=("cylindriska koordinater", "strömfördelning", "parallella strömvägar"),
        start_here='Betrakta en tunn halvcirkelformad strömbana mellan radierna R och R+dR. Alla sådana banor går mellan samma kontaktytor A och B och ligger elektriskt parallellt.',
        hints=(
            'Banans längd är πR och dess tvärsnittsarea vinkelrätt mot strömmen är h dR. Skriv dess konduktans dG=σh dR/(πR) så att parallellkopplingen blir enkel.',
            'Integrera dG från a till b och invertera först den totala konduktansen för att få resistansen. Radierna beskriver vilka banor som finns, inte strömmens riktning.',
            'Som alternativ kontroll: sätt V(A)−V(B)=U och låt vinkeln öka från A till B. Då är E_φ=U/(πR). Integrera J_φ=σE_φ över en radiell snittyta med areaelement h dR för att få I.',
        ),
        self_checks=(
            'Större σ eller h ska minska resistansen. När b→a⁺ går den ledande tvärsnittsarean mot noll och resistansen mot oändligheten.',
            'För en tunn ring, b−a≪a, ska resultatet närma sig πa/[σh(b−a)], alltså längd delat med konduktivitet gånger tvärsnittsarea. Den inre banan har större J än den yttre vid samma U.',
        ),
        common_pitfall='Att addera banornas resistanser som om de låg i serie, eller behandla strömmen som radiell mellan inner- och ytterytan. Här går den längs halvcirklarna mellan A och B.',
        visualization_note="En enkel tvärsnittsskiss med flera parallella halvcirkelformade strömvägar är mer informativ än en färgkarta över J.",
        geometry_hint='I tvärsnittet är A och B de två raka radialytorna vid halvringens ändar. Rita flera halvcirklar mellan dem. h är höjden vinkelrätt mot denna bild och ingår i varje banas tvärsnittsarea.',
        setup_hint='Skriv G=∫_a^b σh/(πR) dR och sedan R_el=1/G. Skilj konduktans G i siemens från materialets konduktivitet σ i S/m.',
    ),
    "SteadyCurrentInterfaceCharge": G(
        problem_id="5.15",
        learning_goal="Kombinera stationär strömkontinuitet med elektrostatikens randvillkor för att hitta fri ytladdning i ett materialgränsskikt.",
        concepts=("randvillkor", "J=σE", "ytladdning"),
        start_here='Välj normalen n=+x̂ från medium 1 (x<0) till medium 2 (x>0). Dela J1=αx̂+βŷ i normal och tangentiell del innan du använder randvillkoren.',
        hints=(
            'Stationärt tillstånd innebär att ingen ytterligare ytladdning ansamlas: J2x=J1x=α. Det utesluter inte en redan etablerad, tidsoberoende ytladdning. Ohms lag ger E1x=α/σ1 och E2x=α/σ2.',
            'Det stationära elektriska fältets tangentiella komponent är kontinuerlig: E2y=E1y=β/σ1. Därför är J2y=σ2β/σ1; hela J-vektorn behöver inte vara kontinuerlig.',
            'Använd Gauss randvillkor ρ_s=D2x−D1x=ε0(ε2E2x−ε1E1x). För del (b), sök materialvillkoret som gör detta noll även när en normal ström passerar gränsen.',
        ),
        self_checks=(
            'Ytladdningen ska vara oberoende av β och ha enheten C/m². Den byter tecken om α byter tecken med samma normalriktning.',
            'För α≠0 krävs ε1/σ1=ε2/σ2 för noll ytladdning. Om α=0 är ytladdningen noll oavsett materialkvoterna; identiska material är ett annat enkelt kontrollfall.',
        ),
        common_pitfall='Att kräva kontinuitet för E_n eller hela J. Här är J_n och E_t kontinuerliga, medan språnget i D_n bestämmer den fria ytladdningen.',
        geometry_hint='Gränsen är yz-planet: x är normalriktning och y är tangentriktning. En liten Gaussbox ger D-språnget över gränsen, medan en tunn rektangulär slinga ger kontinuitet för E_y.',
        setup_hint='Skriv E1=(α/σ1, β/σ1, 0) och E2=(α/σ2, β/σ1, 0). Sätt endast x-komponenterna i ρ_s=ε0(ε2E2x−ε1E1x). ε1 och ε2 används här som relativa permittiviteter, som i appen och facit.',
    ),

    # ------------------------------------------------------------------
    # Kapitel 6 – Biot–Savarts lag
    # ------------------------------------------------------------------
    "FiniteWireBiotSavart": G(
        problem_id="6.1",
        learning_goal="Härleda fältet från en ändlig rak ledare och se hur Biot–Savart, vektorpotential och Ampères lag hänger ihop.",
        concepts=("Biot–Savarts lag", "vektorpotential", "Ampères lag"),
        start_here="Använd cylindersymmetrin för riktningen redan innan du integrerar: vilket håll måste B ha runt en rak z-riktad ström?",
        hints=(
            "Parametrisera källan med z′ från −L till L. I Biot–Savart är dℓ′=dz′ ẑ och vektorn till fältpunkten har både radiell och z-komponent; korsprodukten lämnar bara φ̂.",
            "För del (b) har A bara en z-komponent för den raka ledaren. Integrera A_z först och ta sedan B=∇×A; vid z=0 blir derivatorna betydligt enklare.",
            "I gränsen L→∞ får du full cylindersymmetri. Då kan en cirkulär Ampereslinga användas direkt och ska ge samma gränsvärde som Biot–Savart.",
        ),
        self_checks=(
            "För en oändlig ledare ska |B| skala som 1/R.",
            "Riktningen ska följa högerhandsregeln runt strömmen och resultatet ska vara oberoende av φ.",
        ),
        common_pitfall="Att använda Ampères lag för den ändliga ledaren som om fältet vore konstant runt en cirkel; den fulla symmetrin finns först i det oändliga gränsfallet.",
    ),
    "SquareLoopOnAxis": G(
        problem_id="6.2",
        learning_goal="Summera magnetfält från flera räta ledarsegment och utnyttja symmetri för att eliminera tvärkomponenter.",
        concepts=("superposition", "ändlig rak ledare", "symmetri"),
        start_here="Ta en av kvadratens fyra sidor först. Bestäm dess B-bidrag i en punkt på z-axeln och fråga sedan vad rotation med 90° gör med komponenterna.",
        hints=(
            "Varje sida kan behandlas med Biot–Savart eller resultatet för en ändlig rak ledare. Avståndet från fältpunkten till varje sida är samma.",
            "När de fyra sidornas bidrag summeras tar komponenterna parallella med xy-planet ut varandra. Endast axelkomponenten återstår.",
            "Sätt z=0 först efter att det allmänna axelfältet är framtaget för del (b). Använd högerhandsregeln separat för att bestämma tecknet längs z-axeln.",
        ),
        self_checks=(
            "På mycket stort |z| ska slingan börja bete sig som en magnetisk dipol och fältet avta ungefär som 1/|z|³.",
            "I centrum ska alla fyra sidor bidra lika mycket till axelkomponenten.",
        ),
        common_pitfall="Att multiplicera fältvektorn från en sida med fyra utan att först projicera den på z-riktningen; tvärkomponenterna roteras och tar ut varandra.",
    ),
    "RightAngleWireCorner": G(
        problem_id="6.3",
        learning_goal="Superponera fält från två halv-oändliga räta ledare med olika riktningar.",
        concepts=("Biot–Savart", "superposition", "vektorriktning"),
        start_here="Dela den böjda ledaren i två räta halv-oändliga segment. Behandla deras fält i punkten 5 cm ovanför böjen var för sig.",
        hints=(
            "För varje segment kan du använda den ändliga-raka-ledarens formel med en ändpunkt i böjen och den andra på oändligt avstånd.",
            "De två bidragen har samma belopp av symmetriskäl, men de pekar inte i samma riktning. Bestäm båda riktningarna med dℓ×r eller högerhandsregeln.",
            "Summera vektorerna geometriskt. Eftersom bidragen är lika stora kommer resultatet att ligga längs en bisektris i det horisontella planet.",
        ),
        self_checks=(
            "Byter strömmen riktning ska hela B-vektorn byta riktning.",
            "Resultatet ska minska proportionellt mot 1/höjden om hela geometrin skalas endast i höjdled långt från böjens storleksskala.",
        ),
        common_pitfall="Att anta att de två fältbidragen pekar åt samma håll bara för att strömmen är densamma i den sammanhängande ledaren.",
    ),
    "ThinCurrentStripField": G(
        problem_id="6.5",
        learning_goal="Ersätta ett brett strömförande band med en kontinuerlig samling parallella linjeströmmar.",
        concepts=("superposition", "ytström", "oändlig rak ledare"),
        start_here="Skär bandet i infinitesimala parallella trådar över bredden. Vilken ström dI bär en remsa med bredd dx′ om totalströmmen är jämnt fördelad?",
        hints=(
            "Använd dI=(I/2a)dx′ och det kända fältet från en oändligt lång rak ledare för varje remsa.",
            "I del (a) ligger observationspunkten i bandets plan. Alla bidrag får samma normalriktning, så integralen reduceras till en skalär 1/avstånd-integral.",
            "I del (b) måste varje tråds cirkulära B-fält projiceras. Symmetrin gör att en komponent tar ut sig mellan remsorna x′ och −x′ medan den andra adderas.",
        ),
        self_checks=(
            "När bandbredden blir mycket liten vid fast I ska resultatet närma sig fältet från en linjeström.",
            "I den symmetriska punkten ovanför mittlinjen ska den tvärkomponent som är udda i x′ försvinna.",
        ),
        common_pitfall="Att använda samma avstånd och samma fältriktning för alla remsor; i del (b) ändras både avståndet och riktningen över bandets bredd.",
    ),
    "CircularArcOnAxis": G(
        problem_id="6.8",
        learning_goal="Genomföra Biot–Savart-integralen för en cirkelbåge där symmetrin inte räcker för att eliminera alla komponenter.",
        concepts=("cirkelbåge", "Biot–Savart", "vektorintegral"),
        start_here="Parametrisera kvartscirkeln med vinkeln φ och skriv både dℓ och vektorn från bågelementet till punkten z ẑ innan du tar korsprodukten.",
        hints=(
            "Alla bågelement ligger på samma avstånd √(a²+z²) från en punkt på z-axeln, så nämnaren kan tas ut ur integralens vinkelberoende del.",
            "Beräkna dℓ×R-vektorn komponentvis. För en kvartsbåge överlever normalt både tvärkomponenter och z-komponenten eftersom full rotationssymmetri saknas.",
            "För den hela cirkeln kan du antingen integrera 0→2π eller använda symmetri: alla tvärkomponenter tar ut varandra och bara z-komponenten återstår.",
        ),
        self_checks=(
            "I centrum z=0 ska kvartscirkeln ge ett B-bidrag vinkelrätt mot slingans plan från z-komponenten, medan vissa tvärtermer förenklas.",
            "För en hel cirkel ska resultatet stämma med det välkända axelfältet från en strömslinga.",
        ),
        common_pitfall="Att använda helcirkelns symmetri redan i del (a) och därför kasta bort x- och y-komponenter som faktiskt finns för en kvartsbåge.",
    ),
    "RotatingChargedDisk": G(
        problem_id="6.13",
        learning_goal="Omvandla en roterande ytladdning till en kontinuerlig fördelning av cirkulära strömslingor.",
        concepts=("ytladdning", "konvektionsström", "strömslinga"),
        start_here="Dela skivan i tunna ringar med radie R och bredd dR. Bestäm först laddningen på en sådan ring och hur stor ström dess rotation motsvarar.",
        hints=(
            "Ringens laddning är dq=ρs 2πR dR. Ett varv tar tiden 2π/ω, så den motsvarande ringströmmen blir dI=dq·ω/(2π).",
            "Använd axelfältet från en cirkulär strömslinga med radie R för varje dI. Fältbidragen pekar alla längs rotationsaxeln.",
            "Integrera R från 0 till a. Var noga med |z| eller motsvarande teckenhantering om uttrycket ska gälla på båda sidor om skivan.",
        ),
        self_checks=(
            "B ska vara proportionellt mot både ρs och ω och byta riktning om någon av dem byter tecken/riktning.",
            "Långt från skivan ska fältet avta som ett dipolfält, ungefär 1/|z|³.",
        ),
        common_pitfall="Att använda hela skivans laddning som om den gick i en enda ring med radie a; olika radier har olika strömbidrag och olika axelfält.",
    ),

    # ------------------------------------------------------------------
    # Kapitel 7 – Kraft, moment och magnetiskt flöde
    # ------------------------------------------------------------------
    "ElectronOrbitDipoleMoment": G(
        problem_id="7.1",
        learning_goal="Koppla en laddnings periodiska rörelse till en ekvivalent ström och ett magnetiskt dipolmoment.",
        concepts=("magnetiskt moment", "ekvivalent ström", "elektronladdning"),
        start_here="Betrakta först den cirkulerande laddningen som en ström: hur mycket laddning passerar en given punkt per omloppstid?",
        hints=(
            "Omloppstiden är T=2πa/v. Den konventionella strömmen är I=q/T, där q för en elektron är negativt.",
            "Magnetiska dipolmomentet för en plan strömslinga är m=I A n̂ med A=πa².",
            "Bestäm n̂ från den positiva omloppsriktningen med högerhandsregeln och låt elektronens negativa laddning vända momentets riktning relativt partikelns rörelse.",
        ),
        self_checks=(
            "Beloppet ska vara proportionellt mot e·v·a.",
            "En positiv laddning med samma rörelse skulle ge motsatt riktning på m jämfört med elektronen.",
        ),
        common_pitfall="Att sätta strömriktningen lika med elektronens rörelseriktning; konventionell ström går motsatt en negativ laddnings rörelse.",
    ),
    "CircularLoopTorqueUniformField": G(
        problem_id="7.2",
        learning_goal="Se hur det lokala kraftbidraget på en strömslinga summeras till det globala momentet m×B.",
        concepts=("Lorentzkraft på ledare", "kraftmoment", "magnetiskt moment"),
        start_here="För del (a), parametrisera ett litet strömelement på cirkeln och skriv först dF=I dℓ×B. Ta därefter momentet dT=r×dF kring centrum.",
        hints=(
            "Med r=a(cosφ x̂+sinφ ŷ) och dℓ=a(−sinφ x̂+cosφ ŷ)dφ kan både dF och dT skrivas explicit i φ.",
            "Integrera dT runt 0→2π. Termer som är udda/sinus- eller cosinusmedelvärden försvinner, medan en komponent summeras till ett nettomoment.",
            "I del (b) använder du m=Iπa² ẑ och jämför direkt med T=m×B. Del (c) kontrolleras med magnetnålsbilden: m vill vrida sig mot B.",
        ),
        self_checks=(
            "Nettokraften på den slutna slingan i ett homogent B-fält ska vara noll även om nettomomentet inte är noll.",
            "Momentets belopp ska vara mB sinθ och här är vinkeln mellan m och B 90°.",
        ),
        common_pitfall="Att blanda ihop nettokraft och kraftmoment; motsatta delar av slingan kan ge krafter som tar ut varandra men ändå bildar ett kraftpar.",
    ),
    "DipoleDipoleTorque": G(
        problem_id="7.3",
        learning_goal="Beräkna momentet på en magnetisk dipol i det icke-homogena fältet från en annan dipol.",
        concepts=("dipolfält", "magnetiskt moment", "vektorgeometri"),
        start_here="Beräkna först B-fältet från den ena dipolen i den andra dipolens position. Använd vinkeln θ mellan r̂ och ẑ för att skriva fältets riktning.",
        hints=(
            "Dipolfältet kan skrivas B=(μ0/4πr³)[3(m·r̂)r̂−m]. Här är m=m ẑ och m·r̂=m cosθ.",
            "Momentet på den andra spolen är T=m×B. Den del av B som ligger parallellt med ẑ bidrar inte till korsprodukten.",
            "Efter att ha tagit beloppet uppstår en produkt sinθ cosθ; den kan skrivas med sin(2θ) om du vill förenkla numeriken.",
        ),
        self_checks=(
            "Momentet ska vara noll för θ=0° och θ=90° i denna konfiguration.",
            "Beloppet ska skala som m²/r³.",
        ),
        common_pitfall="Att använda B på dipolaxeln eller ekvatorialplanet som specialfall trots att θ=45° ligger mellan dessa riktningar.",
    ),
    "LoopDipoleApproximationError": G(
        problem_id="7.5",
        learning_goal="Kvantifiera när fjärrfältsapproximationen av en strömslinga som magnetisk dipol faktiskt är tillräckligt noggrann.",
        concepts=("dipolapproximation", "relativt fel", "gränsfall"),
        start_here="Skriv både det exakta axelfältet från en cirkulär slinga och dipolens axelfält med samma magnetiska moment m=Iπa².",
        hints=(
            "Inför den dimensionslösa variabeln x=z/a. Då kan både det exakta och approximativa fältet skrivas som samma prefaktor gånger en ren funktion av x.",
            "Bildar du kvoten B_dip/B_exact försvinner μ0, I och a. Det gör 1%-villkoret till en enkel dimensionslös olikhet.",
            "Använd |B_dip−B_exact|/|B_exact|<0,01 och lös efter x. Det sökta avståndet är därefter z=xa.",
        ),
        self_checks=(
            "Felet ska gå mot noll när z/a→∞.",
            "Resultatet ska vara ett rent tal gånger a; inga andra dimensionsbärande parametrar kan finnas kvar.",
        ),
        common_pitfall="Att jämföra med ett dipolmoment m=Ia i stället för m=Iπa², eller att använda absolut fel i tesla i stället för det efterfrågade relativa felet.",
        visualization_note="En graf över relativfelet mot z/a kan här faktiskt hjälpa studenten att se var dipolapproximationen blir användbar.",
    ),
    "AntarcticIceFlux": G(
        problem_id="7.6",
        learning_goal="Använd ∇·B=0 för att byta en besvärlig flödesyta mot en enklare sfärisk yta.",
        concepts=("magnetiskt flöde", "Gauss lag för B", "jordens dipolfält"),
        start_here=(
            "Försök inte direkt integrera över hela is–luft-gränsen. Slut i stället isvolymen till en sluten yta och använd att det totala magnetiska flödet genom varje sluten yta är noll."
        ),
        hints=(
            "Det totala flödet som lämnar isen till luften måste vara motsatt flödet genom isens botten mot jorden. Därför räcker det att integrera B·dS över den sfäriska polarkalotten vid jordradien.",
            "Använd jordens dipolfälts radiella komponent B_r på r=rJ. Sätt polvinkeln θ=0 vid sydpolen och integrera till θmax=20°.",
            "Ytelementet på sfären är dS=rJ² sinθ dθ dφ. φ-integralen ger 2π och θ-integralen innehåller cosθ sinθ.",
        ),
        self_checks=(
            "Om polarområdet krymper mot θmax→0 ska flödet gå mot noll.",
            "Svaret ska ha enheten weber och vara proportionellt mot jordens magnetiska moment m.",
        ),
        common_pitfall="Att använda ∇·B som om det fanns en magnetisk laddning inuti jorden; den fundamentala poängen är just att nettomagnetflödet genom en sluten yta är noll.",
    ),
    "CopperWireMagneticLevitation": G(
        problem_id="7.7",
        learning_goal="Jämföra magnetisk krafttäthet J×B med tyngdkraft per volym.",
        concepts=("krafttäthet", "J×B", "kraftjämvikt"),
        start_here="Arbeta per volym i stället för att införa trådens okända tvärsnittsarea. Vilken magnetisk krafttäthet får en strömtäthet J i ett homogent B-fält?",
        hints=(
            "Den magnetiska kraften per volym är f=J×B. Med J längs +x och B längs +y pekar kraften i +z.",
            "Tyngdkraften per volym är ρCu g i −z-riktningen. Sätt beloppen lika för svävning.",
            "Lös efter B och konvertera J från A/mm² till A/m² innan numerisk insättning.",
        ),
        self_checks=(
            "Trådens radie ska inte behövas; både magnetisk kraft och tyngd är proportionella mot volymen.",
            "Om J fördubblas ska det nödvändiga B-fältet halveras.",
        ),
        common_pitfall="Att använda densiteten ρCu direkt i g/cm³ tillsammans med SI-enheter för J och B.",
    ),
    "InfiniteWireRectangularLoopFlux": G(
        problem_id="7.10",
        learning_goal="Beräkna magnetiskt flöde genom en plan yta när B både varierar i belopp och lutar relativt ytans normal.",
        concepts=("magnetiskt flöde", "fält från rak ledare", "projektion"),
        start_here="Bestäm B-vektorn från den oändliga x-riktade ledaren i en godtycklig punkt (x,y,c) på rektangelns yta. Flödet använder B·n, inte |B|.",
        hints=(
            "Avståndet till x-axeln är R=√(y²+c²). B går azimutalt runt x-axeln och kan delas i y- och z-komponenter.",
            "För ytan z=c är normalen ±ẑ. Bestäm därför B_z; den innehåller en faktor y/(y²+c²).",
            "B är oberoende av x, så x-integralen ger bara faktorn a. Integrera sedan y från 0 till b; integralen av y/(y²+c²) ger en logaritm.",
        ),
        self_checks=(
            "Om b→0 ska flödet gå mot noll.",
            "Det är endast B-komponenten normal mot slingan som bidrar; den tangentiella komponenten får inte finnas i fluxresultatet.",
        ),
        common_pitfall="Att använda B=μ0I/(2πR) direkt i flödesintegralen utan projektion på ẑ.",
    ),

    # ------------------------------------------------------------------
    # Kapitel 8 – Magnetiska material och magnetiska kretsar
    # ------------------------------------------------------------------
    "PermanentMagnetAirGapBHCurve": G(
        problem_id="8.1",
        learning_goal="Bestäm arbetspunkten för en permanentmagnet genom skärningen mellan materialets B–H-kurva och magnetkretsens lastlinje.",
        concepts=("B–H-kurva", "magnetisk krets", "luftgap"),
        start_here="Läckage försummas och tvärsnittet är samma, så samma B går genom magneten och luftgapet. Skriv sedan cirkulationslagen för H runt hela magnetkretsen.",
        hints=(
            "I luftgapet gäller H_g=B/μ0. I permanentmagneten måste H_m hämtas från den givna tabellen och kan vara negativt.",
            "Utan spolen gäller ungefär H_m ℓ_m + H_g d = 0. Detta är en rät lastlinje i B–H-diagrammet; hitta dess skärning med tabellkurvan genom interpolation.",
            "Med N varv och ström I ändras cirkulationslagen till H_m ℓ_m + H_g d = NI med tecken enligt lindningens riktning. Arbetspunkten förskjuts längs samma materialkurva.",
        ),
        self_checks=(
            "B i luftgapet och magneten ska vara samma när läckage och areaförändring försummas.",
            "I del (a) måste permanentmagnetens H ligga i det negativa området av den givna tabellen för att balansera luftgapets positiva H.",
        ),
        common_pitfall="Att sätta H_m=B/(μ0μr) med en konstant μr; uppgiften ger uttryckligen ett icke-linjärt permanentmagnetmaterial via tabellen.",
        visualization_note="Just här är en B–H-graf med lastlinje pedagogiskt relevant eftersom lösningen bokstavligen är deras skärningspunkt.",
    ),
    "NonlinearIronMagneticCircuit": G(
        problem_id="8.2",
        learning_goal="Lösa en magnetisk krets där järnets materiallag är icke-linjär men flödet är gemensamt med luftgapet.",
        concepts=("icke-linjär B–H-lag", "Ampères lag", "luftgap"),
        start_here="Eftersom tvärsnittet är samma och läckage försummas kan du använda ett enda okänt B för både järn och luftgap.",
        hints=(
            "I luftgapet är H_g=B/μ0. I järnet måste materiallagen B=aH/(b+H) inverteras så att H_järn uttrycks som funktion av B.",
            "Sätt in båda H-bidragen i magnetomotoriska balansvillkoret H_järn·ℓ_järn + H_g d = NI.",
            "Ekvationen blir icke-linjär i B. När du löser den, kontrollera materiallagens villkor H>0 och att B ligger under mättnadsvärdet a; en matematisk rot kan vara fysikaliskt otillåten.",
        ),
        self_checks=(
            "Samma B ska gå genom järn och luftgap i den idealiserade serienkretsen.",
            "Luftgapet bör stå för en betydande del av den magnetomotoriska spänningen eftersom μ0 är mycket mindre än järnets effektiva permeabilitet.",
        ),
        common_pitfall="Att ersätta den givna icke-linjära materiallagen med en konstant relativ permeabilitet.",
    ),
    "MagneticBridgeCircuit": G(
        problem_id="8.4",
        learning_goal="Översätta en förgrenad järngeometri till ett nätverk av magnetiska reluktanser och hitta flödet i en bestämd gren.",
        concepts=("reluktans", "magnetisk krets", "flödesdelning"),
        start_here="Identifiera först magnetkretsens topologi: flödet går genom den vänstra ringhalvan och delar sig därefter mellan bryggan och den högra ringhalvan innan grenarna återförenas.",
        hints=(
            "För varje del används reluktansen ℜ=ℓ/(μ0μrS). Ringhalvorna har samma area men bryggan har en annan area och en annan medelväglängd.",
            "Rita ett magnetiskt motsvarighetsschema: en seriereluktans följd av två parallella reluktanser. Spolens magnetomotoriska spänning NI driver kretsen.",
            "Bestäm först totalflödet genom seriedelen och därefter hur det delar sig mellan de parallella grenarna. Det efterfrågade flödet är just bryggans grenflöde.",
        ),
        self_checks=(
            "Flödet i vänstra seriedelen ska vara summan av flödena genom bryggan och den högra ringhalvan.",
            "En gren med större reluktans ska bära mindre magnetiskt flöde vid samma magnetomotoriska potentialskillnad.",
        ),
        common_pitfall="Att lägga alla järndelar i serie; bryggan skapar en verklig parallell väg för det magnetiska flödet.",
        visualization_note="Ett reluktansnät bredvid den geometriska skissen är sannolikt mer lärorikt än en 3-D-fältbild för denna uppgift.",
    ),
    "CurrentCarryingMagneticTube": G(
        problem_id="8.5",
        learning_goal="Hålla isär H, B och M när ett fritt strömförande material kan vara magnetiskt.",
        concepts=("Ampères lag för H", "magnetisering", "styckvis fält"),
        start_here="Bestäm H först. Ampères lag för H beror på den fria strömmen, så samma H-lösning används i både kopparfallet och järnfallet.",
        hints=(
            "Dela upp R<a, a<R<b och R>b. I rörets material är den fria strömmen jämnt fördelad över annulusarean π(b²−a²), så den omslutna strömmen beror på R.",
            "Cirkulationslagen ∮H·dℓ=I_fri,innesluten ger H_φ i varje område. För R<a omsluts ingen fri ström.",
            "När H är känt: i omagnetiskt material är M=0 och B=μ0H. I linjärt järn gäller M=(μr−1)H och B=μ0μrH inne i materialet, men vakuumrelationen gäller utanför.",
        ),
        self_checks=(
            "H-fältet ska vara identiskt i del (a) och (b) eftersom den fria strömfördelningen är densamma.",
            "Utanför röret ska H motsvara fältet från hela strömmen I och avta som 1/R.",
        ),
        common_pitfall="Att sätta μr direkt in i Ampères lag för H och därmed ändra H när materialet byts; μr påverkar B och M, inte den fria strömkällan till H.",
    ),
    "HorseshoeMagnetAnchorForce": G(
        problem_id="8.6",
        learning_goal="Beräkna attraktionskraft från uppmätt magnetiskt flöde med hjälp av magnetiskt tryck i luftgap.",
        concepts=("magnetiskt tryck", "magnetiskt flöde", "kraft"),
        start_here="Materialegenskaperna behövs inte när flödet redan är känt. Börja med att omvandla Φ0 till B i luftgapens polytor.",
        hints=(
            "När läckage försummas är B≈Φ0/S vid vardera polytan.",
            "Magnetiskt tryck i ett litet luftgap är p=B²/(2μ0). Kraften från en pol är pS.",
            "Hästskoformen har två polytor som drar i ankaret. Summera därför båda lika stora kraftbidragen.",
        ),
        self_checks=(
            "Kraften ska vara proportionell mot Φ0².",
            "Glömmer du en av de två polytorna blir resultatet exakt en faktor två för litet i den idealiserade modellen.",
        ),
        common_pitfall="Att försöka bestämma H eller permanentmagnetens B–H-kurva trots att det uppmätta flödet redan räcker för kraftberäkningen.",
    ),
    "PermanentlyMagnetizedCylinderAxis": G(
        problem_id="8.12",
        learning_goal="Ersätta en homogen magnetisering med bundna magnetiseringsströmmar och därefter skilja mellan B och H.",
        concepts=("magnetisering", "magnetiseringsström", "B och H"),
        start_here="Beräkna de bundna magnetiseringsströmmarna från M. För konstant M är volymströmmen ∇×M noll; fråga i stället vilken yta som får K_m=M×n.",
        hints=(
            "På cylinderns mantel är n=R̂, så K_m går azimutalt och har konstant belopp M. Magneten är därmed ekvivalent med en ändlig solenoid med ytströmstäthet M.",
            "B längs axeln kan därför byggas som fältet från en ändlig solenoid eller genom att summera cirkulära strömslingor från z′=0 till h.",
            "När B är känt används H=B/μ0−M inne i magneten och H=B/μ0 utanför. Undersök sedan gränsen a≫h separat; den kan vara överraskande för B.",
        ),
        self_checks=(
            "På axeln måste B vara parallellt med ẑ av rotationssymmetri.",
            "I gränsen a≫h ger facitmodellen B→0 lokalt medan H→−M inne i magneten; kontrollera att dina uttryck tillåter detta.",
        ),
        common_pitfall="Att anta B=μ0M inne i en permanentmagnet. Magnetiseringens eget avmagnetiserande H-fält kan göra att B blir mycket mindre, till och med noll i ett gränsfall.",
    ),
    "MagnetizationCurrentsCylinder": G(
        problem_id="8.13",
        learning_goal="Härleda både volym- och ytmagnetiseringsströmmar från ett linjärt magnetiserat strömförande material och visa att deras nettoström tar ut sig.",
        concepts=("magnetiseringsström", "M=(μr−1)H", "cylindriska koordinater"),
        start_here="Bestäm först H inne i ledaren från den fria, jämnt fördelade strömmen I. Därifrån följer M direkt för ett linjärt material.",
        hints=(
            "För R<a är H_φ proportionellt mot R. Sätt M_φ=(μr−1)H_φ.",
            "Volymens magnetiseringsströmtäthet är J_m=∇×M. För ett rent φ-fält som beror på R behöver du z-komponenten (1/R)d(RM_φ)/dR.",
            "På ytan R=a används K_m=M×n med n=R̂. Beräkna sedan total volymström genom tvärsnittet och total ytström längs manteln; de ska ha motsatta tecken.",
        ),
        self_checks=(
            "Volym- och ytmagnetiseringsströmmarna ska tillsammans ge noll nettomagnetiseringsström i z-riktningen.",
            "När μr→1 ska både J_m och K_m gå mot noll.",
        ),
        common_pitfall="Att använda J_m=∇×H i stället för ∇×M; H bestäms av fri ström medan magnetiseringsströmmarna kommer från M.",
    ),

    # ------------------------------------------------------------------
    # Kapitel 9 – Induktans, induktion och elektromotorisk spänning
    # ------------------------------------------------------------------
    "MutualInductanceParallelWiresSquare": G(
        problem_id="9.2",
        learning_goal="Beräkna ömsesidig induktans genom att integrera magnetiskt flöde från två motriktade oändliga ledare genom en snedställd kvadrat.",
        concepts=("ömsesidig induktans", "magnetiskt flöde", "geometri"),
        start_here="Välj strömmen I1 i slinga 1 som källa och beräkna B mellan de två oändliga ledarna. Därefter är M=Φ21/I1.",
        hints=(
            "Mellan ledarna pekar de två B-bidragen åt samma håll genom kvadratens plan. Om x mäts från vänstra ledaren blir B(x) summan av två 1/avstånd-termer.",
            "Den snedställda kvadraten har inte konstant höjd i integrationsriktningen. För 0<x<d/2 är dess vertikala bredd proportionell mot x; använd symmetri för den andra halvan.",
            "Skriv dS = [kvadratens lokala bredd] dx och integrera B(x)dS. I kvoten Φ/I1 ska I1 försvinna och resultatet få induktansenheten henry.",
        ),
        self_checks=(
            "M ska vara proportionell mot μ0 och mot längdskalan d.",
            "De två halvorna av kvadraten ska ge samma flödesbidrag av spegelsymmetri.",
        ),
        common_pitfall="Att använda kvadratens hela area gånger B i centrum; B varierar kraftigt och blir singulärt nära de tangerande ledarna, även om integralen är ändlig.",
        visualization_note="En skiss som visar den lokala kvadratbredden som funktion av x gör integraluppställningen betydligt lättare att förstå.",
    ),
    "MutualInductanceCoaxialLoops": G(
        problem_id="9.4",
        learning_goal="Se reciprociteten i ömsesidig induktans genom två olika approximativa flödesberäkningar.",
        concepts=("ömsesidig induktans", "dipolapproximation", "reciprocitet"),
        start_here="Bestäm först vilken ström som är källa och vilket flöde som ska beräknas. Gör sedan del (a) och (b) som två oberoende vägar till samma M.",
        hints=(
            "I del (a): ersätt den lilla slingan med dipolmomentet m=I_liten πa². Använd dipolfältets z-komponent över den stora cirkelskivans yta och integrera 2πR dR.",
            "I del (b): använd det exakta axelfältet från den stora cirkulära slingan i den lilla slingans centrum. Eftersom a≪b,d kan detta B antas konstant över den lilla arean πa².",
            "Dividera respektive flöde med den ström som skapade fältet. De två uttrycken ska sammanfalla, vilket illustrerar M12=M21.",
        ),
        self_checks=(
            "M ska vara symmetrisk under byte av vilken slinga som betraktas som källa och mottagare inom approximationerna.",
            "När d blir mycket stort ska M avta ungefär som 1/d³.",
        ),
        common_pitfall="Att anta att dipolfältet från den lilla slingan är konstant över den stora slingan i del (a); den approximationen är inte motiverad när den mottagande slingan är stor.",
    ),
    "OpenSecondaryTransformerVoltage": G(
        problem_id="9.6",
        learning_goal="Koppla en tidsvarierande primärström till sekundärspänning via järnkärnans flöde och Faradays lag.",
        concepts=("Faradays lag", "transformator", "flödeskoppling"),
        start_here="Sekundärlindningen är öppen, så du behöver inte lösa någon sekundärström. Bestäm i stället flödet i järnkärnan som funktion av primärströmmen.",
        hints=(
            "Med samma approximation som för en lång magnetisk krets fås H≈N1 i1(t)/ℓ och B=μ0μrH.",
            "Flödet genom kärnan är Φ(t)=B(t)S. Sekundärens flödeskoppling är N2Φ(t).",
            "Använd ε2=−d[N2Φ(t)]/dt. Derivatan av cos(ωt) ger en faktor ω och en sinus med tecken enligt vald polaritet.",
        ),
        self_checks=(
            "Spänningsamplituden ska vara proportionell mot N1N2, μr, S, I0 och ω.",
            "Om ω→0 ska den inducerade spänningen gå mot noll även om primärströmmen är stor.",
        ),
        common_pitfall="Att använda transformatorns spänningsförhållande U2/U1=N2/N1 utan att någon primärspänning ens är given; här ska spänningen härledas från di1/dt.",
    ),
    "MovingLoopFieldWork": G(
        problem_id="9.13",
        learning_goal="Koppla mekaniskt arbete vid rörelse genom ett magnetfält till inducerad ström och resistiv värme.",
        concepts=("rörelse-emk", "Lenz lag", "energibalans"),
        start_here="Dela rörelsen i tre faser: slingan går in i fältområdet, är helt inne, och går ut. I vilken fas ändras magnetflödet?",
        hints=(
            "Under in- och utpassage ändras överlappningsarean med hastigheten dA/dt=a v, så |ε|=Bav. När slingan är helt inne är flödet konstant och ε=0.",
            "Den inducerade strömmen är I=ε/RΩ. Lenz lag säger att den magnetiska kraften motverkar rörelsen under de två övergångarna.",
            "Det mekaniska arbetet vid konstant hastighet kan enklast fås som den resistiva energin ∫I²RΩ dt. Varje övergång varar tiden a/v och det finns två lika stora bidrag.",
        ),
        self_checks=(
            "Inget arbete mot magnetisk broms behövs i idealmodellen när hela slingan ligger i ett helt homogent fält.",
            "Det totala arbetet ska öka med v eftersom snabbare rörelse ger större inducerad ström och större momentan bromskraft.",
        ),
        common_pitfall="Att räkna hela sträckan genom område B som en period med inducerad emk; endast när flödet genom slingan förändras uppstår emk.",
        visualization_note="En enkel animation av överlappningsarean A(t) kan vara mycket pedagogisk här, eftersom den direkt visar när dΦ/dt är noll respektive icke-noll.",
    ),
    "MovingLoopDipoleEmf": G(
        problem_id="9.14",
        learning_goal="Visa att tidsvarierande flöde i ett medföljande system och rörelse-emk i ett fast system beskriver samma inducerade spänning.",
        concepts=("Faradays lag", "rörelse-emk", "dipolfält"),
        start_here="Utnyttja a≪z. Då kan slingan behandlas som liten och dipolfältet utvecklas nära z-axeln. Gör först del (a), där flödesmetoden är kortast.",
        hints=(
            "I det medföljande systemet är slingan stilla och Φ≈B_z(z)πa². Sätt dz/dt=v och använd ε=−dΦ/dt.",
            "Dipolens axelfält avtar som z⁻³. Därför ger tidsderivatan en extra faktor proportionell mot v/z och slutresultatet skalar som z⁻⁴.",
            "I det fasta systemet används ε=∮(v×B)·dℓ. Den relevanta termen är dipolfältets lilla radiella komponent vid slingans radie; v ẑ kors B_R R̂ ger en tangentiell kraft runt hela slingan.",
        ),
        self_checks=(
            "Båda metoderna måste ge samma belopp på emk.",
            "När v=0 eller z→∞ ska emk gå mot noll.",
        ),
        common_pitfall="Att i del (b) använda enbart B_z. För rörelse-emk runt en cirkel ger v×B_z=0; den lilla radiella fältkomponenten är avgörande.",
    ),

    # ------------------------------------------------------------------
    # Kapitel 10 – Förskjutningsströmmar
    # ------------------------------------------------------------------
    "DisplacementCurrentCapacitor": G(
        problem_id="10.2",
        learning_goal="Se varför en tidsvarierande kondensatorström motsvaras av samma förskjutningsström genom gapet.",
        concepts=("förskjutningsström", "D-fält", "laddningskontinuitet"),
        start_here="Koppla den tillförda strömmen till hur snabbt plattladdningen Q(t) ändras. Därefter kan D-fältet mellan stora plattor skrivas direkt från Q(t).",
        hints=(
            "Strömmen till en platta är i(t)=dQ/dt med tecken enligt vald riktning.",
            "När randeffekter försummas är D=Q/A normalt mot plattorna och ungefär homogent över arean.",
            "Derivera D med avseende på tiden: J_F=∂D/∂t. Lägg märke till att plattavståndet d inte behövs för just denna storhet.",
        ),
        self_checks=(
            "Integralen av J_F över plattarean ska exakt ge den ledningsström i(t) som kommer fram i ledaren.",
            "J_F ska ha samma sinusform och fas som den givna strömmen i(t), inte som plattspänningen i allmänhet.",
        ),
        common_pitfall="Att först integrera strömmen till Q(t) och sedan tappa bort att tidsderivatan i J_F tar tillbaka den ursprungliga strömfunktionen.",
    ),
    "RadialChargeExpansionMaxwellTest": G(
        problem_id="10.3",
        learning_goal="Använd sfärisk symmetri och kontinuitet för att förstå hur ledningsström och förskjutningsström kan ta ut varandra i Ampère–Maxwells lag.",
        concepts=("sfärisk symmetri", "kontinuitetsekvationen", "Ampère–Maxwells lag"),
        start_here=(
            "Del (a) är i första hand en symmetriuppgift. En sfäriskt symmetrisk B-vektor skulle behöva vara radiell, men kombinera det med ∇·B=0 och kravet på ett reguljärt fält utan magnetiska monopoler."
        ),
        hints=(
            "För del (b), använd kontinuitetsekvationen i sfärisk symmetri: ∂ρ/∂t + (1/r²)∂(r²J_r)/∂r=0. Integrera från centrum till r och använd regularitet vid r=0 för att få J_r.",
            "Gauss lag ger D_r(r,t) från den inneslutna laddningen: 4πr²D_r = ∫_0^r ρ(r′,t)4πr′²dr′.",
            "Derivera D_r med avseende på tiden och jämför J_F=∂D/∂t med J. Om deras summa försvinner blir högerledet i ∇×B=μ0(J+J_F) noll, vilket gör B=0 konsistent med alla ekvationer.",
        ),
        self_checks=(
            "Trots att de verkliga laddningarna rör sig kan B=0 vara en lösning eftersom förskjutningsströmmen exakt kompenserar den radiella ledningsströmmen i Ampère–Maxwells lag.",
            "Resultatet får inte bryta sfärisk symmetri genom att välja någon särskild axel eller azimutal riktning.",
        ),
        common_pitfall="Att resonera 'rörliga laddningar ger alltid B≠0' utan att först kontrollera vad full sfärisk symmetri och Maxwells förskjutningsström tillåter.",
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
