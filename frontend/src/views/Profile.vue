<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      
      <div class="col-md-6">
        <div class="profile-sidebar bg-dark text-white p-4 album-card" v-if="authenticated">
          <div class="profile-userpic text-center">
            <img
              src="images/background.jpg"
              alt="Profile"
              class="profile-img img-fluid rounded-circle"
            />
          </div>
          <div class="profile-usertitle text-center mt-3">
            <div class="profile-usertitle-name">
              {{ user && user.username }}
            </div>
            <div class="profile-usertitle-email">{{ user && user.email }}</div>
          </div>
          
        </div>
        <div v-else class="text-center">
          <p>Please log in to access this page.</p>
          <router-link to="/login" class="btn btn btn-outline-light d-block mx-auto custom-btn btn-lg">Login</router-link>
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
/* .profile-sidebar {
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
} */

.profile-img {
  width: 200px;
  height: 200px;
  object-fit: cover;
  border: 5px solid #8a2be2;
}

.profile-usertitle-name {
  font-size: 1.5rem;
  font-weight: bold;
}

.profile-usertitle-email {
  margin-top: 5px;
}



.btn-primary {
  background-color: #8a2be2;
  border: none;
}

.btn-primary:hover {
  background-color: #6b1d9e;
}
</style>