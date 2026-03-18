def chiffrer_cesar(msg):
    key =  10
    resultat = ""
    for c in msg.upper():
        if c.isalpha():
            decale = (ord(c) - 65 + key) % 26
            resultat += chr(decale + 65)
        else:
            resultat += c
    msg = resultat
    return msg

def dechiffrer_cesar(msg):
    key = -10
    return chiffrer_cesar(msg,key)