import requests

import cmon.helper
from cmon import Flow


def test_extend_fastapi():
    def extend_rest_function(app):
        @app.get('/hello', tags=['My Extended APIs'])
        async def foo():
            return {'msg': 'hello world'}

        return app

    cmon.helper.extend_rest_interface = extend_rest_function
    f = Flow(protocol='http')

    with f:
        response = requests.get(f'http://localhost:{f.port}/hello')
        assert response.status_code == 200
        assert response.json() == {'msg': 'hello world'}
