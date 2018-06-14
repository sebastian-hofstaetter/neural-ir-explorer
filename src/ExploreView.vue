<template>
    <div>
        <configuration-selector v-on:config-change="handleConfigChange" />

        <exploration-search v-bind:selected-config="compiledConfigurations" />

    </div>
</template>

<script lang="ts">
import Vue from "vue";
import ExplorationSearch from "./components/ExplorationSearch.vue";
import ConfigurationSelector from "./components/ConfigurationSelector.vue";
import {
  SelectedConfiguration
} from "./models";

export default Vue.extend({
  //props: ['name', 'initialEnthusiasm'],
  data() {
    var compiledConfigurations: SelectedConfiguration[] = [];
    return {
      compiledConfigurations: compiledConfigurations
    };
  },
  methods: {
    handleConfigChange(newConfig:SelectedConfiguration[]) {
        this.compiledConfigurations = newConfig
    },
  },
  components: {
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