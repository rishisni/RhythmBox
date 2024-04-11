<template>
  <div class="container mt-4 text-light">
    <h1 class="main-heading">Albums</h1>
    <div class="row">
      <div class="col-md-4 mt-2" v-for="album in albums" :key="album.id">
        <div class="card mb-4 bg-dark text-white album-card">
          <!-- Apply Bootstrap's img-fluid class to make the image responsive -->
          <img :src="'data:image/jpeg;base64,' + album.photo_data" class="card-img-top album-image" alt="Album Cover">
          <div class="card-body">
            <h5 class="card-title">{{ album.name }}</h5>
            <p class="card-text">Artist: {{ album.artist }}</p>
            <p class="card-text">Song Count : {{ album.song_count }}</p>
            <div class="d-flex justify-content-between">
              <router-link :to="'/albums/' + album.id + '/add-song'" class="btn " style="background-color: #8a2be2;">
                <i class="fas fa-plus"></i> 
              </router-link>
              <router-link :to="'/albums/' + album.id + '/songs'" class="btn " style="background-color: #8a2be2;">
                <i class="fas fa-music"></i> 
              </router-link>
              <router-link :to="'/albums/' + album.id + '/edit'" class="btn " style="background-color: #8a2be2;">
                <i class="fas fa-pencil-alt"></i> 
              </router-link>
              <button class="btn " @click="confirmDelete(album.id)" style="background-color: #8a2be2;">
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
/* No custom styles needed, Bootstrap classes and color scheme applied */
.album-image {
  height: 300px; 
  object-fit: cover; 
}
</style>
