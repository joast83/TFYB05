"""Progressiv studievägledning för övningsuppgifter i TFYB05.

Målet är att hjälpa studenten att välja rätt fysikalisk idé och matematisk
representation utan att omedelbart visa en fullständig lösning. Ledtrådarna är
ordnade från konceptuell startpunkt till den avgörande uppställningen. De första
posterna täcker de uppgifter från kapitel 2 och 3 som redan finns registrerade i
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
