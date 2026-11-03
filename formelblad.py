"""Show the three original formula-sheet pages from the course booklet."""

from pathlib import Path

import streamlit as st


st.title("Formelblad")
st.caption("Ur Problemsamling för elektromagnetism, E. Peter Münger, september 2024. "
           "Originalets tre sista sidor, med formler, integraler och koordinatsystem.")

assets = Path(__file__).resolve().parent / "assets"
sheet = (assets / "formelblad.pdf").read_bytes()
st.download_button("Ladda ner formelbladet (PDF)", sheet, file_name="formelblad.pdf",
                   mime="application/pdf")
for page in range(1, 4):
    st.image((assets / f"formelblad-{page}.svg").read_text(encoding="utf-8"),
             caption=f"Formelblad · sida {page} av 3", width="stretch")
