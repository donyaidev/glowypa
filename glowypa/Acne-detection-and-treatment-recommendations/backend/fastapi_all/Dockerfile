# FROM python:3.12.4

# WORKDIR /app

# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
FROM python:3.12.4

# Cài đặt các phụ thuộc hệ thống
RUN apt-get update && apt-get install -y \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Đặt thư mục làm việc
WORKDIR /app

# Sao chép tệp yêu cầu và cài đặt các phụ thuộc
COPY requirements.txt .
RUN pip install -r requirements.txt
# --no-cache-dir
# Sao chép mã ứng dụng
COPY . .

# Lệnh để chạy ứng dụng
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
