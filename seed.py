from models import db, User, Feedback
from app import app

db.drop_all()
db.create_all()

user_data = [
    {'fn': 'alice', 'ln': 'Smith', 'em': 'alice@example.com', 'un': 'ali23', 'pw': 'P@ssw0rd'},
    {'fn': 'Bob', 'ln': 'Johnson', 'em': 'bob@example.com', 'un': 'b0bby', 'pw': 'S3curePwd'},
    {'fn': 'Charlie', 'ln': 'Brown', 'em': 'charlie@example.com', 'un': 'c-brown', 'pw': 'MyP@55'},
    {'fn': 'Daisy', 'ln': 'Taylor', 'em': 'daisy@example.com', 'un': 'daizy.t', 'pw': 'P@ssw0rd!'},
    {'fn': 'Ethan', 'ln': 'Anderson', 'em': 'ethan@example.com', 'un': '3thanA', 'pw': 'Secret@123'}
    ]

placeholder_comment = """
Customer support, a mere illusion,
No answers found in this vast confusion.
My pleas unheard, lost in the abyss,
No comfort offered, just silence, amiss.

Forms unresponsive, errors abound,
Frustration mounting, I could not rebound.
Inadequate functionality, a bitter pill,
A bitter taste, that lingers still.

Oh, website, you failed to meet my needs,
With broken promises and careless deeds.
I leave this feedback, a dissatisfied verse,
Hoping for improvement, a chance to reverse.
"""

for user in user_data:

    new_user = User(username=user['un'], password=user['pw'], email = user['em'], first_name = user['fn'], last_name = user['ln'])
    new_user.register

    new_feedback = Feedback(title = "Test feedback", content = placeholder_comment, user_id = new_user.username)
    db.session.add(new_feedback)
    db.session.commit()

