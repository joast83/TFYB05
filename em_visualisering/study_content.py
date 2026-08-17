"""Student-facing problem text and pedagogical method metadata.

The problem statements are transcribed from the supplied TFYB05 problem collection.
The method labels and mathematical-focus descriptions are pedagogical metadata for the
study interface; they are not part of the original problem sheet.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MethodMeta:
    label: str
    rationale: str
    math_focus: str


CHAPTER_TITLES = {2: 'Coulombs lag, elektrisk fältstyrka och potential',
 3: 'Dielektriska material',
 4: 'Energi och kraft i elektrostatiska fält',
 5: 'Strömmar och strömtäthet',
 6: 'Biot–Savarts lag',
 7: 'Kraft, moment och magnetiskt flöde',
 8: 'Magnetiska material och magnetiska kretsar',
 9: 'Induktans och elektromotorisk spänning',
 10: 'Förskjutningsströmmar'}

METHOD_META = {    'force_balance': MethodMeta('Kraftjämvikt och vektorkomponenter', 'Identifiera alla krafter, välj axlar och projicera vektorer innan du sätter in fältformler.', 'Vektoruppdelning, projektioner, tecken och eventuella småparameterapproximationer.'),
    'direct_field_integral': MethodMeta('Direkt fältintegral / Biot–Coulomb-superposition', 'Parametrisera källan, skriv vektorn från källelementet till fältpunkten och integrera komponentvis.', 'Källkoordinat, separationsvektor, dℓ/dS/dV och komponentvis vektorintegral.'),
    'potential': MethodMeta('Potential först', 'Utnyttja att potentialen är en skalär: summera/integrera potentialbidrag och ta gradient först om E behövs.', 'Skalär integral, styckvisa uttryck, referensnivå och sambandet E = −∇V.'),
    'gauss': MethodMeta('Gauss lag och symmetri', 'Välj en sluten yta som följer problemets symmetri och håll noga reda på innesluten laddning eller fri laddning.', 'Ytnormaler, flödesintegral, symmetriargument och styckvis innesluten källa.'),
    'poisson_gauss': MethodMeta('Gauss/Poisson med randvillkor', 'Skriv fältekvationen i den naturliga koordinaten, integrera och bestäm integrationskonstanter från randvillkoren.', 'Divergens, en-dimensionell differentialekvation, integrationskonstanter och randvillkor.'),
    'superposition': MethodMeta('Superposition och geometrisk uppdelning', 'Bygg den verkliga källan som en summa av enklare källor vars fält eller potential du redan kan bestämma.', 'Geometrisk decomposition, vektorsumma/skalarsumma och konsekvent koordinatsystem.'),
    'optimization': MethodMeta('Dimensionering och optimering', 'Skriv först den fysikaliska begränsningen, eliminera en beroende storhet och optimera sedan den återstående funktionen.', 'Bivillkor, funktionsoptimering, derivata och kontroll av randfall.'),
    'dielectric_boundaries': MethodMeta('Randvillkor för E, D och material', 'Dela upp fälten i normal- och tangentialkomponenter och använd rätt kontinuitets- eller språngvillkor.', 'Normal-/tangentialuppdelning, skalärprodukter, enhetsnormaler och styckvisa materialrelationer.'),
    'energy_capacitance': MethodMeta('Energi, kapacitans och fälttryck', 'Bestäm först vad som hålls konstant (Q eller V) och uttryck energin eller trycket i den geometriska parameter som ändras.', 'Differentiation med avseende på geometri, energibalans och tydlig hantering av konstanta storheter.'),
    'image_charge': MethodMeta('Spegelladdningsmetoden', 'Ersätt ledarrandvillkoret med en fiktiv laddningskonfiguration som ger rätt potential på ledarytan.', 'Spegling i geometri, superposition och separationsvektorer till verkliga och fiktiva källor.'),
    'stationary_current': MethodMeta('Stationär ström: J = σE och kontinuitet', 'Utgå från att samma stationära ström måste passera relevanta ytor och koppla J till E via materialets konduktivitet.', 'Flödesintegral av J, differentialresistans, radial geometri och kontinuitet.'),
    'biot_savart': MethodMeta('Biot–Savarts lag', 'Parametrisera ledaren eller strömfördelningen och skriv dℓ × R-vektorn innan du integrerar.', 'Korsprodukt, parametrisering av kurva/yta, separationsvektor och komponentsymmetri.'),
    'magnetic_moment': MethodMeta('Magnetiskt moment och kraftmoment', 'Identifiera eller bygg det magnetiska momentet och koppla det till B-fältet och relevant korsprodukt.', 'Korsprodukter, vektorvinklar, riktning enligt högerhandsregeln och dipolapproximation.'),
    'magnetic_flux': MethodMeta('Magnetiskt flöde', 'Välj en lämplig yta och beräkna B·dS; byt yta om ∇·B = 0 gör en annan yta enklare.', 'Ytparametrisering, normalvektor, skalärprodukt och eventuella ytsubstitutioner.'),
    'magnetic_circuit': MethodMeta('Magnetisk krets / reluktans', 'Översätt geometrin till magnetomotorisk spänning, reluktanser och gemensamma eller förgrenade flöden.', 'Serie-/parallellkoppling, flödeskontinuitet och vid behov lösning av en icke-linjär algebraisk ekvation.'),
    'ampere_material': MethodMeta('Ampères lag för H och materialrelationer', 'Bestäm H från fri ström först; använd sedan materialrelationerna för att få B och M styckvis.', 'Cirkulationsintegral, styckvisa radialområden och separation mellan H, B och M.'),
    'magnetic_pressure': MethodMeta('Magnetiskt tryck och kraft', 'Gå från magnetiskt flöde till B i luftgapet och använd fältets energitäthet/tryck för den mekaniska kraften.', 'Area, flödestäthet, energitäthet och kraft som tryck gånger area.'),
    'magnetization_currents': MethodMeta('Magnetisering som bundna strömmar', 'Översätt M till volym- och ytmagnetiseringsströmmar eller använd B = μ0(H+M) där det är enklare.', 'Curl av M, korsprodukt M×n och orientering av cylindriska/sfäriska basvektorer.'),
    'mutual_inductance': MethodMeta('Ömsesidig induktans via flöde', 'Bestäm B från den ena kretsen, integrera flödet genom den andra och dividera flödeskopplingen med strömmen.', 'Ytintegral, geometri/projektion och definitionen M = Φ/I.'),
    'faraday_transformer': MethodMeta('Faradays lag och flödeskoppling', 'Bestäm först magnetiskt flöde från primärströmmen och derivera sedan NΦ med avseende på tiden.', 'Kedjeregel, tidsderivata, sinus/cosinus-fas och flödeskoppling.'),
    'motional_emf': MethodMeta('Rörelse-emk / Faradays lag / Lenz', 'Bestäm hur flödet ändras under rörelsen eller integrera v×B längs den rörliga ledaren; använd Lenz lag för riktningen.', 'Tidsberoende geometri, kedjeregel, linjeintegral av v×B och teckenkonvention.'),
    'ampere_maxwell': MethodMeta('Ampère–Maxwells lag och förskjutningsström', 'Koppla laddningskontinuitet till J och ∂D/∂t innan du drar slutsatser om det magnetiska fältet.', 'Divergens, tidsderivata, kontinuitetsekvation och vektorsymmetri.'),
}

METHOD_BY_ID = {'2.1': 'force_balance',
 '2.2': 'direct_field_integral',
 '2.3': 'direct_field_integral',
 '2.4': 'direct_field_integral',
 '2.5': 'potential',
 '2.6': 'gauss',
 '2.7': 'optimization',
 '2.8': 'superposition',
 '2.9': 'gauss',
 '2.10': 'superposition',
 '2.11': 'gauss',
 '2.12': 'gauss',
 '2.13': 'poisson_gauss',
 '2.16': 'potential',
 '2.18': 'energy_capacitance',
 '2.19': 'poisson_gauss',
 '3.1': 'superposition',
 '3.3': 'dielectric_boundaries',
 '3.6': 'gauss',
 '3.7': 'gauss',
 '3.9': 'dielectric_boundaries',
 '3.11': 'optimization',
 '3.12': 'dielectric_boundaries',
 '3.13': 'optimization',
 '3.14': 'dielectric_boundaries',
 '3.18': 'superposition',
 '3.19': 'dielectric_boundaries',
 '4.1': 'energy_capacitance',
 '4.2': 'energy_capacitance',
 '4.3': 'force_balance',
 '4.5': 'energy_capacitance',
 '4.6': 'energy_capacitance',
 '4.7': 'image_charge',
 '5.1': 'stationary_current',
 '5.2': 'stationary_current',
 '5.7': 'stationary_current',
 '5.10': 'stationary_current',
 '5.15': 'dielectric_boundaries',
 '6.1': 'biot_savart',
 '6.2': 'biot_savart',
 '6.3': 'biot_savart',
 '6.5': 'biot_savart',
 '6.8': 'biot_savart',
 '6.13': 'biot_savart',
 '7.1': 'magnetic_moment',
 '7.2': 'magnetic_moment',
 '7.3': 'magnetic_moment',
 '7.5': 'magnetic_moment',
 '7.6': 'magnetic_flux',
 '7.7': 'force_balance',
 '7.10': 'magnetic_flux',
 '8.1': 'magnetic_circuit',
 '8.2': 'magnetic_circuit',
 '8.4': 'magnetic_circuit',
 '8.5': 'ampere_material',
 '8.6': 'magnetic_pressure',
 '8.12': 'magnetization_currents',
 '8.13': 'magnetization_currents',
 '9.2': 'mutual_inductance',
 '9.4': 'mutual_inductance',
 '9.6': 'faraday_transformer',
 '9.13': 'motional_emf',
 '9.14': 'motional_emf',
 '10.2': 'ampere_maxwell',
 '10.3': 'ampere_maxwell'}

CHAPTER_METHOD_KEYS = {2: ['direct_field_integral', 'gauss', 'potential', 'superposition', 'optimization'],
 3: ['dielectric_boundaries', 'gauss', 'superposition', 'optimization'],
 4: ['energy_capacitance', 'image_charge', 'force_balance', 'gauss'],
 5: ['stationary_current', 'dielectric_boundaries', 'gauss', 'energy_capacitance'],
 6: ['biot_savart', 'gauss', 'superposition', 'direct_field_integral'],
 7: ['magnetic_moment', 'magnetic_flux', 'force_balance', 'biot_savart'],
 8: ['magnetic_circuit', 'ampere_material', 'magnetization_currents', 'magnetic_pressure'],
 9: ['mutual_inductance', 'faraday_transformer', 'motional_emf', 'magnetic_flux'],
 10: ['ampere_maxwell', 'gauss', 'stationary_current', 'magnetic_flux']}

PROBLEM_STATEMENTS = {'2.1': 'Två små kulor, vardera med massa m och laddning Q, är upphängda i var sin tunn tråd med längd ℓ. Båda '
        'trådarna är fästa i samma punkt. Härled ett uttryck för vinkeln mellan trådarna, α, förutsatt att α är liten.',
 '2.2': 'En tunn metalltråd har böjts till en ring med radie a. Ringen har tillförts en laddning Q som är jämnt '
        'fördelad över tråden. Ringen ligger i xy-planet med centrum i origo. Beräkna E-fältet längs z-axeln.',
 '2.3': 'En smal tråd har belagts med en konstant linjeladdningstäthet ρℓ . Dimensionen hos ρℓ är C/m. Tråden är rak '
        'med en total längd av a + b där a och b är positiva storheter. Det omgivande mediet är vakuum. '
        'Koordinatsystemets origo ligger på avstånd b från vänster ändpunkt och a från höger ändpunkt. ẑ-axeln går '
        'längs tråden och är positiv mot höger. Se figur nedan.\n'
        '\n'
        '(a) Beräkna det elektriska fältet E i punkten xx̂. Det vill säga i punkten (x, 0, 0).\n'
        '\n'
        '(b) Uttrycket i (a)-uppgiften förenklas betydligt om vi antar att x ≪ a och även x ≪ b. Beräkna detta '
        'gränsvärde genom att låta a och b gå mot oändligheten. (Observera att vi för den skull inte behöver anta att '
        'a = b.)',
 '2.4': 'Figuren illustrerar en halvcirkelformad yta som är gjord av ett isolerande material. På ytan har man lyckats '
        'fixera en ytladdningstäthet ρs som är konstant över hela ytan. Beräkna det elektriska fältet E i en punkt z '
        'ẑ det vill säga i en punkt på avståndet z rakt ovanför cirkelns medelpunkt. Halvcirkens radie är a.',
 '2.5': 'Ett sfäriskt skal med radie a har belagts med en laddning Q jämnt fördelad över ytan. Beräkna potentialen på '
        'olika avstånd från sfärens centrum. (Referens på oändligt avstånd.) Uppgiften kan lätt lösas med Gauss sats '
        'men det är intressant att se att vi kommer fram till samma resultat med hjälp av V (r) =\n'
        '\n'
        '⋆ avser källområdet. Det vill säga det område som innehåller laddning. Gedär ⊙ nomför denna räkning.',
 '2.6': 'Två långa koncentriska cylindrar med radie a respektive b, b > a, ges en ytladdningstäthet ρsa respektive ρsb '
        '. Bestäm elektriska fältstyrkan som funktion av avståndet R från cylindrarnas symmetriaxel.',
 '2.7': 'En kondensator består av två sfäriska koncentriska metallskal. Den yttre sfären har radien b = 1,0 m. Den '
        'elektriska fältstyrkan i luften mellan sfärerna får inte överstiga Emax = 2,0·106 V/m. Hur stor skall radien '
        'hos den inre sfären vara för att man skall kunna lägga så stor spänning som möjligt över kondensatorn? '
        'Beräkna även denna maximala spänning.',
 '2.8': 'Två koncentriska sfäriska metalliska skal har radierna a respektive b. Den inre sfärens laddning är Qa medan '
        'den yttre sfären har laddningen Qb .\n'
        '\n'
        '(a) Beräkna potentialen V (r) där r mäter avståndet från sfärernas centrum. (Referenspunkten ligger på '
        'oändligt avstånd.)\n'
        '\n'
        '(b) Sfärerna sätts ett ögonblick i ledande förbindelse med varandra. Ange laddningsfördelningen på skalen '
        'sedan kontakten brutits.',
 '2.9': 'Vid ett visst tillfälle är det luftelektriska fältet vertikalt nedåtriktat och är vid jordytan 300 V/m medan '
        'det på 1400 m höjd är 20 V/m. Beräkna hur stor den elektriska laddningen är i genomsnitt per volymsenhet '
        'under 1400 m höjd.',
 '2.10': 'Ett isolerande material är format till ett klot i vilket ett sfäriskt hålrum gjorts. Det sfäriska hålrummet '
         'har sitt centrum på avståndet d från klotets centrum. Hålrummets radie är a och klotets radie är b där b > '
         '(a + d). Det isolerande materialet innehåller en konstant rymdladdningstäthet ρ. Beräkna den elektriska '
         'fältstyrkan E på x-axeln för x > b. Se figur. Tips: Superposition.',
 '2.11': 'Spänningen U har lagts över två långa koaxiella cylindriska skal med radierna a och b, b > a. Beräkna '
         'beloppet av den elektriska fältstyrkan mittemellan skalen.',
 '2.12': '(a) Under normala förhållanden fungerar luft som en mycket god isolator för elektriska fältstyrkor upp till '
         'ett visst värde, Emax . För större E fungerar luft som en ledare. Bestäm den maximalt tillåtna laddningen, '
         'Qmax , på en sfärisk ledare med radien a placerad i luft. Bestäm även sfärens potential, Vmax , i detta '
         'fall.\n'
         '\n'
         '(b) Beräkna Qmax och Vmax då Emax = 3 · 106 V/m och a = 10 cm.',
 '2.13': 'I ett urladdningsrör består katoden av en cylinder med radie a = 1,0 mm och längd ℓ = 40 mm. Anoden är en '
         'lika lång cylinder, som ligger koaxiellt och har radien b = 4,0 mm. Katodens potential är noll, anodens U = '
         '300 V. Om man antar att det elektronmoln som finns mellan katod och anod bildar en i rummet likformigt '
         'fördelad laddning (konstant rymdladdningstäthet), hur stor är då hela denna rymdladdning, när elektriska '
         'fältstyrkan vid katodens yta är noll?',
 '2.16': 'I ett sfäriskt område, med radie a, finns en laddningstäthet ρ(r) = A · (a − r) där r mäter avståndet från '
         'centrum. Utanför detta område det vill säga för r > a är ρ = 0. Enheten för ρ är C/m3 . Beräkna potentialen '
         'i sfärens centrum, det vill säga för r = 0, då referenspunkten ligger på oändligt avstånd.',
 '2.18': 'Två kondensatorplattor med arean A = 500 cm2 ligger på ett avstånd d0 = 10 mm från varandra. De laddas upp '
         'så att potentialskillnaden blir U = 200 V varefter batteriet kopplas bort.\n'
         '\n'
         '(a) Hur stor är vardera plattans laddning?\n'
         '\n'
         '(b) Vid oförändrad laddning på plattorna förs en oladdad metallplatta, med tjocklek d1 = 6 mm in mellan dem. '
         'Vad blir då potentialdifferensen?\n'
         '\n'
         '(c) Om vi, i stället för att föra in plattan med tjocklek d1 , ökar avståndet till d2 = 30 mm, vilken blir '
         'då potentialdifferensen?',
 '2.19': 'Två kondensatorplattor på avståndet d har mellan sig en likformigt fördelad laddning med tätheten ρ0 . Den '
         'ena plattan är jordad och den andra har potentialen\n'
         '\n'
         '(a) Beräkna var mellan plattorna den elektriska fältstyrkan E är noll.\n'
         '\n'
         '(b) Beräkna villkoret på V0 för att E skall vara noll någonstans mellan plattorna.',
 '3.1': 'En HCl-molekyl ligger i origo med H+ -jonen i punkten z = d/2 och Cl− -jonen i z = −d/2. Avståndet d = 0,218 '
        'Å. Beräkna det elektriska fältets storlek i punkter på avståndet r0 = 10 Å längs z- respektive y-axlarna.',
 '3.3': 'En plattkondensator där avståndet mellan plattorna är 1 cm, hålles laddad med spänningen 10 kV. En 0,5 cm '
        'tjock porslinsskiva med relativ permittivitet 6 är inskjuten mellan plattorna. Beräkna E och D, dels i '
        'porslinet, dels i luften mellan plattorna.',
 '3.6': 'Ett sfäriskt plåtskal av försumbar tjocklek har radien 3a. En ledande kula med radien a befinner sig mitt i '
        'skalet och mellanrummet är fyllt med ett ämne med relativ permittivitet εr = 2,5. Genom en liten öppning i '
        'skalet är den inre sfären jordad via en fin metalltråd. På den yttre sfären ligger laddningen Q. Vad är '
        'förhållandet mellan den del av Q som befinner sig på plåtskalets utsida och den del som befinner sig på dess '
        'insida? Vi bortser från trådens och öppningens störande inverkan på fältet och räknar med sfärisk symmetri. '
        '(Med jordad menas att den har samma potential som en mycket avlägsen punkt.)',
 '3.7': 'En volym som begränsas av två koncentriska sfärer med radierna a och b är fylld med ett material med relativ '
        'permittivitet εr och konstant rymdladdningstäthet ρ0 . Beräkna fältstyrka och potential som funktion av '
        'radien. I områdena r < a och r > b har vi vakuum.',
 '3.9': 'Två koncentriska ledande sfärer med yttre och inre radien b respektive a är laddade med laddningarna −Q '
        'respektive +Q. Området mellan skalen är fyllt med två olika dielektrikum med de relativa permittiviteterna ε1 '
        'och ε2 . Se figur. Beräkna E och D i området mellan skalen. (Att E-fälten är riktade i radiell riktning '
        'behöver inte bevisas utan kan förutsättas.)',
 '3.11': 'Man skall tillverka en plattkondensator med kapacitansen 100 pF som skall tåla en spänning av 50 kV. Mellan '
         'metallplattorna lägger man därför ett antal skikt av 0,10 mm tjock makrofol. Makrofol är en isolator med '
         'relativ permittivitet εr = 3,0 och en genomslagsfältstyrka av 200 kV/mm.\n'
         '\n'
         '(a) Hur många skikt makrofol krävs minst för att uppfylla ovanstående krav?\n'
         '\n'
         '(b) Hur stora måste de vara till ytan? Plattmellanrummet antas helt utfyllt av makrofolen.',
 '3.12': 'En cylinderkondensators belägg består av två koaxiella metallcylindrar, den inre med en ytterradie av a = '
         '2,0 cm och den yttre med en innerradie av c = 5,0 cm. Kondensatorn har två lika tjocka koaxiella '
         'isolationslager som helt fyller mellanrummet. Deras relativa permittivitet är ε1 = 4,0 och ε2 = 3,0 räknat '
         'inifrån och utåt. Beräkna kondensatorns kapacitans per längdenhet.',
 '3.13': '(a) Vilken är den högsta tillåtna spänningen över en plattkondensator med plattavståndet 10 mm då det är '
         'luft med genomslagshållfastheten 3 · 106 V/m i mellanrummet?\n'
         '\n'
         '(b) Samma fråga som ovan men med plexiglas mellan plattorna. Plexiglas: Genomslagshållfasthet 20 · 106 V/m '
         'och relativ permittivitet εr = 3.\n'
         '\n'
         '(c) Samma fråga igen men med en 9 mm tjock plexiglasskiva och resten luft mellan plattorna.',
 '3.14': 'I en stor plattkondensator är avståndet mellan plattorna d. Den övre plattan har potentialen V0 , V0 > 0, '
         'och den undre plattan har potentialen noll. På den undre plattan lägges ett 0,8d tjockt dielektrikum med '
         'relativ permittivitet εr . Bestäm:\n'
         '\n'
         '(a) Beloppen av E- och D-fälten i luften och i dielektrikumet.\n'
         '\n'
         '(b) Ytladdningstätheten av fria laddningar på metallplattorna.\n'
         '\n'
         '(c) Ytpolarisationsladdningstätheten på dielektrikumets ytor.',
 '3.18': 'En cylinderformad volym, med radie a och höjd h, består av en elektret med polarisation P = P ẑ där P är '
         'konstant inuti volymen. Se figur.\n'
         '\n'
         '(a) Beräkna E-fältet längs hela symmetriaxeln, det vill säga z-axeln.\n'
         '\n'
         '(b) Beräkna D-fältet längs samma axel.\n'
         '\n'
         '(c) Vad blir de approximativa uttrycken för E och D om a ≫ h?\n'
         '\n'
         '(d) Hur skulle beskrivningen i (c)-uppgiften ändrats om vi inte haft en elektret utan i stället två ytor med '
         'fri ytladdningstäthet, ρs = P vid z = h och ρs = −P vid z = 0?',
 '3.19': 'Ett gränsskikt mellan två medier går längs ett plan som är parallellt med z-axeln men skär x-axeln i punkten '
         'ax̂ och y-axeln i punkten bŷ. Konstanterna a och b är positiva. Se figur. Medium ⃝, 1 som är det som '
         'innehåller origo, utgörs av en perfekt ledare medan medium ⃝ 2 är ett perfekt dielektrikum. Med perfekt '
         'dielektrikum menar vi ett material som är linjärt, har relativ permittivitet εr , är en perfekt isolator, σ '
         '= 0, och inte innehåller någon fri laddningstäthet, ρ = 0.\n'
         '\n'
         'På metallytan ligger dock en ytladdningstäthet av fria laddningar, ρs . Beräkna Doch E-fälten i en punkt '
         'omedelbart utanför metallytan.',
 '4.1': 'Hur stort arbete åtgår för att ladda ett tunt, sfäriskt ledande skal med radie a till laddningen Q?',
 '4.2': 'En plan luftkondensator med plattarea A = 50 cm2 laddas upp till en spänning av V = 450 V. Hur stort skall '
        'avståndet mellan plattorna, d, vara för att en kraft F = 0,05 N skall fordras för att dra isär dem?',
 '4.3': 'En horisontell ebonitplatta med tjocklek d = 2 cm och relativ permittivitet εr = 5 är metalliserad på '
        'översidan. Under plattan placeras ett kopparbleck med tjocklek t = 0,1 mm. Hur stor måste spänningen mellan '
        'kopparblecket och det övre belägget vara för att kopparblecket ska bli hängande utan stöd? Koppars densitet '
        'är ρCu = 8,9 g/cm3 Räkna med ett infinitesimalt tjockt luftlager mellan kopparbleck och ebonitplatta.',
 '4.5': 'Vi gör en uppskattning av mängden laddning, |Q|, och elektrostatisk energi, We , i ett normalt åskväder genom '
        'följande räkning. Nedre delen av åskmolnet ses som en ledande yta med arean A = 1 km2 . På denna yta antas '
        'molnets laddning, −Q, samlad. Den underliggande markytan, även den med area A = 1 km2 , ses på samma sätt som '
        'en ledare med en laddning +Q. Molnets underdel ligger på höjden h = 200 m över marken. Luftens '
        'genomslagshållfasthet är Emax = 20 000 V/cm.\n'
        '\n'
        '(a) Beräkna den totala laddningen Q i åskmolnet.\n'
        '\n'
        '(b) Beräkna den totala energin We .',
 '4.6': 'En cylinderkondensator består av två långa koaxiella metallrör med radier a = 3 cm och b = 5 cm. Rören är '
        'kopplade till en likspänningskälla som ger dem en potentialskillnad V0 = 1 kV. En lång hålcylinder med '
        'relativ permittivitet εr = 8 är instucken en bit i kondensatorn. Hålcylindern passar precis in i mellanrummet '
        'mellan metallrören. Med hur stor kraft söker kondensatorn suga in hålcylindern?',
 '4.7': 'En liten laddad kula hänger på avståndet a ovanför ett ledande plan med stor utsträckning. Kulans laddning är '
        'q.\n'
        '\n'
        '(a) Beräkna hur mycket laddning som induceras i planets ytskikt inom ett avstånd b, b > a, från kulan.\n'
        '\n'
        '(b) Hur mycket laddning får vi totalt i hela planet?\n'
        '\n'
        '(c) Med vilken kraft påverkas kulan av planet?',
 '5.1': 'Mellan två långa koaxiella cylindriska elektroder med längd ℓ och vilkas radier är a respektive b, b > a, och '
        'vilka hålles vid en potentialskillnad U , hälles en vätska med konduktiviteten σ. Beräkna den elektriska '
        'strömstyrkan genom vätskan.',
 '5.2': 'En koaxialkabel med längd ℓ = 150 cm består av en innerledare med diameter a = 1,0 mm och en ytterledare med '
        'innerdiameter b = 4,0 mm. Utrymmet mellan inner- och ytterledaren är fyllt med ett isolationsmaterial som '
        'ursprungligen hade mycket hög resistivitet. Av misstag har kabeln kommit att uppvärmas kraftigt varvid '
        'isoleringsmaterialets resistivitet sjunkit till i medeltal ρ = 5,0 · 106 Ωm. Den optimistiske användaren '
        'fortsätter dock att utnyttja kabeln som förut, det vill säga för att transportera likström vid V = 120 V '
        'spänningsfall mellan innerledare och skärm.\n'
        '\n'
        '(a) Beräkna den totala läckströmen genom kabelns isolation.\n'
        '\n'
        '(b) Beräkna den totala effekt som läckströmmen i isolationen alstrar.',
 '5.7': 'Mellanrummet mellan två koaxiella metallcylindrar, radie a respektive b, b > a, är fyllt med en elektrolyt. '
        'Elektrolyten har en relativ permittivitet εr som är oberoende av radien R. Ledningsförmågan, σ(R), varierar '
        'dock enligt σ(R) = k/R2 där k är en konstant. Cylindrarnas längd är ℓ.\n'
        '\n'
        '(a) Beräkna resistansen mellan cylindrarna.\n'
        '\n'
        '(b) Beräkna laddningstätheten, ρ(R), av fria laddningar i elektrolyten om potentialskillnaden mellan '
        'metallcylindrarna är U .',
 '5.10': 'Ett motstånd har formen av en halv cylindrisk ring med innerradie a, ytterradie b och höjden h. Se figur. '
         'Materialet i motståndet har konduktiviteten σ. Uppskatta motståndets resistans, det vill säga resistansen '
         'från ytan A till ytan B i figuren. Vi antar att strömmen går i tangentiell riktning, det vill säga att J = J '
         '· ϕ̂, och att J enbart beror av avståndet till z-axeln.',
 '5.15': 'Ett gränsskikt mellan två medium går längs yz-planet. Medium ⃝, 1 x < 0, och medium ⃝, 2 x > 0, är inte '
         'perfekta dielektrikum som i uppgift 3.20, utan karakteriseras av ε1 och σ1 respektive ε2 och σ2 . Vi kan '
         'alltså ha strömmar genom medierna. Vi antar dock att steady-state, fortvarighetstillstånd, råder. Det vill '
         'säga att alla strömmar och laddningstätheter är tidsoberoende. Antag att strömtätheten för x = 0− är J 1 = '
         'αx̂ + β ŷ.\n'
         '\n'
         '(a) Beräkna ytladdningstätheten av fria laddningar, ρs , i ytskiktet.\n'
         '\n'
         '(b) Vilket samband måste gälla mellan materialkonstanterna för att vi inte skall få någon fri '
         'ytladdningstäthet i ytskiktet?',
 '6.1': 'En sluten krets består, till en del, av en rät ledare med längd 2L. Strömmen går i positiv z-riktning. Se '
        'figur. Vi söker bidraget till magnetiska flödestätheten, B, från den räta ledaren då fältpunkten är belägen i '
        '(R cos ϕ, R sin ϕ, z)T i kartesiska koordinater.\n'
        '\n'
        '(a) Beräkna B via Biot-Savarts lag. Ange även gränsvärdet för B då L → ∞.\n'
        '\n'
        '(b) Beräkna B via B = ∇ × A det vill säga genom att först beräkna A. För att undvika alltför mycket algebra '
        'är det tillåtet att sätta z = 0 innan operationen B = ∇ × A utförs.\n'
        '\n'
        '(c) Låt den räta ledaren vara oändligt lång redan från början. Beräkna B med hjälp av cirkulationssatsen.',
 '6.2': 'En kvadratisk slinga med sida a ligger i xy-planet enligt figuren. Slingans centrum är beläget i origo.\n'
        '\n'
        '(a) Bestäm B-fältet längs hela z-axeln om slingan för strömmen I medurs relativt positiv ẑ-riktning.\n'
        '\n'
        '(b) Beräkna ett numeriskt värde på B-fältet i kvadratens mittpunkt då sidan a = 3,0 m och strömmen I är 10 A.',
 '6.3': 'En lång, rak, tunn, strömförande ledare är böjd i rät vinkel och ligger i horisontalplanet. Beräkna till '
        'storlek och riktning den magnetiska flödestätheten 5 cm ovanför böjen om strömstyrkan är 5 A.',
 '6.5': 'Ett långt, rakt och tunt metallband med bredden 2a genomflytes av strömmen I. Beräkna magnetiska '
        'flödestätheten i en punkt på avståndet 2a från bandets mittlinje. Strömmen antas vara jämt fördelad över '
        'bandets bredd.\n'
        '\n'
        '(a) Dels i bandets plan.\n'
        '\n'
        '(b) Dels i ett mot bandet vinkelrätt plan genom mittlinjen.',
 '6.8': '(a) En ledningstråd ligger i xy-planet enligt figur. Tråden som för strömmen I, är alltså sammansatt av tre '
        'delar. Två av dem är räta ledare. Magnetiska flödestätheten från sådana har vi beräknat i uppgift 6.1 så dom '
        'bryr vi oss inte om. Din uppgift är att beräkna det B-fält som den krökta delen orsakar i en godtycklig punkt '
        'på z-axeln. Den krökta delen består av en kvarts cirkelbåge med radie a. Observera att B är en vektor som kan '
        'ha flera komposanter. Ge svaret med hjälp av det koordinatsystem som definieras i figuren.\n'
        '\n'
        '(b) Vad blir B-fältet i en punkt på z-axeln om slingan utgörs av en hel cirkel med radie a?',
 '6.13': 'En tunn cirkulär skiva av ett elektriskt isolerande material är på ena sidan uppladdad med en konstant '
         'ytladdningstäthet ρs . Skivan, vars radie är a, roterar med vinkelhastigheten ω kring sin egen axel. Bestäm '
         'magnetiska flödestätheten på skivans axel som funktion av avståndet från skivans plan.',
 '7.1': 'En elektron med laddning −e och hastighet v rör sig i en cirkelbana med radie a. Cirkeln ligger i xy-planet. '
        'Vilket magnetiskt dipolmoment ger rörelsen upphov till?',
 '7.2': 'En cirkulär strömförande slinga med radie a är placerad i ett homogent magnetfält B = B x̂. Slingans plan '
        'sammanfaller med xy-planet. Slingan genomflyts av strömmen I i positiv omloppsriktning relaterad till '
        'z-riktningen.\n'
        '\n'
        '(a) Beräkna det vridande momentet, T , med avseende på slingans centrum genom att summera bidragen dT = r × '
        'dF .\n'
        '\n'
        '(b) Kontrollera att du får samma resultat med det uttryck för kraftmomentet som ges på formelbladet, T = m × '
        'B.\n'
        '\n'
        '(c) Kontrollera att vridningsriktningen är den du förväntar dig. Det magnetiska momentet kan liknas vid en '
        'magnetnål med nordände vid vektorns spets.',
 '7.3': 'Två små spolar har samma magnetiska moment m = m · ẑ, där m = 1 Am2 . Ortsvektorn mellan dem, r, har längden '
        '1 m och bildar vinkeln θ = 45◦ med zriktningen. Bestäm beloppet av det vridande momentet på någon av '
        'spolarna.',
 '7.5': 'Den magnetiska flödestätheten från en cirkulär trådslinga med radien a och strömmen I kan för a ≪ r, där r är '
        'avståndet från slingan, approximeras med ett dipolfält. Beräkna hur långt ut på symmetriaxeln man måste gå '
        'för att dipolfältet skall avvika med mindre än 1 % från det rätta värdet.',
 '7.6': 'Vid ett tillfälle i jordens historia antas hela området söder om 70◦ sydlig bredd vara täckt av ett 1000 m '
        'högt islager med lodrät randyta. Beräkna hur stort magnetiskt flöde som passerar genom isen ut i luften. '
        'Jordens magnetiska moment antas riktat rakt söderut och ha storleken m = 0,824 · 1023 Am2 . Jordradien rJ = '
        '637 mil.',
 '7.7': 'En rak horisontell koppartråd med strömtätheten J = J · x̂, där J = 3,0 A/mm2 , befinner sig i ett homogent '
        'magnetfält, B = B · ŷ. Hur stort skall B vara för att den magnetiska kraften skall kompensera tyngdkraften? '
        'Koppars densitet ρCu = 8,9 g/cm3 . Tyngdkraften verkar i negativ z-riktning.',
 '7.10': 'En oändlig rät ledare ligger längs x-axeln och för strömmen I i positiv riktning. Se figur. En rektangulär '
         'trådslinga, som består av ett varv, är belägen i planet z = c. Rektangeln har utsträckningen a i x-led och b '
         'i y-led. Rektangelns hörn ligger alltså i punkterna (0, 0, c), (a, 0, c), (a, b, c) och (0, b, c). Beräkna '
         'det magnetiska flöde som strömmen I orsakar genom slingan.',
 '8.1': 'En permanentmagnet med längd ℓ = 20 cm har böjts så att den bildar en praktiskt taget sluten ring. Luftgapets '
        'längd är d = 1 mm. Magnetmaterialets egenskaper beskrivs av tabellen. H( A/m) -5000 -4000 -3000 -2000\n'
        '\n'
        '(a) Hur stor magnetisk flödestäthet bör man få i luftgapet? Läckage försummas.\n'
        '\n'
        '(b) För att förstärka magnetiska flödestätheten i luftgapet lindar man en spole med 100 varv på '
        'permanentmagneten. Vilken flödestäthet bör man få om strömmen',
 '8.2': 'En magnetisk krets, se figur, är tillverkad av ett järnämne med tvärsnitt S = 2 cm² och total längd ℓ = 0,5 '
        'm. Luftgapets längd d = 1 mm. Genom lindningen, N = 100 varv, går strömmen I = 2,0 A. Sambandet mellan B-fält '
        'och H-fält ges av B = aH/(b + H), som gäller för H > 0, där a = 2,0 T och b = 400 A/m med B och H i '
        'SI-enheter. Beräkna B-fältet i luftgapet. Läckning försummas.',
 '8.4': 'En magnetisk krets består av en järnring med medeldiameter 15,0 cm och tvärsnittsarea 1,20 cm2 . Längs en '
        'diameter, se figur, löper en brygga av samma material men med tvärsnittsarea 0,80 cm2 . På den ena ringhalvan '
        'finns en spole med 160 varv som för strömmen 2,00 mA. Järnmaterialets relativa permeabilitet är 150. Beräkna '
        'hur stort magnetiskt flöde som går genom bryggan.',
 '8.5': 'Ett cylindriskt rör, med innerradie a och ytterradie b, för strömmen I i längdriktningen. Beräkna '
        'magnetiseringen M , magnetiska fä1tstyrkan H samt magnetiska flödestätheten B på olika avstånd, R, från '
        'rörets symmetriaxel.\n'
        '\n'
        '(a) Röret består av koppar som är omagnetiskt.\n'
        '\n'
        '(b) Röret består av järn vars magnetiska egenskaper antas vara linjära och beskrivas av en relativ '
        'permeabilitet µr .',
 '8.6': 'En hästskoformad permanentmagnet har försetts med ett ankare av mjukjärn, se figur. Såväl ankare som '
        'permanentmagnet har tvärsnittsarea S = 2,8 cm2 . Man känner inte de magnetiska egenskaperna hos vare sig '
        'permanentmagnet eller ankare men det magnetiska flödet i kretsen har uppmätts till Φ0 = 3,0 · 10−4 Wb. Med '
        'hur stor kraft dras permanentmagnet och ankare samman?',
 '8.12': 'En cylindrisk volym, med radie a och höjd h, består av en permanentmagnet med magnetisering M = M ẑ. M är '
         'konstant inuti volymen.\n'
         '\n'
         '(a) Beräkna B-fältet längs z-axeln. Fältpunkt i z ẑ.\n'
         '\n'
         '(b) Beräkna H-fältet längs z-axeln.\n'
         '\n'
         '(c) Vad blir de approximativa uttrycken för B och H då a blir mycket stor?',
 '8.13': 'Figuren illustrerar en lång cylindrisk ledare som för strömmen I i positiv z-riktning. Radien är a och '
         'strömmen antas jämnt fördelad över ledarens tvärsnitt. Metallmaterialets magnetiska ϕ̂ egenskaper beskrivs '
         'av en konstant relativ permeabilitet µr .\n'
         '\n'
         '(a) Beräkna de magnetiseringsströmtätheter som uppträder i ledaren och på dess yta.\n'
         '\n'
         '(b) Visa att den totala magnetiseringsström som uppträder i z-riktningen är noll.',
 '9.2': 'Figuren till höger illustrerar två slingor. Slinga 1 består av två parallella oändliga räta ledare. Eftersom '
        'dessa tänkes bilda en sluten krets bör de föra samma ström men i motsatta riktningar. Avståndet mellan '
        'ledarna är d. Slinga 2 utgörs av omkretsen √ till en kvadrat, med sidan d/ 2, som är orienterad enligt '
        'figuren. Kvadratens hörn tangerar alltså slinga 1 men utan att det bildas elektrisk kontakt. Beräkna den '
        'ömsesidiga induktansen mellan slingorna.',
 '9.4': 'Figuren illustrerar två envarviga cirkulära strömslingor som har en gemensam axel. Slingornas radier är a '
        'respektive b där a ≪ b. Avståndet mellan dem är d där d ≫ a. I detta fall har vi möjlighet att beräkna ett '
        'approximativt värde på ömsesidiga induktansen, M , på två olika sätt.\n'
        '\n'
        '(a) Betrakta den lilla strömslingan som ett magnetiskt dipolmoment, m, vars B-fält approximativt ges på '
        'formelbladet.\n'
        '\n'
        '(b) Antag att det B-fält som den stora slingan orsakar i den lilla är konstant över den lilla slingans yta.',
 '9.6': 'På en sluten järnkrets ligger två lindningar. Den ena, med N1 varv, för strömmen I1 . Den andra, som är '
        'öppen, har N2 varv. Vad blir spänningen över den senare lindningens ändar om strömmen i den första lindningen '
        'är i1 (t) = I0 cos(ωt)? Järnkretsens medellängd är ℓ och dess tvärsnitt S. Materialets relativa permeabilitet '
        'är µr .',
 '9.13': 'Hur stort arbete, W , krävs för att flytta den kvadratiska slingan med konstant hastighet, v = 10 m/s, från '
         'läge A till läge C? Förflyttningen sker genom område B där vi har ett konstant magnetfält, B = 1 T. Slingans '
         'resistans är RΩ = 0,05 Ω. ℓ = 30 cm a = 10 cm',
 '9.14': 'En magnetisk dipol m = mẑ är belägen i origo. På stort avstånd, z > 0, från dipolen rör sig en liten '
         'cirkulär slinga med hastigheten v längs z-axeln. Slingans radie är a ≪ z och dess plan har ẑ som '
         'normalriktning. (Slingans centrum ligger hela tiden på z-axeln och hastigheten v räknas positiv då slingan '
         'avlägsnar sig från origo.) Vi kan beräkna den elektromotoriska spänning som uppstår i slingan på två olika '
         'sätt.\n'
         '\n'
         '(a) Vi beskriver situationen med hjälp av ett koordinatsystem som följer med slingan. Slingan är då orörlig '
         'medan dipolen tycks avlägsna sig med hastigheten v. Detta ger ett tidsvarierande B-fält genom slingan. '
         '(Hastigheten v är konstant.)\n'
         '\n'
         '(b) Vi håller fast vid det koordinatsystem som är givet i texten och beräknar elektromotoriska spänningen '
         'för en rörlig slinga. Notera gärna likheten i räkningarna med beräkningen av ömsesidig induktans i uppgift '
         '9.4 och fundera på hur man skulle kunna använda det resultatet för att lösa denna uppgift.',
 '10.2': 'En plattkondensator matas med en tidsvarierande ström i(t) = I₀ sin(ωt). Plattornas area är A och avståndet '
         'mellan dem d. Mellan plattorna har vi vakuum. Beräkna förskjutningsströmtätheten J_F ≡ ∂D/∂t genom '
         'kondensatorn. Vi bortser från randeffekter.',
 '10.3': 'Ett intressant test av Maxwells ekvationer är följande tankeexperiment. Vi fogar samman en mängd positiv '
         'laddning så att vi får ett laddat klot. I ett visst ögonblick släpper vi laddningarna fria. Den inbördes '
         'repulsionen bör leda till att laddningarna strömmar radiellt ut från symmetricentrum. Vi får alltså en tids '
         'och rumsberoende laddningstäthet ρ(r,t), där r mäter avståndet till centrum. Eftersom vi har laddningar i '
         'rörelse förväntar vi oss att en magnetisk flödestäthet, B, skall uppträda. Vi antar att laddningarna rör sig '
         'i vakuum.\n'
         '\n'
         '(a) Avgör, utan att göra några direkta beräkningar, vilken riktning B-fältet bör ha. Använd symmetriargument '
         'och argument baserade på någon fundamental egenskap hos B-fältet.\n'
         '\n'
         '(b) Försök att hitta ett B-fält som uppfyller Maxwells ekvationer. Tips: Beräkna strömtätheten J(r,t) och '
         'förskjutningsströmtätheten uttryckta i laddningstätheten ρ(r,t).'}


def problem_id_from_name(name: str) -> str:
    """Return the leading chapter.problem token from a registered problem name."""
    return name.split(maxsplit=1)[0]


def chapter_number(problem_id: str) -> int:
    return int(problem_id.split(".", 1)[0])


def statement_for_problem(problem) -> str:
    return PROBLEM_STATEMENTS.get(problem_id_from_name(problem.name), problem.description)


def method_key_for_problem(problem) -> str:
    pid = problem_id_from_name(problem.name)
    return METHOD_BY_ID[pid]


def method_meta_for_problem(problem) -> MethodMeta:
    return METHOD_META[method_key_for_problem(problem)]


def method_options_for_problem(problem) -> tuple[str, ...]:
    pid = problem_id_from_name(problem.name)
    chapter = chapter_number(pid)
    correct = method_key_for_problem(problem)
    keys = list(CHAPTER_METHOD_KEYS.get(chapter, ()))
    if correct not in keys:
        keys.insert(0, correct)
    return tuple(dict.fromkeys(keys))


def method_label(method_key: str) -> str:
    return METHOD_META[method_key].label
