<template>
    <div class="container d-flex justify-content-center">
        <div class="w-50">
            <label for="serviceName" class="form-label">Service Name: </label>
            <input type="text" v-model="name" class="form-control">
            <br>
            <label for="description" class="form-label">Description: </label>
            <textarea v-model="description" class="form-control" />
            <br>
            <label for="basePrice" class="form-label">Base Price: </label>
            <input type="number" v-model="base_price" class="form-control">
            <br>
            <label for="timeRequired" class="form-label">Time Required (in hours): </label>
            <input type="number" v-model="time_required" class="form-control">
            <br>
            <button @click="addservice" class="btn">Add</button>
            <button class="btn"><router-link to="/admin/services">Cancel</router-link></button>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'AddNewService',
        data(){
            return{
                name: '',
                description: '',
                base_price: 0,
                time_required: 0
            }
        },
        methods:{
            addservice(){
                fetch('http://127.0.0.1:5000/addservice', {
                    method: "POST",
                    headers:{
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        'name': this.name,
                        'description': this.description,
                        'base_price': this.base_price,
                        'time_required': this.time_required
                    })
                })
                .then(resp => resp.json())
                .then(data => {
                    console.log(data)
                })
                this.$router.push('/admin/services')
            }
        }
    }
</script>

<style scoped>

</style>