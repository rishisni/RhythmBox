<template>
  <div class="admin-summary">
    <h1 class="main-heading">Statistics</h1>
    <div v-if="loading" class="text-center">Loading...</div>
    <div v-else>
      <div v-if="error" class="alert alert-danger">{{ error }}</div>
      <div v-else>
        <div class="container">
          <div class="row">
            <div
              class="col-md-6 col-lg-4 mb-3"
              v-for="(item, index) in summaryItems"
              :key="index"
            >
              <div class="card bg-dark text-white album-card">
                <div class="card-body">
                  <h5 class="card-title">{{ item.title }}</h5>
                  <p class="card-text">{{ item.value }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- Song-wise Like and Report Counts Table -->
        <div class="card mt-4 album-card bg-dark">
          <div class="card-body bg-dark">
            <h5 class="card-title text-center text-white">
              Song-wise Like and Report Counts
            </h5>
            <table class="table bg-dark text-white album-card">
              <thead>
                <tr>
                  <th scope="col">Song Name</th>
                  <th scope="col">Like Count</th>
                  <th scope="col">Report Count</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(song, index) in songSummary" :key="index">
                  <td>{{ song.name }}</td>
                  <td>{{ song.likeCount }}</td>
                  <td>{{ song.reportCount }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div class="card mt-4 album-card bg-dark">
          <div class="card-body bg-dark">
            <h5 class="card-title text-center text-white">
              Song-wise Like and Report
            </h5>
            <AdminGraph :songSummary="songSummary"></AdminGraph>
          </div>
        </div>
        <div class="card mt-4 album-card bg-dark">
          <div class="card-body bg-dark">
            <h5 class="card-title text-center text-white">
              Overview
            </h5>
            <OverviewGraph
              :totalSongs="summary.total_songs"
              :totalLikes="summary.total_likes"
            ></OverviewGraph>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "@/axios-config";
import AdminGraph from "@/views/AdminGraph.vue";
import OverviewGraph from "@/views/OverviewGraph.vue"

export default {
  name: "AdminSummary",
  components: {
    AdminGraph,
    OverviewGraph
  },
  data() {
    return {
      loading: true,
      error: null,
      summary: null,
    };
  },
  computed: {
    summaryItems() {
      if (!this.summary) return [];
      return [
        { title: "Total Users:", value: this.summary.total_users },
        { title: "Total Creators:", value: this.summary.total_creators },
        { title: "Total Albums:", value: this.summary.total_albums },
        { title: "Total Songs:", value: this.summary.total_songs },
        { title: "Total Likes:", value: this.summary.total_likes },
        { title: "Total Reports:", value: this.summary.total_reports },
      ];
    },
    songSummary() {
      if (
        !this.summary ||
        !this.summary.song_like_counts ||
        !this.summary.song_report_counts
      )
        return [];
      const songSummary = [];
      for (const [songName, likeCount] of Object.entries(
        this.summary.song_like_counts
      )) {
        const reportCount = this.summary.song_report_counts[songName] || 0;
        songSummary.push({ name: songName, likeCount, reportCount });
      }
      return songSummary;
    },
  },
  methods: {
    fetchAdminSummary() {
      axios
        .get("/admin-summary", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        .then((response) => {
          this.summary = response.data;
          this.loading = false;
        })
        .catch((error) => {
          this.error = "Error fetching admin summary";
          console.error("Error fetching admin summary:", error);
          this.loading = false;
        });
    },
  },
  created() {
    this.fetchAdminSummary();
  },
};
</script>

<style>
.card-title {
  font-size: 1.2rem;
  font-weight: bold;
}
</style>
