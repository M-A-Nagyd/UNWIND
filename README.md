# **Unwind - Music Streaming Application**

## **Overview**
Unwind is a modern music streaming application that allows users to create accounts, log in, and explore a vast collection of playlists and tracks. With a user-friendly interface and seamless music playback, Unwind makes it easy for users to enjoy their favorite songs on any device.

## **Features**
- **User Authentication**: Create a new account or log in to an existing one.  
- **Playlist Management**: View and browse playlists with their associated tracks.  
- **Music Playback**: Play songs directly from the playlist.  
- **Like Songs**: Users can like their favorite tracks for easier access later.  
- **Responsive Design**: The application is fully responsive and works well on desktop, tablet, and mobile devices.  

---

## **Technologies Used**
- **Frontend**: HTML, CSS, 
- **Backend**: Flask (Python)  
- **Database**: MySQL  

---

## **Installation**
Follow these steps to set up the project locally.

1. **Clone the repository**:  
   ```bash
   git clone https://github.com/yourusername/unwind.git
   cd unwind
   
2.**Setup**:
Refer to the SQL scripts to understand the structure of the program. Create the following folders in the static folder:\
/unwind\
│\
├── /static\
│    ├── styles.css\
|    ├── styles1.css\
│    ├── home.css\
|    ├── /*songs*\
|    ├── /*artist photos*\
|    └── /*album photos*\
│\
├── /templates\
│    ├── login.html\
│    ├── new_user.html\
│    └── playlist_details.html\
|\
├── app.py\
├── requirements.txt\
└── README.md\
add appropriate contents in all these folder and run db scripts for all these and store them in their corresponding tables.\
3.**Run**\
execute the app.py program and run the program via\

```bash
http://127.0.0.1:5000/
