<template>
    <span class="up-down" v-bind:class="{ up: score1 - score2 > 0, down:score1 - score2 < 0 }">
      <template v-if="score1 - score2 == 0">
        <i class="fas fa-exchange-alt"></i> 0
      </template>
      <template v-if="score1 - score2 > 0">
        <i class="fas fa-plus-circle"></i> {{score1 - score2}}
      </template>
      <template v-if="score1 - score2 < 0">
        <i class="fas fa-minus-circle"></i> {{-1 * (score1 - score2)}}
      </template>
    </span>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  props: ['score1', 'score2'],
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