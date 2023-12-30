<template>
  <div class="search">
  <header>
    <ul class="nav_links">
      <li><h1>Search Results</h1></li>
      <li><a ><router-link  :to="{ name: 'UserDashboard', params: { id: this.$route.query.user_id}}"><button class="slo">User Dashboard</button></router-link></a></li>
      
    </ul>
</header>
    <div class="boxes" v-for="albums in album"   :key="albums.album_id">
      <div class="ven" v-if="this.$route.query.name==albums.name">
        <h1 class="name">{{ albums.name }}</h1>
        <br>
        <div class="carde" v-for="songs in albums.songs" :key="songs.song_id">
        <img :src="getImageUrl(songs.image)">
        <h2>{{ songs.name }}</h2>
        <h2>ft.{{ songs.artist }}</h2>
        </div>
        <br>
      </div>
    </div>
    <div class="boxes" v-for="songs in song" :key="songs.song_id">
      <div class="carde" v-if="this.$route.query.name==songs.name">
          <img :src="getImageUrl(songs.image)"  alt="Description of the image"> 
          <div class="texts">
            <h2>{{ songs.name }}</h2>
            <h2>ft. {{ songs.artist }}</h2>
          </div>
      </div>
    </div>
   
  </div>
</template>

<script>
export default {
    name:'SearchPage',
    data(){
      return {
      user: null,
      album:null,
      song:null,
    };
    },
  mounted() {
    this.fetchAlbum();
    this.fetchSong();
    console.log(this.$route.params.name)
  },
  methods:{

    getImageUrl(image) {
      console.log(image)
      return require(`../assets/images/${image}`)
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
              console.log(result); 
              if (result) {
                this.album = result;
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
    logout() {
      // Send the logout request to the server
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
            this.$router.push(`/login`);
          } else {
            console.log("Logout failed");
          }
        })
        .catch(error => {
          console.error(error);
          
        });
    }
  }
}
</script>

<style>
.boxes{
  width:100%;
  margin:50px auto;
  border-radius:20px;
  background: #232526;  /* fallback for old browsers */
  background: -webkit-linear-gradient(to right, #414345, #232526);  /* Chrome 10-25, Safari 5.1-6 */
  background: linear-gradient(to right, #414345, #232526); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
}
.boxes h1{
  font-size:40px;
  color:white;
  font-weight: 200px;
}
.carde{
  width:300px;
  align-items: center;
  text-align: center;
  margin-top: 20px;
  margin-left: 30px;
  margin-bottom: 40px;
  border:1px solid grey;
  background: black;
}
.carde img{
  width:100%;
}
.carde .btn {
  position: absolute;
  top: 70%;
  left: 13%;
  transform: translate(-50%, -50%);
  -ms-transform: translate(-50%, -50%);
  background-color: #f1f1f1;
  color: black;
  font-size: 16px;
  padding: 16px 30px;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  text-align: center;
}
.carde .btn:hover {
  background-color: black;
  color: white;
}
.text{
  padding:5px;
  background-color:#fff;
}
.texts{
  padding:5px;
  background-color:#000;
}
.carde h2{
  color:white;
}
ul li h2{
  margin-right: 500px;
  font-size:40px;
}
ul li a{
  font-size:20px;
}
</style>