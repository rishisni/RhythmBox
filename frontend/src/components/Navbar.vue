<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
      
      <a class="navbar-brand" href="#">
        <img src="images/logo1.png" alt="Logo" height="30">
      </a>

      
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <router-link to="/" class="nav-link" >
              <i class="fas fa-home"></i> Home
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/register"><i class="fas fa-user"></i>User</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/admin-login"><i class="fas fa-user-shield"></i>Admin</router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>

export default {
    name :"NavBar"
  
};
</script>

<style scoped>
/* Add custom styles here if needed */
</style>
