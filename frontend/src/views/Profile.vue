<template>
  <div>
    
    <div v-if="authenticated">
      <h1>Profile</h1>
      <div v-if="user">
        <p><strong>Username:</strong> {{ user.username }}</p>
        <p><strong>Email:</strong> {{ user.email }}</p>
      </div>
      <div v-else>
        <p>Loading...</p>
      </div>
    </div>
    <div v-else>
      <p>Please log in to access this page.</p>
      <router-link to="/login" class="text-center">
                      Login 
                    </router-link>
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



