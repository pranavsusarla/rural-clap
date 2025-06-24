<template>
    <div v-if="!me['is_blocked']">
        <div class="d-flex justify-content-around">
            <h4 class="m-5">Welcome {{ me['email_id'] }}!</h4>
            <h5 class="m-5 text-danger">Your total service requests: {{ my_service_requests.length }}</h5>
            <h5 class="m-5 text-danger">Your closed service requests: {{ closedreqs }}</h5>
        </div>
        <h5 class="text-center text-success m-5">Checkout available services or dive into your service requests!</h5>
    </div>
</template>

<script>
    export default {
        name: 'CustomerHome',
        data(){
            return{
                me: {},
                my_service_requests: {}
            }
        },
        methods:{
            async getme(){
                await fetch('http://127.0.0.1:5000/getme',{
                    method: "GET",
                    headers:{
                        'Authorization': 'Bearer ' + this.$store.state.token,
                        'Access-Control-Allow-Origin': "*"
                    }
                })
                .then(resp => resp.json())
                .then(data => {
                    console.log(data)
                    this.me = data.me;
                    this.my_service_requests = data.my_service_requests
                })
            }
        },
        computed:{
            closedreqs(){
                var cnt = 0;
                for(let i=0; i<this.my_service_requests.length; i++){
                    if(this.my_service_requests[i].service_status == 'closed'){
                        cnt++;
                    }
                }
                return cnt;
            }
        },
        mounted(){
            this.getme();
        }
    }
</script>

<style scoped>

</style>