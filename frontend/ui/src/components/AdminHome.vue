<template>
    <div class="container">
        <div class="navbar justify-content-evenly" v-if="this.$store.state.role == 'admin'">
            <div>
                <router-link to="/admin/home">Welcome to Admin's Dashboard</router-link>
            </div>
            <!-- <button @click="showToken">Show token</button>
            <h3 v-if="token != '' ">{{ token }}</h3> -->
            <div class="justify-content-evenly">
                <button class="btn"><router-link to="/admin/allusers">Manage Users</router-link></button>
                <button class="btn"><router-link to="/admin/services">Manage Services</router-link></button>
                <button class="btn"><router-link to="/admin/requests">Manage Requests</router-link></button>
                <button class="btn btn-primary" @click="generateCSV">Export Service Requests</button>
            </div>
        </div>
        <div v-else>
            {{ this.$router.push('/login') }}
        </div>
        <router-view/>
        <!-- <AddNewService /> -->
    </div>
</template>

<script>
// import AddNewService from './AddNewService.vue';

    export default {
        name: 'AdminHome',
        data(){
            return{
                waiting: false
            }
        },
        methods:{
            async generateCSV(){
                this.waiting = true;
                const res = await fetch('http://127.0.0.1:5000/startcsvrequest')
                const data = await res.json()
                if (res.ok){
                    const task_id = data['task_id']
                    const intv = setInterval(async () => {
                        const csv_res = await fetch(`http://127.0.0.1:5000/getcsvbytaskid?task_id=${task_id}`)
                        if (csv_res.ok){
                            this.waiting = false;
                            clearInterval(intv)
                            window.location.href = `http://127.0.0.1:5000/getcsvbytaskid?task_id=${task_id}`
                        }
                    }, 1000)
                }
            }
        }  
    }
</script>

<style scoped>

</style>
