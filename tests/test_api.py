from fastapi.testclient import TestClient
from app.api import app
from unittest.mock import patch

client = TestClient(app)


# IMPORTANT: patch WHERE IT IS USED (app.routers)
@patch("app.routers.enqueue_job")
@patch("app.routers.set_job_status")
def test_upload_csv(mock_status, mock_queue):

    file_content = "a,b\n1,2\n3,4"

    response = client.post(
        "/api/upload/csv",
        files={"file": ("test.csv", file_content, "text/csv")}
    )

    # DEBUG (uncomment if it fails again)
    # print(response.status_code)
    # print(response.text)

    assert response.status_code == 201

    json_data = response.json()

    assert "preview" in json_data
    assert "file_name" in json_data