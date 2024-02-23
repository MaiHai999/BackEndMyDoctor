

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()



class BlockToken(Base):
    __tablename__ = "BlockToken"
    id = Column('ID' ,Integer, primary_key=True)
    jti = Column('JTI',String(300),nullable=False)

    def set_attribute(self, jti):
        self.jti = jti



