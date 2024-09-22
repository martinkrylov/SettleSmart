import pytest
from app.services.recommender import Recommender


def test_get_recommendations():
    user = {"conditions": ["Prostate cancer", "Breast cancer"]}  # Replace with actual user identifier
    recommendations = Recommender().get_recommendations(user)
    print("recommendations:", recommendations)
    for recommendation in recommendations:
        print(recommendation.to_json())

    assert len(recommendations) > 0