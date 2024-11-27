<template>
  <div id="app" class="main-container">
    <!-- Sidebar for Active Chats -->
    <div class="sidebar">
      <b>
        <div class="w-40px">
          <select name="" id="" v-model="chatStatusFilter" @change="filterChatsByStatus"
            class="no-border px-3 py-2 text-black" style="font-size: 16px; outline: none;">
            <option value="" selected style="font-size: 16px; color: black;">All Chats</option>
            <option value="true" style="font-size: 16px; color: black;">Active Chats
            </option>

          </select>
        </div>

      </b>
      <ul class="chat-list">
        <ul>
          <li v-for="chat in activeChat" :key="chat.message_id">

            <div class="flex bg-white justify-between rounded-lg p-4 text-black shadow-md"
              @click="ConversationSSE(chat.sender_wa_id), ActiveWaid = chat.sender_wa_id, ActiveWaidName = chat.sender_name">

              <div class="">

                <p>{{ chat.sender_name }}</p>
                <p>{{ chat.message_content }}</p>
              </div>


              <div class="messageTime">
                <p>{{ chat.last_chat_time.split('T')[1].substring(0, 5) }}</p>
              </div>
            </div>


          </li>
        </ul>
      </ul>
    </div>


    <!-- Chat Area -->
    <div class="chat-area">

      <!-- Chat Header -->
      <div class="chat-header">

        <div class="timer">

          <div class="text-gray-600" v-if="ActiveWaid">
            <i class="bi bi-person-circle" style="font-size: 2.1rem;"></i>
          </div>


          <div class="flex flex-col items-start justify-start w-full text-[14px]  p-3">
            <h3><b>{{ ActiveWaidName }}</b></h3>
            <p style="font-size: 13px; color: rgb(132, 138, 134);"><b>{{ ActiveWaid }}</b></p>
          </div>

          <div class="flex items-start justify-end w-full">
            <span id="currentTime">{{ selectedRemainingTime }}</span>
          </div>

        </div>
      </div>

      <!-- Chat Content Section -->
      <div class="chat-content" id="chatContent" ref="chatContent">
        <div v-html="chatContent"></div>
        <div id="messages">
          <div v-for="(message, index) in selectedchat" :key="message.id">
            <!-- Show Date Separator if Date Changes -->
            <div v-if="shouldShowDate(index)" class="text-center my-2 text-sm text-gray-500">
              <p>{{ formatDate(selectedchat[index].timestamp.split('T')[0]) }}</p>
            </div>

            <!-- Message Bubble -->
            <div :class="{ 'message': true, 'sent-message': message.direction == 'sent' }">
              <div>
                <div v-if="message.context_message_id" class="replied-message-context mb-2 text-sm text-gray-600">
                  
                  <div class="replied-message">
                    <p><strong>Replied to:</strong> {{ getRepliedMessageContent(message.context_message_id) }}</p>
                  </div>

                </div>

                <div>
                  <p>{{ message.message_content }}</p>
                </div>

                <div class="messageTime">
                  <p>{{ message.timestamp.split('T')[1].substring(0, 5) }}</p>
                </div>

              </div>
            </div>
          </div>
        </div>

