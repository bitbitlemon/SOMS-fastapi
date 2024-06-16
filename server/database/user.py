from typing import Optional
from sqlalchemy.orm import Session
from server.models.user import User, UserProfile
from server.schemas.user import UserUpdate
from log import logger
from utils import ProjectException


def get_user_by_openid(db: Session, openid: str) -> User | None:
    return db.query(User).filter(User.openid == openid).first()


def get_user_profile_by_openid(db: Session, openid: str) -> UserProfile | None:
    user = db.query(User).filter(User.openid == openid).first()
    if not user:
        return None
    return db.query(UserProfile).filter(UserProfile.user_id == user.id).first()


def get_user_profile_by_user_id(db: Session, user_id: int) -> UserProfile | None:
    return db.query(UserProfile).filter(UserProfile.user_id == user_id).first()


def get_user_profile_by_student_id(db: Session, student_id: str) -> UserProfile | None:
    return db.query(UserProfile).filter(UserProfile.student_id == student_id).first()


def get_model_by_id(session: Session, model, model_id: Optional[int], model_name: str):
    """
    根据某个表主键id获取该表id的对象
    :param session: 数据库对象
    :param model: 表模型
    :param model_id: 表id
    :param model_name: 表名
    :return: None
    """
    if model_id is not None:
        exists = session.query(model).filter(model.id == model_id).first()
        if not exists:
            raise ProjectException(f"{model_name} ID {model_id} 不存在!")
        return exists


def create_user(session: Session, openid: str, session_key: str, nick_name: str, avatar_url: str, user_type: str = 'student') -> User | None:
    """
    创建新用户及其资料。

    :param session: 数据库对象
    :param openid: 用户的唯一标识
    :param session_key: 会话密钥
    :param nick_name: 用户昵称
    :param avatar_url: 用户头像URL
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
            user_type=user_type
        )
        session.add(new_profile)
        session.commit()  # 提交事务以保存用户资料
        logger.debug("新用户创建成功，用户ID: {}，openid: {}".format(new_user.id, new_user.openid))
        return new_user
    except Exception as e:
        # 如果遇到错误，回滚事务
        session.rollback()
        logger.error(f"创建用户失败: {e}")
        raise ProjectException(f"创建用户失败: {e}")
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
            raise ProjectException(f"未找到ID为 {openid} 的用户。")
    except Exception as e:
        session.rollback()
        logger.error(f"更新会话密钥失败: {e}")
        raise ProjectException(f"更新会话密钥失败: {e}")
    finally:
        session.close()



def update_student_profile(session: Session, user_id: int, info: UserUpdate):
    """
    更新用户资料。

    :param session: 数据库对象
    :param user_id: 用户ID
    :param info: 新用户信息的对象
    :return: None
    """
    try:
        # 查找指定ID的用户资料
        profile = session.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if profile:
            # 更新用户资料
            if info.nick_name is not None:
                profile.nick_name = info.nick_name
            if info.avatar_url is not None:
                profile.avatar_url = info.avatar_url
            if info.student_id is not None:
                profile.student_id = info.student_id
            if info.user_type is not None:
                profile.user_type = info.user_type
            if info.class_id is not None:
                profile.class_id = info.class_id
            # 提交事务
            session.commit()
            logger.debug(f"用户ID {user_id} 的资料已更新。")
        else:
            logger.error(f"未找到ID为 {user_id} 的用户资料。")
            raise ProjectException(f"未找到ID为 {user_id} 的用户资料。")
    except Exception as e:
        session.rollback()
        logger.error(f"更新用户资料失败: {e}")
        raise ProjectException(f"更新用户资料失败: {e}")
    finally:
        session.close()

