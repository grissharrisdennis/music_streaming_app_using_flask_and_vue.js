<template>
<div class="user" v-if="user">
  <header>
    <ul class="nav_links">
  <br>
      <h1>Welcome {{ user.username }} <p>Email:{{ user.email }}</p> </h1>

      <li><router-link   :to="{ name: 'UserProfile', params: { id: user.id }}"><button class='slo' >User Profile</button></router-link></li>
      <li><button @click="openModal" class="slo">Creator Account</button>
        <PopupModal v-show="isModalVisible" @close="closeModal" :id=user.id /></li>
      
      <li>
        <a>
          <div class="searchbox">
              <input type="search" name="search_query" v-model="query" id="search_query" >
              <button type="submit" @click="search" class="fa fa-search">Search</button>
          </div>
        </a>
      </li>
      <li><button @click="logout()" class="slo">Logout</button></li>
</ul>
</header>
<div class="dash" v-if="song">
  <h1>Popular Songs</h1>
  <div class="songs-listss" >
    <div class="opas" v-for="songs in song" :key="songs.id">
    <div class="music" >
      <img :src="getImageUrl(songs.image)">
      <div class="music-content">
        <h3>{{ songs.name }}</h3>
        <button @click="ModalVisible=true" class="btn"><i class="fa fa-play"></i></button>
        <h4>ft.{{ songs.artist }}</h4>
          <star-rating v-model:rating="rating" :starSize="20" starColor="#0b34d5" />
          <button class="postrate" @click="postRating(songs.id)">Rate</button>
      </div>
      
    </div>
    <MusicPlayer v-if="ModalVisible" @close="ModalVisible = false"  :audio="songs.audio" :song_id="songs.id" />
  </div>
  </div>

  </div>
  <div class="song-list" >
   <h1>Your Playlist</h1>
   <br>
   <router-link   :to="{ name: 'NewPlaylist', params: { id: user.id }}"><button class='slo' >New Playlist</button></router-link> 
   <div class="small-containers" v-if="playlist">
    <div class="small-container" v-for="play in playlist" :key="play.id">
      
      <h2>{{ play.name }}</h2>
      <br>
      <br>
      <router-link   :to="{ name: 'UpdatePlaylist', params: {playlist_id:play.id, id: user.id }}"><button class='slo' > Add Songs</button></router-link>
      <router-link   :to="{ name: 'PlaylistDetails', params: {playlist_id:play.id, id: user.id }}"><button class='slo' > View</button></router-link>
    </div>
    
  </div>
  </div>
  <div class="genrelist">
   <h1>genres</h1>
  </div>
</div>

</template>


