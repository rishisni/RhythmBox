<template>
  <div id="app">
    <NavBar />

    <router-view />
    <FooterBar />
  </div>
</template>

<script>
import NavBar from "./components/Navbar.vue";
import FooterBar from "./components/Footer.vue";

export default {
  name: "App",
  components: {
    NavBar,
    FooterBar,
  },
};
</script>


