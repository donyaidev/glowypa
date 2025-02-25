from pdfminer.high_level import extract_text
import os
import fitz
import time

class Process_pdf:
    def __init__(self, pdf_input_path, output_dir="/Users/nhatthuong/Documents/Acne-detection-and-treatment-recommendations/backend/fastapi_all/ai/rag/convert_document", chunk_len=500):
        self.pdf_input_path=pdf_input_path
        self.output_dir = output_dir 
        self.chunk_len = chunk_len 
        
        self.file_name = self.pdf_input_path.split('/')[-1].split('.')[0]
        if not os.path.exists(os.path.join(self.output_dir, self.file_name)):
            os.makedirs(os.path.join(self.output_dir, self.file_name))
    
    def extract_text(self):
        texts = []
        pdf_document = fitz.open(self.pdf_input_path)
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text = page.get_text("text")
            texts.append(text)
        pdf_document.close()
        text_pdf ="".join(texts)
        return text_pdf

def run_test(path_pdf):
    processer=Process_pdf(path_pdf)
    start = time.time()
    re=processer.extract_text()
    print(re)
    print(time.time()-start)
    
if __name__=="__main__":
    path_pdf = "/Users/nhatthuong/Documents/Acne-detection-and-treatment-recommendations/backend/fastapi_all/ai/rag/documents/RESUME_NGUYEN_NHAT_THUONG.pdf"
    run_test(path_pdf=path_pdf)