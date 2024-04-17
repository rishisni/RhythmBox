<template>
  <div class="container mt-4">
    <h1 class="main-heading">All Songs</h1>
    <div v-if="loading" class="text-center text-white">Loading...</div>
    <div v-else>
      <div v-if="songs.length === 0" class="text-center text-white">No songs found.</div>
      <div v-else>
        <div class="row">
          <div
            v-for="song in songs"
            :key="song.id"
            class="col-md-6 col-lg-4 mb-4"
          >
            <div class="card bg-dark text-white p-4 album-card">
              <div class="card-body">
                <p
                  class="card-text d-flex justify-content-between align-items-center"
                >
                  <strong>Album:</strong> {{ song.album_name }}
                  <strong>Song:</strong> {{ song.name }}
                </p>
                <p
                  class="card-text d-flex justify-content-between align-items-center"
                >
                  <strong>Artist:</strong> {{ song.artist_name }}
                  <strong>Duration:</strong> {{ formatDuration(song.duration) }}
                </p>
                <div class="audio-player">
                  <audio
                    controls
                    :src="getAudioSource(song)"
                    type="audio/mpeg"
                  ></audio>
                </div>
                <div class="d-flex justify-content-between align-items-center">
                  <button
                    @click="showLyrics(song)"
                    class="btn btn-outline-light mt-2" style="background-color: #8a2be2;"
                  >
                    <i class="fas fa-file-audio"></i>
                  </button>
                 <button
                    class="btn btn-outline-light mt-2" style="background-color: #8a2be2;"
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
                    class="btn btn-outline-light mt-2" style="background-color: #8a2be2;"
                    @click="reportSong(song.id)"
                  >
                    <!-- Report button -->
                    <i class="fas fa-flag"></i>
                  </button>
                </div>
                <br />
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
      return `${minutes} m ${remainingSeconds} s`;
    },
    formatDatetime(dateCreated) {
      const now = new Date();
      const added = new Date(dateCreated);
      const diffMs = now - added;
      const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
      const diffMinutes = Math.floor(diffMs / (1000 * 60));

      if (diffMinutes < 60) {
        return `${diffMinutes} min ago`;
      } else if (diffHours < 24) {
        return `${diffHours} hrs ago`;
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

