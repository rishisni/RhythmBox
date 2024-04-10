<template>
  <div class="container mt-4">
    <h1>Albums</h1>
    <div class="row">
      <div class="col-md-4" v-for="album in albums" :key="album.id">
        <div class="card mb-4">
            <img :src="'/' + album.cover_photo" class="card-img-top" alt="Album Cover">

          <div class="card-body">
            <h5 class="card-title">{{ album.name }}</h5>
            <p class="card-text">Artist: {{ album.artist }}</p>
            <p class="card-text">Song Count : {{ album.song_count }}</p>
            <div class="btn-group" role="group" aria-label="Album Actions">
              <router-link :to="'/albums/' + album.id + '/add-song'" class="btn btn-success ">
              <i class="fas fa-plus"></i> 
            </router-link>
            
            <router-link :to="'/albums/' + album.id + '/songs'" class="btn btn-info ">
              <i class="fas fa-music"></i> 
            </router-link>
              
              <router-link :to="'/albums/' + album.id + '/edit'" class="btn btn-primary">
                <i class="fas fa-pencil-alt"></i> 
              </router-link>
              
              <button class="btn btn-danger" @click="confirmDelete(album.id)">
                <i class="fas fa-trash-alt"></i> 
              </button>
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
  name: "ShowAlbums",
  data() {
    return {
      albums: [],
    };
  },
  mounted() {
    this.getAlbums();
  },
  methods: {
    getAlbums() {
      axios
        .get("/albums", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        .then((response) => {
          this.albums = response.data;
        })
        .catch((error) => {
          console.error("Error fetching albums:", error);
          alert("Failed to fetch albums. Please try again.");
        });
    },
    confirmDelete(albumId) {
      if (confirm("Are you sure you want to delete this album?")) {
        this.deleteAlbum(albumId);
      }
    },
    deleteAlbum(albumId) {
      axios
        .delete(`/albums/${albumId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        .then(() => {
          
          this.albums = this.albums.filter((album) => album.id !== albumId);
          alert("Album deleted successfully.");
        })
        .catch((error) => {
          console.error("Error deleting album:", error);
          alert("Failed to delete album. Please try again.");
        });
    },
  },
};
</script>

<style scoped>
/* Add custom styles here if needed */
</style>
