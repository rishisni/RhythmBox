<template>
  <div class="container mt-4">
    <div class="logo">
      <img src="/images/logo1.png" alt="Logo" class="logo-image" />
    </div>

    <div class="lyrics mt-4 text-center">
      <pre>{{ lyrics }}</pre>
    </div>

    <div class="text-center mt-3">
      <button @click="downloadLyrics" class="btn btn-primary">
        Download Lyrics
      </button>
    </div>
  </div>
</template>

<script>
import { saveAs } from "file-saver";

export default {
  name: "LyricsPage",
  data() {
    return {
      lyrics: "",
    };
  },
  mounted() {
    this.lyrics = this.$route.params.lyrics;
  },
  methods: {
    downloadLyrics() {
      const blob = new Blob([this.lyrics], {
        type: "text/plain;charset=utf-8",
      });
      saveAs(blob, "lyrics.txt");
    },
  },
};
</script>

<style scoped>
.logo {
  position: absolute;

  left: 20px;
}

.logo-image {
  width: 100px;
}


.lyrics {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 5px;
  border: 1px solid #8a2be2;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}


.btn-primary {
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 3px;
  padding: 8px 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-primary:hover {
  background-color: #0056b3;
}
</style>
