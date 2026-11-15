from users_cli import filter_by_min_age, filter_by_city

SAMPLE_USERS = [
    {
        "name": "An", "age": 22, "city": "HCM"
    },
    {
        "name": "Binh", "age": 30, "city": "HN"
    },
    {
        "name": "Chi", "age": 27, "city": "HCM"
    },
]

def test_filter_by_city():
    result = filter_by_city(SAMPLE_USERS,"HCM")
    assert len(result) == 2
    assert result[0]["name"] == "An"
    assert result[1]["name"] == "Chi"

def test_filter_by_min_age():
    result = filter_by_min_age(SAMPLE_USERS,25)
    assert len(result) == 2
    assert result[0]["age"] == 30
    assert result[1]["age"] == 27
