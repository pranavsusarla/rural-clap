<template>
  <div class="card">
    <!-- Card Header -->
    <div class="card-header" @click="toggleExpand">
      <h6 class="m-1 p-1">{{ professional.email_id }}</h6>
      <button class="toggle-button">{{ expanded ? "Collapse" : "Expand" }}</button>
    </div>

    <!-- Card Body (Expanded Content) -->
    <div v-if="expanded" class="card-body">
      <p><strong>User ID:</strong> {{ professional.user_id }}</p>
      <p><strong>Service Type:</strong> {{ professional.service_type }}</p>
      <p><strong>Experience:</strong> {{ professional.experience }} years</p>
      <button v-if="!clickedbutton" class="approve-button" @click="approveProfessional">Approve</button>
      <button v-if="clickedbutton" class="approve-button" disabled>Done</button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    professional: {
      type: Object,
      required: true,
    },
    is_approved: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      expanded: false, // Controls expansion
      clickedbutton: false
    };
  },
  methods: {
    toggleExpand() {
      this.expanded = !this.expanded;
    },
    approveProfessional() {
      // Handle the approve button logic here
      this.clickedbutton = true;
      this.$emit("approve", this.professional.user_id); // Emit event with user_id
    },
  },
};
</script>

<style scoped>
.card {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 15px;
  margin: 10px 0;
  background-color: #f9f9f9;
  cursor: pointer;
  max-width: 400px;
  transition: box-shadow 0.3s ease;
}

.card:hover {
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.toggle-button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 3px;
  cursor: pointer;
}

.toggle-button:hover {
  background-color: #0056b3;
}

.card-body {
  margin-top: 10px;
}

.approve-button {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 3px;
  cursor: pointer;
}

.approve-button:hover {
  background-color: #218838;
}
</style>
