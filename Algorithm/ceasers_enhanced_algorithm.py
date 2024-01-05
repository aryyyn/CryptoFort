import random
import time

def enhancedEncryption(NormalText, EncryptionCode):
    Encrypted_text = ""
    #EncryptionCode += EncryptionCode * (len(NormalText) // len(EncryptionCode) + 5)
    for i in range(len(NormalText)):  
        ch = NormalText[i]
        Enc = chr(ord(ch) + int(EncryptionCode[i]))
        Encrypted_text += Enc
    return Encrypted_text 




#def SimpleDecryption(EncryptionCode):
    #Example = "Qbttxpse234"
    #DecryptedText = ""
    #for i in range(len(Example)):
       # Dec = Example[i]
        #Decrypt =chr(ord(Dec) - int(EncryptionCode[i]))
       # print(f"{i} :{DecryptedText}")
        #DecryptedText+=Decrypt
    #print(f"Decrypted Text: {DecryptedText}")

        
#EncryptedCode = 
#simpleEncryption("Password123")
#SimpleDecryption(EncryptedCode)




