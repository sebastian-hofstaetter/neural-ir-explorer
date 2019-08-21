<template>
  <div class="query-cluster-section">
    <div class="cluster-c-back">
      <div class="cluster-controls">
        <div class="control-bar-element">
          Sort
          <i
            class="fas fa-sort-amount-down selection-option"
            v-bind:class="{ active: sortBy == 'desc' }"
            @click="sortBy = 'desc'; sortAll()"
          ></i>
          <i
            class="fas fa-sort-amount-up-alt selection-option"
            v-bind:class="{ active: sortBy == 'asc' }"
            @click="sortBy = 'asc'; sortAll()"
          ></i>
        </div>
        <div
          class="control-bar-element selection-option"
          v-bind:class="{ active: collapsAll }"
          @click="collapsAll = !collapsAll"
        >
          <i class="fas fa-tasks"></i> Collaps clusters
        </div>
        <div class="control-bar-element">
          <input placeholder="Prefix filter" />
        </div>
      </div>
    </div>

    <div class="cluster-list">
      <div class="cluster-card" v-for="c in clusters" :key="c.id">
        <div class="cluster-info">
          <span class="score">{{parseInt(c.data.tk_med)}}</span>
          <up-down-score v-bind:score2="c.data.tk_med" v-bind:score1="c.data.bm25_med" />
          <span class="summary">{{c.data.summary}}</span>
        </div>
        <div
          class="query"
          v-for="q in filterCollapsed(c.data.queries,c.id)"
          :key="q.qid"
          @click="indicateChange(q.qid)"
        >
          <span class="score">{{q.rank_tk}}</span>
          <up-down-score v-bind:score2="q.rank_tk" v-bind:score1="q.bm25_rank" />
          <span>{{q.text}}</span>
        </div>
        <div class="more-queries" v-show="c.data.queries.length-maxCollapsCountPerCluster[c.id] > 0" @click="toggleSingleCollapsesCluster(c.id,c.data.queries.length+1)">
            + {{c.data.queries.length-maxCollapsCountPerCluster[c.id]}} more queries
        </div>
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
import UpDownScore from "./UpDownScore.vue";

import FetchHelper from "../fetch-helper";

export default Vue.extend({
  data() {
    var clusters: any = [];
    return {
      //availableConfigurations: availableConfigurations,
      clusters: clusters,
      sortBy: "desc", // or "asc"
      prefixFilter: "",
      collapsAll: true,
      maxCollapsCount: 10,
      maxCollapsCountPerCluster:<any>{}
    };
  },
  methods: {
    indicateChange(qid: string) {
      this.$emit("query-select", qid);
    },
    toggleSingleCollapsesCluster(cluster:any,val:number){
        this.$set(this.maxCollapsCountPerCluster,cluster,val);
        this.$forceUpdate()
    },
    sortAll(){
        const compareCluster = (a:any, b:any) => {
          var a_float = parseInt(a.data.tk_med)
          var b_float = parseInt(b.data.tk_med)
          var base = this.sortBy == "asc" ? -1 : 1;
          if (a_float < b_float) return -1 * base;
          if (a_float > b_float) return 1 * base;
          return 0;
        }
        const compareQueries = (a:any, b:any) => {
          var a_float = parseInt(a.rank_tk)
          var b_float = parseInt(b.rank_tk)
          var base = this.sortBy == "asc" ? -1 : 1;
          if (a_float < b_float) return -1 * base;
          if (a_float > b_float) return 1 * base;
          return 0;
        }
        for (var cid in this.clusters) {
            this.clusters[cid].data.queries.sort(compareQueries)
        }
        this.clusters.sort(compareCluster);
        this.$forceUpdate();
    },
    filterCollapsed(queries: any[],clusterId:string) {
      if (this.collapsAll == false) return queries;
      return queries.slice(0, this.maxCollapsCountPerCluster[clusterId]);
    }
  },
  created: function() {
    fetch("/evaluated-queries")
      .then(FetchHelper.status)
      .then(FetchHelper.json)
      .then(data => {
        for (var cid in data.clusters) {
          this.maxCollapsCountPerCluster[cid] = this.maxCollapsCount;
          this.clusters.push({ id: cid, data: data.clusters[cid] });
        }
      })
      .catch(error => {
        console.log(error);
      });

    this.$root.$on("server-change", (servers: AvailableConfiguration[]) => {
      //this.availableConfigurations = servers;
      //if (this.availableConfigurations.length == 1) {
      //  this.addNewCompiled();
      // }
    });
  },
  computed: {},
  components: {
    UpDownScore
  }
});
</script>

<style lang="scss">
.query-cluster-section {
}

.cluster-c-back {
  background: white;
  text-align: center;
  position: fixed;
  top: 45px;
  left: 0;
  right: 0;
  z-index: 100;
}
.cluster-controls {
  padding: 10px;

  .control-bar-element {
    display: inline;
    margin: 10px;
  }

  .selection-option {
    cursor: pointer;
    padding: 5px;
    margin: 5px;

    &:hover {
      border-bottom: 2px solid #c49de8;
    }
    &.active {
      border-bottom: 2px solid blueviolet;
    }
  }
}

.cluster-list {
  z-index: 0;
  display: block;
  text-align: center;
  margin: 50px;

  .cluster-card {
    display: inline-block;
    border: 1px solid #d5d5d5;
    border-radius: 2px;
    box-shadow: 2px 2px 8px #d3d3d3;
    padding: 10px;
    width: 400px;
    margin: 10px;
    vertical-align: top;
    text-align: left;
    .more-queries {
        color: gray;
        margin-top: 5px;
        cursor: pointer;
    }
    .cluster-info {
      margin-bottom: 5px;
      padding-bottom: 5px;
      border-bottom: 1px solid #d5d5d5;
      text-align: center;

      .score {
        border: 1px solid gray;
        border-radius: 50%;
        width: 18px;
        position: relative;
        display: inline-block;
        text-align: center;
      }
      .summary {
        font-weight: 500;
        margin: 3px;
      }
    }
  }
}

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
  }
}
</style>