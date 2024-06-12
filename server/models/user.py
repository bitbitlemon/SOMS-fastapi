from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from server.database import Base, engine


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    openid = Column(String(255), unique=True, nullable=False)  # 通过用户code返回的openid
    session_key = Column(String(255), nullable=False)  # 通过用户code返回的session_key，可用于解密用户名等

    # 关联其他表
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    user_achievements = relationship("UserAchievement", back_populates="user")


class UserProfile(Base):
    __tablename__ = 'user_profiles'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # users表中的id
    nick_name = Column(String(255), nullable=False)  # 昵称
    avatar_url = Column(String(255), nullable=False)  # 头像地址
    student_id = Column(String(255), nullable=True)  # 学号，可为空
    college = Column(String(255), nullable=True)  # 学院
    user_type = Column(Enum('student', 'teacher', 'admin', name='user_types'), nullable=False)  # 用户类型

    # 反向关联
    user = relationship("User", back_populates="profile")


Base.metadata.create_all(engine)

