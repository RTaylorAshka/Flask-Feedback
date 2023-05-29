from unittest import TestCase
from models import User,db,connect_db
from flask import Flask


# Use test database and don't clutter tests with SQL
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedbackDB_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = False

app.app_context().push()

connect_db(app)
db.drop_all()
db.create_all()


class UserTests(TestCase):

    def tearDown(self) -> None:
       db.session.query(User).delete()
       return super().tearDown()

    def test_register_user(self):
       username="username"
       password="password"
       email="email@email.com"
       first_name="firstname"
       last_name="last_name"
       new_user = User(username=username, password=password, email = email, first_name = first_name, last_name = last_name)
       new_user.register
       self.assertEqual(len(User.query.all()),1)


    def test_success_login(self):
       username="username"
       password="password"
       email="email@email.com"
       first_name="firstname"
       last_name="last_name"
       new_user = User(username=username, password=password, email = email, first_name = first_name, last_name = last_name)
       new_user.register

       result=User.authenticate(new_user,"password")
       self.assertEqual(result,True)

    def test_failing_login_on_pwd_error(self):
       username="username"
       password="password"
       email="email@email.com"
       first_name="firstname"
       last_name="last_name"
       new_user = User(username=username, password=password, email = email, first_name = first_name, last_name = last_name)
       new_user.register

       result=User.authenticate(new_user,"wrong_password")
       self.assertEqual(result,False)
