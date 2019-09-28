<template>
    <div class="single-query-view" v-bind:style="{paddingTop: headerHeight+'px'}">
        <div class="section-header" ref="header">
            <div class="cluster-card info-card" v-if="showInfoBox">
              <div class="close-info" @click="showInfoBox=false"><i class="fas fa-times"></i></div>
              <h1>Alright, now for the details 🔬</h1>
              <p>Here is what you see around you and what you can do with it:
                  <ul>
                      <li>At the top you can select which query terms to highlight: we have two different styles: text-color and background color. (We use it to focus on specific terms)</li>
                      <li>There are two highlighting modes: vector-to-vector minimum similarity (with the slider) and per kernel (as the neural model sees the similarities)</li>
                      <li>Compare two documents side-by-side by selecting them with the compare button <i class="far fa-clone"></i></li>
                  </ul>
              </p>
            </div>
            <div class="controls noselect">
                <div class="line">
                    <span class="back-button" @click="goBack()"><i class="fa fa-chevron-left"></i></span>
                    <div class="terms">
                        <template  v-for="(tq,tqi) in tokenized_query"><span :key="'qt'+tqi" 
                    v-bind:class="{selected1:tqi in qt_selected_indices && qt_selected_indices[tqi]==1,selected2:tqi in qt_selected_indices && qt_selected_indices[tqi]==2}" 
                    v-bind:style="controlTermStyle(tqi)" @click="qt_toggle_term(tqi)">{{tq}}</span>  <wbr :key="'qtbr'+tqi"/></template></div>
                </div>
                <div class="line center">
                    <div class="part-line" v-bind:class="{selected:highlight_mode == 'qt'}">
                        <div class="shadow" @click="toggle_highlight_mode('qt')"></div>
                        <div class="label">Min. similarity</div>
                        <span class="range-holder"><input type="range" min="1" max="100" steps="1" v-model="qt_min_sim" class="slider"><div class="label" v-bind:style="{left:qt_min_sim+'px'}">{{qt_min_sim/100}}</div></span>
                    </div>
                        <div class="label">or</div>
                    <div class="part-line" v-bind:class="{selected:highlight_mode == 'kernel'}">
                        <div class="shadow" @click="toggle_highlight_mode('kernel')"></div>
                        <div class="label">Kernels</div>
                        <div class="kernels"><span v-for="(k,ki) in runInfo.kernels_mus_display" :key="'k'+ki" v-bind:class="{selected:highlight_mode == 'kernel' && ki in kernel_selected_indices}" @click="kernel_toggle_kernel(ki)">{{k}}&#8203;</span></div>
                    </div>
                </div>
                <div class="line heading" v-if="currentDisplayMode == 'list' && runInfo.kernels_mus_display != undefined">
                    <span class="rank">Rank</span>
                    <span class="main-score">Score (length & log)</span>
                    <span class="kernels">Log-Kernel scores: <span>{{runInfo.kernels_mus_display[0]}} to {{runInfo.kernels_mus_display[runInfo.kernels_mus_display.length-1]}} & rest </span></span>
                </div>
            </div>
        </div>
        <div class="full-list" v-if="currentDisplayMode == 'list'">
            <div class="document" v-for="(d,di) in documentData" :key="d.id">
                <div class="head"><hr v-if="di>0" /><span v-if="d.judged_relevant" class="star" title="Judged as relevant">⭐</span><span class="rank">{{di+1}}</span><span class="main-score"> <b>{{d.score.toFixed(2)}}</b> ({{(d.val_len[1]*runInfo['model_weights_log_len_mix'][1]).toFixed(2)}} & {{(d.val_log[1]*runInfo['model_weights_log_len_mix'][0]).toFixed(2)}})</span> <span class="kernel-value" v-bind:class="{selected: highlight_mode == 'kernel' && ker_index in kernel_selected_indices}" v-for="(kernel_score,ker_index) in d.val_log[0]" :key="'ks'+ker_index">{{(kernel_score[0] * kernel_score[1] * runInfo['model_weights_log_len_mix'][0]).toFixed(2)}} </span> <span>{{(d.val_log[2]* runInfo['model_weights_log_len_mix'][0]).toFixed(2)}}</span>
                <a class="compare-button" v-bind:class="{selected:di in comparing_documentDataIds}" @click="addToCompare(di)"><i class="far fa-clone"></i></a>
                </div>
                <div class="text">
                    <template v-for="(t,ti) in d.tokenized_document"><span :key="d.id + ti" v-bind:style="termStyle(documentData,di,ti)">{{t}}</span> <wbr :key="'br'+d.id + ti"/></template>
                </div>
            </div>
        </div>
        <div class="side-by-side" v-if="currentDisplayMode == 'side-by-side'">
            <div class="document" v-bind:class="{left: di == 0,right: di == 1}" v-for="(d,di) in comparing_documentData" :key="d.id">
                <div class="head">
                <template v-if="di == 0">
                    <div class="legend"><span>Score</span><hr/><span>Len-score</span><span>Log-score</span><span><i>Kernels</i></span><span v-for="(k,ki) in runInfo.kernels_mus_display" :key="'k2'+ki" v-bind:class="{selected:highlight_mode == 'kernel' && ki in kernel_selected_indices}" @click="kernel_toggle_kernel(ki)">{{k}}</span></div>
                    <div class="values"><span>{{d.score.toFixed(2)}}</span><hr/><span>{{(d.val_len[1]* runInfo['model_weights_log_len_mix'][1]).toFixed(2)}}</span><span>{{(d.val_log[1]* runInfo['model_weights_log_len_mix'][0]).toFixed(2)}}</span><br/><span class="kernel-value" v-bind:class="{selected: highlight_mode == 'kernel' && ker_index in kernel_selected_indices}" v-for="(kernel_score,ker_index) in d.val_log[0]" :key="'ks'+ker_index">{{(kernel_score[0] * kernel_score[1]* runInfo['model_weights_log_len_mix'][0]).toFixed(2)}}</span></div>
                    <div class="diffs"><UpDownScore v-bind:score1="comparing_documentData[0].score" v-bind:score2="comparing_documentData[1].score" maxDec="2" /><hr/><UpDownScore v-bind:score1="comparing_documentData[0].val_len[1]* runInfo['model_weights_log_len_mix'][1]" v-bind:score2="comparing_documentData[1].val_len[1]* runInfo['model_weights_log_len_mix'][1]" maxDec="2" /><UpDownScore v-bind:score1="comparing_documentData[0].val_log[1]* runInfo['model_weights_log_len_mix'][0]" v-bind:score2="comparing_documentData[1].val_log[1]* runInfo['model_weights_log_len_mix'][0]" maxDec="2" /> <br/> <UpDownScore v-for="i_mus in runInfo.kernels_mus_display.length" v-bind:key="'kdiffmus'+i_mus" v-bind:score1="comparing_documentData[0].val_log[0][i_mus-1][0] * comparing_documentData[0].val_log[0][i_mus-1][1]*runInfo['model_weights_log_len_mix'][0]" v-bind:score2="comparing_documentData[1].val_log[0][i_mus-1][0]*comparing_documentData[1].val_log[0][i_mus-1][1]*runInfo['model_weights_log_len_mix'][0]" maxDec="2" /></div>                   
                </template>
                <template v-if="di == 1">
                    <div class="values"><span>{{d.score.toFixed(2)}}</span><hr/><span>{{(d.val_len[1]* runInfo['model_weights_log_len_mix'][1]).toFixed(2)}}</span><span>{{(d.val_log[1]* runInfo['model_weights_log_len_mix'][0]).toFixed(2)}}</span><br/><span class="kernel-value" v-bind:class="{selected: highlight_mode == 'kernel' && ker_index in kernel_selected_indices}" v-for="(kernel_score,ker_index) in d.val_log[0]" :key="'ks'+ker_index">{{(kernel_score[0] * kernel_score[1]* runInfo['model_weights_log_len_mix'][0]).toFixed(2)}}</span></div>
                </template>
                </div>
                <div class="text">
                    <template v-for="(t,ti) in d.tokenized_document"><span :key="d.id + ti" v-bind:style="termStyle(comparing_documentData,di,ti)">{{t}}</span> <wbr :key="'br'+d.id + ti"/></template>
                </div>
            </div>
            <a @click="goToList()">Go back to all</a>
        </div>
    </div>
