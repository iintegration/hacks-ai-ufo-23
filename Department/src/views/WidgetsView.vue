

<template>
    <div class="body">
        <header class="header">
            <label for="upload" class="label">
                Загрузить данные
            </label>
            <input style="color: black;" type="file" id="upload" name="file" v-on:change="handleFileUpload()" />
            <UserIco />

        </header>
        <div class="widgets">

            <Widget v-for="item in items" :myArray=item />
        </div>
    </div>
</template>

<script>
import router from '../router';
import Widget from '../components/Widget.vue';
import UserIco from '../components/userIco.vue';
import FindBar from '../components/FindBar.vue';
import axios from 'axios';
export default {
    methods: {
        handleFileUpload() {
            this.file = this.$refs.file.files[0];
            let formData = new FormData();
            formData.append('uploaded_file', this.file);
            const token = localStorage.getItem('token')
            axios.post('https://hackathon.sosus.org/upload/',
                formData,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                        'x-token': token,
                    }
                }
            ).then(function () {
                console.log('SUCCESS!!');
            })
                .catch(function () {
                    console.log('FAILURE!!');
                });
        },
    },
    components: { FindBar, UserIco, Widget },
    mounted() {
        console.log('mount')
        const token = localStorage.getItem('token')
        axios({ url: "https://hackathon.sosus.org/subjects/", method: "GET", headers: { 'x-token': token } })
            .then(resp => {
                if (resp.data[0] != null) {
                    this.items = resp.data
                }

                console.log(this.items)
            }
            )
            .catch(err => {
                console.log(err);
            })
    },

    data() {

        return {
            items: [{
                "created": "2023-06-24T04:52:37.332Z",
                "obj_key": "123-124",
                "state": "string",
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "modified": "2023-06-24T04:52:37.332Z",
                "general_contractor": "string",
                "general_designer_key": "string",
                "number_of_workers": 0,
                "square": "string",
                "subtype": "string",
                "type": "string"
            }],
            file: ''

        }
    },
}
</script>

<style lang="scss" scoped>
.header {
    display: flex;
    justify-content: space-between;
    background-color: whitesmoke;
    border-bottom: 1px solid gray ;
    padding-top: 2px;
    padding-left: 5px;
    padding-right: 5px;
    margin-bottom: 20px;

}

.widgets {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    min-width: 100vw;
    margin-left:  20px;
}
.label{
    color: black;

}
#upload {
   position: absolute;
   z-index: -1;
}
</style>