</div>
        <!-- Message Input Area -->
        <div class="message-input-area" v-if="selectedRemainingTime != 'Chat is expired'">
          <input type="text" v-model="newMessage" @keyup.enter="sendMessage" placeholder="Type a message..." />
          <label for="file-upload" class="upload-label">
            <i class="bi bi-paperclip"></i>
          </label>

          <button @click.stop="togglePicker" class="emoji-button"><i class="bi bi-emoji-smile"></i></button>

          <!-- Emoji Picker (conditionally rendered) -->
          <div v-if="showPicker" class="custom-picker" ref="picker">
            <EmojiPicker @select="onEmojiSelect" />
          </div>

          <input type="file" id="file-upload" @change="FileUpload" class="file-input" />
          <button id="send-button" @click="sendChatMessage()">Send</button>
        </div>
        <div v-else class="message-input-area flex justify-center text-center">

          <h2>Chats are marked as expired 24 hours after the last received customer message.
            <br>WhatsApp allows only template messages to be sent in such chats.
          </h2>

        </div>
      </div>

      <!-- Contact Information -->
      <div class="contact-info">

        <div class="inner-container bg-white p-4 border-radius-4 h-inherit">
          <h4><i class="bi bi-person-vcard"
              style=" font-size:18px; color: gray; font-weight: 300; margin-right:2px"></i><strong> Contact
              Details</strong> </h4>
          <table class="contact-table">
            <tbody>
              <tr>
                <td style=" color: gray; font-weight: 300;">Name</td>
                <td>{{ contactInfo.name }}</td>
              </tr>
              <tr>
                <td style=" color: gray; font-weight: 300;">Phone</td>
                <td>{{ contactInfo.phone }}</td>
              </tr>
              <tr>
                <td style=" color: gray; font-weight: 300;">Email</td>
                <td>{{ contactInfo.email }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="inner-container bg-white p-4 border-radius-4 h-inherit">
          <h4><i class="bi bi-at" style=" color: gray; font-weight: 300; margin-right:2px"></i><strong>Contact
              Attributes</strong></h4>
          <table class="contact-table">
            <tbody>
              <tr>
                <td style=" color: gray; font-weight: 300;">Created at</td>
                <td>{{ contactInfo.created_at }}</td>
              </tr>
              <tr>
                <div v-for="(tag, index) in contactInfo.tags" :key="index">
                  <td style=" color: gray; font-weight: 300;">{{ tag.split(':')[0] }}</td>
                  <td>{{ tag.split(':')[1] }}</td>
                </div>
              </tr>

            </tbody>
          </table>
        </div>


      </div>
    </div>
 
</template>

<script>
import EmojiPicker from 'vue3-emoji-picker';
import { toZonedTime } from "date-fns-tz";
export default {
  components: { EmojiPicker },
  name: 'ChatbotView',

  data() {
    return {
      // Default to first item
      chatStatusFilter: "",
      showPicker: false,
      activeChat: [],
      selectedchat: [],
      selectedChatTime: null,
      selectedRemainingTime: null,
      timer: null,
      ActiveWaid: "",
      ActiveWaidName: "",
      chats: [],
      chatTitle: "",
      chatContent: "",
      contactInfo: {},
      messages: [],
      newMessage: "",
      currentTime: "",
      progressSeconds: 0,
      eventSourceA: null,
      eventSourceB: null,
    };
  },
  async mounted() {
    // Add click event listener when component is mounted
    document.addEventListener('click', this.handleClickOutside);
    await this.fetchActiveChatlist();

  },

  methods: {

    getRepliedMessageContent(replyToId) {
      const repliedMessage = this.selectedchat.find(message => message.message_id === replyToId);
      return repliedMessage ? repliedMessage.message_content : '';
    },

    shouldShowDate(index) {
      if (index === 0) return true; // Always show the date for the first message
      const currentDate = this.selectedchat[index].timestamp.split('T')[0];
      const previousDate = this.selectedchat[index - 1].timestamp.split('T')[0];
      return currentDate !== previousDate; // Show date separator if the date changes
    },
    formatDate(date) {
      // Format date to a more readable format if needed
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(date).toLocaleDateString(undefined, options);
    },

    FileUpload(event) {
      const file = event.target.files[0];
      console.log('File uploaded:', file);
    },

    togglePicker() {
      this.showPicker = !this.showPicker;
    },
    handleClickOutside(event) {
      if (this.showPicker && !this.$refs.picker.contains(event.target)) {
        this.showPicker = false; // Hide the picker
      }
    },

    onEmojiSelect(emoji) {
      if (emoji && emoji.i) {
        this.newMessage += emoji.i; // Append the emoji from the 'i' property
      } else {
        console.error("Invalid emoji object:", emoji);
      }
    },

    SetChatTime(chatTime) {

      console.log(chatTime);
      this.selectedChatTime = chatTime;

      // Convert the chatTime string to a Date object
      const chatDate = new Date(chatTime);



      const TimeZoneChatTime = chatDate;


      // Add 24 hours to chatDate
      const EndDate = new Date(TimeZoneChatTime.setHours(TimeZoneChatTime.getHours() + 24));


      // Clear any existing timer to avoid multiple intervals
      if (this.timer) {
        clearInterval(this.timer);
      }

      // Function to update the remaining time
      const updateRemainingTime = () => {


        const currentDate = new Date();
        const utcDate = toZonedTime(currentDate, "UTC");// Local timezone

        // console.log(utcDate);
        // console.log(EndDate);
        // Get the current date and time
        const timeDifference = EndDate - utcDate; // Calculate the difference

        if (timeDifference <= 0) {
          // If time has expired, stop the timer and show "Chat is expired"
          clearInterval(this.timer);
          this.selectedRemainingTime = 'Chat is expired';

          return;
        }

        // Calculate remaining days, hours, minutes, seconds

        const minutes = Math.floor((timeDifference / 1000 / 60) % 60);
        const hours = Math.floor((timeDifference / 1000 / 60 / 60) % 24);
        const days = Math.floor(timeDifference / 1000 / 60 / 60 / 24);

        // Construct remaining time string
        let remainingTime = '';
        if (days > 0) remainingTime += `${days} : `;
        remainingTime += `${String(hours).padStart(2, '0')} : `; // Format hours
        remainingTime += `${String(minutes).padStart(2, '0')}  `; // Format minutes
        this.selectedRemainingTime = remainingTime.trim();
      };

      // Call the update function immediately to show the initial remaining time
      updateRemainingTime();

      // Set up the interval to update the remaining time every second
      this.timer = setInterval(updateRemainingTime, 1000);
    },

    beforeDestroy() {
      // Clear the timer when the component is destroyed to avoid memory leaks
      if (this.timer) {
        clearInterval(this.timer);
      }
    },

    async fetchActiveChatlist(chatStatusFilter = null) {
      try {

        if (this.eventSourceB) {
          // Close the previous EventSource connection
          this.eventSourceB.close();
          console.log("Previous SSE connection closed.");
        }

        const token = localStorage.getItem('token');

        // Create a new EventSource for receiving SSE
        this.eventSourceB = new EventSource(`http://localhost:8000/active-conversations?token=${token}`, {
          headers: {
            'Authorization': `Bearer ${token}`  // Unfortunately, EventSource does not support custom headers directly
          }
        });

        // Listen for events
        this.eventSourceB.onmessage = (event) => {
          const activeChats = JSON.parse(event.data);

          // Map the received active chat data
          this.activeChat = activeChats.map((activechat) => ({
            message_content: activechat.message_content,
            sender_name: activechat.sender_name,
            business_account_id: activechat.business_account_id,
            active: activechat.active,
            message_id: activechat.message_id,
            id: activechat.id,
            sender_wa_id: activechat.sender_wa_id,
            last_chat_time: activechat.last_chat_time
          })).filter(activechat => {
            if (chatStatusFilter !== null) {
              return activechat.active == (chatStatusFilter === 'true');
            }
            return true;
          });

        };



        // Handle connection errors
        this.eventSourceB.onerror = (error) => {
          console.error("Unable to fetch active conversations", error);
          this.eventSourceB.close(); // Close the connection on error
        };

      } catch (error) {
        console.error("Unable to fetch active conversations");
      }
    },

    filterChatsByStatus(event) {
      const status = event.target.value;
      this.fetchActiveChatlist(status);
    },

    ConversationSSE(wa_id) {

      this.selectedRemainingTime = null;
      // Check if there's an existing EventSource instance
      if (this.eventSourceA) {
        // Close the previous EventSource connection
        this.eventSourceA.close();
        console.log("Previous SSE connection closed.");
      }

      // Fetch the token
      const token = localStorage.getItem('token');

      // Create a new EventSource instance with the new wa_id
      this.eventSourceA = new EventSource(`http://localhost:8000/sse/conversations/${wa_id}?token=${token}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      this.ActiveContactDetails(wa_id);

      // Handle incoming messages
      this.eventSourceA.onmessage = (event) => {
        try {
          // Parse the new conversations data
          const newConversations = JSON.parse(event.data);

          // Determine if the user is already scrolled to the bottom
          const chatContent = this.$refs.chatContent;
          const isAtBottom = chatContent.scrollHeight - chatContent.scrollTop <= chatContent.clientHeight + 10;

          this.selectedchat = newConversations;  // Update the UI with the new data

          // Get the last chat timestamp and call SetChatTime
          if (newConversations.length > 0) {
            // Filter messages to only include those with direction "received"
            const receivedMessages = newConversations.filter(
              (message) => message.direction === "Receive"
            );

            if (receivedMessages.length > 0) {
              // Get the last "received" message
              const lastReceivedMessage =
                receivedMessages[receivedMessages.length - 1];

              // Pass its timestamp to SetChatTime
              this.SetChatTime(lastReceivedMessage.timestamp);
            }
          }



          // Only scroll to the bottom if the user is already at (or near) the bottom
          if (isAtBottom) {
            this.scrollToBottom();
          }
        } catch (error) {
          console.error("Error parsing SSE data", error);
        }
      };

      // Handle errors
      this.eventSourceA.onerror = (error) => {
        console.error("SSE connection error:", error);
        // You can handle reconnections or notify the user here if needed
      };

      console.log("New SSE connection established.");
    },

    // Scroll logic to be called after new data is loaded
    scrollToBottom() {
      this.$nextTick(() => {
        const chatContent = this.$refs.chatContent;
        if (chatContent) {
          chatContent.scrollTop = chatContent.scrollHeight;
        }
      });
    },

    async ActiveContactDetails(wa_id) {
      const token = localStorage.getItem('token');

      try {

        const response = await fetch(`http://localhost:8000/contacts/${wa_id}`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          }
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }


        const contact = await response.json()

        this.contactInfo = contact;

      } catch (error) {

        console.error("Error fetching contact details:", error);

      }
    },


    async sendChatMessage() {

      const message = this.newMessage
      const reciever = this.ActiveWaid
      try {
        const token = localStorage.getItem("token");

        const requestBody = {
          wa_id: reciever,
          body: message
        }

        const response = await fetch("http://localhost:8000/send-text-message/", {
          method: "POST",
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestBody)

        })
        if (!response.ok) {
          throw new Error("Network response not okay");
        }
        else {
          this.newMessage = "";
        }

      } catch (error) {
        console.error("Error sending message")
      }
    }

  },


  beforeUnmount() {

    document.removeEventListener('click', this.handleClickOutside);
    // Clean up the EventSource instance
    if (this.eventSourceB) {

      this.eventSourceB.close();
      console.log("SSE connection closed on component unmount.");
    }
    if (this.eventSourceA) {
      this.eventSourceA.close();
      console.log("SSE connection closed on component unmount.");
    }
  },


};
</script>





