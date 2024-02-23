
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String , DateTime , Text
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()



class User(Base):
    __tablename__ = "User"
    id = Column('ID' ,Integer, primary_key=True)
    email =  Column('EMAIL',String(120),nullable=True)
    password =  Column('PASSWORD',String(30),nullable=True)
    id_facebook =  Column('IDFACEBOOK',String(150),nullable=True)
    id_google =  Column('IDGOOGLE',String(150),nullable=True)
    role = Column('ROLE' ,Integer , nullable=True)

    conversations = relationship('Conversation' , backref='user')

    def set_attribute(self, email, password, id_facebook, id_google , role):
        self.email = email
        self.password = generate_password_hash(password)
        self.id_facebook = id_facebook
        self.id_google = id_google
        self.role = role

class Conversation(Base):
    __tablename__ = "Conversations"
    id = Column('ID' ,Integer, primary_key=True)
    title = Column('TITLE',String(300),nullable=True)
    create_date = Column('CREATDATE' , DateTime , nullable=True)
    id_user = Column('IDUSER',Integer , ForeignKey('User.ID') , nullable=True)
    status = Column('STATUS', Integer , nullable=True)

    messages = relationship('Message' , backref='mess')

    def set_attribute(self , title, create_date, id_user, status):
        self.title = title
        self.create_date = create_date
        self.id_user = id_user
        self.status = status


class Message(Base):
    __tablename__ = "Message"
    id = Column('ID' ,Integer, primary_key=True)
    human = Column('HUMAN' ,Text)
    ai = Column('AI' ,Text)
    status = Column('STATUS' ,Integer)
    id_conversation = Column('IDCONVERSATION' ,Integer,ForeignKey('Conversations.ID'))

    def set_attribute(self ,human , ai , status , id_conversation):
        self.human = human
        self.ai = ai
        self.status = status
        self.id_conversation = id_conversation


class BlockToken(Base):
    __tablename__ = "BlockToken"
    id = Column('ID' ,Integer, primary_key=True)
    jti = Column('JTI',String(300),nullable=False)

    def set_attribute(self, jti):
        self.jti = jti
