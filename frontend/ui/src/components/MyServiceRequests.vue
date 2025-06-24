<template>
    <div class="container mt-4">
      <h2>Your Service Requests</h2>
      <div v-if="serviceRequests.length === 0">No service requests found.</div>

      <div class="row">
        <div v-for="request in serviceRequests" :key="request.service_request_id" class="col-md-4">
          <div class="card mb-3">
            <div class="card-body">
              <span v-if="message !== ''"><h5 class="text-danger">{{ message }}</h5></span>
              <h5 class="card-title">Service Name: {{ services.find(s => s.service_id === request.service_id).name }}</h5>
              <p class="card-text"><strong>Requested for:</strong> {{ request.date_of_request }}</p>
              <p class="card-text" v-if="request.service_status != 'rejected'"><strong>Status:</strong> <span class="text-success">{{ request.service_status }}</span></p>
              <p class="card_text" v-else><strong>Status:</strong> <span class="text-danger">{{ request.service_status }}</span></p>
              <p class="card-text"><strong>Professional ID:</strong> {{ request.professional_id }}</p>
              <div v-if="request.service_status != 'rejected'">
                <p v-if="request.rating != 0" class="card-text"><strong>Rating: </strong><i v-for="star in 5" :key="star" :class="['fa', 'fa-star', star <= request.rating ? 'text-warning' : 'text-secondary']"></i></p>
                <p v-if="request.remarks" class="card-text"><strong>Remarks:</strong> {{ request.remarks }}</p>
                <div v-if="request.service_status === 'accepted'">
                    <button class="btn me-2 btn-success" @click="closeRequest(request.service_request_id)">Close Request</button>
                </div>
                <div v-else-if="request.service_status == 'closed'">
                    <div v-if="!request.remarks"><button class="btn btn-primary me-2" @click="openReviewModal(request)">Add Remarks</button></div>
                    <div v-else><button class="btn btn-primary me-2" @click="openReviewModal(request)">Edit Remarks</button></div>
                </div>
                <div v-else>
                    <button class="btn btn-primary me-2" @click="editRequest(request)">Edit</button>
                    <button class="btn btn-danger me-2" @click="deleteRequest(request.service_request_id)">Delete</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- For modal to review -->
      <div v-if="showModal" class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add Remarks</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>

          <div class="modal-body">
            <p><strong>Service:</strong> {{ selectedRequest.serviceName }}</p>
            <p><strong>Date Requested:</strong> {{ selectedRequest.date_of_request }}</p>
            <p><strong>Professional ID:</strong> {{ selectedRequest.professional_id }}</p>

            <!-- Star Rating -->
            <div class="mb-3">
              <strong>Rating:</strong>
              <div>
                <i v-for="star in 5" :key="star" class="fa fa-star star" 
                   :class="{ selected: star <= selectedRating }"
                   @click="setRating(star)">
                </i>
              </div>
            </div>

            <!-- Remarks Box -->
            <textarea v-model="remarks" class="form-control" rows="3" placeholder="Add your remarks..."></textarea>
          </div>

          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeModal">Cancel</button>
            <button class="btn btn-success" @click="submitReview">Submit</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Backdrop -->
    <div v-if="showModal" class="modal-backdrop fade show"></div>

    <!-- for date edit -->
    <div v-if="showDateModal" class="modal fade show d-block" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Edit Date</h5>
                    <button type="button" class="btn-close" @click="closeDateModal"></button>
                </div>
                <div class="modal-body">
                    <p><strong>Service:</strong> {{ selectedRequest.serviceName }}</p>
                    <p><strong>Professional ID:</strong> {{ selectedRequest.professional_id }}</p>
                    <p><strong>New Date: </strong></p>
                    <input id="startDate" class="form-control" type="date" v-model="date" />
                </div>
                <div class="modal-footer">
                    <button class="btn btn-secondary" @click="closeDateModal">Cancel</button>
                    <button class="btn btn-success" @click="submitDate">Submit</button>
                </div>
            </div>
        </div>
    </div>
    <div v-if="showDateModal" class="modal-backdrop fade show"></div>
    </div>
  </template>

