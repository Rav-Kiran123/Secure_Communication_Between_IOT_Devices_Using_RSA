import socket
import sys
import uuid
import hashlib
import time
import getpass
import messaging_util
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64decode
import random


class Connection:
    def __init__(self, c, key, n):
        # conn is tuple: (IP, port)
        self.conn = c
        self.pubkey = key
        self.num = n
        self.last_msg = None


class ConnectionHandler:
    arr = [None,None,None,None,None]
    def __init__(self):
        self.arr = [None,None,None,None,None]
        self.size = 0
        self.max = 5

    def add_conn(self, tup, key):
        num = self.size + 1
        if num > self.max:
            return None  # cannot add another connection, already at max
        c = Connection(tup, key, num)
        self.arr[num-1] = c
        self.size = num
        return c

    def get_conn(self, tup):
        for c in self.arr:
            if c == None:
                continue
            if str(c.conn[0]) == str(tup[0]) and str(c.conn[1]) == str(tup[1]):
                return c
            return None

    def remove_conn(self, tup):
        i = 0
        for c in self.arr:
            if str(c.conn[0]) == str(tup[0]) and str(c.conn[1]) == str(tup[1]):
                self.size = self.size - 1
                self.arr[i] = None
                return True
                i += 1
                return False


# defines
PUB_KEY_FILE = "CLIENTrsa.pub"  # File that stores the client's public key
PRIV_KEY_FILE = "CLIENTrsa"  # File used to store the client's private key
REFRESH_TIMESTEP = 600  # Time
block_list = None
password = None
# end defines
secret_num = 0
iot_salt = None


def send_socket(s, msg, addr):
    sent = False
    s.settimeout(30)
    while sent == False:
        try:
            numSent = s.sendto(msg, addr)
            sent = True
        except socket.timeout:  # socket.error is subclass
            print("Timeout, trying again later...")
            time.sleep(60)  # check back in a minute


'''
hash password with salt
 @param salt
 @return hashed and salted password
'''


def hash_password(salt):
    hashedpassword = hashlib.sha256(password.encode()).hexdigest()
    return hashlib.sha256(hashedpassword.encode() + salt.encode()).hexdigest()


def connect(msgnum, salt):
    global password
    global iot_salt
    global secret_num
    # prompt for username
    username = input("username : ")
    # get and hash pasword
    password = input("password : ")
    hashed = hash_password(salt)
    #print(hashed)
    # set up salt to test iot
    iot_salt = str(uuid.uuid4().hex)
    # set up diffie hellman numbers
    secret_num, diffie_pub = messaging_util.get_diffie_nums()
    # form message
    print(iot_salt)
    return "ACK:PASS,"+msgnum+","+username+","+hashed+","+iot_salt+","+diffie_pub+","+clientPubText
'''
Helper method to initalize the current IOT's public key
 param: pubKey The text form public key of this client
'''


def init_pub(pubKey):
    global IOTpubtext
    IOTpubtext = pubKey


'''
Method that initializes the public and private key's of the client as well
as the connection handler.
'''


def init():
    global clientPub  # Object form of the client's public key
    global clientPriv  # Object form of the client's private key (never send)
    # Textual form of client's public key (used for sending and things)
    global clientPubText
    global handler
    global block_list  # List of (IP, port) tuples to block
    global seq_num  # The sequence number of the next message to send
    # Initialize global public key for client
    pub = open(PUB_KEY_FILE, "r")
    clientPubText = pub.read()
    clientPub = RSA.importKey(clientPubText)
    clientPub = PKCS1_OAEP.new(clientPub)
    pub.close()
    # Initialize global private key for client
    priv = open(PRIV_KEY_FILE, "r")
    clientPrivText = priv.read()
    clientPriv = RSA.importKey(clientPrivText)
    clientPriv = PKCS1_OAEP.new(clientPriv)
    priv.close()
    handler = ConnectionHandler()
    block_list = list()


def encrypt_RSA(public_key, message):
    key = public_key
    rsakey = RSA.importKey(key)
    rsakey = PKCS1_OAEP.new(rsakey)
    encrypted = rsakey.encrypt(message.encode("ascii"))
    return encrypted


'''
This is the method to decrypt using 4096 but RSA encryption with PKCS1_OAEP
padding.
It uses this IOT's private key to decrypt the 'package' and return the base64
decoded decrypted string.
 @param package String to be decrypted
 @return decrypted string
'''


def decrypt_RSA(package):
    # open private key file
    key = open(PRIV_KEY_FILE, "r").read()
    rsakey = RSA.importKey(key)
    rsakey = PKCS1_OAEP.new(rsakey)
    # decrypt text
    decrypted = rsakey.decrypt(package)
    return decrypted


'''
Method that abstracts the secure sending of data to the current IOT
 @param s The socket used to send messages accross the network
 @param msg The uncrypted message to send securely to the client
 @param conn The connection object pertaining to the current connected IOT
'''


