# Live Flight Tracker & Spatiotemporal Visualization

A Django-based spatiotemporal web application that ingests, filters, and renders real-time aviation telemetry on interactive geospatial maps. The system handles live flight queries, calculates geographic bounding boxes, and plots aircraft trajectories and state vectors with smooth client-side animation.

---

## Architecture & Features

- **Backend:** Django with PostgreSQL / SQLite support for aviation telemetry and geospatial queries.
- **Frontend:** Interactive Google Maps JavaScript API mapping with Solid.js components and dynamic flight status tables.
- **Data Ingestion:** Integrations for live flight data pipelines (Flightradar24 / OpenSky Network APIs).
- **Spatiotemporal Calculations:** Automatic viewport calculation, circular boundary averaging, zoom factor determination, and localized flight filtering.

---

## Prerequisites

- Python 3.9+ (Python 3.10 recommended)
- PostgreSQL (or local SQLite for development)
- Google Cloud Platform account with **Maps JavaScript API** enabled
- Flightradar24 API access token (or compatible aviation telemetry feed)

---

## Quickstart & Local Setup

### 1. Clone the Repository
bash
git clone https://github.com/mesas998/flights.git
cd flights


### 2. Set Up Virtual Environment
bash
python3 -m venv venv
source venv/bin/activate

### 3. Configure Environment Variables
Copy the example environment file and configure your credentials:
bash
cp .env.example .env

Ensure the following variables are defined in `.env` (or exported in your shell / WSGI configuration):
env
SECRET_KEY="your-django-secret-key"
DEBUG=True
GOOGLE_API_KEY="your-google-maps-api-key"
FR24_API_TOKEN="your-fr24-api-token"

> **Security Note:** In Google Cloud Console, restrict `GOOGLE_API_KEY` using **HTTP Referrer Restrictions** to your deployment domain (e.g., `*.yourdomain.com/*` and `localhost:8000/*`).

### 4. Database Migrations & Initial Setup
2.Create and Populate README.md:Handover Documentation.Create the README.md file directly in that folder using your preferred text editor (e.g., nano README.md or via the PythonAnywhere Files tab), pasting the handover guide:Markdown# Live Flight Tracker & Spatiotemporal Visualization

A Django-based spatiotemporal web application that ingests, filters, and renders real-time aviation telemetry on interactive geospatial maps. The system handles live flight queries, calculates geographic bounding boxes, and plots aircraft trajectories and state vectors with smooth client-side animation.

---

## Architecture & Features

- **Backend:** Django with PostgreSQL / SQLite support for aviation telemetry and geospatial queries.
- **Frontend:** Interactive Google Maps JavaScript API mapping with Solid.js components and dynamic flight status tables.
- **Data Ingestion:** Integrations for live flight data pipelines (Flightradar24 / OpenSky Network APIs).
- **Spatiotemporal Calculations:** Automatic viewport calculation, circular boundary averaging, zoom factor determination, and localized flight filtering.

---

## Prerequisites

- Python 3.9+ (Python 3.10 recommended)
- PostgreSQL (or local SQLite for development)
- Google Cloud Platform account with **Maps JavaScript API** enabled
- Flightradar24 API access token (or compatible aviation telemetry feed)

---

## Quickstart & Local Setup

### 1. Clone the Repository
bashgit clone https://github.com/mesas998/flights.gitcd flights
### 2. Set Up Virtual Environment
bashpython3 -m venv venvsource venv/bin/activatepip install --upgrade pippip install -r requirements.txt
### 3. Configure Environment Variables
Copy the example environment file and configure your credentials:
bashcp .env.example .env
Ensure the following variables are defined in `.env` (or exported in your shell / WSGI configuration):
envSECRET_KEY="your-django-secret-key"DEBUG=TrueGOOGLE_API_KEY="your-google-maps-api-key"FR24_API_TOKEN="your-fr24-api-token"
> **Security Note:** In Google Cloud Console, restrict `GOOGLE_API_KEY` using **HTTP Referrer Restrictions** to your deployment domain (e.g., `*.yourdomain.com/*` and `localhost:8000/*`).

### 4. Database Migrations & Initial Setup
bashpython manage.py migratepython manage.py collectstatic --noinput

### 5. Run the Server
bash
python manage.py runserver

Navigate to `http://127.0.0.1:8000/flight/?count=1` to verify map rendering and flight data display.

---

## Key Project Structure

