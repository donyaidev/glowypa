import os
import fitz
import time


class ProcessPDF:
    def __init__(self, pdf_input_path):
        self.pdf_input_path = pdf_input_path
    
    def extract_text(self):
        """Extract text from the PDF file."""
        texts = []
        try:
            pdf_document = fitz.open(self.pdf_input_path)
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                text = page.get_text("text")
                texts.append(text)
            pdf_document.close()
        except Exception as e:
            print(f"Error processing {self.pdf_input_path}: {e}")
        return "".join(texts)
    
    def run_test(self, path_pdf):
        """Run a test extraction on a single PDF."""
        processor = ProcessPDF(path_pdf)
        start = time.time()
        result = processor.extract_text()
        end = time.time()
        print(f"Time taken to process {path_pdf}: {end - start} seconds")
        return result
        
    def processing_document(self, folder_path: str):
        """Process all PDF files in a given folder and extract text."""
        text = ''
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.pdf'):
                    path_pdf = os.path.join(root, file)
                    text += self.run_test(path_pdf)
        return text


def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()