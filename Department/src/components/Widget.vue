<template>
    <div style="border: 1px solid black; border-radius: 10px;" @click="$router.push({name: 'Widget', params: {obj_id:myArray.id}})">
        <div class="objectKey">
            {{ myArray.obj_key }}
        </div>
        <div class="objectBody">
            {{ myArray.general_contractor }}
        </div>
    </div>
</template>

<script>
import router from '../router';
export default {
    
    props: {
            myArray: {
                type:Array,
                required:true 
            },

        },
    data() {
      
        return {

        }
    },
}
</script>

<style lang="scss" scoped>
    .objectKey{
        display: flex;
        place-content: center;
        color: black;
        padding-top: 5px;
        border-bottom: 1px solid black;
    }
    .objectBody{
        min-width: 200px;
        min-height: 80px;
        color: black;
        padding-left: 5px;
    }

</style>