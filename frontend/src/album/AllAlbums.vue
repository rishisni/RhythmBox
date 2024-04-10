<template>
  <div class="container mt-4">
    <h1>All Albums</h1>
    <div v-if="albums.length === 0">
      <p>No albums found.</p>
    </div>
    <div v-else class="row">
      <div class="col-md-4" v-for="album in albums" :key="album.id">
        <div class="card mb-4">
          
          <img :src="'/' + album.cover_photo" class="card-img-top" alt="Album Cover">

          <div class="card-body">
            <h5 class="card-title">{{ album.name }}</h5>
            <p class="card-text">Artist: {{ album.artist }}</p>
            <p class="card-text">Song Count: {{ album.song_count }}</p>
            <p class="card-text">Created By: {{ album.created_by.username }}</p>
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
  name: "AllAlbums",
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
        .get("/albums/all", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`
          }
        })
        .then((response) => {
          this.albums = response.data;
        })
        .catch((error) => {
          console.error("Error fetching albums:", error);
          
        });
    },
    getAlbumImageUrl(album) {
      
      return `/static/uploads/images/${album.cover_photo}`;
    }
  }
};
</script>

<style scoped>
.album-image {
  height: 300px; 
  object-fit: cover; 
}
</style>