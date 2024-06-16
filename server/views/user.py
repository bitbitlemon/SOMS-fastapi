from fastapi import APIRouter, Depends
from server.models.user import *
from server.controllers.user import *
from log import logger
from server.schemas.user import UserLogin, UserUpdate, APIResponse
from server.models import success_response, error_response
from utils import ProjectException, object_to_dict

Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.post("/user/login", tags=["user", "login"])
async def wx_code_login(user: UserLogin, db: Session = Depends(get_db)) -> APIResponse:
    """通过wx code获取openid和用户信息"""
    try:
        user_ = user_login(db, user.code, user.info, user.iv)
        access_token = create_access_token({"id": user_.id, "openid": user_.openid})
        return success_response({"access_token": access_token, "token_type": "bearer"})
    except ProjectException as e:
        logger.error(e)
        return error_response(str(e))
    except Exception as e:
        logger.exception(e)
        return error_response("服务器错误，请重试", 500)


@router.post("/user/update", tags=["user", "update"])
async def _update_student_info(student_info: UserUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> APIResponse:
    """更新用户信息"""
    try:
        update_student_info(db, student_info, user)
        return success_response()
    except ProjectException as e:
        logger.error(e)
        return error_response(str(e))
    except Exception as e:
        logger.exception(e)
        return error_response("服务器错误，请重试", 500)


@router.get("/user/token", tags=["user"])
async def verify_token(user: User = Depends(get_current_user)) -> APIResponse:
    """验证token"""
    return success_response()


@router.get("/user/profile", tags=["user", "get"])
async def _get_user_profile(db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> APIResponse:
    """获取用户信息"""
    try:
        user_profile = get_user_profile_by_user_id(db, user.id)
        return success_response(object_to_dict(user_profile))
    except ProjectException as e:
        logger.error(e)
        return error_response(str(e))
    except Exception as e:
        logger.exception(e)
        return error_response("服务器错误，请重试", 500)




