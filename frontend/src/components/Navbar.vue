<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
      <a class="navbar-brand" href="#">
        <img src="images/logo1.png" alt="Logo" height="30" />
      </a>

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item" v-if="!authenticated">
            <router-link to="/" class="nav-link">
              <i class="fas fa-home"></i> Home
            </router-link>
          </li>
          <li class="nav-item" v-if="!authenticated">
            <router-link to="/register" class="nav-link">
              <i class="fas fa-user"></i> User
            </router-link>
          </li>
          <li class="nav-item" v-if="!authenticated">
            <router-link to="/admin-login" class="nav-link">
              <i class="fas fa-user-shield"></i> Admin
            </router-link>
          </li>

          <li class="nav-item" v-if="authenticated">
            <router-link to="/" class="nav-link">
              <i class="fas fa-home"></i> Home
            </router-link>
          </li>
          <li class="nav-item" v-if="authenticated">
            <router-link to="/profile" class="nav-link">
              <i class="fas fa-user"></i> Profile
            </router-link>
          </li>
          <li class="nav-item" v-if=" authenticated &&(userRole === 'is_creator' || userRole === 'is_admin') " >
            <router-link to="/add-album" class="nav-link">
              <i class="fas fa-plus"></i> Add Album
            </router-link>
          </li>
           <li class="nav-item" v-if=" authenticated &&(userRole === 'is_creator' || userRole === 'is_admin') " >
            <router-link to="/albums" class="nav-link">
              <i class="fas fa-eye"></i> My Albums
            </router-link>
          </li>
          <li class="nav-item" v-if="authenticated">
            <router-link to="/albums/all" class="nav-link">
             <i class="fas fa-solid fa-record-vinyl"></i> Albums
            </router-link>
          </li>
          <li class="nav-item" v-if="authenticated">
            <router-link to="/songs" class="nav-link">
              <i class="fas fa-music"></i> Songs
            </router-link>
          </li>
          <li class="nav-item" v-if="authenticated && userRole !== 'is_admin'">
            <router-link to="/my-playlist" class="nav-link">
              <i class="fas fa-list"></i> My Playlist
            </router-link>
          </li>

          <li class="nav-item" v-if="authenticated">
            <button class="btn btn-danger" @click="logout">Logout</button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>


<script>
import axios from "@/axios-config";
export default {
  name: "NavBar",
  data() {
    return {
      authenticated: false, // Set to true when user is authenticated
      userRole: "", // Set user role here (user, creator, admin)
    };
  },
  mounted() {
    // Fetch user role after authentication
    this.getUserRole();
  },
  methods: {
    logout() {
      axios
        .post("/logout", null, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        .then(() => {
          localStorage.removeItem("access_token");
          this.successMessage = "Logout successful!";
          this.$router.push("/");
          setTimeout(() => {
            window.location.reload(); // Refresh the page after a delay
          }, 100);
        })
        .catch((error) => {
          console.error("Logout failed:", error);
        });
    },

    getUserRole() {
      // Make an API request to fetch the user's role from the backend
      axios
        .get("/user-role", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        .then((response) => {
          // Update the userRole data property based on the response from the backend
          this.userRole = response.data.is_admin ? 'is_admin' : (response.data.is_creator ? 'is_creator' : 'user');
          this.authenticated = true; // Set authenticated to true
        })
        .catch((error) => {
          console.error("Error fetching user role:", error);
          // Handle error fetching user role, if needed
        });
    },
  },
};
</script>

<style scoped>
/* Add custom styles here if needed */
</style>
