<template>
  <div>
    <header>

<ul class="navi_links">
      <h1>Create Album</h1>
      <li><router-link  :to="{ name: 'CreatorDashboard', params: { id: $route.params.id }}"><button class="slo">DashBoard</button></router-link></li>
      <li><button class="slo" @click="logout()">Logout</button></li>   
</ul>
</header>
<br>


<form >
    
    <br>
    <br>
  <div class="form-group">
    <label for="album_name">Album Name:</label>
    <input type="text" id="album_name" v-model="album_name" name="album_name">
  </div>

  <div class="form-group">
    <label for="artist">Artist:</label>
    <input type="text" id="artist" v-model="artist" name="artist">
  </div>

   <div class="form-group">
    <label for="language">Language:</label>
    <input type="text" id="language"  v-model="language" name="language" required>
  </div>

  <button type="submit"  @click="create_album">Create</button>
</form>
</div>
</template>

<script>
export default {
  name:"CreateAlbum",
  data() {
      return {
        album_name: '',
        artist: '',
        language: '',
    };
  },
methods:{
  async create_album() {
    const data = {
      album_name: this.album_name,
      artist: this.artist,
      language: this.language
    };

    try {
      const response = await fetch(`http://127.0.0.1:5000/api/post/album`, {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Authentication-Token": localStorage.getItem("token"),
          "Content-Type": "application/json" // Add this line to specify JSON content type
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const errorMessage = await response.text();
        console.error("Error from backend:", errorMessage);
        return;
      }

      const responseData = await response.json();
      console.log(responseData.message);
      this.$router.push(`/${this.$route.params.id}/creator/dashboard`);
    } catch (error) {
      console.error("Error while sending the request:", error);
      // Handle error cases
    }
  }
  
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