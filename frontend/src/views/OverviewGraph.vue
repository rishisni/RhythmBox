<template>
  <div class="overview-graph">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script>
import axios from '@/axios-config';
import Chart from 'chart.js/auto';

export default {
  data() {
    return {
      summary: null
    };
  },
  mounted() {
    this.fetchAdminSummary();
  },
  methods: {
    fetchAdminSummary() {
      axios.get('/admin-summary'
      , {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
        .then(response => {
          this.summary = response.data;
          this.renderGraph();
        })
        .catch(error => {
          console.error('Error fetching admin summary:', error);
          // Handle error, such as displaying a message to the user
        });
    },
    renderGraph() {
      if (!this.summary) return;

      const ctx = this.$refs.chartCanvas.getContext('2d');
      
      // Extract data from summary
      const { total_users, total_creators, total_albums, total_songs, total_likes, total_reports } = this.summary;
      
      // Render chart using Chart.js
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: ['Total Users', 'Total Creators', 'Total Albums', 'Total Songs', 'Total Likes', 'Total Reports'],
          datasets: [{
            label: 'Summary',
            data: [total_users, total_creators, total_albums, total_songs, total_likes, total_reports],
            backgroundColor: [
              'rgba(255, 99, 132, 0.2)',
              'rgba(54, 162, 235, 0.2)',
              'rgba(255, 206, 86, 0.2)',
              'rgba(75, 192, 192, 0.2)',
              'rgba(153, 102, 255, 0.2)',
              'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
              'rgba(255, 99, 132, 1)',
              'rgba(54, 162, 235, 1)',
              'rgba(255, 206, 86, 1)',
              'rgba(75, 192, 192, 1)',
              'rgba(153, 102, 255, 1)',
              'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });
    }
  }
};
</script>

<style scoped>
.admin-summary-graph {
  margin-top: 20px;
}
</style>

