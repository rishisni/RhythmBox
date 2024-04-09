<template>
  <div>
    <h1>Profile</h1>
    <div v-if="user">
      <p><strong>Username:</strong> {{ user.username }}</p>
      <p><strong>Email:</strong> {{ user.email }}</p>
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>
  </div>
</template>

<script>
import axios from '@/axios-config';

export default {
  name: 'UserProfile',
  data() {
    return {
      user: null
    };
  },
  mounted() {
    this.fetchUserProfile();
  },
  methods: {
    fetchUserProfile() {
      axios.get('/profile')
        .then(response => {
          this.user = response.data;
        })
        .catch(error => {
          console.error('Error fetching user profile:', error);
        });
    }
  }
};
</script>
