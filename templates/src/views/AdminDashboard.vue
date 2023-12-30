<template>
  <div class="admin" v-if="admin">
    <header>
<ul class="navi_links">
      <h1>Welcome Admin, {{ admin.username }}</h1>
      <li><a><p>@email:{{ admin.email }}</p></a></li>
      
      <li><button class="slo" @click="logout()">Logout</button></li> 
      <li><router-link :to="{ name: 'TrackPage', query: { id:admin.id }}"><button class="slo">Tracks</button></router-link></li>
      <li><router-link :to="{ name: 'AlbumPage', query: { id:admin.id }}"><button class="slo">Albums</button></router-link></li>
</ul>
</header>
    <br>
    <div id="apep" v-if="count">
    <div class="container">
      <div class="box">
        <h2>Song Count</h2>
        <p>{{ count.songCount }}</p>
      </div>
      <div class="box">
        <h2>Album Count</h2>
        <p>{{ count.albumCount }}</p>
      </div>
      <div class="box">
        <h2>User Count</h2>
        <p>{{ count.userCount }}</p>
      </div>
      <div class="box">
        <h2>Creator Count</h2>
        <p>{{ count.creatorCount }}</p>
      </div>
    </div>
  </div>
    <div class="car">
  <img :src="getImageSource(plot)" alt="Summary Image" class="carimg" >
    </div>
  </div>
</template>

<script>
export default {
    name:"AdminDashboard",
    data() {
      return {
      admin: null,
      user:null,
      error: null,
      count:null,
      plot:''
    };
  },
  mounted() {
    this.fetchAdmin();
    this.fetchCounts();
    this.fetchplot();
  },
  methods: {
    fetchplot(){
      fetch(`http://127.0.0.1:5000/api/generate_summary`, {
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
            this.plot = result;
          }
          console.log(this.plot)
        })
        .catch(error => {
          console.error(error);
          this.error = error;
        });
 },
 getImageSource() {
      if (this.plot) {
        return `data:image/png;base64, ${this.plot}`;
      } else {
        return '';
      }
    },
    
    fetchAdmin() {
      const admin_id = this.$route.params.id;
      fetch(`http://127.0.0.1:5000/api/${admin_id}/admin`, {
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
            this.admin = result;
          }
        })
        .catch(error => {
          console.error(error);
          this.error = error;
        });
    },
    async fetchCounts() {
      fetch(`http://127.0.0.1:5000/api/get_counts`, {
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
          console.log(result); 
          if (result) {
            this.count = result;
          }
        })
        .catch(error => {
          console.error(error);
          this.error = error;
        });
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

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Lato', 'Arial', sans-serif;
}
.plot{
  font-size:26px;
 }

.car{
  width: 600px; 
  border: 1px solid #ccc;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); 
  margin: 30px;
 
}


.carimg {
  width: 100%; 
  height: auto; 
  display: block;
}

header{
display:flex;
justify-content:flex-end;
align-items:center;
padding:10px 10%;
background-color:#000;
}
.logo {
cursor:pointer;
margin-right:auto;
}
.navi_links{
list-style:none;
}
.navi_links li{
display:inline-block;
padding:10px 10px;
}
.navi_links h1{
  font-size: 40px;
  float: left;
  margin-right: 700px;
  color:white;
  font-family:fantasy;
}
.navi_links h1 p{
  font-size: 15px;
}
.navi_links li a{
transition:all 0.3s ease 0s;
color:#FFFFFF;
}
.navi_links li a:hover{
color:#0088a9
}
.container {
  display: flex;
  justify-content: space-around;
}

.box {
  border: 1px solid #ccc;
  padding: 20px;
  margin: 10px;
  text-align: center;
}

</style>
   
