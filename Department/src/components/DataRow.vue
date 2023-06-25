<template>
    <div class="rowBody">
        <a>{{ tasksArray.name }}</a>
        <a>{{ tasksArray.predicted_end_date }} Дней</a>
        <a>Не успели сделать</a>
        <ReasonRow  v-for:="item in tasksArray.reason" :reasonArr="item"></ReasonRow>
    </div>
</template>

<script>
import ReasonRow from './ReasonRow.vue';
export default {
    props: {
        object: {
            type: Object
        },
        tasksArray: Object
    },
    data() {
        return {
            
        };
    },
    components: { ReasonRow },
    mounted() {
        console.log(this.tasksArray)
    }
}
</script>

<style lang="scss" scoped>
.rowBody {
    display: flex;
    justify-items: space-around;
    border:1px solid black;

}

.rowBody a {
    text-align: start;
    flex-basis: 33%;
    border-left: 1px solid black;

    padding: 2px;
    
}
</style>