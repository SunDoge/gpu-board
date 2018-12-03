<template>
  <div id="app">
    <section class="section">
      <div class="tile is-ancestor">
        <server-e-chart v-for="(addr,key) in servers" :key="key" :addr="addr"></server-e-chart>
      </div>
    </section>
    <my-footer></my-footer>
  </div>
</template>

<script>
import MyFooter from "./components/MyFooter.vue";
import ServerEChart from "./components/serverEChart.vue";
import config from "./config.js";

export default {
  name: "app",
  components: {
    // Server,
    MyFooter,
    ServerEChart
  },
  data: function() {
    return {
      servers: {},
      sockets: {}
    };
  },
  mounted: function() {
    // eslint-disable-next-line
    console.log(config);

    const servers = config.servers;
    this.servers = Object.assign({}, this.servers, servers);
  }
};
</script>

<style>
@import "../node_modules/bulma/css/bulma.css";
@import "../node_modules/@fortawesome/fontawesome-free/css/all.css";
.tile{
  padding:0 50px;
  display: flex;
  flex-flow: row wrap;
  justify-content: space-around;
  align-items:center;
  align-content: space-around;
}
</style>
