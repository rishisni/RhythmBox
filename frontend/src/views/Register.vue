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
                    v-if="successMessage"
                    class="alert"
                    :class="
                      successMessage.includes('successful')
                        ? 'alert-success'
                        : 'alert-danger'
                    "
                    role="alert"
                  >
                    {{ successMessage }}
                  </div>

                  <p class="text-center h1 fw-bold mb-5 mx-1 mx-md-4 mt-4">
                    Sign up
                  </p>
                  <form @submit.prevent="registerUser" class="mx-1 mx-md-4">
                    <div class="form-group d-flex mb-4 align-items-center">
                      <label for="username" class="mr-3"
                        ><i class="fas fa-user"></i
                      ></label>
                      <input
                        type="text"
                        id="username"
                        v-model="username"
                        class="form-control form-control-plain"
                        placeholder="Username"
                        required
                      />
                    </div>
                    <div class="form-group d-flex mb-4 align-items-center">
                      <label for="email" class="mr-3"
                        ><i class="fas fa-envelope"></i
                      ></label>
                      <input
                        type="email"
                        id="email"
                        v-model="email"
                        class=" form-control form-control-plain"
                        placeholder="Email"
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
                    <div class="form-group d-flex mb-4 align-items-center">
                      <label for="isCreator" class="mr-3"
                        ><i class="fas fa-check-square"></i
                      ></label>
                      <input
                        type="checkbox"
                        id="isCreator"
                        v-model="isCreator"
                        class="form-check-input"
                        :value="true"
                      />
                      <label for="isCreator" class="form-check-label"
                        >Register as Creator</label
                      >
                    </div>
                    <button type="submit" class="btn btn btn-outline-light d-block mx-auto custom-btn btn-lg">
                      Register
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
                    Already registered?
                    <router-link to="/login" class="text-center">
                      Login here.
                    </router-link>
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
  name: "UserRegister",
  data() {
    return {
      username: "",
      email: "",
      password: "",
      isCreator: false,
      successMessage: "",
    };
  },
  methods: {
    registerUser() {
      const userData = {
        username: this.username,
        email: this.email,
        password: this.password,
        is_creator: this.isCreator,
      };

      axios
        .post("/register", userData)
        .then((response) => {
          this.successMessage = response.data.message;
        })
        .catch((error) => {
          if (error.response) {
            console.error("Server Error:", error.response.data);
            this.successMessage =
              "Registration failed: " + error.response.data.message;
          } else if (error.request) {
            console.error("No Response:", error.request);
            this.successMessage =
              "Registration failed: No response from the server";
          } else {
            console.error("Request Error:", error.message);
            this.successMessage = "Registration failed: Request error";
          }
        });
    },
  },
};
</script>
