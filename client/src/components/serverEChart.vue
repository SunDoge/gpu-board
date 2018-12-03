<template>
  <div :id="addr" class="serverChart"></div>
</template>
<script>
import io from "socket.io-client";
import echarts from "echarts";
export default {
  name: "eChart",
  props: ["addr"],
  data: function() {
    return {
      gpus: [],
      hostname: "",
      updateTime: "",
      mychart: {}
    };
  },
  mounted() {
    let self = this;
    self.socketIO();
  },
  methods: {
    socketIO: function() {
      let self = this;
      const socket = io(self.addr);
      socket.on("gpustat", data => {
        self.$data.hostname = data.hostname;
        self.$data.gpus = data.gpus;
        self.$data.updateTime = data.query_time;
        self.drawFig();
      });
    },
    drawFig: function() {
      const self = this;
      self.mychart = echarts.init(document.getElementById(self.addr));
      self.mychart.setOption({
        title: {
          text: self.hostname,
          subtext: self.addr + "\n" + self.updateTime
        },
        yAxis: {
          data: (function() {
            let y = [];
            for (let i in self.gpus) {
              y[i] = "GPU" + i;
            }
            return y;
          })(),
          axisTick: { show: false },
          inverse: true
        },
        xAxis: {
          show: false
        },
        tooltip: {
          trigger: "item"
        },
        series: [
          {
            type: "bar",
            name: "使用率",
            barWidth: 10,
            data: (function() {
              let y = [];
              for (let i in self.gpus) {
                y[i] = {
                  value: self.gpus[i]["utilization.gpu"],
                  name: "GPU" + i + "的使用率",
                  itemStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                      { offset: 0, color: "rgb(0,255,0)" },
                      {
                        offset: 1,
                        color:
                          "rgb(" +
                          parseInt(
                            (self.gpus[i]["utilization.gpu"] / 100) * 255
                          ) +
                          "," +
                          parseInt(
                            255 - (self.gpus[i]["utilization.gpu"] / 100) * 255
                          ) +
                          ",0)"
                      }
                    ])
                  },
                  tooltip: {
                    formatter:
                      "GPU" +
                      i +
                      "<br/>{b}:{c}%<br/>温度：" +
                      self.gpus[i]["temperature.gpu"] +
                      "℃"
                  }
                };
              }
              return y;
            })(),
            stack: "utilization",
            label: {
              show: true,
              formatter: "{c}%",
              position: "right"
            },
            z: 3
          },
          {
            type: "bar",
            itemStyle: {
              normal: {
                color: "#ddd"
              }
            },
            barWidth: 10,
            data: (function() {
              let y = [];
              for (let i in self.gpus) {
                y[i] = {
                  value: 100 - self.gpus[i]["utilization.gpu"],
                  tooltip: {
                    formatter: function() {}
                  }
                };
              }
              return y;
            })(),
            stack: "utilization",
            animation: false
          },
          {
            type: "bar",
            name: "内存使用率",
            barWidth: 10,
            data: (function() {
              let y = [];
              for (let i in self.gpus) {
                y[i] = {
                  value: (
                    (self.gpus[i]["memory.used"] /
                      self.gpus[i]["memory.total"]) *
                    100
                  ).toFixed(1),
                  name: "GPU" + i + "的内存使用率",
                  itemStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                      { offset: 0, color: "rgb(0,255,0)" },
                      {
                        offset: 1,
                        color:
                          "rgb(" +
                          parseInt(
                            (self.gpus[i]["memory.used"] /
                              self.gpus[i]["memory.total"]) *
                              255
                          ) +
                          "," +
                          parseInt(
                            255 -
                              (self.gpus[i]["memory.used"] /
                                self.gpus[i]["memory.total"]) *
                                255
                          ) +
                          ",0)"
                      }
                    ])
                  },
                  tooltip: {
                    position: "top",
                    formatter: function() {
                      let str =
                        '<table class="memory-info"><tr><th>pid</th><th>user</th><th>cmd</th><th>memory</th></tr>';
                      for (let j in self.gpus[i].processes) {
                        str +=
                          "<tr><td>" +
                          self.gpus[i].processes[j].pid +
                          "</td><td>" +
                          self.gpus[i].processes[j].username +
                          "</td><td>" +
                          self.gpus[i].processes[j].command +
                          "</td><td>" +
                          self.gpus[i].processes[j].gpu_memory_usage +
                          "MiB</td></tr>";
                      }
                      str += "</table>";
                      return (
                        "GPU" +
                        i +
                        "<br/>GPU" +
                        i +
                        "已使用内存:" +
                        self.gpus[i]["memory.used"] +
                        "MiB<br/>" +
                        str
                      );
                    }
                  },
                  label: {
                    show: true,
                    formatter:
                      self.gpus[i]["memory.used"] +
                      " MiB/" +
                      self.gpus[i]["memory.total"] +
                      " MiB",
                    position: "right"
                  }
                };
              }
              return y;
            })(),
            stack: "memory",
            z: 3
          },
          {
            type: "bar",
            itemStyle: {
              normal: {
                color: "#ddd"
              }
            },
            barWidth: 10,
            data: (function() {
              let y = [];
              for (let i in self.gpus) {
                y[i] = {
                  value:
                    100 -
                    (self.gpus[i]["memory.used"] /
                      self.gpus[i]["memory.total"]) *
                      100,
                  tooltip: {
                    formatter:
                      "GPU" +
                      i +
                      "<br/>GPU" +
                      i +
                      "的空闲内存:" +
                      (self.gpus[i]["memory.total"] -
                        self.gpus[i]["memory.used"]) +
                      "MiB"
                  }
                };
              }
              return y;
            })(),
            stack: "memory",
            animation: false
          }
        ]
      });
    }
  }
};
</script>
<style>
.serverChart {
  width: 450px;
  height: 500px;
}
.memory-info {
  width: 300px;
}
.memory-info td,
.memory-info th {
  color: snow;
  width: 25%;
  text-align: center;
}
</style>