from sqlalchemy.orm import Session, joinedload
from server.models.achievement import *
from server.schemas.achievement import *
from utils import ProjectException


def query_all_achievements(db: Session):
    return db.query(Achievement).all()


def query_achievement_by_id(db: Session, achievement_id: int):
    return db.query(Achievement).filter(Achievement.id == achievement_id).first()


def add_achievement(db: Session, achievement_data: AchievementCreate):
    new_achievement = Achievement(
        title=achievement_data.title,
        description=achievement_data.description
    )
    db.add(new_achievement)
    db.commit()
    db.refresh(new_achievement)
    return new_achievement


def update_achievement(db: Session, achievement_data: AchievementUpdate):
    achievement_to_update = db.query(Achievement).filter(Achievement.id == achievement_data.id).first()

    if not achievement_to_update:
        raise ProjectException(f"成果 ID {achievement_data.id} 不存在")

    if achievement_data.title is not None:
        achievement_to_update.title = achievement_data.title

    if achievement_data.description is not None:
        achievement_to_update.description = achievement_data.description

    db.commit()
    db.refresh(achievement_to_update)
    return achievement_to_update


def delete_achievement(db: Session, achievement_id: int):
    achievement_to_delete = db.query(Achievement).filter(Achievement.id == achievement_id).first()
    if not achievement_to_delete:
        raise ProjectException(f"成果 ID {achievement_id} 不存在")

    db.delete(achievement_to_delete)
    db.commit()
    return achievement_to_delete


def query_all_achievement_rules(db: Session):
    return db.query(AchievementRule).all()


def query_achievement_rule_by_id(db: Session, achievement_rule_id: int):
    return db.query(AchievementRule).filter(AchievementRule.id == achievement_rule_id).first()


def add_achievement_rule(db: Session, achievement_rule_data: AchievementRuleCreate):
    new_achievement_rule = AchievementRule(
        achievement_id=achievement_rule_data.achievement_id,
        primary_subject=achievement_rule_data.primary_subject,
        secondary_subject=achievement_rule_data.secondary_subject,
        tertiary_subject=achievement_rule_data.tertiary_subject,
        level=achievement_rule_data.level,
        text_info=achievement_rule_data.text_info,
        requires_file=achievement_rule_data.requires_file,
        score=achievement_rule_data.score
    )
    db.add(new_achievement_rule)
    db.commit()
    db.refresh(new_achievement_rule)
    return new_achievement_rule


def update_achievement_rule(db: Session, achievement_rule_data: AchievementRuleUpdate):
    achievement_rule_to_update = db.query(AchievementRule).filter(
        AchievementRule.id == achievement_rule_data.id).first()

    if not achievement_rule_to_update:
        raise ProjectException(f"成果表单规则 ID {achievement_rule_data.id} 不存在")

    if achievement_rule_data.achievement_id is not None:
        achievement_rule_to_update.achievement_id = achievement_rule_data.achievement_id

    if achievement_rule_data.primary_subject is not None:
        achievement_rule_to_update.primary_subject = achievement_rule_data.primary_subject

    if achievement_rule_data.secondary_subject is not None:
        achievement_rule_to_update.secondary_subject = achievement_rule_data.secondary_subject

    if achievement_rule_data.tertiary_subject is not None:
        achievement_rule_to_update.tertiary_subject = achievement_rule_data.tertiary_subject

    if achievement_rule_data.level is not None:
        achievement_rule_to_update.level = achievement_rule_data.level

    if achievement_rule_data.text_info is not None:
        achievement_rule_to_update.text_info = achievement_rule_data.text_info

    if achievement_rule_data.requires_file is not None:
        achievement_rule_to_update.requires_file = achievement_rule_data.requires_file

    if achievement_rule_data.score is not None:
        achievement_rule_to_update.score = achievement_rule_data.score

    db.commit()
    db.refresh(achievement_rule_to_update)
    return achievement_rule_to_update


