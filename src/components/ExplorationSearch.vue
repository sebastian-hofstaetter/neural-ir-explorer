<template>
    <div class="search-area">
        <div class="search-bar">
            <span class="search-title">Search</span>
            <span class="sep"></span>
            <input placeholder="search query" v-model="query" @keyup.enter="search()"/>
            <span class="sep"></span>
            <span class="toggle-button" v-on:click="showAllContent=!showAllContent" v-bind:class="[showAllContent ? 'on' : 'off']"><i class="fas fa-align-left"></i> <span v-if="showAllContent">Show content</span> <span v-else>Hide content</span></span>
        </div>
        <div class="search-results" 
             v-bind:style="{ 'grid-template-columns': '20px repeat('+results.length+', minmax(auto,300px))' }"
             v-bind:class="[{ 'highlight-mode': highlightDoc }]">

            <div class="position-number" v-for="i in maxResultNumber" :key="'pos'+i"
                 v-bind:style="{ 'grid-row': i + 1 }">
                 {{i}}
            </div>

            <template class="single-result" v-for="(r,index) in results" v-if="r">

                <div class="conf-head" :key="r.basedOn.id + '-' + index" v-bind:style="{ 'grid-column': index + 2 }">
                  <div class="top-row">
                    <span class="based-on">#{{r.basedOn.id}}</span>
                    <span class="total-found">Found: {{r.totalFound}}</span>
                  </div>

                  <div class="preprocessing-info">{{r.preprocessingInfo}}</div>
                </div>

                <div class="single-doc" v-for="(item,row) in r.results" :key="r.basedOn.id + '-' + item.id"
                    v-bind:style="{ 'grid-column': index + 2, 'grid-row': row + 2 }"
                    v-bind:class="[{ 'highlight-doc': highlightDoc && highlightDocId == item.id }]"
                    v-on:click="toggleHighlight(item.id)">
                    <span class="score">{{item.score}}</span> - <span class="id">{{item.id}}</span> - <span class="title">{{item.title}}</span>
                    <div class="content" v-if="showAllContent || (highlightDoc && highlightDocId == item.id)">{{item.contents}}</div>
                </div>

            </template>
        </div>
    </div>
</template>

<script lang="ts">
import Vue from "vue";
import { SearchResult, ResultItem, SelectedConfiguration } from "../models";
import FetchHelper from "../fetch-helper";

export default Vue.extend({
  //props: ["selectedConfig"],

  data() {
    var results: SearchResult[] = [];
    return {
      query: "",
      results: results,
      selectedConfig: <SelectedConfiguration[]>[],
      showAllContent: true,
      highlightDoc: false,
      highlightDocId: ""
    };
  },
  created: function() {
    this.$root.$on("config-change", (data: SelectedConfiguration[]) => {
      this.selectedConfig = data;
      if (this.query != "") {
        this.search();
      }
    });
  },
  methods: {
    search() {
      this.results = new Array(this.selectedConfig.length);

      var searchRequest = (index: number) => {
        fetch(this.selectedConfig[index].basedOn.server + "/search?query="+encodeURIComponent(this.query), {
          headers: { "Content-Type": "application/json" },
          method: "POST",
          body: JSON.stringify(this.selectedConfig[index])
        })
          .then(FetchHelper.status)
          .then(FetchHelper.json)
          .then(data => {
            this.$set(this.results, index, data);
          })
          .catch(error => {
            console.log(error);
          });
      };

      for (var i = 0; i < this.selectedConfig.length; i++) {
        searchRequest(i);
      }
    },
    toggleHighlight(id: string) {
      if (this.highlightDocId == id) {
        this.highlightDoc = false;
        this.highlightDocId = "";
      } else {
        this.highlightDoc = true;
        this.highlightDocId = id;
      }
    }
  },
  computed: {
    maxResultNumber() {
      var maxNum = 0;
      for (let i = 0; i < this.results.length; i++) {
        if (this.results[i]) {
          const numResults = this.results[i].results.length;
          if (numResults > maxNum) {
            maxNum = numResults;
          }
        }
      }
      return maxNum;
    }
  }
});
</script>

<style lang="scss">
.search-area {
  padding: 10px;
}
.search-title {
  display: inline-block;
  font-size: 15px;
  padding: 5px 0;
}
.sep {
  border-right: 1px solid gray;
  padding: 8px;
  margin-right: 20px;
}
.search-bar input {
  margin: 10px auto;
  display: inline-block;
  padding: 10px;
  width: 300px;
}
.search-results {
  display: grid;
  grid-gap: 10px;

  .position-number {
    grid-column: 1;
    text-align: center;
    color: gray;
    font-weight: bold;
    border-top: 1px solid gray;
  }
  .conf-head {
    grid-row: 1;
    .based-on {
      font-weight: bold;
    }
    .top-row {
      padding-bottom: 10px;
      margin-bottom: 10px;
      border-bottom: 1px solid blueviolet;
    }
    .total-found {
      font-style: italic;
      color: gray;
    }
  }
  .single-doc {
    .id {
      font-weight: bold;
    }
  }
  &.highlight-mode .single-doc{
      color:#cccccc;
  }
  &.highlight-mode .single-doc.highlight-doc{
      color:black;
  }
}
.toggle-button {
  cursor: pointer;
  &.on {
    color: black;
  }
  &.off {
    color: gray;
  }
  &.on .fas {
    color: blueviolet;
  }
  &.off .fas {
    color: lavender;
  }
}
</style>