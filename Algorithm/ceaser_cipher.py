import random,time

def simpleEcnryption(NormalText):
    Encrypted_text = ""
    epoch = time.time()
    for i in range(len(NormalText)):
        ch = NormalText[i]
        Enc = (chr(ord(ch) + 24))
        Encrypted_text+=Enc
    return Encrypted_text
        
        
EncryptedText = simpleEcnryption("Prasiddha123 Hex")
print(EncryptedText)


