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
    data = query_submitted_form_content_with_user_details(db, 2000)
    # print(data)
    for item in data:
        print(item)

