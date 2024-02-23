


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
        all_entity = session.query(entity).all()
        return all_entity

    @staticmethod
    def get_entity_id(session , entity , id):
        entity_all = session.query(entity).filter_by(id=id).all()
        return entity_all[0]

