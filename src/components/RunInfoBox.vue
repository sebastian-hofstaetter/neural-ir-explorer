<template>
    <div class="run-info">
      &ndash;
        <div class="run" v-for="srv in availableRuns" :key="srv.server+srv.testCollection">
             {{srv.model_info}} @ {{srv.test_collection}}
        </div>
    </div>
</template>

<script lang="ts">
import Vue from "vue";
import { AvailableConfiguration, ConfigParameterType } from "../models";
import FetchHelper from "../fetch-helper";

export default Vue.extend({
  //props: ['name', 'initialEnthusiasm'],
  data() {
    return {
      availableRuns: <string[]>[]
    };
  },
  methods: {
    
  },
  created: function() {

    fetch("/run-info")
        .then(FetchHelper.status)
        .then(FetchHelper.json)
        .then(data => {
          this.availableRuns.push(data.runs);
        })
        .catch(error => {
          console.log(error);
        });
  },
});
</script>

<style lang="scss">

.run-info{
  display: inline-block;

 .run {
    font-weight: normal;
    padding: 4px;
    padding-left: 0px;
    //border-left: 1px solid gray;
    //margin-left: 10px;
    padding-right: 0;
    display: inline-block;
    font-size: 13px;

  }
}
</style>