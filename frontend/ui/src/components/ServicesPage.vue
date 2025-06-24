<template>
    <div class="container d-flex justify-content-center">
        <div v-if="!areyousure">
        <button @click="getServices" class="btn">Refresh page</button>
        <button class="btn"><router-link to="/admin/services/addnewservice">Add New Service</router-link></button>
        <!-- {{ services }} -->
        <div class="d-flex justify-content-center">
        <div>
            <!-- class="row row-cols-2 row-cols-md-4"> -->
        <ShowServices 
            v-for="service in services"
            :key="service.service_id"
            @update-service="updateService"
            @delete-service="areyousurefn"
            :service="service"
            class="col"
        />
        </div>
        </div>
        </div>
        <div v-else>
            <button @click="deleteService" class="btn btn-danger">Are you sure you want to delete this service?</button>
        </div>
        <router-view />
    </div>
</template>

<script>
    import ShowServices from '@/components/ShowServices.vue'
    export default {
        name: 'ServicesPage',
        components: {ShowServices},
        data(){
            return{
                services: [],
                areyousure: false,
                service_id: 0,
                re_render: 0
            }
        },
        methods:{
            getServices(){
                fetch('http://127.0.0.1:5000/getservices',{
                    method: "POST",
                    headers:{
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        'serviceName': ""
                    })
                })
                .then(resp => resp.json())
                .then(data =>{
                    this.services = data.services
                })
            },
            areyousurefn(id){
                this.areyousure = true;
                this.service_id = id;
            },
            updateService(service_id, name, price, time, description){
                console.log("Is this even working?: ", service_id, name, price, time, description)
                fetch("http://127.0.0.1:5000/updateservice",{
                    method: "POST",
                    headers:{
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        'service_id': service_id,
                        'name': name,
                        'price': price,
                        'time_required': time,
                        'description': description
                    })
                })
                .then(resp => resp.json())
                .then(data => {
                    console.log(data);
                })
                this.getServices();
                this.re_render++;
                // this.$router.push('/admin/services')
            },
            deleteService(){
                this.areyousure = false;
                fetch("http://127.0.0.1:5000/deleteservice", {
                    method: "POST",
                    headers:{
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        "service_id": this.service_id
                    })
                })
                .then(resp => resp.json())
                .then(data => {
                    console.log(data);
                })
                this.service_id = 0;
                this.getServices();
                // this.re_render++;
                // this.$router.push('/admin/services')
            }
        },
        mounted(){
            this.getServices();
        },
    }
</script>

<style scoped>

</style>
