<template>
    <div class="run-info" v-bind:class="{open:showAll,selectable:availableRuns.length > 1}">
        <div class="run" @click="showAll=!showAll">
             {{selectedRun.model_info}} @ {{selectedRun.test_collection}} <span v-if="availableRuns.length > 1"><i class="fas fa-sort-down"></i></span>
        </div>
        <div class="dropdown" v-show="showAll">
        <div class="run" v-for="srv in availableRuns" v-if="srv!=selectedRun" :key="srv.model_info+srv.test_collection" @click="changeSelection(srv)">
             {{srv.model_info}} @ {{srv.test_collection}}
        </div>
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
      showAll:false,
      selectedRun:{},
      availableRuns: <string[]>[]
    };
  },
  methods: {
    changeSelection(newRun){
      this.selectedRun = newRun;
      this.$emit("run-changed",newRun)
      this.showAll=false
    }
  },
  created: function() {

    fetch("/run-info")
        .then(FetchHelper.status)
        .then(FetchHelper.json)
        .then(data => {
          this.availableRuns.push(...data.runs);
          this.selectedRun = this.availableRuns[0];
          this.$emit("run-changed",this.availableRuns[0])
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
  border-bottom:2px solid transparent;
  padding:3px;
  padding-bottom: 8px;
  margin-bottom: -2px;
  position: relative;

  &.selectable:hover, &.selectable.open{
    border-bottom:2px solid blueviolet;
    cursor: pointer;
  }

  .dropdown{
    position:absolute;
    background: white;
    border:1px solid blueviolet;
    right: 0;
    left: 0;
    top: 100%;
    margin-top: 1px;
    .run{
      cursor: pointer;
      display: block;
      padding: 10px 0;
      &:hover{
        background: #f4f4f4;
      }
    }
  }

 .run {
    font-weight: normal;
    padding: 4px;
    padding-left: 0px;
    //border-left: 1px solid gray;
    //margin-left: 10px;
    padding-right: 0;
    display: inline-block;
    font-size: 13px;
    span {
      top:-2px;
      margin-left:4px;
      opacity: 0.8;
      position: relative;
    }

  }
}
</style>