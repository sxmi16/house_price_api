from pydantic import BaseModel, Field
from typing import Optional

class HousePredictionRequest(BaseModel):
    """Schema for house prediction request - validates all 13 features"""

    # Property listing features
    total_images: int = Field(..., ge=0, le=50, description="Number of property images (0-50)")

    # Basic property features
    beds: int = Field(..., ge=0, le=10, description="Number of bedrooms (0-10)")
    baths: float = Field(..., ge=0, le=10, description="Number of bathrooms (0-10, can be decimal like 2.5)")
    area: float = Field(..., gt=0, le=10000, description="Property area in square feet (must be positive, max 10000)")

    # Location features
    latitude: float = Field(..., ge=-90, le=90, description="Property latitude (-90 to 90)")
    longitude: float = Field(..., ge=-180, le=180, description="Property longitude (-180 to 180)")

    # Binary features (0 or 1)
    garden: int = Field(..., ge=0, le=1, description="Has garden: 0=No, 1=Yes")
    garage: int = Field(..., ge=0, le=1, description="Has garage: 0=No, 1=Yes")
    new_construction: int = Field(..., ge=0, le=1, description="Is new construction: 0=No, 1=Yes")
    pool: int = Field(..., ge=0, le=1, description="Has pool: 0=No, 1=Yes")
    terrace: int = Field(..., ge=0, le=1, description="Has terrace: 0=No, 1=Yes")
    air_conditioning: int = Field(..., ge=0, le=1, description="Has AC: 0=No, 1=Yes")
    parking: int = Field(..., ge=0, le=1, description="Has parking: 0=No, 1=Yes")

    class Config:
        schema_extra = {
            "example": {
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
        }

# YOUR TASK: Add the PredictionResponse schema
# This schema defines what your API returns after making a prediction
# It should have:
# - predicted_price: float (the predicted house price)
# - currency: str with default value "USD"
# - model_version: str (the version of the model used)

class PredictionResponse(BaseModel):
    """Schema for prediction response"""
    predicted_price: float = Field(..., description="The predicted house price")
    currency: str = Field(default = "USD", description="Currency of the predicted price")
    model_version: str = Field(..., description="Version of the model used for prediction")

    class Config:
        schema_extra = {
            "example": {
                "predicted_price": 425000.50,
                "currency": "USD",
                "model_version": "1.0.0"
            }
        }

# YOUR TASK: Add the ModelInfoResponse schema
# This schema defines what the /model/info endpoint returns
# It should have:
# - model_type: str
# - version: str
# - features: list of strings
# - training_date: str
# - rmse: float
# - description: str

class ModelInfoResponse(BaseModel):
    """Schema for model information response"""
    model_type: str = Field(..., description="Type of the model (e.g., 'Random Forest', 'Linear Regression')")
    version: str = Field(..., description="Version of the model")
    features: list[str] = Field(..., description="List of features used by the model")
    training_date: str = Field(..., description="Date when the model was trained (YYYY)")
    rmse: float = Field(..., description="Root Mean Square Error of the model on the test set")
    description: str = Field(..., description="A brief description of the model and its purpose")

    class Config:
        schema_extra = {
            "example": {
                "model_type": "Random Forest",
                "version": "1.0.0",
                "features": ["total_images", "beds", "baths", "area", "latitude", "longitude", "garden", "garage", "new_construction", "pool", "terrace", "air_conditioning", "parking"],
                "training_date": "2023-01-15",
                "rmse": 25000.75,
                "description": "This model predicts house prices based on various features of the property."
            }
        }

# YOUR TASK: Add the HealthCheckResponse schema
# This schema defines what the /health endpoint returns
# It should have:
# - status: str (should be "healthy" or "unhealthy")
# - model_loaded: bool (True if model is loaded, False otherwise)
# - message: str (a descriptive message)

class HealthCheckResponse(BaseModel):
    """Schema for health check response"""
    status: str = Field(..., description="Health status of the API (e.g., 'healthy' or 'unhealthy')")
    model_loaded: bool = Field(..., description="Whether the model has been successfully loaded")
    message: str = Field(..., description="A descriptive message about the API model status")

    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "model_loaded": True,
                "message": "The model is loaded and ready to make predictions."
            }
        }
