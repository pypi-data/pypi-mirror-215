import socket
import command_pb2

class Controle():
    def __init__(self, ip = '127.0.0.1', port = 20011, logger=True) -> None:
        self.robot_id = 0 # Protobuff message atributes
        self.yellow_team = 0
        self.wheel_left = 0
        self.wheel_right = 0

        self.ip = ip # Network parameters
        self.port = port
        self.buffer_size = 1024

        self.eletronica_ip = '127.0.0.1' # Receiver parameters
        self.eletronica_porta = 20012

        self.create_socket()

        self.logger=logger

    def create_socket(self):
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.ip, self.port))
        self.socket.setblocking(False) 
        self.socket.settimeout(0.0)
    
    def send_mensage(self, index, yellow_team, wheel_left, wheel_right):
        self.robot_id = index
        self.yellow_team = yellow_team
        self.wheel_left = wheel_left
        self.wheel_left = wheel_left

        msg = command_pb2.Command()
        msg.id = self.robot_id
        msg.yellowteam = yellow_team
        msg.wheel_left = self.wheel_left
        msg.wheel_right = self.wheel_right

        try: 
            self.socket.sendto(msg.SerializeToString(), (self.eletronica_ip, self.eletronica_porta))
            if self.logger: print("[CONTROLE] Enviado!")

        except socket.error as e:
            if e.errno == socket.errno.EAGAIN:
                if self.logger:
                    print("[CONTROLE] Falha ao enviar. Socket bloqueado")
            else:
                print("[CONTROLE] Socket error:", e)
            

class Commands():
    def __init__(self, ip='127.0.0.1', port=20012, logger=True):
        self.robot_id = 0 # Protobuff message atributes
        self.yellow_team = 0
        self.wheel_left = 0
        self.wheel_right = 0

        self.ip = ip # Network parameters
        self.port = port
        self.buffer_size = 1024

        self.create_socket()

        self.logger=logger

    def create_socket(self):
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.ip, self.port))
        self.socket.setblocking(False) 
        self.socket.settimeout(0.0)

    def get_commands(self):
        try: 
            bytesAddressPair = self.socket.recvfrom(self.buffer_size)
            msgRaw = bytesAddressPair[0]
            self.update_parameters(msgRaw)

            if self.logger:
                print("[ELETRONICA] Recebido!")
            
        except socket.error as e:
            # Handle non-blocking socket error
            if e.errno == socket.errno.EAGAIN:
                print("[ELETRONICA] Falha ao receber. Socket bloqueado.")
            else:
                print("[ELETRONICA] Socket error:", e)

    def update_parameters(self, msgRaw):
        msg = command_pb2.Command()
        msg.ParseFromString(msgRaw)
        
        self.robot_id = msg.id
        self.yellow_team = msg.yellowteam
        self.wheel_left = msg.wheel_left
        self.wheel_right = msg.wheel_right


    
