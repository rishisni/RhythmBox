<template>
  <div class="container mt-4">
    <h1>Add Album</h1>
    <form @submit.prevent="addAlbum">
      <div class="mb-3">
        <label for="name" class="form-label">Album Name</label>
        <input type="text" class="form-control" id="name" v-model="album.name" required>
      </div>
      <div class="mb-3">
        <label for="artist" class="form-label">Artist</label>
        <input type="text" class="form-control" id="artist" v-model="album.artist" required>
      </div>
      <div class="mb-3">
        <label for="coverPhoto" class="form-label">Cover Photo</label>
        <input type="file" class="form-control" id="coverPhoto" @change="onFileChange" required>
      </div>
      <button type="submit" class="btn btn-primary">Add Album</button>
    </form>
  </div>
</template>

<script>
import axios from "@/axios-config";

export default {
  name: "AddAlbum",
  data() {
    return {
      album: {
        name: "",
        artist: "",
        coverPhoto: null
      }
    };
  },
  methods: {
    addAlbum() {
      let formData = new FormData();
      formData.append("name", this.album.name);
      formData.append("artist", this.album.artist);
      formData.append("cover_photo", this.album.coverPhoto);

      axios
        .post("/add-album", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
            Authorization: `Bearer ${localStorage.getItem("access_token")}`
          }
        })
        .then(() => {
          alert("Album added successfully");
          
          this.album = {
            name: "",
            artist: "",
            coverPhoto: null
          };
          this.$router.push('/albums');
        })
        .catch((error) => {
          console.error("Error adding album:", error);
          alert("Failed to add album. Please try again.");
        });
    },
    onFileChange(event) {
      this.album.coverPhoto = event.target.files[0];
    }
  }
};
</script>

<style scoped>
/* Add custom styles here if needed */
</style>
