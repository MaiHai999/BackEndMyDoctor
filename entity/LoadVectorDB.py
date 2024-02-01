
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import FAISS


class LoadVectorDB:
    def __init__(self,path_vector_db = "../../asset/database/db_vector_vn"):
        embedding_model = GPT4AllEmbeddings()
        self.db = FAISS.load_local(path_vector_db, embedding_model)

    def querying(self, query , k = 1):
        docs = self.db.similarity_search(query)
        list_text = [docs[i].page_content for i in range(k)]
        return list_text

    def score_search(self ,query, k = 1 ):
        docs_and_scores = self.db.similarity_search_with_score(query)
        list_text_scores = [(docs_and_scores[0][i].page_content ,docs_and_scores[1]) for i in range(k)]
        return list_text_scores

    







