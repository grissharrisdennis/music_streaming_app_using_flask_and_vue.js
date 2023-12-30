<template>
 <header>

<ul class="navi_links">
      <h1>New Playlist</h1>
      <li><router-link  :to="{ name: 'UserDashboard', params: { id: $route.params.id }}"><button class="slo">User DashBoard</button></router-link></li> 
</ul>
</header>
<br>
<div class="newplay">
<form >
    <h1>New Playlist</h1>

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
    name:"NewPlaylist",
  data() {
    return {
      name: '',
      song:null,
      selectedSongs: []
    };
  },
  mounted() {
    this.fetchSong();
  }, 
  methods: {
    getImageUrl(image) {
      return require(`../assets/images/${image}`);
    },
    create_playlist() {
      const data = {
                name: this.name,
                selected_songs: this.selectedSongs 
        };

      
      fetch(` http://127.0.0.1:5000/api/${this.$route.params.id}/post/playlist`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': localStorage.getItem('token')
        },
        body: JSON.stringify(data),
      })
        .then(response => response.json())
        .then(result => {
          console.log(result.message);
          this.$router.push(`/${this.$route.params.id}/admin/dashboard`)
        })
        .catch(error => {
          console.error(error);
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
  }
}

</script>

<style>
	.song-container {
        display: flex;
        align-items: center;
        margin-bottom: 10px;
        border: 1px solid #ccc;
        padding: 10px;
        border-radius: 5px;
    }

    .song-image {
        width: 50px; /* Adjust the size of the image */
        height: 50px; /* Adjust the size of the image */
        margin-right: 10px;
        border-radius: 50%; /* For a circular shape */
    }
form {
   width: 600px;
   margin: 50px auto;
   align-items: center;
   padding: 20px;
   border: 2px solid #333;
   border-radius: 10px;
	box-shadow: 0 0 10px #333;

}

/* Apply styles to each form group */
.form-group {
  align-items:center;
  margin-bottom: 15px;
}
h1{
text-align:center;
}
/* Apply styles to labels */
label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

/* Apply styles to input fields */
input {
  width: 100%;
  padding: 10px;
  border-radius: 4px;
  border: 1px solid #ccc;
  box-sizing: border-box;
}

/* Apply styles to the submit button */
input[type="submit"] {
			background-color: #333;
			color: #fff;
			padding: 10px 20px;
			border: none;
			border-radius: 4px;
			font-size: 16px;
			cursor: pointer;
			transition: all 0.3s ease;
		}

		input[type="submit"]:hover {
			background-color: #fff;
			color: #333;
		}


</style>