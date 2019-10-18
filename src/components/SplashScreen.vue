<template>
    <div class="splashscreen">
      <div class="splash-card" v-if="currentScreenIdx==0">
        <h1>Welcome to the Neural-IR-Explorer 🕵️‍♂️</h1>
        <p>
          The Neural-IR-Explorer is a interactive exploration tool. It allows you to browse around the actual results of a neural re-ranking run. 
          We focus on the text of the query and document &ndash; just as the neural re-ranking model does. This tool is meant to complement metrics-based evaluation.
          It (hopefully) enables you to gain new insights about how a neural model makes ranking decicions and how a test collection is composed (both the types of queries and the ranking judgements)
          With the Neural-IR-Explorer you can highlight and view temporary results, such as the similarities between query and document terms for the returned list of documents per query.
        </p>
        <ReRankingOverview class="ranking-overview" />
        <span class="fig-caption">Figure 1: Re-ranking overview workflow between first stage and re-ranking model</span>
        <p>Before we start exploring, let's take a quick look at the workflow shown in Figure 1. Typically, for efficiency, neural retrieval models depend on a candidate selection of documents.
           This candidate selection is provided by a traditional retrieval model (BM25 based on inverted index statistics). Therefore, in the result view of the Neural-IR-Explorer we compare the neural model results with the first stage baseline. 
           Keep in mind that this setup means that the neural model operates in a constrained environment and the requirements may differ from a full-collection retrieval.
           For a more comprehensive overview, we suggest the recent survey work by <a target="blank" href="https://www.microsoft.com/en-us/research/publication/introduction-neural-information-retrieval/">Mitra et al.</a></p>
        <div><span class="skip-button" @click="$emit('all-done')">Take me to the action!</span><span class="next-button" @click="currentScreenIdx=1">Next: The neural re-ranking model</span></div>
      </div>

      <div class="splash-card" v-if="currentScreenIdx==1">
        <template v-if="runInfo.score_type == 'tk'">
          <h2>TK: The Transformer-Kernel Model</h2>
          <p>
            Search engines operate under a strict time constraint as a fast response is paramount to user satisfaction. Thus, neural re-ranking models have a limited time-budget to re-rank documents. 
            Given the same amount of time, a faster re-ranking model can incorporate more documents than a less efficient one, leading to a higher effectiveness. 
            To utilize this property, we propose TK (Transformer-Kernel): a neural re-ranking model for ad-hoc search using an efficient contextualization mechanism. 
            TK employs a very small number of Transformer layers (up to three) to contextualize query and document word embeddings. 
            To score individual term interactions, we use a document-length enhanced kernel-pooling, which enables users to gain insight into the model. 
            TK offers an optimal ratio between effectiveness and efficiency: under realistic time constraints (maximum of 200 ms per query) TK achieves the highest effectiveness in comparison to BERT and other re-ranking models.
            The Neural-IR-Explorer is meant to complement metrics based results found in the TK paper <a target="blank" href="https://arxiv.org">on arXiv</a> (there is also a cool time-budget aware evaluation of neural IR models in there 👌)</p>

          <TkArchitecture class="tk-arch" />
          <span class="fig-caption">Figure 2: TK model overview</span>
          <p>We employ a small number of Transformer layers (we evaluate up to three) to contextualize query and document word embeddings.
             We score the interactions of the contextualized representations with simple, yet effective soft-histograms based on the kernel-pooling technique. 
             Additionally, we enhance kernel-pooling with document length normalization.
          <div><span class="next-button" @click="$emit('all-done')">Let's go!</span></div>
        </template>
        <template v-if="runInfo.score_type == 'knrm'">
          <h2>KNRM: Kernel-pooling based re-ranking</h2>
          <p>
            <i style="color:gray">Chenyan Xiong, Zhuyun Dai, Jamie Callan, Zhiyuan Liu, and Russell Power. 2017. End-to-End Neural Ad-hoc Ranking with Kernel Pooling. In Proc. of SIGIR.</i><br/>
            The KNRM (Kernel-based Neural Ranking) model counts the amount of different similarities between the query and document term representations via a differentiable soft-histogram (Gaussian kernel functions).
            It has very few learnable parameters (other than the embedding) &ndash; only the kernel bin weights are trained. Therefore, KNRM is very fast as there is no complicated architecture increasing the runtime.
          </p>
          <KnrmArchitecture class="knrm-arch" />
          <span class="fig-caption">Figure 2: KNRM model overview</span>
          <p>
            The single cosine interaction matrix allows to inspect the model at this point. In this demo we make use of this fact to highlight exactly those interactions as well as the internal kernel scores before summing them up to the final score
            The original paper is available <a target="blank" href="https://arxiv.org/pdf/1706.06613.pdf">on arXiv</a>.
            More information can also be found in our IR course slides <a target="blank" href="https://github.com/sebastian-hofstaetter/teaching/tree/master/advanced-information-retrieval/lectures">on GitHub</a>.
          </p>
          <div><span class="next-button" @click="$emit('all-done')">Let's go!</span></div>
        </template>
      </div>

    </div>
