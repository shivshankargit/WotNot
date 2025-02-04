<template>
  <div class="flex flex-col m-8 md:ml-72">
    <div class="flex flex-col md:flex-row justify-between mb-4 border-b pb-5">

      <div>
        <h2 class="text-xl md:text-2xl font-bold">Profile Settings</h2>
        <p>Change your business profile details</p>
      </div>

    </div>

    <h3>Changing the profile display picture is currently unavailable</h3>
    <div v-if="loading">Loading...</div>
    <div v-else class="w-full max-w-3xl space-y-6">
      <div class="grid grid-cols-2 gap-6">
        <div>
          <label for="about" class="block mb-2 font-bold">About</label>
          <input id="about" type="text" v-model="profile.about"
            class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-green-500" />
        </div>
        <div>
          <label for="businessAddress" class="block mb-2 font-bold">Business Address</label>
          <input id="businessAddress" type="text" v-model="profile.address"
            class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-green-500" />
        </div>
      </div>
      <div class="grid grid-cols-2 gap-6">
        <div>
          <label for="businessDescription" class="block mb-2 font-bold">Business Description</label>
          <textarea id="businessDescription" v-model="profile.description"
            class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-green-500 resize-none"></textarea>
        </div>
        <div>
          <label for="businessEmail" class="block mb-2 font-bold">Email for Business Contact</label>
          <input id="businessEmail" type="email" v-model="profile.email"
            class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-green-500" />
        </div>
      </div>
      <div class="grid grid-cols-2 gap-6">
        <div>
          <label for="businessIndustry" class="block mb-2 font-bold">Business Industry</label>
          <select id="businessIndustry" v-model="profile.vertical"
            class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-green-500">
            <option value="TECH">Tech</option>
            <option value="BEAUTY">Beauty</option>
            <option value="HEALTH">Health</option>
            <option value="EDU">Education</option>
            <option value="OTHER">Other</option>
          </select>
        </div>
        <div>
          <label for="websites" class="block mb-2 font-bold">Websites (comma-separated)</label>
          <input id="websites" type="text" v-model="profile.websites"
            class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-green-500" />
        </div>
      </div>
      <div class="flex justify-end space-x-4">
        <button type="button" @click="resetProfile"
          class="bg-gray-300 text-white rounded px-6 py-2 hover:bg-gray-400 transition">
          Reset
        </button>
        <button type="button" @click="updateProfile"
          class="bg-green-500 text-white rounded px-6 py-2 hover:bg-green-600 transition">
          Save
        </button>
      </div>
    </div>
    <div>
   
    <div class="flex flex-col md:flex-row justify-between mb-4 border-b pb-5">
    
          <div>
            <h2 class="text-xl md:text-2xl font-bold">Signup for API</h2>
            <p>Signup with facebook to get Whatsapp API</p>
          </div>
    
    </div>
    
      <!-- fb-signup -->
      <div>
        <div id="fb-root"></div>
        <button @click="launchWhatsAppSignup"
          style="background-color: #1877f2; border: 0; border-radius: 4px; color: #fff; cursor: pointer; font-family: Helvetica, Arial, sans-serif; font-size: 16px; font-weight: bold; height: 40px; padding: 0 24px;">
          Login with Facebook
        </button>
        <p>Session info response:</p>
                <pre>{{ sessionInfoResponse }}</pre>
                <br />
                <p>SDK response:</p>
                <pre>{{ sdkResponse }}</pre>
      </div>
    </div>
  </div>
</template>

<script>
/* global FB */
import axios from "axios";
import { useToast } from "vue-toastification";

