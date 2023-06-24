<template>
    <div>
        <p v-tooltip="reasonArr.about">{{ reasonArr.name }}</p>
    </div>
</template>

<script>
    export default {
        components: {
        },
        props: {
            reasonArr: Array
        },
        data() {
            return {
                
            }
        },
        mounted() {
            console.log('HOHO')
            console.log(this.reasonArr)
        }

    }
</script>

<style lang="scss" scoped>

</style>