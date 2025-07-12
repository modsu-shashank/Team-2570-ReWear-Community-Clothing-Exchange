from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from bson.objectid import ObjectId
import os
import datetime
import uuid
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MONGO_URI'] = os.getenv('MONGO_URI')

mongo = PyMongo(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.email = user_data['email']
        self.name = user_data['name']
        self.points = user_data.get('points', 0)
        self.role = user_data.get('role', 'user')

@login_manager.user_loader
def load_user(user_id):
    user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if user_data:
        return User(user_data)
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/item/<item_id>')
def item_detail(item_id):
    item = mongo.db.items.find_one({'_id': ObjectId(item_id)})
    if not item:
        flash('Item not found', 'error')
        return redirect(url_for('browse'))
    
    owner = mongo.db.users.find_one({'_id': ObjectId(item['owner_id'])})
    if not owner:
        flash('Owner information not found', 'error')
        return redirect(url_for('browse'))
    
    return render_template('item_detail.html', item=item, owner=owner)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')

        if mongo.db.users.find_one({'email': email}):
            flash('Email already registered', 'error')
            return redirect(url_for('register'))

        user = {
            'email': email,
            'password_hash': generate_password_hash(password),
            'name': name,
            'points': 0,
            'role': 'user'
        }
        
        mongo.db.users.insert_one(user)
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = mongo.db.users.find_one({'email': email})
        if user:
            if 'password_hash' in user:
                if check_password_hash(user['password_hash'], password):
                    user_obj = User(user)
                    login_user(user_obj)
                    if user_obj.role == 'admin':
                        return redirect(url_for('admin_index'))
                    return redirect(url_for('dashboard'))
            elif 'password' in user:
                if check_password_hash(user['password'], password):
                    mongo.db.users.update_one(
                        {'_id': user['_id']},
                        {'$set': {'password_hash': user['password']}}
                    )
                    user_obj = User(user)
                    login_user(user_obj)
                    if user_obj.role == 'admin':
                        return redirect(url_for('admin_index'))
                    return redirect(url_for('dashboard'))
        
        flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_items = mongo.db.items.find({'owner_id': current_user.id})
    items_count = mongo.db.items.count_documents({'owner_id': current_user.id})
    
    active_swaps = mongo.db.swaps.count_documents({
        '$or': [
            {'requester_id': current_user.id},
            {'receiver_id': current_user.id}
        ],
        'status': 'pending'
    })
    
    notifications = mongo.db.notifications.count_documents({
        'user_id': current_user.id,
        'read': False
    })
    
    return render_template('dashboard.html', 
                        user_items=user_items, 
                        items_count=items_count,
                        active_swaps=active_swaps,
                        notifications=notifications)

@app.route('/admin')
@login_required
def admin_index():
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    total_users = mongo.db.users.count_documents({})
    total_items = mongo.db.items.count_documents({})
    total_swaps = mongo.db.swaps.count_documents({})
    active_swaps = mongo.db.swaps.count_documents({'status': 'pending'})
    
    pending_items = list(mongo.db.items.find({'status': 'pending'}))
    for item in pending_items:
        owner = mongo.db.users.find_one({'_id': ObjectId(item['owner_id'])})
        if owner:
            item['owner'] = owner
    
    recent_activity = list(mongo.db.activity.find().sort('timestamp', -1).limit(10))
    for activity in recent_activity:
        user = mongo.db.users.find_one({'_id': ObjectId(activity['user_id'])})
        if user:
            activity['user'] = user
    
    return render_template('admin/index.html', 
                        total_users=total_users,
                        total_items=total_items,
                        total_swaps=total_swaps,
                        active_swaps=active_swaps,
                        pending_items=pending_items,
                        recent_activity=recent_activity)

@app.route('/admin/approve/<item_id>', methods=['POST'])
@login_required
def approve_item(item_id):
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    item = mongo.db.items.find_one({'_id': ObjectId(item_id)})
    if not item:
        flash('Item not found', 'error')
        return redirect(url_for('admin_index'))
    
    mongo.db.items.update_one(
        {'_id': ObjectId(item_id)},
        {'$set': {'status': 'available'}}
    )
    
    mongo.db.activity.insert_one({
        'type': 'item_approved',
        'item_id': item_id,
        'user_id': current_user.id,
        'timestamp': datetime.now()
    })
    
    flash('Item approved successfully!', 'success')
    return redirect(url_for('admin_index'))

@app.route('/admin/reject/<item_id>', methods=['POST'])
@login_required
def reject_item(item_id):
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    item = mongo.db.items.find_one({'_id': ObjectId(item_id)})
    if not item:
        flash('Item not found', 'error')
        return redirect(url_for('admin_index'))
    
    mongo.db.items.update_one(
        {'_id': ObjectId(item_id)},
        {'$set': {'status': 'rejected'}}
    )
    
    mongo.db.activity.insert_one({
        'type': 'item_rejected',
        'item_id': item_id,
        'user_id': current_user.id,
        'timestamp': datetime.now()
    })
    
    flash('Item rejected successfully!', 'success')
    return redirect(url_for('admin_index'))

@app.route('/admin/items')
@login_required
def admin_items():
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    items = list(mongo.db.items.find())
    for item in items:
        owner = mongo.db.users.find_one({'_id': ObjectId(item['owner_id'])})
        if owner:
            item['owner'] = owner
    
    return render_template('admin/items.html', items=items)

@app.route('/admin/users')
@login_required
def admin_users():
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    users = mongo.db.users.find()
    return render_template('admin/users.html', users=users)

@app.route('/admin/view_user/<user_id>')
@login_required
def view_user(user_id):
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('admin_users'))
    
    items = mongo.db.items.find({'owner_id': ObjectId(user_id)})
    
    swaps = mongo.db.swaps.find({
        '$or': [
            {'requester_id': ObjectId(user_id)},
            {'receiver_id': ObjectId(user_id)}
        ]
    })
    
    return render_template('admin/view_user.html', user=user, items=items, swaps=swaps)

