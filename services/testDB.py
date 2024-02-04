from BackEnd.source.entity.LoadVectorDB import LoadVectorDB

path = "../../asset/database/db_vector_en"
db = LoadVectorDB(path)

# print(db.get_len_db())


text = db.querying("covid 19 how many people died" , k = 2)
for i in text:
    print(i , end="\n\n\n\n")
