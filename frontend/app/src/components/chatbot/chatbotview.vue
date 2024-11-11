<template>
    <div id="app" class="main-container">
      <!-- Sidebar for Active Chats -->
      <div class="sidebar">
        <b>
        <div class="chatType">
          <h1>Active Chats</h1>
        </div>
          
  
  
        </b>
        <ul class="chat-list">
          <ul>
            <li v-for="chat in activeChat" :key="chat.message_id">
  
              <div class="bg-white rounded-lg p-4 text-black shadow-md"
                @click="ConversationSSE(chat.sender_wa_id), ActiveWaid = chat.sender_wa_id ,ActiveWaidName=chat.sender_name,SetChatTime(chat.last_chat_time)">
  
                <p>{{ chat.sender_name}}</p>
                <p>{{ chat.message_content }}</p>
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
            
  
  
            <span id="currentTime">{{ selectedRemainingTime }}</span>
          </div>
          <i class="fas fa-user-circle" style="font-size: 2rem;"></i>
  
          <div>
            <h3>{{ ActiveWaidName }}</h3>
            <p style="font-size: medium;">{{ ActiveWaid }}</p>
            
          </div>
          
  
          <div>
  
          </div>
          <select id="userDropdown" @change="selectUser">
            <option value="" disabled selected>Select User</option>
            <option v-for="chat in chats" :key="chat.message_id" :value="chat.message_id">{{ chat.contact_details.name }}
            </option>
          </select>
        </div>
  
        <!-- Chat Content Section -->
        <div class="chat-content" id="chatContent" ref="chatContent">
          <div v-html="chatContent"></div>
          <div class="" id="messages">
            <div v-for="message in selectedchat" :key="message.id"
              :class="{ 'message': true, 'sent-message': message.direction == 'sent' }">
              <div><p>{{ message.message_content }}</p></div>
              <div class="messageTime"><p>{{ message.timestamp.split('T')[1].substring(0, 5) }}</p></div>
              
              
            </div>
          </div>
        </div>
  
        <!-- Message Input Area -->
        <div class="message-input-area">
          <input type="text" v-model="newMessage" @keyup.enter="sendMessage" placeholder="Type a message..." />
          <label for="file-upload" class="upload-label">
            <i class="fas fa-paperclip"></i>
          </label>
          <input type="file" id="file-upload" @change="handleFileUpload" class="file-input" />
          <button @click="sendChatMessage()">Send</button>
        </div>
      </div>
  
      <!-- Contact Information -->
      <div class="contact-info">
        <h3>{{ contactInfo.name }}</h3>
        <p><strong>Phone Number:</strong> {{ contactInfo.phone }}</p>
        <h4>Contact Attributes</h4>
        <table class="contact-table">
          <tbody>
            <tr>
              <td><strong>Email:</strong></td>
              <td>{{ contactInfo.email }}</td>
            </tr>
            <tr>
              <td><strong>Created at:</strong></td>
              <td>{{ contactInfo.created }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ChatbotView',
    data() {
      return {
        // Default to first item
        activeChat: [],
        selectedchat: [],
        selectedChatTime: null,
        selectedRemainingTime: null,
        timer: null,
        ActiveWaid: "",
        ActiveWaidName:"",
        chats: [],
        chatTitle: "",
        chatContent: "",
        contactInfo: {},
        messages: [],
        newMessage: "",
        currentTime: "",
        progressSeconds: 0,
        ws: null,
        eventSource: null
      };
    },
    async mounted() {
  
      await this.fetchActiveChatlist();
  
    },
    methods: {
  
      SetChatTime(chatTime) {
        this.selectedChatTime = chatTime;
  
        // Convert the chatTime string to a Date object
        const chatDate = new Date(chatTime);
        
  
  
        const TimeZoneChatTime=chatDate;
        
       
        // Add 24 hours to chatDate
        const EndDate = new Date(TimeZoneChatTime.setHours(TimeZoneChatTime.getHours() + 24));
        
  
        // Clear any existing timer to avoid multiple intervals
        if (this.timer) {
          clearInterval(this.timer);
        }
  
        // Function to update the remaining time
        const updateRemainingTime = () => {
          const currentDate = new Date();
           // Get the current date and time
          const timeDifference = EndDate - currentDate; // Calculate the difference
  
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
  
      async fetchActiveChatlist() {
      try {
          const token = localStorage.getItem('token');
  
          // Create a new EventSource for receiving SSE
          const eventSource = new EventSource(`http://localhost:8000/active-conversations?token=${token}`, {
            headers: {
              'Authorization': `Bearer ${token}`  // Unfortunately, EventSource does not support custom headers directly
            }
          });
  
          // Listen for events
          eventSource.onmessage = (event) => {
              const activeChats = JSON.parse(event.data);
  
              // Map the received active chat data
              this.activeChat = activeChats.map((activechat) => ({
                  message_content: activechat.message_content,
                  sender_name:activechat.sender_name,
                  business_account_id: activechat.business_account_id,
                  active: activechat.active,
                  message_id: activechat.message_id,
                  id: activechat.id,
                  sender_wa_id: activechat.sender_wa_id,
                  last_chat_time: activechat.last_chat_time
              }));
          };
  
          // Handle connection errors
          eventSource.onerror = (error) => {
              console.error("Unable to fetch active conversations", error);
              eventSource.close(); // Close the connection on error
          };
  
      } catch (error) {
          console.error("Unable to fetch active conversations");
      }
  },
  
      async fetchChat(wa_id) {
        try {
          const token = localStorage.getItem('token');
          const response = await fetch(`http://localhost:8000/conversations/${wa_id}`, {
            method: "GET",
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
            }
          });
  
          const result = await response.json();
  
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
  
          // Set the initial chat data
          this.selectedchat = result;
  
          // Now set up Server-Sent Events (SSE) for real-time updates
          this.setupSSE(wa_id);
  
        } catch (error) {
          console.error("Unable to fetch conversation data", error);
        }
      },
  
      ConversationSSE(wa_id) {
        // Check if there's an existing EventSource instance
        if (this.eventSource) {
          // Close the previous EventSource connection
          this.eventSource.close();
          console.log("Previous SSE connection closed.");
        }
  
        // Fetch the token
        const token = localStorage.getItem('token');
  
        // Create a new EventSource instance with the new wa_id
        this.eventSource = new EventSource(`http://localhost:8000/sse/conversations/${wa_id}?token=${token}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
  
        // Handle incoming messages
        this.eventSource.onmessage = (event) => {
          try {
            // Parse the new conversations data
            const newConversations = JSON.parse(event.data);
  
            // Determine if the user is already scrolled to the bottom
            const chatContent = this.$refs.chatContent;
            const isAtBottom = chatContent.scrollHeight - chatContent.scrollTop <= chatContent.clientHeight + 10;
  
            this.selectedchat = newConversations;  // Update the UI with the new data
  
            // Only scroll to the bottom if the user is already at (or near) the bottom
            if (isAtBottom) {
              this.scrollToBottom();
            }
          } catch (error) {
            console.error("Error parsing SSE data", error);
          }
        };
  
        // Handle errors
        this.eventSource.onerror = (error) => {
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
  
    }
  
  };
  </script>
  
  
  
  
  
  <style scoped>
  /* Main container layout */
  .main-container {
    display: flex;
    height: 90vh;
    background-color: #f4f4f4;
    font-family: Arial, sans-serif;
    width: 100%;
    margin: -24px;
  }
  
  /* Sidebar styling */
  .sidebar {
    width: 20%;
    background-color:  #ffffff;
    color: #ffffff;
    padding: 15px;
    overflow-y: auto;
   
  }
  
  .sidebar h1 {
    color: #000;
    margin-bottom: 10px;
  }
  .chatType{
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
  
  .chat-list li a {
    text-decoration: none;
    color: #ffffff;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .chat-list li a:hover {
    background-color: #25d366;
    padding: 5px;
    border-radius: 5px;
  }
  
  /* Chat area styling */
  .chat-area {
    flex-grow: 1;
    background-color: #ffffff;
  
    border-left: 1px solid #ccc;
    height: 90vh;
  }
  
  .chat-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px;
    background-color: #f8f9fa;
    width: 100%;
    /* Make sure it occupies the full width of the container */
    max-width: 100%;
    /* Remove any width restrictions if necessary */
    box-sizing: border-box;
    border-bottom: 1px solid #ccc;
    /* Optional: add a bottom border */
    height: 105px;
  }
  
  .chat-header i{
   font-size:20px;
  }
  
  .status {
    color: #4caf50;
    font-weight: bold;
  }
  
  .chat-content {
    height: calc(100vh - 200px);
    overflow-y: auto;
  }
  
  .message {
    margin: 10px 0;
  
  }
  
  
  
  .user-message {
    display: flex;
  
    padding: 10px;
    border-radius: 10px;
    max-width: 70%;
  }
  
  /* Message Input Area */
  .message-input-area {
    display: flex;
    align-items: center;
  }
  
  .message-input-area input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  .message-input-area button {
    margin-left: 10px;
    padding: 10px;
    background-color: #075E54;
    color: rgb(255, 255, 255);
  }
  
  .chat-list li {
    margin-bottom: 15px;
  }
  
  .chat-list a {
    color: #ffffff;
    text-decoration: none;
    padding: 10px;
    display: block;
    background-color: #128C7E;
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
    background-color: #fff;
    border-left: 1px solid #ddd;
  }
  
  .chat-header {
    
    padding: 10px 30px 10px 30px;
    background-color: #075e54;
    color: white;
    text-align: center;
    font-size: 1.5em;
    width: 100%;
  }
  
  /* Style for the select dropdown */
  #userDropdown {
    background-color: #075e54;
    /* Green background */
    color: white;
    /* White text color */
    padding: 1px;
    border: 1px solid #ccc;
    border-radius: 10px;
    width: 30%;
  }
  
  /* Optional: Change text color for options */
  #userDropdown option {
    background-color: #075e54;
    /* Green background for options */
    color: white;
    /* White text color for options */
  }
  
  .status {
    display: block;
    font-size: 0.8em;
    color: #c1c1c1;
    margin-top: 5px;
  }
  
  .chat-content {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
    background-color: #f9f9f9;
  }
  
  .message {
    display: flex;
  justify-content: space-between;
    background-color: #dcf8c6;
    margin-bottom: 10px;
    padding: 10px;
    border-radius: 10px;
    width: fit-content;
    max-width: 60%;
    min-width: 80px;
  }
  
  
  .sent-message {
    display: flex;
  
    background-color: #bef991;
    margin-bottom: 10px;
    align-self: flex-end;
    margin-left: auto;
    padding: 10px;
    border-radius: 10px;
    width: fit-content;
    max-width: 60%;
    
  }
  .messageTime{
    display: flex;
    margin-top: auto;
    align-items: flex-end;
    margin-left: 5px;
  
    font-size: 12px;
    color: #666;
  }
  
  .user-message {
    
    margin: 0;
    font-size: 1em;
  }
  
  /* Timer styling */
  .timer {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 10px;
    /* Space between timer and title */
  }
  
  .timer-circle {
    position: relative;
    width: 50px;
    height: 50px;
  }
  
  .timer-circle span {
    font-size: 0.8em;
    /* Adjusted font size */
    color: #4caf50;
    /* Text color */
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
  
  .status {
    margin-left: auto;
    /* Push status to the right */
  }
  
  .timer i {
    margin-right: 5px;
    color: #FFD700;
    /* Gold color for the icon */
  }
  
  /* Circular progress bar styles */
  .progress-circle {
    stroke: #4caf50;
    stroke-width: 5;
    fill: none;
    transform: rotate(-90deg);
    transform-origin: 50% 50%;
  }
  
  /* Message input area styling */
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
  
  button {
    margin-left: 10px;
    padding: 10px 15px;
    background-color: #25d366;
    /* Change background to a darker color */
    color: rgb(255, 255, 255);
    /* Text color is white */
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #1da857;
    /* Darker green on hover */
  }
  
  
  /* Contact information styling */
  .contact-info {
    width: 30%;
    padding: 20px;
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
    background-color: #128C7E;
    color: white;
    padding: 5px 10px;
    border-radius: 5px;
    margin-bottom: 5px;
    display: inline-block;
  }
  
  .tags ul li button {
    margin-left: 10px;
    background: none;
    border: none;
    color: white;
    cursor: pointer;
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
  
  .contact-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
  }
  
  .contact-table th,
  .contact-table td {
    border: 1px solid #4c4b4b;
    padding: 8px;
    text-align: left;
  }
  
  .contact-table th {
    background-color: #f2f2f2;
  }
  
  .available-text {
    font-size: 12px;
    /* Adjust the size as needed */
    color: #ffffff;
    top: 2px;
    /* Optional: Change color if needed */
  }
  </style>