from PIL import Image
import pytesseract

# If Tesseract is not installed globally, specify the path to its executable.
# For Windows, adjust the path if necessary.
pytesseract.pytesseract.tesseract_cmd = r'../OCR/ocr/tesseract.exe'

def convert_image_to_text(image_path):
    """
    This function takes an image file path as input and returns the extracted text using Tesseract OCR.

    :param image_path: str, the path to the image file
    :return: str, extracted text from the image
    """
    try:
        # Try to open the image file and handle errors in case of invalid image format
        with Image.open(image_path) as img:
            img.verify()  # Verifies the image to ensure it's not corrupted
            
            # Open the image again to process it
            img = Image.open(image_path)

            # Use Tesseract to extract text from the image
            extracted_text = pytesseract.image_to_string(img)

            return extracted_text
    except Exception as e:
        print(f"Error: {e}")
        return None
# Example usage
image_path = '/run/media/spidey/0F56533E3399A505/Dore-AI/Dore-AI/ignore-this/Screenshot 2024-09-28 123441.png'  # Replace with the path to your image file
text = convert_image_to_text(image_path)
if text:
    print("Extracted Text:\n", text)
else:
    print("Failed to extract text.")
