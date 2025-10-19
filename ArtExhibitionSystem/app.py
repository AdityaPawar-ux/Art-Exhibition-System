from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this for production

# Flask-Login Setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User Class (Updated: Added artist_name)
class User(UserMixin):
    def __init__(self, id, username, email, artist_name=None):
        self.id = id
        self.username = username
        self.email = email
        self.artist_name = artist_name

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id, username, email, artist_name FROM users WHERE id = %s', (user_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        return User(row['id'], row['username'], row['email'], row['artist_name'])
    return None

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )

# Initialize DB (All tables: users without bio + paintings with price + orders with status + new fields)
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Users table (no bio)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            artist_name VARCHAR(100)
        )
    ''')
    
    # Paintings table (with price)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS paintings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            type VARCHAR(50),
            artist VARCHAR(100),
            description TEXT,
            image_path VARCHAR(255),
            price DECIMAL(10,2) DEFAULT 0.00
        )
    ''')
    try:
        cursor.execute("ALTER TABLE paintings ADD COLUMN price DECIMAL(10,2) DEFAULT 0.00")
    except mysql.connector.Error:
        pass  # Already exists
    
    # Contacts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # About content table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS about_content (
            id INT PRIMARY KEY DEFAULT 1,
            content TEXT
        )
    ''')
    cursor.execute("INSERT IGNORE INTO about_content (id, content) VALUES (1, 'Welcome to our art exhibition! We showcase beautiful paintings from talented artists around the world.');")
    
    # Orders table (Updated: Add status + new fields for purchase form)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            painting_id INT NOT NULL,
            purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status VARCHAR(20) DEFAULT 'Pending',
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (painting_id) REFERENCES paintings(id)
        )
    ''')
    try:
        cursor.execute("ALTER TABLE orders ADD COLUMN status VARCHAR(20) DEFAULT 'Pending'")
        cursor.execute("ALTER TABLE orders ADD COLUMN name VARCHAR(100) DEFAULT NULL")  # NEW: For purchase form
        cursor.execute("ALTER TABLE orders ADD COLUMN address TEXT DEFAULT NULL")  # NEW: For purchase form
        cursor.execute("ALTER TABLE orders ADD COLUMN payment_method VARCHAR(20) DEFAULT NULL")  # NEW: COD/GPay
    except mysql.connector.Error:
        pass  # Already exists
    
    conn.commit()
    cursor.close()
    conn.close()

# Call init_db on start
with app.app_context():
    init_db()

# Admin login check
def is_admin_logged_in():
    return session.get('admin_logged_in', False)

# Home route (Enhanced: Public + User's paintings if logged in)
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM paintings")
    all_paintings = cursor.fetchall()  # Public gallery
    
    user_paintings = []  # User's own paintings
    if current_user.is_authenticated:
        artist = current_user.artist_name or current_user.username
        cursor.execute("SELECT * FROM paintings WHERE artist = %s", (artist,))
        user_paintings = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    user_message = f"Welcome back, {current_user.username}!" if current_user.is_authenticated else None
    return render_template('index.html', 
                           paintings=all_paintings, 
                           user_paintings=user_paintings, 
                           user_message=user_message,
                           is_logged_in=current_user.is_authenticated)

# User's My Paintings Route (New - Personalized)
@app.route('/my_paintings')
@login_required
def my_paintings():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    artist = current_user.artist_name or current_user.username
    cursor.execute("SELECT * FROM paintings WHERE artist = %s ORDER BY id DESC", (artist,))
    my_paintings = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('my_paintings.html', paintings=my_paintings)

