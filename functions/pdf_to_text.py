import PyPDF2
from io import BytesIO


def extract_text_from_pdf(file_stream):
    """
    Extracts text from the first page of a PDF file.

    :param file_stream: A file-like object (BytesIO or file pointer) representing the PDF.
    :return: Extracted text as a string or an empty string if no text is found.
    """
    try:
        reader = PyPDF2.PdfReader(file_stream)

        # Check if the PDF has pages
        if len(reader.pages) > 0:
            page = reader.pages[0]  # Extract text from the first page
            text = page.extract_text()
            return text if text else "No text found on the first page."
        else:
            return "The PDF has no pages."

    except Exception as e:
        print(f"Error reading PDF: {e}")
        return "Error extracting text from PDF."
