import mysql.connector

class MyConnect:
    def __init__(self ,user , password, database = 'MyDoctor', host = 'localhost'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Connected to MySQL database successfully!")
        except mysql.connector.Error as err:
            print("Error: ", err)

    def close(self):
        if self.connection:
            self.connection.close()
            print("Connection closed.")

    def execute_query(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print("Error: ", err)
        finally:
            cursor.close()


if __name__ == "__main__":
    user = 'root'
    password = '01692032691'

    my_connect = MyConnect(user ,password)
    my_connect.connect()

    query = "SELECT * FROM MyDoctor.User;"
    result = my_connect.execute_query(query)
    print("Result: ", result)
