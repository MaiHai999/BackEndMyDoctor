

class MessageService:
    def __init__(self, db):
        self.db = db

    def create_models(self):
        class Message(self.db.Model):
            __tablename__ = 'Message'
            id = self.db.Column("ID", self.db.Integer, primary_key=True)
            human = self.db.Column('HUMAN', self.db.Text(), unique=False, nullable=True)
            ai = self.db.Column('AI', self.db.Text(), nullable=True)
            status = self.db.Column('STATUS', self.db.Integer, nullable=True)
            id_conversation = self.db.Column('IDCONVERSATION', self.db.Integer, nullable=True)

        return Message
