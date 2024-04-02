

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from BackEnd.source.source.services.models import User
from BackEnd.source.source.entity.EntityHandler import EntityHandler

class MyConnectPro:
    def __init__(self ,user , password, database = 'MyDoctor', host = 'localhost' , port = 3306):
        self.host = host
        self.username = user
        self.password = password
        self.database = database
        self.port = port

    def connect(self):
        connection_url = f"mysql+mysqlconnector://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        self.engine = create_engine(connection_url, echo=True)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        session = self.Session()
        return session

    def execute_query(self, query):
        if not self.engine or not self.Session:
            self.connect()
        session = self.Session()
        try:
            result = session.execute(text(query))
            return result.fetchall()
        finally:
            session.close()

# Example usage:
if __name__ == "__main__":
    # Initialize DatabaseManager with initial connection details
    db_manager = MyConnectPro('root', '01692032691')

    # Connect to the database
    db_manager.connect()

    session = db_manager.get_session()

    users = User()
    users.set_attribute("haimai@gmail.com" , "99999" , None , None , 2)
    EntityHandler.save(session , users)

    all_users = EntityHandler.get_all(session , User)

    print("\n\n\n")
    # In ra thông tin của các user
    for user in all_users:
        print(f"ID: {user.id}, Email: {user.email}")




