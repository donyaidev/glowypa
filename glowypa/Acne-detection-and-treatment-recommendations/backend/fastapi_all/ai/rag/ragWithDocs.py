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
    # "/home/nhatthuong/Documents/Thesis/Acne-detection-and-treatment-recommendations/backend/fastapi_all/ai/rag/doctor_advice/storage/Acne_Vulgaris.pdf"
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
except Exception as e:
    logger.error(f"Error splitting documents: {e}")
    raise
# Create embeddings, vectorstore, and chains
try:
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)
    vectorstore = Chroma.from_documents(documents=docs, embedding=embeddings)
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
except Exception as e:
    logger.error(f"Error creating embeddings or vectorstore: {e}")
    raise
# Create language model and chains
try:
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.3, max_tokens=500, google_api_key=GOOGLE_API_KEY)
except Exception as e:
    logger.error(f"Error initializing language model: {e}")
    raise
# Create chains system prompt
system_prompt = (
"Bạn là trợ lý cho các nhiệm vụ trả lời câu hỏi. hãy sử dụng tiếng Việt Nam"
"Sử dụng các phần sau đây của ngữ cảnh đã thu thập được để trả lời "
"Câu hỏi. Nếu bạn không biết câu trả lời, hãy nói rằng bạn "
"không biết." 
"Vui lòng trả lời bằng tiếng Việt và không sử dụng từ ngữ không phù hợp."
"Bạn là trợ lý của Glowypa chuyên gia về điều trị tư vấn mụn, nếu có ai hỏi bạn là ai thì hãy trả lời"
"Nếu chưa biết loại mụn gì của người bệnh thì hãy nói người bệnh rằng, Bạn hãy sử dụng chức năng Ance Scan Daily của Glowypa để xác định loại mụn của mình và bật chức năng Medical record để tôi có thể truy cập và đưa câu trả lời"
"Không khuyên người dùng đi bác sĩ nếu tình trạng mụn có thể tự chữa được (mức độ mụn không tự chữa được mới khuyên đi bác sĩ)"
"Glowypa đang cung cấp bạn thông tin điều trị mụn như một bác sĩ tư vấn mụn, hãy cung cấp cho người dùng những kiến thức bạn có, bạn đang là một bác sĩ của Glowypa và bạn là người tư vấn trực tiếp"
"\n\n"
"{context}"
)


#multi agent 

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

try:
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
except Exception as e:
    logger.error(f"Error creating chains: {e}")
    raise

def remove_newlines(input_string):
    return input_string.replace('\n', '')

def chatgpt_response_to_html(response_text):
    """
    Convert ChatGPT's response into HTML formatted text.
    Args:
        response_text (str): The text response from ChatGPT.
    Returns:
        str: HTML formatted string.
    """
    html_output = markdown.markdown(response_text)
    return html_output

def mainChat(question, chatHistoryCache, medical_db):
    try:
        full_input = medical_db + chatHistoryCache + "\nDưới đây là câu hỏi mới\n" + question
        response = rag_chain.invoke({"input": full_input, "system": system_prompt})
        markdown_tag = chatgpt_response_to_html(response["answer"])
        answer = remove_newlines(markdown_tag)
        return answer
    except Exception as e:
        logger.error(f"Error during chat invocation: {e}")
        return "<p>Xin lỗi, đã xảy ra lỗi khi xử lý yêu cầu của bạn.</p>"



