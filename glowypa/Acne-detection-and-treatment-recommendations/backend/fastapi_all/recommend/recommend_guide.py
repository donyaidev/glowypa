import os
from openai import OpenAI
from dotenv import load_dotenv
import markdown
import logging
load_dotenv()
import json
import re
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import numpy as np
import torch

import requests


class RecommendGuide:
    def __init__(self):
        self._token = os.getenv('GITHUB_TOKEN')
        self.endpoint = "https://models.inference.ai.azure.com"
        self.model_name = "gpt-4o"
        
    def embeddding_calling(self, input_data: str):
        url_call = "http://acne-detection-and-treatment-recommendations-embedding-1:8888/get_embedding"
        print("input dataa", input_data)
        try:
            response = requests.post(url_call, json={"text": input_data})
            if response.status_code == 200:
                embeddding_text = response.json()['embedding']
                return np.array(embeddding_text)
        except BaseException as e:
            logging.error(f"Error: {e}")
        
    def remove_newlines(self, input_string):
        """
        Remove newlines from a string and normalize spaces
        """
        if not isinstance(input_string, str):
            input_string = str(input_string)
        # Remove newlines and normalize spaces
        cleaned = input_string.replace('\n', ' ').replace('\r', ' ')
        # Remove multiple spaces
        cleaned = ' '.join(cleaned.split())
        
        return cleaned
      
    def treatment_gpt_acne_detect(self, treatment_routine):
        client = OpenAI(
            base_url=self.endpoint,
            api_key=self._token,
        )
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": """Tôi là Bác sĩ Nguyen GlowyPa, chuyên gia da liễu đồng hành cùng GlowyPa. Tôi sẽ hướng dẫn chi tiết liệu trình skincare được thiết kế riêng cho bạn.

                    LƯU Ý QUAN TRỌNG:
                    1. Thứ tự sử dụng sản phẩm:
                    - Bước 1: [step] - [product_name] ... - [cách dùng]
                    - Bước 2: [step] - [product_name] ... - [cách dùng]
                    [...]
                    
                    2. Tần suất sử dụng:
                    - Sản phẩm [product_name]: ... lần/tuần
                    - Sản phẩm [product_name]: ... lần/ngày
                    [...]

                    3. Những điều cần tránh:
                    - Không kết hợp ... với ...
                    - Không sử dụng ... khi ...
                    [...]

                    4. Cách xử lý khi có kích ứng:
                    - Dấu hiệu nhận biết
                    - Các bước xử lý
                    - Khi nào cần gặp bác sĩ

                    5. Tips bổ sung:
                    - Chế độ ăn uống hỗ trợ
                    - Thói quen sinh hoạt
                    - Các yếu tố môi trường cần lưu ý"""

                },
                {
                    "role": "user",
                    "content": f"""Đây là liệu trình của bạn, bao gồm các sản phẩm: {treatment_routine}, lưu ý không trả về link hình ảnh, cũng như link sản phẩm!"""
                }
            ],
            temperature=0.8,  # Giữ mức độ sáng tạo vừa phải
            top_p=0.1,  # Đảm bảo tính nhất quán trong câu trả lời
            presence_penalty=0.1,  # Tránh lặp lại thông tin
            frequency_penalty=0.1,  # Đa dạng từ ngữ sử dụng
            max_tokens=4000,  # Đủ độ dài ch    o hướng dẫn chi tiết
            stop=["Note:", "Warning:", "Caution:"],  # Ngắt câu trả lời tại các điểm phù hợp
            model="gpt-4o-mini"  # Sử dụng model phù hợp
        )
        args = response.choices[0].message.content
        # args = self.remove_newlines(args)
        return args
    
    def calculate_cosine_get_top_5(self, routines, messageUser):
        embedding_messageUser = self.embeddding_calling(messageUser)
        # Chuyển numpy array sang torch tensor
        embedding_messageUser = torch.from_numpy(embedding_messageUser)

        for routine in routines:
            embedding_context = self.embeddding_calling(routine['context'])
            # Chuyển numpy array sang torch tensor
            embedding_context = torch.from_numpy(embedding_context)
            
            calculate_cosine = torch.cosine_similarity(
                embedding_messageUser.unsqueeze(0),
                embedding_context.unsqueeze(0),
                dim=1
            )
            routine['cosine_score'] = calculate_cosine.item()
        top_5 = sorted(routines, 
                    key=lambda x: x['cosine_score'], 
                    reverse=True)[:5]
        return top_5

    
    def calculate_total_likes_get_top(self, routines):
        def count_routine_likes(routine):
            total_likes = 0
            morning_products = routine.get('daily_routine', {}).get('morning', [])
            for product in morning_products:
                total_likes += product.get('like', 0)
            evening_products = routine.get('daily_routine', {}).get('evening', [])
            for product in evening_products:
                total_likes += product.get('like', 0)
            return total_likes
        routines_with_total = []
        for routine in routines:
            total_likes = count_routine_likes(routine)
            routines_with_total.append({
                'routine': routine,
                'total_likes': total_likes
            })
        top_routine = max(routines_with_total, key=lambda x: x['total_likes'])
        return top_routine['routine']

  

if __name__ == "__main__":
    rcm = RecommendGuide()
    treatment_routine = {
            "context": "",
            "acne_treatment": "acne_scars",
            "daily_routine": {
            "morning": [
            {
                "step": "Cleanser",
                "product": "Sanctuary Spa's Triple Cleansing Mousse",
                "usage": "Use to cleanse your face.",
                "link": "https://shopee.vn/-Date-9-21-Mousse-r%E1%BB%ADa-m%E1%BA%B7t-tr%E1%BA%AFng-da-AHA-Sanctuary-Spa-Triple-Cleansing-Mousse-150ml-i.1127550.7073380259",
                "image": "https://www.dropbox.com/scl/fi/rvpds2lhoge17xguzx5j3/cleanser.jpg?rlkey=mfkiz3m3otwva5i37qytxgxa4&st=5bivyeoa&dl=1",
                "like": 999,
            },
            {
                "step": "Exfoliator (1-2 times a week)",
                "product": "The Ordinary's Lactic Acid 10% + HA Serum",
                "usage":
                "Use after cleansing, but only in the morning if not microneedling that day. If microneedling, use in the evening.",
                "link": "https://shopee.vn/Tinh-ch%E1%BA%A5t-The-Ordinary-Lactic-Acid-5-10-HA-c%E1%BA%A5p-n%C6%B0%E1%BB%9Bc-s%C3%A1ng-m%E1%BB%8Bn-da-(Bill-Canada-US)-Cila-House-i.249374.1296069913?sp_atk=f94c5d1d-a900-462c-80ff-a8c7cd7b4ec3&xptdk=f94c5d1d-a900-462c-80ff-a8c7cd7b4ec3",
                "image": "https://www.dropbox.com/scl/fi/41z1lrh7mozhdyvr93jgr/cream-day.jpg?rlkey=3l5lrbzyu3js5ghod1m2nvtjv&st=g3kpk5qo&dl=1",
                "like": 999,

            },
            {
                "step": "Serum",
                "product": "Pixi Collagen and Retinol Serum",
                "usage": "Apply after exfoliating or after cleansing.",
                "link": "https://www.pixibeauty.com/products/collagen-retinol-serum?srsltid=AfmBOoq_B-2c7Urqjh2WTsih6-Zi_-Ug8QOpDyvXYAk42mqsD4pDwdpg",
                "image": "https://www.dropbox.com/scl/fi/e7h7olov88w7ompyqsh0p/serum.jpg?rlkey=2w2pt2tfhmz6v1gu03yvzchac&st=am9qsd69&dl=1",
                "like": 999,
            },
            {
                "step": "Day Moisturizer",
                "product": "Nivea's Oil Free Face Cream",
                "usage": "Use to keep your skin hydrated.",
                "link": "https://www.amazon.de/-/en/Nivea-Visage-Oil-Free-Face-Milk/dp/B001RYSGEA",
                "image": "https://www.dropbox.com/scl/fi/41z1lrh7mozhdyvr93jgr/cream-day.jpg?rlkey=3l5lrbzyu3js5ghod1m2nvtjv&st=cp5rze7e&dl=1",
                "like": 999,
            },
            {
                "step": "Sunscreen",
                "product": "Skin Defence SPF 50++",
                "usage":"Essential to use in the morning to protect your skin from UV damage.",
                "link": "https://www.thebodyshop.com.vn/kem-chong-nang-skin-defence-multi-protection-light-essence-60ml.html",
                "image": "https://www.dropbox.com/scl/fi/t3ne18inbphk1efq8p1wm/sunscreen.jpg?rlkey=x15f2kjatct6vix0g4zr3btu4&st=o8guq384&dl=1",
                "like": 999,
            },
            ],
            "evening": [
            {
                "step": "Cleanser",
                "product": "Sanctuary Spa's Triple Cleansing Mousse",
                "usage": "Cleanse your face before bed.",
                "link": "https://shopee.vn/-Date-9-21-Mousse-r%E1%BB%ADa-m%E1%BA%B7t-tr%E1%BA%AFng-da-AHA-Sanctuary-Spa-Triple-Cleansing-Mousse-150ml-i.1127550.7073380259",
                "image": "https://www.dropbox.com/scl/fi/6xx4vyukfeh4asm9qnuyu/celtafill.png?rlkey=mhn98m9ganau9czojax3p8cxl&st=ctklg0h5&dl=1",
                "like": 999,
            },
            {
                "step": "Exfoliator (1-2 times a week)",
                "product": "The Ordinary's Lactic Acid 10% + HA Serum",
                "usage": "Use as mentioned above.",
                "link": "https://shopee.vn/Tinh-ch%E1%BA%A5t-The-Ordinary-Lactic-Acid-5-10-HA-c%E1%BA%A5p-n%C6%B0%E1%BB%9Bc-s%C3%A1ng-m%E1%BB%8Bn-da-(Bill-Canada-US)-Cila-House-i.249374.1296069913?sp_atk=f94c5d1d-a900-462c-80ff-a8c7cd7b4ec3&xptdk=f94c5d1d-a900-462c-80ff-a8c7cd7b4ec3",
                "image": "https://www.dropbox.com/scl/fi/hv7xibg01q4nvm0md08xn/exfoliator.png?rlkey=yrsq1bzqzvspsqo6qs2hedmr6&st=8ylo37kr&dl=1",
                "like": 999,
            },
            {
                "step": "Serum",
                "product": "Pixi Collagen and Retinol Serum",
                "usage": "Apply after exfoliating.",
                "link": "https://www.pixibeauty.com/products/collagen-retinol-serum?srsltid=AfmBOoq_B-2c7Urqjh2WTsih6-Zi_-Ug8QOpDyvXYAk42mqsD4pDwdpg",
                "image": "https://www.dropbox.com/scl/fi/e7h7olov88w7ompyqsh0p/serum.jpg?rlkey=2w2pt2tfhmz6v1gu03yvzchac&st=fejizr2l&dl=1",
                "like": 999,
            },
            {
                "step": "Night Moisturizer",
                "product": "CeraVe Moisturizing Cream",
                "usage": "Hydrate and restore your skin overnight.",
                "link": "https://shopee.vn/Kem-D%C6%B0%E1%BB%A1ng-%E1%BA%A8m-D%C3%A0nh-Cho-Da-Kh%C3%B4-Cerave-454G-i.152872415.18854062290?sp_atk=c594f888-9457-4708-b1c3-e7a008b3cbc7&xptdk=c594f888-9457-4708-b1c3-e7a008b3cbc7",
                "image": "https://www.dropbox.com/scl/fi/2k2k992r4oys0j6obdis9/cream-night.jpg?rlkey=n6cx0lm41km6ubfnshc67c6ci&st=yj1dax26&dl=1",
                "like": 999,
            },
            ],
      },
    },
    rcm.treatment_gpt_acne_detect(treatment_routine)