<style scoped>
/* Main container layout */


.main-container {
  display: flex;
  height: 92.2vh;
  width: 100%;
  background-color: #f4f4f4;
  font-family: Arial, sans-serif;
}

/* Sidebar styling */
.sidebar {
  width: 20%;
  padding: 15px;
  background-color: #ffffff;
  color: #ffffff;
  overflow-y: auto;
}

.sidebar h1 {
  color: #000;
  margin-bottom: 10px;
}

.chatType {
  display: flex;
  border-bottom: 1px solid #ccc;
  margin-bottom: 20px;
}

.chat-list {
  list-style: none;
  padding: 0;
}

.chat-list li {
  margin-bottom: 15px;
}

.chat-list a {
  display: block;
  padding: 10px;
  color: #ffffff;
  background-color: #128C7E;
  text-decoration: none;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.chat-list a:hover {
  background-color: #25D366;
}

/* Chat area styling */
.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: #f5f6fa;
  border-left: 1px solid #ddd;
}

.chat-header {
  display: flex;
  align-items: center;
  height: 65px;
  padding: 10px 30px;
  background-color: #f9f9f9;
  border-bottom: 1px solid #ccc;
  color: #000;
  font-size: 1rem;
  text-align: center;
  width: 100%;
  box-sizing: border-box;
}

