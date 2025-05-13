from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import pytz

db = SQLAlchemy()

def get_china_time():
    """获取中国时区的当前时间"""
    china_tz = pytz.timezone('Asia/Shanghai')
    return datetime.now(china_tz)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=get_china_time)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    predictions = db.relationship('Prediction', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def update_last_login(self):
        self.last_login = get_china_time()
        db.session.commit()

    def get_stats(self):
        """获取用户统计信息"""
        total_predictions = len(self.predictions)
        today_predictions = len([p for p in self.predictions 
                               if p.created_at.date() == get_china_time().date()])
        return {
            'total_predictions': total_predictions,
            'today_predictions': today_predictions
        }

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_path = db.Column(db.String(200), nullable=False)
    true_label = db.Column(db.String(50))
    predictions = db.Column(db.JSON)  # 存储所有模型的预测结果
    created_at = db.Column(db.DateTime, default=get_china_time)
    updated_at = db.Column(db.DateTime, default=get_china_time, onupdate=get_china_time)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'image_path': self.image_path,
            'true_label': self.true_label,
            'predictions': self.predictions,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    @staticmethod
    def get_stats():
        """获取预测统计信息"""
        total = Prediction.query.count()
        today = Prediction.query.filter(
            Prediction.created_at >= get_china_time().date()
        ).count()
        return {
            'total': total,
            'today': today
        } 