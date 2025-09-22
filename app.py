from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory, session
import mysql.connector
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, auth
import requests
import json

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Initialize Firebase Admin SDK
try:
    import json
    # Get the Firebase service account JSON from environment variable
    cred_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
    if not cred_json:
        raise ValueError("FIREBASE_CREDENTIALS_JSON environment variable is not set!")

    # Parse JSON string into dict
    cred_dict = json.loads(cred_json)
    cred = credentials.Certificate(cred_dict)

    # Initialize Firebase
    firebase_admin.initialize_app(cred)
    print("Firebase Admin SDK initialized successfully!")

except Exception as e:
    print(f"Firebase Admin SDK initialization failed: {e}")
    print("Make sure FIREBASE_CREDENTIALS_JSON env variable is set correctly on Render")


# Authentication helper functions
def verify_firebase_token(token):
    """Verify Firebase ID token"""
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        print(f"Token verification failed: {e}")
        return None

def require_auth(f):
    """Decorator to require authentication for routes"""
    def decorated_function(*args, **kwargs):
        # Check if user is logged in via session
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Database connection using environment variables
def get_connection():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        ssl_ca="ca.pem"  # if Aiven requires SSL cert
    )
    return conn

# Initialize database tables
def init_database():
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Create kings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS kings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                batch VARCHAR(50),
                bio TEXT,
                image_path VARCHAR(200),
                vote_count INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create queens table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS queens (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                batch VARCHAR(50),
                bio TEXT,
                image_path VARCHAR(200),
                vote_count INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insert king candidates if table is empty
        cursor.execute("SELECT COUNT(*) FROM kings")
        if cursor.fetchone()[0] == 0:
            kings_data = [
                ("Aung Min Khant", "HND-65", "Bio", "Kings/Aung Min Khant.png"),
                ("Aung Khant Paing", "HND-65", "Vote Me", "Kings/Aung Khant Paing.png"),
                ("Aung Thaw Hein", "HND-60", "Vote Me", "Kings/Aung Thaw Hein.png"),
                ("Han Htoo Naung", "HND-60", "A yin lu htet po myan say ya ml", "Kings/Han Htoo Naung.jpg"),
                ("Hein Lin Thaw", "HND-60", "လူမရှိလို့ ဝင်ပြိုင်တာ မရှိတဲ့ a shyak တွေလည်း ကုန်ပါပြီ", "Kings/Hein Lin Thaw.png"),
                ("Htet Oo Wai yan", "HND-58", "", "Kings/Htet Oo Wai Yan.png"),
                ("Htoo Aung Linn", "HND-69", "✨Ready to wear the crown 👑", "Kings/Htoo Aung Linn.png"),
                ("Kaung Zaw Hein", "HND-57", "I Developed This Website, Vote ME or Get BANNED!", "Kings/Kaung Zaw Hein.jpg"),
                ("Lin Latt Maung", "HND-52", "Love is crowned with cuteness 👑", "Kings/Lin Latt Maung.png"),
                ("Lin Sat Naing", "HND-68", "Vote Me", "Kings/Lin Sat Naing.png"),
                ("Min Thu Ta", "HND-65", "Vote Me", "Kings/Min Thu Ta.png"),
                ("Naing Aung Khant", "HND-59", "Vote Me", "Kings/Naing Aung Khant.jpg"),
                ("Nyan Lynn Htun", "HND-60", "Vote Me", "Kings/Nyan Lynn Htun.png"),
                ("Tun Lin Aung", "HND-68", "Hated, Dated, Still Celebrated.", "Kings/Tun Lin Aung.png"),
                ("Tun Win Aung", "HND-64", "Vote Me", "Kings/Tun Win Aung.png")
            ]
            
            cursor.executemany("""
                INSERT INTO kings (name, batch, bio, image_path) 
                VALUES (%s, %s, %s, %s)
            """, kings_data)
        
        # Insert queen candidates if table is empty
        cursor.execute("SELECT COUNT(*) FROM queens")
        if cursor.fetchone()[0] == 0:
            queens_data = [
                ("Aye Thu Aung", "HND-60", "Vote Me", "Queen/Aye Thu Aung.png"),
                ("Ban Htoi Mai", "L3 Batch42", "Vote Me", "Queen/Ban Htoi Mai.png"),
                ("Hla Wutt Hmone Oo", "HND-69", "Shinning Bright ✨", "Queen/Hla Wutt Hmone Oo.png"),
                ("Hnin Thiri", "HND-68", "Taste like your sweetest dreams💭 💕", "Queen/Hnin Thiri.jpg"),
                ("Hsu Wati Hnin", "HND-59", "Vote Me", "Queen/Hsu Wati Hnin.png"),
                ("May Thu Lwin", "HND-8 Business", "💕 \"Brains, beauty, and a heart that shines 🌸\" 💕", "Queen/May Thu Lwin.png"),
                ("Pan Myat Nadi", "Pre IGCse batch6", "Vote Me", "Queen/Ma Pan Myat Nadi.png"),
                ("Pwint Phyu Soe", "HND-65", "Soft look, strong soul", "Queen/Pwint Phyu Soe.jpg"),
                ("Shwe Phyo Wai", "HND-59", "Vote Me", "Queen/Shwe Phyo Wai.png"),
                ("Thanzin Cho", "HND-69", "Progress, not perfection", "Queen/Thanzin Cho.png"),
                ("Thet Htar Shwe Zin", "GUF-91", "A queen not only wears a crown but represents her people.", "Queen/Thet Htar Shwe Zin.png"),
                ("Thet Myat Noe", "HND-64", "Your vibe attracts your tribe.", "Queen/Thet Myat Noe.png"),
                ("Thiri Naing", "Level-3 Batch-38", "Vote Me", "Queen/Thiri Naing.png"),
                ("Thoon Waddy", "HND-9 Business", "Vote Me", "Queen/Thoon Waddy.png"),
                ("Thuu Thuu Han Wai", "HND-65", "Brown tones & soft vibes", "Queen/Thuu Thuu Han Wai.png"),
                ("Zwe Sandar Htet", "HND-57", "Born to be a princess, destined to be a queen.", "Queen/Zwe Sandar Htet.png")
            ]
            
            cursor.executemany("""
                INSERT INTO queens (name, batch, bio, image_path) 
                VALUES (%s, %s, %s, %s)
            """, queens_data)
        
        conn.commit()
        print("Database initialized successfully!")
        
    except Exception as e:
        print(f"Database initialization error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

# Routes
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/auth", methods=["POST"])
def authenticate():
    """Handle Firebase authentication"""
    try:
        data = request.get_json()
        id_token = data.get('idToken')
        
        if not id_token:
            return jsonify({"success": False, "message": "No token provided"}), 400
        
        # Verify the Firebase ID token
        decoded_token = verify_firebase_token(id_token)
        
        if decoded_token:
            # Store user info in session
            session['user_id'] = decoded_token['uid']
            session['user_email'] = decoded_token.get('email', '')
            session['user_name'] = decoded_token.get('name', '')
            
            return jsonify({
                "success": True, 
                "message": "Authentication successful",
                "user": {
                    "uid": decoded_token['uid'],
                    "email": decoded_token.get('email', ''),
                    "name": decoded_token.get('name', '')
                }
            })
        else:
            return jsonify({"success": False, "message": "Invalid token"}), 401
            
    except Exception as e:
        print(f"Authentication error: {e}")
        return jsonify({"success": False, "message": "Authentication failed"}), 500

@app.route("/logout")
def logout():
    """Handle user logout"""
    session.clear()
    return redirect(url_for('login'))

@app.route("/")
@require_auth
def home():
    return render_template("home.html")

@app.route("/candidates")
@require_auth
def candidates():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM kings ORDER BY name")
    kings = cursor.fetchall()
    
    cursor.execute("SELECT * FROM queens ORDER BY name")
    queens = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template("candidate-king.html", kings=kings, queens=queens)

@app.route("/viewmore")
@require_auth
def viewmore():
    candidate_id = request.args.get('id')
    if not candidate_id:
        return redirect(url_for('candidates'))
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Try to find in kings first
    cursor.execute("SELECT *, 'king' as type FROM kings WHERE name LIKE %s", (f"%{candidate_id.replace('_', ' ')}%",))
    candidate = cursor.fetchone()
    
    # If not found in kings, try queens
    if not candidate:
        cursor.execute("SELECT *, 'queen' as type FROM queens WHERE name LIKE %s", (f"%{candidate_id.replace('_', ' ')}%",))
        candidate = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if not candidate:
        flash("Candidate not found!", "error")
        return redirect(url_for('candidates'))
    
    return render_template("viewmore.html", candidate=candidate)

@app.route("/vote", methods=["POST"])
@require_auth
def vote():
    try:
        candidate_id = request.form.get('candidate_id')
        candidate_type = request.form.get('candidate_type')  # 'king' or 'queen'

        if not candidate_id or not candidate_type:
            return jsonify({"success": False, "message": "Missing candidate information"})

        conn = get_connection()
        cursor = conn.cursor()

        # 1. Check if user already voted for this type
        cursor.execute(
            "SELECT * FROM votes WHERE user_uid = %s AND candidate_type = %s",
            (session['user_id'], candidate_type)
        )
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({"success": False, "message": f"You have already voted for a {candidate_type}!"})

        # 2. Update vote count in candidate table
        table_name = f"{candidate_type}s"
        cursor.execute(f"UPDATE {table_name} SET vote_count = vote_count + 1 WHERE id = %s", (candidate_id,))
        if cursor.rowcount == 0:
            conn.rollback()
            cursor.close()
            conn.close()
            return jsonify({"success": False, "message": "Candidate not found"})

        # 3. Record that the user has voted
        cursor.execute(
            "INSERT INTO votes (user_uid, candidate_type, candidate_id) VALUES (%s, %s, %s)",
            (session['user_id'], candidate_type, candidate_id)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"success": True, "message": f"{candidate_type.capitalize()} vote recorded successfully!"})

    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"})



@app.route("/results")
def results():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM kings ORDER BY vote_count DESC")
    kings = cursor.fetchall()
    
    cursor.execute("SELECT * FROM queens ORDER BY vote_count DESC")
    queens = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template("voting_result.html", kings=kings, queens=queens)

@app.route("/lantern")
def lantern():
    return render_template("lantern.html")

@app.route("/about")
def about():
    return render_template("about_us.html")

@app.route("/final")
def final():
    return render_template("final.html")

@app.route("/winner")
def winner():
    return render_template("winner.html")

# Serve images from templates folder
@app.route('/img/<path:filename>')
def serve_image(filename):
    return send_from_directory('templates/img', filename)

@app.route('/Kings/<path:filename>')
def serve_king_images(filename):
    return send_from_directory('templates/Kings', filename)

@app.route('/Queen/<path:filename>')
def serve_queen_images(filename):
    return send_from_directory('templates/Queen', filename)

@app.route('/Queen_Viewmore/<path:filename>')
def serve_queen_viewmore_images(filename):
    return send_from_directory('templates/img/Queen_Viewmore', filename)

@app.route('/King_Viewmore/<path:filename>')
def serve_king_viewmore_images(filename):
    return send_from_directory('templates/img/King_Viewmore', filename)

# Serve static files (CSS, JS, etc.)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# Initialize database on startup
if __name__ == "__main__":
    init_database()
    port = int(os.environ.get("PORT", 5000))  # Use Render's PORT, default to 5000 locally
    app.run(host="0.0.0.0", port=port, debug=True)
