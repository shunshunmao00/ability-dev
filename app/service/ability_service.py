import requests
import websockets
from app.service import umm_client, uvisible_client
from app.global_data.global_data import g
import logging


# 针对于websocket请求的代理, 收到websocket请求后, 与upstream建立websocket连接
async def get_up_socket(prev_request):
    path = prev_request.path
    if path.startswith('/visible/'):
        # http://localhost:8080/visible-ability/visible/9002/
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
        logging.critical("internal_ip: {}".format(internal_ip))

        protocol = prev_request.protocol
        if protocol == "http":
            protocol = "ws"
        else:
            protocol = "wss"

        url = "{}://{}:{}/{}".format(protocol, internal_ip, k8s_port, filename)

        # 建立websocket连接
        ws = await websockets.connect(url)
        return ws
    raise Exception('当前不支持3')


def forward_request(prev_request):
    path = prev_request.path

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
