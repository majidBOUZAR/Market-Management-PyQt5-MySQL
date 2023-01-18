import cv2,time
from pyzbar.pyzbar import decode
         
vid = cv2.VideoCapture(1)
camera = True
used =[]

while camera == True :
    
    success, img = vid.read()
    detectedBarcodes = decode(img)
    
    for barcode in detectedBarcodes:
        print('aprouved')
        print((barcode.data))
        time.sleep(5)
