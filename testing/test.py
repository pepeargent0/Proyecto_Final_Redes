import schemathesis
@schemathesis.given("http://localhost:8000/openapi.json")
def test_api_behavior(case):
    case.call()
    assert case.response.status_code < 500
