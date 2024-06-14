from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from server.database import Base, engine


class StudentClass(Base):
    __tablename__ = 'classes'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)  # 班名
    major_id = Column(Integer, ForeignKey('majors.id'))  # 专业外键

    major = relationship("Major", back_populates="classes")
    user_profiles = relationship("UserProfile", back_populates="student_class")


class Major(Base):
    __tablename__ = 'majors'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)  # 专业名称
    college_id = Column(Integer, ForeignKey('colleges.id'))  # 二级学院外键

    college = relationship("College", back_populates="majors")
    classes = relationship("StudentClass", back_populates="major")


class College(Base):
    __tablename__ = 'colleges'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)  # 二级学院名称

    majors = relationship("Major", back_populates="college")


Base.metadata.create_all(engine)
