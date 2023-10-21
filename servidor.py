# importando bibliotecas 
import socket
import threading

# Infos da conexão 
host = 'localhost'
port = 65535

# Conexão com o Servidor.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(10)

#Lista de Clientes(IPs) e Apelidos.
clientes = []
apelidos = []

# Enviando mensagens para todos os clientes conectados.
def broadcast(message):
    for cliente in clientes:
        cliente.send(message)
## Tratamento/Manuseio de mensagem para os clientes.
def handle(cliente):
    ### Fazendo um loop para mandar mensagens ou remover o cliente caso aconteça erros.
    while True:
        try:
            #Broadcast de mensagens
            message = cliente.recv(1024)
            broadcast(message)
        except:
            #Removendo CLientes
            index = clientes.index(cliente)
            clientes.remove(cliente)
            cliente.close()
            apelido = apelidos[index]
            broadcast('{} saiu!'.format(apelido).encode('ascii'))
            apelidos.remove(apelido)
            break
                #Função receive ou receber/ouvir
def receive():
    while True:
        #Aceitando a conexão
        cliente, endereço = server.accept()
        print("Conectado com {}".format(str(endereço)))
        
        #Pedir e guardar o apelido
        cliente.send("USR".encode('ascii'))
        apelido = cliente.recv(1024).decode('ascii')
        apelidos.append(apelido)
        clientes.append(cliente)

        #Printar e fazer o broadcast dos apelidos
        print("Seu apelido é {}".format(apelido))
        broadcast("{} entrou!".format(apelido).encode('ascii'))
        cliente.send('Conectado ao servidor!'.encode('ascii'))

        #inciciar a função de ouvir para o cliente
        thread = threading.Thread(target=handle, args=(cliente,))
        thread.start()
print("O servidor está escutando...")
receive()
