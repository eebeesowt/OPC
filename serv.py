from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
import requests


def open_handler(address, *args):
    print(f"{address}:")
    proj = str(args[0])
    proj = proj.split('.')
    proj = {'projectors': proj[0]}
    requests.get('http://192.168.1.148:5000/resShutterOpen', params=proj)


def close_handler(address, *args):
    print(f"{address}:")
    proj = str(args[0])
    proj = proj.split('.')
    proj = {'projectors': proj[0]}
    requests.get('http://192.168.1.148:5000/resShutterClose', params=proj)


dispatcher = Dispatcher()
dispatcher.map("/resolumeShutter/open", open_handler)
dispatcher.map("/resolumeShutter/close", close_handler)

ip = "127.0.0.1"
port = 7001

server = BlockingOSCUDPServer((ip, port), dispatcher)
server.serve_forever()  # Blocks forever