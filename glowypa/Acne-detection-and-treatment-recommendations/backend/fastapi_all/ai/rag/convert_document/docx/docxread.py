from docx import Document
from docx.shared import Inches
import os
from PIL import Image
import time
import json

class Process_docx:
    def __init__(self, path_input_docx, output_dir="./"):
        self.path_input_docx = path_input_docx
        self.output_dir = output_dir
        self.file_input_name = path_input_docx.split('/')[-1]
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    def save_image_from_docx(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        docx=Document(self.path_input_docx)
        for rel in docx.part.rels.values():
            if "image" in rel.target_ref:
                img_data = rel.target_path.blob
                img_filename = os.path.basename(rel.target_ref)
                img_path = os.path.join(self.output_dir, self.file_input_name.split('.')[0], img_filename)
                with open(img_path, 'wb') as f:
                    f.write(img_data)
                print(f'Image saved to {img_path}')
    def extract_text_and_tables(self, save=False):
        docx = Document(self.path_input_docx)
        print("Extracting text and table: ")
        #explore words
        dict_chunks={}
        for i, para in enumerate(docx.paragraphs, 1):
            if para.text:
                dict_chunks[f'chunk{i}']=para.text
        #explore table
        dict_table = {}
        for i, table in enumerate(docx.tables, 1):
            lst_row= []
            for row in table.rows:
                row_data = [cell.text for cell in row.cells]
                row_data_text = "\t".join(row_data)
                lst_row.append(row_data_text)
            text_table = "\n".join(lst_row)
            dict_table[f'table{i}'] = text_table
        if save:
            with open(os.path.join(self.output_dir, f"{self.file_input_name.split('.')[0]}_text.json"), 'w', encoding='utf-8') as f:
                json.dump(dict_chunks, f, ensure_ascii=False, indent=4)
            with open(os.path.join(self.output_dir, f"{self.file_input_name.split('.')[0]}_table.json"), 'w', encoding='utf-8') as f:
                json.dump(dict_table, f, ensure_ascii=False, indent=4)
        return dict_chunks, dict_table
    
    def extract_infor_for_DB(self, save=False):
        lst_infor=[]
        docx = Document(self.path_input_docx)
        for i, para in enumerate(docx.paragraphs, 1):
            lst_infor.append({'chunk': para.text, 
                              "payloads":{
                                  "file_name": self.path_input_docx,
                                  "position para": i,
                                  "type": ".docx",
                                  "lst_img_relevant":{
                                      'path':[],
                                      'OCR_text': []
                                  },
                                  "lst_table_relevant": [],
                              }})
        if save:
            with open(os.path.join(self.output_dir, f"{self.file_input_name.split('.')[0]}_infor.json"), 'w', encoding='utf-8') as f:
                json.dump(lst_infor, f, ensure_ascii=False, indent=4)
        return lst_infor
    
def run_test(path):
    Processer = Process_docx(path)
    print(Processer.extract_infor_for_DB(save=True))
if __name__=="__main__":
    path_docx_file = '/Users/nhatthuong/Documents/Acne-detection-and-treatment-recommendations/backend/fastapi_all/ai/rag/documents/acne_treatment.docx'
    start = time.time()
    run_test(path_docx_file)
    print(time.time() - start)