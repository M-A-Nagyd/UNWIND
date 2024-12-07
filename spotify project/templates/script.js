document.addEventListener("DOMContentLoaded", function() {
    // Fetch artist data and album data from the backend using a Flask route
    fetch("/get_data")
        .then(response => response.json())
        .then(data => {
            const artistList = document.getElementById('artists-list');
            const albumList = document.getElementById('albums-list');
            
            data.artists.forEach(artist => {
                let artistCard = `
                    <div class="artist">
                        <img src="${artist.image}" alt="${artist.name}">
                        <h3>${artist.name}</h3>
                    </div>`;
                artistList.innerHTML += artistCard;
            });

            data.albums.forEach(album => {
                let albumCard = `
                    <div class="album">
                        <img src="${album.image}" alt="${album.album_name}">
                        <h3>${album.name}</h3>
                    </div>`;
                albumList.innerHTML += albumCard;
            });
        });
});
