import pytest
import requests

# API Endpoints
CAT_FACTS_URL = "https://catfact.ninja/fact"
DOG_API_URL = "https://dog.ceo/api/breeds/image/random"
AGIFY_API_URL = "https://api.agify.io?name=michael"
ADVICE_API_URL = "https://api.adviceslip.com/advice"


@pytest.mark.parametrize("url, expected_key, status_code", [
    (CAT_FACTS_URL, "fact", 200),
    (DOG_API_URL, "message", 200),
    (AGIFY_API_URL, "age", 200),
    (ADVICE_API_URL, "slip", 200)
])
def test_api_response_status_and_keys(url, expected_key, status_code):
    """
    Validate API response:
      - Correct HTTP status code
      - JSON contains expected key
    """
    response = requests.get(url, timeout=10)
    assert response.status_code == status_code

    data = response.json()
    assert expected_key in data, f"Expected key '{expected_key}' not found in {url}"


@pytest.mark.parametrize("url, key_type_map", [
    (CAT_FACTS_URL, {"fact": str}),
    (DOG_API_URL, {"message": str, "status": str}),
    (AGIFY_API_URL, {"name": str, "age": int, "count": int}),
    (ADVICE_API_URL, {"slip": dict})
])
def test_api_json_structure(url, key_type_map):
    """
    Validate JSON structure and types of returned data
    """
    response = requests.get(url, timeout=10)
    data = response.json()

    for key, expected_type in key_type_map.items():
        assert key in data, f"Key '{key}' missing in {url}"
        assert isinstance(data[key], expected_type), f"Key '{key}' in {url} is not {expected_type}"


def test_dog_api_message_is_url():
    """
    Validate Dog API returns a valid URL in 'message'
    """
    response = requests.get(DOG_API_URL, timeout=10)
    data = response.json()
    assert data["message"].startswith("https://"), f"Expected URL in 'message', got {data['message']}"


def test_cat_fact_not_empty():
    """
    Validate Cat Facts API returns a non-empty fact
    """
    response = requests.get(CAT_FACTS_URL, timeout=10)
    data = response.json()
    assert data["fact"], "Cat fact is empty"
