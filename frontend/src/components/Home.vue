<template>
  <div class="music-stream-home">
    <div class="container mt-4">
      <div class="row mb-4 text-white">
        <div class="col-md-12">
          <h2>Welcome to our Music Streaming Platform!</h2>
          <p>
            Discover the latest hits, explore your favorite genres, and enjoy an
            immersive music experience like never before.
          </p>
        </div>
      </div>
      <div class="row">
        <div class="col-md-6 col-sm-12">
          <div class="image-container">
            <img
              src="images/image1.jpg"
              alt="Image 1"
              class="img-fluid rounded"
            />
          </div>
        </div>
        <div class="col-md-6 col-sm-12">
          <div class="image-container">
            <img
              src="images/image2.jpg"
              alt="Image 2"
              class="img-fluid rounded"
            />
          </div>
        </div>
      </div>
      <div class="row mt-4 justify-content-between">
        <div class="col-md-4 trending">
          <h2>Recently Added Songs</h2>
          <ul>
            <li v-for="song in topSongs" :key="song.id">
              <strong>{{ song.name }}</strong>
            </li>
          </ul>
        </div>
        <div class="col-md-4 new-song">
          <h2>Most Liked Songs</h2>
          <ul>
            <li v-for="song in topLikedSongs" :key="song.id">
              <strong>{{ song.name }}</strong>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "@/axios-config";

export default {
  name: "HomePage",
  data() {
    return {
      topSongs: [],
      topLikedSongs: [],
    };
  },
  mounted() {
    this.fetchTopSongs();
    this.fetchTopLikedSongs();
  },
  methods: {
    fetchTopSongs() {
      axios
        .get("/songs/top")
        .then((response) => {
          this.topSongs = response.data.top_songs;
        })
        .catch((error) => {
          console.error("Error fetching top songs:", error);
        });
    },
    fetchTopLikedSongs() {
      axios
        .get("/songs/top-liked")
        .then((response) => {
          this.topLikedSongs = response.data.top_liked_songs;
        })
        .catch((error) => {
          console.error("Error fetching top liked songs:", error);
        });
    },
  },
};
</script>

<style scoped>
.image-container {
  margin-bottom: 20px;
}

.trending,
.new-song {
  /* background-color: #f8f9fa; */
  padding: 20px;
}

.trending h2,
.new-song h2 {
  margin-bottom: 15px;
  font-size: 24px;
}
</style>
