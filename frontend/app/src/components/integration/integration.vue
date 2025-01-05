<template>
  <div class="content-section m-8 md:ml-72">

    <div class="flex flex-col md:flex-row justify-between mb-4 border-b pb-5">
      <div>
        <h2 class="text-2xl font-bold ">Integration</h2>
        <p>Integrate other application with WotNot</p>
      </div>

    </div>



    <div class="woocommerceBox cursor-pointer p-4  hover:bg-gray-300 rounded-lg mb-4">
      <img src="@/assets/woocommerce.png" alt="Woocommerce" @click="showPopup = true">
    </div>

    <PopUp v-if="showPopup" @close="showPopup = false"
      class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 custom-scrollbar">

      <div class="popup-content custom-scrollbar p-4">
        <form class="space-y-4" @submit.prevent="submitIntegrationForm(this.SelectedAction)">
          <h2 class="text-xl font-bold ">Woocommerce</h2>
          <hr class="mb-4" />

          <div>
            <label class="block text-gray-700 font-semibold mb-2" required>Select action<span
                class="text-red-800">*</span></label>
            <select v-model="SelectedAction"
              class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400" required>
              <option value="" disabled>Select your option</option>
              <option value="woo/order_confirmation">Send Order Confirmation</option>
              <option value="Abandoned Cart">Abandoned Cart</option>
              <option value="woo/pwn">PWNs (Pre Webinar Notifications)</option>
            </select>
          </div>

          <div v-if="SelectedAction === 'woo/order_confirmation'">
            <label class="block text-gray-700 font-semibold mb-2">Select template<span
                class="text-red-800">*</span></label>
            <select v-model="selectedTemplate"
              class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400" required>
              <option v-for="template in templates" :key="template.id" :value="template">
                {{ template.name }}
              </option>
            </select>

            <div v-if="selectedTemplate !== null">
              <label for="" class="block text-gray-700 font-semibold mb-2">Add Parameters<span
                  class="text-red-800">*</span></label>
              <div v-for="(parameter, index) in parameters" :key="index" class="flex items-center space-x-2 mb-2">

                <select v-model="parameter.key" class="w-full p-2 border rounded-md bg-gray-100">
                  <option value="" disabled>Select your parameter</option>
                  <option v-for="option in parameterOptions" :key="option" :value="option.key">{{ option.label }}
                  </option>
                </select>
                <button @click.prevent="removeParameter(index)"
                  class="relative my-2 h-8 w-24 border-2 border-solid border-red-500 text-red-500 hover:text-gray-200 hover:bg-red-700">
                  Remove
                </button>
              </div>
              <button @click.prevent="addParameter"
                class="relative my-2 h-auto w-auto p-1 border-2 border-solid border-green-500 text-green-500 hover:text-gray-200">
                Add Parameter
              </button>




              <h3 class="text-lg font-bold mb-2">Woocommerce Setup</h3>
              <input type="text" v-model="webhookLink" class="w-full p-2 border rounded-md bg-gray-100" disabled>

              <ul class="list-disc pl-5 mt-4 space-y-2 text-sm">
                <li>Navigate to <b>WooCommerce > Settings</b></li>
                <li>Click on the <b>Advanced tab</b></li>
                <li>In the <b>Advanced settings</b>, click on <b>Webhook</b></li>
                <li>Click the <b>Add Webhook</b> button.</li>
                <li><b>Configure Webhook Settings</b></li>
                <li><b>Name</b>: Give your webhook a name to identify it.</li>
                <li><b>Status:</b> Set this to Active.</li>
                <li>Topic: Choose the event you want the webhook to listen to</li>
                <li><b>Delivery URL: use the above given webhook URL</b></li>
                <li><b>Secret:</b> leave blank</li>
                <li><b>API Version:</b> Leave the default version</li>
                <li>Click Save Webhook to activate the integration</li>
              </ul>
            </div>
          </div>

          <div v-if="SelectedAction === 'woo/pwn'">
            <label class="block text-gray-700 font-semibold mb-2">Select template<span
                class="text-red-800">*</span></label>
            <select v-model="selectedTemplate"
              class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400" required>
              <option value="" disabled>Select your template</option>
              <option v-for="template in templates" :key="template.id" :value="template">{{ template.name }}</option>
            </select>

            <div v-if="selectedTemplate !== null">

              <div v-for="(parameter, index) in parameters" :key="index" class="flex items-center space-x-2 mb-2">

                <select v-model="parameter.key" class="w-full p-2 border rounded-md bg-gray-100">
                  <option value="" disabled>Select your parameter</option>
                  <option v-for="option in parameterOptions" :key="option" :value="option.key">{{ option.label }}
                  </option>
                </select>
                <button @click.prevent="removeParameter(index)"
                  class="relative my-2 h-8 w-24 border-2 border-solid border-red-500 text-red-500 hover:text-gray-200 hover:bg-red-700">
                  Remove
                </button>
              </div>
              <button @click.prevent="addParameter"
                class="relative my-2 h-auto w-auto p-1 border-2 border-solid border-green-500 text-green-500 hover:text-gray-200">
                Add Parameter
            </button>


              <label class="block text-gray-700 font-semibold mb-2">REST API Key<span
                  class="text-red-800">*</span></label>
              <input type="text" id="APIkey" class="w-full p-2 border rounded-md bg-gray-100" v-model="wooAPIkey"
                placeholder="Enter your REST API key">

              <label class="block text-gray-700 font-semibold mb-2">REST API Secret<span
                  class="text-red-800">*</span></label>
              <input type="text" class="w-full p-2 border rounded-md bg-gray-100" v-model="wooAPIsecret"
                placeholder="Enter your REST API secret">


              <label class="block text-gray-700 font-semibold mb-2">Time and Days<span
                  class="text-red-800">*</span></label>
              <div class="flex items-center ">

                <div class="mr-2">
                  <label for="scheduleTime" class="block text-sm font-medium">Time<span
                      class="text-red-800">*</span>(GMT
                    +5:30)</label>
                  <input type="time" v-model="scheduleTime" id="scheduleTime" required
                    class="border border-gray-300 rounded px-3 py-2 w-full">
                </div>


                <div class="flex justify-between items-center mt-4">
                  <div v-for="day in days" :key="day.id" @click="toggleDaySelection(day.id)" :class="[
                    'w-10 h-10 flex items-center justify-center cursor-pointer rounded-full font-bold transition-all duration-200',
                    day.selected ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700',
                  ]">
                    {{ day.initial }}
                  </div>
                </div>
                <!-- <p class="mt-4 text-gray-700 font-medium">
                    Selected days: {{ selectedDays.join(", ") }}
                  </p> -->
              </div>

              <label class="block text-gray-700 font-semibold mb-2">Select a Date Range<span
                class="text-red-800">*</span></label>
              <div class="flex">
               
                  <div class="mb-4">
                    <label for="scheduleTime" class="block text-sm font-medium">Start Date</label>
                    <input type="date" id="startDate" v-model="startDate"
                      class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
                  </div>
                  <div class="mb-4">
                    <label for="scheduleTime" class="block text-sm font-medium">End Date</label>
                    <input type="date" id="endDate" v-model="endDate"
                      class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
                  </div>
                
              </div>

              <label class="block text-gray-700 font-semibold mb-2">Product ID<span
                class="text-red-800">*</span></label>
              <input type="text" class="w-full p-2 border rounded-md bg-gray-100" v-model="productID">

              
              <label class="block text-gray-700 font-semibold mb-2">Order Status<span
                class="text-red-800">*</span></label>
              <input type="text" class="w-full p-2 border rounded-md bg-gray-100" v-model="OrderStatus">

              
              <label class="block text-gray-700 font-semibold mb-2">Woocommerce Base URL<span
                class="text-red-800">*</span></label>
              <input type="text" class="w-full p-2 border rounded-md bg-gray-100" v-model="Base_url">             

              <ul class="list-disc pl-5 mt-4 space-y-2 text-sm">
                <li>Navigate to <b>WooCommerce > Settings</b></li>
                <li>Click on the <b>Advanced tab</b></li>
                <li>In the <b>Advanced settings</b>, click on <b>REST API</b></li>
                <li>Click the <b>Add Key</b> button.</li>
                <li><b>Configure REST API Settings</b></li>
                <li><b>Description</b>: Give your REST API a description to identify it.</li>
                <li><b>User:</b>Select the user</li>
                <li>Permission: Select the permission</li>
                <li>Click on <b>generate API Key</b></li>
              </ul>

            </div>
          </div>




          <button type="submit" class="bg-[#23a455] text-[#f5f6fa] px-4 py-2 rounded">Save Integration</button>

        </form>
      </div>


    </PopUp>
    <h3 class="text-xl md:text-2xs mb-4 text-gray-600"><b>Integration List</b></h3>
    <div class="overflow-x-auto max-h-[45vh] custom-scrollbar">
      <table class="w-full rounded-lg border-collapse">
        <thead>
          <tr class=" text-center">
            <th class="p-2 md:p-4 border-b-2 sticky top-0 bg-[#ffffff]">ID</th>
            <th class="p-2 md:p-4 border-b-2 sticky top-0 bg-[#ffffff]">Application</th>
            <th class="p-2 md:p-4 border-b-2 sticky top-0 bg-[#ffffff]">Type</th>
            <th class="p-2 md:p-4 border-b-2 sticky top-0 bg-[#ffffff]">API Key</th>
            <th class="p-2 md:p-4 border-b-2 sticky top-0 bg-[#ffffff] z-10">Action</th>

          </tr>
        </thead>
        <tbody class="bg-white">
          <tr v-for="integration in integrations" :key="integration.id">
            <td class="border-[#ddd] p-2 md:p-4 text-center">{{ integration.id }}</td>
            <td class="border-[#ddd] p-2 md:p-4 text-center">{{ integration.app }}</td>
            <td class="border-[#ddd] p-2 md:p-4 text-center">{{ integration.type }}</td>
            <td class="border-[#ddd] p-2 md:p-4 text-center">{{ integration.api_key }}</td>
            <button @click="deleteIntegration(integration.id)"
              class="hover:bg-white rounded-full p-2 center">
              <lord-icon src="https://cdn.lordicon.com/skkahier.json" 
                colors="primary:#ff5757,secondary:#000000" style="width:32px;height:32px">
              </lord-icon>
            </button>
          </tr>
        </tbody>
      </table>
    </div>


  </div>
