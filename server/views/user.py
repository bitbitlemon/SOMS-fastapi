from fastapi import APIRouter, Depends
from server.database import engine, SessionLocal
from server.database.user import get_user_profile_by_user_id
from server.models.user import *
from server.controllers.user import *
from log import logger
from server.schemas.user import UserLogin, StudentIdUpdate
from server.models import success_response, error_response

Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.post("/user/login")
async def wx_code_login(user: UserLogin, db: Session = Depends(get_db)):
    """通过wx code获取openid和用户信息"""
    try:
        openid = user_login(db, user.code, user.info, user.iv)
    except Exception as e:
        logger.error(e)
        return error_response(str(e))
    access_token = create_access_token({"openid": openid})
    return success_response({"access_token": access_token, "token_type": "bearer"})


@router.post("/user/set/student")
async def set_student_info(student_info: StudentIdUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """设置学号和归属学院"""
    try:
        update_student_info(db, student_info, user)
        return success_response()
    except Exception as e:
        logger.error(e)
        return error_response(str(e))


@router.get("/user/token")
async def verify_token(user: User = Depends(get_current_user)):
    return success_response()


@router.get("/user/profile")
async def get_user_profile(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        user_profile = get_user_profile_by_user_id(db, user.id)
        user_profile = user_profile.__dict__
        del user_profile['_sa_instance_state']
    except Exception as e:
        logger.error(e)
        return error_response(str(e))
    return success_response(user_profile)




