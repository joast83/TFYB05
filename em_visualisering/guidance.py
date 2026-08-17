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


G = SolutionGuidance


GUIDANCE_BY_CLASS: dict[str, SolutionGuidance] = {
    # ------------------------------------------------------------------
    # Kapitel 2 – Coulombs lag, E-fält och potential i vakuum/luft
    # ------------------------------------------------------------------
    "ChargedSpheresSmallAngle": G(
        problem_id="2.1",
        learning_goal="Koppla ihop kraftjämvikt, geometri och småvinkelapproximation i samma härledning.",
        concepts=("Coulombs lag", "statisk jämvikt", "små vinklar"),
        start_here=(
            "Börja inte med Coulombs lag. Rita först krafterna på en av kulorna och inför "
            "halva vinkeln mellan trådarna. Vilka tre krafter verkar på kulan?"
        ),
        hints=(
            "Symmetrin gör att varje tråd lutar med vinkeln α/2 från lodlinjen. Skriv kraftjämvikt i horisontell och vertikal riktning.",
            "Kulornas inbördes avstånd är 2ℓ sin(α/2). För liten α kan både sin(α/2) och tan(α/2) ersättas med sina argument.",
            "Efter småvinkelapproximationen innehåller Coulombkraften en faktor 1/α² medan jämvikten ger ytterligare en faktor α. Samla därför alla α-termer innan du löser ekvationen.",
        ),
        self_checks=(
            "Om |Q| ökar ska α öka, inte minska.",
            "Kontrollera att uttrycket för α är dimensionslöst och att α→0 när Q→0.",
        ),
        common_pitfall="Att använda α som trådens vinkel mot lodlinjen i stället för α/2.",
    ),
    "ChargedRingAxis": G(
        problem_id="2.2",
        learning_goal="Använd symmetri för att reducera en vektorintegral till en enda komponent.",
        concepts=("Coulombs lag", "superposition", "symmetri"),
        start_here=(
            "Fråga först vilka fältkomponenter som över huvud taget kan finnas på z-axeln. "
            "Para ihop ett laddningselement med elementet diametralt mittemot."
        ),
        hints=(
            "Alla laddningselement på ringen ligger på samma avstånd från observationspunkten. De tvärgående komponenterna tar ut varandra parvis.",
            "Skriv dQ = λ a dφ och λ = Q/(2πa). Behåll endast z-komponenten av dE.",
            "När geometrifaktorerna är konstanta runt hela ringen återstår i praktiken bara integralen av dQ över ringen.",
        ),
        self_checks=(
            "E måste vara noll i ringens centrum, z=0.",
            "För |z|≫a ska fältet närma sig fältet från en punktladdning Q.",
        ),
        common_pitfall="Att integrera fältets belopp och glömma att dE är en vektor.",
        visualization_note="En axelgraf är användbar först efter härledningen, framför allt för att kontrollera z=0 och fjärrfältet.",
    ),
    "FiniteLineCharge2D": G(
        problem_id="2.3",
        learning_goal="Sätt upp Coulombintegralen för en ändlig linjeladdning och tolka gränsen mot en oändlig tråd.",
        concepts=("linjeladdning", "vektorintegral", "gränsvärde"),
        start_here=(
            "Låt källpunkten ligga på z-axeln med koordinat z′. Skriv först vektorn från "
            "källelementet till observationspunkten (x,0,0)."
        ),
        hints=(
            "Integrera z′ från −b till a och använd dQ = ρℓ dz′. Avståndsvektorn innehåller både en x- och en z-komponent.",
            "Dela upp integralen i E_x och E_z innan du integrerar. Det gör det tydligt varför en osymmetrisk ändlig tråd kan ge en z-komponent.",
            "I gränsen a,b→∞ ska ändeffekterna försvinna. Kontrollera särskilt att E_z→0 och jämför E_x med Gauss-lagens resultat för en oändlig linjeladdning.",
        ),
        self_checks=(
            "Om a=b ska E_z vara noll redan för den ändliga tråden.",
            "Det oändliga gränsfallet ska skala som 1/x.",
        ),
        common_pitfall="Att anta cylindersymmetri redan i del (a), trots att tråden där är ändlig och kan vara osymmetrisk kring origo.",
    ),
    "SemiCircularSurfaceAxis": G(
        problem_id="2.4",
        learning_goal="Hantera en ytladdningsintegral där endast en del av symmetrin finns kvar.",
        concepts=("ytladdning", "polära koordinater", "komponentsymmetri"),
        start_here=(
            "Använd polära koordinater i den laddade halvcirkelytan. Innan du räknar: vilken "
            "horisontell komponent måste försvinna av spegelsymmetri, och vilken behöver inte göra det?"
        ),
        hints=(
            "Sätt dS = R dR dφ och dQ = ρs dS. Avståndet till punkten på z-axeln är √(R²+z²).",
            "Dela dE i x-, y- och z-komponenter. Integralen över vinkeln avgör vilka komponenter som tar ut varandra.",
            "Gör vinkelintegralen och radialintegralen separat. Halvcirkeln gör att en tvärkomponent överlever, till skillnad från en hel cirkelskiva.",
        ),
        self_checks=(
            "Den komponent som motsvarar figurens spegelsymmetri ska bli exakt noll.",
            "Långt från ytan ska hela laddningsfördelningen bete sig ungefär som en punktladdning med den totala laddningen.",
        ),
        common_pitfall="Att låna symmetrin från en hel skiva och därför sätta alla tvärkomponenter till noll.",
    ),
    "SphericalShellPotential": G(
        problem_id="2.5",
        learning_goal="Beräkna potential direkt från en laddningsintegral och förstå varför resultatet blir styckvis.",
        concepts=("potentialintegral", "sfärisk symmetri", "källområde"),
        start_here=(
            "Placera observationspunkten på z-axeln utan att förlora generalitet. Då beror avståndet "
            "|r−r′| endast på r, a och polvinkeln θ."
        ),
        hints=(
            "Använd dQ = ρs a² sinθ dθ dφ med ρs = Q/(4πa²). φ-integralen kan göras direkt.",
            "I nämnaren får du √(r²+a²−2ar cosθ). Substitutionen u=cosθ reducerar integralen till en enkel rotintegral.",
            "När gränserna sätts in uppstår |r−a|. Det är just den absolutbeloppsfaktorn som delar svaret i r<a och r>a.",
        ),
        self_checks=(
            "Potentialen ska vara kontinuerlig vid r=a.",
            "Inuti skalet ska V vara konstant; utanför ska den falla som 1/r.",
        ),
        common_pitfall="Att försöka använda E-fältets Gauss-lösning när uppgiften uttryckligen vill att potentialintegralen genomförs.",
    ),
    "ConcentricChargedCylinders": G(
        problem_id="2.6",
        learning_goal="Välja rätt Gaussyta och hålla reda på vilken laddning som omsluts i olika radialområden.",
        concepts=("Gauss lag", "cylindersymmetri", "styckvis fält"),
        start_here="Dela först upp rummet i R<a, a<R<b och R>b. Rita en koaxial Gauss-cylinder i varje område.",
        hints=(
            "På mantelytan är E radiellt och konstant i belopp. Ändytorna ger inget flöde.",
            "Skriv den inneslutna laddningen per vald längd L. I mellanområdet omsluts bara laddningen på den inre cylindern.",
            "Utanför båda cylindrarna måste bidragen från båda ytladdningarna tas med i Q_innesluten.",
        ),
        self_checks=(
            "Fältet ska ha 1/R-beroende i de områden där den inneslutna laddningen per längd är konstant.",
            "Språnget i E_n över en laddad yta ska vara förenligt med ytladdningstätheten.",
        ),
        common_pitfall="Att använda samma inneslutna laddning i alla tre radialområden.",
    ),
    "SphericalCapacitorDesign": G(
        problem_id="2.7",
        learning_goal="Göra en fysikalisk optimering där genomslagsfältet sätter en begränsning.",
        concepts=("sfärisk kondensator", "fältmaximum", "optimering"),
        start_here="Bestäm först var mellan sfärerna |E| är störst. Det är där genomslagsvillkoret ska appliceras.",
        hints=(
            "Mellan sfärerna har E(r) samma radialberoende som fältet från den inneslutna laddningen Q.",
            "Använd E(a)=Emax för att uttrycka den största tillåtna Q som funktion av den inre radien a.",
            "Sätt sedan in Q(a) i U=∫_a^b E(r)dr. Då blir U en enkel funktion av a som kan maximeras med derivata.",
        ),
        self_checks=(
            "U ska gå mot noll både när a→0 och när a→b.",
            "Optimum måste därför ligga strikt mellan 0 och b.",
        ),
        common_pitfall="Att optimera kondensatorns vanliga spänningsuttryck med Q konstant, trots att Q här begränsas av Emax och därför beror på a.",
    ),
    "ConcentricSphericalShells": G(
        problem_id="2.8",
        learning_goal="Bygga en styckvis potential genom superposition och använda ledarvillkor efter sammankoppling.",
        concepts=("superposition", "sfärskal", "elektrostatisk ledare"),
        start_here="Behandla varje sfäriskt skal separat: vad är potentialen från ett jämnt laddat skal innanför respektive utanför skalet?",
        hints=(
            "Summera bidragen från Qa och Qb och skriv V(r) separat för r<a, a<r<b och r>b.",
            "Potentialen från ett skal är konstant på alla punkter innanför det skalet. Det förenklar de två innersta områdena.",
            "När skalen kopplas ihop blir de en enda sammanhängande ledare i elektrostatisk jämvikt. Fråga vad E måste vara i metall och i den tomma region som inte behöver bära laddning.",
        ),
        self_checks=(
            "V ska vara kontinuerlig vid både r=a och r=b.",
            "Efter sammankopplingen ska den totala laddningen Qa+Qb vara bevarad.",
        ),
        common_pitfall="Att kräva att laddningen på varje ursprungligt skal bevaras efter att de satts i ledande förbindelse.",
    ),
    "AtmosphericChargeDensity": G(
        problem_id="2.9",
        learning_goal="Översätta en observerad fältändring till medelladdning via Gauss lag/divergens.",
        concepts=("Gauss lag", "fältgradient", "teckenkonvention"),
        start_here="Välj z uppåt och skriv de givna vertikala fälten som signerade z-komponenter innan du använder några belopp.",
        hints=(
            "Använd en stor tunn/vertikal Gaussvolym med botten vid marken och toppen på 1400 m. Sidoflödet försummas i den idealiserade modellen.",
            "Flödet bestäms av E_top·n_top och E_bottom·n_bottom. Lägg märke till att normalerna pekar åt motsatta håll.",
            "Dividera Q_innesluten = ε0Φ_E med volymen A h för att få den genomsnittliga rymdladdningstätheten.",
        ),
        self_checks=(
            "Arean A ska försvinna ur slututtrycket.",
            "Tecknet ska stämma med att E_z blir mindre negativ när z ökar.",
        ),
        common_pitfall="Att subtrahera fältens belopp utan att först ta hänsyn till ytornas normalriktningar.",
    ),
    "OffsetCavitySphereExterior": G(
        problem_id="2.10",
        learning_goal="Använd superposition för att ersätta ett hålrum med en negativ laddningsfördelning.",
        concepts=("superposition", "homogent laddat klot", "förskjutet centrum"),
        start_here="Tänk det verkliga objektet som ett helt laddat klot plus ett mindre klot med laddningstäthet −ρ där hålrummet finns.",
        hints=(
            "För x>b ligger observationspunkten utanför båda kloten. Varje homogent sfäriskt laddningsmoln kan därför ersättas av sin totala laddning placerad i respektive centrum.",
            "Beräkna total laddning för det stora klotet och för det negativa 'hål-klotet' separat.",
            "Sätt in rätt avstånd från observationspunkten till de två olika centren. Det är den förskjutningen som hindrar bidragen från att kombineras till en enda punktladdning i origo.",
        ),
        self_checks=(
            "Om a→0 ska hålrummets bidrag försvinna.",
            "Om d→0 ska problemet reduceras till två koncentriska sfäriska laddningsfördelningar.",
        ),
        common_pitfall="Att använda avståndet x till båda sfärernas centrum trots att hålrummets centrum är förskjutet.",
    ),
    "CoaxialCylinderVoltage": G(
        problem_id="2.11",
        learning_goal="Gå från Gauss-lagens koaxialfält till ett givet spänningsfall.",
        concepts=("koaxial geometri", "Gauss lag", "potentialskillnad"),
        start_here="Bestäm först den allmänna formen E(R)=C/R mellan cylindrarna; bestäm sedan konstanten från spänningen U.",
        hints=(
            "Integrera E radiellt mellan a och b. Logaritmen ln(b/a) är den naturliga geometrifaktorn i en koaxial kondensator.",
            "Lös ut konstanten C ur U=|∫_a^b E·dℓ|.",
            "'Mittemellan skalen' betyder här radialkoordinaten R=(a+b)/2, inte det geometriska medelvärdet.",
        ),
        self_checks=(
            "E ska minska med ökande R.",
            "Om U fördubblas ska E fördubblas överallt.",
        ),
        common_pitfall="Att anta ett homogent fält U/(b−a), vilket inte gäller för cylindrisk geometri.",
    ),
    "SphericalConductorBreakdown": G(
        problem_id="2.12",
        learning_goal="Koppla luftens genomslagsfält till maximal laddning och potential på en sfärisk ledare.",
        concepts=("ledande sfär", "genomslag", "potential"),
        start_here="Var är fältet från en laddad ledande sfär störst? Applicera Emax just där.",
        hints=(
            "Utanför sfären är E(r) samma som för en punktladdning Q i centrum och avtar som 1/r².",
            "Sätt E(a)=Emax och lös först ut Qmax.",
            "Använd därefter sfärens potential relativt oändligheten. Du kan också integrera E från a till ∞ som kontroll.",
        ),
        self_checks=(
            "Qmax ska växa som a² medan Vmax ska växa som a.",
            "En större sfär kan därför bära högre potential vid samma tillåtna ytfält.",
        ),
        common_pitfall="Att sätta genomslagsvillkoret vid någon godtycklig punkt utanför sfären i stället för på ytan.",
    ),
    "CoaxialTubeSpaceCharge": G(
        problem_id="2.13",
        learning_goal="Lösa Poisson/Gauss-problemet i cylindrisk geometri när det finns en konstant rymdladdning.",
        concepts=("rymdladdning", "cylindrisk Gauss lag", "randvillkor"),
        start_here="Anta E=E(R) R̂. Använd först Gauss lag i differential- eller integralform för att hitta den allmänna radialformen när ρ är konstant.",
        hints=(
            "Integrationen ger två typer av termer: en proportionell mot R från rymdladdningen och en integrationskonstant proportionell mot 1/R.",
            "Randvillkoret E(a)=0 bestämmer integrationskonstanten innan spänningen används.",
            "Använd därefter potentialskillnaden mellan a och b för att bestämma ρ. Den totala molnladdningen fås från ρ gånger volymen π(b²−a²)ℓ.",
        ),
        self_checks=(
            "Elektronmolnets totala laddning ska få negativt tecken med de angivna potentialerna.",
            "Det insatta E(R) ska verkligen ge E(a)=0.",
        ),
        common_pitfall="Att använda det laddningsfria koaxialfältet C/R trots att området innehåller konstant rymdladdning.",
    ),
    "RadialChargeSphere": G(
        problem_id="2.16",
        learning_goal="Välja den kortaste vägen till potentialen i centrum för en sfäriskt symmetrisk laddningsfördelning.",
        concepts=("potential", "sfäriska skal", "rymdladdning"),
        start_here="För just V(0) är det enklare att summera potentialbidrag från tunna sfäriska skal än att först bestämma E(r) överallt.",
        hints=(
            "Ett tunt skal med radie r och tjocklek dr har laddning dQ=ρ(r)4πr²dr.",
            "Alla punkter på skalet ligger på avstånd r från centrum, så dess bidrag där är dV=dQ/(4πε0 r).",
            "Sätt in ρ(r)=A(a−r) och integrera endast från 0 till a. Referensen V(∞)=0 är redan inbyggd i Coulombpotentialen.",
        ),
        self_checks=(
            "Integranden ska vara ändlig vid r=0.",
            "Dimensionen ska bli volt; A har dimension C/m⁴ eftersom ρ=A(a−r).",
        ),
        common_pitfall="Att göra en lång styckvis E-fältsberäkning när direkt potentialintegration i centrum är betydligt enklare.",
    ),
    "InsertedMetalPlateCapacitor": G(
        problem_id="2.18",
        learning_goal="Skilja på vad som hålls konstant före och efter att batteriet kopplats bort.",
        concepts=("plattkondensator", "konstant laddning", "ledare i fält"),
        start_here="Markera tidsordningen: kondensatorn laddas med batteriet anslutet, sedan kopplas batteriet bort. Vad är därför bevarat i del (b) och (c)?",
        hints=(
            "I del (a) används den vanliga plattkondensatorn C=ε0A/d0 och Q=CU.",
            "En ideal metallplatta har E=0 inuti. Med oförändrad fri laddning ligger samma fält i de återstående luftgapens sammanlagda tjocklek d0−d1.",
            "När plattavståndet ändras utan batteri är Q och därmed ytladdningstätheten konstant. Då är E oförändrat men U=Ed ändras proportionellt mot avståndet.",
        ),
        self_checks=(
            "Insättning av metallplattan ska minska spänningen när Q hålls konstant.",
            "Ökat plattavstånd ska öka spänningen när Q hålls konstant.",
        ),
        common_pitfall="Att hålla U konstant i del (b) och (c) trots att batteriet har kopplats bort.",
    ),
    "UniformSpaceChargePlates": G(
        problem_id="2.19",
        learning_goal="Kombinera Poissons ekvation med en föreskriven potentialskillnad och sedan lokalisera E=0.",
        concepts=("Poissons ekvation", "1D-fält", "randvillkor"),
        start_here="Välj en x-koordinat mellan plattorna och bestäm tydligt vilken platta som ligger vid x=0. Skriv sedan dE/dx=ρ0/ε0.",
        hints=(
            "Integrera en gång: E(x) är linjär men innehåller en konstant som ännu inte är bestämd.",
            "Bestäm konstanten genom potentialskillnaden mellan plattorna, V0=−∫E·dx med konsekvent orientering.",
            "Sätt därefter E(x)=0. För del (b) krävs att den erhållna nollpunkten verkligen ligger mellan 0 och d.",
        ),
        self_checks=(
            "Med konstant ρ0 ska E vara en rät linje som funktion av x.",
            "Villkoret i del (b) ska vara symmetriskt i tecknet på V0 när det skrivs som en begränsning på |V0|.",
        ),
        common_pitfall="Att lösa E=0 innan integrationskonstanten har bestämts från potentialrandvillkoret.",
    ),

    # ------------------------------------------------------------------
    # Kapitel 3 – Dielektriska material
    # ------------------------------------------------------------------
    "HClDipoleField": G(
        problem_id="3.1",
        learning_goal="Se hur två motsatta punktladdningar övergår i dipolfält när observationsavståndet är stort.",
        concepts=("elektrisk dipol", "superposition", "fjärrfältsapproximation"),
        start_here="Skriv fältet som summan av H+- och Cl−-jonens Coulombfält. Utnyttja sedan att r0 är mycket större än jonseparationen d.",
        hints=(
            "På z-axeln ligger observationspunkten på dipolens axel; bidragen får samma huvudriktning men olika avstånd till laddningarna.",
            "På y-axeln är avstånden till de två jonerna lika. Där tar vissa komponenter ut varandra medan de komponenter längs dipolaxeln adderas.",
            "Utveckla i den lilla parametern d/r0 och behåll första icke-försvinnande termen. Resultatet ska skala som dipolmomentet e d delat med r0³.",
        ),
        self_checks=(
            "Båda fälten ska avta som 1/r0³ i dipolapproximationen.",
            "Axelfältet ska vara större än ekvatorialfältet vid samma r0.",
        ),
        common_pitfall="Att behandla den neutrala molekylen som en punktladdning; dess nettoladdning är noll och 1/r²-termen försvinner.",
    ),
    "PorcelainSlabCapacitor": G(
        problem_id="3.3",
        learning_goal="Använd randvillkor för D och spänningssumman över två seriekopplade materialskikt.",
        concepts=("D-fält", "dielektrikum", "seriekopplade skikt"),
        start_here="Det finns ingen fri laddning i gränsytan mellan luft och porslin. Vilken normal komponent är därför kontinuerlig?",
        hints=(
            "För plana skikt gäller D_luft=D_porslin i normalriktningen. Däremot är E=D/ε olika i de två materialen.",
            "Skriv E_porslin = D/(ε0εr) och E_luft = D/ε0.",
            "Den givna spänningen är summan av potentialfallen: U=E_porslin d_porslin + E_luft d_luft. Lös först D och därefter E i varje skikt.",
        ),
        self_checks=(
            "E ska vara mindre i porslinet än i luften med faktorn εr när D är samma.",
            "Spänningsfallen över de två delarna ska tillsammans bli 10 kV.",
        ),
        common_pitfall="Att sätta samma E i båda materialen bara för att fältlinjerna är normala mot gränsytan.",
    ),
    "GroundedInnerSphereChargeSplit": G(
        problem_id="3.6",
        learning_goal="Kombinera Gauss lag, laddningskonservering och ett jordningsvillkor för en flerledargeometri.",
        concepts=("jordad ledare", "sfärisk symmetri", "dielektrikum"),
        start_here="Inför okända laddningar på den inre sfären, plåtskalets insida och plåtskalets utsida. Skriv först vilka relationer som följer direkt av Gauss lag och skalets nettoladdning Q.",
        hints=(
            "Fältet i själva metallen måste vara noll. En Gaussyta inne i plåtskalets metall ger därför en relation mellan laddningen på den inre sfären och laddningen på skalets insida.",
            "Plåtskalets två ytladdningar måste tillsammans ge dess givna nettoladdning Q.",
            "Den återstående ekvationen kommer från jordningen: potentialen på den inre sfären ska vara samma som vid oändligheten. Beräkna potentialbidrag från den inre sfären och från skalet, med rätt permittivitet i mellanrummet.",
        ),
        self_checks=(
            "De två laddningarna på plåtskalet ska summera till Q.",
            "Det slutliga förhållandet Q_utsida/Q_insida ska vara dimensionslöst och oberoende av a när geometrin bara innehåller radierna a och 3a.",
        ),
        common_pitfall="Att sätta potentialen på det yttre skalet till noll; det är den inre sfären som är jordad.",
    ),
    "ChargedDielectricShell": G(
        problem_id="3.7",
        learning_goal="Lösa E och V styckvis i en sfäriskt symmetrisk geometri med både vakuum och dielektrikum.",
        concepts=("Gauss lag för D", "styckvis medium", "potentialkontinuitet"),
        start_here="Dela upp problemet i r<a, a<r<b och r>b. Använd D-fältet först, eftersom Gauss lag för D kopplar direkt till den fria rymdladdningen.",
        hints=(
            "För r<a omsluter en Gaussyta ingen laddning. För a<r<b omsluts bara laddningen mellan a och r. För r>b omsluts all laddning i skalvolymen.",
            "När D(r) är känd fås E=D/ε0 i vakuum och E=D/(ε0εr) i dielektrikumet.",
            "Bestäm potentialen från V(∞)=0 genom att integrera E inåt och se till att V är kontinuerlig vid r=b och r=a.",
        ),
        self_checks=(
            "E ska vara noll i hålrummet r<a av sfärisk symmetri och noll innesluten laddning.",
            "Utanför b ska fältet motsvara den totala fria laddningen och avta som 1/r².",
        ),
        common_pitfall="Att använda εr även i vakuumområdena eller glömma att potentialen måste matchas mellan regionerna.",
    ),
    "DielectricFilledSphericalGap": G(
        problem_id="3.9",
        learning_goal="Använd ett gränsvillkor geometriskt: E är tangentiellt mot gränsytan mellan de två dielektrika.",
        concepts=("randvillkor", "E och D", "sfärisk Gaussyta"),
        start_here="Gränsytan mellan materialen är ett plan genom centrum. Det radiella E-fält som uppgiften låter dig anta ligger därför längs gränsytan, inte normalt mot den.",
        hints=(
            "Tangentiella E-komponenten är kontinuerlig. Alltså har båda dielektrikumen samma radiella E(r) vid ett givet r.",
            "D skiljer sig däremot: D1=ε0ε1E och D2=ε0ε2E.",
            "Använd en sfärisk Gaussyta. Varje material upptar en halv sfäryta, så flödet är summan av två halvsfärsbidrag och ska bli Q.",
        ),
        self_checks=(
            "E ska vara samma på båda sidor om den radiella materialgränsen.",
            "D ska vara större i materialet med större εr.",
        ),
        common_pitfall="Att använda kontinuitet för D_n trots att fältet här är tangentiellt mot materialgränsen.",
    ),
    "MakrofolCapacitorDesign": G(
        problem_id="3.11",
        learning_goal="Dimensionera först mot genomslag och därefter mot önskad kapacitans.",
        concepts=("genomslag", "plattkondensator", "dimensionering"),
        start_here="Lös del (a) helt innan du använder kapacitansformeln. Vilken minsta total dielektrikumtjocklek krävs för att 50 kV inte ska överskrida genomslagsfältet?",
        hints=(
            "För ett homogent makrofolskikt gäller E=U/d_total. Kravet E≤E_genomslag ger ett minsta d_total.",
            "Dividera den minsta tjockleken med 0,10 mm per skikt och avrunda uppåt till helt antal skikt.",
            "Använd sedan den faktiskt valda totalstjockleken i C=ε0εrA/d för att lösa ut arean.",
        ),
        self_checks=(
            "Antalet skikt måste vara ett heltal och får aldrig avrundas nedåt.",
            "Större total tjocklek minskar kapacitansen vid oförändrad area, så arean måste anpassas därefter.",
        ),
        common_pitfall="Att använda den kontinuerligt beräknade minimitjockleken i del (b) i stället för tjockleken hos det heltalsantal skikt som faktiskt valdes.",
    ),
    "CoaxialTwoDielectricCapacitance": G(
        problem_id="3.12",
        learning_goal="Bygga kapacitansen för två koaxiella dielektriska skikt genom att summera potentialfall.",
        concepts=("koaxial kondensator", "D-fält", "seriekopplade dielektrika"),
        start_here="Bestäm först radien för gränsen mellan de två lika tjocka skikten. Arbeta sedan med en fri linjeladdning λ på innerledaren.",
        hints=(
            "Gauss lag ger D_R=λ/(2πR) genom båda skikten eftersom samma fria laddning omsluts.",
            "I skikt i gäller E_i(R)=D_R/(ε0ε_i). Integrera E_1 från a till mellanradien och E_2 därifrån till c.",
            "Summera de två potentialfallen till U och använd C/L=λ/U.",
        ),
        self_checks=(
            "Om ε1=ε2 ska uttrycket kollapsa till den vanliga koaxialkapacitansen med ett enda material.",
            "Båda bidragen till U ska innehålla logaritmer av radiekvoter.",
        ),
        common_pitfall="Att behandla skikten som två plana kondensatorer; den radiella koaxialgeometrin ger logaritmiska potentialfall.",
    ),
    "BreakdownVoltageCases": G(
        problem_id="3.13",
        learning_goal="Skilja mellan homogen isolering och två material i serie när genomslagsfält begränsar spänningen.",
        concepts=("genomslagsfält", "D-kontinuitet", "serielager"),
        start_here="I del (a) och (b) är fältet homogent, men i del (c) är samma D normal mot två olika material. Behandla därför del (c) separat.",
        hints=(
            "För ett homogent medium är U_max=E_genomslag d. εr påverkar inte denna relation när hela gapet är fyllt av samma material.",
            "I blandfallet utan fri gränsladdning är D samma i luft och plexiglas. Därför är E_luft/E_plexi=εr.",
            "Bestäm vilket material som når sitt genomslagsfält först när D ökas. Sätt D till den begränsande nivån och summera därefter U=E_luft d_luft+E_plexi d_plexi.",
        ),
        self_checks=(
            "I del (c) ska luftens fält vara större än plexiglasets när εr>1.",
            "Båda lokala fälten måste ligga under respektive genomslagsgräns vid den slutliga U_max.",
        ),
        common_pitfall="Att anta att den totala spänningen i blandfallet kan fås genom att multiplicera hela gapet med ett enda genomslagsfält.",
    ),
    "DielectricSlabCapacitor": G(
        problem_id="3.14",
        learning_goal="Knyta ihop D-kontinuitet, spänningsfall, fri ytladdning och polarisationsladdning.",
        concepts=("D-fält", "polarisation", "randvillkor"),
        start_here="Börja med del (a): eftersom gränsytan inte bär fri laddning är D_n samma i luft och dielektrikum. Låt detta gemensamma D vara den enda okända fältamplituden.",
        hints=(
            "Skriv E_luft=D/ε0 och E_diel=D/(ε0εr). De två skikttjocklekarna är 0,2d respektive 0,8d.",
            "Använd V0=E_luft(0,2d)+E_diel(0,8d) för att bestämma D.",
            "På metallplattorna är den fria ytladdningen ±D_n. För polarisationsladdningen använder du P=ε0(εr−1)E_diel och ρ_sp=P·n på dielektrikumets två ytor.",
        ),
        self_checks=(
            "D ska vara samma i båda materialen men E ska inte vara det.",
            "Polarisationsladdningarna på dielektrikumets två plana ytor ska ha motsatta tecken.",
        ),
        common_pitfall="Att blanda ihop fri ytladdning på metallplattorna med bunden polarisationsladdning på dielektrikumets ytor.",
    ),
    "ElectretCylinderAxis": G(
        problem_id="3.18",
        learning_goal="Ersätta en homogen polarisation med dess bundna laddningar och sedan använda superposition.",
        concepts=("elektret", "bunden laddning", "fält från skiva"),
        start_here="Beräkna först de bundna laddningarna från P: ρ_p=−∇·P i volymen och ρ_sp=P·n på ytan. Vilka av cylinderns ytor blir laddade?",
        hints=(
            "P är konstant, så volymladdningen är noll. Mantelytan har P·n=0, medan botten- och toppytan får motsatta konstanta ytladdningar.",
            "E-fältet på z-axeln blir därför superpositionen av fältet från två jämnt laddade cirkelskivor. Använd standardintegralen för en skiva eller integrera ringelement.",
            "När E är känt används D=ε0E+P inne i elektreten och D=ε0E utanför. I gränsen a≫h liknar systemet en oändlig plan kondensator av bundna laddningar.",
        ),
        self_checks=(
            "För a≫h ska E i huvudsak finnas mellan ändytorna och vara riktat motsatt P.",
            "För elektreten ska D bli kontinuerligt och i den plana gränsen gå mot noll, eftersom ytladdningen är bunden och inte fri.",
        ),
        common_pitfall="Att behandla ±P på ändytorna som fria laddningar när D-fältet beräknas; det ändrar randvillkoret i del (d).",
    ),
    "ObliqueConductorDielectricBoundary": G(
        problem_id="3.19",
        learning_goal="Bestäm fältets riktning från ledarrandvillkoret och geometrin hos ett snett plan.",
        concepts=("ledarrandvillkor", "ytladdning", "normalvektor"),
        start_here="Skriv först planets ekvation från skärningarna x=a och y=b. Ta sedan fram en normalvektor som pekar från ledaren mot dielektrikumet.",
        hints=(
            "Planet kan skrivas x/a+y/b=1. En normal är därför proportionell mot (1/a,1/b,0), eller ekvivalent mot (b,a,0). Normalisera den.",
            "I en perfekt ledare är E=0 och strax utanför ledaren måste den tangentiella E-komponenten vara noll. Fältet är alltså rent normalt mot ytan.",
            "Randvillkoret för den normala D-komponenten ger D_n=ρs när normalriktningen väl är vald. Därefter fås E=D/(ε0εr) i dielektrikumet.",
        ),
        self_checks=(
            "Det slutliga D-fältet ska ha belopp |ρs| och ligga längs ytans normal.",
            "Ingen z-komponent ska uppstå eftersom planet är parallellt med z-axeln.",
        ),
        common_pitfall="Att använda vektorn (a,b,0) som normal. För planet x/a+y/b=1 är normalen proportionell mot (1/a,1/b,0), inte mot skärningspunkterna själva.",
    ),
    # ------------------------------------------------------------------
    # Kapitel 4 – Energi, kraft och spegelladdning
    # ------------------------------------------------------------------
    "SphericalShellChargingEnergy": G(
        problem_id="4.1",
        learning_goal="Förstå uppladdningsarbete som en successiv process där potentialen ändras medan laddningen byggs upp.",
        concepts=("elektrostatisk energi", "potential", "uppladdningsarbete"),
        start_here=(
            "Tänk inte på skalet som att det får hela laddningen Q på en gång. Betrakta i stället ett mellanläge där skalet redan har laddningen q och du för in ytterligare dq."
        ),
        hints=(
            "Potentialen hos ett tunt ledande sfäriskt skal med aktuell laddning q är samma som potentialen från en punktladdning q på avståndet a.",
            "Det lilla arbete som krävs för nästa laddningsbidrag är dW = V(q)dq. Det viktiga är att V inte är konstant under uppladdningen.",
            "Integrera från q=0 till q=Q. Jämför gärna resultatet med formen W=(1/2)QV för en färdiguppladdad kondensatorliknande geometri.",
        ),
        self_checks=(
            "Energin ska vara proportionell mot Q²; byte av tecken på Q får inte ändra energin.",
            "Vid given Q ska ett större skal kräva mindre uppladdningsarbete eftersom potentialen blir lägre.",
        ),
        common_pitfall="Att använda slutpotentialen V(Q) för hela laddningen och skriva W=QV; då missar man att potentialen växer från noll under processen.",
    ),
    "ParallelPlateForceDistance": G(
        problem_id="4.2",
        learning_goal="Koppla den elektriska fältenergin eller det elektriska trycket till den mekaniska kraften mellan kondensatorplattor.",
        concepts=("elektriskt tryck", "plattkondensator", "kraft"),
        start_here="Bestäm först fältet mellan plattorna i termer av V och d. Därefter behöver du en relation mellan fältstyrka och kraft per area.",
        hints=(
            "För en stor plan luftkondensator utan randeffekter är E≈V/d.",
            "Det attraktiva elektriska trycket på en ledaryta kan skrivas p=(1/2)ε0E². Multiplicera med plattarean A för att få kraftens belopp.",
            "Sätt den givna kraften lika med detta uttryck och lös därefter efter avståndet d. Kontrollera vilken storhet som ligger under en kvadratrot.",
        ),
        self_checks=(
            "Vid samma spänning ska kraften öka kraftigt när plattavståndet minskar.",
            "Det sökta avståndet ska få längdenhet efter dimensionskontroll.",
        ),
        common_pitfall="Att använda F=QE med hela plattans laddning och hela fältet; en platta ska inte räknas som påverkad av sitt eget fält.",
    ),
    "CopperFoilLevitationEbonite": G(
        problem_id="4.3",
        learning_goal="Använd randvillkor mellan luft och dielektrikum för att koppla elektriskt tryck till tyngdkraft.",
        concepts=("dielektrikum", "elektriskt tryck", "kraftjämvikt"),
        start_here=(
            "Börja med kraftjämvikten på kopparblecket per area. Dess tyngd per area är ρCu t g. Vilket elektriskt tryck måste balansera detta?"
        ),
        hints=(
            "Det infinitesimala luftgapet är viktigt för kraften på kopparblecket: använd p=(1/2)ε0 E_luft² i gapet.",
            "Det finns ingen fri ytladdning i gränsen luft–ebonit, så den normala D-komponenten är densamma. Därför är E_luft=εr E_ebonit.",
            "Spänningsfallet över det infinitesimala luftgapet kan försummas. Skriv därför U≈E_ebonit d och kombinera detta med kraftjämvikten.",
        ),
        self_checks=(
            "E_luft ska vara större än E-fältet inne i eboniten när εr>1.",
            "Ett tjockare eller tätare kopparbleck ska kräva högre spänning för att sväva.",
        ),
        common_pitfall="Att använda E=U/d direkt som fältet i luftgapet; U/d beskriver i denna approximation främst fältet i eboniten.",
    ),
    "ThundercloudEnergyEstimate": G(
        problem_id="4.5",
        learning_goal="Göra en ordningsstorleksmodell av ett åskmoln som en plattkondensator och koppla genomslagsfält till laddning och energi.",
        concepts=("plattkondensator", "genomslagsfält", "fältenergi"),
        start_here="Modellera molnundersidan och marken som två stora motsatt laddade plattor. Börja med sambandet mellan ytladdningstäthet och fältet mellan plattorna.",
        hints=(
            "För två stora motsatt laddade plattor blir fältet mellan dem E=σs/ε0. Sätt E till det givna genomslagsfältet för uppskattningen.",
            "När σs är känd fås den totala laddningen från Q=σsA. Konvertera arean och fältstyrkan till SI innan du sätter in talen.",
            "Energin kan beräknas antingen som (1/2)QU med U=Eh eller från energitätheten (1/2)ε0E² multiplicerad med volymen Ah.",
        ),
        self_checks=(
            "De två energiberäkningarna ska ge samma resultat.",
            "Resultatet bör bli mycket stort jämfört med laboratoriekondensatorer; modellen omfattar en area på en kvadratkilometer.",
        ),
        common_pitfall="Att använda fältet från en ensam laddad platta, σs/(2ε0), trots att modellen innehåller två motsatt laddade ledarytor.",
    ),
    "CylindricalCapacitorDielectricPullIn": G(
        problem_id="4.6",
        learning_goal="Beräkna en dielektrisk indragningskraft genom hur kapacitansen ändras med inskjutningslängden.",
        concepts=("energimetod", "kapacitans", "dielektrisk kraft"),
        start_here=(
            "Inför en inskjutningslängd x. Fråga hur den totala kapacitansen ändras när en liten extra längd dx går från vakuum/luft till dielektrikum."
        ),
        hints=(
            "En koaxial kondensator har en kapacitans per längdenhet. Den redan fyllda delen och den ofyllda delen ligger elektriskt parallellt eftersom de har samma spänning mellan samma två ledare.",
            "Skriv C(x) som summan av bidraget från längden x med εr och resten med εr=1. Då blir dC/dx konstant.",
            "Spänningskällan är fortfarande ansluten, alltså är V0 konstant. Använd kraftrelationen F=(1/2)V0² dC/dx för rörelse i riktning mot ökande kapacitans.",
        ),
        self_checks=(
            "Kraften ska dra dielektrikumet längre in eftersom det ökar kapacitansen.",
            "I den idealiserade modellen blir kraften oberoende av hur långt cylindern redan är inskjuten, så länge ändeffekter försummas.",
        ),
        common_pitfall="Att använda energin (1/2)CV² och direkt derivera den som mekanisk potentiell energi utan att ta hänsyn till att spänningskällan utbyter energi med kondensatorn.",
    ),
    "PointChargeConductingPlane": G(
        problem_id="4.7",
        learning_goal="Använd spegelladdningsmetoden både för inducerad ytladdning och för kraften på en punktladdning.",
        concepts=("spegelladdning", "ledarvillkor", "inducerad ytladdning"),
        start_here=(
            "Ersätt först det jordade/utbredda ledande planet med den spegelladdning som ger V=0 i planet. Därefter kan samma konstruktion användas på två olika sätt i deluppgifterna."
        ),
        hints=(
            "Placera spegelladdningen −q på samma avstånd a på andra sidan planet. Fältet ovanför planet blir då identiskt med det verkliga fältet.",
            "För den inducerade ytladdningen: bestäm E_n precis ovanför planet och använd ρs=ε0E_n. Integrera sedan över en cirkelskiva med radie b i planet.",
            "För kraften på den verkliga kulan räcker det att beräkna Coulombkraften från spegelladdningen. Avståndet mellan q och −q är 2a.",
        ),
        self_checks=(
            "När b→∞ ska den integrerade inducerade laddningen gå mot −q.",
            "Kraften måste vara attraktiv och riktad mot planet oavsett tecknet på q.",
        ),
        common_pitfall="Att multiplicera kraften från spegelladdningen med två; spegelladdningen är redan konstruerad så att dess fält vid den verkliga laddningen ger rätt kraft.",
        visualization_note="Här kan en geometrisk bild av verklig laddning, spegelladdning och fältlinjer vara mer pedagogisk än en generell fältkarta.",
    ),

    # ------------------------------------------------------------------
    # Kapitel 5 – Strömmar och strömtäthet
    # ------------------------------------------------------------------
    "ConductiveCoaxialElectrodes": G(
        problem_id="5.1",
        learning_goal="Översätta det välkända koaxiala E-fältet till stationär ström genom ett ledande medium.",
        concepts=("Ohms lag i punktform", "koaxial geometri", "ström"),
        start_here="I stationärt tillstånd har problemet samma potentialgeometri som en koaxial kondensator. Sök därför först E(R) från den givna potentialskillnaden.",
        hints=(
            "Cylindersymmetrin ger E_R=C/R. Bestäm konstanten genom att integrera E från a till b och sätta potentialskillnaden till U.",
            "Använd därefter J=σE. Strömtätheten varierar alltså också som 1/R.",
            "Den totala strömmen fås genom en cylindrisk yta med radie R och längd ℓ: I=∫J·dS. R ska försvinna ur resultatet.",
        ),
        self_checks=(
            "Samma totalström måste passera varje koaxial cylinderyta i steady state.",
            "Om σ fördubblas vid samma U ska strömmen fördubblas.",
        ),
        common_pitfall="Att använda I=J gånger ett konstant tvärsnitt; den relevanta strömytan har arean 2πRℓ och J beror samtidigt på R.",
    ),
    "CoaxialCableLeakage": G(
        problem_id="5.2",
        learning_goal="Beräkna läckström och effektförlust genom ett resistivt koaxialt isolationsskikt.",
        concepts=("resistivitet", "koaxial resistans", "Joulevärme"),
        start_here="Behandla isolationen som ett koaxialt motstånd mellan innerledare och skärm, inte som en resistor med konstant tvärsnittsarea.",
        hints=(
            "För en tunn cylindrisk skiva med radie R och tjocklek dR går strömmen radiellt genom arean 2πRℓ. Skriv dR_el=ρ dR/(2πRℓ).",
            "Integrera från inner- till ytterradien. Om de givna storheterna är diametrar ändras båda med samma faktor 2, så kvoten b/a i logaritmen blir densamma.",
            "När den totala resistansen är känd används I=V/R och därefter P=VI eller V²/R.",
        ),
        self_checks=(
            "Längre kabel ska ge större läckström eftersom den erbjuder större ledande yta parallellt.",
            "Effekten måste vara positiv och uppfylla P=VI.",
        ),
        common_pitfall="Att använda R=ρℓ/A med kabelns längd som strömriktning; läckströmmen går radiellt genom isolationen.",
    ),
    "VariableSigmaCoaxialElectrolyte": G(
        problem_id="5.7",
        learning_goal="Hantera stationär ström när konduktiviteten varierar i rummet och koppla fältets divergens till fri rymdladdning.",
        concepts=("kontinuitet", "variabel konduktivitet", "Gauss lag"),
        start_here="Börja med strömkonservering, inte med J=σE. I steady state måste samma totala ström passera varje koaxial cylinderyta.",
        hints=(
            "Sätt J_R(R)=I/(2πRℓ). När σ(R)=k/R² används E_R=J_R/σ(R), vilket ger ett annat R-beroende än i ett homogent medium.",
            "Integrera E_R från a till b för att koppla I till den givna potentialskillnaden U och därmed få resistansen.",
            "Den fria rymdladdningen fås från ρ=∇·D=ε0εr∇·E. Använd divergensen av ett radiellt cylindriskt fält: ∇·(E_R R̂)=(1/R)d(RE_R)/dR.",
        ),
        self_checks=(
            "Trots att σ varierar ska ∇·J=0 i hela elektrolyten i steady state.",
            "Den resulterande laddningstätheten behöver inte vara noll; den behövs för att forma E så att J kan vara kontinuerlig.",
        ),
        common_pitfall="Att anta ρ=0 bara för att strömmen är stationär. Kontinuitet kräver ∇·J=0, inte nödvändigtvis ∇·E=0 när σ varierar.",
    ),
    "SemicylindricalRingResistor": G(
        problem_id="5.10",
        learning_goal="Beräkna resistans i en geometri där strömvägens längd beror på radien och olika radiala skikt ligger parallellt.",
        concepts=("cylindriska koordinater", "strömfördelning", "parallella strömvägar"),
        start_here="Betrakta en tunn remsa mellan R och R+dR. Den går från A till B längs en halvcirkel och kan ses som en egen resistor parallellt med alla andra remsor.",
        hints=(
            "Strömvägens längd för remsan är πR och dess tvärsnittsarea är h dR. Skriv remsans konduktans hellre än dess resistans.",
            "Alla remsor har samma potentialskillnad mellan ytorna A och B, så deras konduktanser ska adderas/integreras från a till b.",
            "Alternativt: potentialen ändras med vinkeln φ, så E_φ=U/(πR), J_φ=σE_φ och totalströmmen fås genom att integrera J över en radial snittyta.",
        ),
        self_checks=(
            "Större höjd h eller större konduktivitet σ ska minska resistansen.",
            "Radialintegralen ska ge en logaritm ln(b/a).",
        ),
        common_pitfall="Att behandla hela halvringen som en enda ledare med medelradie; strömmen delar sig mellan många parallella banor med olika längd.",
        visualization_note="En enkel tvärsnittsskiss med flera parallella halvcirkelformade strömvägar är mer informativ än en färgkarta över J.",
    ),
    "SteadyCurrentInterfaceCharge": G(
        problem_id="5.15",
        learning_goal="Kombinera stationär strömkontinuitet med elektrostatikens randvillkor för att hitta fri ytladdning i ett materialgränsskikt.",
        concepts=("randvillkor", "J=σE", "ytladdning"),
        start_here="Översätt först den givna J1 till E1 med J=σE. Därefter behöver normal- och tangentialkomponenterna behandlas med olika randvillkor.",
        hints=(
            "I steady state kan ingen laddning byggas upp obegränsat vid gränsen, så den normala strömkomponenten är kontinuerlig: J2n=J1n.",
            "Det stationära E-fältet är konservativt, därför är den tangentiella E-komponenten kontinuerlig: E2t=E1t. Detta bestämmer E2.",
            "Använd till sist ρs=D2n−D1n=ε0(ε2E2n−ε1E1n). Lägg märke till att den tangentiella komponenten inte kommer in i ρs.",
        ),
        self_checks=(
            "Om ε1/σ1 = ε2/σ2 ska den fria ytladdningen försvinna.",
            "β-komponenten i den givna J1 ska inte påverka den slutliga normala ytladdningen.",
        ),
        common_pitfall="Att sätta E_n kontinuerlig. I ett ledande steady-state-gränsskikt är det J_n som är kontinuerlig, medan E_n kan hoppa och skapa ytladdning.",
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
