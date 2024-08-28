<template>
  <div class="content-section">
    <button @click="showPopup = true">Add Contact</button>
    <PopUp1 v-if="showPopup" @close="closePopup">
      <form @submit.prevent="submitForm" id="contactForm">
        <input type="hidden" v-model="contact.id" id="contactId">
        <input type="text" v-model="contact.name" id="name" placeholder="Name" required>
        <input type="email" v-model="contact.email" id="email" placeholder="Email" required>
        <input type="text" v-model="contact.phone" id="phone" placeholder="Phone" required>
        <input type="text" v-model="contact.tags" id="tags" placeholder="Tags (comma separated)">
        <button type="submit">{{ contact.id ? 'Update Contact' : 'Add Contact' }}</button>
      </form>

    </PopUp1>
    <!-- Action Popup -->
    <PopUpSmall v-if="showActionPopup" @close="closeActionPopup">
      <div class="action-popup-content">
        <p>What action do you want to take?</p>
        <div class="action-buttons">
          <button @click="modifyContact">Modify</button>
          <button @click="deleteContact(selectedContact.phone)">Delete</button>
        </div>

      </div>
    </PopUpSmall>
    <div class="contactsListContainer">

      <table class="contactsList-table">
        <thead>
          <tr>
            <th>id</th>
            <th>contacts_Name</th>
            <th>phone_number</th>
            <th>email</th>
            <th>tags</th>

            <th>Action</th><!-- Action-->

          </tr>
        </thead>
        <tbody>

          <tr v-for="contact in contacts" :key="contact.id">
            <td>{{ contact.id }}</td>
            <td>{{ contact.name }}</td>
            <td>{{ contact.phone }}</td>
            <td>{{ contact.email }}</td>
            <td>{{ contact.tags }}</td>

            <td>
              <button @click="openActionPopup(contact)">Action</button>
            </td>

          </tr>

        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import PopUp1 from "../popups/popup1";
import PopUpSmall from "../popups/popup_small";
export default {
  components: {
    PopUp1, PopUpSmall
  },
  async mounted() {
    await this.fetchContactList();
  },
  name: "ContActs1",
  data() {
    return {
      showPopup: false,
      showActionPopup: false,
      contact: {
        id: "",
        name: "",
        email: "",
        phone: "",
        tags: "",
      },
      selectedContact: null,
      contacts: [],
    };
  },
  methods: {
    async submitForm() {
      const { id, name, email, phone, tags } = this.contact;

      // Ensure tags are correctly handled, whether they're a string or already an array
      const tagArray = Array.isArray(tags)
        ? tags
        : typeof tags === 'string'
          ? tags.split(",").map(tag => tag.trim()).filter(tag => tag.length > 0) // Ensure no empty tags
          : [];

      const url = id ? `http://localhost:8000/contacts/${id}` : "http://localhost:8000/contacts/";
      const method = id ? "PUT" : "POST";
      const token = localStorage.getItem("token");

      try {
        const response = await fetch(url, {
          method: method,
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ name, email, phone, tags: tagArray }),
        });

        if (response.ok) {
          alert("Contact saved successfully");
          this.clearForm();
          this.fetchContactList();
        } else {
          const errorData = await response.json();
          alert(`Error: ${errorData.detail}`);
        }
      } catch (error) {
        console.error("Error saving contact:", error);
        alert("Error saving contact");
      }
    },
    clearForm() {
      this.contact = {
        id: "",
        name: "",
        email: "",
        phone: "",
        tags: "",
      };
      this.showPopup = false;
    },
    closePopup() {
      this.showPopup = false;
      this.clearForm();  // Clear the form when closing the popup
    },
    async fetchContactList() {
      const token = localStorage.getItem("token");
      try {
        const response = await fetch("http://localhost:8000/contacts/", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          throw new Error("Network response was not ok");
        }

        const contactsList = await response.json();
        this.contacts = contactsList.map((contact) => ({
          id: contact.id,
          name: contact.name,
          phone: contact.phone,
          email: contact.email,
          tags: contact.tags,
        }));
      } catch (error) {
        console.error("Error fetching contact:", error);
      }
    },
    openActionPopup(contact) {
      this.selectedContact = contact;
      this.showActionPopup = true;
    },
    closeActionPopup() {
      this.showActionPopup = false;
      this.selectedContact = null;
    },
    modifyContact() {
      this.contact = { ...this.selectedContact };
      this.showPopup = true;
      this.closeActionPopup();
    },
    async deleteContact(phone) {
      const confirmDelete = confirm("Are you sure you want to delete this contact?");
      if (!confirmDelete) return;

      const token = localStorage.getItem("token");
      try {
        const response = await fetch(`http://localhost:8000/contacts/${phone}`, {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });

        if (response.ok) {
          alert("Contact deleted successfully");
          this.fetchContactList();
          this.closeActionPopup();
        } else {
          const errorData = await response.json();
          alert(`Error: ${errorData.detail}`);
        }
      } catch (error) {
        console.error("Error deleting contact:", error);
        alert("Error deleting contact");
      }
    },
  },
};
</script>


<style scoped>
.contactsListContainer {
  background-color: #f5f6fa;
  border-radius: 12px;
  width: 100%;
  padding: 20px;
  margin-bottom: 20px;
  max-width: 1100px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);

}

.contactsList-table {
  width: 100%;
  border-radius: 12px;
  border-collapse: collapse;
  overflow-x: auto;
  display: block;
  max-height: 400px;
  /* Adjust height as needed */

}

th {
  padding: 20px;
  text-align: left;
  border-collapse: collapse;
  border: 1px solid #ddd;


}

.contactsList-table td {
  border: 1px solid #ddd;

  padding: 20px;
  text-align: left;
  border-collapse: collapse;
}

.contactsList-table thead th {
  position: sticky;
  top: 0;
  background-color: #dddddd;
  border-collapse: collapse;
  border: 1px solid #ddd;

}

.contactsList-table tbody {
  background-color: white;
}


/* Add your styles here */
</style>
