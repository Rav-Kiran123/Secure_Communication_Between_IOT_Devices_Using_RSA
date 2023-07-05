import random

LARGE_PRIME = 105341
RAND_LIMIT = 500000

def parse_message(msg):
    abc = ":"
    if abc.encode('utf-8') not in msg:
        return None
    
    x = []

    c = msg.split(abc.encode('utf-8'),1)
    x.append(c[0])

    args = c[1].split(",".encode('utf-8'))
    for arg in args:
        x.append(arg)
    #print(x)
    #x = ["CONNECT","bb61c8e5246e4e4ba7300dbdf746072a" ,"1", "Ravi"]
    return x

def get_diffie_nums():
    secret_num = int(random.randint(0,RAND_LIMIT))
    raisedRand = int(pow(int(3),secret_num))
    moddedRand = int(raisedRand  % int(LARGE_PRIME))
    return (secret_num,str(moddedRand))



def set_seq_num(my_secret_num,others_public_num):
    global seq_num

    try:
        received_long = int(others_public_num)
        raised_long = pow(received_long,my_secret_num)
        return raised_long % int(LARGE_PRIME)
    except ValueError:
        print("Erroneous Sequence Number Sent")
    return None