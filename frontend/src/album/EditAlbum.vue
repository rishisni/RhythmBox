<template>
  <div class="container-fluid  text-white py-4 d-flex justify-content-center align-items-center">
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
          <button type="submit" class="btn btn-primary d-block mx-auto">Save Changes</button>
        </form>
      </div>
    </div>
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
    };
  },
  created() {
    
    this.fetchAlbum();
  },
  methods: {
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
         
          this.$router.push(`/albums`);
        })
        .catch(error => {
          console.error('Error editing album:', error);
        });
    },
  },
};
</script>

