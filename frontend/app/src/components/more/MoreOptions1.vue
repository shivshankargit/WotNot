<template>
  <div class="content-section">

    <h2>Integration</h2>
    <p>Your content for Integration goes here.</p>

    <div class="woocommerceBox">
      <img src="@/assets/woocommerce.png" alt="" @click="showPopup = true">
    </div>

    <PopUp v-if="showPopup" @close="showPopup = false">



      <v-form>
        <h3>Woocommerce</h3>
        <div>
          <label for="">Select action</label>
          <select v-model="SelectedAction" required>
            <option value="" disabled>Select your option</option>
            <option value="Confirmation">Send Order Confirmation</option>
            <option value="">Abondoned Cart</option>
          </select></div>
        
        <div  v-if="SelectedAction === 'Confirmation'">
          <label for="selectTemplate">select template</label>
          <select v-model="selectedTemplate" >
            <option value="">option</option>
            <option v-for="template in templates" :key="template.id" :value="template.id">{{ template.name }}</option>
          </select></div>
        

        

        <div class="webhookConfig" v-if="selectedTemplate !== null">
          <h3>Woocommerce Setup</h3>
          <input type="text" v-model="webhookLink" disabled>
          
          <ul>
            <li>Navigate to <b>WooCommerce > Settings</b></li>
            <li>Click on the <b>Advanced tab</b></li>
            <li>In the <b>Advanced settings</b>, click on <b>Webhook</b></li>
            <li>Click the <b>Add Webhook</b> button.</li>
            <li><b>Configure Webhook Settings</b></li>
            <li><b>Name</b>: Give your webhook a name to identify it.</li>
            <li><b>Status:</b> Set this to Active.</li>
            <li>Topic: Choose the event you want the webhook to listen to</li>
            <li><b>Delivery URL:use the above given webhook URL</b></li>
            <li><b>Secret:</b> leave blank</li>
            <li><b>API Version:</b> Leave the default version</li>
            <li>Click Save Webhook to activate the integration</li>
          </ul>
        </div>
      



      </v-form>


    </PopUp>

  </div>
</template>

<script>
import PopUp from "../popups/popup"

export default {

  name: 'MoreOptions1',
  data() {

    return {
      showPopup: false,
      SelectedAction: null,
      templates: [],
      selectedTemplate: null,
      webhookLink: '',

    }

  },
  components: {
    PopUp
  },
  async mounted() {
    await this.fetchTemplates()
    await this.fetchapiKey();


    // Fetch contacts when the component is mounted
  },
  methods: {
    togglepopup() {
      console.log("event")
    },
    async fetchTemplates() {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch('http://localhost:8000/templates/', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const templateNames = await response.json();
        this.templates = templateNames.map(name => ({ id: name, name }));
      } catch (error) {
        console.error('Error fetching templates:', error);
      }
    },

    async fetchapiKey() {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch("http://localhost:8000/webhooklink",
          {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
            }
          });


          if(!response.ok){
            throw new Error('Network response was not ok'); 
          }

          const result= await response.json()
          this.webhookLink=result.webkook_link
      } catch (error) {
        console.error('Error fetching API key:', error);
      }

    }
  }
}
</script>

<style scoped>
/* Add your styles here */
.woocommerceBox {
  padding: 10px;
  border-radius: 10px;
  border: solid;
  width: fit-content;
}

.webhookConfig ul li {
  margin-bottom: 5px;
}
</style>