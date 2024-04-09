<template>
  <div class="container mt-4">
    <h1>Albums</h1>
    <div class="row">
      <div class="col-md-4" v-for="album in albums" :key="album.id">
        <div class="card mb-4">
          <img :src=" 'uploads/images/' + album.cover_photo" class="card-img-top" alt="Album Cover">
          <div class="card-body">
            <h5 class="card-title">{{ album.name }}</h5>
            <p class="card-text">Artist: {{ album.artist }}</p>
            <router-link :to="'/albums/' + album.id" class="btn btn-primary">View Details</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "@/axios-config";

export default {
  name: "ShowAlbums",
  data() {
    return {
      albums: []
    };
  },
  mounted() {
    this.getAlbums();
  },
  methods: {
    getAlbums() {
      axios
        .get("/albums",{
        headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`
          }
        })
        .then((response) => {
          this.albums = response.data;
        })
        .catch((error) => {
          console.error("Error fetching albums:", error);
          alert("Failed to fetch albums. Please try again.");
        });
    }
  }
};
</script>

<style scoped>
/* Add custom styles here if needed */
</style>
