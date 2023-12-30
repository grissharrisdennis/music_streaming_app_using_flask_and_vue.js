<template>
  <header>
    <ul class="nav_links">
      <h1>Creator Login</h1>
      <li><a ><router-link   :to="{ name: 'UserDashboard', params: { id:this.$route.params.id }}"><button class="slo">UserDashboard</button></router-link></a></li>
    </ul>
  </header>  
    <div class="user-login-dark">
    <form @submit.prevent="login">
      <br>
        <h5>Login</h5>
      <br>
      <br>
      <div class="input-group">
        <label for="username">Username</label>
        <input type="username" id="username" v-model="username" placeholder="Enter your username">
      </div>
        <br>
        <br>
      <div class="input-group">
        <label for="password">Password</label>
        <input type="password" id="password" v-model="password" placeholder="Enter your password">
      </div>
        <br>
        <br>
        <br>
        <button type="log-in-button" >Log In</button>
        <br>
        <h4>Not Registered</h4>
        <h4><router-link class="lie" to="/register">Sign Up</router-link></h4>
      </form>
    </div>
    
  </template>
  
  <script>
  export default {
    name: 'CreatorLogin',
    data() {
      return {
        username: '',
        password: '',
      };
    },
    methods: {
      login() {
        const data = {
          username: this.username,
          password: this.password,
        };
        fetch('http://127.0.0.1:5000/api/creator/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
        })
          .then(response => {
            console.log(response); // Log the response to inspect it
            return response.json();
          })
          .then(result => {
            // Handle the login response
            console.log(result.token);
            console.log(result.id)
  
            if (result.message === 'Creator Successfully Logged In') {
              localStorage.setItem('token', result.token);
              this.$router.push(`/${result.id}/creator/dashboard`);
            } 
          })
          .catch(error => {
            console.error(error);
          });
      },
    },
  };
  
  </script>
  
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
   .user-login-dark {
    height: 100vh;
    width: 100%;
    position: relative;
  }
  @keyframes fade {
    0%{
      opacity:1;
    }
    33%{
      opacity:0;
    }
    66%{
      opacity:0;
    }
    100%{
      opacity: 1;
    }
  }
 
  .user-login-dark form {
    width: 500px;
    height:500px;
    padding: 20px;
    position: static;
    border: 1px solid #ccc;
    border-radius: 5px;
    margin: 0 auto;
    background: #283c86;
    position: relative;
    top: 140px;
  }
  .user-login-dark h5{
    color:#fff;
    font-size:40px;
  }
  .h2{
    position:relative
  }
  .user-login-dark h4{
    font-size:15px;
    color:black;
  }
  .lie{
    text-decoration:none;
    font-size:20px;
    color:#FFFFF0;
  }
  .input-group {
      margin-bottom: 15px;
    }
    
    .input-group label {
      display: block;
      color:#fff;
      margin-bottom: 5px;
    }
    
    .input-group input {
      width: 50%;
      padding: 10px;
      font-size: 16px;
      border-radius: 5px;
      border: 1px solid #ccc;
    }
  
    button[type="log-in-button"] {
      width: 100%;
      padding: 10px;
      font-size: 16px;
      border-radius: 5px;
      border: none;
      background-color: #4caf50;
      color: white;
      cursor: pointer;
    }
  
    button[type="log-in-button"]:hover{
      background-color:#000;
    }
  </style>