<template >
  <section class="enrolment">
    <el-row>
      <el-col
        :span="16"
        :offset="2"
      >
        <el-input
          placeholder="Enter module code here, e.g. IS1103"
          v-model="keywords"
          class="input-with-select"
          @keypress="getAverage"
        >
          <el-button
            slot="append"
            icon="el-icon-search"
            @click="getAverage"
          ></el-button>
        </el-input>
      </el-col>
    </el-row>
    <el-row class="previous">
      <el-col
        :span="16"
        :offset="2"
        class="previous-search"
      >
        <ul>
          <li
            v-for="(item,index) in previous.module_codes"
            v-bind:key="index"
          >
            {{item}}
          </li>
        </ul>
      </el-col>

    </el-row>
    <el-row
      class="search-results"
      :gutter="2"
      v-if="showRate"
    >
      <el-col
        v-for="(item, index) in datas.results"
        v-bind:key="index"
        :span=" 6"
      >
        <h3>{{item.name}}</h3>
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
          id="chart"
        ></div>
      </el-col>
    </el-row>

  </section>
</template>
<script>
export default {
  name: "enrolment",
  data() {
    return {
      keywords: "",
      showRate: false,
      previous: {},
      datas: {
        results: [
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
      },
      option: {
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
      }
    };
  },
  created() {},
  mounted() {
    this.getPrevious();
  },
  methods: {
    drawline() {
      let chart = this.$echarts.init(document.getElementById("chart"));
      chart.setOption(this.option);
    },
    getPrevious() {
      let that = this;
      let url = "/api/student/recent_search_courses/title";
      this.$http
        .get(url, {
          "Content-Type": "application/json;charset=UTF-8"
        })
        .then(function(response) {
          let data = response.data || {};
          that.previous = data;
        })
        .catch(function() {
          console.log("xxx");
        });
    },
    getAverage() {
      let that = this;
      if (!that.keywords) {
        return;
      }
      let url =
        "/api/student/mod_class_id/average?mod_class_id=" + that.keywords;
      this.$http
        .get(url, {
          "Content-Type": "application/json;charset=UTF-8"
        })
        .then(function(response) {
          that.showRate = true;
          let data = response.data || {};

          for (let index in data) {
            if (index != "message") {
              if (index == "m3_ave") {
                that.datas.results[0].score = data[index];
              }
              if (index == "m1_ave") {
                that.datas.results[1].score = data[index];
              }
              if (index == "t1_t2_t3_ave") {
                that.datas.results[2].score = data[index];
              }
            }
          }
          that.getFinalMarks(that.keywords);
        })
        .catch(function() {});
    },
    getFinalMarks(id) {
      let that = this;
      let url = "/api/student/module_code/final_marks?module_code=" + id;
      this.$http
        .get(url, {
          "Content-Type": "application/json;charset=UTF-8"
        })
        .then(function(response) {
          let data = response.data || {};
          that.option.xAxis.data = data.final_marks_x;
          that.option.series[0].data = data.final_marks_y;
          that.drawline();
        })
        .catch(function() {});
    }
  }
};
</script>
<style scoped>
.search-results {
  padding: 40px 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
}
.bar-charts {
  height: 500px;
}
.charts {
  padding: 20px;
  height: 500px;
}
.previous-search {
  height: 200px;
  text-align: left;
  border: 1px solid rgba(0, 0, 0, 0.12);
  background: rgb(245, 247, 250);
}
.previous {
  padding: 20px;
}
.line-chart {
  height: 100%;
  width: 100%;
}
</style>

