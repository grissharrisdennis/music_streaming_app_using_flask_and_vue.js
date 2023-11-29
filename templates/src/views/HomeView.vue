<template>
  <NavBar></NavBar> 
  <div class="home">
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
.home{
  height:800px;
  background: url('../assets/ani.jpg'),url('../assets/kk.jpg'),url('../assets/chitra.jpg');
  background-repeat: no-repeat,no-repeat;
  padding: 15px;
  background-position: left,center,right;
  background-size: contain;
}
</style>