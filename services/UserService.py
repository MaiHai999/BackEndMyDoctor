
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String , DateTime
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()



class User(Base):
    __tablename__ = "User"
    id = Column('ID' ,Integer, primary_key=True)
    email =  Column('EMAIL',String(120),nullable=True)
    password =  Column('PASSWORD',String(30),nullable=True)
    id_facebook =  Column('IDFACEBOOK',String(150),nullable=True)
    id_google =  Column('IDGOOGLE',String(150),nullable=True)
    role = Column('ROLE' ,Integer , nullable=True)

    def set_attribute(self, email, password, id_facebook, id_google , role):
        self.email = email
        self.password = generate_password_hash(password)
        self.id_facebook = id_facebook
        self.id_google = id_google
        self.role = role
