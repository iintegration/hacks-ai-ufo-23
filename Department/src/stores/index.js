
import Vuex from 'vuex'
import { createStore } from "vuex";
import axios from 'axios'


const store = createStore({
    state () {
      return {
        status: '',
        token: localStorage.getItem('token') || '',
        user : {
        }
      }
    },
    mutations: {
        auth_request(state){
            state.status = 'loading'
          },
          auth_success(state, token, user){
            state.status = 'success'
            state.token = token
            state.user = user
          },
          auth_error(state){
            state.status = 'error'
          },
          logout(state){
            state.status = ''
            state.token = ''
          },
    },
    actions: {
        login({commit}, user){
            console.log(user)
            return new Promise((resolve, reject) => {
              commit('auth_request')
              axios({url: 'https://hackathon.sosus.org/auth/', data: {'login': user.username, 'password':user.password}, method: 'POST' })
              .then(resp => {
                const token = resp.data.token
                const user = resp.data.user
                localStorage.setItem('token', token)
                axios.defaults.headers.common['X-Token'] = token
                commit('auth_success', token, user)
                resolve(resp)
              })
              .catch(err => {
                commit('auth_error')
                localStorage.removeItem('token')
                reject(err)
              })
            })
          },
    },
    getters : {
        isLoggedIn: state => !!state.token,
        authStatus: state => state.status,
        userName: state => state.user.username
    }
  })

  export default store