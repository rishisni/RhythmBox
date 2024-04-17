<template>
  <div v-if="userRole.is_admin || userRole.is_creator" class="container mt-4">
    <div class="container-fluid text-white py-4 d-flex justify-content-center align-items-center">
      <div class="col-md-6 col-lg-6 col-xl-5">
        <div class="container mt-4 border rounded p-4">
          <h1 class="main-heading">Add Song</h1>
          <form @submit.prevent="addSong">
            <div class="mb-3">
              <label for="name" class="form-label">Song Name</label>
              <input
                type="text"
                class="form-control form-control-plain"
                id="name"
                v-model="song.name"
                required
              />
            </div>
            <div class="mb-3">
              <label for="lyrics" class="form-label">Lyrics</label>
              <textarea
                class="form-control form-control-plain"
                id="lyrics"
                v-model="song.lyrics"
                rows="5"
                required
              ></textarea>
            </div>
            <div class="mb-3">
              <label for="genre" class="form-label">Genre</label>
              <input
                type="text"
                class="form-control form-control-plain"
                id="genre"
                v-model="song.genre"
                required
              />
            </div>
            <div class="mb-3">
              <label for="duration" class="form-label"
                >Duration (in seconds)</label
              >
              <input
                type="number"
                class="form-control form-control-plain"
                id="duration"
                v-model.number="song.duration"
                required
              />
            </div>
            <div class="mb-3">
              <label for="songFile" class="form-label">Song File</label>
              <input
                type="file"
                class="form-control form-control-plain"
                id="songFile"
                ref="songFile"
                @change="onFileChange"
                required
              />
            </div>
            <div class="d-grid gap-2">
              <button type="submit" class="btn btn btn-outline-light d-block mx-auto custom-btn" >Add Song</button>
            </div>
          </form>
          <p v-if="successMessage" class="text-success mt-3">{{ successMessage }}</p>
          <p v-if="errorMessage" class="text-danger mt-3">{{ errorMessage }}</p>
        </div>
      </div>
    </div>
  </div>
  <div v-else>
    <p class="text-white text-center mt-4">You are not authorized to access this page.</p>
  </div>
</template>

<script>
import axios from "@/axios-config";

export default {
  name: "AddSong",

  data() {
    return {
      song: {
        name: "",
        lyrics: "",
        genre: "",
        duration: 0,
        filePath: null,
      },
      userRole: {
        is_admin: false,
        is_creator: false
      },
      successMessage: '',
      errorMessage: ''
    };
  },
  created() {
    this.getUserRole();
  },
  methods: {
    getUserRole() {
      axios
        .get("/user-role", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        .then((response) => {
          this.userRole = response.data;
        })
        .catch((error) => {
          console.error("Error fetching user role:", error);
        });
    },
    addSong() {
      let formData = new FormData();
      formData.append("name", this.song.name);
      formData.append("lyrics", this.song.lyrics);
      formData.append("genre", this.song.genre);
      formData.append("duration", this.song.duration);
      formData.append("song_file", this.song.filePath);

      axios
        .post(`/albums/${this.$route.params.albumId}/add-song`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        .then(() => {
          this.successMessage = 'Song added successfully!';
          setTimeout(() => {
            this.successMessage = '';
          }, 3000);
          this.song = {
            albumId: "",
            name: "",
            lyrics: "",
            genre: "",
            duration: 0,
            filePath: null,
          };
          this.$router.push(`/albums/${this.$route.params.albumId}/songs`);
        })
        .catch((error) => {
          this.errorMessage = 'Failed to add song. Please try again.';
          console.error("Error adding song:", error);
          setTimeout(() => {
            this.errorMessage = '';
          }, 3000);
        });
    },
    onFileChange() {
      this.song.filePath = this.$refs.songFile.files[0];
    },
  },
};
</script>
