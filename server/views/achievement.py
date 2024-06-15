from fastapi import APIRouter
from server.controllers.achievement import *
from server.controllers.user import get_db, Depends, get_current_user_admin
from server.database import Base, engine
from log import logger
from server.schemas.achievement import *
from server.schemas.user import APIResponse
from server.models import success_response, error_response





Base.metadata.create_all(bind=engine)
router = APIRouter()



@router.get("/achievement/achievement/all", tags=["achievement", "get"])
async def _get_all_class(db: Session = Depends(get_db), user: User = Depends(get_current_user_admin)) -> APIResponse:
    """获取所有班级信息"""
    try:
        achievement_infos = get_all_achievement_and_info(db)
        return success_response(achievement_infos)
    except ProjectException as e:
        logger.error(e)
        return error_response(str(e))
    except Exception as e:
        logger.exception(e)
        return error_response("服务器错误，请重试", 500)


@router.post("/achievement/achievement/get", tags=["achievement", "get"])
async def _get_class(query_achievement: AchievementBase, db: Session = Depends(get_db), user: User = Depends(get_current_user_admin)) -> APIResponse:
    """获取指定id的班级信息"""
    try:
        achievement_info = get_achievement_and_info_by_id(db, query_achievement.id)
        return success_response(achievement_info)
    except ProjectException as e:
        logger.error(e)
        return error_response(str(e))
    except Exception as e:
        logger.exception(e)
        return error_response("服务器错误，请重试", 500)


@router.post("/achievement/achievement/add", tags=["achievement", "add"])
async def _update_class(achievement: AchievementCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user_admin)) -> APIResponse:
    """增加成果表"""
    try:
        add_achievement(db, achievement)
        return success_response()
    except ProjectException as e:
        logger.error(e)
        return error_response(str(e))
    except Exception as e:
        logger.exception(e)
        return error_response("服务器错误，请重试", 500)


@router.post("/achievement/achievement/update", tags=["achievement", "update"])
async def _update_class(achievement: AchievementUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user_admin)) -> APIResponse:
    """更新指定id的成果表信息"""
    try:
        update_achievement(db, achievement)
        return success_response()
    except ProjectException as e:
        logger.error(e)
        return error_response(str(e))
    except Exception as e:
        logger.exception(e)
        return error_response("服务器错误，请重试", 500)



@router.post("/achievement/achievement/delete", tags=["achievement", "delete"])
async def _delete_class(achievement: AchievementBase, db: Session = Depends(get_db), user: User = Depends(get_current_user_admin)) -> APIResponse:
    """删除指定id的成果表"""
    try:
        delete_achievement(db, achievement.id)
        return success_response()
    except ProjectException as e:
        logger.error(e)
        return error_response(str(e))
    except Exception as e:
        logger.exception(e)
        return error_response("服务器错误，请重试", 500)