def send_secure(s, msg, conn):
    print("The message is:\n",msg)
    encrypted_msg = encrypt_RSA(conn.pubkey, msg)
    print(encrypted_msg)
    # print "The encrypted message is:\n"+encryptedMsg
    send_socket(s, encrypted_msg, conn.conn)


'''
Method that abstracts the secure communication between the client and the
current IOT
 @param s The socket used to send the encrypted data
 @param conn The connection object pertaining to the current connected IOT
'''


def handle_data(s, conn):
    global handler
    print("")
    print("What would you like to send?, enter 'exit' to end")
    data = input(">")
    # if the user types in 'exit', send FIN msg
    if(data == 'exit'):
        send_secure(s, "FIN:"+str(seq_num), conn)
        handler.remove_conn(conn.conn)
    # otherwise, send a data msg
    else:
        data = "DATA:"+data+","+str(seq_num)
        send_secure(s, data, conn)
'''
Decrypts data received from server and checks seq. no. to make sure it's valid
 @param data data to decrypt
'''


def recv_secure(data):
    global seq_num
    # decrypt data
    decrypted_data = decrypt_RSA(data).decode()
    param_arr = decrypted_data.rsplit(",", 1)
    try:
        # check seq. no
        recieved_seq_num = (int)(param_arr[1])
        if(recieved_seq_num != seq_num+1):
            print("Incorrect sequence number recieved")
            return
        # set next seq. no
        else:
            seq_num += 2
    except ValueError:
        print ("Non Integer Sequence Number recieved")
        print ("Decrypted data: ")
        print (param_arr[0])


def is_legit_server(pwd, salt):
    # hash (client side) password with given salt
    hashed = hash_password(salt)
    # compare our hashed password w/ server's hashed password
    return True


# create a UDP socket
init()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('', 50000)
sock.bind(server_address)
refresh_list_time = time.time()
logging_on = False
global handler
while True:
    # Receive response
    print ("")

    # if it's time to refresh the list, clear out the block list and update refresh
    # time
    if(time.time() >= refresh_list_time):
        del block_list[:]
        refresh_list_time = time.time() + REFRESH_TIMESTEP
    
    try:
        data, server = sock.recvfrom(8192)
    except socket.timeout:
        
        continue   
    print ("Data received from: ", server)

    # if server is being blocked, don't read message
    if(server in block_list):
        continue
    # if the client is connected to an IOT, decrypt message and send encrypted message
    if handler.get_conn(server) != None:
        c = handler.get_conn(server)
        recv_secure(data)
        handle_data(sock, c)
        continue
    # parse the command
    terminal = messaging_util.parse_message(data)
    #print(terminal)
    #print(terminal)
    # connect message - server asking user to login
    if(terminal[0].decode() == "CONNECT"):
        #print(terminal)
        # if we're currently trying to log on, ignore other connect messages
        if(logging_on):
            continue
        # give user the option of not connecting to the device -loop to prevent illegal chars
        
        while True:
            c = input("Do you want to connect to "+terminal[3].decode()+"? (Y/N) ")
            # user tries to log onto IOT
            if(c == 'Y' or c == 'y'):
                #print(terminal[2], terminal[3])
                msg = connect(terminal[2].decode(), terminal[1].decode())
                # changing the port # to the port the server would listen to
                ackaddr = (server[0], 50001)
                # print "Sending ", msg, " to ", ackaddr
                send_socket(sock, msg.encode("utf-8"), ackaddr)
                # user is currently trying to log on -> should be true ;P
                logging_on = True
                break
                # user doesn't wanna log onto IOT, block brocasts for now
            elif(c == 'N' or c == 'n'):
                # put in spam numbers
                block_list.append(server)
                break
    # ack message / encrypt?
    elif(terminal[0].decode() == "ACK"):
        if(terminal[1].decode() == "ENCRYPT"):
            logging_on = False
            conn = ackaddr
            # check if there is the correct number of arguments and auth. IOT
            if(len(terminal) == 5 and is_legit_server(terminal[3], iot_salt)):
                # set up IOT pub. key
                init_pub(terminal[2].decode())
                # get client pub. key
                # msg = get_pub_msg()
                # generate the starting seq. no.
                seq_num = messaging_util.set_seq_num(secret_num, terminal[4])
                if seq_num is None:
                    print("This server is kinda sketchy - bad diffie number")
                    continue
                # try to add the connection
                new_conn = handler.add_conn(conn, IOTpubtext)
                if new_conn == None:
                    print ("Unable to add IOT, max connections enabled")
                    continue
                
                print ("Congrats, we logged on.")
                # send_socket(sock, msg, ackaddr)
                
                handle_data(sock, new_conn)  # send something
            else:
                print ("ERROR : Error getting the public key from IOT")
    elif(terminal[0]=="ERROR"):
        logging_on = False
        if(terminal[1] == "LOGIN"):
            print("ERROR : Invalid username or password")
        if(terminal[1] == "ARGUMENT"):
            print("ERROR : Bad Argument")
        if(terminal[1] == "NULLPUBKEY"):
            print("ERROR : Null public key sent")
    
    else:
        break

sock.close()
        
        