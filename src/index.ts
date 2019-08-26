import Vue from "vue";
import ExploreView from "./ExploreView.vue";
import RunInfoBox from "./components/RunInfoBox.vue"
import "./global-styles.scss"
import '@fortawesome/fontawesome-free/css/all.css';

let v = new Vue({
    el: "#app",
    template: `
    <div>
        <header><div class="inner-header"><i class="fas fa-search"></i> neural-ir-explorer <run-info-box @run-changed="(x) => {currentRun = x}" /></div></header>
        <explore-view v-bind:run-info="currentRun" />
        <footer><div class="inner-footer"> Made with <i class="fa fa-heart"></i> by Sebastian Hofstätter</div></footer>
    </div>
    `,
    data(){
        return {currentRun:{}}
    },
    components: {
        ExploreView,
        RunInfoBox
    },
});