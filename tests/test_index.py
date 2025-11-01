import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

def test_index_page():
    from app import app                 
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert "Пользователи" in html