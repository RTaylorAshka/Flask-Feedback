from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from flask_bcrypt import Bcrypt 


db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    
    
    db.app = app
    db.init_app(app)


class Feedback(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer(),
                   primary_key = True,
                   autoincrement = True
                   )
    title = db.Column(db.String(100),
                       nullable = False
                       )
    content = db.Column(db.Text(),
                       nullable = False
                       )
    user_id = db.Column(db.String(), db.ForeignKey('users.username', ondelete='CASCADE'))

    

class User(db.Model):

    __tablename__ = 'users'

    username = db.Column(db.String(20),
                   primary_key=True,
                   unique = True
                   )
    password = db.Column(db.Text,
                         nullable = False
                         )
    email = db.Column(db.String(50),
                       unique = True,
                       nullable = False
                       )
    first_name = db.Column(db.String(30),
                       nullable = False
                       )
    last_name = db.Column(db.String(30),
                       nullable = False
                       )
    
    feedback = db.relationship('Feedback', cascade = 'all, delete, delete-orphan', backref = 'user')

    # hashes password and adds to database
    @property
    def register(self):

        hashed = bcrypt.generate_password_hash(self.password)
        hashed_utf8 = hashed.decode('utf8')

        self.password = hashed_utf8

        db.session.add(self)
        db.session.commit()

    # returns full name of user
    @property
    def fullname(self):

        return (f'{self.first_name} {self.last_name}')

    # authenticates password
    def authenticate(self, pwd):
        
        if bcrypt.check_password_hash(self.password, pwd):
            return True
        else:
            return False
        

        