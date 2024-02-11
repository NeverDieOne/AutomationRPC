import pytest
from rpc_client import JsonRpcClient
import time


@pytest.fixture(scope='session')
def client():
    _client = JsonRpcClient(port=9000)
    yield _client


@pytest.fixture(scope='function')
def load_scene(client: JsonRpcClient):
    client = client.LoadScene(sceneName='Game')
    time.sleep(5)
