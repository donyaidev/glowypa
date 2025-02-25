import logging
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredExcelLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
import markdown
from dotenv import load_dotenv
import os
pwwd = '/home/nhatthuong/Documents/Thesis/Acne-detection-and-treatment-recommendations/backend/fastapi_all/'

#load env
dotenv_path = f'{pwwd}/.env'
load_dotenv(dotenv_path=dotenv_path)
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# List of document file paths
document_links = [
    f"{pwwd}ai/rag/documents/acne_treatment_2.docx",
    f"{pwwd}ai/rag/documents/acne_treatment.docx"
]
all_docs = []
try:
    for document_link in document_links:
        try:
            if document_link.endswith('.pdf'):
                loader = PyPDFLoader(document_link)
            elif document_link.endswith('.docx'):
                loader = Docx2txtLoader(document_link) 
            elif document_link.endswith('.xlsx'):
                loader = UnstructuredExcelLoader(document_link)
            else:
                logger.warning(f"Unsupported file format: {document_link}")
                continue

            data = loader.load()
            all_docs.extend(data)
        except Exception as e:
            logger.error(f"Error loading document {document_link}: {e}")
except Exception as e:
    logger.error(f"Error processing document links: {e}")
    raise
# Split documents into chunks
try:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
    docs = text_splitter.split_documents(all_docs)
    print(docs)
except Exception as e:
    logger.error(f"Error splitting documents: {e}")
    raise
# Create embeddings, vectorstore, and chains
try:
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)
    vectorstore = Chroma.from_documents(documents=docs, embedding=embeddings)
    # retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 5,  
            "fetch_k": 5,  
            "lambda_mult": 0.7  
        }
    )
except Exception as e:
    logger.error(f"Error creating embeddings or vectorstore: {e}")
    raise

def main():
    results = retriever.get_relevant_documents('Black head')


if __name__ == '__main__':
    main()
