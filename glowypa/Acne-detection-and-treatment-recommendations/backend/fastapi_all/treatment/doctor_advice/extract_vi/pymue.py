import fitz  
import json
import base64
import io
from PIL import Image
from langdetect import detect
import uuid 
import tempfile
import easyocr
import os
import numpy as np
import re
import torch
import time

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.bool_):
            return bool(obj)
        return super(NumpyEncoder, self).default(obj)

class ExtractTextPDFpyMUPDF:
    def __init__(self):
        self.json_extract = None
        self.gpu = torch.cuda.is_available()
        if self.gpu:
            print("Initializing readers with GPU...")
            self.reader_vi = easyocr.Reader(['vi'], gpu=True)
            self.reader_en = easyocr.Reader(['en'], gpu=True)
            self.reader_ja = easyocr.Reader(['ja'], gpu=True)
            self.reader_en_vi = easyocr.Reader(['en', 'vi'], gpu=True)
            self.reader_en_ja = easyocr.Reader(['en', 'ja'], gpu=True)
        else:
            print("Initializing readers with CPU...")
            self.reader_vi = easyocr.Reader(['vi'], gpu=False)
            self.reader_en = easyocr.Reader(['en'], gpu=False)
            self.reader_ja = easyocr.Reader(['ja'], gpu=False)
            self.reader_en_vi = easyocr.Reader(['en', 'vi'], gpu=False)
            self.reader_en_ja = easyocr.Reader(['en', 'ja'], gpu=False)
        
    def detect_languages_in_text(self, text):
        """Phát hiện tất cả ngôn ngữ có trong văn bản"""
        if not text.strip():
            return ['vi']
        paragraphs = re.split(r'\n+', text)
        detected_langs = set()
        for paragraph in paragraphs:
            if not paragraph.strip():
                continue
            try:
                lang = detect(paragraph)
                if lang in ['en', 'vi', 'ja']:
                    detected_langs.add(lang)
            except:
                continue
        if not detected_langs:
            return ['vi']
            
        return sorted(list(detected_langs))
        
    def determine_ocr_languages(self, detected_langs):
        """Xác định các bộ ngôn ngữ OCR cần sử dụng"""
        langs = set(detected_langs)
        ocr_combinations = []
        
        if 'ja' in langs and 'vi' in langs:
            # Nếu có cả ja và vi, OCR riêng với en,ja và vi
            ocr_combinations.append(['en', 'ja'])
            ocr_combinations.append(['vi'])
        elif 'ja' in langs and 'en' in langs and 'vi' in langs:
            # Nếu có cả 3 ngôn ngữ
            ocr_combinations.append(['en', 'ja'])
            ocr_combinations.append(['en', 'vi'])
        elif 'ja' in langs:
            ocr_combinations.append(['en', 'ja'])
        elif 'en' in langs and 'vi' in langs:
            ocr_combinations.append(['en', 'vi'])
        else:
            ocr_combinations.append(list(langs))
        return ocr_combinations
        
    def extract_pdf_content(self, file_path):
        file_name = os.path.basename(file_path)  
        result = {
            "file_name": file_name,
            "context": [],
            "image_page": []
        }
        
        doc = fitz.open(file_path)
        print(f"Total pages in PDF: {len(doc)}")
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            
            detected_langs = self.detect_languages_in_text(text)
            ocr_combinations = self.determine_ocr_languages(detected_langs)
            
            result["context"].append({
                "page": page_num + 1,
                "context": text,
                "detected_languages": detected_langs,
                "ocr_combinations": ocr_combinations
            })
            try:
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()
                img_base64 = base64.b64encode(img_byte_arr).decode('utf-8')
                
                result["image_page"].append({
                    "page": page_num + 1,
                    "imgbase64": img_base64,
                    "detected_languages": detected_langs,
                    "ocr_combinations": ocr_combinations
                })
                print(f"Successfully extracted image from page {page_num + 1}")
                print(f"Detected languages: {detected_langs}")
                print(f"OCR combinations to use: {ocr_combinations}")
                
            except Exception as e:
                print(f"Error processing page {page_num + 1}: {str(e)}")
                continue
        
        doc.close()
        print(f"Total images extracted: {len(result['image_page'])}")
        self.json_extract = result
        return self.json_extract

    def get_reader_for_languages(self, lang_combo):
        """Lấy reader phù hợp với bộ ngôn ngữ"""
        lang_combo = sorted(lang_combo)
        if lang_combo == ['en', 'ja']:
            return self.reader_en_ja
        elif lang_combo == ['en', 'vi']:
            return self.reader_en_vi
        elif lang_combo == ['ja']:
            return self.reader_ja
        elif lang_combo == ['en']:
            return self.reader_en
        elif lang_combo == ['vi']:
            return self.reader_vi
        return self.reader_vi

    def merge_ocr_results(self, results_list):
        """Merge kết quả OCR từ nhiều lần chạy và sắp xếp theo vị trí"""
        if not results_list:
            return []
        merged = {}
        # Merge results từ các lần OCR khác nhau
        for results in results_list:
            for bbox, text, conf in results:
                # Xử lý text: thay thế \n bằng khoảng trắng
                text = text.replace('\n', ' ').strip()
                
                # Bỏ qua text rỗng
                if not text:
                    continue
                # Chuyển các giá trị numpy sang Python native types
                bbox_coords = []
                for point in bbox:
                    bbox_coords.append([float(point[0]), float(point[1])])
                # Tính toán tọa độ trung tâm của bbox
                center_x = (bbox_coords[0][0] + bbox_coords[2][0]) / 2
                center_y = (bbox_coords[0][1] + bbox_coords[2][1]) / 2
                # Tạo key duy nhất cho mỗi vùng text
                bbox_key = tuple(map(lambda x: round(float(x), 2), bbox_coords[0] + bbox_coords[2]))
                if bbox_key not in merged or float(conf) > merged[bbox_key][1]:
                    merged[bbox_key] = (text, float(conf), bbox_coords, center_x, center_y)
        # Chuyển dict thành list và sắp xếp
        results = list(merged.values())
        # Tìm các dòng text dựa trên khoảng cách Y
        line_threshold = 10  # Ngưỡng để xác định cùng dòng
        lines = {}
        for item in results:
            text, conf, bbox, center_x, center_y = item
            # Tìm dòng phù hợp hoặc tạo dòng mới
            line_found = False
            for line_y in lines.keys():
                if abs(center_y - line_y) <= line_threshold:
                    lines[line_y].append(item)
                    line_found = True
                    break
            if not line_found:
                lines[center_y] = [item]
        # Sắp xếp từng dòng theo trục X và sắp xếp các dòng theo trục Y
        sorted_results = []
        for line_y in sorted(lines.keys()):
            # Sắp xếp các phần tử trong dòng theo X
            line_items = sorted(lines[line_y], key=lambda x: x[3])  # x[3] là center_x
            sorted_results.extend(line_items)
        # Chuyển về format ban đầu (bbox, text, conf)
        return [(item[2], item[0], item[1]) for item in sorted_results]

    def format_text_with_newlines(self, merged_results):
        """Format text với xuống dòng dựa trên vị trí Y"""
        if not merged_results:
            return ""
        # Nhóm text theo dòng
        line_threshold = 10
        current_line_y = None
        formatted_text = []
        current_line = []
        for bbox, text, _ in merged_results:
            # Xử lý text: thay thế \n bằng khoảng trắng
            text = text.replace('\n', ' ').strip()
            # Bỏ qua text rỗng
            if not text:
                continue
            center_y = (bbox[0][1] + bbox[2][1]) / 2
            if current_line_y is None:
                current_line_y = center_y
                current_line.append(text)
            elif abs(center_y - current_line_y) <= line_threshold:
                current_line.append(text)
            else:
                # Thêm dòng hiện tại vào kết quả
                formatted_text.append(" ".join(current_line))
                # Bắt đầu dòng mới
                current_line = [text]
                current_line_y = center_y
        # Thêm dòng cuối cùng
        if current_line:
            formatted_text.append(" ".join(current_line))
        # Join tất cả các dòng với khoảng trắng thay vì xuống dòng
        return " ".join(formatted_text)

    def ocr_extract_text_page(self):
        if not self.json_extract:
            return {}
        slide_context = {}
        total_images = len(self.json_extract["image_page"])
        print(f"Processing {total_images} images with OCR")
        for idx, image in enumerate(self.json_extract["image_page"]):
            try:
                page_num = image['page']
                detected_langs = image['detected_languages']
                ocr_combinations = image['ocr_combinations']
                print(f"Processing page {page_num}")
                print(f"Detected languages: {detected_langs}")
                print(f"OCR combinations to use: {ocr_combinations}")
                image_bytes = base64.b64decode(image["imgbase64"])
                all_results = []
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_image_path = os.path.join(temp_dir, f'page_{uuid.uuid4()}.png')
                    with open(temp_image_path, 'wb') as f:
                        f.write(image_bytes)
                    for lang_combo in ocr_combinations:
                        reader = self.get_reader_for_languages(lang_combo)
                        results = reader.readtext(temp_image_path)
                        # Xử lý text trong kết quả OCR
                        processed_results = []
                        for bbox, text, conf in results:
                            text = text.replace('\n', ' ').strip()
                            if text:  # Chỉ thêm vào kết quả nếu text không rỗng
                                processed_results.append((bbox, text, conf))
                        all_results.append(processed_results)
                        print(f"Completed OCR with languages: {lang_combo}")
                    merged_results = self.merge_ocr_results(all_results)
                    # Format text thành một dòng duy nhất
                    formatted_text = self.format_text_with_newlines(merged_results)
                    # Chuyển đổi các giá trị numpy sang Python native types
                    bounding_boxes = [
                        {
                            "bbox": [[float(x), float(y)] for x, y in bbox],
                            "text": text.replace('\n', ' ').strip(),
                            "confidence": float(conf)
                        }
                        for bbox, text, conf in merged_results
                    ]
                    
                    # slide_context[f"slide_{page_num}"] = {
                    #     "text": formatted_text,
                    #     "detected_languages": detected_langs,
                    #     "ocr_combinations": ocr_combinations,
                    #     "bounding_boxes": bounding_boxes
                    # }
                    
                    slide_context[f"slide_{page_num}"] = formatted_text
                    print(f"Successfully processed page {page_num}")
                    
            except Exception as e:
                print(f"Error processing page {page_num}: {str(e)}")
                # slide_context[f"slide_{page_num}"] = {
                #     "text": "",
                #     "detected_languages": detected_langs,
                #     "ocr_combinations": ocr_combinations,
                #     "bounding_boxes": []
                # }
                slide_context[f"slide_{page_num}"] = formatted_text

        return slide_context

    def extract_text_pdf_pymu(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found: {file_path}")
            
        print(f"Processing PDF: {file_path}")
        self.extract_pdf_content(file_path)
        
        print("Processing content with OCR...")
        result = self.ocr_extract_text_page()
            
        return {
            "file_name": self.json_extract['file_name'],
            "pages": result
        }
        
    def save_to_json(self, data, output_path):
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4, cls=NumpyEncoder)

# if __name__ == "__main__":
#     file_path = "/home/nhatthuong/Documents/Thesis/Acne-detection-and-treatment-recommendations/backend/fastapi_all/treatment/doctor_advice/extract_vi/test_vienjna.pdf"
#     output_json = "output_re.json"
#     extract = ExtractTextPDFpyMUPDF()
#     try:
#         print("Starting PDF processing...")
#         time_start = time.time()
#         content = extract.extract_text_pdf_pymu(file_path)
#         time_end = time.time()
#         print("Processing time:", time_end - time_start)
#         print("\nSaving results to JSON...")
#         extract.save_to_json(content, output_json)
#         print(f"Successfully saved content to {output_json}")
#         print("\nProcessing Summary:")
#         print(f"Total pages with content: {len(content['pages'])}")
#     except Exception as e:
#         print(f"Error: {str(e)}")