<script>
import PopupModal from '@/components/PopupModal.vue'
import MusicPlayer from '@/components/MusicPlayer.vue'
import StarRating from 'vue-star-rating'
export default {
  name: 'UserDashboard',
  components: {
    PopupModal,
    MusicPlayer,
    StarRating 
  },
  data() {
    return {
      user: null,
      error: null,
      query:null,
      message:'',
      rating:',',
      song:null,
      playlist:null,
      isModalVisible: false,
      ModalVisible:false
    };
  },
  mounted() {
    this.fetchUser();
    this.fetchSong();
    this.fetchPlaylist();
  }, 
  methods: {
    postRating(song_id){
         const data={
          rating:this.rating,
         }
         console.log(this.rating)
         const id=this.$route.params.id
         fetch(`http://127.0.0.1:5000/api/post/${id}/${song_id}/rating`, {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': localStorage.getItem('token'),
        },
        body: JSON.stringify(data),
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
          console.log(result); // Log the entire result object\
          this.rating = result.rating
        })
        .catch(error => {
          console.error(error);
          this.error = error;
        });
      },
    getImageUrl(image) {
      return require(`../assets/images/${image}`);
    },
    openModal() {
      this.isModalVisible = true;
    },
    closeModal() {
      this.isModalVisible = false;
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
    
    
    fetchUser() {
      const id = this.$route.params.id;
      fetch(`http://127.0.0.1:5000/api/${id}/user`, {
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
                this.song = result;
              }
            })
            .catch(error => {
              console.error(error);
              this.error = error;
            });
        },
        fetchPlaylist(){
          fetch(`http://127.0.0.1:5000/api/get/playlist`, {
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
                this.playlist = result;
              }
            })
            .catch(error => {
              console.error(error);
              this.error = error;
            });
        },
    logout() {
      
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

<style>

.dash h1 {
  font-size: 24px;
  margin-bottom: 15px;
  color: #000;
}
.song-list{
  background-color: #fff;
}
.song-list h1 {
  font-size: 24px;
  margin-bottom: 15px;
  color: #000;
}
.small-containers {
  display: flex;
}

.small-container {
  width: 300px;
  height: 200px; 
  margin-right: 10px; /* Spacing between small containers */
  background: #000428;  /* fallback for old browsers */
  background: -webkit-linear-gradient(to right, #004e92, #000428);  /* Chrome 10-25, Safari 5.1-6 */
  background: linear-gradient(to right, #004e92, #000428); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
  
  border: 1px solid #ccc;
  border-radius: 5px;
}
.small-container h2{
  margin-top: 10px;
  color: #eee;
}

.music img{
  width: 100%;
  height: 57%;
  object-fit: cover;
  position: absolute;
  top:0;
  left:0;
}
.music-content{
  width:280;
}
.music-content h3{
  float: left;
  width:100px;
}
.music-content button{
  background-color: DodgerBlue;
  border: none;
  color: white;
  padding: 12px 16px;
  font-size: 16px;
  cursor: pointer;
  float: right;
}
.dash{
  display: flex;
  flex-direction: column;
  
}
.songs-listss{
  display: flex;
  flex-direction: column;
  
  background: #fff;
  width:100%;
}
.playlist{
  display: flex;
  justify-content: center;
}
.genrelist{
  margin-top: 10px;
  display: flex;
  justify-content: space-around;
}

.music{
  
  margin: 20px;
  width:280px;
  height:360px;
  padding:2rem 1rem;
  background:#fff;
  box-shadow: 0px 7px 10px rgba(0,0,0,0.5);
  position: relative;
  display: flex;
  flex-direction: row;
  align-items: flex-end;
  border-radius: 9px;
  transition: 0.5s ease-in-out;
}

  .slo{
    cursor: pointer;
    border: 0;
    border-radius: 4px;
    font-weight: 600;
    margin: 0 10px;
    width: 200px;
    padding: 10px 0;
    box-shadow: 0 0 20px rgba(1, 1, 1, 0.2);
    transition: 0.4s;
    color: rgb(255, 255, 255);
    background-color: rgba(1, 1, 1, 1);
    border: 1px solid rgba(104, 85, 224, 1);
  }
.slo:hover{
    color: black;
    box-shadow: 0 0 20px rgba(104, 85, 224, 0.6);
    background-color: rgba(255, 255, 225, 1);
  }
header{
display:flex;
justify-content:flex-end;
align-items:center;
padding:10px 40%;
background-color:#000;
}

.nav_links{
list-style:none;
}
.nav_links li{
display:inline-block;
padding:10px 10px;
}
.nav_links h1{
  font-size: 40px;
  float: left;
  margin-right: 500px;
  color:white
}
.nav_links li a{
  text-decoration: none;
  color:#eee;
  transition:all 0.3s ease 0s;
}
.nav_links li a:hover{
  background-color:#eee;
  color:#000;
}
.nav_links h1 p{
  font-size: 15px;
}
button{
padding:12px 25px;
background-color:rgba(o,136,169,1);
border:none;
border-radius:50px;
cursor:pointer;

transition:all 0.3s ease 0s;
}
button:hover{
background-color:rgba(0,136,189,0.8);
}
.postrate{

background-color:rgba(o,136,169,1);
border:none;
border-radius:10px;
cursor:pointer;

transition:all 0.3s ease 0s;
}
.postrate:hover{
background-color:rgba(0,13,189,0.8);
}


.user{
 margin:0;
 padding:0;
 box-sizing:border-box;
 background:#eee;
 font-family:Arial;
 }
 .navigator{
 margin:0;
 padding:0;
 box-sizing:border-box;
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


</style>
