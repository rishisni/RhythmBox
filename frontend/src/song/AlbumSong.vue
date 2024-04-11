<template>
  <div class="container mt-4">
    <h1 class="main-heading">{{ albumName }} Songs</h1>
    <div v-if="loading" class="text-center">Loading...</div>
    <div v-else>
      <div v-if="songs.length === 0" class="text-center">No songs found.</div>
      <div v-else>
        <div v-for="song in songs" :key="song.id" class="card mb-3">
          <div class="card-body">
            <h5 class="card-title">{{ song.name }}</h5>
            <p class="card-text">Genre: {{ song.genre }}</p>
            <strong>Duration:</strong> {{ formatDuration(song.duration) }}
            <p class="card-text">Added by: {{ song.added_by.username }}</p>
            <strong>Added</strong> {{ formatDatetime(song.date_created) }}
            <audio
              controls
              :src="getAudioSource(song)"
              type="audio/mpeg"
            ></audio>
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
  name: "AlbumSong",
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