<script>
    export default {
        name: 'MyServiceRequests',
        data(){
            return{
                serviceRequests: [],
                services: [],
                professionals: [],
                message: '',
                remarks: '',
                showModal: false,
                selectedRequest: {},
                selectedRating: 0,
                date: '',
                showDateModal: false
            }
        },
        methods:{
            async fetchServiceRequests() {
                try {
                    // Fetch services
                    const serviceResponse = await fetch('http://127.0.0.1:5000/getservices', {
                        method: "POST",
                        headers: {
                            'Authorization': 'Bearer ' + this.$store.state.token,
                            'Access-Control-Allow-Origin': "*",
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            serviceName: ''
                        })
                    });

                    const serviceData = await serviceResponse.json();
                    this.services = serviceData.services;

                    // Fetch service requests
                    const requestResponse = await fetch('http://127.0.0.1:5000/bookservice', {
                        method: "GET",
                        headers: {
                            'Authorization': 'Bearer ' + this.$store.state.token,
                            'Access-Control-Allow-Origin': "*"
                        }
                    });

                    const requestData = await requestResponse.json();
                    this.serviceRequests = requestData.service_requests;

                } catch (error) {
                    console.error("Error fetching service requests:", error);
                }
            },
            deleteRequest(id){
                console.log(id, ': service req to be deleted')
                fetch('http://127.0.0.1:5000/deleteservicerequest', {
                    method: "POST",
                    headers: {
                        'Access-Control-Allow-Origin': "*",
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        'id': id
                    })
                })
                .then(resp => resp.json())
                .then(data => {
                    console.log(data);
                    alert(data.message);
                })
            },
            closeRequest(id){
                fetch(`http://127.0.0.1:5000/request?id=${id}&type=close`)
                .then(resp => resp.json())
                .then(data => alert(data.message))
            },
            openReviewModal(request){
                this.selectedRequest = {
                    serviceName: this.services.find(s => s.service_id === request.service_id).name,
                    date_of_request: request.date_of_request,
                    professional_id: request.professional_id,
                    service_request_id: request.service_request_id,
                    rating: request.rating,
                    remarks: request.remarks
                }
                this.showModal = true;
            },
            setRating(value){
                this.selectedRating = value;
            },
            closeModal(){
                this.showModal = false;
                this.remarks = '';
                this.selectedRating = 0;
            },
            submitReview(){
                fetch("http://127.0.0.1:5000/addremarks", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*",
                    },
                    body: JSON.stringify({
                        id: this.selectedRequest.service_request_id,
                        remarks: this.remarks,
                        rating: this.selectedRating,
                    }),
                })
                .then((resp) => resp.json())
                .then((data) => {
                    alert(data.message);
                    this.closeModal();
                })
            },
            editRequest(request){
                this.selectedRequest = {
                    serviceName: this.services.find(s => s.service_id === request.service_id).name,
                    date_of_request: request.date_of_request,
                    professional_id: request.professional_id,
                    service_request_id: request.service_request_id,
                    rating: request.rating,
                    remarks: request.remarks
                }
                this.showDateModal = true;
            },
            closeDateModal(){
                this.showDateModal = false;
            },
            submitDate(){
                fetch("http://127.0.0.1:5000/updatedate", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*",
                    },
                    body: JSON.stringify({
                        id: this.selectedRequest.service_request_id,
                        date: this.date
                    }),
                })
                .then((resp) => resp.json())
                .then((data) => {
                    alert(data.message);
                    this.closeDateModal();
                })
            }
        },
        mounted(){
            this.fetchServiceRequests();
        }
    }
</script>

<style scoped>
/* Modal Backdrop */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1040;
}
.modal {
  z-index: 1050;
}

/* Star Rating */
.star {
  font-size: 1.5rem;
  cursor: pointer;
  color: #ccc;
  transition: color 0.3s;
}
.star.selected {
  color: gold;
}
</style>