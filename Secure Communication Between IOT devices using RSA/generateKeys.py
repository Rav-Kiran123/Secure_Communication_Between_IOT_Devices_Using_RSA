import sys, time
from socket import*
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64decode

def generateRSAKeys(pubName, privName):
    rng = Random.new().read
    key = RSA.generate(4096,rng)
    binPrivKey = key.exportKey('PEM')
    binPubKey = key.publickey().exportKey('PEM')
    with open(pubName,"w") as f:
        f.write(binPrivKey.decode('utf-8'))
        f.close()
    with open(privName,"w") as f:
        f.write(binPubKey.decode('utf-8'))
        f.close()
generateRSAKeys("IOTrsa","IOTrsa.pub")
generateRSAKeys("CLIENTrsa","CLIENTrsa.pub")