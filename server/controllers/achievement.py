from server.database.achievement import *
from server.database.entity import *
from server.database.user import *
from utils import ProjectException, object_to_dict




def get_all_achievement_and_info(session: Session):
    achievements_with_submitted_forms = query_all_achievements_with_submitted_forms(session)
    result = []
    for achievement_with_submitted_form in achievements_with_submitted_forms:
        submitted_forms = achievement_with_submitted_form.submitted_forms
        # 计算每种状态的数量
        pending_num = sum(1 for form in submitted_forms if form.review_status == ReviewStatus.pending)
        approved_num = sum(1 for form in submitted_forms if form.review_status == ReviewStatus.approved)
        rejected_num = sum(1 for form in submitted_forms if form.review_status == ReviewStatus.rejected)
        # 将对象转换为字典
        row = object_to_dict(achievement_with_submitted_form)
        # 更新字典，添加统计信息
        row.update({
            'submitted_num': len(submitted_forms),
            'pending_num': pending_num,
            'approved_num': approved_num,
            'rejected_num': rejected_num
        })
        result.append(row)
    return result



def get_achievement_and_info_by_id(session: Session, achievement_id: int):
    achievement_with_submitted_form = query_achievement_with_submitted_forms_by_id(session, achievement_id)
    if achievement_with_submitted_form:
        submitted_forms = achievement_with_submitted_form.submitted_forms
        # 计算每种状态的数量
        pending_num = sum(1 for form in submitted_forms if form.review_status == ReviewStatus.pending)
        approved_num = sum(1 for form in submitted_forms if form.review_status == ReviewStatus.approved)
        rejected_num = sum(1 for form in submitted_forms if form.review_status == ReviewStatus.rejected)
        # 将对象转换为字典
        row = object_to_dict(achievement_with_submitted_form)
        # 更新字典，添加统计信息
        row.update({
            'submitted_num': len(submitted_forms),
            'pending_num': pending_num,
            'approved_num': approved_num,
            'rejected_num': rejected_num
        })
        return row
    raise ProjectException(f"成果表 ID {achievement_id} 不存在")