export default {

  data() {
    return {
      profile: {
        about: "",
        address: "",
        email: "",
        description: "",
        websites: "",
        vertical: "OTHER",
        messaging_product: "whatsapp",
        profile_picture_url: "" // Default value
      },
      originalProfile: {}, // For reset functionality
      loading: true,

      // fb-signup
      sessionInfoResponse: "",
      sdkResponse: "",
    };
  },
  async mounted() {
    await this.fetchProfile();
    document.addEventListener('click', this.handleOutsideClick);


    const checkAndSend = () => {
      if (this.sessionInfoResponse && this.sdkResponse) {
        // Send data to the backend
        fetch("http://localhost:8000/subscribe_customer", {
          method: "POST",
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            sessionInfoResponse: this.sessionInfoResponse,
            sdkResponse: this.sdkResponse,
          }),
        })
          .then((response) => response.json())
          .then((data) => {
            console.log("Response from backend:", data);
          })
          .catch((error) => {
            console.error("Error sending data to backend:", error);
          });
      }
    };

    // Watch for changes in both variables
    this.$watch(
      () => [this.sessionInfoResponse, this.sdkResponse],
      (newValues) => {
        const [newSessionInfoResponse, newSdkResponse] = newValues;
        if (newSessionInfoResponse && newSdkResponse) {
          checkAndSend();
        }
      },
      { immediate: true, deep: true }
    );


    // Initialize the Facebook SDK
    window.fbAsyncInit = () => {
      FB.init({
        appId: "2621821927998797", // Replace with your App ID
        autoLogAppEvents: true,
        xfbml: true,
        version: "v21.0",
      });
    };

    // Dynamically load the Facebook SDK
    const script = document.createElement("script");
    script.src = "https://connect.facebook.net/en_US/sdk.js";
    script.async = true;
    script.defer = true;
    script.crossOrigin = "anonymous";
    document.body.appendChild(script);

    // Set up an event listener for messages from Facebook
    window.addEventListener("message", (event) => {
      if (
        event.origin !== "https://www.facebook.com" &&
        event.origin !== "https://web.facebook.com"
      ) {
        return;
      }

      try {
        const data = JSON.parse(event.data);
        if (data.type === "WA_EMBEDDED_SIGNUP") {
          if (data.event === "FINISH") {
            const { phone_number_id, waba_id } = data.data;
            console.log(
              "Phone number ID:",
              phone_number_id,
              "WhatsApp business account ID:",
              waba_id
            );
          } else if (data.event === "CANCEL") {
            const { current_step } = data.data;
            console.warn("Cancelled at step:", current_step);
          } else if (data.event === "ERROR") {
            const { error_message } = data.data;
            console.error("Error:", error_message);
          }
        }
        this.sessionInfoResponse = JSON.stringify(data, null, 2);

      } catch {
        console.log("Non-JSON Response:", event.data);
      }
    });
  },

  methods: {
    fbLoginCallback(response) {
      if (response.authResponse) {
        const code = response.authResponse.code;
        console.log("Auth Response Code:", code);
        // Handle the code by sending it to your backend server for further processing.
      }
      this.sdkResponse = JSON.stringify(response, null, 2);
    },

    launchWhatsAppSignup() {
      FB.login(
        this.fbLoginCallback,
        {
          config_id: "951833230236631", // Replace with your configuration ID
          response_type: "code", // Must be 'code' for System User access token
          override_default_response_type: true,
          extras: {
            setup: {},
            featureType: "only_waba_sharing",
            sessionInfoVersion: "2",
          },
        }
      );
    },

    loadFacebookSDK() {
      if (!document.getElementById('facebook-jssdk')) {
        const script = document.createElement('script');
        script.id = 'facebook-jssdk';
        script.src = "https://connect.facebook.net/en_US/sdk.js";
        script.async = true;
        script.defer = true;
        script.onload = this.initializeFacebookSDK; // Ensure SDK is initialized once loaded
        document.body.appendChild(script);
      } else {
        this.initializeFacebookSDK(); // SDK is already loaded
      }
    },

    initializeFacebookSDK() {
      window.fbAsyncInit = () => {
        FB.init({
          appId: '2621821927998797',  // Replace with your actual Facebook app ID
          cookie: true,
          xfbml: true,
          version: 'v20.0',
        });
        this.renderFacebookButton();
      };
    },
    async fetchProfile() {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.get("http://localhost:8000/get-business-profile", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.status >= 200 && response.status < 300 && response.data.data.length) {
          const data = response.data.data[0]; // Access the first object in the "data" array
          this.profile = {
            about: data.about || "",
            address: data.address || "",
            email: data.email || "",
            websites: (data.websites && data.websites.join(", ")) || "",
            vertical: data.vertical || "OTHER",
            messaging_product: data.messaging_product || "whatsapp",
            description: data.description || "",
            profile_picture_url: data.profile_picture_url || "",
          };
          this.originalProfile = { ...this.profile }; // Save original profile for reset
        }
      } catch (error) {
        console.error("Error fetching profile:", error.response?.data?.detail || error.message);
      } finally {
        this.loading = false;
      }
    },
    async updateProfile() {
      const toast = useToast();
      try {
        const token = localStorage.getItem("token");
        const payload = {
          ...this.profile,
          websites: this.profile.websites.split(",").map((site) => site.trim()), // Convert to array
        };

        const response = await axios.post("http://localhost:8000/update-profile", payload, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.status >= 200 && response.status < 300) {
          toast.success("Profile updated successfully!");
          this.originalProfile = { ...this.profile }; // Update originalProfile after successful save
        }
      } catch (error) {
        toast.error("Failed to update profile!");
        console.error("Error updating profile:", error.response?.data?.detail || error.message);
      }
    },
    resetProfile() {
      this.profile = { ...this.originalProfile }; // Reset to original data
    },
  },
};
</script>

<style scoped>
/* Add your custom styles here */
</style>
