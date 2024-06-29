from datetime import datetime

from exts import db
from sqlalchemy.orm import validates


class UD(db.Model):
    university = db.Column(db.String(255))
    department = db.Column(db.String(255))

    __table_args__ = (db.PrimaryKeyConstraint('university', 'department'), {})


class Course(db.Model):
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(255), nullable=False)
    course_description = db.Column(db.Text)
    duration = db.Column(db.Integer)
    university = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(255), nullable=False)
    video_num = db.Column(db.Integer, nullable=False)
    avg_clarity_rating = db.Column(db.Float)
    avg_interactivity_rating = db.Column(db.Float)
    avg_engagement_rating = db.Column(db.Float)
    avg_correctness_rating = db.Column(db.Float)
    avg_content_depth_rating = db.Column(db.Float)

    __table_args__ = (db.ForeignKeyConstraint(['university', 'department'],
                                              ['ud.university', 'ud.department']),
                      {})


class Teacher(db.Model):
    teacher_id = db.Column(db.Integer, primary_key=True)
    teacher_name = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(255), nullable=False)
    university = db.Column(db.String(255), nullable=False)
    video_num = db.Column(db.Integer, nullable=False)
    avg_clarity_rating = db.Column(db.Float)
    avg_interactivity_rating = db.Column(db.Float)
    avg_engagement_rating = db.Column(db.Float)
    avg_correctness_rating = db.Column(db.Float)
    avg_content_depth_rating = db.Column(db.Float)

    __table_args__ = (db.ForeignKeyConstraint(['university', 'department'],
                                              ['ud.university', 'ud.department']),
                      {})


class TC(db.Model):
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.teacher_id'), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), primary_key=True)

    __table_args__ = (db.PrimaryKeyConstraint('teacher_id', 'course_id'), {})


class CoursePlan(db.Model):
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.teacher_id'), primary_key=True)
    week = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.Text, nullable=False)
    key_point = db.Column(db.Text, nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint('course_id', 'teacher_id', 'week'),
        db.ForeignKeyConstraint(['course_id', 'teacher_id'], ['tc.course_id', 'tc.teacher_id']),
        {}
    )


class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    upload_account = db.Column(db.Integer, db.ForeignKey('account.account_id'), nullable=False)
    upload_date = db.Column(db.Date, nullable=False)
    course_id = db.Column(db.Integer, nullable=False)
    teacher_id = db.Column(db.Integer, nullable=False)
    week = db.Column(db.Integer, nullable=False)
    video_path = db.Column(db.String(255), nullable=False)
    clarity_rating = db.Column(db.Integer, default=None)
    interactivity_rating = db.Column(db.Integer, default=None)
    engagement_rating = db.Column(db.Integer, default=None)
    correctness_rating = db.Column(db.Integer, default=None)
    content_depth_rating = db.Column(db.Integer, default=None)
    error_description = db.Column(db.Text, nullable=False, default="未分析")
    correction = db.Column(db.Text, default=None)
    comments = db.Column(db.Text, default=None)

    __table_args__ = (
        db.ForeignKeyConstraint(['course_id', 'teacher_id', 'week'],
                                ['course_plan.course_id', 'course_plan.teacher_id', 'course_plan.week']),
        {}
    )

    @validates('clarity_rating', 'interactivity_rating', 'engagement_rating', 'correctness_rating', 'content_depth_rating')
    def validate_ratings(self, key, value):
        if value is not None and (value < 1 or value > 5):
            raise ValueError(f"{key} must be between 1 and 5")
        return value


class Account(db.Model):
    account_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_date = db.Column(db.Date, nullable=False)
    university = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(255), nullable=False)

    __table_args__ = (db.ForeignKeyConstraint(['university', 'department'],
                                              ['ud.university', 'ud.department']),
                      {})


class UserActionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    action_type = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
