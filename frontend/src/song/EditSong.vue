<template>
  <div class="container mt-4">
    <h1 class="main-heading">Edit Song</h1>
    <div v-if="loading" class="text-center">Loading...</div>
    <div v-else>
      <form @submit.prevent="updateSong">
        <div class="form-group">
          <label for="name">Name:</label>
          <input
            type="text"
            class="form-control"
            v-model="song.name"
            id="name"
            required
          />
        </div>
        <div class="form-group">
          <label for="lyrics">Lyrics:</label>
          <textarea
            class="form-control"
            v-model="song.lyrics"
            id="lyrics"
            rows="5"
            required
          ></textarea>
        </div>
        <div class="form-group">
          <label for="genre">Genre:</label>
          <input
            type="text"
            class="form-control"
            v-model="song.genre"
            id="genre"
            required
          />
        </div>
        <div class="form-group">
          <label for="duration">Duration:</label>
          <input
            type="number"
            class="form-control"
            v-model="song.duration"
            id="duration"
            required
          />
        </div>
        <button type="submit" class="btn btn-primary">Update Song</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "@/axios-config";

export default {
  name: "EditSong",
  data() {
    return {
      songId: null,
      song: {
        name: "",
        lyrics: "",
        genre: "",
        duration: "",
      },
      loading: true,
    };
  },
  mounted() {
    this.songId = this.$route.params.songId;
    this.fetchSong();
  },

  methods: {
    fetchSong() {
      axios
        .get(`/songs/${this.songId}`)
        .then((response) => {
          this.song = response.data;
          this.loading = false;
        })
        .catch((error) => {
          console.error("Error fetching song:", error);
          this.loading = false;
        });
    },
    updateSong() {
      
      axios
        .put(
          `/albums/${this.$route.params.albumId}/songs/${this.songId}`,
          this.song,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          }
        )
        .then(() => {
          this.$router.push({
            name: "ShowSong",
            params: { albumId: this.$route.params.albumId },
          });
        })
        .catch((error) => {
          console.error("Error updating song:", error);
        });
    },
  },
};
</script>

