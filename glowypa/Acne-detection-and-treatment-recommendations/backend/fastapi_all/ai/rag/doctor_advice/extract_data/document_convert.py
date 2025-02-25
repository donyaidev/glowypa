import json
import logging
from pathlib import Path
import pandas as pd
import yaml
import tempfile
import os

import logging
from docling_core.types.doc import ImageRefMode, PictureItem, TableItem
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import (
    DocumentConverter,
    PdfFormatOption,
    WordFormatOption,
)
from docling.pipeline.simple_pipeline import SimplePipeline
from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline
logger = logging.getLogger(__name__)
class ExtractData: 
    def __init__(self):
        self.conv_results = None
        self.json_result = None
        self.metadata = None
        self.pipeline_option = PdfPipelineOptions()
        self.pipeline_option.images_scale = 0.4
        self.pipeline_option.generate_picture_images = True
        self.doc_converter = (DocumentConverter(allowed_formats=[InputFormat.PDF], 
                format_options={InputFormat.PDF: PdfFormatOption(pipeline_cls=StandardPdfPipeline, pipeline_options=self.pipeline_option)},
            )
        )
        
    def _collect_data_text(self, page_no: str) -> list:
        """Collect data text from json following page"""
        object_page = []
        for object_text in self.json_result["texts"]:
            if page_no == str(object_text['prov'][0]['page_no']):
                bbox = object_text['prov'][0]['bbox']
                object_page.append({
                    'bbx_left': bbox['l'],
                    'bbx_top': bbox['t'],
                    'bbx_right': bbox['r'],
                    'bbx_bottom': bbox['b'],
                    'text': object_text['text']
                })
        return object_page

    def _collect_data_table(self, page_no: str) -> list:
        """Collect data table from json following page"""
        object_page = []
        for table in self.conv_results.document.tables:
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
        return object_page
    
    def _collect_data_pictures(self, page_no: str) -> list:
        """Collect data image and OCR text from json following page"""
        object_page = []
        for object_pictures in self.json_result["pictures"]:
            if page_no == str(object_pictures['prov'][0]['page_no']):
                bbox = object_pictures['prov'][0]['bbox']
                object_page.append({
                    'bbx_left': bbox['l'],
                    'bbx_top': bbox['t'],
                    'bbx_right': bbox['r'],
                    'bbx_bottom': bbox['b'],
                    'uri': object_pictures['image']['uri']
                })
    
    def _collect_data_json_convert(self) -> list[dict]:
        """Text convert and chunking"""
        metadata = {'file_name': self.json_result["origin"]["filename"],'pages': {}}
        texts = ""
        for page_no in self.json_result["pages"]:
            object_page = []
            object_page.extend(self._collect_data_text(page_no))
            object_page.extend(self._collect_data_table(page_no))
            sorted_data = sorted(object_page, key=lambda x: (x['bbx_top'], x['bbx_left']), reverse=True)
            texts = ' '.join(item['text'] for item in sorted_data)
            metadata['pages'][f'slide_{page_no}'] = texts
        return metadata 
        
    def text_from_pdf(self, file_path: str) -> dict:
        self.conv_results = self.doc_converter.convert(Path(file_path))
        try:
            self.json_result = json.loads(json.dumps(self.conv_results.document.export_to_dict()))
        except Exception as e:
            logger.warning(e)
            return
        metadata = self._collect_data_json_convert()
        return metadata
