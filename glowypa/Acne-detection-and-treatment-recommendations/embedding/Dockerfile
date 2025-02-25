FROM python:3.12.4

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# # Expose the port that the app runs on
# EXPOSE 8888

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8888"]
