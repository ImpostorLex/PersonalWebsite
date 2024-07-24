from flask import render_template, request, send_from_directory, url_for, redirect, flash
from app.posts import bp
from app.extensions import db, login_required
from werkzeug.utils import secure_filename
import base64
from bs4 import BeautifulSoup
import os
from datetime import datetime
from icecream import ic

IMAGE_FOLDER = 'app/static/uploads'

from app.models.post import Post, Category
def getCategories():
    
    categories = Category.query.all()
    
    return categories


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    
    categories = getCategories()
    

    if request.method == 'POST':
        
        title = request.form.get('title')
        editor_data = request.form.get('editordata')
        category = request.form.get('category_select')
        
        
        converted_html = convert_base64_to_image(editor_data)
        
        current_date = datetime.now()

        formatted_date = current_date.strftime("%B %d %Y")
        
    
        insert_content = Post(title=title, content=converted_html, date_created=formatted_date, category_id=category)
        
        db.session.add(insert_content)
        db.session.commit()
        
        flash("Succesfully registered content")
    
    return render_template('posts/index.html', category_names=categories)

@bp.route('/categories/')
def categories():
    return render_template('posts/categories.html')


# -------------------- IMAGE HANDLING SECTION BELOW --------------------
@bp.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(IMAGE_FOLDER, filename)



def convert_base64_to_image(html_content):
    # Utilize BS4 as they can easily get all images on an HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    
    for img in soup.find_all('img'):
        
        
        if img.get('src') and img.get('src').startswith('data:image'):
            base64_data = img['src']
            
            filename = secure_filename(f"image_{len(os.listdir(IMAGE_FOLDER)) + 1}.png")
            save_base64_image(base64_data, filename)
            
            img['src'] = url_for('posts.uploaded_file', filename=filename)
            
    return str(soup)



def save_base64_image(base64_data, filename):
    img_data_decoded = base64.b64decode(base64_data.split(",")[1])
    with open(os.path.join(IMAGE_FOLDER, filename), 'wb') as f:
        f.write(img_data_decoded)
        
        
# -------------------- IMAGE HANDLING SECTION ABOVE --------------------