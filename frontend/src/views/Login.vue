<template>
  <section class="vh-100" >
    <div class="container h-100">
      <div class="row d-flex justify-content-center align-items-center h-100">
        <div class="col-lg-12 col-xl-11">
          <div class="card text-white bg-dark album-card" style="border-radius: 25px">
            <div class="card-body p-md-5">
              <div class="row justify-content-center">
                <div class="col-md-10 col-lg-6 col-xl-5 order-2 order-lg-1">
                  <div
                    v-if="errorMessage"
                    class="alert alert-danger"
                    role="alert"
                  >
                    {{ errorMessage }}
                  </div>
                  <div
                    v-if="successMessage"
                    class="alert alert-success"
                    role="alert"
                  >
                    {{ successMessage }}
                  </div>

                  <p class="text-center h1 fw-bold mb-5 mx-1 mx-md-4 mt-4">
                    Login
                  </p>
                  <form
                    @submit.prevent="loginUser"
                    class="mx-1 mx-md-4"
                    method="POST"
                  >
                    <div class="form-group d-flex mb-4 align-items-center">
                      <label for="usernameOrEmail" class="mr-3"
                        ><i class="fas fa-user"></i
                      ></label>
                      <input
                        type="text"
                        id="usernameOrEmail"
                        v-model="usernameOrEmail"
                        class="form-control form-control-plain"
                        placeholder="Username or Email"
                        required
                      />
                    </div>
                    <div class="form-group d-flex mb-4 align-items-center">
                      <label for="password" class="mr-3"
                        ><i class="fas fa-lock"></i
                      ></label>
                      <input
                        type="password"
                        id="password"
                        v-model="password"
                        class="form-control form-control-plain"
                        placeholder="Password"
                        required
                      />
                    </div>
                    <button type="submit" class="btn btn btn-outline-light d-block mx-auto custom-btn btn-lg">
                      Login
                    </button>
                  </form>
                </div>
                <div
                  class="col-md-10 col-lg-6 col-xl-7 d-flex align-items-center order-1 order-lg-2"
                >
                  <img
                    src="images/logo1.png"
                    class="img-fluid"
                    alt="Sample image"
                  />
                </div>
              </div>
              <div class="container mt-3">
                <div class="row justify-content-center">
                  <div class="col-md-10 col-lg-6 col-xl-5">
                    New user?
                    <router-link to="/register">Register here.</router-link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import axios from "@/axios-config";
export default {
  name: "UserLogin",
  data() {
    return {
      usernameOrEmail: "",
      password: "",
      errorMessage: "",
      successMessage: "",
    };
  },
  methods: {
    loginUser() {
      const userData = {
        usernameOrEmail: this.usernameOrEmail,
        password: this.password,
      };

      axios
        .post("/login", userData)
        .then((response) => {
          const { access_token, profile_url } = response.data;

          localStorage.setItem("access_token", access_token);

          this.successMessage = "Login successful";
          window.location.href = profile_url;

          this.errorMessage = "";
        })
        .catch((error) => {
          if (
            error.response &&
            error.response.data &&
            error.response.data.message
          ) {
            this.errorMessage = error.response.data.message;
          } else {
            this.errorMessage = "User login failed";
          }

          this.successMessage = "";
        });
    },
  },
};
</script>