def delete_achievement_rule(db: Session, achievement_rule_id: int):
    achievement_rule_to_delete = db.query(AchievementRule).filter(AchievementRule.id == achievement_rule_id).first()
    if not achievement_rule_to_delete:
        raise ProjectException(f"成果表单规则 ID {achievement_rule_id} 不存在")

    db.delete(achievement_rule_to_delete)
    db.commit()
    return achievement_rule_to_delete


def query_all_submitted_forms(db: Session):
    return db.query(SubmittedForm).all()


def query_submitted_form_by_id(db: Session, submitted_form_id: int):
    return db.query(SubmittedForm).filter(SubmittedForm.id == submitted_form_id).first()


def add_submitted_form(db: Session, submitted_form_data: SubmittedFormCreate):
    new_submitted_form = SubmittedForm(
        achievement_id=submitted_form_data.achievement_id,
        user_id=submitted_form_data.user_id,
        submission_date=submitted_form_data.submission_date,
        review_status=submitted_form_data.review_status,
        total_score=submitted_form_data.total_score
    )
    db.add(new_submitted_form)
    db.commit()
    db.refresh(new_submitted_form)
    return new_submitted_form


def update_submitted_form(db: Session, submitted_form_data: SubmittedFormUpdate):
    submitted_form_to_update = db.query(SubmittedForm).filter(SubmittedForm.id == submitted_form_data.id).first()

    if not submitted_form_to_update:
        raise ProjectException(f"提交成果表 ID {submitted_form_data.id} 不存在")

    if submitted_form_data.achievement_id is not None:
        submitted_form_to_update.achievement_id = submitted_form_data.achievement_id

    if submitted_form_data.user_id is not None:
        submitted_form_to_update.user_id = submitted_form_data.user_id

    if submitted_form_data.submission_date is not None:
        submitted_form_to_update.submission_date = submitted_form_data.submission_date

    if submitted_form_data.review_status is not None:
        submitted_form_to_update.review_status = submitted_form_data.review_status

    if submitted_form_data.total_score is not None:
        submitted_form_to_update.total_score = submitted_form_data.total_score

    db.commit()
    db.refresh(submitted_form_to_update)
    return submitted_form_to_update


def delete_submitted_form(db: Session, submitted_form_id: int):
    submitted_form_to_delete = db.query(SubmittedForm).filter(SubmittedForm.id == submitted_form_id).first()
    if not submitted_form_to_delete:
        raise ProjectException(f"提交成果表 ID {submitted_form_id} 不存在")

    db.delete(submitted_form_to_delete)
    db.commit()
    return submitted_form_to_delete


def query_all_submitted_form_contents(db: Session):
    return db.query(SubmittedFormContent).all()


def query_submitted_form_content_by_id(db: Session, submitted_form_content_id: int):
    return db.query(SubmittedFormContent).filter(SubmittedFormContent.id == submitted_form_content_id).first()


def add_submitted_form_content(db: Session, submitted_form_content_data: SubmittedFormContentCreate):
    new_submitted_form_content = SubmittedFormContent(
        submitted_form_id=submitted_form_content_data.submitted_form_id,
        form_rule_id=submitted_form_content_data.form_rule_id,
        text_info=submitted_form_content_data.text_info,
        file_link=submitted_form_content_data.file_link,
        review_status=submitted_form_content_data.review_status,
        score=submitted_form_content_data.score
    )
    db.add(new_submitted_form_content)
    db.commit()
    db.refresh(new_submitted_form_content)
    return new_submitted_form_content


