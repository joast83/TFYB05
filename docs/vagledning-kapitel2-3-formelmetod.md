# Formelbaserad vägledning i kapitel 2–3

Granskningen omfattar samtliga 27 registrerade uppgifter i kapitel 2 och 3.
Utgångspunkten är undervisningens arbetsordning:

1. Skriv den allmänna lag eller definition som behövs.
2. Identifiera dess storheter, källor, koordinater och randvillkor från uppgiften.
3. Sätt in dem, förenkla med den symmetri som faktiskt finns och lös ekvationen.
4. Kontrollera och tolka resultatet med tecken, enheter och gränsfall.

Symmetri är fortfarande ett nödvändigt beräkningssteg när ett fält ska tas ut
ur en Gaussintegral. Den får inte antas för en ändlig tråd eller för ett helt
klot med ett förskjutet hålrum. För direkt källintegration kan komponenternas
symmetri också bekräftas efter att integralen ställts upp.

## Genomgång

| Uppgifter | Start och beräkningsväg |
| --- | --- |
| 2.1 | Kraftjämvikt och Coulombs lag → krafter och laddningsavstånd → komponentekvationer → småvinkelapproximation. |
| 2.2–2.4 | Bevarad integralmetod från PR #27: fältintegral → dQ′, r−r′, avstånd och integrationsgränser → komponentintegraler. |
| 2.5 | Bevarad potentialintegral från PR #27, med skalets ytelement och separat behandling av inre/yttre observationspunkter. |
| 2.6 | Gauss lag → cylindrisk mantel/ändytor → innesluten ytladdning i tre områden → E. |
| 2.7, 2.12 | Gauss lag → sfäriskt fält → genomslagsvillkor → potentialintegral; i 2.7 därefter optimering. |
| 2.8 | Gauss lag → styckvis innesluten laddning → fält och potentialintegral → laddningsbevarande och lika potential vid kontakt. |
| 2.9 | Gauss lag med givna fält → signerat flöde → laddning per volym. |
| 2.10 | Superposition och Gauss lag för vardera hjälpsfären → laddningar och separata centrumavstånd → vektorsumma. |
| 2.11 | Gauss lag → cylindriskt fält med okänd laddning → given spänning bestämmer konstanten. |
| 2.13, 2.19 | Differentialformen av Gauss lag → symmetrianpassad ekvation → integration och randvillkor. |
| 2.16 | Potentialintegral → volymladdningselement och avstånd till centrum → vinkel- och radialintegration. |
| 2.18 | Gaussbox och potentialintegral → initial Q → bevarad Q och luftgapens spänningsfall. |
| 3.1 | Coulombs vektorsumma → signerade laddningar och separationsvektorer → komponenter → eventuell dipolapproximation. |
| 3.3, 3.13, 3.14 | Gauss lag för D, materiallag och potentialintegral → skiktdata → fält; därefter genomslag eller yt-/polarisationsladdningar. |
| 3.6, 3.7 | Gauss lag för D → fria laddningar och olika permittiviteter → potentialintegral med jordning/gemensam referens. |
| 3.9 | Gauss lag och tangentiellt E-randvillkor → två hemisfäriska flödesbidrag → E och respektive D. |
| 3.11 | Spänningsintegral och genomslagsvillkor → helt antal skikt → Gaussbox, materiallag och C=Q/U för arean. |
| 3.12 | Cylindrisk Gaussyta för D → materiallag → två spänningsintegraler → kapacitans per längd. |
| 3.18 | Bundna laddningar från P → skivornas dQ′ och separationsvektorer → fältintegraler → D och plan gräns. |
| 3.19 | Normal-/tangentialrandvillkor → enhetsnormal från planet → D och E. |

De tidigare kontrollerna av tecken, enheter, randfall och fysiska begränsningar
behålls. Matematisk riktad hjälp följer samma väg som ledtrådarna. Symmetri är
inte i sig en felaktig startmetod; två formuleringar i 2.2 och 2.4 som kunde
uppfattas så har justerats.

## Geometripaneler

Appens separata geometriskisser tas bort för alla uppgifter, både i
lösningsläget och i det dolda utforskningsläget. Huvudgrafen i utforskningsläget
får hela bredden. Textbaserad hjälp om koordinater och geometri finns kvar.
Hänvisningar till borttagna appskisser i 6.2, 7.5, 7.7 och 9.2 har gjorts
självständiga. Originaluppgifternas figurhänvisningar har inte skrivits om.

## Omfattning och validering

Detta är en omarbetning av lösningsvägledningen, inte en ny original-PDF-kontroll.
Uppgiftstexter, tryckt facit och beräkningsmodeller ändras inte. PR #27:s
integralregressioner behålls. Appens gemensamma tester kontrollerar riktad hjälp
för alla 65 uppgifter och att geometripanelen saknas. Separata exempel från
kapitel 2, 3 och 9 kontrollerar att huvudgrafer fortfarande kan öppnas utan
geometripanel. Dessa tester verifierar appbeteende, inte pedagogisk kvalitet.
