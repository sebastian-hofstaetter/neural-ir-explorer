<template>
    <div>
        <configuration-selector />

        <exploration-search />

    </div>
</template>

<script lang="ts">
import Vue from "vue";
import ExplorationSearch from "./components/ExplorationSearch.vue"
import ConfigurationSelector from "./components/ConfigurationSelector.vue"

export default Vue.extend({
    //props: ['name', 'initialEnthusiasm'],
    data() {
        return {
            enthusiasm: 0,
        }
    },
    methods: {
        increment() { 
            

        },
        decrement() {
            
        },
    },
    computed: {
        exclamationMarks(): string {
            return "";
        }
    },
    components:{
        ExplorationSearch,
        ConfigurationSelector
    }
    });
</script>

<style lang="scss">
$color: red;

.greeting {
    color: $color;
    font-size: 20px;
}
</style>