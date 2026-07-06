# EM-visualiseringar – web version

This package contains a Streamlit wrapper around the original Tkinter/Matplotlib code.

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

The required Python packages are listed in `requirements.txt`.

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
