<template>
    <div>
        <div class="greeting">Search now: {{selectedConfig.length}}</div>
        <input placeholder="search query" />
    </div>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
    props: ['selected-config'],

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