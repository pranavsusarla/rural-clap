<template>
    <div class="container">
    <div v-if="this.$store.state.is_logged_in && this.$store.state.role=='customer' && !this.$store.state.is_blocked" class="d-flex justify-content-evenly">
        <div>
            <button class="btn"><router-link to='/customer/home'>Customer Page</router-link></button>
        </div>
        <div>
            <button class="btn"><router-link to='/customer/searchservices'>Search Services</router-link></button>
            <button class="btn"><router-link to='/customer/myservicerequests'>My Service Requests</router-link></button>
        </div>
        <!-- Put previous requests here -->
    </div>
    <div v-else-if="this.$store.state.is_blocked">
        You have been blocked by the admin.
    </div>
    <div v-else>
        <div v-if="this.$store.state.role=='admin'">
            {{ this.$router.push('/admin') }}
        </div>
        <div v-if="this.$store.state.role=='professional'">
            {{ this.$router.push('/professional') }}
        </div>
        <div v-else>
            {{ this.$router.push('/login') }}
        </div>
    </div>
    <router-view />
</div>
</template>

<script>
    export default {
        name: 'CustomerPage'
    }
</script>

<style scoped>

</style>
