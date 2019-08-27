<template>
  <div class="query-cluster-section">
    <div class="cluster-c-back">
      <div class="cluster-controls">
        <div class="control-bar-element">
          <span class="label">Sort</span>
          <i
            class="fas fa-dice selection-option"
            v-bind:class="{ active: sortBy == 'rand' }"
            @click="sortBy = 'rand'; shuffleAll()"
          ></i>
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
          <input class="prefix-filter" v-bind:class="{selected: prefixInput.length > 0}" v-model="prefixInput" placeholder="Prefix filter" />
        </div>
      </div>
    </div>

    <div class="cluster-list">
      <div class="cluster-card info-card" v-if="showInfoBox">
          <div class="close-info" @click="showInfoBox=false"><i class="fas fa-times"></i></div>
          <h1>Let's start exploring 🎉</h1>
          <p>Here is what you see around you and what you can do with it:
              <ul>
                  <li>At the top you can sort the queries: randomly, ascending or descending (based on the rank of the first relevant document). You can also expand the clusters to see all queries.</li>
                  <li>We clustered the queries based on their mean contextualized encoding. Each card holds the queries for a cluster.</li>
                  <li>At the top of each card is: the median best rank of the neural model, the difference to the first-stage baseline, and a manual summary of the queries in that cluster</li>
                  <li>Each query line contains: the best rank of the neural model, the difference to the first-stage baseline, and the query text</li>
                  <li>Simply click on a query to go to the result view - for much more details on the query result</li>
              </ul>
          </p>
      </div>
      <div class="cluster-card" v-for="c in filteredClusters" :key="c.cluster">
        <div class="cluster-info">
          <span class="score">{{parseInt(c.tk_med)}}</span>
          <up-down-score v-bind:score2="c.tk_med" v-bind:score1="c.bm25_med" />
          <span class="summary">{{c.summary}}</span>
        </div>
          
        <template v-for="q in c.queries" >
            <div
              class="query"
              :key="q.qid"
              @click="indicateChange(q)">
                <span class="score">{{q.rank_tk}}</span>
                <up-down-score v-bind:score2="q.rank_tk" v-bind:score1="q.bm25_rank" />
                <span class="text">{{q.text}}</span>
            </div><br :key="q.qid+'br'"/>
        </template>
        <div class="more-queries" v-show="c.overflowCount > 0" @click="toggleSingleCollapsesCluster(c.cluster,1000)">
            + {{c.overflowCount}} more queries (click to expand)
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
import Triejs from "../lib/trie";

/**
 * From: https://stackoverflow.com/a/6274381
 * Shuffles array in place.
 * @param {Array} a items An array containing the items.
 */
function shuffle(a:any[]) {
    var j, x, i;
    for (i = a.length - 1; i > 0; i--) {
        j = Math.floor(Math.random() * (i + 1));
        x = a[i];
        a[i] = a[j];
        a[j] = x;
    }
    return a;
}


export default Vue.extend({
  data() {
    var clusters: any = [];
    return {
      //availableConfigurations: availableConfigurations,
      clusters: clusters,
      filteredClusters:[],
      sortBy: "rand", // or "asc"
      prefixFilter: "",
      collapsAll: true,
      maxCollapsCount: 10,
      maxCollapsCountPerCluster:<any>{},
      showInfoBox:true,
      searchTrie:new Triejs({enableCache:false,maxCache:5000}),
      searchFiltered:new Set(),
      prefixInput:""
    };
  },
  methods: {
    indicateChange(q: any) {
      this.$emit("query-select", q);
    },
    toggleSingleCollapsesCluster(cluster:any,val:number){
        this.maxCollapsCountPerCluster[cluster] = val;
        this.filterCollapsed();
        this.$forceUpdate()
    },
    shuffleAll(){
        for (var cid in this.clusters) {
            shuffle(this.clusters[cid].data.queries)
        }
        shuffle(this.clusters)
        this.filterCollapsed();
        this.$forceUpdate();
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
        this.filterCollapsed();
        this.$forceUpdate();
    },
    filterCollapsed() {
      this.filteredClusters.length=0
      for(var c = 0;c<this.clusters.length;c++){
        var overflowCount = 0
        var queries = this.clusters[c].data.queries;
        if (this.searchFiltered.size > 0){
            var filteredqs = []
            for(var i=0;i<queries.length;i++){
                if(this.searchFiltered.has(queries[i].qid)){
                    filteredqs.push(queries[i])
                }
            }
            queries = filteredqs
        }
        if (this.collapsAll == true){
            overflowCount = queries.length - this.maxCollapsCountPerCluster[this.clusters[c].id]
            queries = queries.slice(0, this.maxCollapsCountPerCluster[this.clusters[c].id]);
        } 
        if (queries.length > 0){
            var filC = {...this.clusters[c].data}
            filC.queries = queries
            filC.overflowCount = overflowCount
            this.filteredClusters.push(filC)
        }
      }
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
          var queries = data.clusters[cid].queries
          for(var i=0;i<queries.length;i++){
            var current_q = queries[i];
            var current_q_text = queries[i].text.split(" ");
            for(var t=0;t<current_q_text.length;t++){
                this.searchTrie.add(current_q_text[t],current_q.qid)
            }
          }
        }
        this.filterCollapsed();
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
  watch: {
      prefixInput:function(newVal:string,oldVal:string) {
          if(newVal.length>1){
              this.searchFiltered = new Set(this.searchTrie.find(newVal));
          }
          else{
            this.searchFiltered = new Set();
          }
          this.filterCollapsed();  
          this.$forceUpdate();
      },
      collapsAll:function(newVal:boolean,oldVal:boolean) {
          this.filterCollapsed();  
          this.$forceUpdate();
      }
  },
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
  top: 47px;
  left: 0;
  right: 0;
  z-index: 100;
}
.cluster-controls {
  padding: 10px;

  .prefix-filter{
    border: 0;
    border-bottom: 2px solid #c7c7c7;
    padding: 5px;
    outline: 0;
    &:focus, &.selected{
    border-bottom: 2px solid blueviolet;

    }
  }
  .control-bar-element {
    display: inline;
    margin: 10px;
    .label{
        cursor: default;
        color: #777777;
    }
  }

  .selection-option {
    cursor: pointer;
    padding: 5px;

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
  margin-bottom: 10px;

  
  .cluster-card {
    display: inline-block;
    border: 1px solid #d5d5d5;
    border-radius: 2px;
    box-shadow: 2px 2px 8px #e6e6e6;
    padding: 10px;
    width: 400px;
    margin: 10px;
    vertical-align: top;
    text-align: left;

    .more-queries {
        color: gray;
        margin-top: 5px;
        cursor: pointer;
        display: inline-block;
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
    .query{
        cursor: pointer;
        display: inline-grid;
        grid-template-areas: "a a a";
        grid-gap: 5px;
        margin: 5px 0;
        .up-down{
            margin:0;
        }
        &:hover .text{
            font-weight: 500;
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