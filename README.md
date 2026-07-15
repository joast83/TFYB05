# TFYB05 – interaktiva EM-visualiseringar

En Streamlit- och Tkinter-applikation för visualisering av elektrostatik,
magnetostatik och relaterad teori. Alla fysikberäkningar använder SI-enheter,
medan gränssnitten kan visa praktiska enheter som nC, µC, mm och cm.

## Funktioner

- 65 registrerade övningsproblem med 2-D-graf, geometriskiss och 3-D-vy.
- Interaktiv Plotly/WebGL-vy i Streamlit.
- Enhetsväljare med korrekt konvertering till och från SI.
- Metadataanpassade talfält, linjära reglage, logaritmiska reglage och valfält.
- Separata utkast och applicerade parametrar så att figurer inte räknas om vid varje ändring.
- Export av parametrar till JSON/CSV samt figurer till PNG/HTML.
- Gemensam validering, renderingskontroller och automatiska tester.
- Teorisidor för Gauss flödessats och Stokes/Ampères lag.

## Kör webbappen lokalt

```bash
python -m venv .venv
```

Aktivera miljön:

```bash
# Linux/macOS
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Installera och starta:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Streamlit Community Cloud

1. Ladda upp innehållet i denna mapp till roten av GitHub-repot.
2. Skapa en ny app i Streamlit Community Cloud.
3. Ange `streamlit_app.py` som appens huvudfil.
4. Starta deploymenten.

`requirements.txt` och `pyproject.toml` använder samma versionsintervall för att
förhindra att en för gammal Streamlit-version installeras.

## Desktopversion

```bash
python -m em_visualisering
```

Desktopversionen kräver ett grafiskt skrivbord med Tk-stöd.

## Tester

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
```

GitHub Actions kompilerar koden och kör testsviten på Python 3.10, 3.11 och 3.12.

## Projektstruktur

```text
streamlit_app.py                 Webapp
em_visualisering/app.py          Tkinter-app
em_visualisering/core.py         Basmodell och ritverktyg
em_visualisering/parameters.py   Parameter- och valideringsmetadata
em_visualisering/parameter_catalog.py
em_visualisering/unit_scaling.py
em_visualisering/problems/       Övningsproblem per kapitel
em_visualisering/theory_pages.py Interaktiva teorisidor
tests/                           Automatiska tester
```
