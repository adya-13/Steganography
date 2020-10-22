#Steganography using least signifiacnt bit technique
import cv2
import numpy as np

def toBinary(data):
    newd = ''
    if type(data)==str:
        for i in data:
            newd+=format(ord(i), '08b')
        return newd
    elif type(data)==int or type(data)==np.uint8:
        return format(data,'08b')

def encode():
    print("Enter the image path")
    image=cv2.imread(input())
    
    print("Enter the secret message")
    message=input()
    message+='***'

    maximum_bytes=(image.shape[0]*image.shape[1]*3)//8

    if maximum_bytes<len(message):
        raise ValueError("Insuficient Bytes! Need bigger image or smaller message")

    index=0

    binary_message=toBinary(message)
    
    for value in image:
        for pixel in value:
            if index<len(binary_message):
                pixel[0]=int(toBinary(pixel[0])[:-1]+binary_message[index],2)
                index+=1
            if index<len(binary_message):
                pixel[1]=int(toBinary(pixel[1])[:-1]+binary_message[index],2)
                index+=1
            if index<len(binary_message):
                pixel[2]=int(toBinary(pixel[2])[:-1]+binary_message[index],2)
                index+=1

            if index>=len(binary_message):
                break

    return image

def decode():
    print("Enter the image path")
    
    image=cv2.imread(input())
    
    text=""
    for values in image:
        for pixels in values:
            r,g,b=toBinary(pixels[0]),toBinary(pixels[1]),toBinary(pixels[2])
            text+=r[-1]+g[-1]+b[-1]
        

    binary_data=[text[i:i+8] for i in range(0,len(text),8)]
    message=""
    for i in binary_data:
        message+=chr(int(i,2))
        if message[-3:]=='***':
                break
    return message[:-3]


if __name__=='__main__':
    print("Press 1 to encode, 2 to decode")
    n=int(input())
    if n==1:
        image=encode()
        print("Enter new name for the encoded image: ")
        new_image=input()
        new_image+='.png'
        print("Your encoded image is saved as png image")
        cv2.imwrite(new_image,image)
    elif n==2:
        msg=decode()
        print("The hidden message is: {}".format(msg))
    else:
        raise Exception("Enter correct input")