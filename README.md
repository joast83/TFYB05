# TFYB05 – EM-studiehjälp

Ett svenskt studiestöd för elektromagnetism med 65 registrerade uppgifter i
kapitel 2–10, stegvisa ledtrådar, facit och interaktiva visualiseringar.
Webbgränssnittet är byggt med Streamlit. Ett separat Tkinter-program finns för
lokal utforskning av uppgifternas grafer och geometri.

## Kom igång

Du behöver Python 3.10 eller senare. Kör följande från en terminal:

```bash
git clone https://github.com/joast83/TFYB05.git
cd TFYB05
python -m venv .venv
```

Aktivera miljön på macOS/Linux:

```bash
source .venv/bin/activate
```

På Windows, i PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Installera och starta webbappen från projektets rot:

```bash
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

Öppna adressen som Streamlit skriver i terminalen, normalt
<http://localhost:8501>. Stoppa servern med `Ctrl+C`.

## Använd webbappen

Välj arbetssätt i sidofältet. På en smal skärm öppnar du sidofältet med pilen
uppe till vänster.

- **Lös uppgift** är startläget. Välj kapitel och uppgift, gör ett eget försök och
  öppna frivilliga ledtrådar, kontrollpunkter eller **Visa facit** efter behov.
  Facit visar slutresultatet, inte en fullständig lösning.
- **Utforska** visar uppgifternas modeller. Öppna **Parametrar för utforskning**,
  ändra värden och tryck **Applicera parametrar**. Välj sedan **Visa figur**.
  Vissa uppgifter kräver att du väljer **Visa den äldre visualiseringen ändå**.
  Den roterbara 3D-vyn ligger under **Avancerat**. Appens interna beräkning är
  separat från kursens facit.
- **Teori** innehåller fristående modeller med förklaringar och råd om hur de
  används i uppgifter. Inställningarna uppdaterar modellerna direkt.

### Teorimodeller

| Avsnitt | Vad du kan undersöka |
| --- | --- |
| Gauss flödessats | Innesluten laddning, lokalt flöde och totalflöde genom en sfär |
| Stokes sats i magnetostatik | Ampères lag, innesluten ström och orientering |
| Elektrisk potential och fält | Superposition, ekvipotentialer och sambandet E = −∇V |
| Randvillkor mellan dielektrika | Tangentiellt E, normalt D och fri ytladdning |
| Biot–Savarts lag | Högerhandsregeln, slingans axialfält och segmentbidrag |
| Faradays och Lenz lag | Flödesändring, inducerad emk och riktning |

I Gauss testlabb är startläget en laddning på +5 nC i origo. Med mus kan du
lägga till eller ta bort laddningar genom att klicka på rutnätspunkter. På
pekskärm använder du **Placera med koordinater (mobil / tangentbord)**;
tryck i Plotly-figuren visar punktinformation men ändrar inte laddningarna.
Koordinater avrundas till rutnätets steg på 0,25 m.

Modellerna använder fasta referensskalor för att parameterändringar ska synas.
Vissa färgskalor mättas och vissa pilar har komprimerade längder; läs respektive
figurs förklaring och numeriska värden. Det är idealiserade modeller, inte
allmänna fältlösare. En punktladdning precis på Gaussytan är exempelvis ett
singulärt gränsfall.

## Lokalt skrivbordsprogram

```bash
python -m em_visualisering
```

`python problems_svenska.py` fungerar också som kompatibel startfil.
Skrivbordsprogrammet kräver Tkinter och en grafisk skrivbordsmiljö. Kontrollera
Tkinter-installationen med `python -m tkinter`. Om modulen saknas behöver du
installera Tk-stödet för din Python-version; på Debian/Ubuntu finns paketet
`python3-tk`. Webbappen behöver inget grafiskt skrivbord.

Välj uppgift och visningsläge, ändra parametrar och tryck **Rita** eller Enter.
Beräkningarna använder SI-enheter; val av visningsenhet konverterar värdet och
kontrollens gränser. Skrivbordsprogrammet har uppgiftsvisualiseringarna, medan
studieflödet och teorisidorna finns i webbappen.

## Utveckling och verifiering

Installera projektet med testberoenden i din aktiverade virtuella miljö:

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
```

Testsviten kontrollerar bland annat parameterkontrakt, enhetskonvertering,
registrerade uppgifters standardvärden, Matplotlib- och Plotly-figurer,
beräkningssammanfattningar, kursinnehåll samt Streamlit-flöden. Tkinter-testen
kontrollerar enhetslogiken utan att öppna ett fönster och hoppas över om
Tkinter inte är installerat.

För en snabb kontroll av enbart teorifigurerna:

```bash
python smoke_test_theory.py
```

Testerna ersätter inte visuell kontroll. Efter gränssnittsändringar: starta
webbappen, kontrollera standardlägen och parameterändringar på både breda och
smala skärmar och prova laddningsredigering med mus respektive koordinater.

GitHub Codespaces använder `.devcontainer/devcontainer.json`, installerar
projektets testberoenden och startar webbappen på vidarebefordrad port 8501.
För Streamlit Community Cloud är startfilen `streamlit_app.py` och
beroendena finns i `requirements.txt`.

## Projektstruktur

| Fil eller katalog | Ansvar |
| --- | --- |
| `streamlit_app.py` | Webbgränssnitt, parametertillstånd och renderingscache |
| `em_visualisering/app.py` | Tkinter-gränssnitt |
| `em_visualisering/problems/ch02.py` … `ch10.py` | Uppgifternas fysikmodeller och figurer |
| `em_visualisering/registry.py` | Registrering av uppgifter |
| `em_visualisering/core.py` | Gemensam problemklass, konstanter och ritfunktioner |
| `em_visualisering/parameters.py`, `parameter_catalog.py`, `unit_scaling.py` | Validering, kontrollmetadata och visningsenheter |
| `em_visualisering/study_content.py`, `guidance.py`, `facit.py` | Uppgiftstexter, metodstöd, ledtrådar och facit |
| `em_visualisering/theory_pages.py` | Teorimodeller och deras gränssnitt |
| `em_visualisering/plotly_bridge.py` | Plotly-återgivning av uppgifternas 3D-vyer |
| `tests/` | Automatiserade kontroller |

### Lägga till eller ändra en uppgift

1. Följ en befintlig problemklass i rätt kapitelmodul. Använd SI-enheter i
   modellens beräkningar och definiera meningsfulla standardvärden och validering.
2. Registrera uppgiften i `registry.py` och kontrollera dess lägen i `modes.py`.
3. Lägg till parameterinformation i `parameter_catalog.py` där det behövs.
4. Lägg till uppgiftstext, vägledning och facit i respektive innehållsmodul.
5. Kör testsviten och kontrollera uppgiften i gränssnittet. Kontrollera nya
   formler och gränsfall separat; en figur som renderas är inte i sig ett bevis
   för att fysiken är korrekt.

`pyproject.toml` beskriver paketet och utvecklingsberoendena. Håll dess
körberoenden och `requirements.txt` samstämmiga när beroenden ändras.
