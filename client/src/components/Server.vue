<template>
  <article class="tile is-child">
    <template v-if="server">
      <p class="title">{{ server.hostname }}</p>
      <p class="subtitle">{{ server.query_time }}</p>
      <ul>
        <li v-for="gpu in server.gpus" :key="gpu.index">
          <p>{{ gpu.index }}</p>
          <p>{{ gpu["utilization.gpu"] }}%</p>
          <progress class="progress is-primary" :value="gpu['utilization.gpu']" max="100"></progress>
          <p>{{ gpu["memory.used"] }}MiB/{{ gpu["memory.total"] }}MiB</p>
          <progress
            class="progress is-danger"
            :value="gpu['memory.used']"
            max="gpu['memory.total']"
          ></progress>
        </li>
      </ul>
    </template>
    <template v-else>
      <h1>FUCK</h1>
    </template>
  </article>
</template>

<script>
export default {
  props: ["server"]
};
</script>
