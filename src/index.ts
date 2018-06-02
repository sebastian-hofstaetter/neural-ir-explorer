import Vue from "vue";
import ExploreView from "./ExploreView.vue";
import ExplorationSearch from "./components/ExplorationSearch.vue"
import ConfigurationSelector from "./components/ConfigurationSelector.vue"

let v = new Vue({
    el: "#app",
    template: `
    <div>
        <header>ir-explorer</header>
        <explore-view />
    </div>
    `,
    data: { name: "World" }, 
    components: {
        ExploreView,
        //ExplorationSearch,
        //ConfigurationSelector

    },
});