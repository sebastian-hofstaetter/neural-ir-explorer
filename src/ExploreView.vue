<template>
    <div>
        <query-cluster-list v-on:query-select="changeQuery" v-show="currentMainView == 'all-queries'"/>

        <single-query-view v-on:back="currentMainView = 'all-queries'" v-show="currentMainView == 'single-query'" v-bind:query="currentSelectedQuery"/>

    </div>
</template>

<script lang="ts">
import Vue from "vue";
import SingleQueryView from "./components/SingleQueryView.vue";
import QueryClusterList from "./components/QueryClusterList.vue";
import {
  SelectedConfiguration
} from "./models";

export default Vue.extend({
  //props: ['name', 'initialEnthusiasm'],
  data() {
    return {
      currentMainView:"all-queries",
      currentSelectedQuery:""
    };
  },
  methods: {
    changeQuery:function(qid:string){
      this.currentMainView="single-query"
      this.currentSelectedQuery = qid
    }
  },
  components: {
    SingleQueryView,
    QueryClusterList
  }
});
</script>

<style lang="scss">


</style>