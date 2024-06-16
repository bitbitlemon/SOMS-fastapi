from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime




class AchievementScoreRank(BaseModel):
    id: int = Field(..., description="成果表ID")
    limit: Optional[int] = Field(None, description="只获取前几名")
