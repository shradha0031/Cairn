# Cairn

**Safe routes across the red planet.**

Cairn is a walking map for Mars crews. It compares routes across Jezero Crater and highlights the point where a crew must turn back to return safely.

## Project status

Steps 1-7 are complete: the React/Vite frontend and FastAPI backend are scaffolded, the Leaflet map uses a real Mars Trek imagery base with clearly labelled synthetic overlays, the backend generates fallback elevation/slope/hazard grids, the app compares three route candidates, calculates return safety, displays science/emergency stops, and provides an optional mission briefing with a reliable fallback. Verified Jezero elevation and geology integration remain.

The app currently uses a clearly labelled synthetic Jezero sample fixture so the demo can run without pretending that placeholder data is NASA data.

## Structure

- `frontend/` React, Vite, Tailwind CSS, Leaflet, and Recharts
- `backend/` FastAPI service and Python domain modules
- `backend/data/` sample-data notes and future processed rasters
- `DATA_SOURCES.md` dataset provenance and usage notes

## Run the backend

```powershell
cd backend
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the API docs.

Run backend tests from `backend/`:

```powershell
pytest
```

Regenerate the synthetic elevation fixture from `backend/` when needed:

```powershell
python -m scripts.generate_sample_terrain
```

## Run the frontend

```powershell
cd frontend
npm install
npm run dev
```

Open the URL printed by Vite, usually `http://localhost:5173`.

The frontend uses `VITE_API_URL` when present and otherwise targets `http://127.0.0.1:8000`.

## Test route planning

Run the backend and frontend in separate terminals. In the frontend, choose a destination and select **Compare routes**. The app requests safest, shortest, and science-focused candidates, draws them on the map, and shows distance, walk time, slope, safety, and science value in the comparison table. Select a route name in the table to emphasize its map line.

## Test return safety

After comparing routes, use the **Route progress** slider in the **Way back to habitat** panel. The alert should move from GREEN toward AMBER and RED as progress increases. Adjust the **Demo resource budget** slider to explore the thresholds. The budget is an adjustable demo assumption, not an official NASA value. The red map marker shows the calculated turn-back point and the panel names the nearest emergency stop.

## Test science stops

The map displays synthetic science and emergency markers. The **Science stops & support** panel lists delta, river-channel, and layered-rock regions with safety ratings and descriptions. Photo previews remain labelled as pending until a specific Perseverance image and its attribution are verified in `DATA_SOURCES.md`.

## Test mission briefing

After comparing routes, click **Prepare briefing**. The panel summarizes the computed route and safety numbers. If an external wording service is unavailable, Cairn automatically uses its built-in briefing format.
## Assumptions

All astronaut resource and walking values will live in `backend/app/config.py`, be exposed in the UI, and be labelled as assumptions. They are not official NASA values.