.chat-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background-image: url("@/assets/chat-bg.jpg");
  background-size: contain;
  /* Scales the image to fit within the container */
  background-repeat: repeat;
  /* Prevents the image from repeating */
  background-position: center;
  height: calc(100vh - 200px);
}

.chat-content::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 1);
  /* Set the opacity here */
  z-index: -1;
  /* Keeps the overlay behind the content */
}

/* Message styling */
.message {
  display: flex;
  justify-content: space-between;
  background-color: white;
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 10px;
  max-width: 60%;
  min-width: 80px;
  width: fit-content;
}

.sent-message {
  align-self: flex-end;
  margin-left: auto;
  background-color: #dcf8c6;
}

.messageTime {
  display: flex;
  margin-left: 5px;
  font-size: 12px;
  color: #666;
  align-items: flex-end;
}

/* Message input area */
.message-input-area {
  display: flex;
  align-items: center;
  padding: 10px;
  background-color: #f1f1f1;
}

.message-input-area input[type="text"] {
  flex-grow: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}



#send-button {
  padding: 10px 15px;
  margin-left: 10px;
  background-color: #25D366;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

#send-button:hover {
  background-color: #1da857;
}

/* Upload button */
.upload-label {
  cursor: pointer;
  margin-left: 10px;
}

.upload-label i {
  font-size: 18px;
  color: #666;
}

