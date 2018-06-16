<template>
    <div class="search-area">
        <div class="search-bar">
            <input placeholder="search query" v-model="query" @keyup.enter="search()" @change="search()" />
        </div>
        <div class="search-results">
            <div class="single-result" v-for="(r,index) in results" :key="index">
                <div class="based-on">Conf: #{{r.basedOn.id}}</div>
                <div class="preprocessing-info">{{r.preprocessingInfo}}</div>
                <div class="total-found">Found: {{r.totalFound}}</div>
                <div class="documents">
                    <div class="doc" v-for="item in r.results" :key="item.id">
                        <div class="score">{{item.score}}</div>
                        <div class="id">{{item.id}}</div>
                        <div class="title">{{item.title}}</div>
                        <div class="content">{{item.content}}</div>

                    </div>
                </div>

            </div>
        </div>
    </div>
</template>

<script lang="ts">
import Vue from "vue";
import {
  SearchResult,
  ResultItem
} from "../models";

export default Vue.extend({
    props: ['selectedConfig'],

    data() {
        var results:SearchResult[] =[]
        return {
            query:"",
            results:results
        }
    },
    methods: {
        search() {
            this.results=[];
            for(var i = 0;i<this.selectedConfig.length;i++){
                var results:ResultItem[]=[];

                for(var t=0;t<10;t++){
                    results.push({
                        id:"doc:"+i+"-"+t,
                        title:"sample title",
                        contents:"full contents, might be longer",
                        score:20-t,
                        explanation:"score explanation .."
                    })
                }

                var single:SearchResult={
                    basedOn:this.selectedConfig[i],
                    results:results,
                    totalFound:20,
                    preprocessingInfo:"query preprocessing info"
                }
                this.results.push(single);
            }
        },
    }
});
</script>

<style lang="scss">
.search-bar input {
    margin: 10px auto;
    display: block;
    padding: 10px;
    width: 300px;
}
.single-result{
    display: inline-block;

    .total-found{
        font-style: italic;
        color:gray;
    }

    .doc{
        border:1px solid gray;
        border-radius: 4px;
        margin: 4px;
    }
}
</style>