<template>
  <div class="container mt-4 border p-2 rounded">
    <h1 class="main-heading">Edit Song</h1>
    <div v-if="loading" class="text-center">Loading...</div>
    <div class="d-flex justify-content-center" v-else> <!-- Use v-if here -->
      <div class="col-md-6 col-lg-6 col-xl-5 text-white">
        <form @submit.prevent="updateSong">
          <div class="form-group">
            <label for="name">Name:</label>
            <input
              type="text"
              class="form-control form-control-plain"
              v-model="song.name"
              id="name"
              required
            />
          </div>
          <div class="form-group">
            <label for="lyrics">Lyrics:</label>
            <textarea
              class="form-control form-control-plain"
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
              class="form-control form-control-plain"
              v-model="song.genre"
              id="genre"
              required
            />
          </div>
          <div class="form-group">
            <label for="duration">Duration:</label>
            <input
              type="number"
              class="form-control form-control-plain"
              v-model="song.duration"
              id="duration"
              required
            />
          </div>
          <button type="submit" class="btn btn btn-outline-light d-block mx-auto mt-2 custom-btn">Update Song</button>
        </form>
      </div>
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
    this.albumId = this.$route.params.albumId;
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

