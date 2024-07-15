from app.db import session_scope, BaseModel

class DBManager:
    def __init__(self, model):
        if not issubclass(model, BaseModel):
            raise TypeError("Model must be a subclass of BaseModel")
        self.model = model

    def add_record(self, **kwargs):
        with session_scope() as session:
            record = self.model(**kwargs)
            session.add(record)

    def get_all_records(self):
        with session_scope() as session:
            return session.query(self.model).all()

    def get_record_by_id(self, record_id):
        with session_scope() as session:
            return session.query(self.model).filter(self.model.id == record_id).one_or_none()

    def update_record(self, record_id, **kwargs):
        with session_scope() as session:
            record = session.query(self.model).filter(self.model.id == record_id).one_or_none()
            if record:
                for key, value in kwargs.items():
                    setattr(record, key, value)
                session.add(record)
            else:
                print(f"Record with id {record_id} does not exist.")

    def remove_record(self, record_id):
        with session_scope() as session:
            record = session.query(self.model).filter(self.model.id == record_id).one_or_none()
            if record:
                session.delete(record)
            else:
                print(f"Record with id {record_id} does not exist.")