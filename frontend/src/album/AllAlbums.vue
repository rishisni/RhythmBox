<template>
  <div class="container mt-4">
    <h1 class="main-heading">All Albums</h1>
    <!-- If user is not authenticated, display message and login button -->
    <div v-if="!authenticated" class="text-center text-white">
      <p>Please login to view all albums.</p>
      <router-link to="/login" class="btn btn-outline-light custom-btn">Login</router-link>
    </div>
    <div v-else>
      <div v-if="albums.length === 0" class="text-center text-white">
        <p>No albums found.</p>
      </div>
      <div v-else class="row">
        <div class="col-md-4" v-for="album in albums" :key="album.id">
          <div class="card mb-4 bg-dark text-white album-card">
            <img :src="'data:image/jpeg;base64,' + album.photo_data" class="card-img-top album-image" alt="Album Cover">
            <div class="card-body">
              <h5 class="card-title">{{ album.name }}</h5>
              <p class="card-text">Artist: {{ album.artist }}</p>
              <p class="card-text">Song Count: {{ album.song_count }}</p>
              <p class="card-text">Created By: {{ album.created_by.username }}</p>
              <router-link :to="'/albums/' + album.id + '/album-songs'" class="btn btn-block" style="background-color: #8a2be2;">
                <i class="fas fa-music"></i> Songs
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "@/axios-config";

export default {
  name: "AllAlbums",
  data() {
    return {
      albums: [],
    };
  },
  computed: {
    authenticated() {
      return !!localStorage.getItem("access_token");
    },
  },
  mounted() {
    if (this.authenticated) {
      this.getAlbums();
    }
  },
  methods: {
    getAlbums() {
      axios
        .get("/albums/all", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        .then((response) => {
          this.albums = response.data;
        })
        .catch((error) => {
          console.error("Error fetching albums:", error);
        });
    },
  },
};
</script>

<style scoped>
.album-image {
  height: 300px; /* Set the height of the image */
  object-fit: cover; /* Ensure the image covers the entire area */
}

.main-heading {
  font-family: "Roboto", sans-serif; /* Use Google Font Roboto */
  font-size: 3.5rem; /* Adjust the font size as needed */
  font-weight: 700; /* Use bold font weight */
  text-align: center;
  margin-bottom: 30px; /* Add some space below the heading */
  text-shadow: 4px 4px 8px #8a2be2; /* Add a subtle shadow */
  color: #ffffff; /* Set the text color to white */
  letter-spacing: 2px; /* Add letter spacing for better readability */
}
</style>
