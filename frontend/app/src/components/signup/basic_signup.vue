<template>
  <div class="bg-container">
    <div class="max-w-md w-full bg-white p-6 rounded-lg shadow-lg">
      <h2 class="text-2xl sm:text-3xl font-semibold text-center text-gray-800 mb-4">Get started with Wotnot</h2>

      <hr class="my-3 border-gray-300" />

      <div class="space-y-4">
        <div class="w-full">
          <label for="username" class="block text-sm font-medium text-gray-700">Business Name</label>
          <input type="text" id="username" placeholder="Your Business Name"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            required />
        </div>

        <div class="w-full">
          <label for="email" class="block text-sm font-medium text-gray-700">Business Email Address</label>
          <input type="email" id="email" placeholder="Your Business Email Address"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            required />
        </div>

        <div class="w-full">
          <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
          <input type="password" id="password" placeholder="Set Password"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            required />
        </div>
      </div>

      <div class="mt-4 text-sm text-center">
        <p class="mb-2 text-sm">
          By signing up you agree to the
          <a href="#" class="text-[#075e54] font-semibold">Terms</a> and
          <a href="#" class="text-[#075e54] font-semibold">Privacy Policy</a>
        </p>
      </div>

      <button
        class="w-full bg-[#075e54] text-white py-2 rounded-md hover:bg-[#2d988c] focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
        @click.prevent="handleSubmit">
        Get Account
      </button>

      <p class="mt-4 text-center text-sm">
        Already have an account?
        <a href="" class="text-[#075e54] font-semibold mb-4" @click="redirectLogin">Login</a>
      </p>
    </div>
  </div>
</template>



<script>


export default {
  data() {
    return {
      apiUrl: process.env.VUE_APP_API_URL,
    };
  },
  name: 'BasicSignUpForm',
  methods: {

    handleSubmit() {
      // Get the form data
      const formData = {
        username: document.getElementById('username').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value,
      };

      // Check for required fields
      if (!formData.username || !formData.email || !formData.password ) {
        alert('Please fill in all required fields.');
        return;
      }

      // Send a request to your FastAPI endpoint
      fetch(`${this.apiUrl}/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            // console.log(response)
            alert('Account created successfully!');
            // Clear the form fields
            document.querySelectorAll('input').forEach(input => input.value = '');
          } else if (data.detail) {
            alert(data.detail); // Show the error message from the API
          } else {

            alert('Failed to create account. Please try again.');
          }
        })
        .catch(error => console.error(error));
    },
    redirectLogin() {

      this.$router.push('/');
    },


  },
};
</script>


<style scoped>
.bg-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  /* equivalent to min-h-screen */

  background-image: url("@/assets/LoginPage.png");
  background-position: center;
  /* equivalent to bg-gray-100 */
  padding: 0 16px;
  /* equivalent to px-4 */
}

/* Responsive padding for different screen sizes */
@media (min-width: 640px) {

  /* equivalent to sm:px-6 */
  .container {
    padding: 0 24px;
  }
}

@media (min-width: 1024px) {

  /* equivalent to lg:px-8 */
  .container {
    padding: 0 32px;
  }
}
</style>