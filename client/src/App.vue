<template>
  <div id="app">
    <section class="section">
      <div class="tile is-ancestor">
        <server v-for="(server, addr) in servers" :key="addr" :server="server"></server>
      </div>
    </section>
    <my-footer></my-footer>
  </div>
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'
import Server from "./components/Server.vue";
import MyFooter from "./components/MyFooter.vue";
import config from "./config.js";
import io from "socket.io-client";

export default {
  name: "app",
  components: {
    Server,
    MyFooter
  },
  data: function() {
    return {
      servers: {},
      sockets: {}
    };
  },
  created: function() {
    // eslint-disable-next-line
    console.log(config);

    const servers = config.servers;

    for (let addr of servers) {
      // eslint-disable-next-line
      console.log(addr);
      const socket = io(addr);
      // eslint-disable-next-line
      console.log(socket);
      this.servers[addr] = null;
      socket.on("gpustat", data => {
        // this.servers[addr] = data;
        const server = {};
        server[addr] = data;
        this.servers = Object.assign({}, this.servers, server);
        // eslint-disable-next-line
        // console.log(this.servers);
      });
      this.sockets[addr] = socket;
    }
  }
};
</script>

<style>
@import "../node_modules/bulma/css/bulma.css";
@import "../node_modules/@fortawesome/fontawesome-free/css/all.css";
</style>
