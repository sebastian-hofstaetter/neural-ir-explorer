<template>
    <div class="single-query-view">
        <div class="section-header">
            <span class="back-button" @click="goBack()"><i class="fa fa-chevron-left"></i> All queries</span>
            <div class="query">{{query.text}}</div>
            <div class="controls noselect">
                <div class="line">
                    <div class="label">Query terms</div>
                    <div class="terms"><span v-for="(tq,tqi) in tokenized_query" :key="'qt'+tqi" 
                    v-bind:class="{selected1:tqi in qt_selected_indices && qt_selected_indices[tqi]==1,selected2:tqi in qt_selected_indices && qt_selected_indices[tqi]==2}" 
                    v-bind:style="controlTermStyle(tqi)" @click="qt_toggle_term(tqi)">{{tq}}&#8203;</span></div>
                </div>
                <div class="line">
                    <div class="part-line" v-bind:class="{selected:highlight_mode == 'qt'}">
                        <div class="shadow" @click="toggle_highlight_mode('qt')"></div>
                        <div class="label">Min. similarity</div>
                        <span class="range-holder"><input type="range" min="1" max="100" steps="1" v-model="qt_min_sim" class="slider"><div class="label" v-bind:style="{left:qt_min_sim+'px'}">{{qt_min_sim/100}}</div></span>
                    </div>
                        <div class="label">or</div>
                    <div class="part-line" v-bind:class="{selected:highlight_mode == 'kernel'}">
                        <div class="shadow" @click="toggle_highlight_mode('kernel')"></div>
                        <div class="label">Kernels</div>
                        <div class="kernels"><span v-for="(k,ki) in runInfo.kernels_mus" :key="'k'+ki" v-bind:class="{selected:highlight_mode == 'kernel' && ki in kernel_selected_indices}" @click="kernel_toggle_kernel(ki)">{{k}}&#8203;</span></div>
                    </div>
                </div>
            </div>
        </div>
        <div class="document" v-for="(d,di) in documentData" :key="d.id">
            <div class="head"><hr/><span class="rank">{{di+1}}</span> {{d.score.toFixed(2)}} | {{d.val_len[1].toFixed(2)}} + {{d.val_log[1].toFixed(2)}} | <span v-for="(kernel_score,ker_index) in d.val_log[0]" :key="'ks'+ker_index">{{(kernel_score[0] * kernel_score[1]).toFixed(2)}} | </span></div>
            <div class="text">
                <template v-for="(t,ti) in d.tokenized_document"><span :key="d.id + ti" v-bind:style="termStyle(di,ti)">{{t}}</span> <wbr :key="'br'+d.id + ti"/></template>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import Vue from "vue";
import FetchHelper from "../fetch-helper";


