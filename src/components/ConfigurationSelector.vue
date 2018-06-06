<template>
    <div>
        <div class="greeting">Configurations available: </div>
        <div class="config" v-for="conf in compiledConfigurations" :key='conf.configId'>
            {{conf.id}} @ {{conf.basedOn.testCollection}}
            <div class="single-param" v-for="(value, parameterName) in conf.basedOn.parameters" :key="parameterName">
                <div class="param-name">{{ parameterName }}</div>
                <div v-if="value.type == 0"> <!-- ConfigParameterType.Selection -->
                    <div v-for="option in value.valueRange" :key="option" 
                         v-bind:class="{ active: option == conf.parameters[parameterName].value }"
                         @click="conf.parameters[parameterName].value = option">
                        {{option}}
                    </div>
                </div> 
                <div v-else> <!-- ConfigParameterType.Float or ConfigParameterType.Int-->
                    <input v-model.number="conf.parameters[parameterName].value" type="number" step="0.01" :min="value.valueRange.from" :max="value.valueRange.to" />
                    <div>Allowed: {{value.valueRange.from}} - {{value.valueRange.to}}</div>
                </div>

            </div>
        </div>
        <button @click="addNewCompiled()">Add new</button>
    </div>
</template>

<script lang="ts">
import Vue from "vue";
import {AvailableConfiguration,ConfigParameterType,SelectedConfiguration} from "../models";

// todo rest call
var availableConfigurations: AvailableConfiguration[] = [{
        server:"http://localhost:5000",
        testCollection:"trec-8",
        parameters: {
            "stemming":{type: ConfigParameterType.Selection, valueRange: ["Porter","None"]},
            "retrieval-model":{type: ConfigParameterType.Selection, valueRange: ["BM25","LM"]},
            "sim-model-threshold":{type: ConfigParameterType.Float, valueRange: {from: 0.4, to:1}}
        }
    }];


export default Vue.extend({
    
    data() {
        var compiledConfigurations:SelectedConfiguration[] = [];
        return {
            availableConfigurations:availableConfigurations,
            compiledConfigurations:compiledConfigurations
            }
    },
    methods: {
        addNewCompiled() {
            var newConf: SelectedConfiguration = {
                id:this.compiledConfigurations.length,
                basedOn:this.availableConfigurations[0],
                parameters:{}
            }
            
            Object.keys(newConf.basedOn.parameters).forEach(k => {
                newConf.parameters[k] = {
                    type: newConf.basedOn.parameters[k].type,
                    value: 0
                }
                if(newConf.basedOn.parameters[k].type == ConfigParameterType.Selection){
                    newConf.parameters[k].value = (<string[]>newConf.basedOn.parameters[k].valueRange)[0];
                }else{
                    newConf.parameters[k].value = (<{from:number,to:number}>newConf.basedOn.parameters[k].valueRange).from;
                }
            });

            this.compiledConfigurations.push(newConf);
        },
    },
    created: function(){
        this.addNewCompiled();
    },
    computed: {

    }
});
</script>

<style lang="scss">



</style>