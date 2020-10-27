import requests
import websockets
from app.service import umm_client, uvisible_client
from app.global_data.global_data import g


# 针对于websocket请求的代理, 收到websocket请求后, 与upstream建立websocket连接
async def get_up_socket(prev_request):
    path = prev_request.path
    if path.startswith('/visible/'):
        # http://localhost:8080/visible-ability/visible/9002/
        path = path[9:]
        i = path.find('/')
        local_port = path[:i]
        filename = path[i + 1:]
        protocol = prev_request.protocol
        if protocol == "http":
            protocol = "ws"
        else:
            protocol = "wss"

        if local_port == "9000":
            url = "{}://localhost:{}/{}".format(protocol, local_port, filename)
        elif local_port == "9002":
            url = "{}://localhost:{}/{}".format(protocol, local_port, filename)
        elif local_port == "24f61c090e5a4c4f8fadacb9b0815b60":
            local_port = 30604
            url = "{}://k8s.unicom.gq:{}/{}".format(protocol, local_port, filename)
        else:
            raise Exception('当前不支持2')

        # 建立websocket连接
        ws = await websockets.connect(url)
        return ws
    raise Exception('当前不支持3')


def forward_request(prev_request):
    path = prev_request.path

    # if path.startswith('/model/'):
    #     deployment_uuid = path[7:]
    #
    #     res = umm_client.find_and_call_ability(deployment_uuid)
    #     if res['status'] != 'ok':
    #         raise Exception('未找到部署实例')
    #
    #     deployment = res['value']
    #
    #     k8s_port = deployment.get('k8sPort')
    #     if k8s_port is None:
    #         raise Exception('k8s实例端口停止服务')
    #
    #     internal_ip = g.get_central_config()['kubernetes']['ability']['internalIP']
    #     url = 'http://{}:{}/api/model'.format(internal_ip, k8s_port)
    #
    #     res = requests.post(url=url, data=prev_request.body, headers=prev_request.headers)
    #
    #     return {
    #         'response': res,
    #     }

    # if path.startswith('/model/'):
    #     deployment_uuid = path[7:]
    #
    #     # res = umm_client.find_and_call_ability(deployment_uuid)
    #     # if res['status'] != 'ok':
    #         # raise Exception('未找到部署实例')
    #     k8s_port = None
    #     # deployment = res['value']
    #     if deployment_uuid == '42efed5cbcec45ca896d38114896d3b2':
    #         k8s_port = '9001'
    #     # k8s_port = deployment.get('k8sPort')
    #     if k8s_port is None:
    #         raise Exception('k8s实例端口停止服务')
    #
    #     # internal_ip = g.get_central_config()['kubernetes']['ability']['internalIP']
    #     internal_ip = 'localhost'
    #     url = 'http://{}:{}/api/model'.format(internal_ip, k8s_port)
    #
    #     res = requests.post(url=url, data=prev_request.body, headers=prev_request.headers)
    #
    #     return {
    #         'response': res,
    #     }
    #
    # if path.startswith('/file/'):
    #     deployment_uuid, method = path[6:].split('/')
    #
    #     res = umm_client.find_and_call_ability(deployment_uuid)
    #     if res['status'] != 'ok':
    #         raise Exception('未找到部署实例')
    #
    #     deployment = res['value']
    #
    #     k8s_port = deployment.get('k8sPort')
    #     if k8s_port is None:
    #         raise Exception('k8s实例端口停止服务')
    #
    #     internal_ip = g.get_central_config()['kubernetes']['ability']['internalIP']
    #     url = 'http://{}:{}/api/file/{}'.format(internal_ip, k8s_port, method)
    #
    #     res = requests.post(url=url, data=prev_request.body, headers=prev_request.headers)
    #
    #     return {
    #         'response': res,
    #     }
    #
    # if path.startswith('/stream/'):
    #     deployment_uuid, method = path[8:].split('/')
    #
    #     res = umm_client.find_and_call_ability(deployment_uuid)
    #     if res['status'] != 'ok':
    #         raise Exception('未找到部署实例')
    #
    #     deployment = res['value']
    #
    #     k8s_port = deployment.get('k8sPort')
    #     if k8s_port is None:
    #         raise Exception('k8s实例端口停止服务')
    #
    #     internal_ip = g.get_central_config()['kubernetes']['ability']['internalIP']
    #     url = 'http://{}:{}/api/stream/{}'.format(internal_ip, k8s_port, method)
    #
    #     res = requests.post(url=url, data=prev_request.body, headers=prev_request.headers)
    #
    #     return {
    #         'response': res,
    #     }

    # if path.startswith('/web/'):
    #     path = path[5:]
    #     i = path.find('/')
    #     deployment_uuid = path[:i]
    #     filename = path[i + 1:]
    #
    #     res = umm_client.find_and_call_ability(deployment_uuid)
    #     if res['status'] != 'ok':
    #         raise Exception('未找到部署实例')
    #     deployment = res['value']
    #
    #     k8s_port = deployment.get('k8sPort')
    #     if k8s_port is None:
    #         raise Exception('k8s实例端口停止服务')
    #
    #     internal_ip = g.get_central_config()['kubernetes']['ability']['internalIP']
    #     url = 'http://{}:{}/web/{}'.format(internal_ip, k8s_port, filename)
    #
    #     res = requests.get(url=url, headers=prev_request.headers)
    #
    #     return {
    #         'response': res,
    #     }

    # if path.startswith('/web/'):
    #     path = path[5:]
    #     i = path.find('/')
    #     deployment_uuid = path[:i]
    #     filename = path[i + 1:]
    #     k8s_port = None
    #     # res = umm_client.find_and_call_ability(deployment_uuid)
    #     if deployment_uuid == '42efed5cbcec45ca896d38114896d3b2':
    #         k8s_port = '9001'
    #     # if res['status'] != 'ok':
    #     #     raise Exception('未找到部署实例')
    #     # deployment = res['value']
    #     #
    #     # k8s_port = deployment.get('k8sPort')
    #     if k8s_port is None:
    #         raise Exception('k8s实例端口停止服务')
    #
    #     # internal_ip = g.get_central_config()['kubernetes']['ability']['internalIP']
    #     internal_ip = 'localhost'
    #     url = 'http://{}:{}/web/{}'.format(internal_ip, k8s_port, filename)
    #
    #     res = requests.get(url=url, headers=prev_request.headers)
    #
    #     return {
    #         'response': res,
    #     }

    # if path.startswith('/visible/'):
    #     # http://localhost:8080/ability/local_cubeai/9001/
    #     # http://localhost:8080/visible-ability/visible/24f61c090e5a4c4f8fadacb9b0815b60/
    #     path = path[9:]
    #     i = path.find('/')
    #     local_port = path[:i]
    #     filename = path[i + 1:]
    #
    #     # if local_port == "9001":
    #     #     url = 'http://localhost:{}/web/{}'.format(local_port, filename)
    #     # elif local_port == "9000":
    #     #     url = 'http://localhost:{}/{}'.format(local_port, filename)
    #     # elif local_port == "9002":
    #     #     url = 'http://localhost:{}/{}'.format(local_port, filename)
    #     if local_port == "24f61c090e5a4c4f8fadacb9b0815b60":
    #         # http://localhost:8080/ability/local_cubeai/30604/
    #         local_port = 30604
    #         url = 'http://k8s.unicom.gq:{}/{}'.format(local_port, filename)
    #     else:
    #         raise Exception('当前不支持1')
    #
    #     # stream=True, 以支持 upstream 响应的内容是 chunk 传输
    #     res = requests.get(url=url, headers=prev_request.headers, stream=True)
    #
    #     return {
    #         'response': res,
    #     }

    if path.startswith('/visible/'):
        # http://localhost:8080/visible-ability/visible/24f61c090e5a4c4f8fadacb9b0815b60/
        path = path[9:]
        i = path.find('/')
        deployment_uuid = path[:i]
        filename = path[i + 1:]

        res = uvisible_client.find_and_call_ability(deployment_uuid)
        if res['status'] != 'ok':
            raise Exception('未找到部署实例')
        deployment = res['value']

        k8s_port = deployment.get('k8sPort')
        if k8s_port is None:
            raise Exception('k8s实例端口停止服务')

        internal_ip = g.get_central_config()['kubernetes']['ability']['internalIP']

        url = 'http://{}:{}/{}'.format(internal_ip, k8s_port, filename)

        res = requests.get(url=url, headers=prev_request.headers, stream=True)    # 允许分块传输

        return {
            'response': res,
        }

    raise Exception('unsupported API name')
