<template>
    <div>
        <configuration-selector />

        <exploration-search />

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
    return {
    };
  },
  methods: {
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