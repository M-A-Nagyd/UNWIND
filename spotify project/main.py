import mysql.connector
import os
import escape
from flask import Flask, request, render_template, redirect, url_for, flash, session
UPLOAD_FOLDER='static/Album photos'
app = Flask(__name__)
app.secret_key = 'secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Nagyd2006",
    database="spotify"
)
cursor = db.cursor()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form['email']
    password = request.form['password']
    # Query the database to verify user credentials
    cursor.execute("SELECT user_id FROM users WHERE email = %s AND password = %s", (email, password))
    user_id = cursor.fetchone()
    
    if user_id:
        session['user_id'] = user_id[0]  # Store the user_id in session
        return redirect(url_for('next_page'))
    else:
        flash("Invalid username or password. Please try again.")
        return render_template('index.html')

@app.route('/new_user')
def new_user():
    return render_template('new_user.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    dob = request.form['dob']
    
    cursor.execute('select 1 from users where email=%s', (email,))
    
    if cursor.fetchone():
        flash('Account already exists!')
        return redirect(url_for('home'))
    else:
        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for('new_user'))
        if email.endswith('gmail.com') and 7 <= len(password) <= 16:
            cursor.execute('INSERT INTO users (name, email, password, date_of_birth) VALUES (%s, %s, %s, %s)', (username, email, password, dob))
            db.commit()
            flash("Account created successfully!")
            return redirect(url_for('home'))
        else:
            flash("Email must be a Gmail account and password length should be between 7 and 16 characters.")
            return redirect(url_for('new_user'))

@app.route('/next')
def next_page():
    cursor = db.cursor(dictionary=True)
    # Fetch artists
    cursor.execute("SELECT artist_id, name, image FROM artists")
    artists = cursor.fetchall()
    # Fetch albums
    cursor.execute("SELECT album_id, album_name, image FROM albums")
    albums = cursor.fetchall()
    # Fetch playlists
    cursor.execute("SELECT playlist_id, playlist_name, image FROM playlists")
    playlists = cursor.fetchall()
    
    return render_template('home.html', artists=artists, albums=albums, playlists=playlists)

@app.route('/artist/<int:artist_id>')
def artist_details(artist_id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM artists WHERE artist_id = %s", (artist_id,))
    artist = cursor.fetchone()
    
    cursor.execute("""
        SELECT t.track_id, t.track_name, t.file_path, a.album_name, a.image AS album_image
        FROM tracks t
        JOIN albums a ON t.album_id = a.album_id
        WHERE a.artist_id = %s
    """, (artist_id,))
    music = cursor.fetchall()
    
    return render_template('artist_details.html', artist=artist, music=music)

@app.route('/album/<int:album_id>')
def album_details(album_id):
    cursor = db.cursor(dictionary=True)
    # Fetch album's details (name and image)
    cursor.execute("SELECT album_name, image AS album_image FROM albums WHERE album_id = %s", (album_id,))
    album = cursor.fetchone()
    # Fetch the album's music (tracks) details
    cursor.execute("""
        SELECT t.track_id, t.track_name, t.file_path, a.album_name, a.image AS album_image
        FROM tracks t
        JOIN albums a ON t.album_id = a.album_id
        WHERE t.album_id = %s
    """, (album_id,))
    music = cursor.fetchall()
    # Render the album_details.html template with album info and tracks
    return render_template('album_details.html', album=album, music=music)

@app.route('/playlist/<int:playlist_id>')
def playlist_details(playlist_id):
    cursor = db.cursor(dictionary=True)
    # Fetch the playlist's details (name and image)
    cursor.execute("SELECT playlist_name, image FROM playlists WHERE playlist_id = %s", (playlist_id,))
    playlist = cursor.fetchone()
    # Fetch the tracks in the playlist
    cursor.execute("""
        SELECT t.track_id, t.track_name, t.file_path
        FROM tracks t
        JOIN playlist_tracks pt ON t.track_id = pt.track_id
        WHERE pt.playlist_id = %s
    """, (playlist_id,))
    tracks = cursor.fetchall()
    # Render the playlist_details.html template with playlist info and tracks
    return render_template('playlist_details.html', playlist=playlist, tracks=tracks)

@app.route('/like-song', methods=['POST'])
def like_song():
    track_id = request.form.get('track_id')
    user_id = session.get('user_id')  # Get the user_id from session
    
    if track_id and user_id:
        try:
            # Connect to the database and add the track to liked songs
            cursor.execute("INSERT INTO likes (user_id, track_id) VALUES (%s, %s)", (user_id, track_id))
            db.commit()
            flash("Song added to liked songs!")  # Feedback to user
        except Exception as e:
            print("Error adding liked song:", e)
            flash("Failed to add song to liked songs.")
    else:
        flash("Invalid track ID or user session.")
        
    # Redirect back to the artist page or home page
    return redirect(request.referrer or url_for('home'))


@app.route('/create-playlist', methods=['GET', 'POST'])
def create_playlist():
        cursor = db.cursor(dictionary=True)

        if request.method == 'POST':
        # Fetch form data
            playlist_name = request.form['playlist_name']
            playlist_image = request.files['playlist_image']
            selected_songs = request.form.getlist('songs')  # Get selected songs as a list

        # Save playlist image to the static folder
            playlist_image_filename = playlist_image.filename
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], playlist_image_filename)
            playlist_image.save(image_path)

            user_id = session.get('user_id')  # Get the user_id from session

            if user_id:
            # Insert the new playlist into the database
                cursor.execute('INSERT INTO playlists (playlist_name, image, user_id) VALUES (%s, %s, %s)',
                           (playlist_name, playlist_image_filename, user_id))
                db.commit()

            # Get the ID of the newly created playlist
                playlist_id = cursor.lastrowid

            # Insert selected songs into the playlist_tracks table
                for song_id in selected_songs:
                    cursor.execute('INSERT INTO playlist_tracks (playlist_id, track_id) VALUES (%s, %s)', (playlist_id, song_id))

                db.commit()
                flash('Playlist created successfully!')
            else:
                flash('User session not found. Please log in.')

            return redirect(url_for('next_page'))

        else:
        # Fetch all songs from the database to display in the form
            cursor.execute('SELECT track_id, track_name FROM tracks')
            songs = cursor.fetchall()
            return render_template('create_playlist.html', songs=songs)
if __name__ == '__main__':
    app.run(debug=True)
