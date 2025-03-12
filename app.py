from pythonosc.udp_client import SimpleUDPClient
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
import asyncio
from flask import Flask, render_template, request
from projector import Projector
from typing import List


def filter_handler(address, *args):
    print(f"{address}: {args}")


dispatcher = Dispatcher()
dispatcher.map("/filter", filter_handler)

ip = "127.0.0.1"
port = 1337

server = AsyncIOOSCUDPServer((ip, port), dispatcher, asyncio.get_event_loop())
server.serve()

ip = "192.168.1.43"
port = 1337

client = SimpleUDPClient(ip, port)  # Create client

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('channel.html')


@app.route('/channel', methods=['GET', 'POST'])
def channel():
    if request.method == 'POST':
        chan = int(request.form.get('channel'))
        if request.form.get('open') == 'ON':
            client.send_message(f"/eos/chan/{chan}/full", None)
            return render_template('channel.html', address=chan)
        elif request.form.get('close') == 'OFF':
            client.send_message(f"/eos/chan/{chan}/out", None)
            return render_template('channel.html', address=chan)
        elif request.form.get('remdim') == 'RemDim':
            client.send_message(f"/eos/chan/{chan}/remdim", None)
            return render_template('channel.html', address=chan)
        else:
            print('WTF')
    elif request.method == 'GET':
        return render_template('channel.html')


projector_list = [
    ('10.101.10', 1024, 'admin', 'panasonic', 'Бельэтаж'),
    ('10.101.10', 1024, 'admin', 'panasonic', '125'),
    ('10.101.10', 1024, 'admin', 'panasonic', '126'),
    ('10.101.10', 1024, 'admin', 'panasonic', '122')
]


def get_on_projectros():
    projectors: List[Projector] = []
    for projector in projector_list:
        try:
            proj = Projector(*projector, len(projectors))
        except Exception as e:
            print(e)
            print(f'No connection to projector {projector[0]}')
        else:
            projectors.append(proj)
    return projectors


projectors = get_on_projectros()


@app.route('/projector', methods=['GET', 'POST'])
def projector():
    global projectors
    if request.method == 'POST':
        ip = request.form['ip']
        login = request.form['login']
        password = request.form['password']
        label = request.form['label']
        proj = (ip, 1024, login,
                password, label, len(projectors))
        projector_list.append(proj)
        projectors.append(Projector(*proj))
        return render_template('projector.html', projectors=projectors)
    elif request.method == 'GET':
        projectors = get_on_projectros()
        return render_template('projector.html',
                               projectors=projectors)


@app.route('/power', methods=['POST'])
def power():
    global projectors
    if request.method == 'POST':
        id = int(request.form.get('data'))
        if projectors[id].power:
            projectors[id].power_off()
            projectors[id].power = False
            return 'off'
        else:
            projectors[id].power_on()
            projectors[id].power = True
            return 'on'


@app.route('/shutter', methods=['POST'])
def shutter():
    global projectors
    if request.method == 'POST':
        id = int(request.form.get('data'))
        if projectors[id].shutter:
            projectors[id].shutter_close()
            projectors[id].shutter = False
            return 'off'
        else:
            projectors[id].shutter_open()
            projectors[id].shutter = True
            return 'on'


@app.route('/shutter_in', methods=['POST'])
def shutter_in():
    global projectors
    if request.method == 'POST':
        id = int(request.form.get('data'))
        shutter_time = request.form.get('time')
        projectors[id].shutter_in(shutter_time)
        projectors[id].shutter_in_time = shutter_time
        return 'good'


@app.route('/shutter_out', methods=['POST'])
def shutter_out():
    global projectors
    if request.method == 'POST':
        id = int(request.form.get('data'))
        shutter_time = request.form.get('time')
        projectors[id].shutter_out(shutter_time)
        print(shutter_time)
        projectors[id].shutter_out_time = shutter_time
        return 'good'


@app.route('/setScreenFormat', methods=['POST'])
def screen_format():
    global projectors
    if request.method == 'POST':
        id = int(request.form.get('data'))
        format = request.form.get('format')
        projectors[id].set_screen_format(format)
        projectors[id].screen_format = format
        return 'good'


@app.route('/grouped', methods=['POST'])
def grouped():
    global projectors
    if request.method == 'POST':
        id = int(request.form.get('data'))
        print(f'ID ___________________ {id}')
        projectors[id].group = not projectors[id].group
        return 'lol'


@app.route('/gshutOn', methods=['GET'])
def group_shutter_on():
    global projectors
    if request.method == 'GET':
        for projector in projectors:
            if projector.group:
                projector.shutter_open()
                projector.shutter = True
        return render_template('projector.html', projectors=projectors)


@app.route('/gshutOff', methods=['GET'])
def group_shutter_off():
    global projectors
    if request.method == 'GET':
        for projector in projectors:
            if projector.group:
                projector.shutter_close()
                projector.shutter = False
        return render_template('projector.html', projectors=projectors)


@app.route('/deleteProj', methods=['POST'])
def deleteProj():
    global projectors
    if request.method == 'POST':
        id = int(request.form.get('del_but'))
        projectors.remove(projectors[id])
        for index in range(id, len(projectors)):
            projectors[index].id -= 1
        return render_template('projector.html', projectors=projectors)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