</template>

<script lang="ts">
import Vue from "vue";
import FetchHelper from "../fetch-helper";
import UpDownScore from "./UpDownScore.vue";


export default Vue.extend({
    props: ['query',"runInfo"],
    data() {
        return {
            headerHeight:0,
            documentData:<any[]>[],
            comparing_documentData:<any[]>[],
            comparing_documentDataIds:<any[]>{},
            comparing_diffData:{},
            tokenized_query:<string[]>[],
            highlight_mode:'qt',
            qt_selected_indices:<any>{},
            qt_min_sim:40,
            qt_current_max:0,
            kernel_selected_indices:<any>{},
            showInfoBox:true,
            showInfoBoxModel:false,
            currentDisplayMode:"list",
            color_palette:["rgb(44,8,69)", "rgb(91,131,19)", "rgb(37,36,249)", "rgb(182,96,30)", "rgb(132,56,186)", "rgb(31,68,7)", "rgb(222,31,138)", "rgb(29,134,109)", "rgb(223,51,64)", "rgb(19,51,70)", "rgb(122,10,24)", "rgb(22,125,187)", "rgb(176,94,112)", "rgb(69,111,231)", "rgb(90,49,0)", "rgb(208,3,214)", "rgb(114,121,110)"]//["#DB5461","#1A936F","#593C8F","#7A306C","#E16036","#171738",]
        }
    },
    methods: {
        goBack() { 
            this.$emit("back"); 
        },
        goToList(){
            this.comparing_documentData.length=0
            this.comparing_documentDataIds={}
                this.currentDisplayMode = "list"
        },
        addToCompare(didx:number){
            this.comparing_documentDataIds[didx]=1
            this.comparing_documentData.push(this.documentData[didx]);
            if(this.comparing_documentData.length == 2){
                this.currentDisplayMode = "side-by-side"
                this.showInfoBox=false

                this.comparing_diffData["score"] = this.comparing_documentData[0].score - this.comparing_documentData[1].score;
            }
            this.$forceUpdate()
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
        termStyle(documentData:any,docIndex:number,termIndex:number){
            var output=<any>{
                color:"black",
                opacity:1
            }
            var mainKey="color"
            if(this.highlight_mode=="qt"){
                if(Object.keys(this.qt_selected_indices).length == 0) return output;

                var matches = documentData[docIndex].matches[termIndex]
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

                var matches = documentData[docIndex].matches_per_kernel[termIndex]
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

                if(max_val > 0.02){
                    if(this.qt_selected_indices[<number><unknown>max_index]==2){
                        output.color="white"
                        mainKey = "backgroundColor"
                    }
                    output[mainKey] = this.color_palette[<number><unknown>max_index]

                    //output.color="white"
                    //output["backgroundColor"] = this.color_palette[<number><unknown>max_index]
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
                this.comparing_documentData.length = 0
                this.comparing_documentDataIds= {}
                this.currentDisplayMode = "list"
                fetch("/query/"+this.runInfo.id+"/"+newVal.qid)
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
                      requestAnimationFrame(()=>{
                          this.headerHeight = this.$refs.header.clientHeight
                          this.$forceUpdate();
                      })
                    })
                    .catch(error => {
                      console.log(error);
                    });
            }
        }
    },
    computed: {
        
    },
    components:{UpDownScore}
});
</script>

