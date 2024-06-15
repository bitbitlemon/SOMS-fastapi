from server.models.user import *
from server.models.achievement import *
from server.models.entity import *
from server.database import SessionLocal
from server.database.achievement import query_all_achievements
from server.controllers.achievement import get_all_achievement_and_info, get_achievement_and_info_by_id
from utils import object_to_dict

if __name__ == '__main__':
    db = SessionLocal()
    achievements = get_achievement_and_info_by_id(db, 2)
    print(achievements)
