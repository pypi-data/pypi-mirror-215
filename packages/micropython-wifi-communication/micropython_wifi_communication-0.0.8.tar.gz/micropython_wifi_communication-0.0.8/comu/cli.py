import socket

netw = True
try:
    import network
except:
    netw = False
from comu.util import validator, ip
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
        self.HOST = Host  # Endereço IP do servidor
        try:
            self.HOST = ip(self.HOST, self.ifconfig)[0]
        except:
            self.HOST = ip(self.HOST)[0]
        self.PORT = 1238  # Porta para comunicação

        # Cria o socket TCP/IP
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(None)
        # Conecta-se ao servidor
        self.client_socket.connect((self.HOST, self.PORT))
        self.client_socket.settimeout(300)

    def cone(self):
        global netw
        net = self.net
        if net and netw:
            if type(net) != dict:
                net = {}
            sta_if = network.WLAN(network.STA_IF)
            if not sta_if.isconnected():
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
            self.ifconfig = sta_if.ifconfig()

    def send(self, data):
        try:
            self.client_socket.settimeout(5)
            message = str({1: 1, 'inf': data, 0: 0})
            self.client_socket.send(message.encode())
            self.client_socket.settimeout(None)
        except:
            self.ence()

    def close(self):
        self.send('jnhvcdtyGHAJHDGDHgftghjnhbftryuikjnbhgvfrtyuiokmnbvgcfrtyuikjnbhvcfrtyui75414578445445741574')
        self.client_socket.close()
        raise Exception("Servidor finalizado!")

    def recv(self):
        x = None
        try:
            message = self.client_socket.recv(self.trans).decode()
            if not message:
                self.ence()
            self.client_socket.settimeout(None)
            va, me = validator(message)
            me = me['inf']
            if me == 'jnhvcdtyGHAJHDGDHgftghjnhbftryuikjnbhgvfrtyuiokmnbvgcfrtyuikjnbhvcfrtyui75414578445445741574':
                x = True
            elif not va:
                return me
        except:
            self.ence()
        if x:
            self.client_socket.close()
            raise Exception("Servidor finalizado pelo server!")

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
