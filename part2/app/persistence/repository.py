class InMemoryRepository:
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        if not hasattr(obj, "id"):
            raise ValueError("Object must have an id attribute")
        self._storage[obj.id] = obj
        return obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if not obj:
            return None

        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)

        if hasattr(obj, "update"):
            obj.update()

        return obj

    def delete(self, obj_id):
        return self._storage.pop(obj_id, None)
