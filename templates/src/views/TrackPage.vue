<template>
    <div id="app">
    <header>
       <ul class="navi_links">
      <h1>  Tracks</h1>
      <li><router-link :to="{ name: 'AdminDashboard', params: { id:this.$route.query.id }}"><button class="slo">Admin Dashboard</button></router-link></li>
      <li><button class="slo" @click="logout()">Logout</button></li> 
      <li><router-link :to="{ name: 'AlbumPage'}"><button class="slo">Albums</button></router-link></li>
</ul>
</header>
      <div class="albums">
          <div class="songs">
            <div v-for="song in songs" :key="song.id" class="song">
              <h3>{{ song.name }}</h3>
              <button @click="showLyrics(song.lyrics)" class="slo">Lyrics</button>
              <button @click="deleteSong(song.id)" class="slo">Delete Song</button>
            </div>
          </div>
        
      </div>
  
      <!-- Lyrics Popup -->
      <div v-if="showPopup" class="popup">
        <div class="popup-content">
          <span class="close" @click="hideLyrics">&times;</span>
          <h2>Song Lyrics</h2>
          <p>{{ selectedSongLyrics }}</p>
        </div>
      </div>
    </div>
  </template>
  <script>
  export default {
    name:'AlbumPage',
    data() {
      return {
        songs:null,
        showPopup: false,
        selectedSongLyrics: ''
      };
    },
    mounted() {
        this.fetchSong();
      }, 
    methods: {
        fetchSong(){
          fetch(`http://127.0.0.1:5000/api/get/song`, {
            method: 'GET',
            headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': localStorage.getItem('token'),
            }
          })
            .then(response => {
              if (response.ok) {
                console.log(response)
                return response.json();
              } else {
                throw new Error('Network response was not OK');
              }
            })
            .then(result => {
              console.log(result); 
              if (result) {
                this.songs = result;
              }
            })
            .catch(error => {
              console.error(error);
              this.error = error;
            });
        },
        deleteSong(song_id){
          if(confirm("Do you really want to delete this song?")){
          fetch(`http://127.0.0.1:5000/api/${song_id}/delete/song`, {
            method: 'DELETE',
            headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': localStorage.getItem('token'),
            }
          })
            .then(response => {
              if (response.ok) {
                console.log(response)
                return response.json();
              } else {
                throw new Error('Network response was not OK');
              }
            })
            .then(result => {
              console.log(result); // Log the entire result object
            })
            .catch(error => {
              console.error(error);
              this.error = error;
            });
          }
        },
        
        
        logout() {
          // Send the login request to the server
          fetch(' http://127.0.0.1:5000/api/logout', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authentication-Token': localStorage.getItem('token'),
            },
          })
            .then(response => response.json())
            .then(result => {
              console.log(result);
              if (result.message === 'Logged out') {
                console.log("Logout successful");
                localStorage.setItem('token', "null");
                this.$router.push(`/`);
              } else {
                console.log("Logout failed");
              }
            })
            .catch(error => {
              console.error(error);
              
            });
        },
      showLyrics(lyrics) {
        this.selectedSongLyrics = lyrics;
        this.showPopup = true;
      },
      hideLyrics() {
        this.showPopup = false;
        this.selectedSongLyrics = '';
      }
    }
  };
  </script>
  
  <style>
  /* Style your albums, songs, and popup here */
  .album {
    margin-bottom: 20px;
  }
  
  .song {
    margin-bottom: 10px;
  }
  
  .popup {
    display: flex;
    justify-content: center;
    align-items: center;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
  }
  
  .popup-content {
    background-color: white;
    padding: 20px;
    border-radius: 5px;
    max-width: 80%;
    max-height: 80%;
    overflow: auto;
  }
  
  .close {
    position: absolute;
    top: 10px;
    right: 10px;
    cursor: pointer;
    font-size: 24px;
  }
  </style>
