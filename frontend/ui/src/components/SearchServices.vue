<template>
    <div class="container mt-5">
        <div class="d-flex justify-content-between align-content-center mb-4">
            <!-- <label for="serviceName" class="form-label m-2">Search for services: </label> -->
            <input type="text" v-model="serviceName" class="form-control m-2" placeholder="Search without typing anything to get all services">
            <button class="btn btn-success m-2" @click="getServices">Search</button>
        </div>
        <div class="col">
            <div class="row row-cols-1 row-cols-md-2 g-4 justify-content-center">
                <ShowServicesCustomer 
                    v-for="service in services"
                    :key="service.service_id"
                    @requestService="bookService"
                    :service="service"
                    class="col"
                />
            </div>
        </div>
        <div class="d-flex justify-content-center">
            <h6 class="text-success mt-5">{{ message }}</h6>
        </div>
    </div>
</template>

<script>
import ShowServicesCustomer from './ShowServicesCustomer.vue';

    export default {
        name: 'SearchServices',
        components: {ShowServicesCustomer},
        data(){
            return{
                serviceName: '',
                services: [],
                message: ''
            }
        },
        methods:{
            bookService(date, service_id, professional_id){
                fetch('http://127.0.0.1:5000/bookservice',{
                    method: "POST",
                    mode: "cors",
                    headers:{
                        'Content-Type': 'application/json',
                        "Authorization": "Bearer " + this.$store.state.token,
                        'Access-Control-Allow-Origin': "*"
                    },
                    body: JSON.stringify({
                        "date": date,
                        "service_id": service_id,
                        "professional_id": professional_id
                    })
                })
                .then(resp => resp.json())
                .then(data => {
                    console.log("Data after booking service: ", data);
                })
                .catch(e => console.log(e))
            },
            getServices(e){{
                e.preventDefault();
                console.log(this.serviceName);
                // get services here
                fetch('http://127.0.0.1:5000/getservices', {
                    method: "POST",
                    headers:{
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        'serviceName': this.serviceName
                    })
                })
                .then(resp => resp.json())
                .then(data => {
                    this.services = data.services;
                    console.log(this.services);
                    if(this.services.length == 0){
                        this.message = 'Hmm.. this service is not available. Try searching for another service :)';
                    }else{
                        this.message = '';
                }
                })
            }}
        }
    }
</script>

<style scoped>

</style>