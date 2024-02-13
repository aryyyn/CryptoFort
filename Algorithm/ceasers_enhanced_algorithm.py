import random
import time
import random

    
    

def enhancedEncryption(NormalText, EncryptionCode):
        encrypted_text = ""
        
        
        Salt = "T\$P"
        salted_password = NormalText + Salt
        
        EncryptionCode += EncryptionCode * (len(NormalText) // len(EncryptionCode) + len(EncryptionCode))
        reversed_encryption_code = "".join(reversed(EncryptionCode))
        
        num_rounds = 2
        for _ in range(num_rounds):
            for i in range(len(salted_password)):  
                ch = salted_password[i]
                Enc = chr(ord(ch) + int(EncryptionCode[i]))
                Enc_rev = chr(ord(ch) + int(reversed_encryption_code[i]))
                encrypted_text += Enc
                encrypted_text += Enc_rev
        
        return encrypted_text 



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




