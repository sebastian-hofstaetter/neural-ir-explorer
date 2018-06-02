<template>
    <div>
        <div class="greeting">Search now: </div>
        <input placeholder="search query" />
    </div>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
    data() {
        return {
            //enthusiasm: this.initialEnthusiasm,
        }
    },
    methods: {
        decrement() {
            
        },
    },
    computed: {

    }
});
</script>

<style>
.greeting {
    font-size: 20px;
}
</style>