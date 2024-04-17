<template>
  <div v-if="userRole.is_admin || userRole.is_creator" class="container-fluid text-white py-4 d-flex justify-content-center align-items-center">
    <div class="col-md-6 col-lg-6 col-xl-5">
      <div class="container mt-4 border rounded p-4">
        <h1 class="main-heading text-center">Edit Album</h1>
        <form @submit.prevent="editAlbum">
          <div class="mb-3">
            <label for="name" class="form-label">Name:</label>
            <input type="text" class="form-control form-control-plain" id="name" v-model="editedAlbum.name" required>
          </div>
          <div class="mb-3">
            <label for="artist" class="form-label">Artist:</label>
            <input type="text" class="form-control form-control-plain" id="artist" v-model="editedAlbum.artist" required>
          </div>
          <button type="submit" class="btn btn btn-outline-light d-block mx-auto custom-btn">Save Changes</button>
        </form>
        <p v-if="successMessage" class="text-success mt-3">{{ successMessage }}</p>
        <p v-if="errorMessage" class="text-danger mt-3">{{ errorMessage }}</p>
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
  data() {
    return {
      editedAlbum: {
        id: null,
        name: '',
        artist: '',
      },
      userRole: {
        is_admin: false,
        is_creator: false
      },
      successMessage: '',
      errorMessage: ''
    };
  },
  created() {
    this.getUserRole();
    this.fetchAlbum();
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
    fetchAlbum() {
      const albumId = this.$route.params.id;
      axios.get(`/albums/${albumId}`)
        .then(response => {
          this.editedAlbum = response.data;
        })
        .catch(error => {
          console.error('Error fetching album:', error);
        });
    },
    editAlbum() {
      const albumId = this.$route.params.id;
      axios.put(`/albums/${albumId}`, this.editedAlbum, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`
          }
        })
        .then(() => {
          this.successMessage = 'Album edited successfully.';
          setTimeout(() => {
            this.successMessage = '';
          }, 3000);
          this.$router.push(`/albums`);
        })
        .catch(error => {
          this.errorMessage = 'Failed to edit album. Please try again.';
          console.error('Error editing album:', error);
          setTimeout(() => {
            this.errorMessage = '';
          }, 3000);
        });
    },
  },
};
</script>
