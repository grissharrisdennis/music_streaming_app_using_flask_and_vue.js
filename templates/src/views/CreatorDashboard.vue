<template>
    <div class="creator" v-if="user">
      <header>
    
    <ul class="nav_links">
          <h1>Welcome Creator {{ user.username }} <p>Email:{{ user.email }}</p> </h1>
          <li><router-link   :to="{ name: 'CreateAlbum', params: { id: user.id }}"><button class="slo" >CreateAlbum</button></router-link></li>
          <li><router-link   :to="{ name: 'UserDashboard', params: { id: user.id }}"><button class="slo" >User Dashboard</button></router-link></li>
          <li><button @click="logout()" class='slo'>Logout</button></li>
    </ul>
    </header>
  <div class="navigator">
    <div class="albums" v-if="album">
      
      <div class="each-album" v-for="albums in album" :key="albums.id">
        <br>
        <h2>{{ albums.name }}</h2>
        
        <h3>{{ albums.artist }}</h3>
                
        <div id="outer">
          <div class="wer"><button class="upso" @click="deleteAlbum(albums.id)">Delete Album</button></div>
          <div class="wer"><router-link   :to="{ name: 'UploadSong', params: {album_id:albums.id, id: user.id }}"><button class="slo" >Upload Songs</button></router-link></div>
          <div class="wer"><router-link   :to="{ name: 'UpdateAlbum', params: {album_id:albums.id, id: user.id }}"><button class="upal" >Update Album</button></router-link></div>
        </div>
        
        <div class="song-box" v-for="song in albums.songs" :key="song.id">
          <div class="songs">
            <img class="w3-round" :src="getImageUrl(song.image)" >
            <MusicPlayer v-if="ModalVisible" @close="ModalVisible = false" :audio="song.audio" :song_id="song.id" />
          <div class="song-container" >
            <button @click="ModalVisible = true"  class="btn"><i class="fa fa-play"></i></button>
            
           <button class="delete-button" @click="deleteSong(song.id)">Delete Songs</button>
           <router-link   :to="{ name: 'UpdateSong', params: {song_id:song.id, id: user.id,album_id:albums.id}}"><button class="update-button" >Update Songs</button></router-link>
         </div>
         </div>
       </div>
    

            
        </div>
        
      </div>
      <br>
    </div>
    <br>
    <br>
    <br>
   </div>
 
    
    </template>
    
    <script>
    import MusicPlayer from '@/components/MusicPlayer.vue'
    export default {
      name: 'CreatorDashboard',
      components: {
        MusicPlayer,
  },
      data() {
        return {
          user: null,
          error: null,
          album:null,
          ModalVisible: false
        };
      },
      mounted() {
        this.fetchCreator();
        this.fetchAlbum();
      }, 
      methods: {
        openModal() {
      this.ModalVisible = true;
    },
    closeModal() {
      this.ModalVisible = false;
    },
        getImageUrl(image) {
      return require(`../assets/images/${image}`);
    },
        fetchCreator() {
          const id = this.$route.params.id;
          fetch(`http://127.0.0.1:5000/api/${id}/creator`, {
            method: 'GET',
            headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': localStorage.getItem('token'),
            }
          })
            .then(response => {
              if (response.ok) {
                return response.json();
              } else {
                throw new Error('Network response was not OK');
              }
            })
            .then(result => {
              console.log(result); // Log the entire result object
              if (result && result.email && result.id && result.username) {
                this.user = result;
              }
            })
            .catch(error => {
              console.error(error);
              this.error = error;
            });
        },
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
                this.album = result;
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
        }
      },
    };
    </script>
    
    <style scoped>
    .btn {
  background-color: DodgerBlue;
  border: none;
  color: white;
  padding: 12px 16px;
  font-size: 16px;
  cursor: pointer;
}
    .song-box {
  width: 400px;
  height: 410px;
  box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: row; /* Change to row to align items horizontally */
  align-items: center; /* Vertically center items */
  position: relative;
}

  /* Styling for the card container */
  .songs {
  width: 300px;
  height:250px;
  background-color: rgb(13, 11, 11);
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
  margin-bottom: 25px;
}
.songs img{
  width:100%;
  height:100%;
  object-fit: cover;
}

