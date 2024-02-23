
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String , DateTime

Base = declarative_base()

class Conversation(Base):
    __tablename__ = "Conversations"
    id = Column('ID' ,Integer, primary_key=True)
    title = Column('TITLE',String(300),nullable=True)
    create_date = Column('CREATDATE' , DateTime , nullable=True)
    id_user = Column('IDUSER' , Integer , nullable=True)
    status = Column('STATUS', Integer , nullable=True)

    def set_attribute(self , title, create_date, id_user, status):
        self.title = title
        self.create_date = create_date
        self.id_user = id_user
        self.status = status



