from pydantic import BaseModel, Field
from typing import Optional, List





class AchievementScoreRank(BaseModel):
    id: int = Field(..., description="成果表ID")
    limit: Optional[int] = Field(None, description="只获取前几名")


class AchievementLevel(BaseModel):
    levels: List[str] = Field(..., description="要查询的级别")
