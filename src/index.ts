import Vue from "vue";
import ExploreView from "./ExploreView.vue";
import "./global-styles.scss"

let v = new Vue({
    el: "#app",
    template: `
    <div>
        <header>ir-explorer</header>
        <explore-view />
    </div>
    `,
    components: {
        ExploreView,

    },
});