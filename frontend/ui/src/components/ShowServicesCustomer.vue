<template>
    <div class="card m-1">
        <p class="text-success">{{ message }}</p>
        <div class="">
          <div class="">
            <h5>Name: {{ service.name }}</h5> 
            <h6>Base Price: {{ service.price }}</h6>
            <h6 v-if="service.time_required <= 1">Time Required: {{ service.time_required }} hour</h6>
            <h6 v-else>Time Required: {{ service.time_required }} hours</h6>
            <p>Description: {{ service.description }}</p>
            <div v-if="click_service">
              <div v-if="profos.length !== 0">
                <label for="startDate">Date for service:</label>
                <input id="startDate" class="form-control" type="date" v-model="date" />

                <label>Available Professionals:</label>
                <ul class="list-group">
                  <li v-for="profo in profos" :key="profo.id" class="list-group-item d-flex justify-content-between align-items-center">
                    <div>
                      <strong>Name:</strong> {{ profo.email_id }} <br>
                      <strong>Experience:</strong> {{ profo.experience }} years
                    </div>
                    <button class="btn btn-success" @click="requestService(profo.user_id)">Request Service</button>
                  </li>
                </ul>
              </div>

              <div v-else>
                <h5 class="text-danger">No professionals available :(</h5>
              </div>
            </div>
          </div>
          <div>
            <button class="btn btn-success mb-2" @click="selectService">Select Service</button>
          </div>
        </div>
    </div>
</template>

<script>
  export default{
    name: 'ShowServicesCustomer',
    props: ['service'],
    data(){
      return{
        name: this.service.name,
        price: this.service.price,
        time_required: this.service.time_required,
        description: this.service.description,
        profos: [],
        professional_id: '',
        message: '',
        date: '',
        // show_update: false
        click_service: false
      } 
    },
    methods:{
      selectService(){
        // this.$emit('bookService', this.service.service_id);
        this.click_service = true;
        fetch('http://127.0.0.1:5000/getUsers')
        .then(resp => resp.json())
        .then(data => {
          const inputPattern = this.name.trim();
          const regexPattern = inputPattern
          .replace(/%/g, ".*")
          .replace(/_/g, ".");

          console.log('data.p: ', data.professionals);
        
          const regex = new RegExp(`^.*${regexPattern}.*$`, "i");
        
          this.profos = data.professionals.filter(pr => regex.test(pr.service_type));

          this.profos = this.profos.filter(profo => (profo.is_approved & !profo.is_blocked))
        })
      },
      requestService(id){
        console.log(this.date, this.service.service_id, id);
        this.$emit('requestService', this.date, this.service.service_id, id);
        this.click_service = false;
        this.message = "You have requested the service successfully!"
      }
    }
  }
</script>
