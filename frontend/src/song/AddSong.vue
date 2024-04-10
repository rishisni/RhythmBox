<template>
  <div class="container mt-4">
    <h1>Add Song</h1>
    <form @submit.prevent="addSong">
      <div class="mb-3">
        <label for="name" class="form-label">Song Name</label>
        <input type="text" class="form-control" id="name" v-model="song.name" required>
      </div>
      <div class="mb-3">
        <label for="lyrics" class="form-label">Lyrics</label>
        <textarea class="form-control" id="lyrics" v-model="song.lyrics" rows="5" required></textarea>
      </div>
      <div class="mb-3">
        <label for="genre" class="form-label">Genre</label>
        <input type="text" class="form-control" id="genre" v-model="song.genre" required>
      </div>
      <div class="mb-3">
        <label for="duration" class="form-label">Duration (in seconds)</label>
        <input type="number" class="form-control" id="duration" v-model.number="song.duration" required>
      </div>
      <div class="mb-3">
        <label for="songFile" class="form-label">Song File</label>
        <input type="file" class="form-control" id="songFile" ref="songFile" @change="onFileChange" required>
      </div>
      <div class="d-grid gap-2">
        <button type="submit" class="btn btn-primary">Add Song</button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "@/axios-config";

export default {
  name: "AddSong",
  props: {
    albumId: {
      type: Number,
      required: true, // Make albumId prop mandatory
    },
  },
  data() {
    return {
      song: {
        name: "",
        lyrics: "",
        genre: "",
        duration: 0,
        filePath: null,
      },
    };
  },
  methods: {
    addSong() {
      let formData = new FormData();
      formData.append("name", this.song.name);
      formData.append("lyrics", this.song.lyrics);
      formData.append("genre", this.song.genre);
      formData.append("duration", this.song.duration);
      formData.append("song_file", this.song.filePath);

      axios
        .post(`/albums/${this.albumId}/add-song`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        .then(() => {
          alert("Song added successfully!");
          this.song = {
            albumId: "", // Reset album ID if needed
            name: "",
            lyrics: "",
            genre: "",
            duration: 0,
            filePath: null,
          };
          // Redirect to appropriate location (e.g., album details page)
          this.$router.push(`/albums/${this.albumId}`); // Adjust route if needed
        })
        .catch((error) => {
          console.error("Error adding song:", error);
          alert("Failed to add song. Please try again.");
        });
    },
    onFileChange() {
      this.song.filePath = this.$refs.songFile.files[0];
    },
  },
};
</script>

<style scoped>
/* Add custom styles here if needed */
</style>
