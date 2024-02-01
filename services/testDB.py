from BackEnd.source.entity.LoadVectorDB import LoadVectorDB


db = LoadVectorDB()
text = db.querying("Nguyên nhân bệnh đau đầu ")
print(text)