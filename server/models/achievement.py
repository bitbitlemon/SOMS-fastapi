from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from server.database import Base


class Achievement(Base):
    __tablename__ = 'achievements'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    content = relationship("AchievementContent", uselist=False, back_populates="achievement")
    user_achievements = relationship("UserAchievement", back_populates="achievement")


class AchievementContent(Base):
    __tablename__ = 'achievement_contents'

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    achievement_id = Column(Integer, ForeignKey('achievements.id'))

    achievement = relationship("Achievement", back_populates="content")


class UserAchievement(Base):
    __tablename__ = 'user_achievements'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    achievement_id = Column(Integer, ForeignKey('achievements.id'), primary_key=True)
    status = Column(String(50), nullable=False)
    completed_on = Column(DateTime)

    user = relationship("User", back_populates="user_achievements")
    achievement = relationship("Achievement", back_populates="user_achievements")
