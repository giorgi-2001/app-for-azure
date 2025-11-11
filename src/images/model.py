from typing import Annotated

from sqlalchemy.orm import Mapped, mapped_column

from database import Base


int_pk = Annotated[int, mapped_column(primary_key=True, index=True)]

text = Annotated[str, mapped_column(nullable=False)]
number = Annotated[int, mapped_column(nullable=False)]


class Image(Base):
    image_id: Mapped[int_pk]
    name: Mapped[text]
    type: Mapped[text]
    size: Mapped[number]

    def __repr__(self):
        return f"<Image name={self.name} type={self.type} size={self.size}>"
