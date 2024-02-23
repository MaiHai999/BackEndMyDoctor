
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text

Base = declarative_base()

class Message(Base):
    id = Column('ID' ,Integer, primary_key=True)
    human = Column('HUMAN' ,Text)
    ai = Column('AI' ,Text)
    status = Column('STATUS' ,Integer)
    id_conversation = Column('IDCONVERSATION' ,Integer)

    def set_attribute(self ,human , ai , status , id_conversation):
        self.human = human
        self.ai = ai
        self.status = status
        self.id_conversation = id_conversation