</template>


<script>
import PopUp from "../popups/popup";
import { useToast } from 'vue-toastification';

export default {

  name: 'AppIntegration',
  data() {

    return {
      showPopup: false,
      SelectedAction: null,
      templates: [],
      selectedTemplate: null,
      webhookLink: '',
      integrations: [],
      templateParams: [],
      parameters: [],  // List of parameters for the template
      parameterOptions: [{ label: "Customer Name", key: "billing.first_name" },
      { label: "Order ID", key: "id" },
      { label: "Order Total", key: "total" },
      { label: "Customer Phone", key: "billing.phone" },
      { label: "Payment Method", key: "payment_method" },],

      parameterFields: [{ selected: '' }],
      days: [
        { id: 1, name: "Monday", initial: "M", selected: false },
        { id: 2, name: "Tuesday", initial: "T", selected: false },
        { id: 3, name: "Wednesday", initial: "W", selected: false },
        { id: 4, name: "Thursday", initial: "T", selected: false },
        { id: 5, name: "Friday", initial: "F", selected: false },
        { id: 6, name: "Saturday", initial: "S", selected: false },
        { id: 7, name: "Sunday", initial: "S", selected: false },
      ],

      wooAPIsecret:null,
      wooAPIkey:null,
      startDate:null,
      endDate:null,
      productID:null,
      OrderStatus:null,
      Base_url:null

    }

  },
  components: {
    PopUp
  },
  async mounted() {
    await this.fetchTemplates()
    await this.fetchapiKey();
    await this.fetchIntegrationList();
    const script = document.createElement('script');
    script.src = "https://cdn.lordicon.com/lordicon.js";
    document.body.appendChild(script);



    // Fetch contacts when the component is mounted
  },

  computed: {
    selectedDays() {
      return this.days.filter(day => day.selected).map(day => day.name);
    },
  },

  methods: {


    submitIntegrationForm(action){
      if(action=="woo/order_confirmation"){
        this.submitTemplate();
      }
      else if(action=="woo/pwn"){
        this.wooPWNform();
      }
    },

    toggleDaySelection(id) {
      const day = this.days.find(day => day.id === id);
      if (day) {
        day.selected = !day.selected;
      }
    },
    submitSelection() {
      alert(`Selected days: ${this.selectedDays.join(", ")}`);
    },

    addParameter() {
      this.parameters.push({ key: this.parameterOptions[0] }); // Add a new parameter with default value
    },

    removeParameter(index) {
      this.parameters.splice(index, 1); // Remove parameter by index
    },
    togglepopup() {
      console.log("event")
    },
    async fetchTemplates() {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch('http://localhost:8000/template', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const templatelist = await response.json();
        this.templates = templatelist.data;
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


        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const result = await response.json()
        this.webhookLink = result.webkook_link
      } catch (error) {
        console.error('Error fetching API key:', error);
      }

    },
    async submitTemplate() {
      const payload = {
        template_id: this.selectedTemplate.name,
        template_data:JSON.stringify(this.selectedTemplate),
        parameters: this.parameters,
        type: this.SelectedAction,
        

      };

      // Replace with your API endpoint
      try {
        const toast = useToast();
        const token = localStorage.getItem('token');
        const response = await fetch('http://localhost:8000/integrate/woo_order_cnf', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(payload)
        });

        if (response.ok) {
          toast.success("Integration saved successfully");
          this.fetchIntegrationList();

        } else {
          const errorData = await response.json();
          toast.error(`Error: ${errorData.detail}`);
        }
        // Handle successful submission
      } catch (error) {
        console.error('Failed to submit the template: ', error);
      }
    },

    async wooPWNform() {
      const payload = {
        template_id: this.selectedTemplate.name,
        template_data:JSON.stringify(this.selectedTemplate),
        parameters: this.parameters,
        type: this.SelectedAction,
        contacts_start_date:this.startDate,
        contacts_end_date:this.endDate,
        repeat_days:[...this.selectedDays],
        time:this.scheduleTime,
        rest_key:this.wooAPIkey,
        rest_secret:this.wooAPIsecret,
        product_id:this.productID,
        status:this.OrderStatus,
        base_url:this.Base_url

      };

      // Replace with your API endpoint
      try {
        const toast = useToast();
        const token = localStorage.getItem('token');
        const response = await fetch('http://localhost:8000/integrate/woo_pwn', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(payload)
        });

        if (response.ok) {
          toast.success("Integration saved successfully");
          this.fetchIntegrationList();

        } else {
          const errorData = await response.json();
          toast.error(`Error: ${errorData.detail}`);
        }
        // Handle successful submission
      } catch (error) {
        console.error('Failed to submit the template: ', error);
      }
    },

    async deleteIntegration(integration_id) {
      try {

        const toast = useToast();
        const token = localStorage.getItem('token');
        const confirmDelete = confirm("Are you sure you want to delete this contact?                           Note:Make sure to also delete the webhook from woocommece.")
        if (!confirmDelete) return;
        const response = await fetch(`http://localhost:8000/integration/${integration_id}`,
          {
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          }
        );


        if (response.ok) {
          toast.success("Integration deleted successfully")
          this.fetchIntegrationList();
        }
        else {
          const errordata = await response.json()
          toast.error(`Error:${errordata.detail}`)
        }


      } catch (error) {
        console.error('Failed to delete the integration: ', error)

      }
    },

    async fetchIntegrationList() {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch("http://localhost:8000/integration/list", {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const IntegrationList = await response.json();
        this.integrations = IntegrationList.map(integration => ({
          id: integration.id,
          app: integration.app,
          type: integration.type,
          api_key: integration.api_key
        }));
      } catch (error) {
        console.error('Failed to submit the template: ', error);
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

.popup-content {
  max-height: 700px;
  /* Limit the height of the popup */
  overflow-y: auto;
  /* Enable vertical scrolling if content exceeds max-height */
}

/* Custom Scrollbar */
.custom-scrollbar::-webkit-scrollbar {
  width: 8px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  border-radius: 16px;
  background-color: #e7e7e7;
  border: 1px solid #cacaca;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  border-radius: 8px;
  border: 3px solid transparent;
  background-clip: content-box;
  background-color: #075e54;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>