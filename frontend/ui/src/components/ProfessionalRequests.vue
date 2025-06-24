<template>
  <div class="container">
    <div class="d-flex justify-content-between align-content-center mb-4">
      <input type="text" v-model="professionalname" class="form-control m-2" placeholder="Search without typing anything to get all professionals">
      <button class="btn btn-success m-2" @click="modifyprofessionals">Search</button>
    </div>
  <div v-if="buttonPressed">
    <div v-if="filteredProfos.length !== 0">
      <ExpandableCard 
        v-for="professional in filteredProfos"
        :key="professional.user_id"
        :professional="professional"
        :is_approved="professional.is_approved"
        @approve="approveProfessional"
      />
    </div>
    <div v-else>
      There are no professionals with this name
    </div>
  </div>
  <div v-else-if="profos.length !== 0">
    <div>
      <ExpandableCard 
        v-for="professional in profos"
        :key="professional.user_id"
        :professional="professional"
        :is_approved="professional.is_approved"
        @approve="approveProfessional"
      />
    </div>
  </div>
  <div v-else>
    There are no requests from new professionals!
  </div>
</div>
</template>

<script>
import ExpandableCard from './ExpandableCard.vue';
  export default{
    name: 'ProfessionalRequests',
    components: {ExpandableCard},
    data(){
      return{
        profos: [],
        filteredProfos: [],
        professionalname: '',
        buttonPressed: false
      }
    },
    methods:{
      modifyprofessionals(e){
        e.preventDefault();
        const inputPattern = this.professionalname.trim();
        const regexPattern = inputPattern
        .replace(/%/g, ".*")
        .replace(/_/g, ".");
      
        const regex = new RegExp(`^.*${regexPattern}.*$`, "i");
      
        this.filteredProfos = this.profos.filter(p => regex.test(p.email_id));
        console.log('this is being pressed')
        this.buttonPressed = true;
      },
      approveProfessional(user_id){
        console.log(user_id+" to be approved");
        // backend call here
        const data = {
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            body: JSON.stringify({
                'user_id': user_id
              })
        };
        fetch("http://127.0.0.1:5000/professionalrequests", data)
        .then(resp => resp.json())
        .then(data => {
          console.log(data)
        })
      }
    },
    beforeMount(){
      fetch('http://127.0.0.1:5000/professionalrequests')
      .then(resp => resp.json())
      .then(data => {
        if(data.message=="Got requests"){
          this.profos = data.professionals;
          // console.log(this.profos);
        }
      })
    }
  }
</script>
