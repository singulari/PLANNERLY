<template>
  <section style="margin-top:60px;">
    <el-row
      :gutter="4"
      type="flex"
      justify="center"
    >
      <el-col
        :span="8"
        class="compare"
      >
        <el-row>
          <el-input
            placeholder="Key in module code "
            v-model="leftwords"
          >
            <el-button
              slot="append"
              icon="el-icon-search"
              @click="getAverage('left')"
            ></el-button>
          </el-input>
        </el-row>
        <el-row
          class="search-results"
          :gutter="2"
          v-if="showRate"
        >
          <el-col
            v-for="(item, index) in datas.leftresults"
            v-bind:key="index"
            :span=" 8"
          >
            <h5>{{item.name}}</h5>
            <el-rate
              v-model="item.score"
              disabled
              show-score
              text-color="#ff9900"
              score-template="{value}"
            >
            </el-rate>
          </el-col>
        </el-row>
        <el-row class="bar-charts">
          <el-col
            :span="20"
            class="charts"
          >
            <div
              class="line-chart"
              id="left"
            ></div>
          </el-col>
        </el-row>
      </el-col>
      <el-col
        :span="8"
        class="compare"
        :offset="1"
      >
        <el-row offset="2">
          <el-input
            placeholder="Key in module code"
            v-model="rightwords"
          >
            <el-button
              slot="append"
              icon="el-icon-search"
              @click="getAverage(right)"
            ></el-button>
          </el-input>
        </el-row>
        <el-row
          class="search-results"
          :gutter="2"
          v-if="showright"
        >
          <el-col
            v-for="(item, index) in datas.rightresults"
            v-bind:key="index"
            :span="8"
          >
            <h5>{{item.name}}</h5>
            <el-rate
              v-model="item.score"
              disabled
              show-score
              text-color="#ff9900"
              score-template="{value}"
            >
            </el-rate>
          </el-col>
        </el-row>
        <el-row class="bar-charts">
          <el-col
            :span="20"
            class="charts"
          >
            <div
              class="line-chart"
              id="right"
            ></div>
          </el-col>
        </el-row>
      </el-col>
    </el-row>
  </section>
</template>
<script>
export default {
  name: "distribution",
  data() {
    return {
      leftwords: "",
      rightwords: "",
      showright: false,
      showRate: false,
      lOption: {
        title: {
          text: "Academic Year 18/19 Semester 2",
          textAlign: "center",
          left: "center"
        },

        tooltip: {},
        xAxis: {
          data: []
        },
        yAxis: {},
        series: [
          {
            name: "Frequency",
            type: "bar",
            data: []
          }
        ]
      },
      rOption: {
        title: {
          text: "Academic Year 18/19 Semester 2",
          textAlign: "center",
          left: "right"
        },

        tooltip: {},
        xAxis: {
          data: []
        },
        yAxis: {},
        series: [
          {
            name: "Frequency",
            type: "bar",
            data: []
          }
        ]
      },
      datas: {
        leftresults: [
          {
            name: "Module Difficulty",
            score: 4.1
          },
          {
            name: "Module Workload",
            score: 3.9
          },
          {
            name: "Professor Rating",
            score: 4.4
          }
        ],
        rightresults: [
          {
            name: "Module Difficulty",
            score: 4.1
          },
          {
            name: "Module Workload",
            score: 3.9
          },
          {
            name: "Professor Rating",
            score: 4.4
          }
        ]
      }
    };
  },
  created() {},
  mounted() {},
  methods: {
    drawline(type) {
      let id = "";
      if (type == "left") {
        id = "left";
        let chart = this.$echarts.init(document.getElementById(id));
        chart.setOption(this.lOption);
      } else {
        id = "right";
        let chart = this.$echarts.init(document.getElementById(id));
        chart.setOption(this.rOption);
      }
    },
    getAverage(type) {
      let that = this;
      let keywords = "";
      if (type == "left") {
        keywords = that.leftwords;
      } else {
        keywords = that.rightwords;
      }
      if (!keywords) {
        return;
      }
      let url = "/api/student/mod_class_id/average?mod_class_id=" + keywords;
      this.$http
        .get(url, {
          "Content-Type": "application/json;charset=UTF-8"
        })
        .then(function(response) {
          that.showRate = true;
          let data = response.data || {};
          if (type == "left") {
            that.showLeftRate = true;
            for (let index in data) {
              if (index != "message") {
                if (index == "m3_ave") {
                  that.datas.leftresults[0].score = data[index];
                }
                if (index == "m1_ave") {
                  that.datas.leftresults[1].score = data[index];
                }
                if (index == "t1_t2_t3_ave") {
                  that.datas.leftresults[2].score = data[index];
                }
              }
            }
          } else {
            that.showright = true;
            for (let index in data) {
              if (index != "message") {
                if (index == "m3_ave") {
                  that.datas.rightresults[0].score = data[index];
                }
                if (index == "m1_ave") {
                  that.datas.rightresults[1].score = data[index];
                }
                if (index == "t1_t2_t3_ave") {
                  that.datas.rightresults[2].score = data[index];
                }
              }
            }
          }

          that.getFinalMarks(keywords, type);
        })
        .catch(function() {});
    },
    getFinalMarks(id, type) {
      let that = this;
      let url = "/api/student/module_code/final_marks?module_code=" + id;
      this.$http
        .get(url, {
          "Content-Type": "application/json;charset=UTF-8"
        })
        .then(function(response) {
          if (type == "left") {
            let data = response.data || {};
            that.lOption.xAxis.data = data.final_marks_x;
            that.lOption.series[0].data = data.final_marks_y;
            that.drawline(type);
          } else {
            let data = response.data || {};
            that.rOption.xAxis.data = data.final_marks_x;
            that.rOption.series[0].data = data.final_marks_y;
            that.drawline(type);
          }
        })
        .catch(function() {});
    }
  }
};
</script>
<style>
.compare {
  padding: 20px !important;
  border: 1px solid rgba(0, 0, 0, 0.12);
  min-height: 500px;
  text-align: left;
  border-radius: 5px;
}
.search-results {
  padding-top: 60px;
}
.results-item {
  min-height: 200px;
}
.line-chart {
  height: 300px;
}
.charts {
  padding: 20px;
  height: 300px;
}
</style>
>