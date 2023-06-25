
<template>
    <div class="body">
        <div class="lendos">
            <a>Тип: {{ object.subtype }}</a>
            <a>Объект: {{ object.type }}</a>
            <a>Площадь: {{ object.square }}</a>
            <a>Дизайнер: {{ object.general_designer_key }}</a>
            <a>Заказчик: {{ object.general_contractor }}</a>
            <a>Состояние: {{ object.state }}</a>
            <input type="file" id="file" ref="file" v-on:change="handleFileUpload()" />

        </div>
        <div class="infoTables">
            <div class="header">
                <p>Задача</p>
                <p>Сдвиг</p>
                <p>Причина сдвига</p>
            </div>
            <div class="tableBody">
                <DataRow v-for="item in tasks" :tasks-array="item" class="data"></DataRow>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import DataRow from '../components/DataRow.vue';
export default {
    props: {
        object: {
            type: Object,
            requirement: true,
        },
        tasksArray: Array
    },
    data() {
        return {
            object: {
                "created": "2023-06-23T21:45:55.188Z",
                "obj_key": "333-201",
                "state": "Строительство",
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "modified": "2023-06-23T21:45:55.188Z",
                "general_contractor": "Кирилл",
                "general_designer_key": "Альберт",
                "number_of_workers": 1,
                "square": "10квМ2",
                "subtype": "Муниципальный",
                "type": "Школа",
                "photo_url": "/Building.jpg"
            },
            tasks: [],
            headers: [
                {
                    label: "Задача",
                    field: "name"
                },
                { label: "Фактический срок завершения", field: "fact" },
                { label: "Планируемый срок завершения", field: "plan" },
                { label: "Состояние", field: "state" },
            ],
        };
    },
    components: { DataRow },
    mounted() {
        const id = this.$route.params.obj_id
        console.log(id)
        console.log('mount')
        const token = localStorage.getItem('token')
        axios({ url: `https://trackbacks-efficient-precision-youth.trycloudflare.com/subjects/${id}/`, method: "GET", headers: { 'x-token': token } })
            .then(resp => {
                if (resp.data != null) {
                    this.object = resp.data
                }

                console.log(this.object)
            }
            )
            .catch(err => {
                console.log(err);
            })
        axios({ url: `https://trackbacks-efficient-precision-youth.trycloudflare.com/subjects/${id}/tasks/`, method: "GET", headers: { 'x-token': token } })
            .then(resp => {
                if (resp.data != null) {
                    this.tasks = resp.data
                }

                console.log('Tasks')
            }
            )
            .catch(err => {
                console.log(err);
            })
            setInterval(this.handleTaskUpdate,5000)

    },
    methods: {
        handleTaskUpdate() {
            const id = this.$route.params.obj_id
            console.log(id)
            console.log('mount')
            const token = localStorage.getItem('token')
            axios({ url: `https://trackbacks-efficient-precision-youth.trycloudflare.com/subjects/${id}/`, method: "GET", headers: { 'x-token': token } })
                .then(resp => {
                    if (resp.data != null) {
                        this.object = resp.data
                    }

                    console.log(this.object)
                }
                )
                .catch(err => {
                    console.log(err);
                })
        },
        handleFileUpload() {
            const obj_key = this.object.obj_key
            const id = this.$route.params.obj_id
            this.file = this.$refs.file.files[0];
            let formData = new FormData();
            formData.append('uploaded_file', this.file);
            const token = localStorage.getItem('token')
            console.log(obj_key)
            axios.post(`https://trackbacks-efficient-precision-youth.trycloudflare.com/upload/${obj_key}/`,
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
}
</script>

<style lang="scss" scoped>
.infoTables {
    margin: 0 auto;
    justify-content: space-around;
    min-width: 50vw;
    flex-wrap: nowrap;

}

.header {
    display: flex;
    justify-content: space-around;
    margin-bottom: 10px;
    border: 1px solid black;



}

.header p {
    flex-basis: 33%;
    padding: 1px;
    border-right: 1px solid black;

}

.data {
    display: flex;


}

.body {
    display: flex;
    padding: 20px;
    font-size: 15px;
    color: black;
    align-items: flex-start;

}

.lendos {
    display: flex;
    flex-direction: column;
    font-size: 15px;
    color: black;
    gap: 5px;
    border: 1px solid black;
    border-radius: 10px;
    padding: 5px;


}
</style>