import math
import numpy as np

def swap(arr,index1, index2):
    temp = arr[index1]
    arr[index1] = arr[index2]
    arr[index2] = temp

class RC4:
    
    def __init__(self, plainText, key):
        self.plainText = plainText
        self.key = key
        self.initSArr = np.arange(0,256)
        self.tempArr = self.initTempArr()  
        
    def initTempArr(self):
        repeatTimes = math.floor(len(self.initSArr)/len(self.key))
        restKeyLen = len(self.initSArr) - len(self.key) * repeatTimes
        resultTempArr = (self.key*repeatTimes) + (self.key[:restKeyLen])
        return resultTempArr
    
    def KSA(self):
        j = 0
        self.ksaArr = self.initSArr.copy()
        for i in range(0,256):
            j = (j + ord(self.tempArr[i]) + self.initSArr[i])%256
            swap(self.ksaArr, i, j)
        
    def PRGA(self):
        i, j =0,0
        self.keyStream = []
        for m in range(1, len(self.plainText)+1):
            i = (i+1)%256     
            j = (j + self.ksaArr[i])%256
            swap(self.ksaArr,i, j)
            self.keyStream.append(self.ksaArr[(self.ksaArr[i]+self.ksaArr[j])%256])

            
       
    def encrypt(self):
        result = ""
        arr = []
        self.KSA()
        self.PRGA()
        for i in range(len(self.plainText)):
            arr.append(ord(self.plainText[i])^self.keyStream[i])
            result += chr(ord(self.plainText[i])^self.keyStream[i])
        return (result, arr);
        

    def decrypt(self, cipherText):
        result = ""
        for i in range(len(cipherText)):
            result += chr(self.keyStream[i]^cipherText[i])
        return result