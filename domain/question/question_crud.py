from datetime import datetime

from domain.question.question_schema import QuestionCreate, QuestionUpdate
from models import Question, User, Answer
from sqlalchemy.orm import Session
from sqlalchemy import select, func, or_, and_


def get_question_list(db: Session, skip: int = 0, limit: int = 10, keyword: str = ''):
    base_query = select(Question)

    if keyword:
        search = f'%{keyword}%'
        sub_query = (
            select(Answer.question_id, Answer.content, User.username)
            .outerjoin(User, Answer.user_id == User.id)
            .subquery()
        )
        base_query = (
            select(Question)
            .outerjoin(User)
            .outerjoin(sub_query, sub_query.c.question_id == Question.id)
            .where(
                or_(
                    Question.subject.ilike(search),
                    Question.content.ilike(search),
                    User.username.ilike(search),
                    sub_query.c.content.ilike(search),
                    sub_query.c.username.ilike(search)
                )
            )
            .distinct()
        )

    count_query = select(func.count()).select_from(base_query.alias())
    total = db.scalar(count_query)

    list_query = base_query.order_by(Question.create_date.desc()) \
        .offset(skip).limit(limit)
    question_list = db.scalars(list_query).all()
    return total, question_list



def get_question(db: Session, question_id: int):
    question = db.get(Question, question_id)
    return question


def create_question(db: Session, question_create: QuestionCreate,
                    user: User):
    db_question = Question(subject=question_create.subject,
                           content=question_create.content,
                           create_date=datetime.now(),
                           user=user)
    db.add(db_question)
    db.commit()


def update_question(db: Session, db_question: Question,
                    question_update: QuestionUpdate):
    db_question.subject = question_update.subject
    db_question.content = question_update.content
    db_question.modify_date = datetime.now()
    db.commit()


def delete_question(db: Session, db_question: Question):
    db.delete(db_question)
    db.commit()


def vote_question(db: Session, db_question: Question, db_user: User):
    db_question.voter.append(db_user)
    db.commit()

