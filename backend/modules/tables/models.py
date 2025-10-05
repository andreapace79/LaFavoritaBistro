from sqlalchemy import Column, Integer, String, ForeignKey, Enum, CheckConstraint
from sqlalchemy.orm import relationship
from backend.core.db import Base
import enum

class TableStatus(str, enum.Enum):
    free = "free"
    occupied = "occupied"
    reserved = "reserved"
    disabled = "disabled"

class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    area_id = Column(
        Integer,
        ForeignKey("areas.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name = Column(String(100), nullable=False)
    seats = Column(Integer, nullable=False, default=0)
    status = Column(Enum(TableStatus), nullable=False, default=TableStatus.free)

    area = relationship("Area", back_populates="tables")

    __table_args__ = (
        CheckConstraint("seats >= 0", name="ck_tables_seats_nonnegative"),
    )
