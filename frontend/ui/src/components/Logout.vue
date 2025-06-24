<template>
    <div class="container d-flex justify-content-center">
        <h5 class="m-5">Logged Out Successfully!</h5>
    </div>
</template>

<script>
    export default {
        name: 'LogOut',
        mounted(){
            localStorage.clear()
            this.$store.commit('logoutUser')
        }
    }
</script>

<style scoped>

</style>