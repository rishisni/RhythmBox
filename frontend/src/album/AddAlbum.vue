<template>
  <div v-if="userRole.is_admin || userRole.is_creator" class="container-fluid text-white py-4 d-flex justify-content-center align-items-center">
    <div class="col-md-6 col-lg-6 col-xl-5">
      <div class="container mt-4 border rounded p-4">
        <h1 class="main-heading text-center">Add Album</h1>
        <form @submit.prevent="addAlbum">
          <div class="mb-3">
            <label for="name" class="form-label">Album Name</label>
            <input type="text" class="form-control form-control-plain" id="name" v-model="album.name" required>
          </div>
          <div class="mb-3">
            <label for="artist" class="form-label">Artist</label>
            <input type="text" class="form-control form-control-plain" id="artist" v-model="album.artist" required>
          </div>
          <div class="mb-3">
            <label for="coverPhoto" class="form-label">Cover Photo</label>
            <input type="file" class="form-control form-control-plain" id="coverPhoto" @change="onFileChange" required>
          </div>
          <button type="submit" class="btn btn-outline-light d-block mx-auto custom-btn">Add Album</button>
        </form>
      </div>
    </div>
  </div>
  <div v-else>
    <p class="text-white text-center mt-4">You are not authorized to access this page.</p>
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
        photo: null
      },
      userRole: {
        is_admin: false,
        is_creator: false
      }
    };
  },
  mounted() {
    this.getUserRole();
  },
  methods: {
    getUserRole() {
      axios
        .get("/user-role", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`
          }
        })
        .then(response => {
          this.userRole = response.data;
        })
        .catch(error => {
          console.error("Error fetching user role:", error);
        });
    },
    addAlbum() {
      let formData = new FormData();
      formData.append("name", this.album.name);
      formData.append("artist", this.album.artist);
      formData.append("photo", this.album.photo);

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
            photo: null
          };
          this.$router.push('/albums');
        })
        .catch((error) => {
          console.error("Error adding album:", error);
          alert("Failed to add album. Please try again.");
        });
    },
    onFileChange(event) {
      this.album.photo = event.target.files[0];
    }
  }
};
</script>

