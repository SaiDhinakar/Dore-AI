import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'.\Tesseract-OCR\tesseract.exe'
# # Load the image from file
img_path = r"Screenshot 2024-09-28 123441.png"
image = cv2.imread(img_path)
cv2.imshow('Result',image)
# # Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # Use Tesseract to do OCR on the image
text = pytesseract.image_to_string(gray)

# # Print the text
print(text)

cv2.waitKey(0)
