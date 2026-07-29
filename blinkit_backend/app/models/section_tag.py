import uuid

from sqlalchemy import (
    Column,
    UUID,
    ForeignKey,
    UniqueConstraint,
)

from sqlalchemy.orm import relationship
from sqlalchemy import Integer
from app.db.database import Base


class SectionTag(Base):
    __tablename__ = "section_tags"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    section_id = Column(
        UUID(as_uuid=True),
        ForeignKey("sections.id"),
        nullable=False,
    )

    tag_id = Column(
        UUID(as_uuid=True),
        ForeignKey("tags.id"),
        nullable=False,
    )

    group_no = Column(
        Integer,
        nullable=False,
        default=1
    )

    section = relationship(
        "Section",
        back_populates="tags",
    )

    tag = relationship(
        "Tag",
        back_populates="sections",
    )


    __table_args__ = (
        UniqueConstraint(
            "section_id",
            "tag_id",
            name="uq_section_tag",
        ),
    )