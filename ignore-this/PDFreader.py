import os
import PyPDF2


def read_pdf(file_path):
    print("Reading PDF...")
    # Open the PDF file
    with open(file_path, 'rb') as file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)

        # Get the number of pages in the PDF
        num_pages = len(pdf_reader.pages)

        # Initialize an empty string to store the text
        text = ''

        # Loop through each page and extract the text
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    os.system('cls')
    return text


if __name__ == '__main__':
    # Specify the path to the PDF file
    pdf_file_path = r"sample-1.pdf"

    # Read the content of the PDF
    pdf_text = read_pdf(pdf_file_path)
    print("PDF Contents : \n", pdf_text)
