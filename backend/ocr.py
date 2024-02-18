try:
    import Image
except ImportError:
    from PIL import Image

#Import Libraries
from pdf2image import convert_from_path
import pytesseract
import os
from sys import platform

#Inact Tesseract
if platform == "linux" or platform == "linux2":
    # linux
    pytesseract.pytesseract.tesseract_cmd = r'/bin/tesseract'
elif platform == "darwin":
    # OS X
    pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'
elif platform == "win32":
    # Windows...
    pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'

def pdfToString(filename):

    #Declare Output String
    output = ""

    #Convert PDFile to PNGImages
    images = convert_from_path(filename)

    #Each Image to Add in Output String
    for image in images:
        output = output + pytesseract.image_to_string(image)

    #Return Output
    return output

def imageToString(filename):
    return pytesseract.image_to_string(filename)