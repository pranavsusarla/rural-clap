<template>
    <div>
        <h4 class="text-center">My Service Requests</h4>
        <div v-if="prof_ser_reqs.length != 0">
            <ul class="list-group">
                <li
                    v-for="request in prof_ser_reqs"    
                    :key="request.id"
                    class="list-group-item d-flex justify-content-between align-items-center mt-3 mb-3"
                >
                <div>
                    <h5><strong>Service Request</strong> #{{ request.service_request_id }}</h5>
                    <p><strong>Date:</strong> {{ request.date_of_request }}</p>
                    <p><strong>Price:</strong> ₹{{ request.price }}</p>
                    <p><strong>Status:</strong> {{ request.service_status }}</p>
                    <p v-if="request.rating != 0" class="card-text"><strong>Rating: </strong><i v-for="star in 5" :key="star" :class="['fa', 'fa-star', star <= request.rating ? 'text-warning' : 'text-secondary']"></i></p>
                    <p v-if="request.remarks"><strong>Remarks:</strong> {{ request.remarks }}</p>
                </div>
                <div v-if="request.service_status == 'open'">
                    <button class="btn btn-success me-2" @click="acceptRequest(request.service_request_id)">Accept</button>
                    <button class="btn btn-danger" @click="rejectRequest(request.service_request_id)">Reject</button>
                </div>
                </li>
            </ul>
        </div>
        <div v-else>
            You don't have any service requests from customers
        </div>
    </div>
</template>

<script>
    export default {
        name: 'ProfServiceRequest',
        data(){
            return{
                prof_ser_reqs: []
            }
        },
        methods:{
            getserreqs(){
                fetch('http://127.0.0.1:5000/getprofserreqs',{
                    method: "GET",
                    headers:{
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                        'Authorization': 'Bearer ' + this.$store.state.token
                    }
                })
                .then(resp => resp.json())
                .then(data =>{
                    this.prof_ser_reqs = data.prof_ser_reqs;
                })
            },
            acceptRequest(id){
                fetch(`http://127.0.0.1:5000/request?id=${id}&type=accept`)
                .then(resp => resp.json())
                .then(data =>{
                    alert(data.message);
                })
            },
            rejectRequest(id){
                fetch(`http://127.0.0.1:5000/request?id=${id}&type=reject`)
                .then(resp => resp.json())
                .then(data =>{
                    alert(data.message);
                })
            }
        },
        mounted(){
            this.getserreqs();
        }
    }
</script>

<style scoped>

</style>