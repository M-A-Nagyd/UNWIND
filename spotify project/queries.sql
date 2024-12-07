use spotify;
-- Create the Users table
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    date_of_birth DATE,
    profile_image VARCHAR(255)
);

-- Create the Artists table
CREATE TABLE Artists (
    artist_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    genre VARCHAR(255),
    image VARCHAR(255)
);

-- Create the Albums table
CREATE TABLE Albums (
    album_id INT AUTO_INCREMENT PRIMARY KEY,
    album_name VARCHAR(255) NOT NULL,
    release_date DATE,
    image VARCHAR(255),
    artist_id INT,
    FOREIGN KEY (artist_id) REFERENCES Artists(artist_id) ON DELETE CASCADE
);

-- Create the Tracks table
CREATE TABLE Tracks (
    track_id INT AUTO_INCREMENT PRIMARY KEY,
    track_name VARCHAR(255) NOT NULL,
    duration TIME,
    file_path VARCHAR(255),
    album_id INT,
    FOREIGN KEY (album_id) REFERENCES Albums(album_id) ON DELETE CASCADE
);

-- Create the Playlists table
CREATE TABLE Playlists (
    playlist_id INT AUTO_INCREMENT PRIMARY KEY,
    playlist_name VARCHAR(255) NOT NULL,
    image VARCHAR(255),
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Create the Playlist_Tracks table (Many-to-Many relationship between Playlists and Tracks)
CREATE TABLE Playlist_Tracks (
    playlist_id INT,
    track_id INT,
    PRIMARY KEY (playlist_id, track_id),
    FOREIGN KEY (playlist_id) REFERENCES Playlists(playlist_id) ON DELETE CASCADE,
    FOREIGN KEY (track_id) REFERENCES Tracks(track_id) ON DELETE CASCADE
);

-- Create the Followers table (Many-to-Many relationship between Users and Artists)
CREATE TABLE Followers (
    user_id INT,
    artist_id INT,
    PRIMARY KEY (user_id, artist_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (artist_id) REFERENCES Artists(artist_id) ON DELETE CASCADE
);

-- Create the Likes table (Many-to-Many relationship between Users and Tracks)
CREATE TABLE Likes (
    user_id INT,
    track_id INT,
    like_date_time DATETIME,
    PRIMARY KEY (user_id, track_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (track_id) REFERENCES Tracks(track_id) ON DELETE CASCADE
);

-- triggers
-- trigger to set default image for playlist
DELIMITER //

CREATE TRIGGER set_default_playlist_image
BEFORE INSERT ON Playlists
FOR EACH ROW
BEGIN
    IF NEW.image IS NULL OR NEW.image = '' THEN
        SET NEW.image = 'default_playlist_image.png';  
    END IF;
END //

DELIMITER ;





insert into users(name,email,password,date_of_birth) value('trialuser1','trial@gmail.com','trialspotify123','1990-1-1');

insert into artists(name,genre,image) values('The Weeknd','Pop','https://drive.google.com/file/d/1DALP9OnjC8pW45rWeSok5k9Mk_iob3oc/view?usp=drive_link');
insert into artists(name,genre,image) values('Travis Scott','Hip-Hop','https://drive.google.com/file/d/1JdnsNPs1_Cybesbk6mLj8EiujKOQC5o0/view?usp=sharing');
insert into artists(name,genre,image) values('Anirudh Ravichander','Pop','https://drive.google.com/file/d/1MGGg_IueKAmFNNlHVFd1ex7abTDUbBvV/view?usp=drive_link');

select* from artists;
update users set date_of_birth='1990-02-01' where user_id=1;
select month(date_of_birth) from users;

rollback;
select* from artists;

insert into albums(album_name,release_date,image,artist_id) values ('Vettaiyan','2024-10-10','vettaiyan.jpeg',3);
insert into albums(album_name,release_date,image,artist_id) values ('Utopia','2023-07-28','Utopia.png',2);
insert into albums(album_name,release_date,image,artist_id) values ('Devara','2024-09-27','devara.jpeg',3);

insert into tracks(track_name,duration,file_path,album_id) values('Manasilaayo','00:04:05','Manasilaayo.mp3',1);
insert into tracks(track_name,duration,file_path,album_id) values('Hunter Vantaar','00:03:12','Hunter Vantaar.mp3',1);
insert into tracks(track_name,duration,file_path,album_id) values('FEIN','00:03:29','FEIN.mp3',2);
insert into tracks(track_name,duration,file_path,album_id) values('Daavudi','00:03:29','Daavudi.mp3',3);
insert into tracks(track_name,duration,file_path,album_id) values('Chuttamalle','00:03:44','Chuttamalle.mp3',3);
insert into tracks(track_name,duration,file_path,album_id) values('Fear Song','00:03:16','Fear.mp3',3);
insert into tracks(track_name,duration,file_path,album_id) values('Red Sea','00:02:39','Red Sea.mp3',3);
insert into tracks(track_name,duration,file_path,album_id) values('Ayudha Pooja','00:02:55','Ayudha Pooja.mp3',3);
select* from tracks;

insert into playlists(playlist_name,user_id) values('BEST HITS',2);
insert into playlist_tracks(playlist_id,track_id) values(1,7);