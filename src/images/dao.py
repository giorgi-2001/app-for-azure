from threading import Lock

from sqlalchemy import select, delete

from database import SessionLocal
from .model import Image


mutex = Lock()


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        with mutex:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class ImageDAO(metaclass=SingletonMeta):
    def __init__(self):
        self.session_maker = SessionLocal
        self.model = Image

    def get_all_images(self):
        with self.session_maker() as session:
            query = select(self.model).order_by(self.model.created_at)
            result = session.execute(query)
            yield from result.scalars()

    def get_image_by_id(self, image_id: int):
        with self.session_maker() as session:
            query = select(self.model).where(self.model.image_id == image_id)
            result = session.execute(query)
            return result.scalar_one_or_none()

    def create_image(self, image_data):
        with self.session_maker() as session:
            with session.begin():
                new_img = self.model(**image_data)
                session.add(new_img)
                session.commit()
            session.refresh(new_img)
            return new_img

    def delete_image(self, image_id: int):
        with self.session_maker() as session:
            with session.begin():
                query = delete(self.model).where(self.model.image_id == image_id)
                session.execute(query)
                session.commit
            return image_id
