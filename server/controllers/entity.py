from server.database.entity import *
from server.database.user import *
from server.models.entity import StudentClass
from server.schemas.user import UserUpdate
from utils import ProjectException, object_to_dict


def get_all_user(session: Session):
    users = query_all_users(session)
    result = []
    for user in users:
        row = object_to_dict(user)
        if user.student_class:  # 如果关联了班级表
            row.update({
                "class": user.student_class.name,
                "major_id": user.student_class.major_id,
                "major": user.student_class.major.name,
                "college_id": user.student_class.major.college_id,
                "college": user.student_class.major.college.name,
            })
        result.append(row)
    return result


def update_student_info_by_id(session: Session, info: UserUpdate, user_id: int):
    user_profile = get_user_profile_by_user_id(session, user_id=user_id)
    if not user_profile:
        raise ProjectException("错误, 查询不到用户信息!")
    if info.student_id is not None:
        student_id_user_profile = get_user_profile_by_student_id(session, student_id=info.student_id)
        if student_id_user_profile and student_id_user_profile.student_id != info.student_id:
            raise ProjectException("错误, 该学号已存在!")

    # 检查班级id是否存在
    get_model_by_id(session, StudentClass, info.class_id, "班级")

    update_student_profile(session, user_id=user_profile.user_id, info=info)


def get_all_class(session: Session):
    classes = query_all_class(session)
    result = []
    for class_ in classes:
        row = object_to_dict(class_)
        row.update(dict(
            major=class_.major.name,
            college_id=class_.major.college_id,
            college=class_.major.college.name,
        ))
        result.append(row)
    return result


def get_class(session: Session, class_id: int):
    class_ = query_class_by_id(session, class_id)
    if class_:
        row = object_to_dict(class_)
        row.update(dict(
            major=class_.major.name,
            college_id=class_.major.college_id,
            college=class_.major.college.name,
        ))
        return row
    raise ProjectException(f"班级 ID {class_id} 不存在")


def get_all_major(session: Session):
    majors = query_all_majors(session)
    result = []
    for major in majors:
        row = object_to_dict(major)
        row.update(dict(
            college=major.college.name,
        ))
        result.append(row)
    return result


def get_major(session: Session, major_id: int):
    major = query_major_by_id(session, major_id)
    if major:
        row = object_to_dict(major)
        row.update(dict(
            college=major.college.name,
        ))
        return row
    raise ProjectException(f"专业 ID {major_id} 不存在")


def get_all_college(session: Session):
    colleges = query_all_colleges(session)
    result = []
    for college in colleges:
        row = object_to_dict(college)
        result.append(row)
    return result


def get_college(session: Session, college_id: int):
    college = query_college_by_id(session, college_id)
    if college:
        row = object_to_dict(college)
        return row
    raise ProjectException(f"学院 ID {college_id} 不存在")
