import pytesseract
from PIL import Image


def namecheck(text):
    nameTEST = 'HELENE MONTAGNA'
    nametest = 'Helene Montagna'
    if nameTEST in text:
        print('WOW')
    if nametest in text:
        print('wow')


if __name__ == '__main__':

    img = Image.open('images/test1.jpg')
    text = pytesseract.image_to_string(img, config='')
    namecheck(text)

        