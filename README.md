# Gordon RAMsay — kitchen assistant

A **Hackomania 2025** kitchen-assistant prototype exploring how available ingredients can become recipe suggestions. The repository combines a React interface, Flask API, Gemini helpers, a LangGraph recipe workflow and a checked-in Spoonacular Python client.

## What is built

- The text-input page sends a message to Flask's `/chat` endpoint, which invokes the recipe workflow and returns its response.
- Camera capture and preview components form the frontend of an image-recognition experiment.
- Backend helpers use Gemini for food-image and audio experiments; the recipe workflow can call the Spoonacular tool.
- The ingredients page displays sample Pasta and Pizza recipe cards. Shopping-list and community-sharing ideas remain prototype interface concepts.

The intended flow is ingredient capture followed by recipe discovery. The committed camera path still needs integration work, and the example recipe cards are not generated from a live inventory.

## Local setup

You need Python 3 with `venv`, Node.js/npm, and your own Google Gemini and Spoonacular API access for the connected features.

```sh
git clone https://github.com/Neonat/gordon-kitchen-assistant-2025.git
cd gordon-kitchen-assistant-2025
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

Open the [text-input page](http://localhost:3000/textinput), [ingredients page](http://localhost:3000/ingredientspage), or [camera page](http://localhost:3000/camera). These routes are defined in [`frontend/src/App.jsx`](frontend/src/App.jsx); the root route has no page.

## Current integration gaps

The camera frontend sends `/upload-photo` and reads `items`; the backend exposes `/api/upload-photo` and returns `detected_items`. The backend also launches `imagerec.py` from its working directory while the helper is under `backend/utils/`. Those mismatches prevent the documented camera flow from working end to end as committed.

The checked-in Gemini model identifiers and external API behaviour have not been verified against current services. This setup describes the committed source; connected AI/API calls require provider access and separate integration validation.

## Development checks

From the repository root:

```sh
cd frontend
npm run build
npm test -- --watchAll=false --passWithNoTests
```

The frontend currently has no checked-in test files. Backend syntax can be checked from the repository root without starting the API or making model requests:

```sh
python3 -m compileall -q backend
```

## Source guide

| Location | Purpose |
| --- | --- |
| [`frontend/`](frontend/) | React, React Router and Bootstrap interface, using Create React App scripts. |
| [`backend/app.py`](backend/app.py) | Flask routes and upload handling. |
| [`backend/ai.py`](backend/ai.py) | LangGraph recipe workflow. |
| [`backend/utils/`](backend/utils/) | Gemini image/audio helpers and Spoonacular tool. |
| [`backend/spoonacular/`](backend/spoonacular/) | Checked-in generated Spoonacular Python API client. |

## License

The existing project documentation declares the MIT License. A standalone project `LICENSE` file is not included in the current repository.
