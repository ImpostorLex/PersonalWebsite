from flask import Flask, render_template, request, jsonify, url_for, send_from_directory, abort, redirect, flash, Blueprint
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from bs4 import BeautifulSoup
import hashlib
from forms import LoginForm, RegistrationForm
from icecream import ic
from datetime import datetime

import base64


current_date = datetime.now()

formatted_date = current_date.strftime("%B %d %Y")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'your secret keylalal242'

IMAGE_FOLDER = app.config['UPLOAD_FOLDER'] = os.path.abspath(
    'static/upload')


# -------------- DATABASE --------------

db = SQLAlchemy(app)

class EditorData(db.Model):
    __tablename__ = 'editordata'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text)
    short_desc = db.Column(db.String(200))
    content = db.Column(db.Text)
    date_created = db.Column(db.Text)
    date_modified = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    
class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(450), unique=False, nullable=False)

class Categories(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(250), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
class isFirst(db.Model):
    __tablename__ = "isfirst"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    initial_setup = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class userProfile(db.Model):
    __tablename__ = "userProfile"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(25), nullable=False)
    desc = db.Column(db.String(60), nullable=False)
    about = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
class userExperience(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title_exp = db.Column(db.String(125), unique=True, nullable=False)
    body_exp = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    
db.create_all()

@app.route('/demo')
def homie():
    userProfile2 = {
        'title': 'Default Webpage'
    }

    return render_template('demo.html',userProfile2=userProfile2)
# Define a route and a function to handle requests to that route
@app.route('/')
def homepage():
    
    userProfile2 = {
        'title': 'Default Webpage'
    }

    return render_template('default.html', userProfile2=userProfile2)
    
@app.route('/users/<username>')
def username_welcome(username):
    
    existing_user = Users.query.filter_by(username=username).first()
    
    if existing_user:
        userProfile2 = userProfile.query.filter_by(user_id=existing_user.id).first()
        userExperience2 = userExperience.query.filter_by(user_id=existing_user.id).all()
        userBlogs = EditorData.query.filter_by(user_id=existing_user.id).all()
        categories = Categories.query.filter_by(user_id=existing_user.id).all()
        
        # Initialize an empty dictionary to store the user blogs categorized by category name
        user_blogs_dict = {}

        # Iterate over categories
        for category in categories:
            # Get user blogs associated with the current category
            category_blogs = [blog for blog in userBlogs if blog.category_id == category.id]
            
            # Check if any user blogs are associated with the current category
            if category_blogs:
                # If user blogs exist for the category, add them to the dictionary
                user_blogs_dict[category.category_name] = category_blogs
        
        ic(user_blogs_dict)
        # user_blogs_dict: {'asdasda321': [<EditorData 1>]}
        return render_template('homepage.html', userProfile2=userProfile2, 
                              userExperience2=userExperience2, 
                              enumerate=enumerate, blogs=user_blogs_dict)
    else:
        return render_template('default.html')
        

# Query isFirst table to check if this is user's first initial setup.
def isInitialSetup(curr_user):
    
    user_id = curr_user
    is_first_entry = isFirst.query.filter_by(user_id=user_id).first()
    ic("Pagising", is_first_entry.initial_setup)
    
    if is_first_entry.initial_setup == 1:
        ic("Is initial?", is_first_entry.initial_setup)
        
        return False
    else:
        return True
    

@app.route("/welcome", methods=['GET', 'POST'])
@login_required
def welcome():
    user = current_user
    ic("/welcome", user.username)
    
    if request.method == 'POST':
        
         
        webTitle = request.form.get('webTitle')
        webDesc = request.form.get('webDesc')
        about = request.form.get('about')
        expTitle = request.form.get('expTitle')
        expBody = request.form.get('expBody')
        category = request.form.get('category')
            
        category = Categories(category_name=category, user_id=user.id)
        profile = userProfile(title=webTitle, desc=webDesc, about=about, user_id=user.id)
        exp = userExperience(title_exp=expTitle, body_exp=expBody, user_id=user.id)
        is_first_record = isFirst.query.filter_by(user_id=user.id).first()
        is_first_record.initial_setup = 1
        
        db.session.add(category)
        db.session.add(profile)
        db.session.add(exp)
        db.session.commit()

        return redirect(url_for("username_welcome", username=user.username))
    
    is_initial_setup = isInitialSetup(user.id)
    
    # If user already has done the initial setup
    if is_initial_setup == False:
        
        return redirect(url_for('username_welcome', username=user.username))

    else:
        return render_template("initial.html")


# --------------^ IMAGE HANDLING SECTION ^--------------

@app.route("/display/category/<int:id>")
def display(id):
    
    data = EditorData.query.get(id)
    
    if data is None:
        abort(404)
    return render_template('display.html', data=data)

@app.route("/pricing", methods=['GET'])
def pricing():
    
    return render_template("pricing.html")

# -------------- LOGIN/REGISTER HANDLING SECTION --------------

def hash_sha256(data):
    sha256 = hashlib.sha256()
    sha256.update(data.encode('utf-8'))
    return sha256.hexdigest()

@app.route("/login", methods=['GET', 'POST'])
def index():

    form = LoginForm()
    error = ""

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        hashed = hash_sha256(password)
        ic("lala",username)

        is_user_exists = Users.query.filter_by(
            username=username, password=hashed).first()
        if is_user_exists:
            login_user(is_user_exists, remember=True)
            return redirect(url_for('username_welcome', username=username))



        else:
            ic("lalal")
            error = "Invalid username or password."
    
    ic(error)
    return render_template("login.html", form=form, error=error)


@login_manager.user_loader
def load_user(user_id):

    return Users.query.get(int(user_id))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/register", methods=['GET', 'POST'])
def register():

    form = RegistrationForm()

    if request.method == "POST":
        username = request.form.get("register_user")
        password = request.form.get("register_pass")
        confirm = request.form.get("confirm_pass")

        # Check if the username already exists in the database
        existing_user = Users.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists. Please choose a different one.", "error")
            return redirect(url_for('register'))

        if password == confirm:
            hashed = hash_sha256(password)
            new_user = Users(username=username, password=hashed)

        
            db.session.add(new_user)
            db.session.commit()
            ic(new_user.id)

            is_first_entry = isFirst(initial_setup=0, user_id=new_user.id)
            db.session.add(is_first_entry)
            db.session.commit()


            login_user(new_user, remember=True)
            return redirect(url_for('welcome'))
        else:
            flash("Passwords do not match. Please try again.", "error")
            return redirect(url_for('register'))
    
    return render_template("register.html", form=form)


# 1. It starts here by rendering the editor.
@app.route("/editor", methods=['POST', 'GET'])
@login_required
def editor():
    
    user = current_user.username
    userProfile2 = {
        'title': f'{user}\'s webpage'
    }
    user_id = current_user.id
    
    existing_categories_for_user = Categories.query.filter_by(user_id=user_id).all()
  
    if request.method == 'POST':
        html_content = request.form.get('editordata')
        title = request.form.get('title')
        short_desc = request.form.get('short_desc')
        category = request.form.get('category_select')
        
        
        # Pass the html_content to the converter route.
        converted_html = convert_base64_to_image(html_content)
        
        # Insert data
        content = EditorData(title=title, short_desc=short_desc, content=converted_html,date_created= current_date, 
                             date_modified=current_date, category_id=category,user_id=user_id )
        db.session.add(content)
        db.session.commit()
        
        return jsonify({'converted_html': converted_html})
           
    return render_template("editor.html", userProfile2=userProfile2, category_names=existing_categories_for_user)


# 2. Getting all img elements that is base64 encoded using Beautiful soup and securing filename
def convert_base64_to_image(html_content):
    # Utilize BS4 as they can easily get all images on an HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Loop through all the image
    for img in soup.find_all('img'):
        
        # We want to get all base64 encoded image
        if img.get('src') and img.get('src').startswith('data:image'):
            base64_data = img['src']
            
            # Ensure filename is secure by removing special char and spaces
            # Naming convention - image_`number of image in the directory` + 1.png
            filename = secure_filename(f"image_{len(os.listdir(IMAGE_FOLDER)) + 1}.png")
            save_base64_image(base64_data, filename)
            
            # Generates a URL to the `uploaded_file`
            # It do this by modifying the img attribute of current image object that we are holding
            # then when it comes to rendering the work/blog the `img_src` will simply point out to the
            # `uploaded_file route``
            img['src'] = url_for('uploaded_file', filename=filename)
            
    return str(soup)


# 3. Save the base64 image by decoding and storing into a file using the previously generated
# filename
def save_base64_image(base64_data, filename):
    img_data_decoded = base64.b64decode(base64_data.split(",")[1])
    with open(os.path.join(IMAGE_FOLDER, filename), 'wb') as f:
        f.write(img_data_decoded)

# 4. Servers the file on the upload folder when needed 
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(IMAGE_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)


