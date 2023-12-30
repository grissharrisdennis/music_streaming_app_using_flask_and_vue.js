<template>
    <div id="app">
        <header>
<ul class="navi_links">
      <h1>Albums</h1>
      <li><router-link :to="{ name: 'TrackPage'}"><button class="slo">Tracks</button></router-link></li>
      <!-- <li><router-link :to="{ name: 'AdminDashboard', params: { id:this.$route.query.id }}"><button class="slo">Admin Dashboard</button></router-link></li>  -->
      <li>
        <a>
          <div class="searchbox">
              <input type="search" name="search_query" v-model="query" id="search_query" >
              <button type="submit" @click="search" class="fa fa-search">Search</button>
          </div>
        </a>
      </li>
      <li><button class="slo" @click="logout()">Logout</button></li> 
      
</ul>
</header>
<br>
<br>
      <div class="albums">
        <div v-for="album in albums" :key="album.id" class="album">
          <h2>{{ album.name }}</h2>
          <button @click="deleteAlbum(album.id)" class="slo" >Delete Album</button>
          <div class="songs">
            <div v-for="song in album.songs" :key="song.id" class="song">
              <h3>{{ song.name }}</h3>
              <button @click="showLyrics(song.lyrics)" class="slo">Lyrics</button>
              <button @click="deleteSong(song.id)"  class="slo">Delete Song</button>
            </div>
          </div>
        </div>
      </div>
  
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
        albums:null,
        showPopup: false,
        selectedSongLyrics: '',
        query:''
      };
    },
    mounted() {
        this.fetchAlbum();
      }, 
    methods: {
        fetchAlbum(){
          fetch(`http://127.0.0.1:5000/api/get/album`, {
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
              console.log(result); // Log the entire result object
              if (result) {
                this.albums = result;
              }
            })
            .catch(error => {
              console.error(error);
              this.error = error;
            });
        },
        search(){
      const data = {
        query: this.query,
      };

      fetch(`http://127.0.0.1:5000/api/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': localStorage.getItem('token'),
        },
        body: JSON.stringify(data),
      })
        .then(response => {
          if (response.ok) {
            console.log(response);
            return response.json();
          } else {
            throw new Error('Network response was not OK');
          }
        })
        .then(result => {
          console.log(result);
          if (result.message === 'Search is successful') {
            console.log("search successful");
            
            this.$router.push({ name: 'SearchPage',params:{ user_id: this.$route.params.id, id: result.id }, query: { name:result.name,user_id: this.$route.params.id, id: result.id } });
          } else {
            console.log("Search failed");
          }
        })
        .catch(error => {
          console.error(error);
          this.error = error;
        });
    },
        deleteAlbum(album_id){
          if(confirm("Do you really want to delete this album?")){
          fetch(`http://127.0.0.1:5000/api/delete/${album_id}/album`, {
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
  .albums {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: center;
  }

  .album {
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 10px;
    width: 270px;
    background-color: blue;
    /* You can add other styles as per your design */
  }

  .song {
    background-color: #f9f9f9;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 10px;
    margin-top: 10px;
    /* You can add other styles as per your design */
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
