



class ConversationEntity:
    def __init__(self,ID,TITLE , CREATDATE ,IDUSER , STATUS ):
        self._id = ID
        self._title = TITLE
        self._create_date = CREATDATE
        self._id_user = IDUSER
        self._status = STATUS

    # Getter và Setter cho thuộc tính ID
    def get_id(self):
        return self._id

    def set_id(self, value):
        self._id = value

    # Getter và Setter cho thuộc tính TITLE
    def get_title(self):
        return self._title

    def set_title(self, value):
        self._title = value

    # Getter và Setter cho thuộc tính CREATE_DATE
    def get_create_date(self):
        return self._create_date

    def set_create_date(self, value):
        self._create_date = value

    # Getter và Setter cho thuộc tính ID_USER
    def get_id_user(self):
        return self._id_user

    def set_id_user(self, value):
        self._id_user = value

    # Getter và Setter cho thuộc tính STATUS
    def get_status(self):
        return self._status

    def set_status(self, value):
        self._status = value