@app.route('/admin/delete_user/<user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('admin_users'))
    
    mongo.db.items.delete_many({'owner_id': ObjectId(user_id)})
    
    mongo.db.swaps.delete_many({
        '$or': [
            {'requester_id': ObjectId(user_id)},
            {'receiver_id': ObjectId(user_id)}
        ]
    })
    
    mongo.db.users.delete_one({'_id': ObjectId(user_id)})
    
    flash('User and their items/swaps have been deleted successfully!', 'success')
    return redirect(url_for('admin_users'))

@app.route('/admin/swaps')
@login_required
def admin_swaps():
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    swaps = mongo.db.swaps.find()
    return render_template('admin/swaps.html', swaps=swaps)

@app.route('/profile')
@login_required
def profile():
    user = mongo.db.users.find_one({'_id': ObjectId(current_user.id)})
    return render_template('profile.html', user=user)

@app.route('/add-item', methods=['GET', 'POST'])
@login_required
def add_item():
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        size = request.form.get('size')
        condition = request.form.get('condition')
        
        images = []
        if 'images' in request.files:
            uploaded_files = request.files.getlist('images')
            for file in uploaded_files:
                if file and file.filename != '':
                    filename = secure_filename(file.filename)
                    unique_filename = f"{uuid.uuid4()}_{filename}"
                    filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
                    file.save(filepath)
                    images.append(unique_filename)
        
        item = {
            'title': title,
            'description': description,
            'category': category,
            'size': size,
            'condition': condition,
            'owner_id': current_user.id,
            'status': 'pending',
            'created_at': datetime.now(),
            'images': images
        }
        
        mongo.db.items.insert_one(item)
        flash('Item submitted successfully! Awaiting approval.', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('add_item.html')

@app.route('/edit-item/<item_id>', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    item = mongo.db.items.find_one({'_id': ObjectId(item_id)})
    
    if not item:
        flash('Item not found', 'error')
        return redirect(url_for('dashboard'))
    
    if item['owner_id'] != current_user.id:
        flash('You can only edit your own items', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        size = request.form.get('size')
        condition = request.form.get('condition')
        
        update_data = {
            '$set': {
                'title': title,
                'description': description,
                'category': category,
                'size': size,
                'condition': condition
            }
        }
        
        mongo.db.items.update_one({'_id': ObjectId(item_id)}, update_data)
        flash('Item updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('edit_item.html', item=item)

@app.route('/delete-item/<item_id>', methods=['POST'])
@login_required
def delete_item(item_id):
    item = mongo.db.items.find_one({'_id': ObjectId(item_id)})
    
    if not item:
        flash('Item not found', 'error')
        return redirect(url_for('dashboard'))
    
    if item['owner_id'] != current_user.id:
        flash('You can only delete your own items', 'error')
        return redirect(url_for('dashboard'))
    
    mongo.db.items.delete_one({'_id': ObjectId(item_id)})
    flash('Item deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/browse')
def browse():
    items = mongo.db.items.find({'status': 'available'})
    return render_template('browse.html', items=items)

@app.route('/my-swaps')
@login_required
def my_swaps():
    requested_swaps = mongo.db.swaps.find({
        'requester_id': current_user.id
    })
    received_swaps = mongo.db.swaps.find({
        'receiver_id': current_user.id
    })
    
    return render_template('my_swaps.html', 
                        requested_swaps=requested_swaps,
                        received_swaps=received_swaps)

@app.route('/notifications')
@login_required
def notifications():
    user_notifications = mongo.db.notifications.find({
        'user_id': current_user.id
    }).sort('created_at', -1)
    
    notifications_count = mongo.db.notifications.count_documents({
        'user_id': current_user.id
    })
    
    return render_template('notifications.html', 
                        notifications=user_notifications,
                        notifications_count=notifications_count)

@app.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    name = request.form.get('name')
    
    mongo.db.users.update_one(
        {'_id': ObjectId(current_user.id)},
        {'$set': {'name': name}}
    )
    
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('profile'))

if __name__ == '__main__':
    app.run(debug=True)
