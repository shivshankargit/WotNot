<template>
  <div class="content-section">


    <h2>Manage Templates</h2>
    <p>Your content for scheduled broadcasts goes here.</p>
    
    <div class="CreateTemplateContainer">
      <p>Create New Template</p>
      <button >Create Template</button>

    </div>

    <div class="templateList_container">
      <table class="templateList-table">

        <thead>
          <tr>
            <th>Name</th>
            <th>Language</th>
            <th>Status</th>
            <th>Category</th>
            <th>Sub Category</th>
            <th>ID</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="template in templates" :key="template.id">
            <td>{{ template.name }}</td>
            <td>{{ template.language }}</td>
            <td>{{ template.status }}</td>
            <td>{{ template.category }}</td>
            <td>{{ template.sub_category }}</td>
            <td>{{ template.id }}</td>
            <td><button id="TemplatedeleteBtn">Delete</button></td>
            </tr>
        </tbody>
      </table>
    </div>


  </div>
</template>

<script>
export default {
  name: 'BroadCast1',
  data() {
    return {
      templates:[]
    }
  },

  async mounted() {
    await this.fetchtemplateList()  // Fetch contacts when the component is mounted
  },
  
  methods: {
    async fetchtemplateList() {
      const token = localStorage.getItem('token'); 
      try {
        const response = await fetch("http://localhost:8000/template",
          {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
            }
          }
        )

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const templatelist = await response.json();
        this.templates = templatelist.data;
      }
      catch(error){
        console.error("There was an error fetching the templates:", error); 
      }
     }
  }
}
</script>


<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
}

th {
  background-color: #f2f2f2;
}

.CreateTemplateContainer{
  background-color: #f5f6fa;
  border-radius: 12px;
  width: 100%;
  max-width: 1100px;
  padding: 20px;
  display: flex;
  margin-bottom: 20px;
  
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

.CreateTemplateContainer button{
  margin-left: 805px ;
}


.templateList_container{
  background-color: #f5f6fa;
  border-radius: 12px 12px;
  width: 100%;
  padding: 20px;
  margin-bottom: 20px;
  max-width: 1100px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}  

.templateList-table {
  width: 100%;
  border-radius: 12px 12px;
  border-collapse: collapse;
  overflow-x: auto;
  display: block;
  max-height: 400px;
  /* Adjust height as needed */

}

th {
  padding: 20px 43px ;
  text-align: left;
  border-collapse: collapse;
  border: 1px solid #ddd;
 

}

.templateList-table td {
  border: 1px solid #ddd;

  padding: 20px;
  text-align: left;
  border-collapse: collapse;
}

.templateList-table thead th {
  position: sticky;
  top: 0;
  background-color: #dddddd;
  border-collapse: collapse;
  border: 1px solid #ddd;

}

.templateList-table tbody {
  background-color: white;
}

</style>