</template>

<script lang="ts">
import Vue from "vue";
import { AvailableConfiguration, ConfigParameterType } from "../models";
import FetchHelper from "../fetch-helper";

import ReRankingOverview from '../figures/re-ranking-overview.svg';
import TkArchitecture from '../figures/tk_architecture.svg';
import KnrmArchitecture from '../figures/knrm_architecture.svg';

export default Vue.extend({
  props: ['runInfo'],
  data() {
    return {
      currentScreenIdx:0,
    };
  },
  methods: {
    
  },
  created: function() {

  },
  components:{ReRankingOverview,TkArchitecture,KnrmArchitecture}
});
</script>

<style lang="scss">

.splashscreen{
  max-width: 600px;
  margin: auto;
  text-align: center;
  margin-top: 60px;
  
  .splash-card{
    h1,h2{
      font-weight: 500;
      text-align: left;
    }
    p{
      text-align: justify;
      line-height: 13pt;
    }
    .fig-caption{
      display: inline-block;
      font-style: italic;
      margin-bottom: 30px;
    }
  }
  .next-button{
    padding: 8px;
    display: inline-block;
    margin: 10px;
    cursor: pointer;
    background: #e3c9f8;
    border-radius: 4px;
    border: 1px solid #411c5b;
    color: #411c5b;
    font-weight: 500;
  }
  .skip-button{
    padding: 5px;
    display: inline-block;
    margin: 10px;
    cursor: pointer;
    background: #f1f1f1;
    border-radius: 4px;
    border: 1px solid #ccc;
  }
}

