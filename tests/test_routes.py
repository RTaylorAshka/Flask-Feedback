from unittest import TestCase
from models import User,db,connect_db
from app import app


# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedbackDB_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = False

app.app_context().push()

db.drop_all()
db.create_all()

class UserPageTests(TestCase):

    def setUp(self):
        username="username"
        password="password"
        email="email@email.com"
        first_name="firstname"
        last_name="last_name"
        new_user = User(username=username, password=password, email = email, first_name = first_name, last_name = last_name)
        new_user.register
        self.user=new_user
        self.client = app.test_client()

    def tearDown(self) -> None:
       db.session.query(User).delete()
       return super().tearDown()

    def test_take_to_homepage_when_not_logged_in(self):

        with self.client:
            response = self.client.get(f"/users/{self.user.username}",follow_redirects=True)
            self.assertIn(b'You must be logged in to view this page.', response.data)


    def test_show_page_when_logged_in(self):

            with self.client as client:
                with client.session_transaction() as sess:
                     sess["user_id"]=self.user.username
            response = self.client.get(f"/users/{self.user.username}",follow_redirects=True)
            self.assertIn(b'Delete User', response.data)
   
