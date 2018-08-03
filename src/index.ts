import Vue from "vue";
import ExploreView from "./ExploreView.vue";
import ServerSelector from "./components/ServerSelector.vue"
import "./global-styles.scss"
import '@fortawesome/fontawesome-free/css/all.css';

let v = new Vue({
    el: "#app",
    template: `
    <div>
        <header><i class="fas fa-search"></i> ir-explorer <server-selector /> </header>
        <explore-view />
    </div>
    `,
    components: {
        ExploreView,
        ServerSelector
    },
});