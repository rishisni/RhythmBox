<template>
  <div class="container mt-4">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="text-center mb-4">
          <img src="/images/logo1.png" alt="Logo" class="logo-image" />
        </div>

        <div class="lyrics mt-4">
          <pre class="p-3 bg-dark text-white text-align-center">{{ lyrics }}</pre>
        </div>

        <div class="text-center mt-3">
          <button @click="downloadLyrics" class="btn btn btn-outline-light d-block mx-auto custom-btn">
            Download Lyrics
          </button>
        </div>
      </div>
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
.logo-image {
  width: 100px;
}

.lyrics {
  /* background-color: ; */
  border: 1px solid #8a2be2;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}


</style>
