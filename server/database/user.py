from typing import Optional
from sqlalchemy.orm import Session
from server.models.user import User, UserProfile
from server.models.achievement import Achievement, UserAchievement, AchievementContent
from log import logger


def get_user_by_openid(db: Session, openid: str):
    return db.query(User).filter(User.openid == openid).first()


def get_user_profile_by_openid(db: Session, openid: str):
    user = db.query(User).filter(User.openid == openid).first()
    if not user:
        return None
    return db.query(UserProfile).filter(UserProfile.user_id == user.id).first()


def get_user_profile_by_user_id(db: Session, user_id: int):
    return db.query(UserProfile).filter(UserProfile.user_id == user_id).first()



def create_user(session: Session, openid: str, session_key: str, nick_name: str, avatar_url: str, student_id: Optional[str] = None,
                college: Optional[str] = None, user_type: str = 'student'):
    """
    创建新用户及其资料。

    :param session: 数据库对象
    :param openid: 用户的唯一标识
    :param session_key: 会话密钥
    :param nick_name: 用户昵称
    :param avatar_url: 用户头像URL
    :param student_id: 用户学号（可选）
    :param college: 用户所在学院（可选）
    :param user_type: 用户类型，默认为'student'
    :return: None
    """
    try:
        # 创建新的用户对象
        new_user = User(openid=openid, session_key=session_key)
        session.add(new_user)
        session.commit()  # 提交事务以获取用户ID

        # 创建用户资料
        new_profile = UserProfile(
            user_id=new_user.id,
            nick_name=nick_name,
            avatar_url=avatar_url,
            student_id=student_id,
            college=college,
            user_type=user_type
        )
        session.add(new_profile)
        session.commit()  # 提交事务以保存用户资料

        logger.debug("新用户创建成功，用户ID: {}，openid: {}".format(new_user.id, new_user.openid))
    except Exception as e:
        # 如果遇到错误，回滚事务
        session.rollback()
        logger.error(f"创建用户失败: {e}")
    finally:
        # 关闭会话
        session.close()


def update_session_key(session: Session, openid: str, new_session_key: str):
    """
    更新用户的会话密钥。

    :param session: 数据库对象
    :param openid: 用户openid
    :param new_session_key: 新的会话密钥
    :return: None
    """
    try:
        # 查找指定ID的用户
        user = session.query(User).filter(User.openid == openid).first()
        if user:
            # 更新会话密钥
            user.session_key = new_session_key
            session.commit()
            logger.debug(f"用户ID {openid} 的会话密钥已更新。")
        else:
            logger.error(f"未找到ID为 {openid} 的用户。")
    except Exception as e:
        session.rollback()
        logger.error(f"更新会话密钥失败: {e}")
    finally:
        session.close()


def update_student_profile(session: Session, user_id: int, nick_name: Optional[str] = None, avatar_url: Optional[str] = None, student_id: Optional[str] = None, college: Optional[str] = None):
    """
    更新用户资料。

    :param session: 数据库对象
    :param user_id: 用户ID
    :param nick_name: 新的昵称（可选）
    :param avatar_url: 新的头像URL（可选）
    :param student_id: 新的学号（可选）
    :param college: 新的学院（可选）
    :return: None
    """
    try:
        # 查找指定ID的用户资料
        profile = session.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if profile:
            # 更新用户资料
            if nick_name is not None:
                profile.nick_name = nick_name
            if avatar_url is not None:
                profile.avatar_url = avatar_url
            if student_id is not None:
                profile.student_id = student_id
            if college is not None:
                profile.college = college
            session.commit()
            logger.debug(f"用户ID {user_id} 的资料已更新。")
        else:
            logger.error(f"未找到ID为 {user_id} 的用户资料。")
    except Exception as e:
        session.rollback()
        logger.error(f"更新用户资料失败: {e}")
    finally:
        session.close()
