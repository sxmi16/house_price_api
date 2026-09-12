# House Price Prediction API

A production-style FastAPI service that deploys a trained scikit-learn regression model to predict house prices from property listing data. Built as part of the *APIs and Web Services* project - the model itself was trained in an earlier sprint; this project wraps it in a documented, validated REST API.

## Overview

The API loads a pre-trained model once at startup and exposes it through three endpoints: a health check, a model metadata lookup, and a prediction endpoint. All incoming requests are validated against strict field-level constraints before they ever reach the model, and errors are surfaced with proper HTTP status codes rather than raw stack traces.

## Features

- **Fast, validated predictions** — 13 property features (bedrooms, bathrooms, area, location, and 7 amenity flags) validated with Pydantic before inference
- **Singleton model loading** — the model and its metadata load once at startup, not on every request
- **Graceful error handling** — 422 for invalid input, 503 if the model isn't loaded, 500 for unexpected prediction failures
- **Interactive docs** — auto-generated Swagger UI at `/docs` for exploring and testing every endpoint in the browser

## Tech stack

- Python 3.11+
- FastAPI
- Pydantic
- scikit-learn
- joblib
- uvicorn

## Project structure

```
house_price_api/
├── main.py               # FastAPI app and route definitions
├── api.py                # Business logic: model loading, prediction, health checks
├── schemas.py             # Pydantic request/response schemas
├── model.pkl              # Trained scikit-learn model (joblib-serialized)
├── model_metadata.json    # Model metadata (version, features, training date, RMSE)
└── requirements.txt        # Python dependencies
```

## Setup

1. Clone the repository and move into the project folder:
   ```bash
   git clone <your-repo-url>
   cd house_price_api
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the API

Start the server with:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. Interactive documentation is at:

```
http://127.0.0.1:8000/docs
```

## Endpoints

### `GET /health`

Returns the current service status and whether the model is loaded.

```json
{
  "status": "healthy",
  "model_loaded": true,
  "message": "Service status: model and metadata loaded successfully"
}
```

### `GET /model/info`

Returns metadata about the loaded model, including the ordered list of features it expects.

```json
{
  "model_type": "RandomForestRegressor",
  "version": "1.0.0",
  "features": ["total_images", "beds", "baths", "area", "latitude", "longitude",
               "garden", "garage", "new_construction", "pool", "terrace",
               "air_conditioning", "parking"],
  "training_date": "2026-01-15",
  "rmse": 21540.33,
  "description": "House price prediction model trained on residential listing data"
}
```

### `POST /predict`

Accepts 13 property features and returns a predicted price.

**Request body:**
```json
{
  "total_images": 10,
  "beds": 3,
  "baths": 2.5,
  "area": 1800.0,
  "latitude": 40.7128,
  "longitude": -74.0060,
  "garden": 1,
  "garage": 1,
  "new_construction": 0,
  "pool": 0,
  "terrace": 1,
  "air_conditioning": 1,
  "parking": 1
}
```

**Response:**
```json
{
  "predicted_price": 312450.75,
  "currency": "USD",
  "model_version": "1.0.0"
}
```

Invalid input (e.g., `beds` outside the 0–10 range, or a missing required field) returns a `422 Unprocessable Entity` with details on which field failed validation.

## Author

Samiul Islam
