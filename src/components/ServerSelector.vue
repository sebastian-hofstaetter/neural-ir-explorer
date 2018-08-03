<template>
    <div class="server-selector">
        <div class="connected-servers">
            <div class="server" v-for="srv in connectedServers" :key="srv.server+srv.testCollection">
                <i class="fas fa-check-circle"></i> {{srv.testCollection}} @ {{srv.server}}
            </div>
        </div>

        <span @click="showAdd=true" v-if="showAdd==false" class="taskbar-add-button"><i class="fas fa-plus"></i> Add Server</span>

        <div class="add-server" v-if="showAdd==true">
            <input v-model="currentInput" placeholder="New server" />
            <span class="taskbar-add-button" @click="addServer()"><i class="fas fa-plus"></i> Add Server</span>
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
      showAdd: true,
      currentInput: "http://localhost:8080/demo",
      connectedServers: <AvailableConfiguration[]>[]
    };
  },
  methods: {
    addServer() {
      fetch(this.currentInput + "/available-configurations")
        .then(FetchHelper.status)
        .then(FetchHelper.json)
        .then(data => {
          this.connectedServers.push(data);

          this.currentInput = "";
          this.showAdd = false;

          this.$root.$emit("server-change", this.connectedServers);
        })
        .catch(error => {
          console.log(error);
        });
    }
  }
});
</script>

<style lang="scss">
.server-selector,
.connected-servers,
.add-server {
  display: inline-block;
  font-weight: normal;
}
.connected-servers .server {
  padding: 4px;
  padding-left: 10px;
  border-left: 1px solid gray;
  margin-left: 10px;
  padding-right: 0;
  display: inline-block;
  font-size: 13px;

  & .fas {
    color: green;
  }
}
.add-server input {
  padding: 3px;
}
.add-server .taskbar-add-button {
  border-left: 0;
  padding-left: 0;
}
</style>