import os
import tempfile
from pathlib import Path

import pytest

_tmp = Path(tempfile.mkdtemp())
os.environ["PUD_DATABASE_URL"] = f"sqlite:///{_tmp / 'test.db'}"
os.environ["PUD_FRONTEND_DIST"] = str(_tmp / "no-dist")


@pytest.fixture()
def client():
    from fastapi.testclient import TestClient

    from app.main import app

    with TestClient(app) as test_client:
        test_client.delete("/api/history")
        yield test_client
