<template>
  <div class="container mt-4">
    <h1 class="main-heading">Songs</h1>

    <div v-if="songs.length === 0" class="text-center text-white mt-5">No songs found.</div>
    <div v-else>
      <div class="row">
        <div v-for="song in songs" :key="song.id" class="col-md-6 col-lg-4 mb-4">
          <div class="card h-100 text-white bg-dark album-card">
            <div class="card-body">
              <h5 class="card-title text-center mb-3">{{ song.name }}</h5>
              <div class="d-flex justify-content-between mb-3">
                <p class="card-text"><strong>Genre:</strong> {{ song.genre }}</p>
                <p class="card-text"><strong>Duration:</strong> {{ formatDuration(song.duration) }}</p>
              </div>
              <div class="d-flex justify-content-between">
                <p class="card-text"><strong>Added by:</strong> {{ song.added_by.username }}</p>
                <p class="card-text"><strong>Added:</strong> {{ formatDatetime(song.date_created) }}</p>
              </div>
              <audio controls :src="getAudioSource(song)" type="audio/mpeg" class="w-100 mb-3"></audio>
              <div class="d-flex justify-content-between">
                <button @click="showLyrics(song)" class="btn  btn-block mr-2" style="background-color: #8a2be2;">
                  <i class="fas fa-file-audio"></i>
                </button>
                <router-link :to="'/albums/' + albumId + '/songs/' + song.id + '/edit'" class="btn  btn-block" style="background-color: #8a2be2;">
                  <i class="fas fa-pencil"></i>
                </router-link>
                <button @click="deleteSong(song.id)" class="btn  btn-block" style="background-color: #8a2be2;">
                  <i class="fas fa-trash-alt"></i>
                </button>
              </div>
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
  name: "ShowSong",
  data() {
    return {
      albumId: null,
      albumName: "",
      songs: [],
      loading: true,
    };
  },
  mounted() {
    this.albumId = this.$route.params.albumId;
    this.fetchAlbumSongs();
  },
  methods: {
    fetchAlbumSongs() {
      axios
        .get(`/albums/${this.albumId}/songs`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        .then((response) => {
          this.albumName = response.data.album_name;
          this.songs = response.data.songs;
          this.loading = false;
        })
        .catch((error) => {
          console.error("Error fetching album songs:", error);
          this.loading = false;
        });
    },
    showLyrics(song) {
      this.$router.push({
        name: "LyricsPage",
        params: { lyrics: song.lyrics },
      });
    },
    getAudioSource(song) {
      if (song.audio_data) {
        return `data:audio/mpeg;base64,${song.audio_data}`;
      } else {
        return "";
      }
    },
    deleteSong(songId) {
      if (confirm("Are you sure you want to delete this song?")) {
        axios
          .delete(`/albums/${this.albumId}/songs/${songId}`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          })
          .then(() => {
            this.fetchAlbumSongs();
          })
          .catch((error) => {
            console.error("Error deleting song:", error);
          });
      }
    },
    formatDuration(seconds) {
      const minutes = Math.floor(seconds / 60);
      const remainingSeconds = seconds % 60;
      return `${minutes} m ${remainingSeconds} s`;
    },
    formatDatetime(dateCreated) {
      const now = new Date();
      const added = new Date(dateCreated);
      const diffMs = now - added;
      const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
      const diffMinutes = Math.floor(diffMs / (1000 * 60));

      if (diffMinutes < 60) {
        return `${diffMinutes} m ago`;
      } else if (diffHours < 24) {
        return `${diffHours} h ago`;
      } else {
        const options = { year: "numeric", month: "short", day: "numeric" };
        return added.toLocaleDateString(undefined, options);
      }
    },
  },
};
</script>
