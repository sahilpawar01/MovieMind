# MovieMind (Streamlit)

Streamlit app that serves movie recommendations generated from pre-computed similarity scores. The build focuses on keeping only the files required at runtime so the repository stays lightweight for cloud deployments (Render, etc.).

## Runtime Artifacts

Only the following files are necessary to run the service:

- `app.py` – Streamlit UI plus inference logic.
- `movie_list.pkl` – metadata (movie ids, titles).
- `similarity.pkl` – cosine similarity matrix created offline.
- `requirements.txt` – Python dependencies for the app layer only.
- `render.yaml` – Render blueprint (optional but recommended).
- `README.md` – this guide.

Everything else (raw CSVs, notebooks, virtual environments, setup scripts for other platforms) is excluded by `.gitignore` so they never reach the Git remote.

## Local Development

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Add TMDB credentials (needed for posters):
   ```bash
   set TMDB_API_KEY=your_key
   set TMDB_BEARER_TOKEN=your_bearer_token
   ```
   You can also place them in `.streamlit/secrets.toml`.
3. Run the app:
   ```bash
   streamlit run app.py
   ```

## Deploying on Render

1. Commit only the runtime files listed above.
2. Push to GitHub (example remote: `https://github.com/sahilpawar01/MovieMind.git`).
3. In Render, choose **New > Blueprint** and point to the repo. Render will pick up `render.yaml` and provision a Python web service with:
   - Build: `pip install --upgrade pip && pip install -r requirements.txt`
   - Start: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
4. Add the environment variables `TMDB_API_KEY` and `TMDB_BEARER_TOKEN` in Render → Environment.
5. Trigger the first deploy. Subsequent pushes to `main` will redeploy automatically.

## Credits

Original model pipeline inspired by Prashant Kumar / CampusX materials. This repo only contains the assets required to serve the recommender.
