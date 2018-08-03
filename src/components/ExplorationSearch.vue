<template>
    <div class="search-area">
        <div class="search-bar">
            <span class="search-title">Search</span>
            <span class="sep"></span>
            <input placeholder="search query" v-model="query" @keyup.enter="search()"/>
        </div>
        <div class="search-results">
            <div class="single-result" v-for="(r,index) in results" :key="index">
              <template v-if="r">
                <div class="based-on">Conf: #{{r.basedOn.id}}</div>
                <div class="preprocessing-info">{{r.preprocessingInfo}}</div>
                <div class="total-found">Found: {{r.totalFound}}</div>
                <div class="documents">
                    <div class="doc" v-for="item in r.results" :key="item.id">
                        <div class="score">{{item.score}}</div>
                        <div class="id">{{item.id}}</div>
                        <div class="title">{{item.title}}</div>
                        <div class="content">{{item.contents}}</div>

                    </div>
                </div>
              </template>
              <div v-else>loading</div>
            </div>
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
      selectedConfig: <SelectedConfiguration[]>[]
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
        fetch(this.selectedConfig[index].basedOn.server + "/search", {
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
  //display: flex;
  //justify-content: space-between;
}
.single-result {
  display: inline-block;
  width: 50%;
  margin: auto;
  max-width: 300px;

  .total-found {
    font-style: italic;
    color: gray;
  }

  .doc {
    border: 1px solid gray;
    border-radius: 4px;
    margin: 4px;
  }
}
</style>