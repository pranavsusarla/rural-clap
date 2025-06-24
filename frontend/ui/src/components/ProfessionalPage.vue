<template>
    <div class="container">
        <!-- Is approved flag: {{ isapproved_flag }} -->
    <div v-if="!isapproved_flag">
        {{ error }}
    </div>
    <div v-else-if="this.$store.state.is_logged_in && this.$store.state.role=='professional' && !this.$store.state.is_blocked" class="d-flex justify-content-evenly">
        <div>
            <button class="btn"><router-link to='/professional/home'>Professional Page</router-link></button>
        </div>
        <div>
            <button class="btn"><router-link to='/professional/myservicerequests'>My Service Requests</router-link></button>
        </div>
    </div>
    <div v-else-if="this.$store.state.is_blocked">
        You have been blocked by the admin.
    </div>
    <div v-else>
        <div v-if="this.$store.state.role=='admin'">
            {{ this.$router.push('/admin') }}
        </div>
        <div v-if="this.$store.state.role=='customer'">
            {{ this.$router.push('/customer') }}
        </div>
        <div v-else>
            {{ this.$router.push('/login') }}
        </div>
    </div>
    <router-view></router-view>
</div>
</template>

<script>
    export default {
        name: 'ProfessionalPage',
        data(){
            return{
                isapproved_flag: false,
                error: ''
            }
        },
        beforeMount(){
            fetch('http://127.0.0.1:5000/isaccepted', {
                method: "GET",
                headers:{
                    "Authorization": "Bearer " + this.$store.state.token,
                    "Access-Control-Allow-Origin": "*"
                }
            })
            .then(resp => resp.json())
            .then(data =>{
                if(data.message == "Approved"){
                    this.isapproved_flag = true;
                }else{
                    this.error = data.message;
                }
            })
        }
    }
</script>

<style scoped>

</style>
