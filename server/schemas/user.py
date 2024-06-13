from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime


class UserLogin(BaseModel):
    code: str = Field(..., description="wx.login获取到的code")
    info: str = Field(..., description="wx.getUserInfo获取到的加密数据")
    iv: str = Field(..., description="wx.getUserInfo获取到的解密偏移量")


class StudentIdUpdate(BaseModel):
    student_id: str = Field(..., description="学号")
    college: str = Field(..., description="归属学院")



class UserCreate(BaseModel):
    openid: str
    session_key: str


class UserProfileCreate(BaseModel):
    openid: str
    session_key: str



