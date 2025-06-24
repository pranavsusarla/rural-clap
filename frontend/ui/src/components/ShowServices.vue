<template>
    <div class="card m-3">
        <div v-if="!show_update" class="">
          <div class="m-3">
            <h4>Name: {{ service.name }}</h4> 
            <h5>Base Price: {{ service.price }}</h5>
            <h5 v-if="service.time_required <= 1">Time Required: {{ service.time_required }} hour</h5>
            <h5 v-else>Time Required: {{ service.time_required }} hours</h5>
            <p>Description: {{ service.description }}</p>
          </div>
          <button @click="updateService" class="btn btn-success m-3">Update</button>
          <button @click="deleteService" class="btn btn-danger m-3">Delete</button>
        </div>
        <div v-else class="">
          <div class="card m-3">
            <label for="serviceName" class="form-label">Service Name: </label>
            <input type="text" v-model="name" class="form-control">
            <br>
            <label for="description" class="form-label">Description: </label>
            <textarea v-model="description" class="form-control"/>
            <br>
            <label for="basePrice" class="form-label">Base Price: </label>
            <input type="number" v-model="price" class="form-control">
            <br>
            <label for="timeRequired" class="form-label">Time Required (in hours): </label>
            <input type="number" v-model="time_required" class="form-control">
            <br>
            <button @click="emitUpdate" class="btn">Update</button>
            <button @click="this.show_update = !this.show_update" class="btn">Cancel</button>
          </div>
        </div>
    </div>
</template>

<script>
  export default{
    name: 'ShowServices',
    props: ['service'],
    data(){
      return{
        name: this.service.name,
        price: this.service.price,
        time_required: this.service.time_required,
        description: this.service.description,
        show_update: false
      } 
    },
    methods:{
      emitUpdate(){
        console.log(this.service.service_id, this.name, this.price, this.time_required, this.description)
        this.$emit('update-service', this.service.service_id, this.name, this.price, this.time_required, this.description);
        this.name= this.service.name,
        this.price= this.service.price,
        this.time_required= this.service.time_required,
        this.description= this.service.description,
        this.show_update = false;
      },
      updateService(){
        this.show_update = true; 
      },
        deleteService(){
            this.$emit('delete-service', this.service.service_id)
        }
    }
  }
</script>
