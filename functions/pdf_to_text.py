import PyPDF2
def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            if len(reader.pages) > 0:
                page = reader.pages[0]  # Extract text from the first page
                return page.extract_text()
            else:
                return ""
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""