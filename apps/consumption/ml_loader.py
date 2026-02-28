"""
Global ML model loader — loads .pkl models once per process and caches them.
Avoids loading on every request (cold start / Railway free tier friendly).
"""

import os
import joblib
from django.conf import settings

# Process-global cache: load only once per worker
_model_cache = {}
_scaler_cache = None


def get_model(model_type='random_forest'):
    """Return cached model for model_type; load from disk only on first use."""
    global _model_cache
    if model_type not in _model_cache:
        path = os.path.join(settings.ML_MODELS_PATH, f'{model_type}_model.pkl')
        if os.path.isfile(path):
            _model_cache[model_type] = joblib.load(path)
        else:
            _model_cache[model_type] = None
    return _model_cache[model_type]


def get_scaler():
    """Return cached scaler; load from disk only on first use."""
    global _scaler_cache
    if _scaler_cache is None:
        path = os.path.join(settings.ML_MODELS_PATH, 'scaler.pkl')
        if os.path.isfile(path):
            _scaler_cache = joblib.load(path)
        else:
            _scaler_cache = None
    return _scaler_cache
