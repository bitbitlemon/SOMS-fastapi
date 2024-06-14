from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


class UserTypeEnum(str, Enum):
    student = "student"
    teacher = "teacher"
    admin = "admin"


class SetUserProfile(BaseModel):
    user_id: Optional[int] = Field(..., description="用户ID")
    nick_name: Optional[str] = Field(None, description="用户昵称")
    avatar_url: Optional[str] = Field(None, description="用户头像链接")
    student_id: Optional[str] = Field(None, description="学号")
    user_type: Optional[UserTypeEnum] = Field(None, description="用户类型")
    class_id: Optional[int] = Field(None, description="归属班级ID")


# Class 增删改模型
class AddClass(BaseModel):
    name: str = Field(..., description="班级名称")
    major_id: int = Field(..., description="归属专业ID")


class UpdateClass(BaseModel):
    class_id: int = Field(..., description="班级ID")
    name: Optional[str] = Field(None, description="班级名称")
    major_id: Optional[int] = Field(None, description="归属专业ID")


class DeleteClass(BaseModel):
    class_id: int = Field(..., description="班级ID")


class QueryClass(BaseModel):
    class_id: int = Field(..., description="班级ID")


# Major 增删改模型
class AddMajor(BaseModel):
    name: str = Field(..., description="专业名称")
    college_id: int = Field(..., description="归属二级学院ID")


class UpdateMajor(BaseModel):
    major_id: int = Field(..., description="专业ID")
    name: Optional[str] = Field(None, description="专业名称")
    college_id: Optional[int] = Field(None, description="归属二级学院ID")


class DeleteMajor(BaseModel):
    major_id: int = Field(..., description="专业ID")


class QueryMajor(BaseModel):
    major_id: int = Field(..., description="专业ID")


# College 增删改模型
class AddCollege(BaseModel):
    name: str = Field(..., description="二级学院名称")


class UpdateCollege(BaseModel):
    college_id: int = Field(..., description="二级学院ID")
    name: Optional[str] = Field(None, description="二级学院名称")


class DeleteCollege(BaseModel):
    college_id: int = Field(..., description="二级学院ID")


class QueryCollege(BaseModel):
    college_id: int = Field(..., description="二级学院ID")
