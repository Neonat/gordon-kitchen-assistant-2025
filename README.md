# Gordon RAMsay

A kitchen-assistant prototype built at Hackomania 2025. The team explored an ingredient-first recipe workflow through text input, camera capture, Gemini, and Spoonacular.

The repository contains a React interface and a Flask API. Text requests invoke a LangGraph recipe workflow. Camera captures reach a separate Gemini recognition helper. Sample recipe cards illustrate the intended experience while inventory, shopping lists, and community sharing remain incomplete.

[What works](#what-works) · [Stack and architecture](#stack-and-architecture) · [Local setup](#local-setup) · [Current limits](#current-limits)

## What works

- Enter a message on the text-input page and send it to Flask's `/chat` endpoint.
- Run the recipe graph, which asks Gemini to call the Spoonacular tool and then summarise recipe names.
- Capture a camera image, preview it, and submit it to `/api/upload-photo`. The page displays the returned `detected_items`.
- Browse sample Pasta and Pizza cards on the ingredients page.

The camera path uses a separate temporary file for each request. Its result is not a persistent ingredient inventory. Audio helpers are experiments in the backend utilities, rather than a complete voice-input flow.

## Stack and architecture

| Technology | Role in the project |
| --- | --- |
| React 18 and React Router | Separate the text, camera, and ingredients screens into page components. |
| Bootstrap and React Bootstrap | Supply navigation, buttons, and recipe-card styling. |
| Create React App 5 | Run the development server, component tests, and production build. TypeScript is pinned to `4.9.5` for that toolchain. |
| Flask and Flask-CORS | Expose JSON routes to the browser and handle image uploads. |
| LangGraph and LangChain's Google integration | Represent recipe lookup as explicit tool-selection, execution, and response stages. |
| Gemini and Spoonacular | Recognise food images, interpret text, and retrieve recipe data through external services. |

The browser calls Flask on `localhost:5000`. Flask owns the provider calls and credentials. [backend/ai.py](backend/ai.py) defines the text workflow; [backend/utils/imagerec.py](backend/utils/imagerec.py) defines image recognition. The checked-in [Spoonacular client](backend/spoonacular/) is generated API code.

## Local setup

Use Python 3.9 or later with `venv`, Node.js 20 or later, and npm. Connected functions require Google Gemini and Spoonacular access.

```sh
git clone https://github.com/Neonat/gordon-kitchen-assistant-2025.git
cd gordon-kitchen-assistant-2025/backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Create `backend/.env` with your own credentials:

```dotenv
GOOGLE_API_KEY=
SPOONACULAR_API_KEY=
```

From `backend/`, start Flask:

```sh
python app.py
```

In a second terminal, from the repository root, start the React app:

```sh
cd frontend
npm install
npm start
```

Open one of the routes defined in [frontend/src/App.jsx](frontend/src/App.jsx):

| Page | Local URL |
| --- | --- |
| Text input | [localhost:3000/textinput](http://localhost:3000/textinput) |
| Camera | [localhost:3000/camera](http://localhost:3000/camera) |
| Sample recipes | [localhost:3000/ingredientspage](http://localhost:3000/ingredientspage) |

The root route has no page. Allow browser camera access when testing capture.

## Checks and source guide

From `frontend/`:

```sh
npm run build
npm test -- --watchAll=false --runInBand
```

From the repository root:

```sh
python3 -m unittest discover -s backend/tests -v
python3 -m compileall -q backend
```

The camera component test mocks the API response. Backend tests mock recognition and check the route and temporary-file contract. These checks do not establish live recipe or recognition quality.

| Location | Responsibility |
| --- | --- |
| [frontend/src/pages/](frontend/src/pages/) | Camera, text-input, and ingredients pages |
| [frontend/src/components/](frontend/src/components/) | Navigation, capture, preview, and text controls |
| [backend/app.py](backend/app.py) | Chat, upload, and recognition routes |
| [backend/utils/](backend/utils/) | Image, audio, and recipe API helpers |
| [backend/requirements.txt](backend/requirements.txt) | Python dependencies |

Changes to the camera flow should keep the request's `photo` field and the response's `detected_items` field aligned across the React component and Flask route.

## Current limits

The Gemini identifiers in the source describe the original development setup. Current model availability and the live Gemini and Spoonacular integrations have not been validated here. The frontend build retains existing lint warnings.

Flask starts in debug mode with permissive CORS. Captured images are sent to Gemini by the recognition helper. The repository does not implement production authentication, account storage, or a complete inventory-to-recipe flow.

## License and acknowledgements

The existing project documentation declares the MIT License, but the repository has no standalone project `LICENSE` file. The bundled Spoonacular client retains its generated documentation and notices.
