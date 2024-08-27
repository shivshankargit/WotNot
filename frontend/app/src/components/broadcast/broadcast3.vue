<template>
    <div class="content-section">
    
        <h2>Scheduled Broadcasts</h2>
        <p>Your content for scheduled broadcasts goes here.</p>

        <h3>Broadcast list</h3>
    <div class="broadcastListContainer">

      <table class="broadcastList-table">
        <thead>
          <tr>
            <th>id</th>
            <th>Broadcast Name</th>
            <th>Template</th>
            <th>Contacts</th>
            <th>Success</th>
            <th>Failed</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>

          <tr v-for="broadcast in broadcasts" :key="broadcast.id">
            <td>{{ broadcast.id }}</td>
            <td>{{ broadcast.name }}</td>
            <td>{{ broadcast.template }}</td>
            <td>{{ broadcast.contacts }}</td>
            <td>{{ broadcast.success }}</td>
            <td>{{ broadcast.failed }}</td>
            <td>{{ broadcast.status }}</td>
            <td><button class="deleteBroadcast" @click="DeleteScheduledBroadcast(broadcast.id)">Delete</button></td>
          </tr>

        </tbody>
      </table>
    </div>
          
    </div>
  </template>
  
  <script>
  export default {
    name: 'BroadCast3',
    data() {
      return{
        broadcasts: [],

      }
     
    },
    async mounted() {
    
    await this.fetchScheduledBroadcastList();

    // Fetch contacts when the component is mounted
  },
    methods: {

      async fetchScheduledBroadcastList() {
      const token = localStorage.getItem('token');
      try {
        const response = await fetch('http://localhost:8000/scheduled-broadcast/', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const ScheduledbroadcastList = await response.json();
        this.broadcasts = ScheduledbroadcastList.map(broadcast => ({
          id: broadcast.id,
          name: broadcast.name,
          template: broadcast.template,
          contacts: broadcast.contacts,
          success: broadcast.success,
          failed: broadcast.failed,
          status: broadcast.status

        }));
      } catch (error) {
        console.error('Error fetching scheduled-broadcastlist:', error);
      }
    },

    async DeleteScheduledBroadcast(broadcast_id){
      const token = localStorage.getItem('token');
      try {
        
        const response = await fetch(`http://localhost:8000/broadcasts-delete/${broadcast_id}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        
        this.fetchScheduledBroadcastList();


      } catch (error) {
        console.error('Error fetching contacts:', error);
      }
    },
      
    }
  }
  </script>
  
  <style>
.NeWBroadcastButtonContainer {
  background-color: #f5f6fa;
  border-radius: 12px;
  width: 100%;
  max-width: 1100px;
  padding: 20px;
  display: flex;
  margin-bottom: 20px;

  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

.NeWBroadcastButtonContainer button {
  margin-left: 725px;

}

.broadcastListContainer {
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

.broadcastList-table {
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

.broadcastList-table td {
  border: 1px solid #ddd;

  padding: 20px;
  text-align: left;
  border-collapse: collapse;
}

.broadcastList-table thead th {
  position: sticky;
  top: 0;
  background-color: #dddddd;
  border-collapse: collapse;
  border: 1px solid #ddd;

}

.broadcastList-table tbody {
  background-color: white;
}

.CSVimportContainer {
  display: flex;
  align-items: center;

}

.CSVimportContainer a {
  padding-left: 10px;
}

.CSVimportContainer input {
  max-width: 200px;
  margin-top: 20px;
  margin-left: 10px;
}

.CSVimportContainer button {
  margin-left: 10px;
  height: 35px;
}


#response {
  margin-top: 20px;
  font-size: 16px;
  color: #333;
}

.contact-table {
  width: auto;

  border-collapse: collapse;
  overflow-x: auto;
  display: block;
  max-height: 200px;
  /* Adjust height as needed */

  margin-bottom: 20px;
}


.contact-table td {
  padding: 15px;
  text-align: left;
  border-collapse: collapse;
  background-color: #ffffff;
}

.contact-table th {
  padding: 15px;
  text-align: left;
  border-collapse: collapse;
}


.contact-table thead th {
  position: sticky;
  top: 0;
  background-color: #dddddd;
  border-collapse: collapse;
}
</style>

  