<template>
    <div class="body">
        <form class="form">
            <input class="formInput" placeholder="Введите имя пользователя" v-model="username" />
            <input class="formInput" placeholder="Введите пароль" v-model="password" />
        </form>
        <button @click="login" class='button'>Войти</button>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    
    methods: {
        login: function () {
            let username = this.username
            let password = this.password
            this.$store.dispatch('login', { username, password })
                .then(() => this.$router.push('/'))
                .catch(err => console.log(err))
        },
    },
    data() {
        return {
            username: "",
            password: "",
        }
    }
}

</script>

<style lang="scss" scoped>
.body {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 5px;

}

.form {
    width: 20vw;
    border-radius: 20px;
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.formInput {
    background-color: whitesmoke;
    border: 1px solid black;
    border-radius: 10px;
    height: 25px;
    padding-left: 4px;
}

::placeholder {
    color: black;
}

.button {
    background-color: greenyellow;
    border: 1px solid whitesmoke;
    height: 70px;
    border-radius: 10px;
    width: 70px;
}

.buttonActive {
    background-color: green;
    border: none;
    border-radius: 10px;
}</style>