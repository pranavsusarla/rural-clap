<template>
    <div class="container d-flex justify-content-center">
        <div class="w-50  border px-3 rounded" style="background-color: aliceblue;">
            <div class="d-flex justify-content-evenly">
                <label for="" class="form-label">Register as: </label>
                <div>
                    <input class="form-check-input m-1 p-1" type="radio" id="customer" value="customer" v-model="role" checked="checked"/>
                    <label class="form-check-label" for="admin">Customer</label>
                </div>
                <div>
                    <input class="form-check-input m-1 p-1" type="radio" id="professional" value="professional" v-model="role" />
                    <label class="form-check-label" for="professional">Professional</label>
                </div>
            </div>
            <br>
            <div v-if="role == 'customer'">
                <label class="form-label" for="emailId" name="emailId">Email ID: </label>
                <input class="form-control" type="text" name="emailId" v-model="emailId">
                <br>
                <label class="form-label" for="password" name="password">Password: </label>
                <input class="form-control" type="password" name="password" v-model="password">
                <br>
                <label class="form-label" for="address" name="address">Address: </label>
                <input class="form-control" type="text" name="address" v-model="address">
                <br>
                <label class="form-label" for="number" name="number">Phone Number: </label>
                <input class="form-control" type="number" name="number" v-model="phone_number">
                <br>
                <button class="btn btn-success w-100" @click="submitCustomer">Register as Customer</button>
            </div>
            <div v-else>
                <div v-if="availableServices.length !== 0">
                    <label class="form-label" for="emailId" name="emailId">Email ID: </label>
                    <input class="form-control" type="text" name="emailId" v-model="emailId">
                    <br>
                    <label class="form-label" for="password" name="password">Password: </label>
                    <input class="form-control" type="password" name="password" v-model="password">
                    <br>
                    <label for="">Service Type</label>
                    <select class="form-select" v-model="service_type">
                        <option v-for="service in availableServices" :key="service.id" :value="service.name">{{ service.name }}</option>
                    </select>
                    <br>
                    <label class="form-label" for="experience" name="experience">Experience (in years): </label>
                    <input class="form-control" type="number" name="experience" v-model="experience">
                    <br>
                    <button class="btn btn-success w-100" @click="submitProfessional">Register as Professional</button>
                </div>
                <div v-else>
                    The admin has not created any services yet. Please wait for them to create services :)
                </div>
            </div>
            <h3 style="color: red">{{ error }}</h3>
            <h3 style="color: green">{{ professional_message }}</h3>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'RegisterPeople',
        data(){
            return{
                role: 'customer',
                emailId: '',
                password: '',
                address: '',
                phone_number: '',
                service_type: '',
                availableServices: [],
                experience: '',
                error: '',
                professional_message: ''
            }
        },
        methods:{
            submitCustomer(e){
                e.preventDefault();
                console.log("clicked submit customer")
                const data = {
                    method: "POST",
                    headers: { 
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*"
                    },
                    body: JSON.stringify({
                        'emailId': this.emailId,
                        'password': this.password,
                        'role': this.role,
                        'address': this.address,
                        'phone_number': this.phone_number
                     })
                };
                console.log("data created")
                fetch("http://127.0.0.1:5000/register", data)
                .then(resp => resp.json())
                .then(data => {
                    console.log("data recieved")
                    if(data.message == 'User created'){
                        this.error = ''
                        this.$router.push('/login')
                    }else{
                        this.error = data.message
                    }
                })
            },
            submitProfessional(e){
                e.preventDefault();
                const data = {
                    method: "POST",
                    headers: { 
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*"
                    },
                    body: JSON.stringify({
                        'emailId': this.emailId,
                        'password': this.password,
                        'role': this.role,
                        'service_type': this.service_type,
                        'experience': this.experience
                     })
                };
                fetch("http://127.0.0.1:5000/register", data)
                .then(resp => resp.json())
                .then(data => {
                    if(data.message == 'User created'){
                        this.error = ''
                        this.professional_message = "You will be able to login once the admin approves your profile"
                        // this.$router.push('/login')
                    }else{
                        this.error = data.message
                    }
                })
            }
        },
        mounted(){
            fetch('http://127.0.0.1:5000/getservices', {
                method: "POST",
                    headers:{
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        'serviceName': ""
                    })
            })
            .then(resp => resp.json())
            .then(data => {
                this.availableServices = data.services;
                console.log('available services: ', this.availableServices);
            })
        }
    }
</script>

<style scoped>

</style>