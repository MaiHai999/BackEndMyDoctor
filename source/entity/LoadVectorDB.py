from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import FAISS
import time
import os



class LoadVectorDB:
    def __init__(self):
        path_db = os.environ.get("path_vector_db")
        embedding_model = GPT4AllEmbeddings()
        self.db = FAISS.load_local(path_db, embedding_model)

    def querying(self, query , k = 1):
        docs = self.db.similarity_search(query)
        list_text = [docs[i].page_content for i in range(k)]
        return list_text

    def score_search(self ,query):
        docs_and_scores = self.db.similarity_search_with_score(query)
        list_text_scores = [(doc[0].page_content , doc[1]) for doc in docs_and_scores]
        return list_text_scores

    def get_all_data(self):
        dict_db = self.db.docstore._dict
        for key in dict_db:
            print("Key:",key , "Value:", dict_db[key])

    def get_len_db(self):
        dict_db = self.db.docstore._dict
        return len(dict_db)

    def retriever(self):
        return self.db.as_retriever()

if __name__ == "__main__":
    start_time = time.time()

    path = "../../../asset/database/db_vector_en"
    db = LoadVectorDB(path)

    print(db.get_len_db())

    text = db.querying("covid 19 how many people died", k=2)
    for i in text:
        print(i, end="\n\n\n\n")

    # Kết thúc đo thời gian
    end_time = time.time()

    # Tính thời gian chạy
    execution_time = end_time - start_time
    print("Thời gian chạy:", execution_time, "giây")



