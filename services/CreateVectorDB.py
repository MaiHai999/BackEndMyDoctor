from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import GPT4AllEmbeddings


#khai báo và khởi tạo một số biến
pdf_data_path_vn = "../../asset/dataset/Vietnamese-languageBooks"
pdf_data_path_en = "../../asset/dataset/English-languageBooks"
vector_db_path_vn = "../../asset/database/db_vector_vn"
vector_db_path_en = "../../asset/database/db_vector_en"


# Khai bao loader de quet toan bo thu muc data
loader = DirectoryLoader(pdf_data_path_vn, glob="*.pdf", loader_cls=PyPDFLoader)
documents = loader.load()

#Cắt nhỏ văn bản
text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
chunks = text_splitter.split_documents(documents)

# Embeding
embedding_model = GPT4AllEmbeddings()
db = FAISS.from_documents(chunks, embedding_model)
db.save_local(vector_db_path_vn)











