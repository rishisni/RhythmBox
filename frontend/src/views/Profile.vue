<template>
  <div class="container">
    <div class="row">
      <!-- Left Sidebar -->
      <div class="col-md-3">
        <div class="profile-sidebar" v-if="authenticated">
          <div class="profile-userpic">
            <img
              src="images/background.jpg"
              alt="Profile"
              class="profile-img img-fluid rounded-circle"
            />
          </div>
          <div class="profile-usertitle">
            <div class="profile-usertitle-name">
              {{ user && user.username }}
            </div>
            <div class="profile-usertitle-email">{{ user && user.email }}</div>
          </div>
          <div class="profile-usermenu">
            <!-- List of menu items -->
            <ul class="nav flex-column">
              <li class="nav-item">
                <router-link to="/profile" class="nav-link">
                  Profile
                </router-link>
              </li>
            </ul>
          </div>
        </div>
        <div v-else>
          <p>Please log in to access this page.</p>
          <router-link to="/login" class="btn btn-primary">Login</router-link>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import axios from "@/axios-config";

export default {
  name: "UserProfile",
  data() {
    return {
      user: null,
      authenticated: false,
    };
  },
  mounted() {
    this.checkAuthentication();
  },
  methods: {
    checkAuthentication() {
      this.authenticated = localStorage.getItem("access_token") !== null;
      if (this.authenticated) {
        this.fetchUserProfile();
      }
    },
    fetchUserProfile() {
      axios
        .get("/profile", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        .then((response) => {
          this.user = response.data;
        })
        .catch((error) => {
          console.error("Error fetching user profile:", error);
        });
    },
  },
};
</script>

<style scoped>
.card {
  margin-top: 50px;
}

.profile-img {
  width: 250px;
  height: 250px;
  object-fit: cover;
  border: 5px solid #8a2be2;
}
</style>



