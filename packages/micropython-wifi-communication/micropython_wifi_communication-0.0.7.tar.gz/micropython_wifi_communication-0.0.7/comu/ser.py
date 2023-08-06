import socket
netw = True
try:
    import network
except:
    netw = False
from comu.util import validator, ip


class se:

    def __init__(self, net=None, Host='50.1', tr=1024, conecao=False):
        self.trans = tr
        self.HOST = '192.168.' + Host  # Endereço IP do servidor
        self.PORT = 1234  # self.PORTa para comunicação
        self.net = net
        self.conecao = conecao
        x = None
        while not x:
            try:
                self.cone()
                x = True
            except:
                pass

        # Cria o socket TCP/IP
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Associa o socket ao endereço IP e self.PORTa
        self.server_socket.bind((self.HOST, self.PORT))

        # Aguarda por conexões
        self.server_socket.listen(1)

        # Aceita uma nova conexão
        self.client_socket, self.client_address = self.server_socket.accept()
        self.client_socket.settimeout(300)
        print("cliente aceito")

    def cone(self):
        net = self.net
        conecao = self.conecao
        global netw
        ap_config = (self.HOST, '255.255.0.0', self.HOST, '255.255.0.0')
        if net and netw:
            if type(net) != dict:
                net = {}
            SSID = 'MinhaRedeWiFI'  # Nome da rede Wi-Fi
            if 'SSID' in net:
                SSID = net['SSID']
            PASSWORD = 'MinhaSenha123'  # Senha da rede Wi-Fi
            if 'PASSWORD' in net:
                PASSWORD = net['PASSWORD']

            # Configura o ponto de acesso Wi-Fi
            if conecao:
                ap = network.WLAN(network.AP_IF)
                ap.active(True)
                if PASSWORD != '':
                    ap.config(essid=SSID, authmode=network.AUTH_WPA2_PSK, password=PASSWORD)
                else:
                    ap.config(essid=SSID)
                network_config = ap.ifconfig()

                # Atualiza o endereço IP do ponto de acesso para o valor de self.HOST
                ap.ifconfig(ap_config)
            else:
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
                    ap_config = ip(self.HOST,sta_if.ifconfig())
                    self.HOST = ap_config[0]

                    sta_if.ifconfig(ap_config)

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
        while not x:
            try:
                self.cone()
                # self.client_socket.close()
                self.server_socket.listen(1)
                # Aceita uma nova conexão
                self.client_socket, self.client_address = self.server_socket.accept()
                self.client_socket.settimeout(300)
                print("cliente aceito")
                x = True
            except Exception as e:
                print(e)
                pass