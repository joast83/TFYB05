# TFYB05 pedagogy redesign – implementation of ideas 1–8

Copy the contents of this folder directly into the root of the TFYB05 repository.

Files:
- `streamlit_app.py` — replacement student interface.
- `em_visualisering/study_content.py` — problem statements plus method/mathematics metadata.
- `tests/test_streamlit_app.py` — replacement Streamlit UI tests for the new workflow.
- `tests/test_study_content.py` — coverage tests for the 65 registered exercises.
- `em_visualisering/guidance.py` — included unchanged from the all-65 hint version for convenience.

Implemented redesign ideas:

1. **Solve is the default mode.** Parameter controls, rendering quality and graph controls are absent.
2. **Actual problem text is shown.** Statements are transcribed from the supplied problem collection rather than using visualization-oriented `description` fields.
3. **Physics and mathematics are separated.** Each exercise shows its physics concepts and the mathematical move being trained.
4. **Help can be requested by type.** Students can say whether they are stuck on method choice, setup, vector/geometry reasoning, or checking.
5. **Self-checks require an active prediction first.** The authored check is gated until the student writes their own expectation.
6. **Explore requires a prediction before revealing figures.**
7. **Visualizations are pruned.** Only exercises whose authored guidance says a figure is useful are recommended for visualization. Other legacy plots require an explicit override, and 3-D is advanced/optional.
8. **Answer checking is separate from exploration.** A student must mark that they have a completed attempt before revealing the app's analytical/numerical control result.

The new sidebar is intentionally small in Solve mode: work mode, chapter and problem.

Notes:
- The problem statements come from the supplied 2024 problem collection. Figure-heavy exercises use the app's geometry sketch as a clean companion diagram.
- The answer section currently uses the repository's existing `result_summary()` and `physics_check()` functions. It is deliberately described as the app's control result rather than pretending to reproduce the printed facit verbatim.
- Existing plotting/problem implementation files are not changed by this package.


## v2.1: enklare självkontroll och förutsägelse

De obligatoriska fritextfälten har tagits bort.

- **Kontrollera ditt resultat** består nu av separata, stängda kontrollpunkter. Studenten kan tänka själv och sedan öppna dem som extra ledtrådar.
- **Utforska** uppmanar fortfarande studenten att göra en mental förutsägelse före figuren, men kräver inte att något skrivs in.
- Den obligatoriska reflektionsrutan efter figuren är borttagen. I stället visas en kort uppmaning att jämföra figuren med den egna förutsägelsen.
- Principen är: be studenten tänka, men kräv inte textinmatning om programmet inte faktiskt kan tolka eller ge meningsfull återkoppling på texten.


## v2.2: riktigt facit i stället för app-kontroll

- Den tidigare sektionen **Facit / kontroll** är borttagen.
- `result_summary()` och `physics_check()` används inte längre som ersättning för facit i studieläget.
- Varje av de 65 registrerade uppgifterna har nu ett **Visa facit**-fält med slutresultatet från den tryckta problemsamlingens facit.
- Facit är avsiktligt kort: det ger slutresultatet men inte en fullständig lösningsgång.
- Appens numeriska/analytiska kontroll finns kvar enbart under **Utforska → Avancerat**, där den tydligt märks som appens egen beräkning och inte kursfacit.
- De pedagogiska **Kontroll 1/2**-punkterna behålls separat som extra ledtrådar för symmetri, tecken, dimensioner och gränsfall.
