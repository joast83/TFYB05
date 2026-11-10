# Beteckningar i studiehjälpen

Använd den enskilda uppgiftens beteckningar för givna storheter. När en
hjälpstorhet behövs, definiera den där den används. Normalisera inte en
bokstav globalt: i 5.2 är ρ resistivitet medan ρ i 5.7 är laddningstäthet.

Referens: *Problemsamling för elektromagnetism*, bifogad utgåva,
formelbladet (PDF-sida 79) samt uppgifter och facit i kapitel 2–10.
Särskilt tydliga jämförelser är 2.3–2.4, 3.14, 5.15, 7.2–7.3,
8.13 och 10.2–10.3.

| Storhet | Beteckning | Viktig skillnad |
| --- | --- | --- |
| Vektor, enhetsvektor | $\overline{E}$, $\hat{r}$ | Belopp och komponenter saknar överstreck. |
| Linje- och ytladdningstäthet | $\rho_\ell$, $\rho_s$ | Skilj C/m och C/m² från volymtäthet i C/m³. |
| Polarisationsladdning | $\rho_p$, $\rho_{sp}$ | Volym: minus divergensen av P. Yta: P:s komponent längs materialets utåtnormal. |
| Konduktivitet | $\sigma$ | I 5.15 förekommer både konduktiviteten och den fria ytladdningstätheten. |
| Magnetiseringsström | $\overline{J}_m$, $\overline{J}_{sm}$ | Volym (A/m²) respektive yta (A/m). |
| Kraftmoment | $\overline{T}$ | Momentbeloppet skrivs T. |
| Elektromotorisk spänning | $\varepsilon_{\mathrm{ems}}$ | Skilj från permittivitet. Vid flera varv deriveras flödeskopplingen. |
| Förskjutningsströmtäthet | $\overline{J}_F$ | Tidsderivatan av D; i 10.2 är fältet homogent över plattarean A. |

Överstreck används i de satta vektorekvationerna. I löptext utan
matematiksättning används vanliga bokstäver och läsbara index.
När samlingen använder ε₁ och ε₂ för relativa permittiviteter gäller
ε = ε₀ εᵣ för den absoluta permittiviteten. Behåll uppgiftens val av U
eller V för spänning och ange referens/riktning när tecknet spelar roll.

## Matematik i ledtrådar och riktad hjälp

Samma standard gäller för alla kapitel, även uppställningshjälp,
vektor-/geometrihjälp, resultatkontroller och vanliga fel:

- Skriv matematiska uttryck i LaTeX. Använd `$...$` för korta symboler,
  komponenter och villkor i en mening. Skriv inte exempelvis `E_r=Q/(4πε0r²)`
  som vanlig text.
- Lägg centrala uppställningar, integraler och längre bråk i egna `$$`-block
  med tomma rader före och efter. Introducera formeln med en kort mening och
  förklara efteråt vad studenten ska sätta in eller lösa ut.
- Samla relaterade ekvationer i `aligned`, en ekvation per rad. Använd `cases`
  för områdesvisa storheter. Dela långa summor och integraler i flera rader
  i stället för att rada upp allt horisontellt.
- Behåll uppgiftens symboler. Skilj vektorer från belopp/komponenter och
  integrationsvariabel från observationskoordinat. Skriv differentialer
  med `\mathrm d`, funktioner med exempelvis `\sin` och `\ln`, och svenska
  ord i index med `\text{...}`.
- Använd råa Python-strängar (`r"""..."""`) för LaTeX så att `\frac`,
  `\theta` och liknande inte blir kontrolltecken. Lämna ett mellanslag efter
  kommandon när nästa faktor är en bokstav: `\rho_\ell L`, inte `\rho_\ellL`.
- Lägg inte in en ekvation bara för att fylla en kvot. En rent geometrisk
  eller begreppslig ledtråd kan vara vanlig text. Behåll de progressiva
  stegen och undvik att visa ett senare lösningssteg för tidigt.

Exempel: 2.4 visar hur en källintegral byggs upp; 2.8 visar samma läsordning
för Gauss lag, innesluten laddning och en styckvis potentialintegral.
Kontrollera både matematikblock och omgivande text vid ändringar;
`tests/test_universal_display_math.py` täcker alla 65 uppgifternas hjälpfält.

## Integralform som gemensam utgångspunkt

Startlagar och lösningsvägledning använder Gauss lag som flöde genom en
sluten yta och Ampères lag som cirkulation längs en sluten kurva. Behåll
integralformen även när laddnings- eller strömtäthet söks: jämför flödet
med den inneslutna laddningen, eller cirkulationen med strömmen genom ytan.
Ange yta/kurva, normalriktningar och symmetri innan integralen förenklas.
För ett skal bidrar både den yttre och den inre manteln, med motsatta tecken.

Samma arbetssätt gäller bundna laddningar och magnetiseringsströmmar samt
laddningsbevarande och Ampère–Maxwells lag. Tidsderivator i induktion och
förskjutningsström behövs fortfarande. Derivator för potentialer (uttryckligen
begärda i 6.1), geometriska normaler och optimering är separata beräkningssteg;
de innebär inte att Gauss eller Ampères lag byts till differentialform.
Originaluppgifter och det reproducerade formelbladet behåller originaltexten.
