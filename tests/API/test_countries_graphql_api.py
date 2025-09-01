import requests

GRAPHQL_ENDPOINT = "https://countries.trevorblades.com/"

QUERY = """
{
  countries {
    code
    name
    continent {
      name
    }
  }
}
"""

def test_country_data():
    response = requests.post(GRAPHQL_ENDPOINT, json={"query": QUERY})
    assert response.status_code == 200, "API did not return 200 OK"

    data = response.json()
    assert "data" in data and "countries" in data["data"], "Malformed response structure"

    countries = data["data"]["countries"]
    assert len(countries) > 0, "No countries returned"
    for country in countries:
        assert "name" in country and country["name"], "Missing country name"
        assert "code" in country and country["code"], "Missing country code"
        assert "continent" in country and "name" in country["continent"], "Missing continent info"

    # Specific check for South Africa 🇿🇦
    sa = next((c for c in countries if c["code"] == "ZA"), None)
    assert sa is not None, "South Africa not found"
    assert sa["name"] == "South Africa", f"Unexpected name: {sa['name']}"
    assert sa["continent"]["name"] == "Africa", f"Unexpected continent: {sa['continent']['name']}"
    print("All tests passed for country data.")
    print(f"Total countries fetched: {len(countries)}")
    print(f"South Africa details: {sa}")
    2+("Sample countries:", countries[:5])  # Print first 5 countries for verification
    print("GraphQL query executed successfully.")
