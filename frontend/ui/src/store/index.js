import { createStore } from 'vuex'

export default createStore({
  state: {
    is_logged_in: false,
    role: '',
    token: '',
    is_blocked: false
  },
  getters: {
  },
  mutations: {
    loginUser: function(state, data){
      // console.log("from store: ", role, token, is_blocked)
      state.is_logged_in = true;
      state.role = data.role;
      state.token = data.token;
      state.is_blocked = data.is_blocked;
    },
    logoutUser: function(state){
      state.is_logged_in = false;
      state.role = '';
      state.token = '';
      state.is_blocked = false;
      localStorage.clear();
    }
  },
  actions: {
  },
  modules: {
  }
})
