<template>
    <div class="single-query-view">
        <div class="section-header">
            <div @click="goBack()"><i class="fa fa-chevron-left"></i></div>
            <div class="query">Hello {{query}}</div>
            <div class="controls">Kernels</div>
        </div>
        <div class="document" v-for="d in documentData" :key="d.id">
            <div class="head"><span>#{{d.id}}</span> - </div>
            <div class="text"> <span v-for="(t,t_index) in d.tokenized_document" :key="d.id + t_index">{{t}} </span> </div>
        </div>
    </div>
</template>

<script lang="ts">
import Vue from "vue";
import FetchHelper from "../fetch-helper";

export default Vue.extend({
    props: ['query'],
    data() {
        return {
            enthusiasm: this.query,
            documentData:<any[]>[]
        }
    },
    methods: {
        goBack() { 
            this.$emit("back"); 
        },
        decrement() {
            if (this.enthusiasm > 1) {
                this.enthusiasm--;
            }
        },
    },
    watch: { 
      	query: function(newVal, oldVal) { // watch it
            if(newVal!=""){
                fetch("/query/"+newVal)
                    .then(FetchHelper.status)
                    .then(FetchHelper.json)
                    .then(data => {
                      this.documentData.length = 0
                      this.documentData.push(...data.documents);
                    })
                    .catch(error => {
                      console.log(error);
                    });
            }
        }
    },
    computed: {
        exclamationMarks(): string {
            return Array(this.enthusiasm + 1).join('!');
        }
    }
});
</script>

<style lang="scss">
.single-query-view {
    margin: auto;
    max-width: 600px;
    padding-top: 70px;

    .section-header{
        position: fixed;
        top: 50px;
    }
    .document{
        margin: 5px;
        .text{
            text-align:justify; 
        }
    }
}
</style>