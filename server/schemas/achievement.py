from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ReviewStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


# Achievement Pydantic Models
class AchievementBase(BaseModel):
    id: int = Field(..., description="成果表ID")


class AchievementCreate(BaseModel):
    title: Optional[str] = Field(..., description="成果表标题")
    description: Optional[str] = Field(..., description="成果表描述")


class AchievementUpdate(BaseModel):
    id: int = Field(..., description="成果表ID")
    title: Optional[str] = Field(None, description="成果表标题")
    description: Optional[str] = Field(None, description="成果表描述")


# AchievementRule Pydantic Models
class AchievementRuleBase(BaseModel):
    id: int = Field(..., description="成果表单规则ID")


class AchievementRuleCreate(BaseModel):
    achievement_id: Optional[int] = Field(..., description="成果表ID外键")
    primary_subject: Optional[str] = Field(..., description="一级科目")
    secondary_subject: Optional[str] = Field(..., description="二级科目")
    tertiary_subject: Optional[str] = Field(..., description="三级科目")
    text_info: Optional[bool] = Field(..., description="是否需要文字信息")
    requires_file: Optional[bool] = Field(..., description="是否上传信息")


class AchievementRuleUpdate(BaseModel):
    id: int = Field(..., description="成果表单规则ID")
    achievement_id: Optional[int] = Field(None, description="成果表ID外键")
    primary_subject: Optional[str] = Field(None, description="一级科目")
    secondary_subject: Optional[str] = Field(None, description="二级科目")
    tertiary_subject: Optional[str] = Field(None, description="三级科目")
    text_info: Optional[bool] = Field(None, description="是否需要文字信息")
    requires_file: Optional[bool] = Field(None, description="是否上传信息")


# SubmittedForm Pydantic Models
class SubmittedFormBase(BaseModel):
    id: Optional[int] = Field(..., description="提交成果表ID")



class SubmittedFormCreate(BaseModel):
    achievement_id: Optional[int] = Field(..., description="成果表ID外键")
    user_id: Optional[int] = Field(..., description="用户ID外键")
    submission_date: Optional[datetime] = Field(default_factory=datetime.utcnow, description="提交日期")
    review_status: Optional[ReviewStatus] = Field(..., description="审核状态")
    total_score: Optional[float] = Field(..., description="总分")


class SubmittedFormUpdate(BaseModel):
    id: int = Field(..., description="提交成果表ID")
    achievement_id: Optional[int] = Field(None, description="成果表ID外键")
    user_id: Optional[int] = Field(None, description="用户ID外键")
    submission_date: Optional[datetime] = Field(default_factory=datetime.utcnow, description="提交日期")
    review_status: Optional[ReviewStatus] = Field(None, description="审核状态")
    total_score: Optional[float] = Field(None, description="总分")


# SubmittedFormContent Pydantic Models
class SubmittedFormContentBase(BaseModel):
    id: Optional[int] = Field(..., description="提交成果内容ID")


class SubmittedFormContentCreate(BaseModel):
    submitted_form_id: Optional[int] = Field(..., description="提交表单ID外键")
    form_rule_id: Optional[int] = Field(..., description="成果表单规则ID外键")
    text_info: Optional[str] = Field(None, description="文字信息")
    file_link: Optional[str] = Field(None, description="文件链接")
    review_status: Optional[ReviewStatus] = Field(..., description="审核状态")
    score: Optional[float] = Field(None, description="分数")


class SubmittedFormContentUpdate(BaseModel):
    id: Optional[int] = Field(..., description="提交成果内容ID")
    submitted_form_id: Optional[int] = Field(None, description="提交表单ID外键")
    form_rule_id: Optional[int] = Field(None, description="成果表单规则ID外键")
    text_info: Optional[str] = Field(None, description="文字信息")
    file_link: Optional[str] = Field(None, description="文件链接")
    review_status: Optional[ReviewStatus] = Field(None, description="审核状态")
    score: Optional[float] = Field(None, description="分数")


# Review Pydantic Models
class ReviewBase(BaseModel):
    id: Optional[int] = Field(..., description="审核表ID")


class ReviewCreate(BaseModel):
    submitted_form_content_id: Optional[int] = Field(..., description="提交表单内容ID外键")
    reviewer_id: Optional[int] = Field(..., description="审核者ID，用户ID外键")
    review_date: Optional[datetime] = Field(default_factory=datetime.utcnow, description="审核日期")
    review_comments: Optional[str] = Field(..., description="审核意见")
    review_score: Optional[float] = Field(..., description="审核分数")


class ReviewUpdate(BaseModel):
    id: Optional[int] = Field(..., description="审核表ID")
    submitted_form_content_id: Optional[int] = Field(None, description="提交表单内容ID外键")
    reviewer_id: Optional[int] = Field(None, description="审核者ID，用户ID外键")
    review_date: Optional[datetime] = Field(default_factory=datetime.utcnow, description="审核日期")
    review_comments: Optional[str] = Field(None, description="审核意见")
    review_score: Optional[float] = Field(None, description="审核分数")
