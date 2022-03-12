#ORGANIZATION:
#should be fairly simple, just a function that encrypts and a function that decrypts
from math import ceil, floor
from PIL import Image
def encrypt(input, imageDir, resultImageDir):
    inputBitArray = []
    for char in input:
        charValue = ord(char)
        for i in range(4):
            currValue = charValue >> i*2
            inputBitArray.append(currValue & 0b11)
    for i in range(4):
        inputBitArray.append(0b00)
    imObj = Image.open(imageDir)
    imObj = imObj.convert("RGBA")
    imArr = imObj.load()
    newImg = imObj.copy()
    for i in range(ceil(len(inputBitArray)/3)):
        height = floor(i/imObj.width)
        width = i-height*imObj.width
        currPixel = list(imArr[width, height])
        for j in range(3):
            currMessageIndex = i*3+j
            if (currMessageIndex >= len(inputBitArray)):
                break
            currPixel[j] = currPixel[j] >> 2
            currPixel[j] = currPixel[j] << 2
            currPixel[j] = currPixel[j] | inputBitArray[currMessageIndex]
        newImg.putpixel((width, height), tuple(currPixel))
    newImg.save(resultImageDir + ".png", "png")
    imObj.close()


#convert input into bytes
#get photo
#replace last 2 bytes in each pixel with 2 bytes in the input
#save I guess

def printPixels(imageDir):
    imObj = Image.open(imageDir)
    imObj = imObj.convert("RGBA")
    imArr = imObj.load()
    for i in range(imObj.width):
        for j in range(imObj.height):
            if (imArr[i, j] != (0, 0, 0, 0)):
                print(imArr[i, j])
    imObj.close()

def decrypt(imageDir):
    imObj = Image.open(imageDir)
    imObj = imObj.convert("RGBA")
    imArr = imObj.load()
    footerFound = False
    messageData = []
    currPixelNum = 0
    currDataNum = 0
    while (not footerFound):
        height = floor(currPixelNum/imObj.width)
        width = currPixelNum-height*imObj.width
        currPixel = list(imArr[width, height])
        for i in range(3):
            charNum = floor(currDataNum / 4)
            #each 2 bit
            bitNum = currDataNum - charNum*4
            currData = currPixel[i] & 0b11
            if (bitNum == 0):
                messageData.append(0)
            messageData[charNum] = messageData[charNum] | (currData << 2*bitNum)
            #print(currData)
            if (bitNum == 3 and messageData[charNum] == 0):
                footerFound = True
                break
            currDataNum += 1
        currPixelNum += 1
    message = ""
    for i in range(len(messageData)):
        message += chr(messageData[i])
    print(messageData)
    print(message)

def main():
    #encrypt("RESIGN LOBSTER RESIGN LOBSTER RESIGN LOBSTER RESIGN LOBSTER RESIGN LOBSTER", "kol_sword_guy.png", "test2")
    #printPixels("test1.png")
    decrypt("test2.png")
    

if (__name__ == "__main__"):
    main()