def update_submitted_form_content(db: Session, submitted_form_content_data: SubmittedFormContentUpdate):
    submitted_form_content_to_update = db.query(SubmittedFormContent).filter(
        SubmittedFormContent.id == submitted_form_content_data.id).first()

    if not submitted_form_content_to_update:
        raise ProjectException(f"提交成果内容 ID {submitted_form_content_data.id} 不存在")

    if submitted_form_content_data.submitted_form_id is not None:
        submitted_form_content_to_update.submitted_form_id = submitted_form_content_data.submitted_form_id

    if submitted_form_content_data.form_rule_id is not None:
        submitted_form_content_to_update.form_rule_id = submitted_form_content_data.form_rule_id

    if submitted_form_content_data.text_info is not None:
        submitted_form_content_to_update.text_info = submitted_form_content_data.text_info

    if submitted_form_content_data.file_link is not None:
        submitted_form_content_to_update.file_link = submitted_form_content_data.file_link

    if submitted_form_content_data.review_status is not None:
        submitted_form_content_to_update.review_status = submitted_form_content_data.review_status

    if submitted_form_content_data.score is not None:
        submitted_form_content_to_update.score = submitted_form_content_data.score

    db.commit()
    db.refresh(submitted_form_content_to_update)
    return submitted_form_content_to_update


def delete_submitted_form_content(db: Session, submitted_form_content_id: int):
    submitted_form_content_to_delete = db.query(SubmittedFormContent).filter(
        SubmittedFormContent.id == submitted_form_content_id).first()
    if not submitted_form_content_to_delete:
        raise ProjectException(f"提交成果内容 ID {submitted_form_content_id} 不存在")

    db.delete(submitted_form_content_to_delete)
    db.commit()
    return submitted_form_content_to_delete


def query_all_reviews(db: Session):
    return db.query(Review).all()


def query_review_by_id(db: Session, review_id: int):
    return db.query(Review).filter(Review.id == review_id).first()


def add_review(db: Session, review_data: ReviewCreate):
    new_review = Review(
        submitted_form_content_id=review_data.submitted_form_content_id,
        reviewer_id=review_data.reviewer_id,
        review_date=review_data.review_date,
        review_comments=review_data.review_comments,
        review_score=review_data.review_score
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review


def update_review(db: Session, review_data: ReviewUpdate):
    review_to_update = db.query(Review).filter(Review.id == review_data.id).first()

    if not review_to_update:
        raise ProjectException(f"审核 ID {review_data.id} 不存在")

    if review_data.submitted_form_content_id is not None:
        review_to_update.submitted_form_content_id = review_data.submitted_form_content_id

    if review_data.reviewer_id is not None:
        review_to_update.reviewer_id = review_data.reviewer_id

    if review_data.review_date is not None:
        review_to_update.review_date = review_data.review_date

    if review_data.review_comments is not None:
        review_to_update.review_comments = review_data.review_comments

    if review_data.review_score is not None:
        review_to_update.review_score = review_data.review_score

    db.commit()
    db.refresh(review_to_update)
    return review_to_update


def delete_review(db: Session, review_id: int):
    review_to_delete = db.query(Review).filter(Review.id == review_id).first()
    if not review_to_delete:
        raise ProjectException(f"审核 ID {review_id} 不存在")

    db.delete(review_to_delete)
    db.commit()
    return review_to_delete


def query_all_achievements_with_submitted_forms(db: Session):
    """
    查询所有成果及其提交的表单
    """
    return db.query(Achievement).options(joinedload(Achievement.submitted_forms)).all()


def query_achievement_with_submitted_forms_by_id(db: Session, achievement_id: int):
    """
    查询指定ID成果及其提交的表单
    """
    return (db.query(Achievement)
            .options(joinedload(Achievement.submitted_forms))
            .filter(Achievement.id == achievement_id)
            .first())


def query_achievement_rules_by_achievement_id(db: Session, achievement_id: int) -> list[AchievementRule]:
    """
    查询指定成果表ID的所有规则
    :param db: 数据库对象
    :param achievement_id: 成果表ID
    :return: list[AchievementRule]
    """
    return db.query(AchievementRule).filter(AchievementRule.achievement_id == achievement_id).all()

