from datetime import datetime, timedelta
from sqlalchemy import distinct
from server import Log
from server.database.achievement import *
from server.database.entity import *
from server.database.user import *
from utils import ProjectException, object_to_dict


def calculate_submitted_content_stats_db(db: Session):
    # 获取今天和昨天的日期
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)

    # 总提交成果内容数量
    total_submitted_contents = db.query(func.count(SubmittedFormContent.id)).scalar()

    # 待审核的提交成果内容数量
    pending_review_count = db.query(func.count(SubmittedFormContent.id)).join(
        SubmittedForm, SubmittedForm.id == SubmittedFormContent.submitted_form_id
    ).filter(
        SubmittedFormContent.review_status == 'pending'
    ).scalar()

    # 今日待审核的提交成果内容数量
    today_pending_review_count = db.query(func.count(SubmittedFormContent.id)).join(
        SubmittedForm, SubmittedForm.id == SubmittedFormContent.submitted_form_id
    ).filter(
        and_(
            SubmittedFormContent.review_status == 'pending',
            SubmittedForm.submission_date >= today,
            SubmittedForm.submission_date < tomorrow
        )
    ).scalar()

    # 昨日待审核的提交成果内容数量
    yesterday_pending_review_count = db.query(func.count(SubmittedFormContent.id)).join(
        SubmittedForm, SubmittedForm.id == SubmittedFormContent.submitted_form_id
    ).filter(
        and_(
            SubmittedFormContent.review_status == 'pending',
            SubmittedForm.submission_date >= yesterday,
            SubmittedForm.submission_date < today
        )
    ).scalar()

    # 今日提交成果内容数量
    today_contents_count = db.query(func.count(SubmittedFormContent.id)).join(
        SubmittedForm, SubmittedForm.id == SubmittedFormContent.submitted_form_id
    ).filter(
        SubmittedForm.submission_date >= today,
        SubmittedForm.submission_date < tomorrow
    ).scalar()

    # 昨日提交成果内容数量
    yesterday_contents_count = db.query(func.count(SubmittedFormContent.id)).join(
        SubmittedForm, SubmittedForm.id == SubmittedFormContent.submitted_form_id
    ).filter(
        SubmittedForm.submission_date >= yesterday,
        SubmittedForm.submission_date < today
    ).scalar()

    return {
        "total": total_submitted_contents,
        "pending": pending_review_count,
        "today_pending": today_pending_review_count,
        "yesterday_pending": yesterday_pending_review_count,
        "today_submit": today_contents_count,
        "yesterday_submit": yesterday_contents_count
    }


def calculate_daily_submissions_last_14_days(db: Session):
    # 获取今天的日期，并计算14天前的日期
    today = datetime.now().date()
    fourteen_days_ago = today - timedelta(days=13)

    # 查询近14天每天的提交数量
    daily_contents = db.query(
        func.date(SubmittedForm.submission_date).label('date'),
        func.count(SubmittedFormContent.id).label('count')
    ).join(
        SubmittedFormContent, SubmittedForm.id == SubmittedFormContent.submitted_form_id
    ).filter(
        SubmittedForm.submission_date >= fourteen_days_ago,
        SubmittedForm.submission_date < today + timedelta(days=1)  # 包含今天
    ).group_by(
        func.date(SubmittedForm.submission_date)
    ).order_by(
        'date'
    ).all()

    # 创建日期到提交数量的映射
    submissions_by_date = {date: count for date, count in daily_contents}

    # 确保连续14天都有数据，即使某些天没有提交也要显示
    complete_submissions = {
        (fourteen_days_ago + timedelta(days=i)).isoformat(): submissions_by_date.get(
            fourteen_days_ago + timedelta(days=i), 0)
        for i in range(14)
    }
    complete_submissions.update({
        "today": complete_submissions.get(today.isoformat())
    })

    return complete_submissions


def calculate_daily_active_users_last_14_days(db: Session):
    # 获取今天的日期，并计算14天前的日期
    today = datetime.now().date()
    fourteen_days_ago = today - timedelta(days=13)

    # 查询近14天每天的活跃用户数量
    daily_active_users = db.query(
        func.date(Log.timestamp).label('date'),
        func.count(distinct(Log.user_id)).label('active_users')
    ).filter(
        Log.timestamp >= fourteen_days_ago,
        Log.timestamp < today + timedelta(days=1),  # 包含今天
        Log.user_id != None  # 确保 user_id 不为空
    ).group_by(
        func.date(Log.timestamp)
    ).order_by(
        'date'
    ).all()

    # 创建日期到活跃用户数量的映射
    active_users_by_date = {date: active_users for date, active_users in daily_active_users}

    # 确保连续14天都有数据，即使某些天没有活跃用户也要显示
    complete_active_users = {
        (fourteen_days_ago + timedelta(days=i)).isoformat(): active_users_by_date.get(
            (fourteen_days_ago + timedelta(days=i)), 0)
        for i in range(14)
    }
    complete_active_users.update({
        "yesterday": complete_active_users.get((today - timedelta(days=1)).isoformat()),
        "today": complete_active_users.get(today.isoformat())
    })

    return complete_active_users


def calculate_user_scores_for_achievement(db: Session, achievement_id: int):
    # 查询指定 achievement_id 的 SubmittedForm 下每个用户的提交内容的总分
    # 并且这些提交内容的审核状态为 'approved'
    user_scores = db.query(
        SubmittedForm.user_id,
        func.sum(SubmittedFormContent.score).label('total_score')
    ).join(
        SubmittedFormContent, SubmittedForm.id == SubmittedFormContent.submitted_form_id
    ).filter(
        SubmittedForm.achievement_id == achievement_id,
        SubmittedFormContent.review_status == 'approved'
    ).group_by(
        SubmittedForm.user_id
    ).order_by(
        func.sum(SubmittedFormContent.score).desc()  # 按总分降序排列
    ).all()

    # 创建一个字典，键为用户ID，值为其对应的总分
    scores_by_user = {user_id: total_score for user_id, total_score in user_scores}

    return scores_by_user



def calculate_user_scores_with_names(db: Session, achievement_id: int):
    # 使用前面定义的函数查询每个用户的总分
    user_scores = db.query(
        SubmittedForm.user_id,
        func.sum(SubmittedFormContent.score).label('total_score')
    ).join(
        SubmittedFormContent, SubmittedForm.id == SubmittedFormContent.submitted_form_id
    ).filter(
        SubmittedForm.achievement_id == achievement_id,
        SubmittedFormContent.review_status == 'approved'
    ).group_by(
        SubmittedForm.user_id
    ).order_by(
        func.sum(SubmittedFormContent.score).desc()
    ).subquery()

    # 查询用户姓名
    user_names_and_scores = db.query(
        user_scores.c.user_id.label('id'),
        UserProfile.nick_name.label('name'),
        user_scores.c.total_score.label('score')
    ).join(
        UserProfile, UserProfile.user_id == user_scores.c.user_id
    ).all()

    # 将查询结果格式化为 JSON 格式
    results = [
        {"id": user_id, "name": name, "score": score} for user_id, name, score in user_names_and_scores
    ]

    return results

