from sentence_transformers import SentenceTransformer
from huggingface_hub import login
import os

def download_model():
    # Login to Hugging Face
    login(token="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")
    print("Login successful")

    # Create model cache directory if it doesn't exist
    os.makedirs("model_cache", exist_ok=True)

    try:
        # Download and save model
        print("Downloading model...")
        model = SentenceTransformer('BAAI/bge-m3')
        
        # Save model
        print("Saving model to model_cache directory...")
        model.save('model_cache')
        print("Model saved successfully!")
        
        # Verify the saved model
        print("Verifying saved model...")
        test_model = SentenceTransformer('model_cache')
        print("Model verified successfully!")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    download_model()
