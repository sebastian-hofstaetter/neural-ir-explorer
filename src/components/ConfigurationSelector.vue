<template>
    <div class="config">
        <div class="config-title">Configuration<span class="taskbar-add-button" @click="addNewCompiled()"><i class="fas fa-plus"></i> Add</span></div>
        <div class="single-config" v-for="conf in compiledConfigurations" :key='conf.configId'>
            <div class="config-header"><b>#{{conf.id}}</b> {{conf.basedOn.testCollection}} @ {{conf.basedOn.server}}</div>
            <div class="param-selection">
                <template v-for="(value, parameterName) in conf.basedOn.parameters">
                    <div class="param-name" :key="conf.id+parameterName+'name'">{{ parameterName }}</div>
                    <div class="selection-wrapper" v-if="value.type == 0" :key="conf.id+parameterName"> <!-- ConfigParameterType.Selection -->
                        <div v-for="option in value.valueRange" :key="option" 
                            v-bind:class="{ active: option == conf.parameters[parameterName].value }"
                            class="selection-option"
                            @click="conf.parameters[parameterName].value = option; indicateChange()">
                            {{option}}
                        </div>
                    </div> 
                    <div class="number-wrapper" v-else :key="conf.id+parameterName"> <!-- ConfigParameterType.Float or ConfigParameterType.Int-->
                        <input v-model.number="conf.parameters[parameterName].value"
                               @change="indicateChange()"
                               type="number" 
                               step="0.01" 
                               :min="value.valueRange.from" 
                               :max="value.valueRange.to" />
                        <div>Allowed: {{value.valueRange.from}} - {{value.valueRange.to}}</div>
                    </div>
                </template>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import Vue from "vue";
import {
  AvailableConfiguration,
  ConfigParameterType,
  SelectedConfiguration
} from "../models";

// todo rest call
var availableConfigurations: AvailableConfiguration[] = [
  {
    server: "http://localhost:5000",
    testCollection: "trec-8",
    parameters: {
      stemming: {
        type: ConfigParameterType.Selection,
        valueRange: ["Porter", "None"]
      },
      "retrieval-model": {
        type: ConfigParameterType.Selection,
        valueRange: ["BM25", "LM"]
      },
      "sim-model-threshold": {
        type: ConfigParameterType.Float,
        valueRange: { from: 0.4, to: 1 }
      }
    }
  }
];

export default Vue.extend({
  data() {
    var compiledConfigurations: SelectedConfiguration[] = [];
    return {
      availableConfigurations: availableConfigurations,
      compiledConfigurations: compiledConfigurations
    };
  },
  methods: {
    addNewCompiled() {
      var newConf: SelectedConfiguration = {
        id: this.compiledConfigurations.length,
        basedOn: this.availableConfigurations[0],
        parameters: {}
      };

      Object.keys(newConf.basedOn.parameters).forEach(k => {
        newConf.parameters[k] = {
          type: newConf.basedOn.parameters[k].type,
          value: 0
        };
        if (
          newConf.basedOn.parameters[k].type == ConfigParameterType.Selection
        ) {
          newConf.parameters[k].value = (<string[]>newConf.basedOn.parameters[k]
            .valueRange)[0];
        } else {
          newConf.parameters[k].value = (<{ from: number; to: number }>newConf
            .basedOn.parameters[k].valueRange).from;
        }
      });

      this.compiledConfigurations.push(newConf);
      this.indicateChange();
    },
    indicateChange() {
      this.$root.$emit("config-change", this.compiledConfigurations);
    }
  },
  created: function() {
    this.$root.$on("server-change", (servers: AvailableConfiguration[]) => {
      this.availableConfigurations = servers;
      if (this.availableConfigurations.length == 1) {
        this.addNewCompiled();
      }
    });
  },
  computed: {}
});
</script>

<style lang="scss">
.config-title {
  font-size: 15px;
  padding: 5px 0;
}
.config {
  background: #e4e4e4;
  padding: 10px;

  .single-config {
    border: 1px solid #c3c3c3;
    border-radius: 5px;
    display: inline-block;
    padding: 5px;
    margin: 10px;
    background: #eee;
  }

  .config-header {
    border-bottom: 1px solid #dddddd;
    margin-bottom: 12px;
    padding-bottom: 5px;
  }

  .param-selection {
    display: grid;
    grid-template-areas: "a a";
    grid-gap: 10px;

    .param-name {
      color: #777777;
      display: inline-block;
      cursor: default;
    }
    .selection-wrapper {
      display: inline-block;
    }
    .selection-option {
      display: inline;
      cursor: pointer;
      padding: 3px;

      &:hover {
        background: #b56df9;
      }
      &.active {
        background: blueviolet;
        color: white;
      }
    }
  }
}
</style>