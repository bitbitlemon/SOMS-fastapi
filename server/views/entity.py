from fastapi import APIRouter
from server.database import Base, engine
from server.controllers.user import *
from server.controllers.entity import *
from log import logger
from server.schemas.entity import *
from server.schemas.user import UserUpdate, APIResponse
from server.models import success_response, error_response

Base.metadata.create_all(bind=engine)

router = APIRouter()



@router.post("/entity/user/set", tags=["user", "update"])
async def set_user_info(student_info: SetUserProfile, db: Session = Depends(get_db), user: User = Depends(get_current_user_admin)) -> APIResponse:
    """根据更新用户信息"""
    try:
        update = UserUpdate()
        update.nick_name = student_info.nick_name
        update.avatar_url = student_info.avatar_url
        update.student_id = student_info.student_id
        update.user_type = student_info.user_type
        update.class_id = student_info.class_id
        update_student_info_by_id(db, update, student_info.user_id)
        return success_response()
    except ProjectException as e:
        logger.error(e)
        return error_response(str(e))
    except Exception as e:
        logger.exception(e)
        return error_response("服务器错误，请重试", 500)


@router.get("/entity/class/all", tags=["class", "get"])
async def _get_all_class(db: Session = Depends(get_db), user: User = Depends(get_current_user_admin)) -> APIResponse:
    """获取所有班级信息"""
    try:
        user_profile = get_all_class(db)
        return success_response(user_profile)
    except ProjectException as e:
        logger.error(e)
        return error_response(str(e))
    except Exception as e:
        logger.exception(e)
        return error_response("服务器错误，请重试", 500)


@router.post("/entity/class/get", tags=["class", "get"])
async def _get_class(query_class: QueryClass, db: Session = Depends(get_db), user: User = Depends(get_current_user_admin)) -> APIResponse:
    """获取指定id的班级信息"""
    try:
        student_class = get_class(db, query_class.class_id)
        return success_response(student_class)
    except ProjectException as e:
        logger.error(e)
        return error_response(str(e))
    except Exception as e:
        logger.exception(e)
        return error_response("服务器错误，请重试", 500)


@router.post("/entity/class/add", tags=["class", "add"])
async def _update_class(class_: AddClass, db: Session = Depends(get_db), user: User = Depends(get_current_user_admin)) -> APIResponse:
    """增加班级"""
    try:
        add_class(db, class_)
        return success_response()
    except ProjectException as e:
        logger.error(e)
        return error_response(str(e))
    except Exception as e:
        logger.exception(e)
        return error_response("服务器错误，请重试", 500)


@router.post("/entity/class/update", tags=["class", "update"])
async def _update_class(class_: UpdateClass, db: Session = Depends(get_db), user: User = Depends(get_current_user_admin)) -> APIResponse:
    """更新指定id的班级信息"""
    try:
        update_class(db, class_)
        return success_response()
    except ProjectException as e:
        logger.error(e)
        return error_response(str(e))
    except Exception as e:
        logger.exception(e)
        return error_response("服务器错误，请重试", 500)



@router.post("/entity/class/delete", tags=["class", "delete"])
async def _delete_class(class_: DeleteClass, db: Session = Depends(get_db), user: User = Depends(get_current_user_admin)) -> APIResponse:
    """删除指定id的班级"""
    try:
        delete_class(db, class_.class_id)
        return success_response()
    except ProjectException as e:
        logger.error(e)
        return error_response(str(e))
    except Exception as e:
        logger.exception(e)
        return error_response("服务器错误，请重试", 500)


@router.get("/entity/major/all", tags=["major", "get"])
async def _get_all_major(db: Session = Depends(get_db), user: User = Depends(get_current_user_admin)) -> APIResponse:
    """获取所有专业信息"""
    try:
        majors = get_all_major(db)
        return success_response(majors)
    except ProjectException as e:
        logger.error(e)
        return error_response(str(e))
    except Exception as e:
        logger.exception(e)
        return error_response("服务器错误，请重试", 500)


