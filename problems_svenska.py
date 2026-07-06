"""Startfil för den modulära svenska EM-visualiseraren.

Kör med:
    python problems_svenska.py

Alternativt, från samma katalog:
    python -m em_visualisering
"""

from em_visualisering.app import ElectrostaticsApp


def main():
    app = ElectrostaticsApp()
    app.mainloop()


if __name__ == "__main__":
    main()
