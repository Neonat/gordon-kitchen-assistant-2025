# 🍳 Gordon RAMsay

A Hackomania 2025 kitchen-copilot prototype exploring food-image recognition and recipe suggestions from available ingredients. It combines a React interface, a Flask API, Gemini helpers and a Spoonacular recipe client.

## What is implemented

- A text-input page sends recipe requests to the Flask `/chat` endpoint.
- Camera capture and preview components support the image-recognition experiment.
- Gemini image/audio helper modules and a LangGraph recipe workflow live in the backend.
- The ingredients page displays sample recipes. Shopping-list and community-sharing ideas remain prototype UI concepts.

## Local setup

You need Python 3 with `venv`, Node.js/npm, and your own Google Gemini and Spoonacular API access for the connected features.

```sh
git clone https://github.com/Neonat/gordon-RAMsay.git
cd gordon-RAMsay
```

Start the backend from its own directory:

```sh
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Create `backend/.env` using the variable names read by the backend:

```dotenv
GOOGLE_API_KEY=
SPOONACULAR_API_KEY=
```

Fill in your keys locally, then start Flask:

```sh
python app.py
```

Flask uses [localhost:5000](http://localhost:5000). In a second terminal, start the frontend from the repository root:

```sh
cd frontend
npm install
npm start
```

Open [the text-input page](http://localhost:3000/textinput), [ingredients page](http://localhost:3000/ingredientspage), or [camera page](http://localhost:3000/camera). These are the routes currently defined in `frontend/src/App.jsx`; the root route has no page.

## Current integration gaps

The camera frontend sends `/upload-photo` and reads `items`; the backend exposes `/api/upload-photo` and returns `detected_items`. The backend also launches `imagerec.py` from its working directory while the helper is under `backend/utils/`. That path needs integration work before image analysis can run end to end.

The checked-in Gemini model identifiers and external API behavior have not been verified against current services. This setup describes the source as committed; connected AI/API calls require provider access.

## Development checks

```sh
cd frontend
npm run build
npm test -- --watchAll=false --passWithNoTests
```

The frontend currently has no checked-in test files. Backend syntax can be checked without starting the API or making model requests:

```sh
python3 -m compileall -q backend
```

## Source layout

- `frontend/` — React, React Router and Bootstrap interface, using Create React App scripts.
- `backend/app.py` — Flask routes and upload handling.
- `backend/ai.py` — LangGraph recipe workflow.
- `backend/utils/` — Gemini image/audio helpers and Spoonacular tool.
- `backend/spoonacular/` — checked-in generated Python API client.

## License

This project is licensed under the MIT License.
