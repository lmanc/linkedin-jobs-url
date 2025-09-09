from fastapi import status


def test_build_empty_body(client):
    """Test the `/build` endpoint with an empty body."""
    response = client.post('/build', json={})

    assert response.status_code == status.HTTP_200_OK