# Painting Detail Route (New)
@app.route('/painting/<int:painting_id>')
def painting_detail(painting_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM paintings WHERE id = %s", (painting_id,))
    painting = cursor.fetchone()
    cursor.close()
    conn.close()
    if not painting:
        flash('Painting not found!', 'error')
        return redirect(url_for('index'))
    return render_template('painting_detail.html', painting=painting)

# OLD Purchase Route (Commented Out - No Longer Used)
# @app.route('/purchase/<int:painting_id>', methods=['POST'])
# @login_required
# def purchase_painting(painting_id):
#     ... (old code - ignore)

# Purchase Form (GET/POST - New: Show Form Before Order)
@app.route('/purchase_form/<int:painting_id>', methods=['GET', 'POST'])
@login_required
def purchase_form(painting_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT title, price FROM paintings WHERE id = %s", (painting_id,))
    painting = cursor.fetchone()
    cursor.close()
    conn.close()
    if not painting:
        flash('Painting not found!', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        payment_method = request.form['payment_method']
        
        # Insert order with new fields
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO orders (user_id, painting_id, name, address, payment_method) 
            VALUES (%s, %s, %s, %s, %s)
        """, (current_user.id, painting_id, name, address, payment_method))
        order_id = cursor.lastrowid  # Get new order ID
        conn.commit()
        cursor.close()
        conn.close()
        
        flash(f'Order #{order_id} placed successfully for "{painting["title"]}" (₹{painting["price"]}) via {payment_method}!', 'success')
        return redirect(url_for('invoice', order_id=order_id))  # To invoice
    
    return render_template('purchase_form.html', painting=painting)

# Invoice View (New: Generate Bill Page)
@app.route('/invoice/<int:order_id>')
@login_required
def invoice(order_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT o.id, o.name, o.address, o.payment_method, o.purchase_date, 
               p.title, p.type, p.artist, p.description, p.price,
               u.username, u.email
        FROM orders o 
        JOIN paintings p ON o.painting_id = p.id 
        JOIN users u ON o.user_id = u.id 
        WHERE o.id = %s AND o.user_id = %s
    """, (order_id, current_user.id))
    order = cursor.fetchone()
    cursor.close()
    conn.close()
    if not order:
        flash('Invoice not found!', 'error')
        return redirect(url_for('index'))
    
    total = order['price']  # Simple total (no tax/shipping)
    return render_template('invoice.html', order=order, total=total)

# About route
@app.route('/about')
def about():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT content FROM about_content WHERE id = 1")
    about_data = cursor.fetchone()
    cursor.close()
    conn.close()
    content = about_data['content'] if about_data else 'Default about content.'
    return render_template('about.html', content=content)

# Contact route
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)", (name, email, message))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Thank you for your message! We\'ll get back to you soon.', 'success')
        print(f"Contact: {name} ({email}) - {message}")
        return redirect(url_for('contact'))
    return render_template('contact.html')

# User Sign Up Route (Bio removed)
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        artist_name = request.form.get('artist_name', '')  # Optional
        
        hashed_pw = generate_password_hash(password)
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (username, email, password, artist_name)
                VALUES (%s, %s, %s, %s)
            ''', (username, email, hashed_pw, artist_name))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
        except mysql.connector.IntegrityError:
            flash('Username or email already exists!', 'error')
        return render_template('signup.html')
    
    return render_template('signup.html')

# User Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, username, email, password, artist_name FROM users WHERE username = %s', (username,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if row and check_password_hash(row['password'], password):
            user = User(row['id'], row['username'], row['email'], row['artist_name'])
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password!', 'error')
    
    return render_template('login.html')

# User Profile Route (Bio removed, User object)
@app.route('/profile')
@login_required
def profile():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id, username, email, artist_name FROM users WHERE id = %s', (current_user.id,))
    user_data = cursor.fetchone()
    cursor.close()
    conn.close()
    if not user_data:
        flash('User data not found!', 'error')
        return redirect(url_for('user_logout'))
    user = User(user_data['id'], user_data['username'], user_data['email'], user_data['artist_name'])
    return render_template('profile.html', user=user)

# User Logout Route
@app.route('/user_logout')
@login_required
def user_logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

# Admin routes
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if not is_admin_logged_in():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if username == 'admin' and password == 'admin123':
                session['admin_logged_in'] = True
                flash('Logged in successfully!', 'success')
                return redirect(url_for('admin_paintings'))
            else:
                flash('Invalid credentials!', 'error')
        return render_template('admin.html', is_admin=is_admin_logged_in())
    return redirect(url_for('admin_paintings'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    return admin_login()

# Admin Paintings Tab
@app.route('/admin/paintings')
def admin_paintings():
    if not is_admin_logged_in():
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM paintings")
    paintings = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('admin.html', is_admin=is_admin_logged_in(), active_tab='paintings', paintings=paintings)

# Add Painting (Updated: With price)
@app.route('/add_painting', methods=['POST'])
def add_painting():
    if not is_admin_logged_in():
        return redirect(url_for('admin_login'))
    title = request.form['title']
    type_ = request.form['type']
    artist = request.form['artist']
    description = request.form['description']
    image_path = request.form['image_path']
    price = float(request.form.get('price', 0.00))  # New: Price from form
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO paintings (title, type, artist, description, image_path, price) VALUES (%s, %s, %s, %s, %s, %s)",
                   (title, type_, artist, description, image_path, price))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Painting added successfully!', 'success')
    return redirect(url_for('admin_paintings'))

# Edit Painting (Updated: With price)
@app.route('/edit_painting/<int:painting_id>', methods=['GET', 'POST'])
def edit_painting(painting_id):
    if not is_admin_logged_in():
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        title = request.form['title']
        type_ = request.form['type']
        artist = request.form['artist']
        description = request.form['description']
        image_path = request.form['image_path']
        price = float(request.form.get('price', 0.00))  # New: Price
        cursor.execute("UPDATE paintings SET title=%s, type=%s, artist=%s, description=%s, image_path=%s, price=%s WHERE id=%s",
                       (title, type_, artist, description, image_path, price, painting_id))
        conn.commit()
        flash('Painting updated successfully!', 'success')
        cursor.close()
        conn.close()
        return redirect(url_for('admin_paintings'))
    
    cursor.execute("SELECT * FROM paintings WHERE id = %s", (painting_id,))
    painting = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not painting:
        flash('Painting not found!', 'error')
        return redirect(url_for('admin_paintings'))
    
    return render_template('admin.html', is_admin=is_admin_logged_in(), active_tab='edit_painting', 
                           painting=painting, painting_id=painting_id)

# Delete Painting
@app.route('/delete_painting/<int:painting_id>')
def delete_painting(painting_id):
    if not is_admin_logged_in():
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM paintings WHERE id = %s", (painting_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Painting deleted successfully!', 'success')
    return redirect(url_for('admin_paintings'))

# Admin Orders Tab (Updated: Include status + new fields)
@app.route('/admin/orders')
def admin_orders():
    if not is_admin_logged_in():
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT o.id, o.purchase_date, o.status, o.name, o.address, o.payment_method, u.username, p.title, p.price 
        FROM orders o 
        JOIN users u ON o.user_id = u.id 
        JOIN paintings p ON o.painting_id = p.id 
        ORDER BY o.purchase_date DESC
    ''')
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('admin.html', is_admin=is_admin_logged_in(), active_tab='orders', orders=orders)
# Admin Order Detail (View - Updated: Include new fields)
@app.route('/admin/order_detail/<int:order_id>')
def admin_order_detail(order_id):
    if not is_admin_logged_in():
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT o.id, o.purchase_date, o.status, o.name, o.address, o.payment_method, u.username, u.email, p.title, p.type, p.artist, p.description, p.price 
        FROM orders o 
        JOIN users u ON o.user_id = u.id 
        JOIN paintings p ON o.painting_id = p.id 
        WHERE o.id = %s
    ''', (order_id,))
    order = cursor.fetchone()
    cursor.close()
    conn.close()
    if not order:
        flash('Order not found!', 'error')
        return redirect(url_for('admin_orders'))
    return render_template('admin.html', is_admin=is_admin_logged_in(), active_tab='order_detail', order=order)

# Admin Edit Order (GET/POST - Updated: Include new fields in fetch)
@app.route('/admin/edit_order/<int:order_id>', methods=['GET', 'POST'])
def admin_edit_order(order_id):
    if not is_admin_logged_in():
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        status = request.form['status']
        cursor.execute("UPDATE orders SET status = %s WHERE id = %s", (status, order_id))
        conn.commit()
        flash('Order updated successfully!', 'success')
        cursor.close()
        conn.close()
        return redirect(url_for('admin_orders'))
    
    # GET: Fetch order details (updated with new fields)
    cursor.execute('''
        SELECT o.id, o.status, o.name, o.address, o.payment_method, u.username, p.title, p.price 
        FROM orders o 
        JOIN users u ON o.user_id = u.id 
        JOIN paintings p ON o.painting_id = p.id 
        WHERE o.id = %s
    ''', (order_id,))
    order = cursor.fetchone()
    cursor.close()
    conn.close()
    if not order:
        flash('Order not found!', 'error')
        return redirect(url_for('admin_orders'))
    return render_template('admin.html', is_admin=is_admin_logged_in(), active_tab='edit_order', order=order)

# Admin Delete Order (New)
@app.route('/admin/delete_order/<int:order_id>')
def admin_delete_order(order_id):
    if not is_admin_logged_in():
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders WHERE id = %s", (order_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Order deleted successfully!', 'success')
    return redirect(url_for('admin_orders'))

# Admin Contacts Tab
@app.route('/admin/contacts')
def admin_contacts():
    if not is_admin_logged_in():
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM contacts ORDER BY created_at DESC")
    contacts = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('admin.html', is_admin=is_admin_logged_in(), active_tab='contacts', contacts=contacts)

# Delete Contact
@app.route('/delete_contact/<int:contact_id>')
def delete_contact(contact_id):
    if not is_admin_logged_in():
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE id = %s", (contact_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Contact deleted successfully!', 'success')
    return redirect(url_for('admin_contacts'))

# Admin About Tab
@app.route('/admin/about')
def admin_about():
    if not is_admin_logged_in():
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM about_content WHERE id = 1")
    about_data = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('admin.html', is_admin=is_admin_logged_in(), active_tab='about', about_content=about_data)

# Update About
@app.route('/update_about', methods=['POST'])
def update_about():
    if not is_admin_logged_in():
        return redirect(url_for('admin_login'))
    content = request.form['content']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE about_content SET content = %s WHERE id = 1", (content,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('About section updated successfully!', 'success')
    return redirect(url_for('admin_about'))

# Admin Reports Tab (New - Stats, Updated JOIN if needed)
@app.route('/admin/reports')
def admin_reports():
    if not is_admin_logged_in():
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Total paintings count
    cursor.execute("SELECT COUNT(*) FROM paintings")
    total_paintings = cursor.fetchone()[0]
    
    # Total sold (orders count)
    cursor.execute("SELECT COUNT(*) FROM orders")
    total_sold = cursor.fetchone()[0]
    
    # Stock (total - sold, assume unique paintings)
    stock = total_paintings - total_sold
    
    cursor.close()
    conn.close()
    
    return render_template('admin.html', is_admin=is_admin_logged_in(), active_tab='reports', 
                           total_paintings=total_paintings, total_sold=total_sold, stock=stock)

# Admin Logout
@app.route('/admin_logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    return admin_logout()

if __name__ == '__main__':
    app.run(debug=True)
