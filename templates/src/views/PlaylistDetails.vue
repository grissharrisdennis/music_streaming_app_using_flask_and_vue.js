<template>
	<header>

<ul class="navi_links">
      <h1>Playlist</h1>
      <li><router-link  :to="{ name: 'UserDashboard', params: { id: $route.params.id }}"><button class="slo">User DashBoard</button></router-link></li>
</ul>
</header>
<br>
<main v-for="play in playlist" :key="play.id">
  <div class="qwert" v-if="play.id==this.$route.params.playlist_id" >
  <section class="playerss" v-for="song in play.songs" :key="song.id">
    <h2 class="song-titles">{{ song.song_name }}  ft.<span>{{ song.artist }}</span> </h2>
    <br>
   <div clas="contro">
    <audio  ref="audioPlayer" :src="getAudioUrl(song.audio) " @canplaythrough="onAudioCanPlay(song.song_id)"></audio>
    <button class="prev">Prev</button>
    <button class="pausei" v-if="isPlaying" @click="pause()">Pause</button>
    <button class="playi" v-else @click="playing(song.audio)">Play</button>
    <button class="next">Next</button>
   </div>
  </section>
  <br>
  <br>
  <section class="playinglist" v-for="song in play.songs" :key="song.id">
    <h3>{{ play.name }}</h3>
    <button class="song playing">{{ song.song_name }} -{{ song.artist }}</button>
  </section>
</div>
</main>
<!-- <div class="body" v-for="play in playlist" :key="play.id">
<div class="audio-player" >
  <audio ref="audioPlayer" id="audio" @canplaythrough="onAudioCanPlay">
    <source :src="audioSource" id="audioSource" type="audio/mpeg">
  </audio>
<div class="player__header" v-if="play.id==this.$route.params.playlist_id">
  <div class="playa">
    <span class="audio-title" id="audiotitle">{{ play.name }}</span>
  </div>
  <div class="player-middle-row">
    <div class="player-middle-left">
      <span id="audioplaypause"><i class="fa fa-play"></i></span>
      <span id="audiostop"><i class="fa fa-stop"></i></span>
    </div>
    <div class="player-middle-right">
      <span id="duration">0:0</span>
      <span id="durationUpdate">0:0</span>
    </div>
  </div>
  </div>
  <div class="audioplaylistwrap" v-for="song in play.songs" :key="song.id">
    <div class="audio-list" >
      <a class="atrigger" @click="togglePlay(song.audio)"><i :class="isPlaying(song.audio) ? 'fa fa-pause' : 'fa fa-play'"></i></a>
      <div class="audio-list-in">{{ song.song_name }} ft.{{ song.artist }}</div>
    </div>
  </div>
  </div>
</div> -->





  </template>

<script>
export default {
	name:"PlaylistDetails",
	data() {
    return {
      user: null,
      playlist:null,
      audioSource: '', 
      currentAudio: null,
      isPlaying:false,
      player:new Audio

    };
  },
  mounted() {
    this.fetchPlaylist();
    
  }, 
methods:{
  getAudioUrl(audio) {
          return require(`../assets/audios/${audio}`)
        },
        
      playing(audio) {
       this.player.src = this.getAudioUrl(audio);
       console.log(this.player.src);
       this.isPlaying=true
    if (this.player) {
      this.player.play()
        .then(() => {
          // Audio played successfully
          console.log('Audio playback started successfully.');
        })
        .catch(error => {
          // Audio playback failed
          console.error('Error playing audio:', error);
        });
    } else {
      console.error('Cannot play audio. Invalid reference or audio element.');
    }
  },
    pause() {
      
      this.player.pause();
      this.isPlaying = false;
      // if (audioPlayer==this.player.src) {
      //   this.player.pause();
      //   this.isPlaying = false;
      // }
    },
    onAudioCanPlay(songId) {
      console.log(`Audio can play for song ID: ${songId}`);
      // Perform additional actions when audio can play
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
        }   
   
  },
}
</script>


<style scoped>
main{
   width:100%;
   max-width: 768px;
   margin: 0 auto;
   padding: 25px;
}
.song-titles{
  color:#002d2d;
  font-size: 32px;
  font-weight: 700;
  text-transform: uppercase;
  text-align: center;

}
.song-titles span{
  font-weight: 400;
  font-style: italic;
}
.contro{
  display: flex;
  justify-content: center;
  padding: 30px 15px;
  align-items: center;
}
button {
  appearance: none;
  background: none;
  border: none;
  outline: none;
  cursor: none;
}
button:hover{
  opacity: 0.8;
}
.playi, .pausei{
  font-size:20px;
  font-weight: 700;
  padding: 15px 25px;
  margin:0px 15px;
  border-radius: 8px;
  color: #fff;
  background-color: #cc2e50;
}
.next,.prev{
  font-size:16px;
  font-weight: 700;
  padding: 10px 20px;
  margin:0px 15px;
  border-radius: 8px;
  color: #fff;
  background-color: #c50;
}
.playinglist{
  padding: 0px 30px;

}
.playinglist h3{
  color: #212121;
  font-size: 28px;
  font-weight: 400;
  margin-bottom: 30px;
  text-align: center;
}
.playinglist .song{
  display: block;
  width: 100%;
  padding: 15px;
  font-size: 20px;
  font-weight: 700;
  cursor:pointer;
}
.playinglist .song:hover{
  color: #ff5858;
}
.playinglist .song.playing{
  color: #fff;
  background-image: linear-gradient(to right, #cc2e5d,#ff5858);
}


</style>
