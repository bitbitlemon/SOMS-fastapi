from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime


class UserLogin(BaseModel):
    code: str = Field(..., description="wx.login获取到的code")
    info: str = Field(..., description="wx.getUserInfo获取到的加密数据")
    iv: str = Field(..., description="wx.getUserInfo获取到的解密偏移量")


class UserTypeEnum(str, Enum):
    student = "student"
    teacher = "teacher"
    admin = "admin"


class UserUpdate(BaseModel):
    nick_name: Optional[str] = Field(None, description="用户昵称")
    avatar_url: Optional[str] = Field(None, description="用户头像链接")
    student_id: Optional[str] = Field(None, description="学号")
    user_type: Optional[UserTypeEnum] = Field(None, description="用户类型")
    class_id: Optional[int] = Field(None, description="归属班级ID")


class APIResponse(BaseModel):
    code: int
    message: str
    data: dict | None

