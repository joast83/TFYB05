"""Starta programmet med: python -m em_visualisering"""

from .app import ElectrostaticsApp


def main():
    app = ElectrostaticsApp()
    app.mainloop()


if __name__ == "__main__":
    main()
