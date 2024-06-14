from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from server.database import Base, engine


class User(Base):
    """用户表"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    openid = Column(String(255), unique=True, nullable=False)  # 通过用户code返回的openid
    session_key = Column(String(255), nullable=False)  # 通过用户code返回的session_key，可用于解密用户名等

    profile = relationship("UserProfile", back_populates="user", uselist=False)
    user_achievements = relationship("UserAchievement", back_populates="user")


class UserProfile(Base):
    """用户信息表"""
    __tablename__ = 'user_profiles'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # 用户id，关联users表
    nick_name = Column(String(255), nullable=False)  # 用户昵称
    avatar_url = Column(String(255), nullable=False)  # 头像url，来源wx
    student_id = Column(String(255), nullable=True)  # 学号
    user_type = Column(Enum('student', 'teacher', 'admin', name='user_types'), nullable=False)  # 用户类型
    class_id = Column(Integer, ForeignKey('classes.id'), nullable=True)  # 班级外键

    user = relationship("User", back_populates="profile")
    student_class = relationship("StudentClass", back_populates="user_profiles")


Base.metadata.create_all(engine)
