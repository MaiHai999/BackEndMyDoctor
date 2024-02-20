

class MessageEntity:
    def __init__(self, HUMAN , AI , STATUS, IDCONVERSATION):
        self._id = ID
        self._human = HUMAN
        self._ai = AI
        self._status = STATUS
        self._id_conversation = IDCONVERSATION


    # Getter và Setter cho thuộc tính ID
    def get_id(self):
        return self._id

    def set_id(self, value):
        self._id = value

    # Getter và Setter cho thuộc tính HUMAN
    def get_human(self):
        return self._human

    def set_human(self, value):
        self._human = value

    # Getter và Setter cho thuộc tính AI
    def get_ai(self):
        return self._ai

    def set_ai(self, value):
        self._ai = value

    # Getter và Setter cho thuộc tính STATUS
    def get_status(self):
        return self._status

    def set_status(self, value):
        self._status = value

    # Getter và Setter cho thuộc tính ID_CONVERSATION
    def get_id_conversation(self):
        return self._id_conversation

    def set_id_conversation(self, value):
        self._id_conversation = value