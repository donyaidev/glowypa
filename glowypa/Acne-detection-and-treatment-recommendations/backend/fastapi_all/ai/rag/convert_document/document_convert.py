import json
import logging
from pathlib import Path
import pandas as pd
import yaml

from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend
from docling.datamodel.base_models import InputFormat
from docling.document_converter import (
    DocumentConverter,
    PdfFormatOption,
    WordFormatOption,
)
from docling.pipeline.simple_pipeline import SimplePipeline
from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline

_log = logging.getLogger(__name__)


def text_from_pdf(file_path: str):
    input_paths = Path(file_path)
    doc_converter = (
        DocumentConverter(allowed_formats=[InputFormat.PDF], 
            format_options={InputFormat.PDF: PdfFormatOption(pipeline_cls=StandardPdfPipeline, backend=PyPdfiumDocumentBackend),InputFormat.DOCX: WordFormatOption(pipeline_cls=SimplePipeline)},
        )
    )
    conv_results = doc_converter.convert(input_paths)
    json_result = json.loads(json.dumps(conv_results.document.export_to_dict()))
    metadata = {'file_name': json_result["origin"]["filename"],'pages': {}}
    texts = ""
    for page in json_result["pages"]:
        page_no = page
        object_page = []
        texts = ""
        #get text
        for object_text in json_result["texts"]:
            if page_no == str(object_text['prov'][0]['page_no']):
                bbox = object_text['prov'][0]['bbox']
                object_page.append({
                    'bbx_left': bbox['l'],
                    'bbx_top': bbox['t'],
                    'bbx_right': bbox['r'],
                    'bbx_bottom': bbox['b'],
                    'text': object_text['text']
                })
        #get table
        for table in conv_results.document.tables:
            if page_no == str(table.prov[0].page_no):
                cleaned_str = ' '.join(table.export_to_dataframe().to_string(index=False).split())
                bbox = table.prov[0].bbox
                object_page.append({
                    'bbx_left': bbox.l,
                    'bbx_top': bbox.t,
                    'bbx_right': bbox.r,
                    'bbx_bottom': bbox.b,
                    'text': cleaned_str
                })
        #sorted follow top bbx 
        sorted_data = sorted(object_page, key=lambda x: (x['bbx_top'], x['bbx_left']), reverse=True)
        # Concatenate all text from sorted_data
        texts = ' '.join(item['text'] for item in sorted_data)
        metadata['pages'][f'slide_{page_no}'] = texts
    print(metadata)

if __name__ == "__main__":
    text_from_pdf('/Users/nhatthuong/Documents/Acne-detection-and-treatment-recommendations/backend/fastapi_all/ai/rag/convert_document/2206.01062.pdf')
