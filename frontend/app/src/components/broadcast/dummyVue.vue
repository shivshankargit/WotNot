<template>
    <div class="max-w-3xl mx-auto p-6 bg-white shadow rounded-lg">
        <!-- Header -->
        <div class="flex items-center justify-between mb-4">
            <h2 class="text-lg font-semibold">Create Template Message</h2>
            <!-- <button class="px-4 py-2 bg-blue-600 text-white rounded-md">Use a sample</button> -->
            <span class="relative bottom-1 text-4xl cursor-pointer text-black" @click="closePopup">&times;</span>
        </div>

        <!-- Form Section -->
        <form>
            <!-- Template Name and Category -->
            <div class="grid grid-cols-3 gap-4">
                <div>
                    <label class="block text-sm font-medium">Template Name
                        <span class="relative text-sm" :class="{ 'text-black': !nameError, 'text-red-500': nameError }">
                            *
                        </span>
                    </label>
                    <div class="relative mb-2">
                        <input v-model="template.name" :placeholder="nameError || 'Template Name'" @blur="validateTemplateName" :class="[
                            'border border-[#ddd] p-2 rounded-md w-full',
                            { 'border-red-500': nameError, 'placeholder-red-500': nameError }
                        ]" required />

                    </div>
                </div>

                <div>
                    <label class="block text-sm font-medium">Category</label>
                    <select v-model="selectedCategory" class="mt-1 p-2 w-full border border-gray-300 rounded-md h-10">
                        <option value="Marketing">Marketing</option>
                        <option value="Utility">Utility</option>
                        <!-- Other options can go here -->
                    </select>
                </div>

                <!-- Language -->
                <div class="mb-4">
                    <label class="block text-sm font-medium">Language</label>
                    <select class="mt-1 p-2 w-full border border-gray-300 rounded-md h-10">
                        <option>English</option>
                        <!-- Add other languages here -->
                    </select>
                </div>

            </div>



            <!-- Template Type -->
            <!-- <div class="mb-4">
          <label class="block text-sm font-medium mb-2">Select Marketing template</label>
          <div class="flex space-x-4">
            <div>
              <input type="radio" id="standard" name="template" value="standard" class="mr-2">
              <label for="standard">Standard</label>
            </div>
            <div>
              <input type="radio" id="catalog" name="template" value="catalog" class="mr-2">
              <label for="catalog">Catalog</label>
            </div>
            <div>
              <input type="radio" id="carousel" name="template" value="carousel" class="mr-2" disabled>
              <label for="carousel">Carousel</label>
            </div>
            <div>
              <input type="radio" id="limited" name="template" value="limited" class="mr-2" disabled>
              <label for="limited">Limited Time Offers</label>
            </div>
          </div>
        </div> -->

            <label for="">Header</label>
            <input placeholder="Header Text (optional)" class="border border-[#ddd] p-2 rounded-md w-full mb-2" />

            <div class="mb-4">
                <label class="block text-sm font-medium">Body</label>
                <textarea class="mt-1 p-2 w-full border border-gray-300 rounded-md" placeholder="Template Message..."
                    rows="4"></textarea>
            </div>

            <label for="">Footer</label>
            <input placeholder="Footer Text (optional)" class="border border-[#ddd] p-2 rounded-md w-full mb-2" />

            <span>
                <button class="relative my-2 h-8 w-24 border-2 border-solid border-green-500 text-green-500 hover:text-gray-200" @click.prevent="addbutton">
                    Add Button
                </button>
            </span>

            <!-- Button Text and URL Inputs -->
            <input v-if="addButton && selectedSubCategory !== 'ORDER_STATUS'" v-model="button.text"
                placeholder="Button Text (optional)" class="border border-[#ddd] p-2 rounded-md w-full mb-2" />
            <input v-if="addButton && selectedSubCategory !== 'ORDER_STATUS'" v-model="button.url"
                placeholder="Button URL (optional)" class="border border-[#ddd] p-2 rounded-md w-full mb-2" />


            <!-- Sub-Category Selection -->
            <label v-if="selectedCategory === 'Marketing'" for="">Sub-Category</label>
            <select v-model="selectedSubCategory" v-if="selectedCategory === 'Marketing'" required
                class="border border-[#ddd] p-2 rounded-md w-full mb-2">
                <option value="" disabled>Select Sub-Category</option>
                <option value="ORDER_DETAILS">Order Details</option>
                <!-- <option value="ORDER_STATUS">Order Status</option> -->
            </select>
            <!-- Actions -->
            <div class="flex space-x-4">
                <button class="px-4 py-2 bg-green-600 text-white rounded-md">Save</button>
                <button class="px-4 py-2 bg-gray-400 text-white rounded-md">Cancel</button>
            </div>
        </form>
    </div>
</template>

<script>
export default {
    data() {
        return {
            templateName: '',
            isTemplateNameValid: true,
            addButton: false, 
            templates: [],
            showPopup: false,
            showSelectionPopup: false,
            selectedCategory: 'Marketing',
            selectedSubCategory: '',
            template: {
                name: '',
                components: []
            },
            bodyComponent: {
                type: 'BODY',
                text: ''
            },
            headerComponent: {
                type: 'HEADER',
                format: 'TEXT',
                text: ''
            },
            footerComponent: {
                type: 'FOOTER',
                text: ''
            },
            button: {
                type: 'URL',
                text: '',
                url: ''
            },
            nameError: ''
        };
    },

    methods: {
        addbutton() {
            this.addButton = true ;
        },
        validateTemplateName() {
            const regex = /^[a-z_]+$/;

            if (this.template.name.trim() === '') {
                this.nameError = 'Template name is required';
            } else if (!regex.test(this.template.name)) {
                this.template.name = '';
                this.templateName = '';
                this.nameError = `Only lowercase letters and '_'`;
            } else {
                this.nameError = '';
            }
        }
    }
};
</script>


<style scoped>
/* Optional: You can add custom styles here */
</style>