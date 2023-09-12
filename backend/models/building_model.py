from __future__ import annotations
from sqlalchemy import Integer,  String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.extensions import db


class Building(db.Model):
    __tablename__ = "buildings"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    abbr: Mapped[str | None] = mapped_column(String(10))
    buildingFloors: Mapped[list['Floor']] = relationship(back_populates='bluiding_name', lazy='joined')

    def __repr__(self):
        return f'Building({self.id}, "{self.name}")'
    

class Floor(db.Model):
    __tablename__ = "floors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), index=True)
    abbr: Mapped[str | None] = mapped_column(String(10))
    bluiding_id: Mapped[int] = mapped_column(ForeignKey('buildings.id'), index=True)

    bluiding_name: Mapped[Building] = relationship(back_populates='buildingFloors', lazy='joined')
    floor_OTs: Mapped[list[Ot]] = relationship(back_populates='ot_building_floor_name')

    def __repr__(self):
        return f'Building({self.id}, "{self.name}")'


class Ot(db.Model):
    __tablename__ = "ots"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), index=True)
    abbr: Mapped[str | None] = mapped_column(String(10))
    tables: Mapped[int] = mapped_column(Integer)

    building_floor_id: Mapped[int] = mapped_column(ForeignKey('floors.id'), index=True)
    ot_building_floor_name: Mapped[Floor] = relationship(back_populates='floor_OTs', lazy='joined')

    def __repr__(self):
        return f'Building({self.id}, "{self.name}")'
