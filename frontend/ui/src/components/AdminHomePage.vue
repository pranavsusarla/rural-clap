<template>
    <div class="container mt-4">
    <h2 class="mb-4 text-center">Admin Dashboard</h2>
    <div class="row text-center">
      <div class="col-md-3 mb-3">
        <div class="card shadow-sm p-3">
          <h4 class="text-primary">Total Users</h4>
          <h2 class="fw-bold">{{ customers.length + professionals.length }}</h2>
        </div>
      </div>
      <div class="col-md-3 mb-3">
        <div class="card shadow-sm p-3">
          <h4 class="text-primary">Customers</h4>
          <h2 class="fw-bold">{{ customers.length }}</h2>
        </div>
      </div>
      <div class="col-md-3 mb-3">
        <div class="card shadow-sm p-3">
          <h4 class="text-primary">Professionals</h4>
          <h2 class="fw-bold">{{ professionals.length }}</h2>
        </div>
      </div>
      <div class="col-md-3 mb-3">
        <div class="card shadow-sm p-3">
          <h4 class="text-primary">Services</h4>
          <h2 class="fw-bold">{{ services.length }}</h2>
        </div>
      </div>
      <div class="col-md-3 mb-3">
        <div class="card shadow-sm p-3">
          <h4 class="text-primary">Service Requests</h4>
          <h2 class="fw-bold">{{ service_requests.length }}</h2>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
    export default {
        name: 'AdminHomePage',
        data(){
            return{
                customers: [],
                professionals: [],
                services: [],
                service_requests: []
            }
        },
        methods:{
            getme(){
                fetch('http://127.0.0.1:5000/getme',{
                    method: "GET",
                    headers:{
                        'Authorization': 'Bearer ' + this.$store.state.token,
                        'Access-Control-Allow-Origin': '*'
                    }
                })
                .then(resp => resp.json())
                .then(data =>{
                    this.customers = data.customers;
                    this.professionals = data.professionals;
                    this.services = data.services;
                    this.service_requests = data.service_requests;
                })
            }
        },
        mounted(){
            this.getme()
        }
    }
</script>

<style scoped>

</style>