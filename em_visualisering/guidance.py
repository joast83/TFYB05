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
        start_here='Skriv först kraftjämvikten ΣF=0 för en kula och Coulombs lag F_el=Q²/(4πε₀R²). Identifiera krafterna, avståndet R mellan laddningarna och sambandet mellan trådvinkeln θ och den sökta öppningsvinkeln α.',
        hint_titles=('Rita krafterna', 'Eliminera trådspänningen', 'Använd små vinklar'),
        hints=(
            'Krafterna är tyngden mg nedåt, trådspänningen T längs tråden och den elektriska repulsionen horisontellt. Sätt θ=α/2. Geometrin ger R=2ℓ sinθ.',
            'Projicera ΣF=0: T sinθ=F_el och T cosθ=mg. Dividera ekvationerna och sätt in Coulombkraften med R=2ℓ sinθ.',
            'Du har nu tanθ=Q²/[4πε₀mg(2ℓ sinθ)²]. Använd sinθ≈θ och tanθ≈θ i radianer, lös efter θ och byt sist tillbaka till α=2θ.',
        ),
        self_checks=(
            'Ökar vinkeln när |Q| ökar, och minskar den när m eller ℓ ökar? Kontrollera även gränsen Q→0.',
            'Uttrycket för α ska vara dimensionslöst. Sätt in värdena och kontrollera att α verkligen är mycket mindre än 1 radian; annars är småvinkelapproximationen inte tillförlitlig.',
        ),
        common_pitfall='Att använda α som trådens vinkel mot lodlinjen i stället för α/2.',
        setup_hint='Utgå från ΣF=0 och F_el=Q²/(4πε₀R²). Sätt in R=2ℓ sinθ i mg tanθ=F_el. Gör småvinkelapproximationen först när denna ekvation är uppställd.',
        geometry_hint='Rita en lodlinje från upphängningen. Varje kula ligger ℓ sinθ från lodlinjen, så avståndet mellan kulorna är dubbelt så stort. Vinkeln α är hela öppningsvinkeln.',
    ),
    'ChargedRingAxis': G(
        problem_id='2.2',
        learning_goal='Bygg upp Coulombintegralen för en kontinuerlig ringladdning från dQ′, r−r′ och |r−r′| innan symmetri används.',
        concepts=('Coulombs lag', 'linjeladdning och parametrisering', 'vektorintegral'),
        start_here='Utgå från det allmänna uttrycket E(r)=(1/4πε₀)∫[(r−r′)/|r−r′|³] dQ′ över källan. Identifiera först observationspunkten r, källpunkten r′ och laddningselementet dQ′ för hela ringen. Vilken koordinat är lämplig att integrera över?',
        hint_titles=('Laddningen på en liten båge', 'Vektorn från bågen till fältpunkten', 'Integrera ett helt varv'),
        hints=(
            'Låt r=(0,0,z) och r′(φ)=(a cosφ,a sinφ,0), där 0≤φ≤2π. Eftersom λ=Q/(2πa) och dℓ=a dφ blir dQ′=λa dφ=Q dφ/(2π).',
            'Beräkna r−r′=(−a cosφ,−a sinφ,z) och |r−r′|=√(a²+z²). Sätt först nu in dessa uttryck tillsammans med dQ′ i den allmänna fältintegralen.',
            'Enhetsvektorn R̂(φ)=cosφ x̂+sinφ ŷ ändrar riktning runt ringen. Skriv därför bidragen i en fast bas innan du integrerar komponenterna. Bidragen med cosφ och sinφ försvinner över ett helt varv, medan z-komponenten återstår. Kontrollera att detta följer av integralen, utan att ersätta ringen med två punktladdningar.',
        ),
        self_checks=(
            'Fältet ska vara noll vid z=0 och E_z ska byta tecken när z byter tecken. Rotationssymmetrin kring z-axeln bekräftar att tvärkomponenterna ska försvinna.',
            'För |z|≫a ska fältet närma sig punktladdningsfältet. För Q>0 ska det peka bort från ringen på båda sidor.',
        ),
        common_pitfall='Att glömma bågfaktorn a i dQ′=λa dφ eller integrera fältets belopp i stället för dess komponenter. Symmetri kan användas för att kontrollera komponentintegralerna.',
        visualization_note='En axelgraf är användbar först efter härledningen, framför allt för att kontrollera z=0 och fjärrfältet.',
        setup_hint='Starta med E(r)=(1/4πε₀)∫[(r−r′)/|r−r′|³] dQ′. Använd r=(0,0,z), r′=(a cosφ,a sinφ,0), dQ′=Q dφ/(2π) och integrationsgränserna 0 till 2π; integrera sedan komponentvis.',
        geometry_hint='φ beskriver källpunktens position på hela ringen, medan observationspunkten r=(0,0,z) hålls fast. Vektorn r−r′ pekar från laddningselementet mot observationspunkten och har samma längd för alla φ.',
    ),
    'FiniteLineCharge2D': G(
        problem_id='2.3',
        learning_goal='Identifiera källkoordinat, laddningselement och separationsvektor i Coulombintegralen för en ändlig tråd.',
        concepts=('linjeladdning', 'vektorintegral', 'gränsvärde'),
        start_here='Skriv den allmänna Coulombintegralen E(r)=(1/4πε₀)∫[(r−r′)/|r−r′|³] dQ′. Låt sedan r vara den fasta observationspunkten (x,0,0) och låt r′ löpa längs tråden. Bestäm vilka gränser och vilket dQ′ som hör till källan.',
        hint_titles=('Välj källkoordinat och gränser', 'Skriv de två fältkomponenterna', 'Ta gränsen för en lång tråd'),
        hints=(
            'Välj r′=(0,0,z′) med −b≤z′≤a. Trådens konstanta linjeladdningstäthet ger dQ′=ρℓ dz′. Här är z′ integrationsvariabeln medan x hålls konstant.',
            'Identifiera r−r′=(x,0,−z′) och |r−r′|=√(x²+z′²). Sätt in dQ′ och båda dessa uttryck i Coulombintegralen innan du delar upp den i x- och z-komponenter.',
            'Beräkna de två komponentintegralerna över −b≤z′≤a. I del (b) låter du därefter a och b gå mot oändligheten oberoende av varandra; kontrollera att z-komponenten försvinner och att det återstående fältet avtar som 1/|x|.',
        ),
        self_checks=(
            'Om a=b ska E_z försvinna. Om a>b och ρℓ>0 ska E_z vara negativ vid (x,0,0), eftersom mer positiv laddning ligger på +z-sidan.',
            'I den oändliga gränsen ska E_z→0 och |E_x| avta som 1/|x|. Fältet ska peka bort från tråden för positiv linjeladdning.',
        ),
        common_pitfall='Att använda cylindersymmetri för den ändliga tråden, eller blanda ihop observationskoordinaten x med integrationsvariabeln z′.',
        setup_hint='Sätt r=(x,0,0), r′=(0,0,z′), dQ′=ρℓ dz′ och r−r′=(x,0,−z′) i E(r)=(1/4πε₀)∫[(r−r′)/|r−r′|³] dQ′. Nämnaren blir (x²+z′²)^(3/2); integrera från −b till a.',
        geometry_hint='Tråden följer z-axeln från −b till a, medan fältpunkten ligger på x-axeln. Vektorn r−r′ går från källelementet (0,0,z′) till observationspunkten (x,0,0), så dess z-komponent är −z′.',
    ),
    'SemiCircularSurfaceAxis': G(
        problem_id='2.4',
        learning_goal='Bygg upp Coulombintegralen för en halvcirkelskiva och använd först därefter den återstående symmetrin.',
        concepts=('ytladdning', 'polära koordinater', 'komponentsymmetri'),
        start_here='Börja med E(r)=(1/4πε₀)∫[(r−r′)/|r−r′|³] dQ′ över den laddade ytan. Identifiera observationspunkten, välj två koordinater för källpunkten på halvcirkelskivan och bestäm dQ′ från ytladdningstätheten.',
        hint_titles=('Ytelementet på halvskivan', 'Avstånd och riktning till fältpunkten', 'Vilken komponent försvinner?'),
        hints=(
            'Välj r=(0,0,z) och r′=(R cosφ,R sinφ,0), där 0≤R≤a och 0≤φ≤π eftersom skivan ligger på sidan y≥0. Ytelementet är dS′=R dR dφ och dQ′=ρs R dR dφ.',
            'Beräkna r−r′=(−R cosφ,−R sinφ,z) och |r−r′|=√(R²+z²). Sätt in dQ′, separationsvektorn och dess belopp i Coulombintegralen med de två integrationsgränserna.',
            'Skriv R̂(φ)=cosφ x̂+sinφ ŷ i en fast bas innan du integrerar över φ. x-komponenten blir noll, men y-komponenten försvinner inte för en halvcirkelskiva. Genomför därefter radialintegralerna.',
        ),
        self_checks=(
            'För ρs>0 och z>0 ska E_x=0, E_y<0 och E_z>0. Kontrollera riktningarna mot den valda halvcirkeln.',
            'Långt bort ska den ledande termen vara punktladdningsfältet för Q=ρsπa²/2; tvärkomponenten avtar snabbare. Punkten z=0 ligger på skivans kant och är inte ett vanligt reguljärt kontrollvärde.',
        ),
        common_pitfall='Fick du även E_y=0? Kontrollera vinkelgränserna: integralen av sinφ från 0 till π försvinner inte. Ett helt varv skulle beskriva en annan yta.',
        setup_hint='Starta med E(r)=(1/4πε₀)∫[(r−r′)/|r−r′|³] dQ′. Använd dQ′=ρs R dR dφ, r−r′=(−R cosφ,−R sinφ,z) och |r−r′|=√(R²+z²), med 0≤R≤a och 0≤φ≤π.',
        geometry_hint='I originalfiguren ligger den laddade halvcirkelskivan i xy-planet med y≥0. r′ är en rörlig källpunkt på skivan och r=(0,0,z) är den fasta fältpunkten; y-symmetri saknas men x-bidragen tar ut varandra.',
    ),
    'SphericalShellPotential': G(
        problem_id='2.5',
        learning_goal='Härled skalets potential direkt från den allmänna potentialintegralen med ett korrekt dQ′ och |r−r′|.',
        concepts=('potentialintegral', 'sfärisk symmetri', 'källområde'),
        start_here='Utgå från potentialintegralen i originaluppgiften: V(r)=(1/4πε₀)∫ dQ′/|r−r′| över källområdet. Här är källområdet det laddade sfärskalets yta, inte dess volym. Identifiera dQ′, r−r′ och |r−r′| innan du integrerar.',
        hint_titles=('Laddningselementet på skalet', 'Avståndet till observationspunkten', 'Dela upp svaret vid skalradien'),
        hints=(
            'Placera den fasta observationspunkten på z-axeln: r=(0,0,r). Beskriv en källpunkt på skalet med r′=a(sinθ cosφ,sinθ sinφ,cosθ). För jämn ytladdning är ρs=Q/(4πa²) och dQ′=ρs a²sinθ dθ dφ.',
            'Bilda r−r′=(−a sinθ cosφ,−a sinθ sinφ,r−a cosθ). Dess belopp är |r−r′|=√(r²+a²−2ar cosθ). Sätt nu in detta avstånd och dQ′ i originalets potentialintegral.',
            'Integrera först över φ och använd sedan u=cosθ. Vid gränserna dyker r+a och |r−a| upp; behandla därför r<a och r>a var för sig. Fallet r=0 kan kontrolleras direkt utan division med r.',
        ),
        self_checks=(
            'V ska vara kontinuerlig vid r=a och gå mot noll när r→∞.',
            'Kontrollera med E_r=−dV/dr: inuti ska fältet vara noll och utanför ska det ha punktladdningens 1/r²-beroende. Derivatan får däremot ha ett språng vid den laddade ytan.',
        ),
        common_pitfall='Att ersätta den begärda potentialintegralen med Gauss lag, att integrera över skalets volym eller att blanda ihop observationsradien r och skalradien a.',
        setup_hint='Sätt r=(0,0,r), r′=a(sinθ cosφ,sinθ sinφ,cosθ), dQ′=[Q/(4πa²)]a²sinθ dθ dφ och |r−r′|=√(r²+a²−2ar cosθ) i V(r)=(1/4πε₀)∫dQ′/|r−r′|.',
        geometry_hint='Välj observationspunkten på z-axeln tack vare sfärisk symmetri. Källpunkten r′ ligger på sfärytan med fast radie a; vinkeln θ mäts från z-axeln. Skillnadsvektorns längd fås med cosinussatsen.',
    ),
    'ConcentricChargedCylinders': G(
        problem_id='2.6',
        learning_goal='Välja rätt Gaussyta och hålla reda på vilken laddning som omsluts i olika radialområden.',
        concepts=(
            'Gauss lag',
            'cylindersymmetri',
            'styckvis fält',
        ),
        start_here='Skriv Gauss lag ∮_S E·n dS=Q_in/ε₀. Identifiera systemets symmetri, en lämplig sluten yta och vilken laddning den omsluter. Försumma ändeffekter för de långa cylindrarna.',
        hint_titles=('Vilka ytor ger flöde?', 'Vilka cylindrar omsluts?', 'Bestäm fältet områdesvis'),
        hints=(
            'Cylindersymmetrin ger E=E_R(R) R̂. Välj en koaxial Gauss-cylinder med radie R och längd L. På manteln är E·n=E_R och arean 2πRL; på ändytorna är E·n=0.',
            'Beräkna Q_in från de verkliga laddade ytornas areor. För R<a är den noll, för a<R<b är den ρsa·2πaL och för R>b tillkommer ρsb·2πbL.',
            'Sätt in varje laddningsuttryck i E_R·2πRL=Q_in/ε₀ och lös efter E_R i respektive område. Multiplicera med R̂ för vektorfältet och behåll laddningarnas tecken.',
        ),
        self_checks=(
            'För R<a är fältet noll. Utanför båda cylindrarna ska det också bli noll om aρsa+bρsb=0, även om vardera cylindern är laddad.',
            'Med normalen riktad mot större R ska E_R(utanför)−E_R(innanför)=ρs/ε₀ vid varje laddad yta. Kontrollera båda sprången.',
        ),
        common_pitfall='Fick du samma fältuttryck i alla tre områden? Skriv Q_in på nytt för varje radie. Gaussytan kan omsluta noll, en eller två laddade cylinderytor.',
        setup_hint='Identifiera vänsterledet som E_R·2πRL och högerledet som Q_in/ε₀. Gör en rad för varje radialområde och sätt in rätt Q_in innan du löser efter E_R; den godtyckliga längden L ska förkortas bort.',
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
        start_here='Skriv Gauss lag ∮_S E·n dS=Q_in/ε₀ och potentialskillnaden V(a)−V(b)=∫_a^b E_r dr. Bestäm först E_r i gapet från symmetrin och laddningen; använd därefter kravet |E|≤Emax för optimeringen.',
        hint_titles=('Fältet i gapet', 'Laddningsgränsen vid ytan', 'Optimera spänningen'),
        hints=(
            'Sfärisk symmetri ger E=E_r(r) r̂. En sfärisk Gaussyta i a<r<b omsluter innerledarens laddning Q, så 4πr²E_r=Q/ε₀. Lös efter E_r innan du söker fältmaximum.',
            'Fältbeloppet avtar som 1/r² och är störst vid a. Sätt |E(a)|=Emax och bestäm |Q|max(a). När a varieras i optimeringen varierar alltså även den tillåtna laddningen.',
            'Sätt in |Q|max(a) i Umax(a)=∫_a^b |E_r| dr. Derivera med avseende på a med b och Emax konstanta. Lös det stationära villkoret i 0<a<b och jämför med randgränserna.',
        ),
        self_checks=(
            'Vid genomslagsbegränsad laddning ska den tillåtna spänningen gå mot noll när a→0 och när a→b. Ett inre maximum måste jämföras med dessa gränser.',
            'Den stationära punkten ska ligga i 0<a<b och ha negativ andraderivata. Enheten i spänningsuttrycket ska vara Emax gånger en längd.',
        ),
        common_pitfall='Att optimera kondensatorns vanliga spänningsuttryck med Q konstant, trots att Q här begränsas av Emax och därför beror på a.',
        setup_hint='Kedjan är 4πr²E_r=Q/ε₀ → |Q|max=4πε₀a²Emax → Umax(a)=∫_a^b |Q|max/(4πε₀r²) dr. Utför integralen innan du optimerar; håll inte Q konstant.',
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
        start_here='Skriv ∮_S E·n dS=Q_in/ε₀ och V(r)=∫_r^∞ E_r(s) ds med V(∞)=0. Använd sfärisk symmetri och identifiera Q_in i de tre radialområdena innan potentialen beräknas.',
        hint_titles=('Innesluten laddning', 'Integrera genom flera områden', 'När skalen kopplas ihop'),
        hints=(
            'Sfärisk symmetri gör fältet radiellt och lika stort över Gaussytan: 4πr²E_r=Q_in/ε₀. Q_in är 0 för r<a, Qa för a<r<b och Qa+Qb för r>b. Lös efter E_r i varje område.',
            'Integrera från observationsradien till oändligheten. För a<r<b delas vägen vid b; för r<a tillkommer ett område med E=0. Behåll bidragen från alla passerade områden så att potentialen får samma referens överallt.',
            'I del (b) betecknas slutladdningarna qa och qb. Skriv qa+qb=Qa+Qb och V(a)−V(b)=∫_a^b E_r dr=0 under förbindelsen. Sätt in gapfältet med qa och lös sedan laddningsfördelningen.',
        ),
        self_checks=(
            'Potentialen ska vara kontinuerlig vid a och b och närma sig noll vid oändligheten. Utanför b beror den bara på den sammanlagda laddningen.',
            'Efter förbindelsen ska laddningen vara bevarad och potentialskillnaden mellan skalen vara noll. I den sfäriskt symmetriska modellen ska resultatet också ge noll fält i gapet.',
        ),
        common_pitfall='Att bevara Qa och Qb var för sig efter sammankopplingen, eller anta att ett tomt område alltid har E=0. Här måste fältet i gapet följa av potentialvillkoret och geometrin.',
        setup_hint='Sätt först E_r=Q_in/(4πε₀r²) områdesvis. I gapet är V(r)=∫_r^b Qa/(4πε₀s²) ds+∫_b^∞ (Qa+Qb)/(4πε₀s²) ds. Efter förbindelsen används samma uppställning med de nya laddningarna och V(a)=V(b).',
        geometry_hint='Markera en sfärisk Gaussyta i vart och ett av de tre radialområdena. Kontrollera vilka laddade skal som ligger innanför ytan. Dela sedan integrationsvägen från observationsradien till oändligheten där fältuttrycket ändras.',
    ),
    "AtmosphericChargeDensity": G(
        problem_id="2.9",
        learning_goal="Översätta en observerad fältändring till medelladdning via Gauss lag/divergens.",
        concepts=("Gauss lag", "fältgradient", "teckenkonvention"),
        start_here='Skriv Gauss lag ∮_S E·n dS=Q_in/ε₀ och medelladdningstätheten ⟨ρ⟩=Q_in/Volym. Här är fälten givna och laddningen söks. Identifiera ytornas normaler och fältens signerade komponenter innan de sätts in.',
        hint_titles=('Välj riktning och yta', 'Tecknen på topp och botten', 'Från laddning till medeltäthet'),
        hints=(
            'Välj z uppåt: E_z(0)=−300 V/m och E_z(h)=−20 V/m, h=1400 m. Använd en vertikal cylinder med tvärsnittsarea S och höjd h. Det vertikala fältet ger inget flöde genom manteln.',
            'Toppen har normal +ẑ och botten −ẑ. Därför blir ∮E·n dS=S E_z(h)−S E_z(0). Sätt detta lika med Q_in/ε₀.',
            'Lös efter Q_in och dividera med volymen Sh. Du får en medeltäthet; två fältvärden räcker inte för att bestämma den lokala funktionen ρ(z).',
        ),
        self_checks=(
            'S ska förkortas bort och ε0ΔE/h ha enheten C/m³.',
            'Medeltätheten ska vara positiv eftersom E_z ökar med höjden. Om fälten vore lika skulle medeltätheten vara noll, även om lokal laddning kunde finnas.',
        ),
        common_pitfall="Att subtrahera fältens belopp utan att först ta hänsyn till ytornas normalriktningar.",
        geometry_hint='Rita två nedåtpilar, en vid marken och en vid h. Rita sedan utåtnormalerna separat: uppåt på toppen och nedåt på botten. Det är skalärprodukterna E·n som bestämmer flödets tecken.',
        setup_hint='Sätt in flödet och volymen: S[E_z(h)−E_z(0)]=⟨ρ⟩Sh/ε₀. Förkorta S och lös efter ⟨ρ⟩. Använd fältkomponenterna med tecken, inte bara beloppen.',
    ),
    "OffsetCavitySphereExterior": G(
        problem_id="2.10",
        learning_goal="Använd superposition för att ersätta ett hålrum med en negativ laddningsfördelning.",
        concepts=("superposition", "homogent laddat klot", "förskjutet centrum"),
        start_here='Skriv superpositionen E=E_stor+E_hål och Gauss lag ∮_S E·n dS=Q_in/ε₀ för varje sfäriskt symmetrisk hjälpfördelning. Identifiera dess laddning och avståndet från dess eget centrum till observationspunkten.',
        hint_titles=('Bygg hålrummet av två klot', 'Fältet från varje klot', 'Mät från rätt centrum'),
        hints=(
            'Beskriv materialet som ett helt klot med täthet ρ plus ett mindre klot med täthet −ρ i hålrummet. Laddningarna är Q_stor=4πρb³/3 och Q_hål=−4πρa³/3.',
            'För varje klot ger sfärisk symmetri och en Gaussyta utanför klotet 4πs²E_s=Q/ε₀, där s mäts från just det klotets centrum. Punkterna x>b ligger utanför båda hjälpfördelningarna.',
            'Hålrummets centrum ligger vid x=−d enligt originalets geometri. Avstånden är x respektive x+d och båda radiella enhetsvektorerna pekar längs +x här. Sätt in dessa i de två fälten och summera deras signerade x-komponenter.',
        ),
        self_checks=(
            'När a→0 ska hålrummets bidrag försvinna. När d→0 ska resultatet motsvara nettoladdningen i origo.',
            'Långt bort, x≫b,d, ska den ledande termen vara fältet från nettoladdningen 4πρ(b³−a³)/3. För ρ>0 ska E_x vara positivt på den angivna delen av x-axeln.',
        ),
        common_pitfall="Att använda avståndet x till båda sfärernas centrum trots att hålrummets centrum är förskjutet.",
        geometry_hint='Markera centrum 0, hålrummets centrum −d och observationspunkten x>b på samma axel. Kontrollera avstånden i din egen skiss: ett hålrum vid +d skulle i stället ge avståndet x−d.',
        setup_hint='Bestäm först varje hjälpfält ur 4πs²E_s=Q/ε₀. Sätt sedan E_x=[Q_stor/x²+Q_hål/(x+d)²]/(4πε₀). Q_hål innehåller redan minustecknet. En enda Gaussyta kring hela det osymmetriska objektet kan inte ge det lokala fältet på detta sätt.',
    ),
    "CoaxialCylinderVoltage": G(
        problem_id="2.11",
        learning_goal="Gå från Gauss-lagens koaxialfält till ett givet spänningsfall.",
        concepts=("koaxial geometri", "Gauss lag", "potentialskillnad"),
        start_here='Skriv ∮_S E·n dS=Q_in/ε₀ och V(a)−V(b)=∫_a^b E_R dR. Cylindersymmetrin bestämmer hur fältet beror på R; den givna spänningen bestämmer därefter dess storlek.',
        hint_titles=('Flöde genom manteln', 'Bestäm konstanten från spänningen', 'Var ligger mittpunkten?'),
        hints=(
            'Försumma ändeffekter och välj en koaxial Gauss-cylinder med radie a<R<b och längd L. Inför innerledarens laddning per längd λ. E är radiellt, så E_R·2πRL=λL/ε₀.',
            'Lös efter E_R. För fältbeloppet kan du skriva |E_R|=K/R med K=|λ|/(2πε₀). Sätt detta i U=∫_a^b |E_R| dR och bestäm K från U=K ln(b/a).',
            'Mittemellan ytorna är observationsradien R=a+(b−a)/2=(a+b)/2. Sätt in den först när fältfunktionen är bestämd.',
        ),
        self_checks=(
            'Uttrycket ska ha enheten V/m och vara proportionellt mot U. Logaritmens argument b/a ska vara dimensionslöst.',
            'I ett tunt gap, b−a≪a, ska fältet närma sig plattkondensatorns U/(b−a). Generellt avtar fältbeloppet som 1/R.',
        ),
        common_pitfall="Att anta ett homogent fält U/(b−a), vilket inte gäller för cylindrisk geometri.",
        geometry_hint='R mäts från den gemensamma axeln, inte från innerledarens yta. Halva gapbredden (b−a)/2 måste därför läggas till a.',
        setup_hint='Identifiera mantelarean 2πRL och Q_in=λL i Gauss lag. Lös sedan U=∫_a^b |λ|/(2πε₀R) dR efter |λ|, eller efter K=|λ|/(2πε₀), och beräkna fältbeloppet vid R=(a+b)/2.',
    ),
    "SphericalConductorBreakdown": G(
        problem_id="2.12",
        learning_goal="Koppla luftens genomslagsfält till maximal laddning och potential på en sfärisk ledare.",
        concepts=("ledande sfär", "genomslag", "potential"),
        start_here='Skriv ∮_S E·n dS=Q_in/ε₀ och V(a)=∫_a^∞ E_r dr. Bestäm fältet från sfärisk symmetri och laddningen Q innan du tillämpar luftens gräns |E|≤Emax.',
        hint_titles=('Fältet utanför sfären', 'Var nås genomslagsgränsen?', 'Potentialen relativt oändligheten'),
        hints=(
            'Välj en sfärisk Gaussyta med r>a. Fältet är radiellt och konstant över ytan, så 4πr²E_r=Q/ε₀. Lös efter E_r; inne i metallen är E=0.',
            'Det yttre fältbeloppet avtar med r och är störst precis utanför r=a. Sätt |Q|/(4πε₀a²)=Emax och lös efter den största tillåtna laddningens belopp.',
            'Integrera E_r från a till ∞ för att få ytpotentialen med V(∞)=0. Sätt in laddningsgränsen och därefter a=0,10 m och Emax=3·10⁶ V/m i del (b).',
        ),
        self_checks=(
            'Qmax ska växa som a², medan den maximala potentialens belopp växer som a. Kontrollera enheterna C respektive V.',
            'Kvoten |V(a)|/a ska vara Emax vid gränsen. Potentialen har samma tecken som Q, medan genomslagsvillkoret beror på fältets belopp.',
        ),
        common_pitfall="Att sätta genomslagsvillkoret vid någon godtycklig punkt utanför sfären i stället för på ytan.",
        geometry_hint='Markera r=a precis på luftsidan av metallytan. Där är det yttre fältet störst; fältet inne i metallen kan inte användas för luftens genomslagsvillkor.',
        setup_hint='Gauss lag ger E_r=Q/(4πε₀r²). Använd först |E_r(a)|=Emax och därefter V(a)=∫_a^∞ Q/(4πε₀r²) dr. Genomslagsvillkoret gäller belopp, medan potentialen behåller laddningens tecken.',
    ),
    "CoaxialTubeSpaceCharge": G(
        problem_id="2.13",
        learning_goal="Lösa Poisson/Gauss-problemet i cylindrisk geometri när det finns en konstant rymdladdning.",
        concepts=("rymdladdning", "cylindrisk Gauss lag", "randvillkor"),
        start_here='Skriv Gauss lag ∇·E=ρ/ε₀ och V(b)−V(a)=−∫_a^b E·dl. Identifiera den konstanta, okända tätheten ρ, cylindersymmetrin och randvillkoren E_R(a)=0, V(a)=0 och V(b)=U.',
        hint_titles=('Förenkla divergensen', 'Använd fältvillkoret vid katoden', 'Bestäm molnets totala laddning'),
        hints=(
            'Cylindersymmetri och försummade ändeffekter ger E=E_R(R) R̂. Då blir Gauss lag (1/R)d(RE_R)/dR=ρ/ε₀. Integrera med avseende på R: E_R=ρR/(2ε₀)+C/R.',
            'Sätt in E_R(a)=0 för att bestämma C. Detta ger fältet i gapet som funktion av den ännu okända tätheten ρ.',
            'Sätt fältet i U=−∫_a^b E_R dR och lös efter ρ. Den totala molnladdningen är sedan Q=ρπ(b²−a²)ℓ. Omvandla radier och längd till meter.',
        ),
        self_checks=(
            'Kontrollera både E_R(a)=0 och att −∫_a^b E_R dR=+300 V. Med denna spänning ska ρ och molnets totala laddning vara negativa.',
            'För negativ ρ ska E_R peka inåt i gapet, medan kraften på en elektron pekar utåt. Q ska vara proportionell mot ℓ, och ha enheten C.',
        ),
        common_pitfall="Att använda det laddningsfria koaxialfältet C/R trots att området innehåller konstant rymdladdning.",
        geometry_hint='R löper från katodens radie a till anodens radie b. Molnet fyller ett cylindriskt skal, så dess volym är skillnaden mellan två cylindervolymer. Modellen försummar ändeffekter.',
        setup_hint='Börja med d(RE_R)/dR=ρR/ε₀. Efter integration och E_R(a)=0 är E_R=ρ(R−a²/R)/(2ε₀). Bestäm ρ ur U=−∫_a^b E_R dR och använd sedan molnets hela volym.',
    ),
    "RadialChargeSphere": G(
        problem_id="2.16",
        learning_goal="Bygga potentialintegralen i centrum från den givna volymladdningen och källkoordinaterna.",
        concepts=("potential", "sfäriska skal", "rymdladdning"),
        start_here='Skriv V(r)=(1/4πε₀)∫ dQ′/|r−r′| med V(∞)=0. Observationspunkten är r=0. Identifiera dQ′=ρ(r′)dV′, separationsvektorn r−r′ och dess belopp för den givna volymladdningen.',
        hint_titles=('Volymelementet', 'Avståndet till centrum', 'Radialintegralen'),
        hints=(
            'Använd sfäriska källkoordinater: r′=s(sinθ cosφ,sinθ sinφ,cosθ), 0≤s≤a, 0≤θ≤π och 0≤φ≤2π. Då är dQ′=A(a−s)s²sinθ ds dθ dφ.',
            'I centrum är r−r′=−r′ och |r−r′|=s. Sätt in detta och dQ′ i potentialintegralen. Vinkelintegralerna ger 4π eftersom återstoden är oberoende av vinklarna.',
            'Det återstår V(0)=(1/ε₀)∫₀ᵃ A(a−s)s ds. Integrera de två potenstermerna. Utanför a är tätheten noll, så inget ytterligare källbidrag ska adderas.',
        ),
        self_checks=(
            'Efter förenkling är integranden proportionell mot s(a−s); den går mot noll i centrum trots faktorn 1/s i potentialkärnan.',
            'A har enheten C/m⁴. Potentialen ska skala som Aa³/ε0 och ha samma tecken som A. Symmetrin ger E(0)=0, men inte V(0)=0.',
        ),
        common_pitfall='Att sätta V(0)=0 för att fältet är noll i centrum, eller ersätta hela fördelningen med en punktladdning när observationspunkten ligger inuti den.',
        geometry_hint='Skilj på observationspunkten r=0 och källskalets radie r′. Avståndet i Coulombpotentialen är r′; det är inte noll bara för att observationspunkten ligger i origo.',
        setup_hint='Identifiera dQ′=A(a−s)s²sinθ ds dθ dφ och |r−r′|=s vid r=0. Potentialkärnans 1/s lämnar faktorn s i radialintegralen efter vinkelintegrationen; integrera sedan från 0 till a.',
    ),
    "InsertedMetalPlateCapacitor": G(
        problem_id="2.18",
        learning_goal="Skilja på vad som hålls konstant före och efter att batteriet kopplats bort.",
        concepts=("plattkondensator", "konstant laddning", "ledare i fält"),
        start_here='Skriv Gauss lag ∮_S E·n dS=Q_in/ε₀ och potentialskillnaden ΔV=−∫E·dl. Identifiera plattladdningen, fältets riktning och de delar av gapet där fältet finns. Batteriet kopplas bort efter uppladdningen, så Q är därefter bevarad.',
        hint_titles=('Laddningen före frånkoppling', 'Spänningsfallet med metallplattan', 'Det alternativa försöket'),
        hints=(
            'Utan kanteffekter är fältet normalt mot plattorna och homogent i luftgapet. En Gaussbox från metallens inre till gapet ger E A=Q/ε₀ för beloppen. Spänningen i del (a) är U=E d0; kombinera ekvationerna för att bestämma Q.',
            'I del (b) behålls Q från (a), så luftfältet är oförändrat. Inuti den införda metallen är E=0. Beräkna spänningsintegralen över de två luftgapen, vars sammanlagda tjocklek är d0−d1.',
            'I del (c) görs ett separat försök utan metallplattan. Behåll samma Q och integrera luftfältet över det nya avståndet d2. Plattorna bär +Q och −Q i alla tre fallen.',
        ),
        self_checks=(
            'I del (b) ska spänningen minska med faktorn (d0−d1)/d0; i del (c) ska den öka med faktorn d2/d0. Båda jämförs med ursprungsspänningen.',
            'Om d1→0 återfås ursprungsspänningen. Metallplattans placering i gapet ändrar inte resultatet i idealmodellen, så länge den inte vidrör elektroderna och kanteffekter försummas.',
        ),
        common_pitfall='Att hålla U konstant efter att batteriet kopplats bort, eller använda d2−d1 i del (c) trots att metallinsättning och ökat avstånd är alternativa försök.',
        geometry_hint='Rita två separata skisser: (b) två luftgap plus en metallplatta, (c) ett enda luftgap med bredd d2. Inuti metallen är potentialen konstant; bara luftgap bidrar till spänningsfallet.',
        setup_hint='Lös först E A=Q/ε₀ tillsammans med U=E d0. Använd sedan samma E=Q/(ε₀A) i U_b=E(d0−d1) och U_c=E d2. Den införda metallens spänningsfall är noll.',
    ),
    "UniformSpaceChargePlates": G(
        problem_id="2.19",
        learning_goal="Kombinera Poissons ekvation med en föreskriven potentialskillnad och sedan lokalisera E=0.",
        concepts=("Poissons ekvation", "1D-fält", "randvillkor"),
        start_here='Skriv Gauss lag ∇·E=ρ0/ε₀ och V(d)−V(0)=−∫₀ᵈ E_x dx. Välj x=0 vid plattan med V0 och x=d vid jord. Plansymmetrin ger E=E_x(x) x̂; bestäm denna funktion innan du söker dess nollställe.',
        hint_titles=('Fältets lutning', 'Bestäm integrationskonstanten', 'Ligger nollstället i gapet?'),
        hints=(
            'Gauss lag reduceras till dE_x/dx=ρ0/ε₀ eftersom fältet bara varierar tvärs plattorna. Integrera till E_x=ρ0x/ε₀+C.',
            'Sätt in V(0)=V0 och V(d)=0 i potentialskillnaden: ∫₀ᵈ E_x dx=V0. Bestäm C ur denna ekvation; tätheten ensam bestämmer inte hela fältet.',
            'För ρ0≠0, lös E_x(x0)=0. Kräv därefter 0<x0<d för ett nollställe strikt mellan plattorna; x0=0 eller d är gränsfall på ytorna. Hantera ρ0=0 separat.',
        ),
        self_checks=(
            'E_x ska vara linjärt med lutningen ρ0/ε0 och dess integral över gapet ska vara V0. Om V0=0 och ρ0≠0 ligger nollpunkten mitt i gapet.',
            'Villkoret för en inre nollpunkt blir |V0|<|ρ0|d²/(2ε0); likhet placerar nollpunkten på en yta. För ρ0=0 måste fallet behandlas separat: E_x=V0/d är konstant och är noll överallt endast om V0=0.',
        ),
        common_pitfall='Att blanda ihop vilken platta som ligger vid x=0, eller rapportera en algebraisk nollpunkt utanför gapet som en fysisk lösning mellan plattorna.',
        geometry_hint='Markera 0 vid V0-plattan och d vid jord. Om du i stället mäter från den jordade plattan måste du omvandla koordinaten med x_ny=d−x; samma fysiska punkt får då ett annat koordinatvärde.',
        setup_hint='Sätt E_x=ρ0x/ε₀+C i ∫₀ᵈ E_x dx=V0 och lös C. Sätt sedan det färdiga fältuttrycket lika med noll och pröva om lösningen ligger inne i gapet.',
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
            'Sätt q_+=e vid r_+=(0,0,d/2) och q_−=−e vid r_−=(0,0,−d/2). För punkten r=(0,0,r0) är separationsvektorerna (0,0,r0−d/2) och (0,0,r0+d/2). Sätt in dem och deras belopp i summan.',
            'För punkten r=(0,r0,0) är vektorerna (0,r0,−d/2) och (0,r0,d/2), båda med belopp √(r0²+d²/4). Sätt in de signerade laddningarna och summera komponenterna innan du tar fältets belopp.',
            'Beräkna beloppen i de två punkterna. Eftersom d/r0≪1 kan du även utveckla de exakta uttrycken och behålla första termen som inte försvinner. Omvandla d=0,218 Å och r0=10 Å till meter före numerisk insättning.',
        ),
        self_checks=(
            'Med dipolmoment p=ed i positiv z-riktning ska fjärrfältet på positiva z-axeln peka längs p och på y-axeln motsatt p.',
            'Båda beloppen ska avta som 1/r0³. Axelfältet blir ungefär dubbelt så stort som ekvatorialfältet; detta är en fjärrfältsrelation, inte en exakt relation nära laddningarna.',
        ),
        common_pitfall='Att addera de två fältbeloppen på z-axeln trots att bidragen är motriktade, eller anta att nettoladdning noll innebär fält noll.',
        geometry_hint='Rita två separata observationspunkter: (0,0,r0) och (0,r0,0). Avståndet r0 mäts från molekylens mittpunkt, inte från någon av jonerna.',
        setup_hint='Sätt k=1/(4πε₀). På z-axeln ger insättning E_z=ke[(r0−d/2)⁻²−(r0+d/2)⁻²]. På y-axeln används samma vektorsumma med de två lika avstånden; laddningarnas tecken gör att y-bidragen försvinner och z-bidragen adderas.',
    ),
    "PorcelainSlabCapacitor": G(
        problem_id="3.3",
        learning_goal="Använd randvillkor för D och spänningssumman över två seriekopplade materialskikt.",
        concepts=("D-fält", "dielektrikum", "seriekopplade skikt"),
        start_here='Skriv Gauss lag ∮_S D·n dS=Q_fri,in, materiallagen D=εE och potentialskillnaden ΔV=−∫E·dl. Identifiera materialens permittiviteter, skikttjocklekarna och eventuell fri laddning på gränsen.',
        hint_titles=('Randvillkoret mellan skikten', 'Material och tjocklekar', 'Summera spänningsfallen'),
        hints=(
            'Försumma kanteffekter: fälten är normala mot plattorna. En tunn Gaussbox över luft–porslin-gränsen ger (D_porslin,n−D_luft,n)S=0 eftersom ingen fri gränsladdning finns. Sätt det gemensamma fältbeloppet till D.',
            'Identifiera ε_luft=ε₀, ε_porslin=6ε₀ och d_luft=d_porslin=0,005 m. Materiallagen ger E_luft=D/ε₀ och E_porslin=D/(6ε₀).',
            'Sätt in fälten i spänningsintegralen: 10⁴ V=E_luft d_luft+E_porslin d_porslin. Lös efter D och beräkna därefter båda E-beloppen.',
        ),
        self_checks=(
            'E_luft/E_porslin ska vara 6, medan D är samma i båda skikten. D har enheten C/m² och E har enheten V/m.',
            'Spänningsfallen ska summera till 10 kV. Om εr sätts till 1 ska modellen ge det homogena fältet U/d.',
        ),
        common_pitfall='Att fördela spänningen lika bara för att skikten är lika tjocka, eller kräva kontinuitet för E_n när det är D_n som är kontinuerligt.',
        geometry_hint='Materialgränsen är parallell med metallplattorna. En väg från den ena plattan till den andra passerar båda materialen; potentialfallen adderas som för seriekopplade skikt.',
        setup_hint='Gaussboxen ger ett gemensamt D. Sätt E_i=D/ε_i i U=Σ_i E_i d_i, så att D=U/[d_luft/ε₀+d_porslin/(ε₀εr)]. Använd sedan materiallagen för respektive skikt.',
    ),
    "GroundedInnerSphereChargeSplit": G(
        problem_id="3.6",
        learning_goal="Kombinera Gauss lag, laddningskonservering och ett jordningsvillkor för en flerledargeometri.",
        concepts=("jordad ledare", "sfärisk symmetri", "dielektrikum"),
        start_here='Skriv ∮_S D·n dS=Q_fri,in och V(a)=∫_a^∞ E_r dr=0 för den jordade kulan. Inför laddningarna q på kulan samt q_in och q_ut på skalets sidor. Identifiera innesluten fri laddning och permittivitet i varje radialområde.',
        hint_titles=('Vilka laddningar är bevarade?', 'Fälten innanför och utanför skalet', 'Använd jordningsvillkoret'),
        hints=(
            'Sfärisk symmetri ger ett radiellt fält. En Gaussyta inne i skalets metall, där E=0, ger q+q_in=0. Det isolerade skalets laddning är bevarad: q_in+q_ut=Q. Den jordade kulans q är däremot okänd.',
            'I gapet ger 4πr²D_r=q och D=ε₀εrE. Utanför skalet ger 4πr²D_r=q+Q=q_ut och D=ε₀E. Lös efter E_r separat i båda områdena.',
            'Sätt in fälten i jordningsvillkoret 0=∫_a^(3a) E_gap dr+∫_(3a)^∞ E_ut dr. Ersätt q med −q_in, lös efter q_ut/q_in och sätt sist εr=2,5.',
        ),
        self_checks=(
            'Laddningarna på skalets båda sidor ska summera till Q, och den beräknade potentialen på den inre kulan ska vara noll.',
            'Kvoten q_ut/q_in ska vara 2/εr för denna geometri, alltså 0,8 vid εr=2,5. För Q>0 är båda skalytorna positivt laddade och den jordade kulan negativ.',
        ),
        common_pitfall='Att bevara laddningen på den jordade kulan, eller använda en enda permittivitet i en potentialintegral som går genom både dielektrikum och vakuum.',
        geometry_hint='Dela den radiella integrationsvägen vid 3a. Jordningen gäller kulan vid a, inte det yttre skalet. Hålet och tråden försummas enligt uppgiftens antagande om sfärisk symmetri.',
        setup_hint='Identifiera Q_fri,in=q i gapet och q_ut utanför. Efter Gauss lag och potentialintegrationen blir 0=q(1/a−1/(3a))/(4πε₀εr)+q_ut/(4πε₀·3a). Kombinera med q=−q_in, inte med bevarad laddning på den jordade kulan.',
    ),
    "ChargedDielectricShell": G(
        problem_id="3.7",
        learning_goal="Lösa E och V styckvis i en sfäriskt symmetrisk geometri med både vakuum och dielektrikum.",
        concepts=("Gauss lag för D", "styckvis medium", "potentialkontinuitet"),
        start_here='Skriv ∮_S D·n dS=Q_fri,in, D=εE och V(r)=∫_r^∞ E_r(s) ds. Identifiera sfärisk symmetri, innesluten laddning och permittivitet för r<a, a<r<b och r>b. Här behandlas ρ0 som fri rymdladdningstäthet, i enlighet med facit.',
        hint_titles=('Innesluten fri laddning', 'Från D till E i varje område', 'Integrera inåt från oändligheten'),
        hints=(
            'Tolka ρ0 som fri laddningstäthet enligt facit. Välj en sfärisk Gaussyta. D är radiellt och konstant på ytan, så flödet är 4πr²D_r. Beräkna Q_fri,in=∫ρ0 dV: den är 0 i hålrummet, 4πρ0(r³−a³)/3 i materialet och 4πρ0(b³−a³)/3 utanför.',
            'Lös 4πr²D_r=Q_fri,in för varje område. Sätt sedan E_r=D_r/(ε₀εr) i materialet och E_r=D_r/ε₀ i vakuum.',
            'Integrera fältet med V(∞)=0. Bestäm först V(b) från det yttre fältet och använd sedan V(r)=V(b)+∫_r^b E_material(s) ds. I hålrummet är E=0, så V är konstant och lika med V(a).',
        ),
        self_checks=(
            'V ska vara kontinuerlig vid a och b och uppfylla −dV/dr=E_r inom varje område. E=0 i hålrummet betyder inte att V där är noll.',
            'Vid b ska ε0εr E_r(b⁻)=ε0E_r(b⁺). Utanför är fältet oberoende av εr när den fria laddningen hålls fast; för εr=1 försvinner permittivitetssprånget.',
        ),
        common_pitfall='Att tolka ρ0 som total laddningstäthet samtidigt som Gauss lag för D används, eller sätta potentialens integrationskonstant separat till noll i varje område.',
        geometry_hint='Rita en sfärisk Gaussyta i varje region. I skalet omsluts bara material mellan a och observationsradien r; vakuumhålet bidrar inte med laddning.',
        setup_hint='Gör en tabell med område, Q_fri,in och ε. Sätt in varje rad i E_r=Q_fri,in/(4π ε r²), där ε är områdets absoluta permittivitet. Dela potentialintegralen vid materialgränserna och behåll samma referens V(∞)=0.',
    ),
    "DielectricFilledSphericalGap": G(
        problem_id="3.9",
        learning_goal="Använd ett gränsvillkor geometriskt: E är tangentiellt mot gränsytan mellan de två dielektrika.",
        concepts=("randvillkor", "E och D", "sfärisk Gaussyta"),
        start_here='Skriv Gauss lag ∮_S D·n dS=Q_fri,in, D_i=ε₀ε_iE_i och randvillkoret E_1t=E_2t. Identifiera hur en sfärisk Gaussyta delas mellan materialen. Uppgiften tillåter att E antas radiellt.',
        hint_titles=('Fältet vid skiljeplanet', 'Flödet genom två halvklot', 'Bestäm fälten i materialen'),
        hints=(
            'Materialen fyller var sitt halvklot, inte två radiella lager. Det radiella E-fältet är tangentiellt mot skiljeplanet, så E_1r=E_2r=E_r vid samma radie. D-beloppen kan däremot vara olika.',
            'En sfärisk Gaussyta i a<r<b omsluter den fria laddningen +Q. Vardera materialet täcker arean 2πr², och D är normalt mot Gaussytan. Flödet blir 2πr²D_1r+2πr²D_2r.',
            'Sätt in D_1r=ε₀ε1E_r och D_2r=ε₀ε2E_r i flödesekvationen och sätt summan lika med Q. Lös efter E_r och beräkna sedan D i respektive halva.',
        ),
        self_checks=(
            'När ε1=ε2 ska resultatet bli det vanliga fältet i en homogent fylld sfärisk kondensator. D1_r/D2_r ska vara ε1/ε2.',
            'Det totala D-flödet genom sfären ska vara Q. Utanför det yttre skalet är fältet noll i denna idealmodell eftersom ledarnas totala laddning är +Q−Q=0.',
        ),
        common_pitfall='Att behandla halvorna som två radiella serielager eller sätta D1_r=D2_r. Radialriktningen är tangent till materialgränsen men normal till Gaussytan.',
        geometry_hint='Rita skiljeplanet genom centrum och en radiell pil längs planet. Jämför med en sfärisk Gaussyta: samma pil har olika relation till normalerna på de två olika ytorna.',
        setup_hint='Använd först E_1t=E_2t vid skiljeplanet. Gauss lag ger därefter Q=2πr²ε₀(ε1+ε2)E_r. Arean är 2πr² per material; det gemensamma E_r får tas ut ur respektive flödesintegral.',
    ),
    "MakrofolCapacitorDesign": G(
        problem_id="3.11",
        learning_goal="Dimensionera först mot genomslag och därefter mot önskad kapacitans.",
        concepts=("genomslag", "plattkondensator", "dimensionering"),
        start_here='Skriv C=Q/U, Gauss lag ∮_S D·n dS=Q_fri,in, D=ε₀εrE och ΔV=−∫E·dl. Identifiera total isoleringstjocklek nt och villkoret |E|≤E_genomslag. Först bestäms antalet skikt, sedan arean.',
        hint_titles=('Fältet genom flera skikt', 'Välj ett helt antal skikt', 'Bestäm plattarean'),
        hints=(
            'I plattmodellen utan kanteffekter är E homogent och normalt mot plattorna. Spänningsintegralen ger U=E nt. Kräv U/(nt)≤E_genomslag för n skikt med tjocklek t.',
            'Lös n≥U/(E_genomslag t) och avrunda uppåt till heltal. Sätt U=50 kV, t=0,10 mm och E_genomslag=200 kV/mm i förenliga enheter.',
            'En Gaussbox vid en elektrod ger D A=Q och materiallagen ger D=ε₀εrE. Kombinera med U=E nt och C=Q/U: C=ε₀εrA/(nt). Lös A för det valda heltalet n och C=100 pF.',
        ),
        self_checks=(
            'Kontrollera att n skikt klarar 50 kV men n−1 inte gör det. Ett avrundat antal får aldrig ge högre fält än genomslagsgränsen.',
            'A ska ha enheten m² och öka med total tjocklek vid given C. Uppgiften söker idealmodellens minimum, utan extra säkerhetsmarginal.',
        ),
        common_pitfall='Att använda den oavrundade minimitjockleken i areaberäkningen, eller förväxla kV/mm med V/m: 1 kV/mm=10⁶ V/m.',
        geometry_hint='Skikten staplas i fältriktningen mellan samma två elektroder; deras tjocklekar adderas. Hela gapet antas fyllt, så inga luftskikt ska läggas in i modellen.',
        setup_hint='Sätt först in tjockleken nt i U=∫E dl=E nt och tillämpa genomslagsvillkoret. När n är valt, använd Q=ε₀εrE A i C=Q/U för att få A=C nt/(ε₀εr).',
    ),
    "CoaxialTwoDielectricCapacitance": G(
        problem_id="3.12",
        learning_goal="Bygga kapacitansen för två koaxiella dielektriska skikt genom att summera potentialfall.",
        concepts=("koaxial kondensator", "D-fält", "seriekopplade dielektrika"),
        start_here='Skriv ∮_S D·n dS=Q_fri,in, D_i=ε₀ε_iE_i, U=∫_a^c E_R dR och C/L=λ/U. Identifiera cylindersymmetrin, laddningen per längd λ och materialgränsen mellan de två lika tjocka isolationslagren.',
        hint_titles=('Gaussytan och materialgränsen', 'Två potentialintegraler', 'Kapacitans per längd'),
        hints=(
            'Lika radiell tjocklek ger b=(a+c)/2. Välj en koaxial Gauss-cylinder med radie R och längd L. D är radiellt, ändytornas flöde är noll och Q_fri,in=λL, så D_R·2πRL=λL.',
            'Lös efter D_R och använd E_i=D_R/(ε₀ε_i). Sätt upp spänningsintegralen som ∫_a^b E_1R dR+∫_b^c E_2R dR; varje del ger en logaritm av en radiekvot.',
            'Bilda C/L=λ/U med den beräknade spänningen. λ ska förkortas bort. Sätt in a=0,020 m, c=0,050 m, ε1=4 och ε2=3 först när uttrycket är klart.',
        ),
        self_checks=(
            'Om ε1=ε2=εr ska logaritmerna summeras till ln(c/a), vilket ger den vanliga koaxialkapacitansen per längd.',
            'Svaret ska ha enheten F/m. Vid b är D_n kontinuerligt men E_R(b⁺)/E_R(b⁻)=ε1/ε2; lika tjocka lager behöver inte ha lika spänningsfall.',
        ),
        common_pitfall='Att förväxla kapacitans C med kapacitans per längdenhet C/L, eller använda det geometriska medelvärdet √(ac) för två lika tjocka lager.',
        geometry_hint='R mäts från cylinderaxeln. Material 1 fyller a<R<b och material 2 fyller b<R<c. Fältet passerar materialen i följd och är normalt mot deras cylindriska gränsyta.',
        setup_hint='Gauss lag ger D_R=λ/(2πR). Insättning i de två potentialintegralerna ger U=λ[ln(b/a)/ε1+ln(c/b)/ε2]/(2πε₀). Använd sedan definitionen C/L=λ/U.',
    ),
    "BreakdownVoltageCases": G(
        problem_id="3.13",
        learning_goal="Skilja mellan homogen isolering och två material i serie när genomslagsfält begränsar spänningen.",
        concepts=("genomslagsfält", "D-kontinuitet", "serielager"),
        start_here='Skriv ΔV=−∫E·dl, D=εE och Gauss lag ∮_S D·n dS=Q_fri,in. Identifiera material och tjocklek i varje fall. Bestäm fälten i lagren innan du tillämpar respektive villkor |E_i|≤E_i,max.',
        hint_titles=('Ett homogent material', 'Två lokala genomslagsvillkor', 'Summera tillåten spänning'),
        hints=(
            'Utan kanteffekter är fältet homogent i ett enda material. För (a) och (b) ger spänningsintegralen U=Ed med d=10 mm. Sätt E lika med genomslagsgränsen för det material som fyller hela gapet.',
            'I (c) ger en Gaussbox över den oladdade materialgränsen samma D_n i båda lagren. Därför är E_luft=D/ε₀ och E_plexi=D/(ε₀εr). Kräv både D≤ε₀E_luft,max och D≤ε₀εrE_plexi,max.',
            'Välj den mindre tillåtna D-nivån, beräkna båda E-beloppen och sätt in dem i Umax=E_luft·1 mm+E_plexi·9 mm. Båda fältgränserna måste vara uppfyllda samtidigt.',
        ),
        self_checks=(
            'Vid den valda spänningen måste båda fältgränserna vara uppfyllda och minst en vara nådd. Med uppgiftens värden begränsar luftgapet.',
            'Om ett material saknas helt används det kvarvarande materialets gräns. Ett mycket tunt men kvarvarande luftgap kan fortfarande begränsa fältet; gränsen när tjockleken går mot noll behöver inte vara värdet när luften helt tagits bort.',
        ),
        common_pitfall='Att addera båda materialens maximala spänningsfall utan att först kontrollera att fälten kan uppfylla D-kontinuitet samtidigt.',
        geometry_hint='Luft och plexiglas ligger efter varandra i fältriktningen. I del (c) återstår bara 1 mm luft, men fältet där är tre gånger fältet i plexiglaset.',
        setup_hint='I ett material används Umax=Emax d. I två lager bestäms först gemensamt Dmax=min(ε₀E_luft,max, ε₀εrE_plexi,max). Sätt sedan E_i=Dmax/ε_i i U=Σ_i E_i d_i; addera inte två oberoende maxspänningar.',
    ),
    "DielectricSlabCapacitor": G(
        problem_id="3.14",
        learning_goal="Knyta ihop D-kontinuitet, spänningsfall, fri ytladdning och polarisationsladdning.",
        concepts=("D-fält", "polarisation", "randvillkor"),
        start_here='Skriv ∮_S D·n dS=Q_fri,in, D=εE och ΔV=−∫E·dl. För bundna laddningar behövs dessutom P=ε₀(εr−1)E och σ_b=P·n. Identifiera skikten och deras normaler; välj z uppåt från jord till plattan med V0>0.',
        hint_titles=('Fälten i skikten', 'Fri laddning på metallen', 'Bunden laddning på dielektrikumet'),
        hints=(
            'I den plana modellen ger en Gaussbox utan fri gränsladdning samma D_n i luft och dielektrikum. Fälten pekar nedåt. För beloppen gäller E_luft=D/ε₀ och E_diel=D/(ε₀εr). Sätt in tjocklekarna i V0=E_luft·0,2d+E_diel·0,8d och lös D.',
            'En Gaussbox från metallens inre till gapet ger σ_f=D·n, där n pekar från metallen ut i gapet. Använd det beräknade D-fältet: den övre plattans fria laddning är positiv och den undres negativ.',
            'Beräkna P som vektor i dielektrikumet och använd σ_b=P·n med normalen ut ur just dielektrikumet. Dess övre normal är +ẑ och den undre −ẑ. Använd inte metallens normal i detta steg.',
        ),
        self_checks=(
            'För εr=1 ska E=V0/d i hela gapet och den bundna laddningen försvinna. D är kontinuerligt genom materialgränsen även när E har ett språng.',
            'För εr>1 blir den bundna laddningen negativ på dielektrikumets övre yta och positiv på dess undre; de summerar till noll. De fria elektrodladdningarna har motsatta tecken.',
        ),
        common_pitfall='Att använda metallens normal när du räknar dielektrikumets bundna laddning, eller blanda ihop fältbelopp med den negativa z-komponenten.',
        geometry_hint='Dielektrikumet fyller 0<z<0,8d. Dess övre normal är +ẑ och dess undre −ẑ. På den övre metallplattans undersida är normalriktningen i stället −ẑ.',
        setup_hint='Lös D ur V0=Dd[0,2/ε₀+0,8/(ε₀εr)]. Sätt E_z=−E och P_z=−ε₀(εr−1)E_diel. Beräkna sedan σ_f=D·n på metallen och σ_b=P·n på dielektrikumet med respektive utåtnormal.',
    ),
    "ElectretCylinderAxis": G(
        problem_id="3.18",
        learning_goal="Ersätta en homogen polarisation med dess bundna laddningar och sedan använda superposition.",
        concepts=("elektret", "bunden laddning", "fält från skiva"),
        start_here='Skriv ρ_b=−∇·P och σ_b=P·n för att bestämma källaddningarna. Använd sedan E(r)=(1/4πε₀)∫[(r−r′)/|r−r′|³] dQ′ och D=ε₀E+P. Identifiera dQ′ och separationsvektorn från den givna polarisationen P=Pẑ.',
        hint_titles=('Vilka ytor bär laddning?', 'Parametrisera varje skiva', 'Addera de axiella fälten', 'Jämför elektret och fria laddningar'),
        hints=(
            'Konstant P ger ρ_b=0. Mantelns normal är vinkelrät mot P, så σ_b=0 där. Botten vid z=0 har normal −ẑ och σ_b=−P; toppen vid z=h har normal +ẑ och σ_b=+P.',
            'För vardera skivan vid z0=0 eller h: välj r=(0,0,z), r′=(R cosφ,R sinφ,z0), dQ′=σ_b R dR dφ. Då är r−r′=(−R cosφ,−R sinφ,z−z0) och |r−r′|=√(R²+(z−z0)²). Integrera över 0≤R≤a och 0≤φ≤2π och addera skivbidragen.',
            'Vinkelintegrationen tar bort tvärkomponenterna. Radialintegralen ger E_skiva,z=σ_b[sgn(z−z0)−(z−z0)/√((z−z0)²+a²)]/(2ε₀), utanför skivytan. Summera med rätt σ_b och z0; skriv resultatet i områdena z<0, 0<z<h och z>h.',
            'Använd D=ε₀E+Pẑ inne i elektreten och D=ε₀E utanför. Ta därefter den plana gränsen a≫h nära ändytornas centrala delar. I del (d) är ±P fria skivladdningar, inte materialpolarisation, så där används D=ε₀E överallt.',
        ),
        self_checks=(
            'E_z ska ha rätt språng σ_b/ε0 över varje ändyta, medan D_z är kontinuerligt eftersom det inte finns fri ytladdning. Använd ensidiga gränsvärden på ytorna.',
            'I den plana gränsen är E≈−Pẑ/ε0 inne och ungefär noll utanför, medan D≈0 för elektreten. Fria skivladdningar ger samma E men D=ε0E, alltså D≈−Pẑ mellan skivorna.',
        ),
        common_pitfall='Att anta D=0 överallt för en ändlig elektret bara för att fri laddning saknas. ∇·D=0 innebär inte att D är noll; den plana approximationen gäller inte godtyckligt långt från en ändlig cylinder.',
        geometry_hint='Rita utåtnormal −ẑ på botten och +ẑ på toppen. Vid z=0 och h är E diskontinuerligt, så ange vilken sida du menar. Villkoret a≫h gör centralområdet ungefär plant, men långt bort måste den ändliga kroppens fält avta.',
        setup_hint='Beräkna först σ_b=P·n. Sätt sedan E_z(z)=Σ_{z0=0,h} σ_b(z0)/(2ε₀) ∫₀ᵃ R(z−z0)/[R²+(z−z0)²]^(3/2) dR. Summera integralerna innan du använder D=ε₀E+P i rätt område. Vid ändytorna används ensidiga gränsvärden.',
    ),
    "ObliqueConductorDielectricBoundary": G(
        problem_id="3.19",
        learning_goal="Bestäm fältets riktning från ledarrandvillkoret och geometrin hos ett snett plan.",
        concepts=("ledarrandvillkor", "ytladdning", "normalvektor"),
        start_here='Skriv randvillkoren n·(D_2−D_1)=ρs och E_2t=E_1t tillsammans med D_2=ε₀εrE_2. I ledaren är E_1=0; en Gaussbox ger då D_2·n=ρs. Identifiera enhetsnormalen från ledaren mot dielektrikumet innan du sätter in uppgiftens geometri.',
        hint_titles=('Bestäm enhetsnormalen', 'Fältets tillåtna komponenter', 'Sätt in den signerade ytladdningen'),
        hints=(
            'Planet beskrivs av f(x,y)=x/a+y/b−1=0. Ledaren innehåller origo, alltså sidan f<0. Normalen mot medium 2 är n=∇f/|∇f|=(b,a,0)/√(a²+b²), eftersom a,b>0.',
            'Tangentialvillkoret ger E_2t=0. I det isotropa dielektrikumet är D_2 parallellt med E_2, så skriv D_2=D_n n. Gaussboxen ger D_n=ρs.',
            'Sätt in normalen i D_2=ρs n och använd sedan E_2=D_2/(ε₀εr). Behåll tecknet på den fria ytladdningen; negativ ρs vänder båda vektorerna.',
        ),
        self_checks=(
            'Enhetsnormalen ska ha längd 1 och vara vinkelrät mot tangenten (a,−b,0). Ingen z-komponent ska finnas.',
            'För a=b ska normalens x- och y-komponenter vara lika. D har belopp |ρs|; vid given fri ytladdning minskar E med ökande εr.',
        ),
        common_pitfall='Att använda skärningsvektorn (a,b,0) som normal, glömma normaliseringen eller anta att den fria ytladdningen är noll eftersom dielektrikumets volymladdning är noll.',
        geometry_hint='Punkterna (a,0) och (0,b) ligger på linjen i xy-snittet; linjen är parallell med vektorn (a,−b). Ledaren innehåller origo, vilket avgör vilken av de två normalriktningarna som ska väljas.',
        setup_hint='Identifiera först normalen n=(b,a,0)/√(a²+b²). Sätt D_2=D_n n i D_2·n=ρs och använd n·n=1. Materiallagen ger sedan E_2; ρs är fri ytladdning även om fri volymladdning saknas.',
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
        start_here='Skriv kraftbalansen ΣF=0 och det elektrostatiska trycket p=ε₀E²/2 vid en metallyta i luft. Identifiera arean i F=pA och bestäm gapfältet från ΔV=−∫E·dl, utan kanteffekter. Betrakta den givna kraften som beloppet av den yttre kraft som balanserar plattornas attraktion. Använd fältet i luftgapet för att bestämma det elektriska trycket.',
        hint_titles=('Fältet från spänningen', 'Från tryck till kraft', 'Lös efter avståndet'),
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
            'Utgå från ΣF=0, elektriskt tryck p=ε₀E_luft²/2 och randvillkoret D_luft,n=D_diel,n utan fri gränsladdning. Identifiera tyngden per area och vilket fält som verkar på metallen. Skriv kraftbalansen per area för kopparblecket: elektriskt tryck uppåt ska balansera tyngden ρ_Cu t g nedåt. Då förkortas den okända plattarean bort.'
        ),
        hint_titles=('Trycket på blecket', 'Koppla samman fälten', 'Använd kraftbalansen'),
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
        start_here='Skriv ∮E·n dS=Q_in/ε₀ och W_e=∫ ε₀E²/2 dV. Identifiera laddningsytans area, gapets volym och det givna genomslagsfältet i plattmodellen. Följ uppgiftens modell med negativ molnbas och positiv mark som två stora plattor. Låt Q beteckna laddningsbeloppet, så att molnets signerade laddning är −Q.',
        hint_titles=('Laddningen från gapfältet', 'Omvandla de givna enheterna', 'Från energitäthet till energi'),
        hints=(
            'I plattmodellen är E normalt mot ytorna och homogent i gapet. En Gaussbox från markens ledande inre till gapet ger EA=Q/ε₀. Lös efter laddningsbeloppet Q med E=Emax.',
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
            'Skriv energibalansen dW_källa=dW_fält+F_x dx, med dW_källa=V0 dQ, W_fält=CV0²/2 och Q=CV0. Identifiera vilken geometrisk storhet som ändrar C och vad spänningskällan håller konstant. Låt x öka när hålcylindern dras in längs metallrörens axel. Spänningskällan är ansluten och håller V0 konstant; både kondensatorns laddning och dess fältenergi kan därför ändras.'
        ),
        hint_titles=('Dela upp den aktiva längden', 'Kapacitansens ändring', 'Källans arbete och kraften'),
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
            'Skriv V(r)=Σ_i q_i/(4πε₀|r−r_i|), E=−∇V och σ=ε₀E_n omedelbart utanför ledaren. Identifiera en hjälpladdning som gör V=0 på planet; därefter kan ytladningen integreras och kraften beräknas. Välj planet z=0 och den verkliga laddningen q vid z=a. Använd den idealisering med ett oändligt plan på noll potential som ligger bakom appens modell och facit; spegelladdningen är ett hjälpmedel utanför det fysiska området.'
        ),
        hint_titles=('Placera spegelladdningen', 'Bestäm integrationsradien', 'Integrera laddningen och bestäm kraften'),
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
        start_here='Skriv I=∫J·n dS, J=σE och ΔV=−∫E·dl. Identifiera strömmens riktning, tvärsnittsarean vid varje radie och integrationsgränserna. Välj U=V(a)−V(b) och positiv ström radiellt utåt. I stationärt tillstånd passerar samma ström varje cylindrisk yta mellan elektroderna; ändeffekter försummas.',
        hint_titles=('Arean som strömmen passerar', 'Integrera det radiella fältet', 'Lös efter strömmen'),
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
        start_here='Skriv dR_el=ρ dℓ/S, I=V/R_el och P=VI. Identifiera strömvägens längdelement och den area som strömmen passerar vid varje radie. Läckströmmen går genom isolationen från innerledare till skärm, alltså radiellt. Modellera varje tunt radiellt skikt som en resistans i serie med nästa.',
        hint_titles=('Ett tunt resistivt skikt', 'Gränser från diametrarna', 'Läckström och effekt'),
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
        start_here='Skriv ∇·J=0, J=σ(R)E, ΔV=−∫E·dl och ρ_fri=∇·D med D=ε₀εrE. Identifiera den givna konduktiviteten och geometrin innan du bestämmer E och laddningstätheten. Börja med stationär strömkonservering. Välj U=V(a)−V(b) och positiv ström utåt, så att tecknet på den fria laddningstätheten kan följas genom beräkningen.',
        hint_titles=('Hur varierar J och E med radien?', 'Bestäm resistansen', 'Beräkna divergensen'),
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
        start_here='Skriv dG=σ dS/ℓ_bana och R_el=1/G. Identifiera längden och tvärsnittet för en strömbana och avgör vilka banor som har samma potentialskillnad. Betrakta en tunn halvcirkelformad strömbana mellan radierna R och R+dR. Alla sådana banor går mellan samma kontaktytor A och B och ligger elektriskt parallellt.',
        hint_titles=('Längd och tvärsnitt för en bana', 'Summera konduktanser', 'Kontrollera med strömflödet'),
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
        start_here='Skriv J_1n=J_2n, E_1t=E_2t, J_i=σ_iE_i och ρ_s=n·(D_2−D_1). Identifiera normalen, de givna strömkomponenterna och materialkonstanterna. Välj normalen n=+x̂ från medium 1 (x<0) till medium 2 (x>0). Dela J1=αx̂+βŷ i normal och tangentiell del innan du använder randvillkoren.',
        hint_titles=('Normal strömkomponent', 'Tangentiell fältkomponent', 'Ytladdningen från D'),
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
        start_here='Skriv Biot–Savarts lag B(r)=μ₀I/(4π)∫ dℓ′×(r−r′)/|r−r′|³. Identifiera dℓ′, separationsvektorn, dess belopp och gränserna. För potentialvägen används A(r)=μ₀I/(4π)∫dℓ′/|r−r′| och B=∇×A. Beräkna bidraget från det raka segmentet −L<z′<L, med ström i +z-riktningen. Uppgiften anger att segmentet är en del av en sluten krets; returledningens bidrag ingår inte här.',
        hint_titles=('Linjeelement och korsprodukt', 'Vägen via vektorpotentialen', 'Gränsen för lång ledare'),
        hints=(
            'Sätt dℓ′=dz′ẑ och s=R R̂+(z−z′)ẑ. Korsprodukten dℓ′×s=R dz′φ̂ bestämmer riktningen och lämnar en skalär integral över z′.',
            'För vektorpotentialen: A_z=μ0I/(4π)∫_{−L}^L dz′/√(R²+(z−z′)²). Segmentbidraget har bara z-komponent, så B_φ=−∂A_z/∂R. I del (b) får du sätta z=0 innan denna radialderivata tas.',
            'Ta L→∞ i segmentresultatet. För den idealiserade oändliga ledaren i del (c) ger Ampères lag B_φ·2πR=μ0I, med strömriktningen bestämd av högerhandsregeln.',
        ),
        self_checks=(
            'Vid z=0 ska de två ändpunktsbidragen vara lika. För L≫R,|z| ska resultatet närma sig μ0I/(2πR); vid I=0 blir fältet noll.',
            'Segmentets B_φ är oberoende av azimutvinkeln även när L är ändlig. Tecknet vänds om I vänds. A_z kan få en divergent additiv konstant när L→∞, trots att B förblir ändligt.',
        ),
        common_pitfall='Att förklara Ampèreproblemet med att ett ändligt segment saknar rotationssymmetri. Segmentbidraget har sådan symmetri, men Ampères magnetostatiska lag gäller den fullständiga stationära strömkretsens fält, inte ett öppet segment isolerat.',
        geometry_hint='R är vinkelrätt avstånd till z-axeln och z är observationspunktens höjd; z′ är källkoordinat. Markera båda ändarna ±L. Hela ledarens längd är 2L.',
        setup_hint='Skriv B_φ=μ0IR/(4π)∫_{−L}^L [R²+(z−z′)²]^(−3/2) dz′. Kontrollera ändpunkterna med u=z′−z. I potentialvägen ska curl ge minus radialderivatan av A_z.',
    ),
    "SquareLoopOnAxis": G(
        problem_id="6.2",
        learning_goal="Summera magnetfält från flera räta ledarsegment och utnyttja symmetri för att eliminera tvärkomponenter.",
        concepts=("superposition", "ändlig rak ledare", "symmetri"),
        start_here='Skriv B(r)=μ₀I/(4π)∮ dℓ′×(r−r′)/|r−r′|³. Identifiera källpunkt och riktat linjeelement för var och en av kvadratens fyra sidor innan komponenterna summeras. Välj först strömriktning uttryckligt. Appens positiva I går moturs sedd från +z och ger B_z>0, i samma teckenkonvention som det lagrade facit. Uppgiftstextens formulering medurs är inte entydigt förenlig med detta; om du menar medurs sedd från +z ska vektorsvaret få motsatt tecken.',
        hint_titles=('Parametrisera en sida', 'Vilka komponenter ska adderas?', 'Sätt fältpunkten i centrum'),
        hints=(
            'Placera hörnen vid (±a/2,±a/2,0). Medurs sedd från +z är uppgiftens riktning; det tryckta facit använder motsatt tecken. För att jämföra med facit väljer vi här moturs. För nederkanten: r′=(x′,−a/2,0), dℓ′=dx′ x̂, −a/2≤x′≤a/2. Med r=(0,0,z) blir r−r′=(−x′,a/2,z) och |r−r′|=√(x′²+a²/4+z²).',
            'Integrera en sidas Biot–Savartbidrag och ta dess z-komponent. Vid summering över fyra sidor tar tvärkomponenterna ut varandra, men z-komponenterna adderas.',
            'Använd det allmänna uttrycket längs axeln och sätt sedan z=0 i del (b). Där ska a=3,0 m och I=10 A användas, oavsett vilka utforskningsparametrar som valts i appen.',
        ),
        self_checks=(
            'B_z ska vara jämn i z: på båda sidor om slingan pekar axelfältet åt samma håll för en given strömriktning. Om strömmen vänds byter B_z tecken.',
            'Långt bort ska B_z närma sig μ0m_z/(2π|z|³), där |m_z|=|I|a². Centrumfältets belopp med uppgiftens tal är cirka 3,8 µT.',
        ),
        common_pitfall='Att multiplicera hela fältvektorn från en sida med fyra, eller förväxla sidlängden a med halva sidlängden a/2. Bestäm strömriktningen innan tecknet jämförs med facit.',
        geometry_hint='Se slingan från +z och rita en strömpil på varje sida. Höger tumme ger slingans axelfält. Positivt I i appens modell betyder moturs sedd från +z; ett negativt I vänder pilar och fält.',
        setup_hint='För sidan y=−a/2 med ström i +x blir dB_z=μ0I(a/2) dx′/[4π(x′²+a²/4+z²)^(3/2)]. Integrera x′ från −a/2 till a/2 och multiplicera z-komponenten med fyra.',
    ),
    "RightAngleWireCorner": G(
        problem_id="6.3",
        learning_goal="Superponera fält från två halv-oändliga räta ledare med olika riktningar.",
        concepts=("Biot–Savart", "superposition", "vektorriktning"),
        start_here='Skriv B(r)=μ₀I/(4π)∫ dℓ′×(r−r′)/|r−r′|³ för vardera ledardelen. Identifiera deras separata parametriseringar och integrationsgränser; addera vektorerna efter integrationen. Dela ledaren i två halv-oändliga raka delar. I appens koordinater går positiv ström längs +x från negativa x-axeln till hörnet och sedan vidare längs +y. Punkten är (0,0,h).',
        hint_titles=('Två parametriseringar', 'Korsprodukternas riktningar', 'Summera vektorerna'),
        hints=(
            'För inkommande delen: r′=(x′,0,0), −∞<x′≤0, dℓ′=dx′ x̂ och r−r′=(−x′,0,h). För utgående delen: r′=(0,y′,0), 0≤y′<∞, dℓ′=dy′ ŷ och r−r′=(0,−y′,h).',
            'Korsprodukterna blir −h dx′ ŷ respektive h dy′ x̂. Avstånden är √(x′²+h²) respektive √(y′²+h²). Sätt in dessa i varsin Biot–Savartintegral och integrera över respektive halvlinje.',
            'För h>0 ger vardera integral faktorn 1/h efter att h i täljaren räknats med. Summera vektorerna och beräkna sedan beloppet från komponenternas kvadratsumma. Sätt h=0,050 m och I=5 A sist.',
        ),
        self_checks=(
            'Det numeriska beloppet ska bli ungefär 1,4·10⁻⁵ T. Fältet har ingen z-komponent ovanför hörnet i denna geometri.',
            'Beloppet ska skala som |I|/h. Negativ I vänder vektorn men ger samma positiva belopp; en punkt under planet vänder också båda horisontella komponenterna.',
        ),
        common_pitfall='Att addera de två beloppen direkt eller ange bisektrisen utan att välja dess riktning. Högerhandsregeln måste tillämpas på vart och ett av segmenten.',
        geometry_hint='Rita ett xy-snitt ovanifrån med ett inkommande segment på negativa x-axeln och ett utgående på positiva y-axeln. Observationspunkten ligger på höjden h över hörnet, inte i samma plan som ledaren.',
        setup_hint='Skriv B=μ₀I/(4π)[−ŷ∫_{−∞}^0 h dx′/(x′²+h²)^(3/2)+x̂∫₀^∞ h dy′/(y′²+h²)^(3/2)]. Utför integralerna var för sig; använd sedan |B|=√(B_x²+B_y²).',
    ),
    "ThinCurrentStripField": G(
        problem_id="6.5",
        learning_goal="Ersätta ett brett strömförande band med en kontinuerlig samling parallella linjeströmmar.",
        concepts=("superposition", "ytström", "oändlig rak ledare"),
        start_here='Skriv superpositionen B=∫dB med dB=μ₀ dI φ̂/(2πs) för en oändlig rak deltråd. Identifiera delströmmen dI, avståndet s och riktningen φ̂ för varje källäge; komponenterna måste uttryckas i samma bas. Välj ström i +z och bandbredd längs x från −a till a. Betrakta tvärsnittet i xy-planet; uppgiftens två punkter kan då väljas som (2a,0) och (0,2a).',
        hint_titles=('Strömmen i en smal remsa', 'Punkten bredvid bandet', 'Punkten ovanför bandet'),
        hints=(
            'En remsa med bredd dx′ bär dI=I dx′/(2a). Fältet från varje lång tråd har belopp μ0 dI/(2πs), men riktningen beror på observationspunkten.',
            'I punkten (2a,0) pekar alla bidrag i +y för I>0. Integrera 1/(2a−x′) från −a till a; detta ger en logaritm.',
            'I punkten (0,2a) tar y-komponenterna ut varandra för x′ och −x′. X-komponenterna adderas i −x. Projektionen ger en integral med nämnaren x′²+(2a)² och därmed en arctan.',
        ),
        self_checks=(
            'Vid fast observationsavstånd mycket större än a ska bandet likna en linjeström med total ström I. Håll avståndet fast när denna gräns tas, inte punkten 2a.',
            'Ovanför mittlinjen ska B_y=0 och B_x<0 för I>0. I bandets plan till höger om kanten är B_y>0; ett byte av strömriktning vänder båda fälten.',
        ),
        common_pitfall='Att summera trådarnas fältbelopp i normalplanet utan att projicera vektorerna. Olika remsors fält pekar åt olika håll och vissa komponenter tar ut varandra.',
        geometry_hint='I tvärsnittet är strömmen ut ur bilden för I>0, markerad med ⊙. Den går längs bandet, inte tvärs över bredden 2a. Punkten i del (a) ligger utanför bandet, inte inne i metallremsan.',
        setup_hint='Använd dB=μ0 dI[−y x̂+(x−x′)ŷ]/[2π((x−x′)²+y²)]. Sätt in respektive observationspunkt och integrera x′ över bandbredden.',
    ),
    "CircularArcOnAxis": G(
        problem_id="6.8",
        learning_goal="Genomföra Biot–Savart-integralen för en cirkelbåge där symmetrin inte räcker för att eliminera alla komponenter.",
        concepts=("cirkelbåge", "Biot–Savart", "vektorintegral"),
        start_here='Skriv Biot–Savarts lag B(r)=μ₀I/(4π)∫ dℓ′×(r−r′)/|r−r′|³. Identifiera bågens parametrisering, det riktade linjeelementet och vinkelgränserna före korsprodukten. Beräkna bara den krökta delens bidrag i del (a). Appens båge ligger i första kvadranten med φ från 0 till π/2 och positiv I i riktning mot ökande φ, vilket ger det lagrade facits komponenter.',
        hint_titles=('Bågens variabla tangent', 'Integrera en kvartsbåge', 'Jämför med ett helt varv'),
        hints=(
            'Skriv r′=(a cosφ,a sinφ,0), dℓ′=a(−sinφ,cosφ,0)dφ och s=(−a cosφ,−a sinφ,z). Alla element har avståndet √(a²+z²) till fältpunkten.',
            'Korsprodukten blir dℓ′×s=(az cosφ,az sinφ,a²)dφ. Integrera komponenterna separat över 0≤φ≤π/2; en kvartsbåge saknar helcirkelns möjlighet att släcka alla tvärkomponenter.',
            'För del (b), integrera samma uttryck över 0≤φ≤2π. Sinus- och cosinustermerna försvinner, medan z-komponenten summeras över hela varvet.',
        ),
        self_checks=(
            'I centrum z=0 är båda tvärkomponenterna exakt noll och kvartsbågens fält är en fjärdedel av helcirkelns centrumfält.',
            'B_x och B_y är udda i z, medan B_z är jämn. För helcirkeln är B_x=B_y=0 över hela axeln. Negativ I vänder alla komponenter.',
        ),
        common_pitfall='Att ta en fjärdedel av helcirkelns hela fältvektor för alla z. Det ger rätt z-komponent men missar kvartsbågens tvärfält. Lägg inte heller till de raka ledarnas bidrag när frågan gäller bågen ensam.',
        geometry_hint='Rita bågen från (a,0) till (0,a) och observationspunkten (0,0,z). Kontrollera hur din kursfigur orienterar bågen: om koordinater eller strömriktning ändras måste även komponenterna ändras.',
        setup_hint='Sätt den gemensamma nämnaren (a²+z²)^(3/2) utanför integralen. Integrera az cosφ, az sinφ och a² var för sig. På så sätt kan tecken och symmetri kontrolleras innan beloppet beräknas.',
    ),
    "RotatingChargedDisk": G(
        problem_id="6.13",
        learning_goal="Omvandla en roterande ytladdning till en kontinuerlig fördelning av cirkulära strömslingor.",
        concepts=("ytladdning", "konvektionsström", "strömslinga"),
        start_here='Skriv Biot–Savarts lag och definitionen dI=dQ/τ för en roterande laddningsring, med τ=2π/|ω| för periodens belopp. Identifiera ringens laddningselement, radie och signerade strömriktning innan ringbidragen integreras. Dela skivan i tunna ringar. Använd signerad ytladdning ρs och låt ω vara positiv för rotation moturs sedd från +z; då följer den konventionella strömmens tecken av produkten ρsω.',
        hint_titles=('Från ringladdning till ringström', 'Summera ringarnas fält', 'Radialintegralens undre gräns'),
        hints=(
            'En ring med radie r och bredd dr har dq=ρs 2πr dr. Den signerade ringströmmen är dI=dq·ω/(2π)=ρsωr dr; för negativ laddning går strömmen motsatt rörelsen.',
            'Varje ring ger dB_z=μ0 dI r²/[2(r²+z²)^(3/2)]. Summera genom att integrera r från 0 till a, utan att ersätta hela skivan med en enda kantström.',
            'Integrera r³/(r²+z²)^(3/2), exempelvis med u=√(r²+z²). Den undre gränsen blir |z|. Det slutliga axelfältet ska därför gälla på båda sidor om skivan.',
        ),
        self_checks=(
            'Vid z=0 ska B_z=μ0ρsωa/2. B_z är jämn i z och byter tecken när antingen laddning eller rotation vänds; noll laddning eller noll rotation ger noll fält.',
            'Långt bort blir m_z=πρsωa⁴/4 och B_z≈μ0m_z/(2π|z|³). Ett isolerat ringelement får inte användas som modell för hela skivans dipolmoment.',
        ),
        common_pitfall='Att lägga till en extra faktor 2π i ringströmmen eller använda z i stället för |z| vid den undre integrationsgränsen. Positiv rotationsriktning och positiv konventionell ström är inte samma sak för negativ laddning.',
        geometry_hint='r är källringens radie och z observationspunktens höjd; a är skivans ytterradie. Alla ringar har samma vinkelhastighet, men hastigheten ωr och ringarnas laddning varierar med r.',
        setup_hint='Skriv B_z=(μ0ρsω/2)∫₀ᵃ r³/(r²+z²)^(3/2) dr. Med u=√(r²+z²) blir integranden 1−z²/u² och en primitiv funktion u+z²/u; hantera centrumgränsen kontinuerligt.',
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
            'Beräkna omloppstiden τ från banans omkrets och farten v. En laddning −e passerar ett valt snitt per varv, så den signerade strömmen relativt moturs riktning är I=−e/τ.',
            'Använd m=I A n̂ med A=πa² och n̂=ẑ för den valda positiva omloppsriktningen. Blanda inte ihop banradien med arean.',
            'Sätt in τ=2πa/v och förenkla. Högerhandsregeln ska tillämpas på konventionell ström: momentet är motsatt elektronens rörelsemängdsmoment.',
        ),
        self_checks=(
            'Enheten e·v·a är C·m²/s=A·m². Om v eller a fördubblas vid fast värde på den andra parametern fördubblas |m|.',
            'En positiv laddning med samma rörelse får motsatt moment. Om elektronens omloppsriktning vänds byter även m riktning.',
        ),
        common_pitfall='Att rita m som en pil i banplanet. Dipolmomentet är vinkelrätt mot planet, och för den valda elektronrörelsen pekar det in i bilden när du ser från +z.',
        setup_hint='Skriv I=q/τ och m_z=Iπa². Behåll q=−e tills den sista förenklingen så att minustecknet inte tappas bort.',
        geometry_hint='Se xy-planet från +z. Rita elektronens rörelse moturs och strömmen medurs. Symbolen ⊗ i centrum betyder m längs −z, in i bilden; det är ingen radiell vektor.',
    ),
    "CircularLoopTorqueUniformField": G(
        problem_id="7.2",
        learning_goal="Se hur det lokala kraftbidraget på en strömslinga summeras till det globala momentet m×B.",
        concepts=("Lorentzkraft på ledare", "kraftmoment", "magnetiskt moment"),
        start_here='Skriv dF=I dℓ×B och T=∮r×dF. Identifiera linjeelement, hävarm och det givna fältet innan korsprodukterna beräknas. Beräkna först kraften på ett litet strömelement och sedan dess moment kring centrum. Håll isär dℓ, kraften dF och hävarmen r; de är tre olika vektorer.',
        hint_titles=('Parametrisera kraften', 'Integrera vridmomentet', 'Kontrollera med dipolmomentet'),
        hints=(
            'Parametrisera r=a(cosφ,sinφ,0) och dℓ=a(−sinφ,cosφ,0)dφ. Med B=B x̂ ger dF=I dℓ×B en kraft i z-led vars tecken beror på cosφ.',
            'Ta dT=r×dF komponentvis. Då fås dT_x=−IBa²sinφ cosφ dφ och dT_y=IBa²cos²φ dφ. Integrera över ett helt varv: x-bidraget tar ut sig.',
            'Kontrollera del (b) med m=Iπa²ẑ och T=m×B. I del (c) ger positivt moment kring y en vridning av m från +z mot +x, alltså mot B.',
        ),
        self_checks=(
            'Nettokraften ∮dF ska vara noll i det homogena fältet trots att nettomomentet inte är noll. Integralen av cos²φ över ett varv är π.',
            'Vid φ=π/2 är dℓ parallell med B och både dF och dT är noll. Vid I=0 eller B=0 försvinner momentet; om endast ett av tecknen vänds byter T riktning.',
        ),
        common_pitfall='Att byta ordning på en korsprodukt eller använda samma riktning för kraft och moment. Här är kraften lokal i ±z medan det sammanlagda momentet ligger i y-led.',
        setup_hint='Gör de två korsprodukterna i ordning: dF=I dℓ×B, sedan dT=r×dF. Integrera varje momentkomponent över 0≤φ≤2π innan du jämför med m×B.',
        geometry_hint='B ligger i slingans plan längs x. På motsatta sidor x=±a är krafterna motsatta i z men bildar ett kraftpar kring y. Positiv I går moturs sedd från +z.',
    ),
    "DipoleDipoleTorque": G(
        problem_id="7.3",
        learning_goal="Beräkna momentet på en magnetisk dipol i det icke-homogena fältet från en annan dipol.",
        concepts=("dipolfält", "magnetiskt moment", "vektorgeometri"),
        start_here='Skriv B₁=μ₀[3(m₁·r̂)r̂−m₁]/(4πr³) och T₂=m₂×B₁. Identifiera dipolmomenten och separationsvektorn innan du tar komponenter. Bestäm fältet från den första dipolen i den andra spolens centrum. Dipolapproximationen förutsätter att spolarna är små jämfört med avståndet r. Välj separationsvektorn i xz-planet.',
        hint_titles=('Fältet vid andra dipolen', 'Vilken komponent ger moment?', 'Skilj belopp från tecken'),
        hints=(
            'Skriv r̂=sinθ x̂+cosθ ẑ och använd B₁=μ0[3(m₁·r̂)r̂−m₁]/(4πr³), där båda momenten är mẑ.',
            'Endast fältets x-komponent bidrar till T₂=m₂×B₁. Z-komponenten är parallell med m₂ och ger inget kraftmoment.',
            'Korsprodukten ger en signerad y-komponent proportionell mot sinθ cosθ. Ta absolutbelopp först när uppgiftens momentbelopp efterfrågas; sätt därefter m=1 A·m², r=1 m och θ=45°.',
        ),
        self_checks=(
            'Momentet försvinner vid θ=0°, 90° och 180°. Beloppet är störst vid 45° och 135°, men riktningen är motsatt i de två fallen.',
            'Vid uppgiftens värden ska beloppet bli 1,5·10⁻⁷ N·m. Fördubbling av r minskar det med en faktor åtta; samtidig vändning av båda dipolerna ändrar inte momentet.',
        ),
        common_pitfall='Att kalla sin(2θ)-uttrycket ett belopp för alla vinklar. Det är den signerade y-komponenten i den valda geometrin; beloppet innehåller |sin(2θ)|.',
        setup_hint='Beräkna B₁x=3μ0m sinθ cosθ/(4πr³) och därefter T₂y=mB₁x. Använd sedan |T₂y| för det efterfrågade beloppet.',
        geometry_hint='Båda dipolerna är parallella med z, medan r̂ lutar mot x. T är vinkelrätt mot xz-planet, längs ±y. θ är vinkeln mellan separationen och z, inte mellan de två dipolmomenten.',
    ),
    "LoopDipoleApproximationError": G(
        problem_id="7.5",
        learning_goal="Kvantifiera när fjärrfältsapproximationen av en strömslinga som magnetisk dipol faktiskt är tillräckligt noggrann.",
        concepts=("dipolapproximation", "relativt fel", "gränsfall"),
        start_here='Skriv relativfelet δ=|B_dip−B_exakt|/|B_exakt| och kravet δ<0,01. Identifiera samma observationspunkt och samma ström och radie i båda fältuttrycken. Jämför exakt axelfält och dipolfält vid samma punkt och för samma slingmoment m=Iπa². Definiera relativfelet med det exakta fältets belopp i nämnaren.',
        hint_titles=('Två fält vid samma punkt', 'Bilda en dimensionslös kvot', 'Lös felvillkoret'),
        hints=(
            'För z≠0 är B_exakt=μ0Ia²/[2(a²+z²)^(3/2)] och B_dip=μ0Ia²/(2|z|³). Formlerna har samma riktning på båda sidor om slingan.',
            'Inför x=|z|/a och bilda kvoten. För I≠0 blir B_dip/B_exakt=(1+x⁻²)^(3/2), så ström och enheter försvinner.',
            'Lös (1+x⁻²)^(3/2)−1<0,01 efter x. Använd det exakta olikhetsvillkoret; serieutvecklingen 3/(2x²) kan användas som rimlighetskontroll.',
        ),
        self_checks=(
            'Gränsen ligger vid ungefär |z|=12,26a. Strikt mindre än 1 % kräver ett avstånd större än denna gräns; det avrundade facitvärdet är ungefärligt.',
            'Felet går mot noll långt bort och är oberoende av strömmens storlek och tecken. Vid I=0 är båda fälten noll och ett uppmätt relativfel 0/0 odefinierat; grafen visar då samma geometriska gränsvärde som för I≠0.',
        ),
        common_pitfall='Att använda det approximativa fältet som nämnare, eller anta att dipolmodellen fungerar nära centrum. Den divergerar vid z=0 medan slingans exakta fält är ändligt.',
        visualization_note="En graf över relativfelet mot z/a kan här faktiskt hjälpa studenten att se var dipolapproximationen blir användbar.",
        setup_hint='Isolera först x⁻²: det ska vara mindre än (1+tol)^(2/3)−1. Invertera därefter olikheten med hänsyn till att alla storheter är positiva.',
        geometry_hint='z mäts från slingans centrum vinkelrätt mot dess plan. Rita gärna ett sidoperspektiv med slingans plan och normalaxel. Den sökta tröskelpunkten ligger på normalaxeln.',
    ),
    "AntarcticIceFlux": G(
        problem_id="7.6",
        learning_goal="Använd ∇·B=0 för att byta en besvärlig flödesyta mot en enklare sfärisk yta.",
        concepts=("magnetiskt flöde", "Gauss lag för B", "jordens dipolfält"),
        start_here=(
            'Skriv Φ=∫_S B·n dS och ∮_sluten B·n dS=0. Identifiera den efterfrågade öppna ytan och en kompletterande yta med känd normal och enklare fält. Slut isvolymen med bottenytan mot jorden. Det efterfrågade flödet genom hela is–luft-gränsen omfattar både ovansida och lodrät rand; använd ∮B·dS=0 för att ersätta dessa med bottenytan.'
        ),
        hint_titles=('Slut ytan', 'Fältet på bottenkalotten', 'Integrera med rätt normal'),
        hints=(
            'Den slutna isvolymens utåtnormal vid botten pekar in mot jorden. Därför är Φ_luft=−Φ_botten. Jordens moment pekar söderut, så fältet vid sydpolen går från jorden in i isen.',
            'Mät polvinkeln θ från sydpolen, alltså från momentets riktning. Vid 70° sydlig bredd blir θ_max=20°. På r=rJ är B_r=μ0m cosθ/(2πrJ³), positivt radiellt utåt.',
            'Integrera B_r rJ²sinθ dθ dφ över bottenkalotten med radialnormal utåt från jorden. Detta är −Φ_botten och därmed det sökta flödet till luften.',
        ),
        self_checks=(
            'Med m=0,824·10²³ A·m² och rJ=637 mil=6,37·10⁶ m blir flödet cirka 9,5·10⁸ Wb. När kalotten krymper till sydpolen går flödet mot noll.',
            'Istjockleken 1000 m faller bort när bottenkalotten är fixerad: ändrad tjocklek omfördelar flödet mellan ovansida och rand men ändrar inte deras summa. Flödet genom hela den slutna isvolymen är fortfarande noll.',
        ),
        common_pitfall='Att beräkna bara flödet genom isens ovansida, glömma randytan eller använda bottennormalen med fel tecken. ∇·B=0 betyder noll nettoflöde genom en sluten yta, inte noll genom kalotten ensam.',
        setup_hint='Skriv Φ_luft=∫₀²π∫₀^{θ_max} [μ0m cosθ/(2πrJ³)] rJ²sinθ dθ dφ. Håll isvolymens inåtriktade bottennormal skild från jordens radiella normal.',
        geometry_hint='θ mäts från sydpolen och är komplementet till sydlig bredd. Höjden h är istjockleken ovanpå jordytan, inte avståndet från latitudcirkeln till polen. Skissen överdriver tjockleken för läsbarhet.',
    ),
    "CopperWireMagneticLevitation": G(
        problem_id="7.7",
        learning_goal="Jämföra magnetisk krafttäthet J×B med tyngdkraft per volym.",
        concepts=("krafttäthet", "J×B", "kraftjämvikt"),
        start_here='Skriv kraftbalansen J×B+ρg=0 per volym. Identifiera strömriktningen, massdensiteten och den fältriktning som ger en uppåtriktad kraft. Arbeta med kraft per volym. Både magnetisk kraft och tyngdkraft är proportionella mot trådens volym, så den okända längden och tvärsnittsarean behövs inte.',
        hint_titles=('Krafternas riktningar', 'Vertikal kraftbalans', 'Enheter före insättning'),
        hints=(
            'Skriv magnetisk krafttäthet f_mag=J×B. Med J=J x̂ och B=B ŷ blir den JB ẑ; tyngdkrafttätheten är −ρg ẑ.',
            'Sätt den vertikala nettokrafttätheten JB−ρg lika med noll. Detta är ett kraftbalansvillkor, inte i sig ett bevis för stabil svävning.',
            'Omvandla J=3,0 A/mm² till 3,0·10⁶ A/m² och ρ=8,9 g/cm³ till 8,9·10³ kg/m³ innan du löser ut och beräknar B.',
        ),
        self_checks=(
            'Med g=9,81 m/s² blir B≈0,0291 T, alltså 29 mT. Vid mindre B är nettokraften nedåt och vid större B uppåt.',
            'Fördubbling av J halverar det erforderliga B. Om bara strömmen eller bara fältet vänds blir den magnetiska kraften nedåt och kan inte balansera tyngden.',
        ),
        common_pitfall='Att blanda kraft per längd med kraft per volym, eller glömma faktorn 10⁶ vid omvandlingen från A/mm². Kraftbalans i ett homogent fält ger ingen återställande kraft vid en höjdförskjutning.',
        setup_hint='Du kan även skriva I=JA för en bit med längd ℓ: F_mag=JAℓB och F_g=ρAℓg. Förkorta Aℓ först och lös därefter balansvillkoret.',
        geometry_hint='Välj x åt höger och z uppåt. Strömmen går längs +x och lyftkraften längs +z. Då måste B peka längs +y enligt x̂×ŷ=ẑ; B och J×B är vinkelräta.',
    ),
    "InfiniteWireRectangularLoopFlux": G(
        problem_id="7.10",
        learning_goal="Beräkna magnetiskt flöde genom en plan yta när B både varierar i belopp och lutar relativt ytans normal.",
        concepts=("magnetiskt flöde", "fält från rak ledare", "projektion"),
        start_here='Skriv Φ=∫_S B·n dS och B=μ₀I φ̂/(2πR) för den oändliga ledaren. Identifiera avståndet till ledaraxeln, fältets riktning och slingans normal innan flödet integreras. Välj slingans normal till +z och beräkna ledarens fält i punkten (x,y,c). Fältet cirkulerar runt x-axeln och är inte vinkelrätt mot hela slingytan.',
        hint_titles=('Ledarfältets riktning', 'Projicera på ytans normal', 'Integrera över rektangeln'),
        hints=(
            'Avståndet till ledaren är R=√(y²+c²). För ström i +x ger högerhandsregeln B=μ0I(−c ŷ+y ẑ)/[2π(y²+c²)].',
            'Ytelementet är dS=ẑ dx dy, så bara B_z bidrar. Vid närmaste kanten y=0 är B_z=0 trots att hela magnetfältet där är ändligt.',
            'B_z är oberoende av x. X-integralen ger a, och y-integralen från 0 till b innehåller y/(y²+c²), vars primitiva funktion är en halv logaritm.',
        ),
        self_checks=(
            'Flödet ska vara proportionellt mot I och a och byta tecken när strömmen eller vald ytnormal vänds. Vid b→0 försvinner flödet.',
            'För c≫b ska Φ≈μ0Ia b²/(4πc²). När c→0 vid fast b divergerar idealmodellens flöde logaritmiskt; en verklig ledares ändliga radie sätter gränser för modellen.',
        ),
        common_pitfall='Att integrera fältbeloppet μ0I/(2πR) utan projektion eller behandla hela slingytan som om den hade samma avstånd till ledaren.',
        setup_hint='Skriv Φ=a μ0I/(2π)∫₀ᵇ y/(y²+c²)dy. Logaritmens slutliga argument måste vara dimensionslöst; använd kvoten av värdena vid de båda gränserna.',
        geometry_hint='Slingan ligger i z=c, med 0≤x≤a och 0≤y≤b. I ett yz-snitt syns ledaren som en punkt vid origo och slingan som en sträcka på höjden c; normalen pekar uppåt längs z.',
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
            'Skriv H_g=B/μ0 i luftgapet och använd materialtabellen för H_m(B). Magnetens H kan vara negativt även när B är positivt.',
            'Utan spolström gäller H_mℓ_m+Bd/μ0=0. Rita lastlinjen H_m=−Bd/(μ0ℓ_m) och sök skärningen med materialkurvan.',
            'Med spole ersätts högerledet av NI. Positiv I i appen förstärker gapfältet. Interpolera mellan tabellpunkter; utanför den givna materialkurvan kan arbetspunkten inte bestämmas utan fler data.',
        ),
        self_checks=(
            'Vid I=0 ska magnetens negativa H-bidrag balansera gapets positiva bidrag. Kontrollera residualen H_mℓ_m+Bd/μ0−NI, inte bara hur nära kurvorna ser ut att ligga.',
            'Ökad förstärkande NI höjer B inom tabellens giltiga intervall. En tabelländpunkt är inte automatiskt en lösning om lastlinjen missar kurvan.',
        ),
        common_pitfall='Att använda en konstant permeabilitet för permanentmagneten eller extrapolera den tabellerade grenen utan stöd. Originalets ℓ är magnetens längd, medan luftgapet d tillkommer.',
        visualization_note="Just här är en B–H-graf med lastlinje pedagogiskt relevant eftersom lösningen bokstavligen är deras skärningspunkt.",
        setup_hint='Originaluppgiften definierar ℓ som permanentmagnetens längd, alltså ℓ_m=ℓ. Använd H_m(B)ℓ+Bd/μ0=NI där d är luftgapet, utan att dra av d från ℓ.',
        geometry_hint='Följ en sluten medellinje genom magnet och luftgap. Samma flöde passerar båda; gapet är en seriedel. Spolens tecken bestäms av om dess magnetomotoriska spänning hjälper eller motverkar magneten.',
    ),
    "NonlinearIronMagneticCircuit": G(
        problem_id="8.2",
        learning_goal="Lösa en magnetisk krets där järnets materiallag är icke-linjär men flödet är gemensamt med luftgapet.",
        concepts=("icke-linjär B–H-lag", "Ampères lag", "luftgap"),
        start_here='Skriv ∮H·dl=NI, flödeskontinuitet och den givna materiallagen B=aH/(b+H). Identifiera järnets och gapets längder samt materiallagens giltiga gren. Använd ett gemensamt B i järn och gap eftersom tvärsnittet är samma och läckage försummas. Invertera den givna materiallagen innan Ampères lag ställs upp.',
        hint_titles=('Invertera materiallagen', 'Summera cirkulationen', 'Pröva den fysikaliska roten'),
        hints=(
            'Från B=aH/(b+H) fås H=bB/(a−B). Materiallagen gäller för H>0, vilket begränsar den fysiska lösningen till 0<B<a.',
            'Skriv H_järnℓ+Bd/μ0=NI med ℓ som järnets medellängd i appen. Tvärsnittet S förkortas bort när samma B gäller i hela kretsen; flödet är däremot Φ=BS.',
            'Lös den monotona ekvationen i intervallet 0<B<a. Om du multiplicerar bort nämnaren och använder en andragradsekvation måste varje rot återinsättas i både materiallagen och balansvillkoret.',
        ),
        self_checks=(
            'Med uppgiftens värden ska B bli cirka 0,22 T och ligga under a=2 T. Den andra algebraiska roten ligger över a och ger H<0, trots att B där är positivt.',
            'Ökad positiv ström höjer B mot mättnadsgränsen a. Vid I→0⁺ går B→0. Appen tillåter noll som gränsfall men extrapolerar inte den givna H>0-lagen till negativ ström.',
        ),
        common_pitfall='Att godta en rot enbart för att B är positivt. Även B<a och H>0 måste gälla. Arean behövs för flödet men påverkar inte B i denna idealisering.',
        setup_hint='Sätt bBℓ/(a−B)+Bd/μ0=NI. I kontrollerna heter materialkonstanterna Bsat och H0 för att skilja dem från geometriska längder. Summan av järnets och gapets ampervarv ska bli NI.',
        geometry_hint='Järn och luftgap ligger i serie och har samma area S. Summera H gånger respektive delsträcka, inte B gånger hela längden med en enda permeabilitet.',
    ),
    "MagneticBridgeCircuit": G(
        problem_id="8.4",
        learning_goal="Översätta en förgrenad järngeometri till ett nätverk av magnetiska reluktanser och hitta flödet i en bestämd gren.",
        concepts=("reluktans", "magnetisk krets", "flödesdelning"),
        start_here='Skriv ∮H·dl=NI, Φ_in=ΣΦ_ut vid en förgrening och ℜ=ℓ/(μS) för varje homogen del. Identifiera delarnas längder, areor och vilka flöden som är gemensamma. Rita vänster ringhalva som en seriedel med spolen. Mellan ringens två förgreningspunkter ligger bryggan och höger ringhalva parallellt.',
        hint_titles=('Beräkna delarnas reluktanser', 'Fördela flödet', 'Lös för bryggan'),
        hints=(
            'Varje ringhalva har längd πD/2 och area S_ring. Bryggan har längd D och area S_brygga. Använd reluktansen ℜ=ℓ/(μ0μrS) för varje del.',
            'Låt U_m vara den magnetiska potentialskillnaden mellan förgreningspunkterna. Då är Φ_b=U_m/ℜ_b och Φ_h=U_m/ℜ_h, medan vänsterflödet är Φ_v=Φ_b+Φ_h.',
            'Spolens NI används både i vänstra ringhalvan och över parallellgrenarna: NI=ℜ_v(Φ_b+Φ_h)+U_m. Lös först U_m och sedan det efterfrågade bryggflödet.',
        ),
        self_checks=(
            'Med uppgiftens värden blir bryggflödet cirka 1,1·10⁻⁸ Wb. Om S_brygga→0 ska bryggflödet gå mot noll.',
            'Vänsterflödet är summan av de två grenflödena. En större grenreluktans ger mindre grenflöde vid samma U_m; vänd strömmen och alla flöden byter tecken.',
        ),
        common_pitfall='Att lägga alla tre delarna i serie eller dela flödet lika utan att jämföra reluktanserna. Samma material innebär inte samma reluktans när längder och areor skiljer sig.',
        visualization_note="Ett reluktansnät bredvid den geometriska skissen är sannolikt mer lärorikt än en 3-D-fältbild för denna uppgift.",
        setup_hint='Skriv ℜ_v=ℜ_h=πD/(2μ0μrS_ring) och ℜ_b=D/(μ0μrS_brygga). Eliminera Φ_b och Φ_h ur NI=ℜ_v(Φ_b+Φ_h)+U_m.',
        geometry_hint='De två ringhalvorna möts vid bryggans ändar. Det finns en gemensam inkommande gren och två returvägar. Spolen sitter på bara den ena ringhalvan.',
    ),
    "CurrentCarryingMagneticTube": G(
        problem_id="8.5",
        learning_goal="Hålla isär H, B och M när ett fritt strömförande material kan vara magnetiskt.",
        concepts=("Ampères lag för H", "magnetisering", "styckvis fält"),
        start_here='Skriv ∮H·dl=I_fri,in, B=μ₀(H+M) och M=(μr−1)H i materialet. Identifiera cylindersymmetrin och den fria ström som omsluts i varje radialområde. Bestäm H från den fria strömmen innan du räknar B och M. Strömmen antas likformigt fördelad i rörmaterialets area π(b²−a²), inte i hela cirkelskivan.',
        hint_titles=('Innesluten fri ström', 'Cirkulation längs en cirkel', 'Från H till B och M'),
        hints=(
            'Dela upp rummet i R<a, a<R<b och R>b. Den omslutna fria strömmen är respektive 0, I(R²−a²)/(b²−a²) och I.',
            'En cirkulär Ampereslinga ger 2πR H_φ=I_fri,innesluten. Högerhandsregeln kring +z ger positiv φ-riktning för I>0.',
            'I kopparmodellen μr=1 är M=0 och B=μ0H. I järnmaterialet gäller M=(μr−1)H och B=μ0μrH; i hålet och utanför används vakuumrelationen.',
        ),
        self_checks=(
            'H är oberoende av μr och kontinuerligt vid a och b eftersom ingen fri ytström införts. Vid R=a är H=0.',
            'Vid b är H_φ kontinuerligt men B_φ och M_φ kan hoppa. B är tangentiellt mot denna gränsyta, så kravet på kontinuerligt normalt B förbjuder inte hoppet.',
        ),
        common_pitfall='Att blanda H [A/m] och B [T] på samma numeriska skala eller lägga μr i Ampères lag för H. Separata graflägen gör det möjligt att jämföra rätt storhet och enhet.',
        setup_hint='Beräkna först I_fri,innesluten från areakvoten. Använd därefter H_φ=I_fri,innesluten/(2πR), med H=0 i hålet även på axeln. Applicera materialrelationerna bara för a<R<b.',
        geometry_hint='Strömmen går längs rörets axel, medan H, B och M går runt axeln. R är avstånd från axeln; a och b är de två materialgränserna. Ställ μr=1 för del (a).',
    ),
    "HorseshoeMagnetAnchorForce": G(
        problem_id="8.6",
        learning_goal="Beräkna attraktionskraft från uppmätt magnetiskt flöde med hjälp av magnetiskt tryck i luftgap.",
        concepts=("magnetiskt tryck", "magnetiskt flöde", "kraft"),
        start_here='Skriv Φ=∫B·n dS och magnetiskt tryck p=B²/(2μ₀) i luftgapet. Identifiera arean för varje pol och summera krafterna pS på ankaret. Utgå från det uppmätta flödet i magnetkretsen. Samma flöde går genom båda polerna i serie; Φ0 ska inte delas i två.',
        hint_titles=('Fältet vid varje pol', 'Trycket i gapet', 'Summera polernas krafter'),
        hints=(
            'Med försumbart läckage och ungefär jämnt fält är B≈Φ0/S vid varje pol. Omvandla S=2,8 cm² till 2,8·10⁻⁴ m².',
            'Det magnetiska trycket i ett mycket litet luftgap är p=B²/(2μ0). Varje pol bidrar med kraften pS mot ankaret.',
            'Det finns två polytor med area S vardera. Addera deras krafter och sätt först därefter in flödet och arean.',
        ),
        self_checks=(
            'Resultatet blir cirka 256 N, avrundat 260 N i facit. En enda pol ger hälften av hela kraften.',
            'Kraften är attraktiv och beror på Φ0². Om flödets riktning vänds ändras inte kraftbeloppet; dubbelt flöde ger fyra gånger större kraft.',
        ),
        common_pitfall='Att dela flödet mellan de två polerna eller missa faktorn två i kraftsumman. Sambandet vid fast uppmätt flöde ska inte tolkas som att flödet förblir konstant om magnetens verkliga geometri ändras.',
        setup_hint='Skriv F_tot=2·[B²/(2μ0)]S och använd B=Φ0/S. Kontrollera att S är arean för en pol, inte summan av båda polytorna.',
        geometry_hint='Fältet går ut genom den ena polen och in genom den andra, men båda polerna drar ankaret mot magneten. Skissens två kontaktområden motsvarar två kraftbidrag.',
    ),
    "PermanentlyMagnetizedCylinderAxis": G(
        problem_id="8.12",
        learning_goal="Ersätta en homogen magnetisering med bundna magnetiseringsströmmar och därefter skilja mellan B och H.",
        concepts=("magnetisering", "magnetiseringsström", "B och H"),
        start_here='Skriv J_b=∇×M, K_b=M×n och Biot–Savarts lag för de bundna strömmarna. Identifiera magnetiseringens variation och ytornas normaler. Använd sedan H=B/μ₀−M med den lokala magnetiseringen. Använd cylindern 0<z<h och konstant M=Mẑ. Ersätt magnetiseringen med bundna strömmar; ingen fri ström behövs för att skapa magnetens B-fält.',
        hint_titles=('Vilka bundna strömmar finns?', 'Manteln som strömslingor', 'Från B till H'),
        hints=(
            'I volymen är J_m=∇×M=0. På manteln ger K_m=M×R̂=Mφ̂. Ändytorna har normal ±ẑ och därför ingen bunden ytström.',
            'En mantelremsa med höjd dz′ motsvarar en cirkulär slinga med dI=M dz′. Integrera dess axelfält över 0<z′<h med avståndet z−z′ till observationspunkten.',
            'Använd H=B/μ0−Mẑ inuti och H=B/μ0 utanför. För del (c), låt a växa vid fast h och fast observationspunkt z; då fås gränsen för en oändligt utbredd skiva.',
        ),
        self_checks=(
            'B_z är kontinuerligt över ändytorna på axeln och symmetriskt kring z=h/2. H_z hoppar med −M när du går in vid z=0 och med +M när du går ut vid z=h.',
            'Vid a→∞ och fast h,z går B→0. Inuti går H→−M och utanför H→0. För en lång smal cylinder långt från ändarna är i stället B≈μ0M och H≈0.',
        ),
        common_pitfall='Att använda B=μ0M utan avmagnetiserande H eller förväxla en mycket bred cylinder med en mycket lång. På idealiserade gränsytor ska H jämföras genom sina ensidiga gränsvärden.',
        setup_hint='Skriv B_z=μ0M/2 ∫₀ʰ a²/[a²+(z−z′)²]^(3/2) dz′. Efter integrationen bestäms H med den lokala magnetiseringen, som är noll utanför 0<z<h.',
        geometry_hint='Cylinderns botten ligger vid z=0 och toppen vid z=h, inte vid ±h/2. Mantelströmmen går moturs sedd från +z för M>0. Radie-kartan är en parameterstudie av axelfältet, inte ett rumsligt fält utanför axeln.',
    ),
    "MagnetizationCurrentsCylinder": G(
        problem_id="8.13",
        learning_goal="Härleda både volym- och ytmagnetiseringsströmmar från ett linjärt magnetiserat strömförande material och visa att deras nettoström tar ut sig.",
        concepts=("magnetiseringsström", "M=(μr−1)H", "cylindriska koordinater"),
        start_here='Skriv ∮H·dl=I_fri,in, M=(μr−1)H, J_b=∇×M och K_b=M×n. Identifiera den inneslutna fria strömmen och materialets utåtnormal före beräkning av de bundna strömmarna. Bestäm H från den fria transportströmmen och sedan M=(μr−1)H inne i ledaren. Beräkna därefter volymström och ytström var för sig; de har olika enheter.',
        hint_titles=('Magnetiseringen inne i ledaren', 'Volymström och ytström', 'Jämför de integrerade strömmarna'),
        hints=(
            'För R<a är I_fri,innesluten=IR²/a² och H_φ=IR/(2πa²). Därför är M_φ linjär i R.',
            'Volymströmmen är J_m,z=(1/R)d(RM_φ)/dR. På manteln används K_m=M×R̂; eftersom φ̂×R̂=−ẑ är ytströmmen motsatt volymströmmen när I(μr−1)>0.',
            'Integrera J_m över tvärsnittet och K_m över mantelytans skärning med tvärsnittet: I_m,vol=J_m,z πa² och I_m,yta=K_m,z 2πa. Addera först dessa strömmar i ampere.',
        ),
        self_checks=(
            'Volym- och ytbidragen blir (μr−1)I respektive −(μr−1)I. Deras summa är noll, men den fria transportströmmen I finns fortfarande kvar.',
            'Vid μr=1 eller I=0 försvinner båda magnetiseringsströmmarna. Om I eller tecknet på μr−1 ändras vänder båda riktningarna.',
        ),
        common_pitfall='Att addera J_m [A/m²] direkt till K_m [A/m], eller tolka noll nettomagnetiseringsström som att strömmarna och deras fält är noll överallt.',
        setup_hint='Sätt M_φ=(μr−1)IR/(2πa²) i cylindriska curl-formeln. Beräkna K_m från värdet precis innanför R=a. Volymens curl gäller inuti materialet; ytströmmen hanterar hoppet vid gränsen separat.',
        geometry_hint='Både volym- och ytström går axiellt, men i motsatta riktningar. Ytströmmen finns på manteln R=a; den är inte en azimutal ström runt tvärsnittets rand.',
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
            'Välj ledarna längs x vid y=0 och y=d, med ström i +x respektive −x. Välj slingnormal +z och låt u=y vara avståndet från den nedre ledaren. Mellan ledarna adderas fälten: B_z=μ0I[1/u+1/(d−u)]/(2π). Returledaren ska inte subtraheras eftersom dess strömriktning redan är omvänd.',
            'Kvadratens diagonal över mellanrummet är d och sidan d/√2. En remsa på höjden u har bredd 2u för 0<u<d/2 och 2(d−u) för d/2<u<d.',
            'Integrera B_z gånger remsans area, använd spegelsymmetri kring u=d/2 och dividera flödet med I. Behåll båda ledarnas bidrag även när du utnyttjar symmetrin.',
        ),
        self_checks=(
            'M ska vara proportionell mot μ0d och ha enheten henry. Om alla längder fördubblas fördubblas M.',
            'B divergerar vid en ideal linjeledare, men kvadratens lokala bredd går samtidigt mot noll. Flödesintegralen är därför ändlig. Vänd mottagarslingans normal och tecknet på M vänds.',
        ),
        common_pitfall='Att använda hela arean gånger centrumfältet eller anta konstant remsbredd. Kvadratens hörn tangerar ledarna geometriskt utan att slingorna ska vara elektriskt förbundna.',
        visualization_note="En skiss som visar den lokala kvadratbredden som funktion av x gör integraluppställningen betydligt lättare att förstå.",
        setup_hint='Med normal +z skriv Φ=2∫₀^{d/2} [μ0I/(2π)] [1/u+1/(d−u)]·2u du. Förenkla produkten innan ändpunkten u=0 behandlas.',
        geometry_hint='x går längs ledarna och u=y tvärs mellan dem. Detta är en roterad kvadrat, inte en rektangel med konstant bredd. Skissens strömpilar ger positivt flöde genom normal +z.',
    ),
    "MutualInductanceCoaxialLoops": G(
        problem_id="9.4",
        learning_goal="Se reciprociteten i ömsesidig induktans genom två olika approximativa flödesberäkningar.",
        concepts=("ömsesidig induktans", "dipolapproximation", "reciprocitet"),
        start_here='Skriv M=Φ_mottagare/I_källa och Φ=∫B·n dS. Identifiera vilken slinga som är källa i varje del och var de givna småparameterantagandena får användas. Uppgiften antar a≪b och a≪d. Använd två olika källslingor i del (a) och (b), men håll mottagarens normal och strömriktning konsekventa så att M kan jämföras.',
        hint_titles=('Den lilla slingan som källa', 'Integrera över den stora skivan', 'Byt källa och mottagare'),
        hints=(
            'I del (a) ersätts den lilla slingan med m=I_litenπa². På den stora slingans skiva, på axialavstånd d, behövs B_z(R)=μ0m(2d²−R²)/[4π(R²+d²)^(5/2)].',
            'Integrera B_z(R)·2πR dR från 0 till b. Använd inte bara dipolfältets axelvärde över hela den stora arean; både belopp och tecken på B_z kan variera.',
            'I del (b) är den stora slingans exakta axelfält nästan konstant över den lilla arean πa². Beräkna Φ_liten≈B_z(d)πa² och dividera med strömmen i den stora slingan. Resultaten ska sammanfalla.',
        ),
        self_checks=(
            'För d≫b ska M avta som d⁻³. M är proportionell mot den lilla slingans area och är positiv för de samriktade normaler som appen använder.',
            'Reciprocitet betyder M12=M21 för samma geometri. Den asymmetriskt skrivna approximationen får inte användas med a och b utbytta utan att kraven på vilken slinga som är liten fortfarande gäller.',
        ),
        common_pitfall='Att förväxla reciprocitet med tillåtelse att använda en approximation utanför dess giltighetsområde. Kontrollera a/b och a/d före tolkningen av ett numeriskt resultat.',
        setup_hint='Del (a): skriv M=Φ_stor/I_liten och integrera det radiella dipolfältet över skivan. Del (b): skriv M=[μ0I_stor b²/(2(b²+d²)^(3/2))]πa²/I_stor.',
        geometry_hint='Slingornas plan är parallella och deras gemensamma axel går genom båda centrum. I ett snitt genom axeln syns slingorna som två kantställda sträckor, inte två cirklar bredvid varandra i samma plan.',
    ),
    "OpenSecondaryTransformerVoltage": G(
        problem_id="9.6",
        learning_goal="Koppla en tidsvarierande primärström till sekundärspänning via järnkärnans flöde och Faradays lag.",
        concepts=("Faradays lag", "transformator", "flödeskoppling"),
        start_here='Skriv ∮H·dl=N1 i1, B=μ₀μrH, Φ=∫B·n dS och emk₂=−N2 dΦ/dt. Identifiera kärnans längd och area samt den givna tidsberoende strömmen. Sekundärlindningen är öppen: den bär ingen ström men kan ha en inducerad spänning. Bestäm först kärnflödet från den givna primärströmmen, inte från ett antaget spänningsförhållande.',
        hint_titles=('Kärnfältet från primärströmmen', 'Flöde och flödeskoppling', 'Tidsderivata och tecken'),
        hints=(
            'Försumma läckage och anta linjär kärna med konstant μr. Ampères lag ger Hℓ=N1i1(t), och B=μ0μrH.',
            'Flödet per varv är Φ=BS. Sekundärens flödeskoppling är N2Φ, vilket ger ännu en varvtalsfaktor utöver N1 i fältet.',
            'Använd u2=−N2 dΦ/dt med vald positiv omloppsriktning. När i1=I0cos(ωt) ger derivatan −ωI0sin(ωt), så spänningen blir positiv sinus i facits konvention.',
        ),
        self_checks=(
            'Vid t=0 är ström och flöde maximala men spänningen noll eftersom flödesderivatan är noll. Vid en fjärdedels period är den positiva spänningen maximal i den valda konventionen.',
            'Vid ω=0 eller I0=0 är den inducerade spänningen noll. Amplituden skalar med N1N2, μr, S och ω, och om polaritetsreferensen vänds byter hela kurvan tecken.',
        ),
        common_pitfall='Att sätta sekundärspänningen till noll för att kretsen är öppen, eller glömma N2 i flödeskopplingen. Linjär μr är en modellförutsättning, inte en beskrivning av mättnad och hysteres.',
        setup_hint='Skriv Φ(t)=μ0μrN1SI0cos(ωt)/ℓ och derivera N2Φ. Håll isär vinkelfrekvens ω [rad/s] och frekvens f=ω/(2π) [Hz].',
        geometry_hint='Båda lindningarna länkar samma kärnflöde i idealmodellen. Spänningens tecken kräver en vald lindnings- och mätorientering; facits plus framför sinus är knutet till den konventionen.',
    ),
    "MovingLoopFieldWork": G(
        problem_id="9.13",
        learning_goal="Koppla mekaniskt arbete vid rörelse genom ett magnetfält till inducerad ström och resistiv värme.",
        concepts=("rörelse-emk", "Lenz lag", "energibalans"),
        start_here='Skriv Φ=∫B·n dS, emk=−dΦ/dt, I=emk/RΩ och W=∫I²RΩ dt för konstant fart och försumbar självinduktans. Identifiera den överlappande arean som funktion av läget innan du deriverar. Följ flödet genom slingan när dess främre kant flyttas åt +x. Fältområdet är 0<x<ℓ och slingan sträcker sig från x−a till x. Uppgiftens ℓ=30 cm är större än a=10 cm.',
        hint_titles=('När ändras arean?', 'Från inducerad ström till effekt', 'Integrera arbetet över tiden'),
        hints=(
            'När ℓ≥a finns en inträdesfas, en fas med hela slingan inne och en utträdesfas. Endast under in- och utträde ändras överlappningsarean; då är |dA/dt|=av.',
            'Om slingans självinduktans försummas blir i=ε/RΩ, där ε=−dΦ/dt. Lenz lag ger en bromskraft i båda övergångarna. Vid konstant hastighet är den yttre mekaniska effekten lika med i²RΩ.',
            'Varje övergång i uppgiftens geometri varar a/v. Integrera effekten under båda övergångarna. Om du utforskar ℓ<a varar de i stället ℓ/v; när hela fältremsan ligger inuti slingan är flödet åter konstant.',
        ),
        self_checks=(
            'Med B=1 T, a=0,10 m, v=10 m/s och RΩ=0,05 Ω blir arbetet 0,40 J. Effekten är aldrig negativ även om emk och ström byter tecken mellan in- och utträde.',
            'Vid ℓ≥a är arbetet oberoende av ℓ. För ett smalare fältområde minskar arbetet proportionellt mot ℓ. Vid B=0 blir både effekt och arbete noll.',
        ),
        common_pitfall='Att räkna bromsarbete under hela förflyttningen eller använda samma strömriktning vid in- och utträde. Resultatet förutsätter konstant fart och försumbar självinduktans; magnetkraften motverkar rörelsen.',
        visualization_note="En enkel animation av överlappningsarean A(t) kan vara mycket pedagogisk här, eftersom den direkt visar när dΦ/dt är noll respektive icke-noll.",
        setup_hint='Sätt P=(Bav)²/RΩ i de två intervall där överlappningen ändras och P=0 annars. Använd dt=dx/v. För hela passagen blir övergångarnas sammanlagda längd 2min(a,ℓ).',
        geometry_hint='x betecknar främre kanten, inte slingans centrum eller bakre kant. Inträdet börjar vid x=0 och passagen är färdig vid x=ℓ+a. För ℓ≥a ligger slingan helt inne när a≤x≤ℓ.',
    ),
    "MovingLoopDipoleEmf": G(
        problem_id="9.14",
        learning_goal="Visa att tidsvarierande flöde i ett medföljande system och rörelse-emk i ett fast system beskriver samma inducerade spänning.",
        concepts=("Faradays lag", "rörelse-emk", "dipolfält"),
        start_here='Skriv emk=−dΦ/dt med Φ=∫B·n dS, eller emk=∮(v×B)·dℓ för den rörliga slingan i det stationära fältet. Identifiera samma orientering, hastighet och fältkomponenter i båda metoderna. Välj slingnormal +z och positiv omloppsriktning moturs sedd från +z. Slingan befinner sig vid z>0 och v=dz/dt är signerad. Approximationen kräver a≪z.',
        hint_titles=('Flödet i slingans system', 'Rörelse-emk i dipolens system', 'Jämför tecken och belopp'),
        hints=(
            'I del (a) är flödet genom den lilla slingan ungefär Φ=πa²B_z(z), där dipolens axelfält är B_z=μ0m/(2πz³). Använd kedjeregeln dΦ/dt=(dΦ/dz)v.',
            'I del (b) beräknas ε=∮(v×B)·dℓ i dipolens stillastående system. På slingans rand behövs det lilla radiella fältet B_R≈3μ0ma/(4πz⁴), inte bara det axiella fältet.',
            'Eftersom ẑ×R̂=φ̂ bidrar vB_R längs hela omkretsen 2πa. Jämför med −dΦ/dt. För m>0 och v>0 minskar det positiva flödet, så den positiva emk:n försöker bevara det enligt Lenz lag.',
        ),
        self_checks=(
            'Vid v=0 är emk noll. Byt tecken på antingen m eller v och emk:n byter tecken. Fördubblat z minskar beloppet med en faktor 16 i approximationen.',
            'Båda beräkningssätten ska ge samma spänning med samma orientering. Den axiala komponenten ensam ger v×B_z=0 och kan därför inte förklara rörelse-emk:n.',
        ),
        common_pitfall='Att kasta bort det radiella fältet innan rörelseintegralen beräknas eller lägga ihop de två beskrivningssätten som två separata spänningskällor. De beskriver samma fysik.',
        setup_hint='Flödesvägen: derivera μ0ma²/(2z³) med dz/dt=v och använd minustecknet i Faradays lag. Rörelsevägen: multiplicera vB_R vid R=a med 2πa.',
        geometry_hint='Dipolen ligger i origo och slingan i ett plan vinkelrätt mot z-axeln. Positiv v betyder rörelse bort från dipolen; negativ v betyder rörelse mot den. Farten och magnetmomentet kan vändas oberoende.',
    ),

    # ------------------------------------------------------------------
    # Kapitel 10 – Förskjutningsströmmar
    # ------------------------------------------------------------------
    "DisplacementCurrentCapacitor": G(
        problem_id="10.2",
        setup_hint="Välj normalen från den positivt laddade plattan mot den negativa. Skriv D_n=Q/A och i=dQ/dt med samma teckenkonvention. Derivera vid fast A: J_F,n=i/A. En konstant begynnelseladdning bidrar inte till tidsderivatan.",
        geometry_hint="Förskjutningsströmmen går normalt genom hela plattarean. I vakuum passerar inga fria laddningar genom gapet; J_F beskriver det föränderliga elektriska fältet. Avståndet d påverkar spänningen men förkortas bort ur J_F vid given tillförd ström.",
        learning_goal="Se varför en tidsvarierande kondensatorström motsvaras av samma förskjutningsström genom gapet.",
        concepts=("förskjutningsström", "D-fält", "laddningskontinuitet"),
        start_here='Skriv J_F=∂D/∂t, ∮D·n dS=Q_fri,in och i=dQ/dt. Identifiera plattarean och strömmens teckenkonvention; kanteffekter försummas. Koppla den tillförda strömmen till hur snabbt plattladdningen Q(t) ändras. Därefter kan D-fältet mellan stora plattor skrivas direkt från Q(t).',
        hint_titles=('Ström och plattladdning', 'Bestäm D i gapet', 'Derivera vid fast area'),
        hints=(
            'Strömmen till en platta är i(t)=dQ/dt med tecken enligt vald riktning.',
            'Utan randeffekter är D normalt mot plattorna och homogent. En Gaussbox från metallens inre till gapet ger D_n A=Q. Lös efter D_n med samma normal som används för strömmen.',
            'Derivera D med avseende på tiden: J_F=∂D/∂t. Lägg märke till att plattavståndet d inte behövs för just denna storhet.',
        ),
        self_checks=(
            "Integralen av J_F över plattarean ska exakt ge den ledningsström i(t) som kommer fram i ledaren.",
            "J_F ska ha samma sinusform och fas som den givna strömmen i(t), inte som plattspänningen i allmänhet.",
        ),
        common_pitfall="Att först integrera strömmen till Q(t) och sedan tappa bort att tidsderivatan i J_F tar tillbaka den ursprungliga strömfunktionen.",
    ),
    "RadialChargeExpansionMaxwellTest": G(
        problem_id="10.3",
        setup_hint="Integrera ∂(r²J_r)/∂r=−r²∂ρ/∂t från 0 till r. Regularitet i centrum tar bort integrationskonstanten. Derivera sedan D_r=r⁻²∫₀ʳρ(r′,t)r′²dr′ vid fast observationsradie r, inte längs en laddnings bana.",
        geometry_hint="Rita en sfär med centrum i laddningsmolnet. J och J_F är radiella och motriktade. Symmetrin gäller hela fördelningen, inte bara en enskild laddning. Appens expanderande Gaussprofil är ett exempel med bevarad total laddning, inte en lösning för partiklarnas Coulombdrivna rörelse.",
        learning_goal="Använd sfärisk symmetri och kontinuitet för att förstå hur ledningsström och förskjutningsström kan ta ut varandra i Ampère–Maxwells lag.",
        concepts=("sfärisk symmetri", "kontinuitetsekvationen", "Ampère–Maxwells lag"),
        start_here=(
            'Skriv ∇·B=0, ∇×B=μ₀(J+∂D/∂t), ∇·D=ρ och ∂ρ/∂t+∇·J=0. Identifiera vilka fältriktningar sfärisk symmetri tillåter och kräv regularitet i centrum innan ekvationerna integreras. Del (a) är i första hand en symmetriuppgift. En sfäriskt symmetrisk B-vektor skulle behöva vara radiell, men kombinera det med ∇·B=0 och kravet på ett reguljärt fält utan magnetiska monopoler.'
        ),
        hint_titles=('Integrera kontinuitetsekvationen', 'D från laddningen innanför sfären', 'Jämför strömtätheterna'),
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
