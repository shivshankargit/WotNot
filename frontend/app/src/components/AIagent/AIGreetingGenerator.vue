<template>
    <div class="ai-greeting-generator p-4 bg-white shadow-md rounded-md">
        <h3 class="text-lg font-bold mb-2">Generate AI Greeting</h3>

        <div class="mb-2">
            <label class="block mb-1">Name:</label>
            <input type="text" v-model="name" placeholder="Enter recipient name"
                class="border rounded px-2 py-1 w-full" />
        </div>

        <div class="mb-2">
            <label class="block mb-1">Prompt (optional):</label>
            <input type="text" v-model="prompt" placeholder="Enter greeting prompt (default: Happy Diwali)"
                class="border rounded px-2 py-1 w-full" />
        </div>

        <button @click="generateGreeting"
            class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
        Generate Greeting
        </button>

        <div v-if="loading" class="mt-2 text-gray-500">Generating...</div>

        <div v-if="greeting" class="mt-4 p-2 border rounded bg-gray-50">
            <strong>Generated Greeting:</strong>
            <p class="mt-1">{{ greeting }}</p>
        </div>

        <div v-if="error" class="mt-2 text-red-600">{{ error }}</div>
    </div>
</template>

<script>
export default {
    name: "AiGreetingGenerator",
    data() {
        return {
            name: "",
            prompt: "",
            greeting: "",
            loading: false,
            error: "",
        };
    },
    methods: {
        async generateGreeting() {
            this.error = "";
            this.greeting = "";
            if (!this.name) {
                this.error = "Name is required";
                return;
            }

            this.loading = true;
            try {
                const response = await fetch(`${process.env.VUE_APP_API_URL}/generate-greeting`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    name: this.name,
                    prompt: this.prompt || undefined,
                }),
            });

            if (!response.ok) {
                throw new Error("Failed to generate greeting");
            }

            const data = await response.json();
            this.greeting = data.greeting;
        } catch (err) {
            this.error = err.message;
        } finally {
            this.loading = false;
        }
    },
    },    
};
</script>

<style scoped>
.ai-greeting-generator input {
    transition: border-color 0.2s;
}

.ai-greeting-generator input:focus {
    outline: none;
    border-color: #4ade80;
}
</style>
