#importando bibliotecas
import socket 
import threading

#Escolha do apelido
apelido = input("Escolha seu Apelido: ")

#Conectando ao Servidor
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('localhost', 65535))

#Escutando (função receive) ao servidor e enviando apelido
def receive():
    while True:
        try:
            #Tente receber a mensagem do servidor
            #Se(if) conseguir envie o apelido para o cliente
            message = cliente.recv(1024).decode('ascii')
            if message == 'USR':
                cliente.send(apelido.encode('ascii'))
            else:
                    print(message)
        except:
            #Acabar conexão se houver erros.
            print("Ocorreu um erro!")
            cliente.close()
            break
#Enviando mensagens ao servidor.
def write():
    while True:
        message = '{}: {}'.format(apelido, input(''))
        cliente.send(message.encode('ascii'))
#Começando Threads para escutar e escrever
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
