from flask import Flask, request, render_template, redirect, jsonify, flash, session
from models import db, connect_db, User, Feedback
from forms import UserForm, LoginForm, FeedbackForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedbackDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "seeeeecret"

app.app_context().push()
connect_db(app)
db.create_all()



# GET /
# Redirect to /register.
@app.route('/')
def redirect_to_reg():
    return redirect('/register')

# GET /register
# Show a form that when submitted will register/create a user. This form should accept a username, password, email, first_name, and last_name.
# POST /register
# Process the registration form by adding a new user. Then redirect.
@app.route('/register', methods = ['GET', 'POST'])
def get_register_form():

    form = UserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data.capitalize()
        last_name = form.last_name.data.capitalize()

        new_user = User(username=username, password=password, email = email, first_name = first_name, last_name = last_name)

        try:
            new_user.register
        except:
            flash(f'Username "{username}" is taken.')
            return redirect('/register')

        session['user_id'] = new_user.username
        return redirect(f'/users/{new_user.username}')
    
    else:

        return render_template('register-form.html', form = form)
# Make sure you are using WTForms and that your password input hides the characters that the user is typing!  

# GET /login
# Show a form that when submitted will login a user. This form should accept a username and a password.
# POST /login
# Process the login form, ensuring the user is authenticated.
@app.route('/login', methods = ['GET', 'POST'])
def get_login_form():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        try:
            

            user = User.query.filter_by(username = username).first()
            if user.authenticate(password):
                session['user_id'] = user.username
                return redirect(f'/users/{user.username}')
            else:
                flash('Incorrect Password.')
                return redirect('/login')
           
        except:
            flash('Username not recognized.')
            return redirect('/login')
        
            

    return render_template('login-form.html', form = form)

# Make sure you are using WTForms and that your password input hides the characters that the user is typing!


@app.route('/users/<username>')
def get_user_page(username):
    if not logged_in():
        flash(f"You must be logged in to view this page.")
        return redirect('/login')
    else:
        user = User.query.get_or_404(username)
        return render_template('user-page.html', user = user)

@app.route('/logout')
def logout_user():
    session.clear()

    return redirect('/')

# POST /users/<username>/delete
# Remove the user from the database and make sure to also delete all of their feedback. Clear any user information in the session and redirect to /. Make sure that only the user who is logged in can successfully delete their account

@app.route('/users/<username>/delete', methods = ['POST'])
def delete_user(username):

    if has_permissions(username):
        User.query.filter_by(username = username).delete()
        db.session.commit()

        return redirect('/')
    else:
        flash('You do not have permissions to delete this user.')
        return redirect('/')


# GET /users/<username>/feedback/add
# Display a form to add feedback Make sure that only the user who is logged in can see this form
# POST /users/<username>/feedback/add
# Add a new piece of feedback and redirect to /users/<username> — Make sure that only the user who is logged in can successfully add feedback
@app.route('/users/<username>/feedback/add', methods = ['GET', 'POST'])
def add_feedback(username):
    
    if not has_permissions(username):
        flash(f"you do not have permissions to post feedback on {username}'s account.")
        current_user = session['user_id']
        return redirect(f'/users/{current_user}')
    
    else:
        form = FeedbackForm()

        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data

            feedback = Feedback(title = title, content = content, user_id = username)
            db.session.add(feedback)
            db.session.commit()

            return redirect(f'/users/{username}')

        else:

            return render_template('feedback-form.html', form = form)


# GET /feedback/<feedback_id>/update
# Display a form to edit feedback — **Make sure that only the user who has written that feedback can see this form **
# POST /feedback/<feedback_id>/update
@app.route('/feedback/<feedback_id>/update', methods = ['GET', 'POST'])
def edit_feedback(feedback_id):
    

    feedback = Feedback.query.get_or_404(feedback_id)

    if has_permissions(feedback.user_id):
        
        form = FeedbackForm(obj = feedback)
        
        if form.validate_on_submit():
            form.populate_obj(feedback)
            db.session.commit()
            return redirect(f'/users/{feedback.user_id}')
        else:
            return render_template('edit-feedback-form.html', form = form, feedback = feedback)
    else:
        flash('You do not have permissions to edit that form.')
        return redirect('/')

# POST /feedback/<feedback-id>/delete
# Delete a specific piece of feedback and redirect to /users/<username> — Make sure that only the user who has written that feedback can delete it
@app.route('/feedback/<feedback_id>/delete', methods = ['POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)

    if has_permissions(feedback.user_id):
        Feedback.query.filter_by(id = feedback_id).delete()
        db.session.commit()
        current_user = session['user_id']
        return redirect(f'/users/{current_user}')
    else:
        flash('You do not have permissions to delete that feedback.')
        return redirect('/')




def logged_in():

    return (True if 'user_id' in session else False)
    
def has_permissions(username):

    if logged_in() and session['user_id'] == username:

        return True
    
    else:

        return False
        
        
