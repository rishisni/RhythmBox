<template>
  <div class="container mt-4">
    <div class="row justify-content-center text-white">
      <div class="col-md-4 col-10 bg-dark album-card p-4 rounded">
        <h1 class="text-center mb-4">Create Playlist</h1>
        <form @submit.prevent="createPlaylist">
          <div class="form-group">
            <label for="name">Name:</label>
            <input
              type="text"
              id="name"
              v-model="playlistName"
              class="form-control form-control-plain"
              required
            />
          </div>
          <button type="submit" class="btn btn btn-outline-light d-block mx-auto custom-btn mt-2">
            Create
          </button>
        </form>
      </div>
    </div>

    <div class="row justify-content-center mt-4 text-white">
      <div class="col-md-4 col-10 bg-dark album-card p-4 rounded">
        <h2 class="text-center mb-4">Your Playlists</h2>
        <div v-if="playlists && playlists.length > 0">
          <ul class="list-group">
            <li
              v-for="playlist in playlists"
              :key="playlist.id"
              class="list-group-item bg-dark text-white"
            >
              <div class="d-flex justify-content-between align-items-center">
                <span>{{ playlist.name }}</span>
                <div class="d-flex justify-content-between ">
                  <router-link
                    :to="{ name: 'PlaylistDetail', params: { id: playlist.id } }"
                    class="btn  mr-2 " style="background-color: #8a2be2;"
                    ><i class="fas fa-eye"></i
                  ></router-link>
                  <button
                    @click="showAddSongForm(playlist.id)"
                    class="btn  mr-2 " style="background-color: #8a2be2;"
                  >
                    <i class="fas fa-plus"></i>
                  </button>
                  <button
                    @click="deletePlaylist(playlist.id)"
                   class="btn  mr-2 " style="background-color: #8a2be2;"
                  >
                    <i class="fas fa-trash"></i>
                  </button>
                </div>
              </div>
              <form
                v-if="showAddSongForms[playlist.id]"
                @submit.prevent="addSong(playlist.id)"
                class="mt-2"
              >
                <div class="form-group">
                  <label for="song">Select Song:</label>
                  <select
                    v-model="selectedSong"
                    class="form-control form-control-plain"
                    required
                  >
                    <option
                      v-for="song in songs"
                      :key="song.id"
                      :value="song.id"
                    >
                      {{ song.name }}
                    </option>
                  </select>
                </div>
                <button type="submit" class="btn btn-primary mt-2">Add</button>
              </form>
            </li>
          </ul>
        </div>
        <div v-else>
          <p>No playlists created yet.</p>
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
      playlistName: "",
      playlists: [],
      songs: [],
      showAddSongForms: {}, // Object to track visibility of add song forms for each playlist
      selectedSong: null,
    };
  },
  mounted() {
    // Fetch user's playlists and songs upon component mounting
    this.fetchPlaylists();
    this.fetchSongs();
  },
  methods: {
    fetchPlaylists() {
      axios
        .get("/playlists", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        .then((response) => {
          this.playlists = response.data.playlists;
          // Initialize showAddSongForms object with false for each playlist
          this.playlists.forEach((playlist) => {
            this.$set(this.showAddSongForms, playlist.id, false);
          });
        })
        .catch((error) => {
          console.error("Error fetching playlists:", error);
        });
    },
    fetchSongs() {
      axios
        .get("/songs/all", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        .then((response) => {
          this.songs = response.data.songs;
        })
        .catch((error) => {
          console.error("Error fetching songs:", error);
        });
    },
    createPlaylist() {
      axios
        .post(
          "/create-playlist",
          { name: this.playlistName },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          }
        )
        .then((response) => {
          console.log(response.data.message);
          // Optionally, refresh the list of playlists after successful creation
          this.fetchPlaylists();
        })
        .catch((error) => {
          console.error("Error creating playlist:", error);
        });
    },
    showAddSongForm(playlistId) {
      // Toggle visibility of add song form for the specified playlist
      this.showAddSongForms[playlistId] = !this.showAddSongForms[playlistId];
    },
    addSong(playlistId) {
      axios
        .post(
          `/playlists/${playlistId}/add-song`,
          { song_id: this.selectedSong },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          }
        )
        .then((response) => {
          console.log(response.data.message);
          // Optionally, refresh the list of playlists after adding the song
          this.fetchPlaylists();
        })
        .catch((error) => {
          console.error("Error adding song to playlist:", error);
        });
    },
    deletePlaylist(playlistId) {
      axios
        .delete(`/playlists/${playlistId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        .then((response) => {
          console.log(response.data.message);
          // Optionally, refresh the list of playlists after deleting the playlist
          this.fetchPlaylists();
        })
        .catch((error) => {
          console.error("Error deleting playlist:", error);
        });
    },
  },
};
</script>

<style scoped>
/* Add your component-specific styles here */
</style>
