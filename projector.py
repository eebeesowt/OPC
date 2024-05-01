import socket
import hashlib


class Projector:
    def __init__(self, ip, port, login, password, label, id) -> None:
        self.ip = ip
        self.port = port
        self.login = login
        self.password = password
        self.label = label
        self.id = id
        if label == '':
            self.label = ip

        self.power = None
        self.screen_format = None
        self.input = None
        self.group = False
        self.shutter = True
        self.shutter_in_time = None
        self.shutter_out_time = None

        self.screen_dict = {
            '0': '16:10',
            '1': '16:9',
            '2': '4:3'
        }
        self.input_dict = {
            'RG1': 'COMPUTER1',
            'RG2': 'COMPUTER2',
            'VID': 'VIDEO',
            'SVD': 'Y/C',
            'DVI': 'DVI',
            'HD1': 'HDMI',
            'SD1': 'SDI',
            'DL1:HD1': 'Digital Link HD1',
            'DL1:HD2': 'Digital Link HD2',

        }
        self.get_info()
        self.debug_info()

    def send_cmd(self, cmd):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            sock.connect((self.ip, self.port))
        except socket.error as exc:
            raise exc
        serv_answer = sock.recv(1024)
        decode_answer = serv_answer.decode()
        print('CONNECTION SERVER ANSWER --------', decode_answer)
        rand_num = decode_answer.split(' ')[-1][0:-1]
        print('RANDOM NUMBER--------------------', rand_num)
        auth_data = f'{self.login}:{self.password}:{rand_num}'
        print(auth_data)
        md5hash = hashlib.md5(auth_data.encode())
        command = md5hash.hexdigest() + chr(48) + chr(48) + cmd + chr(13)
        print(command)
        sock.send(bytes(command.encode()))
        answ = sock.recv(21)
        decode_answer = answ.decode()[2:-1]
        print('ANSWER AFTER COMMAND-----', decode_answer)
        sock.close()
        return decode_answer

    def get_info(self):
        print('____________GET INFO IN___________')
        power = self.send_cmd('QPW')
        print('POWER ANSW', power)
        if power == '001':
            self.power = True
            shutter = self.send_cmd('QSH')
            if shutter == '0':
                self.shutter = True
            else:
                self.shutter = False
        else:
            self.power = False
        # self.screen_format = self.screen_dict[self.send_cmd('QSF')]
        self.input = self.input_dict[self.send_cmd('QIN')]
        get_shutter_in = self.send_cmd('QVX:SEFS1')
        answer_shutter_in_time = get_shutter_in.split('=')
        if len(answer_shutter_in_time) > 1:
            self.shutter_in_time = answer_shutter_in_time[1]
        get_shutter_out = self.send_cmd('QVX:SEFS2')
        answer_shutter_in_time = get_shutter_out.split('=')
        if len(answer_shutter_in_time) > 1:
            self.shutter_out_time = answer_shutter_in_time[1]
        print('____________GET INFO OUT___________')

    def power_on(self):
        self.send_cmd('PON')

    def power_off(self):
        self.send_cmd('POF')

    def shutter_open(self):
        self.send_cmd('OSH:0')

    def shutter_close(self):
        self.send_cmd('OSH:1')

    def shutter_in(self, shutter_time):
        self.send_cmd(f'VXX:SEFS1={shutter_time}')

    def shutter_out(self, shutter_time):
        self.send_cmd(f'VXX:SEFS2={shutter_time}')

    def set_screen_format(self, screen_format):
        for key, val in self.screen_dict.items():
            if val == screen_format:
                self.send_cmd(f'VSF:{key}')

    def debug_info(self):
        print(
            f'''
    IP--------{self.ip}
    PORT------{self.port}
    LOGIN-----{self.login}
    PASSWORD--{self.password}
    LABEL-----{self.label}
    ID--------{self.id}
    POWER-----{self.power}
    SCREEN_F__{self.screen_format}
    INPUR SRC-{self.input}
    GROUP-----{self.group}
    SHUTTER---{self.shutter}
    SHUTTER_IN---{self.shutter_in_time}
    SHUTTER_OUT---{self.shutter_out_time}
        '''
        )
