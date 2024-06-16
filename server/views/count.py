from fastapi import APIRouter
from server.controllers.count import *
from server.controllers.user import get_db, Depends, get_current_user_admin
from server.database import Base, engine
from server.models import *
from server.schemas.count import AchievementScoreRank, AchievementLevel
from server.schemas.user import APIResponse

Base.metadata.create_all(bind=engine)
router = APIRouter()


@router.get("/count/achievement/status", tags=["count"])
# async def _count_achievement(db: Session = Depends(get_db), user: User = Depends(get_current_user_admin)) -> APIResponse:
async def _count_achievement(db: Session = Depends(get_db)) -> APIResponse:
    """获取所有提交的成果表状态"""
    try:
        content_stats = calculate_submitted_content_stats_db(db)
        complete_active_users = calculate_daily_active_users_last_14_days(db)
        content_stats.update({
            "yesterday_active_users": complete_active_users.get("yesterday"),
            "today_active_users": complete_active_users.get("today"),
        })
        return success_response(content_stats)
    except ProjectException as e:
        logger.error(e)
        return error_response(str(e))
    except Exception as e:
        logger.exception(e)
        return error_response("服务器错误，请重试", 500)


@router.get("/count/daily/active", tags=["count"])
# async def _count_achievement(db: Session = Depends(get_db), user: User = Depends(get_current_user_admin)) -> APIResponse:
async def _daily_active(db: Session = Depends(get_db)) -> APIResponse:
    """获取近14日的每日活跃人数"""
    try:
        complete_active_users = calculate_daily_active_users_last_14_days(db)
        return success_response(complete_active_users)
    except ProjectException as e:
        logger.error(e)
        return error_response(str(e))
    except Exception as e:
        logger.exception(e)
        return error_response("服务器错误，请重试", 500)


@router.get("/count/daily/submission", tags=["count"])
# async def _count_achievement(db: Session = Depends(get_db), user: User = Depends(get_current_user_admin)) -> APIResponse:
async def _daily_submission(db: Session = Depends(get_db)) -> APIResponse:
    """获取近14日的每日提交数量"""
    try:
        submissions_by_date = calculate_daily_submissions_last_14_days(db)
        return success_response(submissions_by_date)
    except ProjectException as e:
        logger.error(e)
        return error_response(str(e))
    except Exception as e:
        logger.exception(e)
        return error_response("服务器错误，请重试", 500)


@router.post("/count/rank/scores", tags=["count"])
# async def _count_achievement(db: Session = Depends(get_db), user: User = Depends(get_current_user_admin)) -> APIResponse:
async def _rank_scores(achievement: AchievementScoreRank, db: Session = Depends(get_db)) -> APIResponse:
    """获取成果总分排行榜"""
    try:
        scores_with_names = calculate_user_scores_with_names(db, achievement.id)
        return success_response(scores_with_names[:achievement.limit])
    except ProjectException as e:
        logger.error(e)
        return error_response(str(e))
    except Exception as e:
        logger.exception(e)
        return error_response("服务器错误，请重试", 500)


@router.post("/count/submission/status", tags=["count"])
# async def _count_achievement(db: Session = Depends(get_db), user: User = Depends(get_current_user_admin)) -> APIResponse:
async def _submission_status(achievement: AchievementLevel, db: Session = Depends(get_db)) -> APIResponse:
    """获取级别分组数量"""
    try:
        achievements = count_approved_achievements_by_level(db, achievement.levels)
        return success_response(achievements)
    except ProjectException as e:
        logger.error(e)
        return error_response(str(e))
    except Exception as e:
        logger.exception(e)
        return error_response("服务器错误，请重试", 500)


@router.get("/count/info", tags=["count"])
# async def _count_achievement(db: Session = Depends(get_db), user: User = Depends(get_current_user_admin)) -> APIResponse:
async def _count_info(db: Session = Depends(get_db)) -> APIResponse:
    """
    获取一些信息
    - 用户类型数量
    - 级别分组数量（国家级、省级）
    - 学院和专业数量
    """
    try:
        data = dict(
            user_types=count_user_types(db),
            level_types=count_approved_achievements_by_level(db),
            count=count_majors_and_colleges(db),
        )
        return success_response(data)
    except ProjectException as e:
        logger.error(e)
        return error_response(str(e))
    except Exception as e:
        logger.exception(e)
        return error_response("服务器错误，请重试", 500)
