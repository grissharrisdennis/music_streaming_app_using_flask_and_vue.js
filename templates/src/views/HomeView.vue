<template>
  <NavBar></NavBar> 
  <div class="home">
    <img src="../assets/ani.jpg">
    <img src="../assets/kk.jpg">
    <img src="../assets/chitra.jpg">
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
export default {
  name: 'HomeView',
  components: {
    NavBar,
  },
}
</script>
<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
.home{
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
img{
  width:100%;
  height:100%;
  object-fit: cover;
  position: absolute;
  top:0;
  left:0;
  animation:fade 9s ease-in-out infinite alternate;
}
img:nth-of-type(1){
  animation-delay:0s;
}
img:nth-of-type(2){
  animation-delay:3s;
}
img:nth-of-type(3){
  animation-delay:6s;
}
</style>