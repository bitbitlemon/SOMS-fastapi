from server.controllers.count import *
from server.models.user import *
from server.models.achievement import *
from server.models.entity import *
from server.database import SessionLocal
from server.database.achievement import query_all_achievements
from server.controllers.achievement import *
from utils import object_to_dict


if __name__ == '__main__':
    db = SessionLocal()
    stats = count_majors_and_colleges(db)
    print(stats)
