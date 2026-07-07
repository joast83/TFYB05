# EM-visualiseringar – web version

This package contains a Streamlit wrapper around the original Tkinter/Matplotlib code. The web version renders the right-hand 3-D panel with Plotly/WebGL so users can rotate, zoom and pan the 3-D views directly in the browser.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Deploy on Streamlit Community Cloud

1. Create a GitHub repository.
2. Upload all files in this folder to the repository root.
3. Go to Streamlit Community Cloud and create a new app from your repository.
4. Set the main file path to `streamlit_app.py`.
5. Deploy.

The required Python packages are listed in `requirements.txt`, including `plotly` for browser-interactive 3-D views.

## Deploy on Render

Use these settings for a Web Service:

- Build command: `pip install -r requirements.txt`
- Start command: `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0`

## Notes

The original desktop entry point still exists:

```bash
python -m em_visualisering
```

For web hosting, use `streamlit_app.py`, not the original Tkinter GUI.

## Interactive 3-D implementation

The original problem classes still define `draw_3d(fig, params, mode)` using Matplotlib-style calls. In the Streamlit app, `em_visualisering.plotly_bridge.make_plotly_3d_figure(...)` captures those calls and converts surfaces, lines, scatter points, arrows and simple 3-D boxes into Plotly traces. The desktop Matplotlib/Tkinter entry point remains unchanged.