<style lang="scss">
.single-query-view {
    margin: auto;
    width: 600px;
    padding-top: 120px;
    margin-top: 50px;
    .section-header{
        position: fixed;
        background: white;
        top: 47px;
        z-index: 100;
        width: 600px;
        .query{
            display: inline;
            font-weight: 500;
            margin:20px;
        }
        .cluster-card{
            position: absolute;
            right: 100%;
            margin-top: 0;
            margin-right: 20px;
            display: inline-block;
            border: 1px solid #d5d5d5;
            border-radius: 2px;
            box-shadow: 2px 2px 8px #e6e6e6;
            padding: 10px;
            width: 400px;
        }
        .back-button{
            width: 13px;
            height: 18px;
            display: inline-block;
            text-align: center;
            vertical-align: middle;
            padding: 7px;
            border-right: 1px solid #c7c7c7;
            margin: -10px;
            margin-right: 10px;
            cursor: pointer;

            &:hover{
                color:blueviolet
            }
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
                margin-left: -9px;
                display: block;
            }
        }
        .line{
            padding: 10px 0;
            &.center{
                padding-left: 40px;
            }
            &.heading{
                padding-top: 20px;
                color: gray;
            }
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

            .rank{
                margin-left:40px;
                margin-right: 10px;
            }
            .main-score{
                margin-right: 25px;
            }
            .kernels{

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
            line-height: 32px;
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
                margin: 10px 0;
            }
            .rank {
                border: 1px solid gray;
                border-radius: 50%;
                width: 18px;
                position: relative;
                display: inline-block;
                text-align: center;
                font-weight:500;
                    margin-right: 10px;
            }
            .main-score{
                width: 145px;
                display: inline-block;
            }
            .kernel-value{
                margin:0 3px;
                display: inline-block;
            }
            .kernel-value.selected{
                font-weight: 500;
                text-decoration: underline;
            }
            .star{
                display: inline-block;
                position: absolute;
                margin-left: -30px;
                cursor: default;
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
        .compare-button{
            opacity: 0.3;
            cursor: pointer;
            padding: 5px;
            margin-left: 20px;
            &.selected{
                opacity:1;
                background: blueviolet;
                border-radius: 2px;
                color:white;
            }
        }
        &:hover{
            .compare-button{
                opacity:1;
            }
        }
    }
    .side-by-side{
        width: 1200px;
        margin-left: -300px;
        text-align: center;
        a{
            display: inline-block;
            text-align: center;
            margin: 20px;
            cursor: pointer;
        }
        .document{
            display: inline-block;
            width: 620px;
            vertical-align: top;
            .head{
                margin:0;
            }
            .legend{
                width: 60px;
                float: left;
                span{
                    display: block;
                }
            }
            .values{
                display: inline-block;
                width: 50px;
                text-align: right;
                span{
                    display: block;
                }
            }
            .diffs{
                float: right;
                width:50px;
                span{
                    margin: 0;
                    display: block;
                }
            }
            &.left{
                .text{
                    margin-right: 220px;
                }
                .head{
                    float: right;
                    width: 180px;
                    margin-right:0;
                    text-align: left;
                }
            }
            &.right{
                width: 500px;
                .text{
                    margin-left: 72px;
                }
                .head{
                    float: left;
                    width: 60px;
                    text-align: left;
                    margin-left: 0;
                }
            }
        }
    }
}
</style>