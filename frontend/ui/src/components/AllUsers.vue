<template>
    <div>
        <div class="d-flex justify-content-between align-content-center mb-4">
            <input type="text" v-model="username" class="form-control m-2" placeholder="Search without typing anything to get all users">
            <button class="btn btn-success m-2" @click="getUsersBySearch">Search</button>
        </div>
        <div class="container d-flex justify-content-center">
            <h3 style="color: red">{{ error }}</h3>

            <div class="m-2 p-2 border">
                Customers:
                <div v-if="customers.length != 0">
                    <UserBlock 
                        v-for="customer in customers" 
                        :key="customer.user_id" 
                        :user="customer" 
                        @bub="updateUserStatus"
                    />
                </div>
                <div v-else>
                    <p>Therr are no customers with that email id</p>
                </div>
            </div>
            <div class="m-2 p-2 border">
                Professionals:
                <div v-if="professionals.length != 0">
                    <UserBlock 
                        v-for="professional in professionals" 
                        :key="professional.user_id" 
                        :user="professional" 
                        @bub="updateUserStatus" 
                    />
                </div>
                <div v-else>
                    <p>There are no professionals with that email id</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import UserBlock from './UserBlock.vue';

    export default {
        name: 'AllUsers',
        components: {UserBlock},
        data(){
            return {
                username: '',
                customers: [],
                professionals: [],
                error: ''
            }
        },
        methods:{
            getUsersBySearch(e){
                e.preventDefault();
                fetch('http://127.0.0.1:5000/getusersbysearch', {
                    method: "POST",
                    headers:{
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        'username': this.username
                    })
                })
                .then(resp => resp.json())
                .then(data => {
                    this.customers = data.customers;
                    this.professionals = data.professionals;
                })
            },
            updateUserStatus(user_id, is_blocked){
                console.log("Parent: ", user_id, is_blocked);
                fetch('http://127.0.0.1:5000/getUsers', {
                    method: "POST",
                    headers:{
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        'user_id': user_id,
                        'is_blocked': !is_blocked
                    })
                })
                .then(resp => resp.json())
                .then(data =>{
                    if(data.message=="Success"){
                        console.log("User blocked/unblocked successfully");
                    }else{
                        console.log(data.message);
                    }
                })
            }
        },
        mounted(){
            fetch("http://127.0.0.1:5000/getUsers")
            .then(resp => resp.json())
            .then(data => {
                if(data.message == "Successful"){
                    this.customers = data.customers
                    this.professionals = data.professionals
                }else{
                    this.error = data.message
                }
            })
        }
    }
</script>

<style scoped>

</style>
