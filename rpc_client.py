import requests
from typing import Any, Optional, Dict


class UnityException(Exception):
    pass


class JsonRpcClient:
    def __init__(self, port: int, hostname: str = 'localhost') -> None:
        self.hostname = hostname
        self.port = port
        self.session = requests.Session()
        self.jsonrpc_id = 0  # start id for rpc methods
        self.url = f'http://{self.hostname}:{self.port}/jsonrpc'

    def __getattr__(self, method_name: str) -> Any:
        if method_name.startswith('_'):
            raise AttributeError('Can not call method starts with _')
        return lambda **x: self.rpc_call(method_name, x)
    
    def _gen_rpc_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        response = {
            'method': method,
            'params': params,
            'jsonrpc': '2.0',
            'id': self.jsonrpc_id
        }
        self.jsonrpc_id += 1
        return response

    def rpc_call(
        self,
        method_name: str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Dict[str, Any]
    ) -> Any:
        params = params if params else {}
        params.update(kwargs)
        payload = self._gen_rpc_request(method_name, params)

        response = self.session.post(self.url, json=payload)
        response.raise_for_status()
        decoded_response = response.json()
        if error := decoded_response.get('error', None):
            error_message = f'{error["message"]}: {error["data"]}'
            raise UnityException(error_message)
        return decoded_response['result']
