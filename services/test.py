from langchain.retrievers.multi_query import MultiQueryRetriever
from BackEnd.source.entity.LoadVectorDB import LoadVectorDB
from BackEnd.source.entity.LoadLLM import LoadModel
import logging



pathDB = "../../asset/database/db_vector_en"
pathLLM = "../../asset/models/vinallama-7b-chat_q5_0.gguf"

db = LoadVectorDB(pathDB)
llm = LoadModel.load_ctransformers(pathLLM)

question = "xin chào "
retriever_from_llm = MultiQueryRetriever.from_llm(retriever=db.retriever() , llm=llm)

# Set logging for the queries
logging.basicConfig()
logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)

unique_docs = retriever_from_llm.get_relevant_documents(query=question)
len(unique_docs)