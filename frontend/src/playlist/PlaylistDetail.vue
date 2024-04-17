<template>
  <div class="container">
    <div class="row justify-content-center mt-4">
      <div class="col-md-6">
        <div
          class="playlist-container bg-dark text-white p-4 rounded album-card"
        >
          <h1>{{ playlist.name }}</h1>
          <ul class="list-group">
            <li
              v-for="song in playlist.songs"
              :key="song.id"
              class="list-group-item d-flex bg-dark text-white justify-content-between align-items-center"
            >
              {{ song.name }}
              
                <audio
                  controls
                  :src="getAudioSource(song)"
                  type="audio/mpeg"
                ></audio>
              
              <button
                @click="removeSong(song.id)"
                class="btn  mr-2 " style="background-color: #8a2be2;"
              >
                <i class="fas fa-trash-alt"></i>
              </button>
            </li>
          </ul>

          <h2 class="mt-4">Add New Song</h2>
          <form @submit.prevent="addNewSong" class="add-song-form">
            <div class="form-group">
              <label for="newSong">Select Song:</label>
              <select v-model="newSong" class="form-control form-control-plain " required>
                <option
                  v-for="song in allSongs"
                  :key="song.id"
                  :value="song.id"
                >
                  {{ song.name }}
                </option>
              </select>
            </div>
            <button type="submit" class="btn btn btn-outline-light d-block mx-auto custom-btn mt-2">Add</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "@/axios-config";

export default {
  data() {
    return {
      playlist: {},
      allSongs: [],
      newSong: null,
    };
  },
  mounted() {
    this.fetchPlaylist();
    this.fetchAllSongs();
  },
  methods: {
    fetchPlaylist() {
      const playlistId = this.$route.params.id;
      axios
        .get(`/playlists/${playlistId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        .then((response) => {
          this.playlist = response.data.playlist;
        })
        .catch((error) => {
          console.error("Error fetching playlist:", error);
        });
    },
    fetchAllSongs() {
      axios
        .get("/songs/all", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        .then((response) => {
          this.allSongs = response.data.songs;
        })
        .catch((error) => {
          console.error("Error fetching songs:", error);
        });
    },
    addNewSong() {
      const playlistId = this.$route.params.id;
      axios
        .post(
          `/playlists/${playlistId}/add-song`,
          { song_id: this.newSong },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          }
        )
        .then((response) => {
          console.log(response.data.message);
          // Optionally, refresh the playlist after adding the song
          this.fetchPlaylist();
        })
        .catch((error) => {
          console.error("Error adding song to playlist:", error);
        });
    },
    removeSong(songId) {
      const playlistId = this.$route.params.id;
      axios
        .delete(`/playlists/${playlistId}/songs/${songId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        .then((response) => {
          console.log(response.data.message);
          // Optionally, refresh the playlist after removing the song
          this.fetchPlaylist();
        })
        .catch((error) => {
          console.error("Error removing song from playlist:", error);
        });
    },
    getAudioSource(song) {
      if (song.audio_data) {
        return `data:audio/mpeg;base64,${song.audio_data}`;
      } else {
        return "";
      }
    },
  },
};
</script>

<style scoped>
.bg-purple {
  background-color: #8a2be2; /* Purple */
}
</style>
