from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import GPT4AllEmbeddings
import os
import glob


#khai báo và khởi tạo một số biến
pdf_data_path_vn = "../../dataset/Vietnamese-languageBooks"
pdf_data_path_en = "../../dataset/English-languageBooks"
vector_db_path_vn = "../../database/db_vector_vn"
vector_db_path_en = "../../database/db_vector_en"


list_file_paths = glob.glob(os.path.join(pdf_data_path_vn, '*.pdf'))
embedding_model = GPT4AllEmbeddings()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)

new_db = FAISS.load_local(vector_db_path_vn, embedding_model)

for path in list_file_paths:
    try:
        print(path)
        loader = PyPDFLoader(path)
        documents = loader.load()

        # Cắt nhỏ văn bản
        chunks = text_splitter.split_documents(documents)

        # Embeding
        db = FAISS.from_documents(chunks, embedding_model)

        #Meger
        new_db.merge_from(db)

    except Exception as e:
        continue

new_db.save_local(vector_db_path_vn)