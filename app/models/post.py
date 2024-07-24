from app.extensions import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    content = db.Column(db.Text)
    date_created = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    

    def __repr__(self):
        return f'<Post "{self.title}">'

class Category(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(30))
    
    def __repr__(self):
        return f'<Category "{self.category_name}">'