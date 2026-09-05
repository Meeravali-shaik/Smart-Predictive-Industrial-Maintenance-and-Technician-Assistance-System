"""Compatibility wrapper for maintenance recommendation engine."""

from app.services.recommendation_service import RecommendationEngine


class MaintenanceRecommendationService(RecommendationEngine):
    """Thin wrapper for the recommendation engine."""

    pass