export default Vue.extend({
    props: ['query',"runInfo"],
    data() {
        return {
            documentData:<any[]>[],
            tokenized_query:<string[]>[],
            highlight_mode:'qt',
            qt_selected_indices:<any>{},
            qt_min_sim:40,
            qt_current_max:0,
            kernel_selected_indices:<any>{},
            color_palette:["rgb(44,8,69)", "rgb(91,131,19)", "rgb(37,36,249)", "rgb(182,96,30)", "rgb(132,56,186)", "rgb(31,68,7)", "rgb(222,31,138)", "rgb(29,134,109)", "rgb(223,51,64)", "rgb(19,51,70)", "rgb(122,10,24)", "rgb(22,125,187)", "rgb(176,94,112)", "rgb(69,111,231)", "rgb(90,49,0)", "rgb(208,3,214)", "rgb(114,121,110)"]//["#DB5461","#1A936F","#593C8F","#7A306C","#E16036","#171738",]
        }
    },
    methods: {
        goBack() { 
            this.$emit("back"); 
        },
        toggle_highlight_mode(new_mode:string){
            this.highlight_mode = new_mode
        },
        kernel_toggle_kernel(kernelIdx:number){
            if(!(kernelIdx in this.kernel_selected_indices)){
                this.kernel_selected_indices[kernelIdx] = 1
            }else if(this.kernel_selected_indices[kernelIdx]==1){
                delete this.kernel_selected_indices[kernelIdx]
            }
            this.$forceUpdate()
        },
        qt_toggle_term(tqi:number){
            if(!(tqi in this.qt_selected_indices)){
                this.qt_selected_indices[tqi] = 1
            }else if(this.qt_selected_indices[tqi]==1){
                this.qt_selected_indices[tqi] = 2
            }
            else if(this.qt_selected_indices[tqi]==2){
                delete this.qt_selected_indices[tqi]
            }
            this.$forceUpdate()
        },
        controlTermStyle(termIndex:number){
            if(!(termIndex in this.qt_selected_indices)){
                return {"color":"gray"}
            }
            else if(this.qt_selected_indices[termIndex]==1){
                return {"color":this.color_palette[termIndex]}
            }
            else if(this.qt_selected_indices[termIndex]==2){
                return {"backgroundColor":this.color_palette[termIndex]}
            }
        },
        termStyle(docIndex:number,termIndex:number){
            var output=<any>{
                color:"black",
                opacity:1
            }
            var mainKey="color"
            if(this.highlight_mode=="qt"){
                if(Object.keys(this.qt_selected_indices).length == 0) return output;

                var matches = this.documentData[docIndex].matches[termIndex]
                var max_val = 0
                var max_index;
                for(var index in this.qt_selected_indices){
                    var val = matches[index]
                    if(val > max_val){
                        max_val = val;
                        max_index = index;
                    }
                }

                if(max_val > this.qt_min_sim/100){
                    if(this.qt_selected_indices[<number><unknown>max_index]==2){
                        output.color="white"
                        mainKey = "backgroundColor"
                    }
                    output[mainKey] = this.color_palette[<number><unknown>max_index]
                }
                output.opacity = max_val / this.qt_current_max
                return output
            }else if(this.highlight_mode=="kernel"){
                if(Object.keys(this.kernel_selected_indices).length == 0) return output;

                var matches = this.documentData[docIndex].matches_per_kernel[termIndex]
                var max_val = 0
                var max_index;
                for(var q_index in this.qt_selected_indices){
                    for(var k_index in this.kernel_selected_indices){
                        var val = matches[q_index][k_index]
                        if(val > max_val){
                            max_val = val;
                            max_index = q_index;
                        }
                    }
                }

                if(max_val > 0.1){
                    output.color="white"
                    output["backgroundColor"] = this.color_palette[<number><unknown>max_index]
                }
                output.opacity = max_val /// this.qt_current_max
                return output
            }
        }
    },
    watch: { 
          query: function(newVal, oldVal) { // watch it
            var stopword_selection = ["where","is","a","and","in","the","are","do","does",]
            if(newVal!=""){
                this.qt_selected_indices = {}
                this.kernel_selected_indices = {2:1}
                this.documentData.length = 0
                fetch("/query/"+newVal.qid)
                    .then(FetchHelper.status)
                    .then(FetchHelper.json)
                    .then(data => {
                      this.documentData.push(...data.documents);
                      this.tokenized_query = data.documents[0].tokenized_query
                      for(var d in data.documents){
                          for(var i=0;i< data.documents[d].matches.length;i++){
                              this.qt_current_max = Math.max(this.qt_current_max,...data.documents[d].matches[i])
                      }}
                      for(var i=0;i<this.tokenized_query.length;i++){
                            this.qt_selected_indices[i] = stopword_selection.findIndex((x) => x == this.tokenized_query[i]) == -1 ? 2 : 1
                      }
                    })
                    .catch(error => {
                      console.log(error);
                    });
            }
        }
    },
    computed: {
        
    }
});
</script>

<style lang="scss">
.single-query-view {
    margin: auto;
    width: 600px;
    padding-top: 120px;

    .section-header{
        position: fixed;
        background: white;
        top: 45px;
        padding:10px;
        z-index: 100;
        width: 600px;
        .query{
            display: inline;
            font-weight: 500;
            margin:20px;
        }
    }
    .controls{
        .range-holder {
            position: relative;
            display: inline-block;
            input{
                width:100px;
                top: -3px;
            }
            .label {
                position: absolute;
                width: 20px;
                height: 20px;
                color: gray;
                top: 20px;
                margin-left: -11px;
                display: block;
            }
        }
        .line{
            margin:10px;
            .part-line{
                display: inline-block;
                position: relative;
                &:not(.selected){
                    .range-holder .label{
                        display: none;
                    }
                    .range-holder .slider::-webkit-slider-thumb{
                        background-color: gray!important;
                    }
                    .range-holder .slider::-moz-range-thumb{
                        background: gray!important;
                        }
                    .range-holder .slider::-ms-thumb{
                        background: gray!important;
                        }
                    .shadow{
                        display: block;
                        position: absolute;
                        top:0;
                        left:0;
                        right: 0;
                        bottom: 0;
                        z-index: 50;
                        opacity: 0.7;
                        background: white;
                        cursor: pointer;
                        &:hover{
                            opacity: 0.5;
                        }
                    }
                }
                &.selected .shadow{
                    display: none;
                }
            }
            
        }
        .label{
            cursor: default;
            display: inline;
        }
        .kernels{
            display: inline-block;
        }
        .kernels span{
            cursor: pointer;
            padding:4px;
            margin:1px;

            &.selected {
                background:lightgray;
                border-bottom: 2px solid blueviolet;
            }
        }
        .terms{
            display: inline-block;
        }
        .terms span{
            cursor: pointer;
            padding:5px;
            margin:10px;
            border-radius: 3px;

            &.selected2 {
                color:white;
            }
            &:not(.selected2){ 
                background: none !important;
            }
        }
    }
    .document{
        margin: 5px;
        position: relative;
        .head{
            margin: 10px 40px;
            hr{
                border: 0.5px solid #dedede;
            }
            .rank {
                border: 1px solid gray;
                border-radius: 50%;
                width: 18px;
                position: relative;
                display: inline-block;
                text-align: center;
                font-weight:500;
            }
        }
        .text{
            text-align:justify; 
            span{
                padding:0 2px;
                margin:0 1px;
                border-radius:2px
            }
        }
    }
}
</style>