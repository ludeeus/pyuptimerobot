import json
import os

TEST_API_TOKEN = "ur1234567-0abc12de3f456gh7ij89k012"
TEST_RESPONSE_HEADERS = {"Content-Type": "application/json"}


def fixture(filename, asjson=True):
    """Load a fixture."""
    path = os.path.join(os.path.dirname(__file__), "fixtures", f"{filename}.json")
    with open(path, encoding="utf-8") as fptr:
        if asjson:
            return json.loads(fptr.read())
        return fptr.read()
