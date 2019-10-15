import pytesseract
from PIL import Image
img = Image.open('images/1.png')
text = pytesseract.image_to_string(img, config='')
print(text)