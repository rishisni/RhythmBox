<template>
  <div>
    <div class="container justify-content-center">
      <h1 class="main-heading">Search Results</h1>
      <!-- If user is not authenticated, display message and login button -->
      <div v-if="!authenticated">
        <p class="text-white">Please login to view search results.</p>
        <router-link to="/login" class="btn btn-outline-light custom-btn">Login</router-link>
      </div>
      <div v-else>
        <div v-if="loading">Loading...</div>
        <div class="text-white text-center" v-else-if="searchResults.length === 0">No results found.</div>
        <div v-else>
          <div class="row justify-content-center">
            <div class="col-md-4 mb-4" v-for="result in searchResults" :key="result.id">
              <div class="card bg-dark text-white album-card">
                <div class="card-body">
                  <h5 class="card-title">{{ result.name }}</h5>
                  <p class="card-text">Artist: {{ result.artist_name }}</p>
                  <p class="card-text">Album: {{ result.album_name }}</p>
                  <router-link :to="'/all-songs'" class="btn" style="background-color: #8a2be2;">
                    <i class="fas fa-music"></i> 
                  </router-link>
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
import axios from '@/axios-config';

export default {
  name: 'SearchResults',
  data() {
    return {
      loading: true,
      searchResults: [],
    };
  },
  computed: {
    authenticated() {
      return !!localStorage.getItem('access_token');
    },
  },
  mounted() {
    if (this.authenticated) {
      this.fetchSearchResults();
    } else {
      this.loading = false;
    }
  },
  methods: {
    fetchSearchResults() {
      const searchQuery = this.$route.query.q;
      if (searchQuery) {
        axios.get(`/search?query=${searchQuery}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          },
        })
          .then(response => {
            this.searchResults = response.data.songs;
          })
          .catch(error => {
            console.error('Error fetching search results:', error);
          })
          .finally(() => {
            this.loading = false;
          });
      } else {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
/* Add custom styles here if needed */
</style>
