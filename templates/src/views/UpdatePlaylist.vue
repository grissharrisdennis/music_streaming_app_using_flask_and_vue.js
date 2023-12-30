<template>
	<header>
   
   <ul class="navi_links">
		<h1>Update Playlist</h1>
		<li><router-link  :to="{ name: 'UserDashboard', params: { id: $route.params.id }}"><button class="slo">User DashBoard</button></router-link></li>  
   </ul>
   </header>
   <br>
   <div class="newplay">
	
   <form>
   
	<br>
	<div class="form-group">
	<label for="name">Playlist Name:</label>
	<input type="text" id="name" v-model="name" name="name">
	</div>
	<h2>Select Songs to Add</h2>
	<ul>
	
	<li v-for="songs in song" :key="songs.id">
		<div class="song-container">
			<img :src="getImageUrl(songs.image)" :alt="songs.name" class="song-image">
			<input type="checkbox" :id="'song_' + song.id" name="selected_songs[]" v-model="selectedSongs" :value="songs.id">
			<label :for="'song_' + songs.id">{{ songs.name }} -ft. {{ songs.artist }}</label>
		</div>
	
	</li>

   </ul>
   <br>
	<input type="submit" @click="create_playlist">
   </form>

   </div>

   </template>

<script>
export default {
    name:"UpdatePlaylist",
	data() {
    return {
      user: null,
      song:null,
      playlist:null,
    };
  },
  mounted() {
    this.fetchSong();
    this.fetchPlaylist();
  }, 
  methods:{
	getImageUrl(image) {
      return require(`../assets/images/${image}`);
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
  }
};
</script>

<style>

		
form {
			display: flex;
			flex-direction: column;
			align-items: center;
			padding: 20px;
			border: 2px solid #333;
			border-radius: 10px;
			box-shadow: 0 0 10px #333;
			width: 400px;
			margin: 50px auto;
		}

		input[type="text"], input[type="number"] {
			padding: 10px;
			margin: 10px 0;
			border: none;
			border-bottom: 2px solid #333;
			width: 100%;
			font-size: 16px;
		}

		input[type="submit"] {
			background-color: #333;
			color: #fff;
			padding: 10px 20px;
			border: none;
			border-radius: 5px;
			font-size: 16px;
			cursor: pointer;
			transition: all 0.3s ease;
		}

		input[type="submit"]:hover {
			background-color: #fff;
			color: #333;
		}
</style>