<template>
  <div >
  
    <div class="music-stream-home">
      <div class="container mt-4">
        <div class="row">
          <div class="col-md-6 col-sm-12">
            <img src="images/music.png" alt="Image 1" class="img-fluid rounded" />
          </div>
          <div class="col-md-6 col-sm-12">
            <img src="images/music1.avif" alt="Image 2" class="img-fluid rounded" />
          </div>
        </div>
        <div class="row mt-4">
          <div class="col-md-6 trending">
            <h2>Trending Songs</h2>
            <ul>
              <li>Song 1</li>
              <li>Song 2</li>
              <li>Song 3</li>
            </ul>
          </div>
          <div class="col-md-6 new_song">
            <h2 class="heading">New Songs</h2>
            <ul>
              <li>New Song 1</li>
              <li>New Song 2</li>
              <li>New Song 3</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>



<script>
export default {
  name: 'HomePage',
}
</script>

<style scoped>
.music-stream-home {
  background-color: black;
  
  background-size: cover;
  background-position: center;
}

.navbar {
  background-color: #8a2be2;
  margin-bottom: 0;
}
.navbar-logo {
  height: 40px;
  width: 150px;
}
.img-fluid {
  margin:10px;
  position: center;
  padding: 2px;
  background-color: #8a2be2;

  height: 400px;
}
.trending {
  color: white;
}
.new_song {
  color: white;
}
.nav-button {
  border: 1px solid transparent;
  background-color: transparent;
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 4px;
  box-shadow: 0 0 8px rgba(142, 140, 140, 0.1),
    0 4px 8px rgba(142, 140, 140, 0.1);
}

.nav-button:hover {
  color: white;
  border-color: rgb(234, 229, 229);
  background-color: rgba(0, 0, 0, 0.1);
}

.nav-button:focus {
  outline: none;
}

ul {
  list-style-type: none;
  padding-left: 0;
}

ul li {
  margin-bottom: 10px;
}

@media (max-width: 768px) {
  .music-stream-home {
    padding: 10px;
  } }
</style>
