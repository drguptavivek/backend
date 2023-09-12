from __future__ import annotations
from datetime import datetime
from typing import List
from sqlalchemy import Integer,  String, Column, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.extensions import db


class Account(db.Model):
    __tablename__ = "accounts"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(50))
    created_by: Mapped[str] = mapped_column(ForeignKey('accounts.id'))
    create_date: Mapped[datetime] = mapped_column(server_default=func.now())
    inactive: Mapped[int] = mapped_column(Integer, server_default='0')
    inactive_date: Mapped[datetime | None] = mapped_column(server_default=func.now())
    inactive_by: Mapped[str | None] = mapped_column(ForeignKey('accounts.id'))

    user_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'))
    accountBelongsToUser: Mapped[User | None] = relationship(back_populates='userAccount')
    AccountHasRoles: Mapped[list[Role]] = relationship(secondary='accounts_roles_table',
                                                       back_populates='RoleAllocatedToAccounts')

    def __repr__(self):
        return f'Account(ID: {self.id}, Name: "{self.username}", deactivated:{self.deactivated} )'


class Role(db.Model):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30),  unique=True, index=True)
    RoleAllocatedToAccounts: Mapped[list[Account]] = relationship(secondary='accounts_roles_table',
                                                                  back_populates="AccountHasRoles")

    def __repr__(self):
        return f'Role({self.id}, "{self.name}")'


class AccountRole(db.Model):
    __tablename__ = "accounts_roles_table"
    account_id = Column(Integer, ForeignKey('accounts.id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('roles.id'), primary_key=True)


class Department(db.Model):
    __tablename__ = "departments"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    abbr: Mapped[str | None] = mapped_column(String(10))
    type: Mapped[str] = mapped_column(String(30))  # department, centre

    departmentUnits: Mapped[list['Unit']] = relationship(back_populates='unitDepartment', lazy='joined')
    departmentUsers: Mapped[list['User']] = relationship(back_populates='userDepartment', lazy='joined')
    departmentHead: Mapped[list[User]] = relationship(secondary='departmentHeads',
                                                      back_populates='userHeadOfDepartment')

    def __repr__(self):
        return f'Department({self.id}, "{self.name}")'


class Unit(db.Model):
    __tablename__ = "units"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30),  unique=True, index=True)
    abbr: Mapped[str] = mapped_column(String(10))
    department_id: Mapped[str] = mapped_column(ForeignKey('departments.id'), index=True)
   
    unitDepartment: Mapped['Department'] = relationship(back_populates='departmentUnits', lazy='joined')
    unitUsers: Mapped[list['User']] = relationship(back_populates='userUnit', lazy='joined')
    unitHead: Mapped[list[User]] = relationship(secondary='unitHeads', back_populates='userHeadOfUnit')

    def __repr__(self):
        return f'Unit({self.id}, "{self.name}")'


class Designation(db.Model):
    __tablename__ = "designations"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50),  unique=True, index=True)
    abbr: Mapped[str] = mapped_column(String(10))
    cadre_id: Mapped[int] = mapped_column(ForeignKey('cadres.id'), index=True)
    
    cadre: Mapped[Cadre] = relationship(back_populates='cadreDesignations')
    designationUsers: Mapped[list['User']] = relationship(back_populates='userDesignation')

    def __repr__(self):
        return f'Designation({self.id}, "{self.name}")'


class Cadre(db.Model):
    __tablename__ = "cadres"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30),  unique=True, index=True)

    cadreDesignations: Mapped[List[Designation]] = relationship(back_populates='cadre')
    cadreUsers: Mapped[list[User]] = relationship(back_populates='userCadre')

    def __repr__(self):
        return f'Cadre({self.id}, "{self.name}")'


class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(String(15), index=True)
    employee_id: Mapped[str] = mapped_column(String(15))
    email: Mapped[str] = mapped_column(String(30), unique=True)
    mobile: Mapped[int] = mapped_column(String(30), nullable=False)
    email2: Mapped[str] = mapped_column(String(30), unique=True)
    email3: Mapped[str] = mapped_column(String(30), unique=True)
    mobile2: Mapped[int] = mapped_column(String(30), nullable=False)
    mobile3: Mapped[int] = mapped_column(String(30), nullable=False)
    officeAddress: Mapped[str | None] = mapped_column(String(60), nullable=False)
    department_id: Mapped[str] = mapped_column(ForeignKey('departments.id'), index=True)
    unit_id: Mapped[str | None] = mapped_column(ForeignKey('units.id'), index=True)  
    designation_id: Mapped[str] = mapped_column(ForeignKey('designations.id'), index=True)    
    designation_group_id: Mapped[str | None] = mapped_column(ForeignKey('cadres.id'), index=True)
    
    create_date: Mapped[datetime] = mapped_column(server_default=func.now())
    inactive: Mapped[int] = mapped_column(Integer, server_default='0')
    inactive_date: Mapped[datetime | None] = mapped_column(server_default=func.now())
    # TO AVOID CIRCULAR REFERENCES, ADDING THE CORRECT ACCOUNT_ID THESE TO BE
    # HANDLED AT PROGRAM LEVEL    
    created_by: Mapped[int | None] = mapped_column(Integer)
    inactive_by: Mapped[int | None] = mapped_column(Integer)

    userDepartment: Mapped[Department] = relationship(back_populates='departmentUsers', lazy='joined') 
    userUnit: Mapped[Unit] = relationship(back_populates='unitUsers', lazy='joined') 
    userDesignation: Mapped[Designation] = relationship(back_populates='designationUsers',  lazy='joined')
    userCadre: Mapped[Cadre] = relationship(back_populates='cadreUsers',  lazy='joined')

    userHeadOfUnit: Mapped[list[Unit]] = relationship(secondary='unitHeads', back_populates="unitHead")
    userHeadOfDepartment: Mapped[list[Department]] = relationship(secondary='departmentHeads',
                                                                  back_populates='departmentHead')
    userAccount: Mapped[List[Account]] = relationship(back_populates='accountBelongsToUser')

    # One user can have multiple accounts

    def __repr__(self):
        return f'User({self.id}, "{self.fullname}")'


class UnitHead(db.Model):
    __tablename__ = "unitHeads"
    unit_id = Column(Integer, ForeignKey('units.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)


class DepartmentHead(db.Model):
    __tablename__ = "departmentHeads"
    department_id = Column(Integer, ForeignKey('departments.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
