<template>
  <section>
    <el-row>
      <el-col
        :span="20"
        class="charts"
      >
        <div
          class="line-chart"
          id="chart"
        ></div>
      </el-col>
      <el-col :span="3">
        <el-button
          class="view-btn"
          @click="viewCap"
        >view CAP range</el-button>
      </el-col>
    </el-row>
    <el-row>
      <el-col
        :offset="2"
        :span="16"
      >
        <el-table
          :data="tableData.results"
          stripe
          style="width: 100%"
        >
          <el-table-column
            v-for="(item,index) in tableData.rows"
            v-bind:key="index"
            :prop="item.name"
            :label="item.name"
          >
          </el-table-column>
        </el-table>
      </el-col>

    </el-row>
    <el-row class="code-modules">
       <el-col
        :offset="2"
        :span="16"
      >
      <h3>MODULES TAKEN PREVIOUSLY</h3>
      </el-col>
      
      <el-col
        :offset="2"
        :span="16"
      >
        <ul>
          <li
            v-for="(item,index) in list"
            v-bind:key="index"
          >
            {{item}}
          </li>
        </ul>
      </el-col>

    </el-row>
    <el-dialog
      title=""
      :visible.sync="openDialog"
      width="30%"
      center
    >
      <span>Your expected CAP falls in the range of:</span><br>
      <span class="honor">{{honours}}</span>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          type="primary"
          @click="openDialog = false"
        >Close</el-button>
      </span>
    </el-dialog>
  </section>
</template>
<script>
export default {
  name: "dashboard",
  data() {
    return {
      openDialog: false,
      honours: "",
      list: [],
      tableData: {
        rows: [
          {
            label: "Intended modules",
            name: "Intended_modules"
          },
          {
            label: "Predicted grades",
            name: "Predicted_grades"
          }
        ],
        results: []
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
            name: "",
            symbolSize: 10,
            type: "line",
            data: []
          }
        ]
      }
    };
  },
  created() {},
  mounted() {
    this.drawline();
    this.getTables();
    this.getList();
  },
  methods: {
    drawline() {
      let that = this;
      let chart = this.$echarts.init(document.getElementById("chart"));
      let token_name = localStorage.getItem("tokens") || "52269_129";
      let url = "/api/student/token_name/caps?token_name=" + token_name;
      this.$http
        .get(url, {
          "Content-Type": "application/json;charset=UTF-8"
        })
        .then(function(response) {
          let data = response.data || {};
          for (let index in data.term_caps) {
            that.option.xAxis.data.push(index);
            that.option.series[0].data.push(data.term_caps[index]);
          }
          //that.option.series[0].data.push(data.cap);
          chart.setOption(that.option);
        })
        .catch(function() {
          console.log("xxx");
        });
    },
    viewCap() {
      let that = this;
      let modules = [];
      let results = that.tableData.results;
      for (let i = 0; i < results.length; i++) {
        modules.push(results[i].Intended_modules);
      }
      let list = JSON.stringify(modules);
      let url = "/api/student/module_codes/honours?module_codes=" + list;
      this.$http
        .get(url, {
          "Content-Type": "application/json;charset=UTF-8"
        })
        .then(function(response) {
          let data = response.data || {};
          that.honours = data.honours || "";
          that.openDialog = true;
        })
        .catch(function() {});
    },
    getTables() {
      let that = this;
      let url =
        '/api/student/module_codes/caps?module_codes=["ST2132","MA1102R"]';
      this.$http
        .get(url, {
          "Content-Type": "application/json;charset=UTF-8"
        })
        .then(function(response) {
          let data = response.data || {};
          for (let index in data) {
            if (index != "message") {
              that.tableData.results.push({
                Intended_modules: index,
                Predicted_grades: data[index]
              });
            }
          }
        })
        .catch(function() {});
    },
    getList() {
      let that = this;
      let tokens = localStorage.getItem("tokens") || "10013_789";
      let url = "/api/student/token_name/module_codes?token_name=" + tokens;
      this.$http
        .get(url, {
          "Content-Type": "application/json;charset=UTF-8"
        })
        .then(function(response) {
          let data = response.data || {};
          that.list = data.module_codes;
        })
        .catch(function() {});
    }
  }
};
</script>
<style>
.search {
  padding: 20px;
  background: lightgray;
}

.search-btn {
  width: 100px;
  height: 100px;
  font-size: 32px;
}
.detail-table {
  padding: 20px;
}
.charts {
  height: 600px;
}
.view-btn {
  width: 160px;
  height: 160px;
  border-radius: 80px;
  background: #00a9f4;
  color: #fff;
  font-size: 16px;
  /* word-break: break-word; */
  /* word-spacing: inherit; */
  word-wrap: break-word;
}
#chart {
  width: 100%;
  height: 100%;
}
.code-modules{
  text-align: left;
  margin-top:20px;
}
</style>
>

