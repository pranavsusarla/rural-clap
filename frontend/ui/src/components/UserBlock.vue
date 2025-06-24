<template>
    <div class="m-2 p-2 d-flex justify-content-evenly align-content-evenly border bg-light">
        <p class="m-1 p-1">{{ user.email_id }}</p>
        <button class="btn btn-success" v-if="this.is_blocked" @click="updateUserStatus">Unblock</button>
        <button class="btn btn-danger" v-else @click="updateUserStatus">Block</button>
    </div>
</template>

<script>
    export default {
        name: 'UserBlock',
        props: ['user'],
        data(){
            return{
                user_id: this.user.user_id,
                is_blocked: this.user.is_blocked
            }
        },
        methods:{
            updateUserStatus(){
                this.$emit('bub', this.user_id, this.is_blocked)
                this.is_blocked = !this.is_blocked
            }
        }
    }
</script>

<style scoped>

</style>