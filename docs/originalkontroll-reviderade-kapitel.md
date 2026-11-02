# Originalkontroll: reviderade uppgifter i kapitel 2–9

**Källa:** E. Peter Münger, *Problemsamling för ELEKTROMAGNETISM*, september 2024.
PDF-version 2024-09-05 (versionscommit `0cbda46b9260c9ee2a9f321502f940f8d17ad181`).
Jämförelsen gjordes mot PDF-filen som användaren bifogade, inklusive de tryckta facitsidorna. **PDF-binären finns ännu inte i GitHub-repot**; se även `docs/kallgranskning-kapitel2.md`.

## Omfattning

Alla **63 registrerade och reviderade uppgifter** i kapitel 2–9 har jämförts med originalets problemtext och tryckta facit. Alla tal, givna enheter, deluppgifter, centrala samband och slutresultat har kontrollerats i dessa uppgifter. Originalfigurerna har särskilt granskats där de avgör källans orientering/geometri (2.10, 6.2, 6.8, 9.2, 9.13). Att en slutformel stämmer med det tryckta facit är **inte ett bevis på att originalfacit är felfritt**.

| Kapitel | Registrerade uppgifter som kontrollerats | Original-PDF: uppgifter | Original-PDF: facit |
| --- | --- | --- | --- |
| 2 | 2.1–2.13 (registrerade), 2.16, 2.18, 2.19 – 16 st | 9–12 | 13–14 |
| 3 | 3.1, 3.3, 3.6, 3.7, 3.9, 3.11–3.14, 3.18, 3.19 – 11 st | 15–19 | 20–22 |
| 4 | 4.1–4.3, 4.5–4.7 – 6 st | 23–24 | 25 |
| 5 | 5.1, 5.2, 5.7, 5.10, 5.15 – 5 st | 26–29 | 30–31 |
| 6 | 6.1–6.3, 6.5, 6.8, 6.13 – 6 st | 32–35 | 36–37 |
| 7 | 7.1–7.3, 7.5–7.7, 7.10 – 7 st | 38–40 | 41 |
| 8 | 8.1, 8.2, 8.4–8.6, 8.12–8.13 – 7 st | 42–46 | 47–48 |
| 9 | 9.2, 9.4, 9.6, 9.13, 9.14 – 5 st | 49–53 | 54–55 |

Kapitel 10 är **inte** med eftersom det ännu inte hade genomgått samma revision vid denna kontroll.

## Rättningar gjorda efter kontrollen

- **8.1 (PDF s. 42, facit s. 47):** återställd komplett fempunkts B–H-tabell och den saknade spolströmmen **2,0 A**. Originalet definierar `ℓ=20 cm` som **permanentmagnetens längd**; beräkningsmodell, lastlinje, parameteretikett, vägledning och test använder nu `H_m ℓ + B d/μ₀ = NI` i stället för `H_m(ℓ−d) + B d/μ₀ = NI`. Detta ger ungefär 0,794 respektive 0,901 T, förenligt med tryckt facit 0,8 och 0,9 T.
- **8.5 (PDF s. 43):** återställde ordet *fältstyrkan* där en etta hade ersatt bokstaven l.
- **8.13 (PDF s. 46):** tog bort ett lösryckt `ϕ̂` ur brödtexten; symbolen tillhör en koordinataxel i figuren.
- **9.2 (PDF s. 49, facit s. 54):** återställde kvadratens sida till `d/√2`. En felplacerad rot hade gjort tidigare uppgiftstext missvisande; fysikmodellen hade redan rätt geometri.
- **9.13 (PDF s. 51, facit s. 54):** återställde tydligt `a=10 cm` och `ℓ=30 cm` samt figurhänvisningen. Det är två olika storheter. Den geometriska vyn i appen behöver fortsatt jämföras visuellt med originalfiguren före slutpublicering.
- **Metoder:** skillnaden mellan Coulombs lag, Biot–Savarts lag, Ampères cirkulationslag och vektorpotential tydliggjordes. Det generiska och fysiskt oklara namnet *Biot–Coulomb-superposition* togs bort; dipolapproximationen i 7.5 fick ett eget metodnamn.

## Avvikelser och gränsfall som medvetet dokumenteras i facit

- **6.2 (PDF s. 32, facit s. 36):** uppgiften skriver *medurs* relativt positiv z-riktning, men det tryckta facit ger **positivt z-riktat B**. Standardhögerhandsregeln ger negativ z-riktning för medurs ström sedd från +z. Både originaltexten och den tryckta formeln har därför behållits, med en explicit varning i appfacit. Kodens positiva strömriktning motsvarar moturs från +z.
- **7.5 (PDF s. 38, facit s. 41):** det tryckta facit anger `12,2 a`. För att uppfylla det strikta villkoret **mindre än 1 %**, med felet relativt det exakta axiella fältet, krävs `|z|/a > 12,257622...`. Det tryckta värdet finns kvar, med en förklaring av avrundningsbegränsningen.
- **8.2 (PDF s. 47):** den tryckta texten beskriver den bortvalda algebraiska roten som *negativ magnetisk flödestäthet i järnmaterialet*. Det är en missvisande beskrivning. Den bortvalda roten ligger ovanför parametern `a` i `B=aH/(b+H)` och ger `H<0`, utanför den givna materiallagens villkor `H>0`. Detta var redan förtydligat i appfacit före denna PR.
- **2.19 (PDF s. 12, facit s. 14):** originalfacit har ett icke-strikt olikhetsvillkor, som inkluderar nollpunkter på plattornas ytor. För ett nollställe *strikt mellan* plattorna gäller strikt olikhet (med icke-noll homogen rymdladdning); vägledningen särskiljer redan dessa fall.

## Tidigare originalkontroll som nu bekräftats

- **2.5:** originalets integral är över källområdet och använder `dQ′`. Den omformulering som gjordes i PR #22 är fysikaliskt och källmässigt korrekt.
- **2.10:** hålrummets centrum ligger vid `x=−d`, och därför ingår `(x+d)²` i fältuttrycket.
- **2.18:** del (c) görs *i stället för* del (b); laddningen bevaras eftersom batteriet har kopplats bort.

## Kvarvarande begränsning

Denna kontroll är en systematisk jämförelse mot originalets uppgiftstexter och tryckta facit, med riktade fysikaliska gränsfallskontroller. Den utgör inte en oberoende nyhärledning av samtliga 63 lösningar eller en fullständig visuell certifiering av varje genererad figur. Riktad hjälp och pedagogisk progression ingår i ett separat framtida projekt och har inte omarbetats här, utöver den nödvändiga rättningen av faktauppgifterna i 8.1.
