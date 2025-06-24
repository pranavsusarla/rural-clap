<template>
    <div v-if="me['is_approved'] && !me['is_blocked']">
        <div class="d-flex justify-content-around">
            <h4 class="m-5">Welcome {{ me['email_id'] }}!</h4>
            <h5 class="m-5 text-success">Your average rating: {{ ratingcalc }}/5</h5>
        </div>
        <br>
        <h5 class="text-center m-5">Checkout your service requests!</h5>
    </div>
</template>

<script>
    export default {
        name: 'ProfessionalHome',
        data(){
            return{
                me: {},
                my_service_requests: {}
            }
        },
        methods:{
            profdata(){
                fetch('http://127.0.0.1:5000/getme',{
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
                    this.my_service_requests = data.my_service_requests;
                    // console.log(typeof this.my_service_requests)
                }
                )
            }
        },
        computed:{
            ratingcalc(){
                // return this.my_service_requests.reduce((sum, item) => sum+item.rating, 0) / this.my_service_requests.length;
                console.log(this.my_service_requests)
                var rating=0;
                var cnt = 0;
                for(let i=0; i<this.my_service_requests.length; i++){
                    rating += this.my_service_requests[i].rating;
                    if(this.my_service_requests[i].rating > 0){
                        cnt++;
                    }
                }
                return rating/cnt || '-';
            }
        },
        mounted(){
            this.profdata();
        }
    }
</script>

<style scoped>

</style>