@router.post("/entity/major/get", tags=["major", "get"])
async def _get_major(query_major: QueryMajor, db: Session = Depends(get_db), user: User = Depends(get_current_user_admin)) -> APIResponse:
    """获取指定id的专业信息"""
    try:
        major = get_major(db, query_major.major_id)
        return success_response(major)
    except ProjectException as e:
        logger.error(e)
        return error_response(str(e))
    except Exception as e:
        logger.exception(e)
        return error_response("服务器错误，请重试", 500)



@router.post("/entity/major/add", tags=["major", "add"])
async def _update_major(major: AddMajor, db: Session = Depends(get_db), user: User = Depends(get_current_user_admin)) -> APIResponse:
    """更新指定id的专业信息"""
    try:
        add_major(db, major)
        return success_response()
    except ProjectException as e:
        logger.error(e)
        return error_response(str(e))
    except Exception as e:
        logger.exception(e)
        return error_response("服务器错误，请重试", 500)


@router.post("/entity/major/update", tags=["major", "update"])
async def _update_major(major: UpdateMajor, db: Session = Depends(get_db), user: User = Depends(get_current_user_admin)) -> APIResponse:
    """更新指定id的专业信息"""
    try:
        update_major(db, major)
        return success_response()
    except ProjectException as e:
        logger.error(e)
        return error_response(str(e))
    except Exception as e:
        logger.exception(e)
        return error_response("服务器错误，请重试", 500)



@router.post("/entity/major/delete", tags=["major", "delete"])
async def _delete_major(major: DeleteMajor, db: Session = Depends(get_db), user: User = Depends(get_current_user_admin)) -> APIResponse:
    """删除指定id的专业"""
    try:
        delete_major(db, major.major_id)
        return success_response()
    except ProjectException as e:
        logger.error(e)
        return error_response(str(e))
    except Exception as e:
        logger.exception(e)
        return error_response("服务器错误，请重试", 500)


@router.get("/entity/college/all", tags=["college", "get"])
async def _get_all_college(db: Session = Depends(get_db), user: User = Depends(get_current_user_admin)) -> APIResponse:
    """获取所有学院信息"""
    try:
        colleges = get_all_college(db)
        return success_response(colleges)
    except ProjectException as e:
        logger.error(e)
        return error_response(str(e))
    except Exception as e:
        logger.exception(e)
        return error_response("服务器错误，请重试", 500)


@router.post("/entity/college/get", tags=["college", "get"])
async def _get_college(query_college: QueryCollege, db: Session = Depends(get_db), user: User = Depends(get_current_user_admin)) -> APIResponse:
    """获取指定id的学院信息"""
    try:
        college = get_college(db, query_college.college_id)
        return success_response(college)
    except ProjectException as e:
        logger.error(e)
        return error_response(str(e))
    except Exception as e:
        logger.exception(e)
        return error_response("服务器错误，请重试", 500)


@router.post("/entity/college/add", tags=["college", "add"])
async def _get_college(college: AddCollege, db: Session = Depends(get_db), user: User = Depends(get_current_user_admin)) -> APIResponse:
    """更新指定id的学院信息"""
    try:
        add_college(db, college)
        return success_response()
    except ProjectException as e:
        logger.error(e)
        return error_response(str(e))
    except Exception as e:
        logger.exception(e)
        return error_response("服务器错误，请重试", 500)


@router.post("/entity/college/update", tags=["college", "update"])
async def _get_college(college: UpdateCollege, db: Session = Depends(get_db), user: User = Depends(get_current_user_admin)) -> APIResponse:
    """更新指定id的学院信息"""
    try:
        update_college(db, college)
        return success_response()
    except ProjectException as e:
        logger.error(e)
        return error_response(str(e))
    except Exception as e:
        logger.exception(e)
        return error_response("服务器错误，请重试", 500)



@router.post("/entity/college/delete", tags=["college", "delete"])
async def _get_class(college: DeleteCollege, db: Session = Depends(get_db), user: User = Depends(get_current_user_admin)) -> APIResponse:
    """删除指定id的专业"""
    try:
        delete_college(db, college.college_id)
        return success_response()
    except ProjectException as e:
        logger.error(e)
        return error_response(str(e))
    except Exception as e:
        logger.exception(e)
        return error_response("服务器错误，请重试", 500)



