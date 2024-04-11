<template>
  <footer class="footer bg-dark text-white py-4  ">
    <div class="container">
      <div class="row">
        <div class="col-md-6">
          <h5><i class="fab fa-instagram"></i> Instagram</h5>
          <ul class="list-unstyled">
            <li><a href="https://www.instagram.com/example" target="_blank"><i class="fab fa-instagram"></i> Instagram</a></li>
            <li><a href="mailto:example@gmail.com"><i class="far fa-envelope"></i> Gmail</a></li>
            <li><a href="https://github.com/example" target="_blank"><i class="fab fa-github"></i> GitHub</a></li>
            <!-- Add more social handles here -->
          </ul>
        </div>
        <div class="col-md-6">
          <h5>About the App</h5>
          <p>This is a music streaming web application built with Vue.js and Bootstrap.</p>
          <!-- Add more information about the app here -->
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'FooterBar'
}
</script>

<style scoped>
/* Add custom styles for the footer here */
.footer {
    margin-top: 300px;
  background-color: #8a2be2;
  color: white;
}

.footer h5 {
  color: #ffffff;
}

.footer ul {
  padding-left: 0;
}

.footer ul li {
  list-style-type: none;
}

.footer a {
  color: #ffffff;
  text-decoration: none;
}

.footer a:hover {
  text-decoration: underline;
}
</style>



