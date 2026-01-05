from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.repository = InMemoryRepository()

    def create(self, obj):
        return self.repository.add(obj)

    def get(self, obj_id):
        return self.repository.get(obj_id)

    def get_all(self):
        return self.repository.get_all()

    def update(self, obj_id, data):
        return self.repository.update(obj_id, data)

    def delete(self, obj_id):
        return self.repository.delete(obj_id)
