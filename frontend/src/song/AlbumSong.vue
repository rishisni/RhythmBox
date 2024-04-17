<template>
  <div class="container mt-4">
    <h1 class="main-heading">{{ albumName }} Songs</h1>
    <div v-if="loading" class="text-center text-white mt-5">Loading...</div>
    <div v-else>
      <div v-if="songs.length === 0" class="text-center text-white mt-5">
        No songs found.
      </div>
      <div v-else>
        <div class="row">
          <div
            v-for="song in songs"
            :key="song.id"
            class="col-md-6 col-lg-4 mb-4"
          >
            <div class="card h-100 text-white bg-dark album-card">
              <div class="card-body">
                <h5 class="card-title text-center mb-3">{{ song.name }}</h5>
                <div class="d-flex justify-content-between mb-3">
                  <p class="card-text">
                    <strong>Genre:</strong> {{ song.genre }}
                  </p>
                  <p class="card-text">
                    <strong>Duration:</strong>
                    {{ formatDuration(song.duration) }}
                  </p>
                </div>
                <audio
                  controls
                  :src="getAudioSource(song)"
                  type="audio/mpeg"
                  class="w-100 mb-3"
                ></audio>
                <div class="d-flex justify-content-between">
                  <p class="card-text">
                    <strong>Added by:</strong> {{ song.added_by.username }}
                  </p>
                  <p class="card-text">
                    <strong>Added:</strong>
                    {{ formatDatetime(song.date_created) }}
                  </p>
                </div>
                <div class="d-flex justify-content-between align-items-center">
                  <button
                    @click="showLyrics(song)"
                    class="btn btn-outline-light mt-2"
                    style="background-color: #8a2be2"
                  >
                    <i class="fas fa-file-audio"></i>
                  </button>
                  <button
                    class="btn btn-outline-light mt-2"
                    style="background-color: #8a2be2"
                    @click="toggleLike(song.id)"
                  >
                    <i
                      :class="{
                        'fas fa-heart': song.liked,
                        'far fa-heart': !song.liked,
                      }"
                    ></i>
                  </button>

                  <button
                    class="btn btn-outline-light mt-2"
                    style="background-color: #8a2be2"
                    @click="reportSong(song.id)"
                  >
                    <!-- Report button -->
                    <i class="fas fa-flag"></i>
                  </button>
                </div>
                <br>
                <div class="d-flex justify-content-between align-items-center">
                  <p>Added: {{ formatDatetime(song.date_created) }}</p>
                  <p>Likes: {{ song.like_count }}</p>
                </div>
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
    toggleLike(songId) {
      axios
        .post(
          `/songs/${songId}/like`,
          {},
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          }
        )
        .then((response) => {
          const updatedSong = this.songs.find((song) => song.id === songId);
          updatedSong.like_count = response.data.like_count;
          updatedSong.liked = !updatedSong.liked;
          alert("Song liked successfully!");
        })
        .catch((error) => {
          console.error("Error toggling like status:", error);
          alert("Failed to like the song. Please try again.");
        });
    },
    reportSong(songId) {
      axios
        .post(
          `/songs/${songId}/report`,
          {},
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          }
        )
        .then(() => {
          alert("Song reported successfully!");
        })
        .catch((error) => {
          console.error("Error reporting song:", error);
          alert("Failed to report the song. Please try again.");
        });
    },
  },
};
</script>

