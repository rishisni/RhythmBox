<template>
  <div class="admin-graph">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';

export default {
  props: {
    songSummary: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      chart: null
    };
  },
  mounted() {
    this.renderChart();
  },
  methods: {
    renderChart() {
      if (!this.songSummary.length) return;

      const labels = this.songSummary.map(song => song.name);
      const likeCounts = this.songSummary.map(song => song.likeCount);
      const reportCounts = this.songSummary.map(song => song.reportCount);
      

      const ctx = this.$refs.chartCanvas.getContext('2d');

      this.chart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: 'Like Count',
            data: likeCounts,
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
          }, {
            label: 'Report Count',
            data: reportCounts,
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
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
  },
  watch: {
    songSummary() {
      if (this.chart) {
        this.chart.destroy();
      }
      this.renderChart();
    },
    immediate: true
  }
};
</script>

<style scoped>
.admin-graph {
  margin-top: 20px;
}
</style>
