<template>
    <div class="container d-flex justify-content-center">
        <div class="w-50 border px-3 rounded" style="background-color: aliceblue;">
            <br>
            <label class="form-label" for="emailId" name="emailId">Registered Email ID: </label>
            <input class="form-control" type="text" name="emailId" v-model="emailId">
            <br>
            <label class="form-label" for="password" name="password">Password: </label>
            <input class="form-control" type="password" name="password" v-model="password">
            <br>
            <div class="d-flex justify-content-evenly">
                <div>
                    <input class="form-check-input m-1 p-1" type="radio" id="admin" value="admin" v-model="role" checked="checked"/>
                    <label class="form-check-label" for="admin">Admin</label>
                </div>
                <div>
                    <input class="form-check-input m-1 p-1" type="radio" id="customer" value="customer" v-model="role" />
                    <label class="form-check-label" for="admin">Customer</label>
                </div>
                <div>
                    <input class="form-check-input m-1 p-1" type="radio" id="professional" value="professional" v-model="role" />
                    <label class="form-check-label" for="professional">Professional</label>
                </div>    
            </div>
            <br>
            <button class="btn btn-success w-100 mt-3" @click="submitLogin">Login</button>
            <h3 style="color: red">{{ error }}</h3>
            <br>
            <button class="btn w-100"><router-link to="/register">Create Account?</router-link></button>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'LoginPage',
        data(){
            return{
                emailId: '',
                password: '',
                role: 'admin',
                error: ''
            }
        },
        methods:{
            submitLogin(e){
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
                        'role': this.role
                     })
                };
                fetch("http://127.0.0.1:5000/login", data)
                .then(resp => resp.json())
                .then(d => {
                    // console.log("data: ", d);
                    if(d.message == "Login Successful"){
                        this.error = ''
                        // console.log(d.token);
                        // console.log(d);
                        this.$store.commit('loginUser', {"role": this.role, "token": d.token, "is_blocked": d.is_blocked});
                        localStorage.token = d.token;
                        if(this.role == "admin"){
                            this.$router.push('/admin/home')
                        }else if(this.role == "customer"){
                            this.$router.push('/customer/home')
                        }else{
                            this.$router.push('/professional/home')
                        }
                    }else{
                        this.error = d.message;
                    }
                })
                console.log("Frontend: "+this.emailId, this.password, this.role)
            }
        }
    }
</script>

<style>

</style>