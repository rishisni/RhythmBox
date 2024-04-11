<template>
  <div class="container mt-4">
    <h1 class="main-heading">All Songs</h1>
    <div v-if="loading" class="text-center">Loading...</div>
    <div v-else>
      <div v-if="songs.length === 0" class="text-center">No songs found.</div>
      <div v-else>
        <div v-for="song in songs" :key="song.id" class="card mb-3">
          <div class="card-body">
            <p class="card-text">
              <strong>Album:</strong> {{ song.album_name }} &nbsp;|&nbsp;
              <strong>Song:</strong> {{ song.name }} &nbsp;|&nbsp;
              <strong>Artist:</strong> {{ song.artist_name }} &nbsp;|&nbsp;
              <strong>Duration:</strong> {{ formatDuration(song.duration) }}
              <strong>Added</strong> {{ formatDatetime(song.date_created) }}
            </p>
            <div class="audio-player">
              <audio
                controls
                :src="getAudioSource(song)"
                type="audio/mpeg"
              ></audio>
            </div>
            <button @click="showLyrics(song)" class="btn btn-primary mt-2">
              Show Lyrics
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "@/axios-config";

export default {
  name: "AllSongs",
  data() {
    return {
      albumId: "",
      songs: [],
      loading: true,
    };
  },
  mounted() {
    this.fetchAllSongs();
  },
  methods: {
    fetchAllSongs() {
      axios
        .get("/songs/all", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        .then((response) => {
          this.songs = response.data.songs;
          this.loading = false;
        })
        .catch((error) => {
          console.error("Error fetching all songs:", error);
          this.loading = false;
        });
    },
    showLyrics(song) {
      this.$router.push({
        name: "LyricsPage",
        params: { albumId: song.albumId, lyrics: song.lyrics },
      });
    },
    getAudioSource(song) {
      if (song.audio_data) {
        return `data:audio/mpeg;base64,${song.audio_data}`;
      } else {
        return "";
      }
    },
    formatDuration(seconds) {
      const minutes = Math.floor(seconds / 60);
      const remainingSeconds = seconds % 60;
      return `${minutes} min ${remainingSeconds} sec`;
    },
    formatDatetime(dateCreated) {
      const now = new Date();
      const added = new Date(dateCreated);
      const diffMs = now - added;
      const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
      const diffMinutes = Math.floor(diffMs / (1000 * 60));

      if (diffMinutes < 60) {
        return `${diffMinutes} minutes ago`;
      } else if (diffHours < 24) {
        return `${diffHours} hours ago`;
      } else {
        const options = { year: "numeric", month: "short", day: "numeric" };
        return added.toLocaleDateString(undefined, options);
      }
    },
  },
};
</script>

