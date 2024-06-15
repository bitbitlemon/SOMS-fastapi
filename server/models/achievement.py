from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float, Boolean, Enum
from sqlalchemy.orm import relationship
from server.database import Base, engine


class Achievement(Base):
    __tablename__ = 'achievements'
    __table_args__ = {'comment': '成果信息表'}

    id = Column(Integer, primary_key=True, comment='成果表ID')
    title = Column(String(255), nullable=False, comment='成果表标题')
    description = Column(Text, nullable=True, comment='成果表描述')

    contents = relationship("AchievementRule", back_populates="achievement")
    submitted_forms = relationship("SubmittedForm", back_populates="achievement")


class AchievementRule(Base):
    __tablename__ = 'achievement_rules'
    __table_args__ = {'comment': '成果表单规则'}

    id = Column(Integer, primary_key=True, comment='成果表单规则ID')
    achievement_id = Column(Integer, ForeignKey('achievements.id'), comment='成果表ID外键')
    primary_subject = Column(String(100), comment='一级科目')
    secondary_subject = Column(String(100), comment='二级科目')
    tertiary_subject = Column(String(100), comment='三级科目')
    text_info = Column(Boolean, default=True, comment='是否需要文字信息')
    requires_file = Column(Boolean, default=False, comment='是否上传信息')

    achievement = relationship("Achievement", back_populates="contents")
    submitted_contents = relationship("SubmittedFormContent", back_populates="form_rule")


class SubmittedForm(Base):
    __tablename__ = 'submitted_forms'
    __table_args__ = {'comment': '提交成果表'}

    id = Column(Integer, primary_key=True, comment='提交成果表ID')
    achievement_id = Column(Integer, ForeignKey('achievements.id'), nullable=False, comment='成果表ID外键')
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, comment='用户ID外键')
    submission_date = Column(DateTime, default=datetime.utcnow, comment='提交日期')
    review_status = Column(Enum('pending', 'approved', 'rejected', name='review_status'), default='pending', comment='审核状态')
    total_score = Column(Float, comment='总分')

    achievement = relationship("Achievement", back_populates="submitted_forms")
    user = relationship("User", back_populates="user_achievements")
    contents = relationship("SubmittedFormContent", back_populates="submitted_form")


class SubmittedFormContent(Base):
    __tablename__ = 'submitted_form_contents'
    __table_args__ = {'comment': '提交成果内容表'}

    id = Column(Integer, primary_key=True, comment='提交成果内容ID')
    submitted_form_id = Column(Integer, ForeignKey('submitted_forms.id'), nullable=False, comment='提交表单ID外键')
    form_rule_id = Column(Integer, ForeignKey('achievement_rules.id'), nullable=False, comment='成果表单规则ID外键')
    text_info = Column(Text, comment='文字信息')
    file_link = Column(String(200), comment='文件链接')
    review_status = Column(Enum('pending', 'approved', 'rejected', name='review_status'), default='pending', comment='审核状态')
    score = Column(Float, comment='分数')

    submitted_form = relationship("SubmittedForm", back_populates="contents")
    form_rule = relationship("AchievementRule", back_populates="submitted_contents")
    reviews = relationship("Review", back_populates="submitted_form_content")


class Review(Base):
    __tablename__ = 'reviews'
    __table_args__ = {'comment': '审核表'}

    id = Column(Integer, primary_key=True, comment='审核表ID')
    submitted_form_content_id = Column(Integer, ForeignKey('submitted_form_contents.id'), nullable=False, comment='提交表单内容ID外键')
    reviewer_id = Column(Integer, ForeignKey('users.id'), nullable=False, comment='审核者ID，用户ID外键')
    review_date = Column(DateTime, default=datetime.utcnow, comment='审核日期')
    review_comments = Column(Text, comment='审核意见')
    review_score = Column(Float, comment='审核分数')

    submitted_form_content = relationship("SubmittedFormContent", back_populates="reviews")
    reviewer = relationship("User", back_populates="reviews")


Base.metadata.create_all(engine)
