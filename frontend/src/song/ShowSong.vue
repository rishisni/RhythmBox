<template>
  <div class="container mt-4">
    <h1>Song Details</h1>
    <div v-if="song">
      <div class="row mb-3">
        <label for="name" class="col-sm-2 col-form-label">Name</label>
        <div class="col-sm-10">{{ song.name }}</div>
      </div>
      <div class="row mb-3">
        <label for="lyrics" class="col-sm-2 col-form-label">Lyrics</label>
        <div class="col-sm-10" v-html="song.lyrics"></div>
      </div>
      <div class="row mb-3">
        <label for="genre" class="col-sm-2 col-form-label">Genre</label>
        <div class="col-sm-10">{{ song.genre }}</div>
      </div>
      <div class="row mb-3">
        <label for="duration" class="col-sm-2 col-form-label">Duration</label>
        <div class="col-sm-10">{{ formatDuration(song.duration) }}</div>
      </div>
      <div class="row mb-3">
        <label for="dateCreated" class="col-sm-2 col-form-label">Date Added</label>
        <div class="col-sm-10">{{ song.date_created.toLocaleDateString() }}</div>
      </div>
      <div v-if="song.filePath">
        <audio :src="song.filePath" controls></audio>
      </div>
    </div>
    <div v-else>
      <p>Loading song details...</p>
    </div>
  </div>
</template>

<script>
import axios from "@/axios-config";
export default {
  name: "ShowSong",
  props: {
    albumId: {
      type: Number,
      required: true,
    },
    songId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      song: null,
    };
  },
  created() {
    this.fetchSong();
  },
  methods: {
    fetchSong() {
      axios
        .get(`/albums/${this.albumId}/songs/${this.songId}`)
        .then((response) => (this.song = response.data))
        .catch((error) => console.error("Error fetching song:", error));
    },
    formatDuration(duration) {
      const minutes = Math.floor(duration / 60);
      const seconds = duration % 60;
      return `${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
    },
  },
};
</script>

<style scoped>
/* Add custom styles here if needed */
</style>
