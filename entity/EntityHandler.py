


from sqlalchemy.exc import IntegrityError

class EntityHandler:

    @staticmethod
    def save(session, user_instance):
        try:
            session.add(user_instance)
            session.commit()
            result = True
        except IntegrityError as e:
            session.rollback()
            print(f"Error: {e}")
            result = False

        return result

    @staticmethod
    def get_all(session , entity):
        all_entity = session.query(entity).all()
        return all_entity

    @staticmethod
    def get_entity_id(session , entity , id):
        entity_all = session.query(entity).filter_by(id=id).first()
        return entity_all

    @staticmethod
    def update_status(session , entity , id , status):
        try:
            entity_update = session.query(entity).filter_by(id=id).first()
            entity_update.status = status
            session.commit()
            result = True
        except IntegrityError as e:
            session.rollback()
            print(f"Error: {e}")
            result = False

        return result


