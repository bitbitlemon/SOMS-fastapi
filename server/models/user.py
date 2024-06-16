from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, text
from sqlalchemy.orm import relationship
from server.database import Base, engine


class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(255), nullable=True, comment="请求的用户id，如果不存在则为空")
    request_type = Column(String(255), comment="请求类型")
    request_path = Column(String(255), comment="请求路径")
    timestamp = Column(DateTime, default=datetime.now, server_default=text("CURRENT_TIMESTAMP"), comment="请求时间")
    source_ip = Column(String(255), comment="来源IP")
    user_agent = Column(String(255), comment="ua")


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'comment': '用户表'}

    id = Column(Integer, primary_key=True, comment='用户ID')
    openid = Column(String(255), unique=True, nullable=False, comment='通过用户code返回的openid')
    session_key = Column(String(255), nullable=False, comment='通过用户code返回的session_key，可用于解密用户名等')

    profile = relationship("UserProfile", back_populates="user", uselist=False)
    user_achievements = relationship("SubmittedForm", back_populates="user")
    reviews = relationship("Review", back_populates="reviewer")


class UserProfile(Base):
    __tablename__ = 'user_profiles'
    __table_args__ = {'comment': '用户信息表'}

    id = Column(Integer, primary_key=True, comment='用户ID')
    user_id = Column(Integer, ForeignKey('users.id'), comment='用户ID外键')
    nick_name = Column(String(255), nullable=False, comment='用户昵称')
    avatar_url = Column(String(255), nullable=False, comment='头像url，来源wx')
    student_id = Column(String(255), nullable=True, comment='学号')
    user_type = Column(Enum('student', 'teacher', 'admin', name='user_types'), nullable=False, comment='用户类型')
    class_id = Column(Integer, ForeignKey('classes.id'), nullable=True, comment='班级ID外键')

    user = relationship("User", back_populates="profile")
    student_class = relationship("StudentClass", back_populates="user_profiles")


Base.metadata.create_all(engine)
