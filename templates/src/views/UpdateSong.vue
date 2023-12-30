<template>
    <header>

<ul class="navi_links">
      <h1>Update Songs</h1>
      <li><router-link  :to="{ name: 'CreatorDashboard', params: { id: $route.params.id }}"><button class="slo">DashBoard</button></router-link></li>
      <li><button class="slo" @click="logout()">Logout</button></li>   
</ul>
</header>
<br>


<form >
    
    <br>
    <br>
  <div class="form-group">
    <label for="song_name">Song Name:</label>
    <input type="text" id="song_name" v-model="song_name" name="song_name">
  </div>

  <div class="form-group">
    <label for="genre">Genre:</label>
    <input type="text" id="genre" v-model="genre" name="genre">
  </div>

  <div class="form-group">
    <label for="artist">Artist:</label>
    <input type="text" id="artist" v-model="artist" name="artist">
  </div>

   <div class="form-group">
    <label for="release">Release Date:</label>
    <input type="date" id="release"  v-model="release" name="release" required>
  </div>
  
  <div class="form-group">
		<label for="image">Image File</label>
		<input type="file" class="form-control-file" @change="select_image($event)" id="image" name="image">
	</div>

  <div class="form-group">
    <label for="lyrics">Lyrics:</label>
    <input type="text" id="lyrics" v-model="lyrics" name="lyrics">
  </div>

  <button type="submit"  @click="UpdateSong">Upload</button>
</form>
</template>

<script>
export default {
  name:"UpdateSong",
  data() {
      return {
        song_name: '',
        artist: '',
        genre: '',
        release: '',
        lyrics: '',
        image: null
    };
  },
methods:{
  select_image(event){
		const file = event.target.files[0];
		this.image_file=file
		console.log("image",this.image_file)
    console.log(this.$route.params.song_id)
	},
  async UpdateSong() {
    const song_id = this.$route.params.song_id;
    const formData = new FormData();
    formData.append("song_name", this.song_name);
    formData.append("artist", this.artist);
    formData.append("genre", this.genre);
    formData.append("release", this.release);
    formData.append("lyrics", this.lyrics);
    formData.append("image", this.image);

    try {
      const response =await  fetch(`http://127.0.0.1:5000/api/${song_id}/put/song`, {
        method: "PUT",
        headers: {
          // 'Content-Type': 'multipart/form-data',
          Accept: "application/json",
          "Authentication-Token": localStorage.getItem("token"),
        },
        body: formData,
      });
      if (!response.ok) {
        const errorMessage = await response.text();
        console.error("Error from backend:", errorMessage);
        return;
      }
      const data =await response.json();
      console.log(data.message);
      this.$router.push(`/${this.$route.params.id}/creator/dashboard`);
    } catch (error) {
      console.error("Error while sending the request:", error);
    }
  },
  
  }
}
</script>

<style>
form {
  width: 500px;
   margin: 50px auto;
   align-items: center;
   padding: 20px;
   border: 2px solid #333;
   border-radius: 10px;
	box-shadow: 0 0 10px #333;
}

/* Apply styles to each form group */
.form-group {
  margin-bottom: 15px;
}

/* Apply styles to labels */
label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

/* Apply styles to input fields */
input {
  width: 50%;
  padding: 10px;
  border-radius: 4px;
  border: 1px solid #ccc;
  box-sizing: border-box;
}

/* Apply styles to the submit button */
button[type="submit"] {
  background-color: #333;
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>