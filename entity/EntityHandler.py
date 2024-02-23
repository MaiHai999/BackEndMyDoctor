


from sqlalchemy.exc import IntegrityError

class EntityHandler:

    @staticmethod
    def save(session, user_instance):
        try:
            session.add(user_instance)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            print(f"Error: {e}")

    @staticmethod
    def get_all(session , entity):
        all_users = session.query(entity).all()
        return all_users