.upload-label:hover i {
  color: #25d366;
}

.file-input {

  display: none;

}

/* Contact information styling */
.contact-info {
  width: 30%;
  padding: 10px;
  padding-top: 13px;
  background-color: #f0f0f0;
  border-left: 1px solid #ddd;
}

.contact-info h3 {
  margin-top: 0;
}

.tags {
  margin-top: 20px;
}

.tags h4 {
  margin-bottom: 10px;
}

.tags ul {
  list-style: none;
  padding: 0;
}

.tags ul li {
  display: inline-block;
  margin-bottom: 5px;
  background-color: #128C7E;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
}

.tags ul li button {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  margin-left: 10px;
}

.tags input {
  padding: 5px;
  margin-top: 10px;
  width: 80%;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.tags button {
  padding: 5px 10px;
  background-color: #128C7E;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.tags button:hover {
  background-color: #25D366;
}

/* Timer styling */
.timer {
  display: flex;
  align-items: center;
  padding: 19px 0 15px 0;
  width: inherit;
  margin-right: 10px;
}



.progress-circle {
  fill: none;
  stroke: #4caf50;
  stroke-width: 5;
  transform: rotate(-90deg);
  transform-origin: 50% 50%;
}

/* Contact table styling */
.contact-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.contact-table th,
.contact-table td {

  padding: 8px;
  text-align: left;
}

.contact-table th {
  background-color: #f2f2f2;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
  .sidebar {
    width: 100%;
  }

  .chat-area,
  .contact-info {
    width: 100%;
    margin-top: 10px;
  }

  .chat-area {
    order: 2;
  }

  .contact-info {
    order: 1;

  }

  .main-container {
    flex-direction: column;
  }
}
</style>