.song-container {
  text-align: center;
  padding: 10px 20px;
  background-color: antiquewhite;
}


  

  
    #outer{
    width:100%;
    text-align: center;
   }
    .wer{
      display: inline-block;
    }
    
    

.delete-button,
.update-button {
    cursor: pointer;
    border: 0;
    border-radius: 4px;
    font-weight: 600;
   
    
    width: 100px;
    padding: 10px 0;
    box-shadow: 0 0 20px rgba(1, 1, 1, 0.2);
    transition: 0.4s;
    color: rgb(255, 255, 255);
    background-color: rgb(100, 232, 44);
    border: 1px solid rgba(104, 85, 224, 1);
}

.delete-button:hover,
.update-button:hover {
  color: black;
  box-shadow: 0 0 20px rgba(104, 85, 224, 0.6);
  background-color: rgba(255, 255, 225, 1);
}
    .albums h2 {
      color:#eee;
    }
    .albums h3 {
      color:#eee;
    }
    
    .upal{
    cursor: pointer;
    border: 0;
    border-radius: 4px;
    font-weight: 600;
    margin: 10px;
    width: 200px;
    padding: 10px 0;
    box-shadow: 0 0 20px rgba(1, 1, 1, 0.2);
    transition: 0.4s;
    color: rgb(255, 255, 255);
    background-color: rgb(100, 232, 44);
    border: 1px solid rgba(104, 85, 224, 1);
  }
  .upal:hover{
    color: black;
    box-shadow: 0 0 20px rgba(104, 85, 224, 0.6);
    background-color: rgba(255, 255, 225, 1);
  }
  .upso{
    cursor: pointer;
    border: 0;
    border-radius: 4px;
    font-weight: 600;
    margin: 10px;
    
    width: 200px;
    padding: 10px 0;
    box-shadow: 0 0 20px rgba(1, 1, 1, 0.2);
    transition: 0.4s;
    color: rgb(255, 255, 255);
    background-color: rgb(100, 232, 44);
    border: 1px solid rgba(104, 85, 224, 1);
  }
  .upso:hover{
    color: black;
    box-shadow: 0 0 20px rgba(104, 85, 224, 0.6);
    background-color: rgba(255, 255, 225, 1);
  }
     .navigator{
     margin:0;
     padding:0;
     box-sizing:border-box;
     }
     .each-album{
     width:100%;
     height:100%;
     justify-content:space-around;
     align-items:center;
     display: flex;
     flex-direction: column;
      flex-wrap: wrap;
      border: 1px solid #ccc;
      border-radius: 6px;
      box-shadow: 0 5px 10px rgba(0,0,0,0.1);
      background:url('../assets/o.jpeg');
     }
     
     
    
    .searchbox {
      display: flex;
      justify-content: center;
      margin-top: 10px;
    }
    
    input[type=search] {
      padding: 10px;
      font-size: 17px;
      border: 2px solid #ccc;
      border-radius: 4px;
      transition: width 0.4s ease-in-out;
      width: 60px;
    }
    
    input[type=search]:focus {
      width: 200px;
    }
    
    button[type=submit] {
      border: none;
      background: #101010;
      cursor: pointer;
    }
    
    .fa-search {
      font-size: 20px;
      color: #ccc;
      transition: color 0.4s ease-in-out;
    }
    
    input[type=search]:focus + button .fa-search {
      color: #000;
    }
    
    header{
    display:flex;
    justify-content:flex-end;
    align-items:center;
    padding:10px 10%;
    background-color:#000;
    }
    
    .nav_links{
    list-style:none;
    }
    .nav_links li{
    display:inline-block;
    padding:10px 10px;
    }
    
   
    </style>
    