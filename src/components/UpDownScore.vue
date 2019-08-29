<template>
    <span class="up-down" v-bind:class="{ up: score1 - score2 > 0, down:score1 - score2 < 0 }">
      <template v-if="score1 - score2 == 0">
        <i class="fas fa-exchange-alt"></i> 0
      </template>
      <template v-if="score1 - score2 > 0">
        <i class="fas fa-plus-circle"></i> {{lowerZero}}
      </template>
      <template v-if="score1 - score2 < 0">
        <i class="fas fa-minus-circle"></i> {{biggerZero}}
      </template>
    </span>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  props: ['score1', 'score2','maxDec'],
  computed:{
    lowerZero:function(){
      if (this.maxDec != null){
        return (this.score1 - this.score2).toFixed(this.maxDec)
      }
      return this.score1 - this.score2
    },
    biggerZero:function(){
      if (this.maxDec != null){
         return (-1 * (this.score1 - this.score2)).toFixed(this.maxDec)
      }
      return -1 * (this.score1 - this.score2)
    },
  }
});
</script>

<style lang="scss">

.up-down{
  display: inline-block;
  color:gray;
  margin: 3px;
  .fas{
    font-size: 7pt;
    vertical-align: middle;
    margin-top: -1px;
  }
  &.up {
    color:green;
  }
  &.down {
    color:red;
  }
}
</style>