text
├── app2/
│   ├── models.py       # Aviation data schemas (Flight, Aircraft, Airport, Bounds)
│   ├── views.py        # Spatial calculations, API fetching, and view handlers
│   └── templates/app2/ # Map rendering views (Google Maps & Solid.js integration)
├── ree/
│   ├── settings.py     # Core settings, database connection, and API key loading
│   ├── urls.py         # App routing
│   └── wsgi.py         # WSGI deployment hook
├── .env.example        # Reference environment variable template
├── requirements.txt    # Frozen Python dependencies
└── setup.py            # Package installation script
---

## Deployment Notes (PythonAnywhere / WSGI)

When deploying under a WSGI daemon (e.g., PythonAnywhere or uWSGI), ensure `GOOGLE_API_KEY` and `FR24_API_TOKEN` are populated in the process environment prior to invoking `get_wsgi_application()`:

2.Create and Populate README.md:Handover Documentation.Create the README.md file directly in that folder using your preferred text editor (e.g., nano README.md or via the PythonAnywhere Files tab), pasting the handover guide:Markdown# Live Flight Tracker & Spatiotemporal Visualization

A Django-based spatiotemporal web application that ingests, filters, and renders real-time aviation telemetry on interactive geospatial maps. The system handles live flight queries, calculates geographic bounding boxes, and plots aircraft trajectories and state vectors with smooth client-side animation.

---

## Architecture & Features

- **Backend:** Django with PostgreSQL / SQLite support for aviation telemetry and geospatial queries.
- **Frontend:** Interactive Google Maps JavaScript API mapping with Solid.js components and dynamic flight status tables.
- **Data Ingestion:** Integrations for live flight data pipelines (Flightradar24 / OpenSky Network APIs).
- **Spatiotemporal Calculations:** Automatic viewport calculation, circular boundary averaging, zoom factor determination, and localized flight filtering.

---

## Prerequisites

- Python 3.9+ (Python 3.10 recommended)
- PostgreSQL (or local SQLite for development)
- Google Cloud Platform account with **Maps JavaScript API** enabled
- Flightradar24 API access token (or compatible aviation telemetry feed)

---

## Quickstart & Local Setup

### 1. Clone the Repository
bashgit clone https://github.com/mesas998/flights.gitcd flights
### 2. Set Up Virtual Environment
bashpython3 -m venv venvsource venv/bin/activatepip install --upgrade pippip install -r requirements.txt
### 3. Configure Environment Variables
Copy the example environment file and configure your credentials:
bashcp .env.example .env
Ensure the following variables are defined in `.env` (or exported in your shell / WSGI configuration):
envSECRET_KEY="your-django-secret-key"DEBUG=TrueGOOGLE_API_KEY="your-google-maps-api-key"FR24_API_TOKEN="your-fr24-api-token"
> **Security Note:** In Google Cloud Console, restrict `GOOGLE_API_KEY` using **HTTP Referrer Restrictions** to your deployment domain (e.g., `*.yourdomain.com/*` and `localhost:8000/*`).

### 4. Database Migrations & Initial Setup
bashpython manage.py migratepython manage.py collectstatic --noinput
### 5. Run the Server
bashpython manage.py runserverNavigate to `http://127.0.0.1:8000/flight/?count=1` to verify map rendering and flight data display.

---

## Key Project Structure

text├── app2/│   ├── models.py       # Aviation data schemas (Flight, Aircraft, Airport, Bounds)│   ├── views.py        # Spatial calculations, API fetching, and view handlers│   └── templates/app2/ # Map rendering views (Google Maps & Solid.js integration)├── ree/│   ├── settings.py     # Core settings, database connection, and API key loading│   ├── urls.py         # App routing│   └── wsgi.py         # WSGI deployment hook├── .env.example        # Reference environment variable template├── requirements.txt    # Frozen Python dependencies└── setup.py            # Package installation script
---

## Deployment Notes (PythonAnywhere / WSGI)

When deploying under a WSGI daemon (e.g., PythonAnywhere or uWSGI), ensure `GOOGLE_API_KEY` and `FR24_API_TOKEN` are populated in the process environment prior to invoking `get_wsgi_application()`:

pythonimport osos.environ["GOOGLE_API_KEY"] = "your-key"os.environ["FR24_API_TOKEN"] = "your-token"os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ree.settings')from django.core.wsgi import get_wsgi_applicationapplication = get_wsgi_application()

---

## Intellectual Property & License

Proprietary Codebase. Copyright (c) 2026. All rights reserved. Handover and usage terms governed by the purchase agreement.



