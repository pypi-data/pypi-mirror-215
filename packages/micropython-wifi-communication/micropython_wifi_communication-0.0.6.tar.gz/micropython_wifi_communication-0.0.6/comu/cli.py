import socket
import network
from comu.util import validator
from time import sleep

class ci:

    def __init__(self, net=None, Host='50.1', tr=1024):
        self.net = net
        x = None
        while not x:
            try:
                self.cone()
                x = True
            except:
                pass
            sleep(1)
        self.trans = tr
        self.HOST = '192.168.' + Host  # Endereço IP do servidor
        self.PORT = 1234  # Porta para comunicação

        # Cria o socket TCP/IP
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(None)
        # Conecta-se ao servidor
        self.client_socket.connect((self.HOST, self.PORT))
        self.client_socket.settimeout(300)

    def cone(self):
        net = self.net
        if net:
            if type(net) != dict:
                net = {}
            sta_if = network.WLAN(network.STA_IF)
            if not sta_if.isconnected():
                print('Conectando-se à rede Wi-Fi...')
                sta_if.active(True)
                ssid = 'MinhaRedeWiFI'
                if 'ssid' in net:
                    ssid = net['ssid']
                password = 'MinhaSenha123'
                if 'password' in net:
                    password = net['password']
                if password != '':
                    sta_if.connect(ssid, password)
                else:
                    sta_if.connect(ssid)
                while not sta_if.isconnected():
                    pass

    def send(self, data):
        try:
            self.client_socket.settimeout(5)
            message = str({1: 1, 'inf': data, 0: 0})
            self.client_socket.send(message.encode())
            self.client_socket.settimeout(None)
        except:
            self.ence()

    def recv(self):
        try:
            message = self.client_socket.recv(self.trans).decode()
            if not message:
                self.ence()
            self.client_socket.settimeout(None)
            va, me = validator(message)
            if not va:
                return me['inf']
        except:
            self.ence()

    def ence(self):
        x = None
        self.client_socket.close()
        while not x:
            try:
                wlan = network.WLAN(network.STA_IF)
                if not wlan.isconnected():
                    self.cone()
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((self.HOST, self.PORT))
                self.client_socket.settimeout(300)
                x = True
            except Exception as e:
                pass
            sleep(1)