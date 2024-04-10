<template>
  <div>
    <h1>Edit Album</h1>
    <form @submit.prevent="editAlbum">
      <div>
        <label for="name">Name:</label>
        <input type="text" id="name" v-model="editedAlbum.name" required>
      </div>
      <div>
        <label for="artist">Artist:</label>
        <input type="text" id="artist" v-model="editedAlbum.artist" required>
      </div>
      <button type="submit">Save Changes</button>
    </form>
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
<style scoped>

</style>
