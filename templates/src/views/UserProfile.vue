<template>
  <div class="userbook">
    <header>
    <ul class="nav_links">
      <li><h2>Profile</h2></li>
      <li><router-link   :to="{ name: 'UserDashboard', params: { id:this.$route.params.id }}"><button class="slo">UserDashboard</button></router-link></li>
      <li><button @click="logout()" class="slo">Logout</button></li>
    </ul>
</header>
</div>

                    <div class="card swiper-slide">
                        <div class="image-content">
                            <span class="overlay"></span>
                            <div class="card-image">
                                <img src="../assets/white.jpg" alt="" class="card-img">
                            </div>
                        </div>
                        <div class="card-content">
                            <h2 class="name">{{user.username}}</h2>
                            <p class="description">{{ user.email }}</p>
                            <button class="button">View More</button>
                        </div>
                      </div>
               
           

</template>

<script>

export default {
    name:'  UserProfile',
    components: {
  },
    data() {
      return {
      user:'',
    };
  },
    

mounted() {
  this.fetchUser();
  },
    methods:{
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
            this.$router.push(`/login`);
          } else {
            console.log("Logout failed");
          }
        })
        .catch(error => {
          console.error(error);
          
        });
    }
    
    },
    
  }
</script>

<style>
.slide-container{
  max-width: 1120px;
  width: 100%;
  padding: 40px 0;
}
.slide-content{
  margin: 0 40px;
  overflow: hidden;
  border-radius: 25px;
}
.card{
  border-radius: 25px;
  background-color: #FFF;
}
.image-content,
.card-content{
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px 14px;
}
.image-content{
  position: relative;
  row-gap: 5px;
  padding: 25px 0;
}
.overlay{
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: 100%;
  background-color: #4070F4;
  border-radius: 25px 25px 0 25px;
}
.overlay::before,
.overlay::after{
  content: '';
  position: absolute;
  right: 0;
  bottom: -40px;
  height: 40px;
  width: 40px;
  background-color: #4070F4;
}
.overlay::after{
  border-radius: 0 25px 0 0;
  background-color: #FFF;
}
.card-image{
  position: relative;
  height: 150px;
  width: 150px;
  border-radius: 50%;
  background: #FFF;
  padding: 3px;
}
.card-image .card-img{
  height: 100%;
  width: 100%;
  object-fit: cover;
  border-radius: 50%;
  border: 4px solid #4070F4;
}
.name{
  font-size: 18px;
  font-weight: 500;
  color: #333;
}
.description{
  font-size: 14px;
  color: #707070;
  text-align: center;
}
.button{
  border: none;
  font-size: 16px;
  color: #FFF;
  padding: 8px 16px;
  background-color: #4070F4;
  border-radius: 6px;
  margin: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}
.button:hover{
  background: #265DF2;
}
.swiper-navBtn{
  color: #6E93f7;
  transition: color 0.3s ease;
}
.swiper-navBtn:hover{
  color: #4070F4;
}
.swiper-navBtn::before,
.swiper-navBtn::after{
  font-size: 35px;
}
.swiper-button-next{
  right: 0;
}
.swiper-button-prev{
  left: 0;
}
.swiper-pagination-bullet{
  background-color: #6E93f7;
  opacity: 1;
}
.swiper-pagination-bullet-active{
  background-color: #4070F4;
}
@media screen and (max-width: 768px) {
  .slide-content{
    margin: 0 10px;
  }
  .swiper-navBtn{
    display: none;
  }
}
.nav_links h2{
  color:#fff;
}
.containers{
    width:30em;
    margin-left:30px;
    font-family:sans-serif;
    display:flex;
    flex-wrap:wrap;
}
.cardn {
    background:linear-gradient(to bottom ,black 0%,black 26%,#ecedef 26%,#ecedef 100%);
    height:16em;
    padding:1em;
    float:left;
    position:relative;
    margin-top:100px;
}
.card-left{
    border-top-left-radius:8px;
    border-bottom-left-radius:8px;
    width:19em;
}
.card-right{
    width:6.5em;
    border-left:0.18em dashed #fff;
    border-top-left-radius:8px;
    border-bottom-left-radius:8px;
}
.card-right::before,.card-right::after{
    width:0.9em;
    height:0.9em;
    background-color:#fff;
    content:"";
    position:absolute;
    display:block;
    border-radius:50%;
    left:-0.5em;
}
.card-right::before{
    top:-0.4em;
}
.card-right::after{
    bottom:-0.4em;
}
        h1{
        font-size:1.0em;
        margin-top:0;
        color:#fff;
        width: 100%;
        }
        h1 span{
        font-weight:normal;
        }        
        .title,
        .name,
        .seat,
        .time{
        text-transform:uppercase;
        font-weight:normal;
        }
        .title h2,
        .name h2,
        .seat h2,
        .time h2{
        font-size:0.7em;
        color:#525252;
        margin:0;
        }
        .title span ,
        .name span,
        .seat span,
        .time span{
        font-size:0.5em;
        color:#a2aeae;
        }
        .title{
         margin:2em 0 0 0;
        }
        .name
        .seat{
         margin:0.7em 0 0 0;
        }
        .time{
        margin:0.7em 0 0 0;
        }
        .time,
        .seat{
        float:left;
        }
        .eye{
        position:relative;
        width:2em;
        height:1.5em;
        background:#fff;
        margin:0 auto;
        border-radius:1em/0.6em;
        z-index:1;
        }
        .eye::before,
        .eye::after{
        content:"";
        display:block;
        position:absolute;
        border-radius:50%;
        }
        .eye::before{
        width:1em;
        background:#3dcee8;
        height:1em;
        z-index:2;
        left:8px;
        top:4px;
        }
        .eye::after{
        width:0.5em;
        background:#fff;
        height:0.5em;
        z-index:3;
        left:12px;
        top:8px;
        }
        .number{
        text-transform:uppercase;
        text-align:center;
        }
        .number h2{
        color:#2980B9;
        margin:0.9em 0 0 0;
        font-size:2.5em;
        }
.number span{
    display:block;
    color:#a2aeae;
}
</style>