.ranking-overview{
  margin-left:-150px;
  margin-bottom: -25px;
  fill:none;fill-rule:evenodd;font-size:11px;overflow:visible;stroke-linecap:square;stroke-miterlimit:3;
	.st1 {fill:#e3c9f8;stroke:#411c5b;stroke-width:1}
	.st2 {fill:#411c5b;font-size:1.00001em}
	.st3 {font-size:1em}
	.st4 {fill:none;stroke:none;stroke-width:0.25}
	.st5 {fill:#833c0b;font-size:1.00001em}
	.st6 {marker-end:url(#mrkr1-13);stroke:#7f7f7f;stroke-linecap:round;stroke-linejoin:round;stroke-width:1}
	.st7 {fill:#7f7f7f;fill-opacity:1;stroke:#7f7f7f;stroke-opacity:1;stroke-width:0.28409090909091}
	.st8 {stroke:#c55a11;stroke-width:1}
	.st9 {fill:#3f3f3f;font-size:1.00001em}
	.st10 {fill:#f4b183;stroke:#c55a11;stroke-width:1}
	.st11 {fill:#000000;font-size:1.00001em}
	.st12 {fill:#f2f2f2;stroke:#3f3f3f;stroke-width:1}
	.st13 {fill:#7f7f7f;font-size:1em;font-style:italic}
	.st14 {fill:#7030a0;font-size:1.00001em}
	.st15 {stroke:#c514ae;stroke-width:1}
	.st16 {stroke:#7f7f7f;stroke-linecap:round;stroke-linejoin:round;stroke-width:1}
}

.knrm-arch{
.st1 {fill:#90aadb;fill-opacity:0.17;stroke:#305497;stroke-dasharray:0.01,2.5;stroke-width:0.5}
		.st2 {marker-end:url(#mrkr1-10);stroke:#7f7f7f;stroke-linecap:round;stroke-linejoin:round;stroke-width:1}
		.st3 {fill:#7f7f7f;fill-opacity:1;stroke:#7f7f7f;stroke-opacity:1;stroke-width:0.28409090909091}
		.st4 {fill:#fff2cc;stroke:none;stroke-width:0.25}
		.st5 {fill:#ffd965;stroke:none;stroke-width:0.25}
		.st6 {fill:#fbe5d5;stroke:none;stroke-width:0.25}
		.st7 {fill:#f4b183;stroke:none;stroke-width:0.25}
		.st8 {fill:none;stroke:none;stroke-width:0.25}
		.st9 {fill:#a5a5a5;font-family:Calibri;font-size:0.75em}
		.st10 {fill:#7f7f7f;font-family:Calibri;font-size:1.00001em}
		.st11 {marker-end:url(#mrkr1-66);stroke:#d8d8d8;stroke-linecap:round;stroke-linejoin:round;stroke-width:0.5}
		.st12 {fill:#d8d8d8;fill-opacity:1;stroke:#d8d8d8;stroke-opacity:1;stroke-width:0.25773195876289}
		.st13 {fill:#7030a0;stroke:none;stroke-width:0.25}
		.st14 {marker-end:url(#mrkr1-74);stroke:#7f7f7f;stroke-linecap:round;stroke-linejoin:round;stroke-width:1}
		.st15 {fill:#7f7f7f;fill-opacity:1;stroke:#7f7f7f;stroke-opacity:1;stroke-width:0.40983606557377}
		.st16 {fill:#e2efd9;stroke:none;stroke-width:0.25}
		.st17 {fill:#a8d08d;stroke:none;stroke-width:0.25}
		.st18 {fill:#538135;stroke:none;stroke-width:0.25}
		.st19 {fill:#bdd0e9;stroke:#305497;stroke-width:0.75}
		.st20 {stroke:#002060;stroke-linecap:round;stroke-linejoin:round;stroke-width:0.75}
		.st21 {fill:none;stroke:#305497;stroke-width:0.75}
		.st22 {fill:#000000;font-family:Calibri Light;font-size:1.16666em}
		.st23 {fill:#dae2f3;stroke:none;stroke-width:0.25}
		.st24 {fill:#759fcc;stroke:none;stroke-width:0.25}
		.st25 {fill:none;stroke:#000000;stroke-width:0.25}
		.st26 {fill:#a5a5a5;font-family:Calibri Light;font-size:0.75em}
		.st27 {fill:#d8d8d8;stroke:none;stroke-width:0.25}
		.st28 {fill:#595959;stroke:none;stroke-width:0.25}
		.st29 {fill:#a5a5a5;stroke:none;stroke-width:0.25}
		.st30 {marker-start:url(#mrkr1-167);stroke:#7f7f7f;stroke-linecap:round;stroke-linejoin:round;stroke-width:1}
		.st31 {fill:#e3c9f8;stroke:none;stroke-width:0.25}
		.st32 {stroke:#7030a0;stroke-linecap:round;stroke-linejoin:round;stroke-width:1}
		.st33 {fill:#000000;font-family:Calibri;font-size:0.75em}
		.st34 {fill:#7f7f7f;font-family:Calibri;font-size:0.833336em}
		.st35 {stroke:#ed7d31;stroke-width:1}
		.st36 {fill:#ed7d31;font-family:Calibri;font-size:0.666664em}
		.st37 {stroke:#70ad47;stroke-width:1}
		.st38 {fill:#70ad47;font-family:Calibri;font-size:0.666664em}
		.st39 {stroke:#4672c4;stroke-width:1}
		.st40 {fill:#305497;font-family:Calibri;font-size:0.666664em}
		.st41 {fill:#000000;font-family:Latin Modern Math;font-size:0.833336em;font-style:italic}
		.st42 {stroke:#7030a0;stroke-width:1}
		.st43 {fill:#7030a0;font-family:Calibri;font-size:0.666664em}
		fill:none;fill-rule:evenodd;font-size:12px;overflow:visible;stroke-linecap:square;stroke-miterlimit:3
}

.tk-arch{
      margin-left: -150px;
    margin-bottom: -55px;
        margin-top: -45px;
  .st1 {fill:#f2f2f2;stroke:none;stroke-width:0.25}
		.st2 {fill:#90aadb;fill-opacity:0.17;stroke:#305497;stroke-dasharray:0.01,2.5;stroke-width:0.5}
		.st3 {fill:#f2f2f2;fill-opacity:0.17;stroke:#7f7f7f;stroke-dasharray:3.5,2.5;stroke-width:0.5}
		.st4 {fill:#fafafa;stroke:#7f7f7f;stroke-width:0.5}
		.st5 {marker-end:url(#mrkr1-22);stroke:#7f7f7f;stroke-linecap:round;stroke-linejoin:round;stroke-width:1}
		.st6 {fill:#7f7f7f;fill-opacity:1;stroke:#7f7f7f;stroke-opacity:1;stroke-width:0.28409090909091}
		.st7 {fill:#fff2cc;stroke:none;stroke-width:0.25}
		.st8 {fill:#ffd965;stroke:none;stroke-width:0.25}
		.st9 {fill:#fbe5d5;stroke:none;stroke-width:0.25}
		.st10 {fill:#f4b183;stroke:none;stroke-width:0.25}
		.st11 {fill:none;stroke:none;stroke-width:0.25}
		.st12 {fill:#7f7f7f;font-family:Calibri;font-size:1.00001em}
		.st13 {fill:#000000;stroke:none;stroke-width:0.25}
		.st14 {fill:#e2efd9;stroke:none;stroke-width:0.25}
		.st15 {fill:#a8d08d;stroke:none;stroke-width:0.25}
		.st16 {fill:#bdd0e9;stroke:#305497;stroke-width:0.75}
		.st17 {stroke:#002060;stroke-linecap:round;stroke-linejoin:round;stroke-width:0.75}
		.st18 {fill:none;stroke:#305497;stroke-width:0.75}
		.st19 {fill:#dae2f3;stroke:#4672c4;stroke-width:0.25}
		.st20 {fill:#002060;stroke:none;stroke-width:0.25}
		.st21 {fill:#759fcc;stroke:none;stroke-width:0.25}
		.st22 {stroke:#7f7f7f;stroke-linecap:round;stroke-linejoin:round;stroke-width:1}
		.st23 {fill:#7f7f7f;font-family:Calibri;font-size:0.666664em}
		.st24 {stroke:#7030a0;stroke-width:1}
		.st25 {fill:#7030a0;font-family:Calibri;font-size:0.75em}
		.st26 {stroke:#70ad47;stroke-width:1}
		.st27 {fill:#70ad47;font-family:Calibri;font-size:0.75em}
		.st28 {stroke:#4672c4;stroke-width:1}
		.st29 {fill:#305497;font-family:Calibri;font-size:0.75em}
		.st30 {fill:#000000;font-family:Times New Roman;font-size:0.75em;font-style:italic}
		.st31 {baseline-shift:-32.4951%;font-size:0.649902em}
		.st32 {font-size:1em}
		.st33 {fill:none;stroke:#7f7f7f;stroke-width:0.25}
		.st34 {stroke:#a5a5a5;stroke-linecap:round;stroke-linejoin:round;stroke-width:0.75}
		.st35 {fill:#3c63ac;stroke:#000000;stroke-linecap:round;stroke-linejoin:round;stroke-width:0.75}
		.st36 {stroke:#7f7f7f;stroke-dasharray:3,3;stroke-linecap:round;stroke-linejoin:round;stroke-width:1}
		.st37 {marker-end:url(#mrkr1-205);stroke:#7f7f7f;stroke-linecap:round;stroke-linejoin:round;stroke-width:1}
		.st38 {fill:#7f7f7f;fill-opacity:1;stroke:#7f7f7f;stroke-opacity:1;stroke-width:0.40983606557377}
		.st39 {stroke:#7f7f7f;stroke-width:1}
		.st40 {fill:#000000;font-family:Cambria Math;font-size:0.75em}
		.st41 {fill:#a5a5a5;stroke:none;stroke-width:0.25}
		.st42 {fill:#7030a0;stroke:none;stroke-width:0.25}
		.st43 {fill:#d8d8d8;stroke:none;stroke-width:0.25}
		.st44 {fill:#e3c9f8;stroke:#7030a0;stroke-width:0.75}
		.st45 {stroke:#411c5b;stroke-linecap:round;stroke-linejoin:round;stroke-width:0.5}
		.st46 {fill:none;stroke:#7030a0;stroke-width:0.75}
		.st47 {fill:#c514ae;stroke:none;stroke-width:0.25}
		.st48 {fill:#f5eef7;stroke:#7030a0;stroke-width:0.5}
		.st49 {stroke:#7f7f7f;stroke-linecap:butt;stroke-width:1}
		.st50 {fill:#e3c9f8;stroke:none;stroke-width:0.25}
		.st51 {stroke:#7030a0;stroke-linecap:round;stroke-linejoin:round;stroke-width:1}
		.st52 {visibility:visible}
		.st53 {fill:#7f7f7f;filter:url(#filter_2.6666667461395);stroke:none}
		.st54 {fill:none;filter:url(#filter_2.6666667461395);stroke:#7f7f7f;stroke-linecap:round;stroke-linejoin:round}
		.st55 {fill:#000000;font-family:Calibri;font-size:0.75em}
		.st56 {fill:#e39be8;fill-opacity:0.17;stroke:#7030a0;stroke-dasharray:0.01,2.5;stroke-width:0.5}
		.st57 {fill:#411c5b;stroke:none;stroke-width:0.25}
		.st58 {marker-end:url(#mrkr1-371);stroke:#000000;stroke-linecap:round;stroke-linejoin:round;stroke-width:0.5}
		.st59 {fill:#000000;fill-opacity:1;stroke:#000000;stroke-opacity:1;stroke-width:0.25773195876289}
		.st60 {fill:none;stroke:#7030a0;stroke-width:1}
		.st61 {fill:none;stroke:#7030a0;stroke-linecap:round;stroke-linejoin:round;stroke-width:0.75}
		.st62 {marker-start:url(#mrkr1-446);stroke:#7f7f7f;stroke-linecap:round;stroke-linejoin:round;stroke-width:1}
		.st63 {fill:#000000;font-family:Calibri Light;font-size:1.16666em}
		.st64 {fill:#a5a5a5;font-family:Calibri;font-size:0.75em}
		.st65 {fill:#a5a5a5;font-family:Calibri Light;font-size:0.75em}
		.st66 {fill:#4672c4;fill-opacity:0.36;stroke:#002060;stroke-dasharray:0,2.25;stroke-linecap:round;stroke-linejoin:round;stroke-width:0.75}
		.st67 {fill:#dae2f3;stroke:none;stroke-width:0.25}
		.st68 {stroke:#002060;stroke-linecap:round;stroke-linejoin:round;stroke-width:1}
		.st69 {fill:#595959;font-family:Calibri;font-size:0.583328em}
		.st70 {stroke:#bfbfbf;stroke-linecap:round;stroke-linejoin:round;stroke-width:0.5}
		.st71 {fill:#3f3f3f;font-family:Times New Roman;font-size:0.75em;font-style:italic}
		.st72 {fill:#3f3f3f;font-family:Times New Roman;font-size:0.811964em;font-style:italic}
		.st73 {baseline-shift:-33.35%;font-size:0.667em}
		.st74 {fill:#002060;font-family:Times New Roman;font-size:0.75em;font-style:italic}
		fill:none;fill-rule:evenodd;font-size:12px;overflow:visible;stroke-linecap:square;stroke-miterlimit:3
}
</style>