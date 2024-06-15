from typing import Optional
from sqlalchemy.orm import Session, joinedload
from log import logger
from server.database.user import get_model_by_id
from server.models.entity import StudentClass, Major, College
from server.models.user import UserProfile
from server.schemas.entity import UpdateClass, AddClass, AddCollege, UpdateCollege, UpdateMajor, AddMajor
from utils import ProjectException


def query_all_users(db: Session):
    return db.query(UserProfile).options(
        joinedload(UserProfile.student_class)
        .joinedload(StudentClass.major)
        .joinedload(Major.college)
    ).all()


def query_all_class(db: Session):
    return db.query(StudentClass).options(joinedload(StudentClass.major).joinedload(Major.college)).all()


def query_class_by_id(db: Session, class_id: int):
    return db.query(StudentClass).options(joinedload(StudentClass.major).joinedload(Major.college)).filter(
        StudentClass.id == class_id).first()


def add_class(db: Session, class_data: AddClass):
    new_class = StudentClass(
        name=class_data.name,
        major_id=class_data.major_id
    )
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    return new_class


def update_class(db: Session, class_data: UpdateClass):
    class_to_update = db.query(StudentClass).filter(StudentClass.id == class_data.class_id).first()

    if not class_to_update:
        raise ProjectException(f"班级 ID {class_data.class_id} 不存在")

    if class_data.name is not None:
        class_to_update.name = class_data.name

    if class_data.major_id is not None:
        get_model_by_id(db, Major, class_data.major_id, "专业")
        class_to_update.major_id = class_data.major_id

    db.commit()
    db.refresh(class_to_update)
    return class_to_update


def delete_class(db: Session, class_id: int):
    class_to_delete = db.query(StudentClass).filter(StudentClass.id == class_id).first()
    if not class_to_delete:
        raise ProjectException(f"班级 ID {class_id} 不存在")

    db.delete(class_to_delete)
    db.commit()
    return class_to_delete


# Major 增删查改函数
def add_major(db: Session, major_data: AddMajor):
    new_major = Major(
        name=major_data.name,
        college_id=major_data.college_id
    )
    db.add(new_major)
    db.commit()
    db.refresh(new_major)
    return new_major


def update_major(db: Session, major_data: UpdateMajor):
    major_to_update = db.query(Major).filter(Major.id == major_data.major_id).first()

    if not major_to_update:
        raise ProjectException(f"专业 ID {major_data.major_id} 不存在")

    if major_data.name is not None:
        major_to_update.name = major_data.name

    if major_data.college_id is not None:
        get_model_by_id(db, College, major_data.college_id, "学院")
        major_to_update.college_id = major_data.college_id

    db.commit()
    db.refresh(major_to_update)
    return major_to_update


def delete_major(db: Session, major_id: int):
    major_to_delete = db.query(Major).filter(Major.id == major_id).first()

    if not major_to_delete:
        return None

    db.delete(major_to_delete)
    db.commit()
    return major_to_delete


def query_all_majors(db: Session):
    return db.query(Major).options(joinedload(Major.college)).all()


def query_major_by_id(db: Session, major_id: int):
    return db.query(Major).options(joinedload(Major.college)).filter(Major.id == major_id).first()


# College 增删查改函数
def add_college(db: Session, college_data: AddCollege):
    new_college = College(
        name=college_data.name
    )
    db.add(new_college)
    db.commit()
    db.refresh(new_college)
    return new_college


def update_college(db: Session, college_data: UpdateCollege):
    college_to_update = db.query(College).filter(College.id == college_data.college_id).first()

    if not college_to_update:
        raise ProjectException(f"学院 ID {college_data.college_id} 不存在")

    if college_data.name is not None:
        college_to_update.name = college_data.name

    db.commit()
    db.refresh(college_to_update)
    return college_to_update


def delete_college(db: Session, college_id: int):
    college_to_delete = db.query(College).filter(College.id == college_id).first()

    if not college_to_delete:
        return None

    db.delete(college_to_delete)
    db.commit()
    return college_to_delete


def query_all_colleges(db: Session):
    return db.query(College).all()


def query_college_by_id(db: Session, college_id: int):
    return db.query(College).filter(College.id == college_id).first()
