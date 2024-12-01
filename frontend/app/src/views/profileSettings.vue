<template>
  <div class="flex flex-col items-center p-6">
    <div class="text-center mb-8">
      Changing the profile display picture is currently unavailable
    </div>
    <div v-if="loading">Loading...</div>
    <div v-else class="w-full max-w-3xl space-y-6">
      <div class="grid grid-cols-2 gap-6">
        <div>
          <label for="about" class="block mb-2 font-bold">About</label>
          <input
            id="about"
            type="text"
            v-model="profile.about"
            class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-green-500"
          />
        </div>
        <div>
          <label for="businessAddress" class="block mb-2 font-bold">Business Address</label>
          <input
            id="businessAddress"
            type="text"
            v-model="profile.address"
            class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-green-500"
          />
        </div>
      </div>
      <div class="grid grid-cols-2 gap-6">
        <div>
          <label for="businessDescription" class="block mb-2 font-bold">Business Description</label>
          <textarea
            id="businessDescription"
            v-model="profile.description"
            class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-green-500 resize-none"
          ></textarea>
        </div>
        <div>
          <label for="businessEmail" class="block mb-2 font-bold">Email for Business Contact</label>
          <input
            id="businessEmail"
            type="email"
            v-model="profile.email"
            class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-green-500"
          />
        </div>
      </div>
      <div class="grid grid-cols-2 gap-6">
        <div>
          <label for="businessIndustry" class="block mb-2 font-bold">Business Industry</label>
          <select
            id="businessIndustry"
            v-model="profile.vertical"
            class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-green-500"
          >
            <option value="TECH">Tech</option>
            <option value="BEAUTY">Beauty</option>
            <option value="HEALTH">Health</option>
            <option value="EDU">Education</option>
            <option value="OTHER">Other</option>
          </select>
        </div>
        <div>
          <label for="websites" class="block mb-2 font-bold">Websites (comma-separated)</label>
          <input
            id="websites"
            type="text"
            v-model="profile.websites"
            class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-green-500"
          />
        </div>
      </div>
      <div class="flex justify-end space-x-4">
        <button
          type="button"
          @click="resetProfile"
          class="bg-gray-300 text-white rounded px-6 py-2 hover:bg-gray-400 transition"
        >
          Reset
        </button>
        <button
          type="button"
          @click="updateProfile"
          class="bg-green-500 text-white rounded px-6 py-2 hover:bg-green-600 transition"
        >
          Save
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useToast } from "vue-toastification";

export default {
  data() {
    return {
      profile: {
        about: "",
        address: "",
        email: "",
        description:"",
        websites: "",
        vertical: "OTHER",
        messaging_product: "whatsapp",
        profile_picture_url: "" // Default value
      },
      originalProfile: {}, // For reset functionality
      loading: true,
    };
  },
  async mounted() {
    await this.fetchProfile();
  },
  methods: {
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
