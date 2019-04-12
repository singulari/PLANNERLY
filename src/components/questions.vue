<template>
  <section class="questions">
    <el-form
      ref="question"
      :model="form"
      :rules="rules"
      style="width:80%;margin:0 auto"
    >
      <el-form-item
        v-for="(item,index) in questions"
        v-bind:key="index"
        :prop="item.name"
      >
        <el-row type="flex">
          <span class="question-item">{{index+1}}. {{item.question}}</span>
        </el-row>
        <el-row class="question-answer">
          <el-input
            v-if="item.type== 'input'"
            v-model="form[item.name]"
          ></el-input>
          <el-slider
            v-if="item.type == 'slide'"
            :min="item.start"
            :max="item.end"
            v-model="form[item.name]"
          ></el-slider>
        </el-row>
      </el-form-item>
      <el-form-item>
        <el-button
          type="primary"
          @click="onSubmit('question')"
        >submit</el-button>
        <el-button @click="onReset('question')" style="margin-left:30px">reset</el-button>
      </el-form-item>
    </el-form>
  </section>
</template>
<script>
export default {
  name: "questions",
  data() {
    return {
      form: {
        workload: 0,
        interest: 0,
        cap: 0,
        modules: "",
        core: ""
      },
      rules: {
        modules: [
          {
            required: true,
            message: "please enter the answer",
            trigger: "blur"
          }
        ],
        core: [
          {
            required: true,
            message: "please enter the answer",
            trigger: "blur"
          }
        ]
      },
      questions: [
        {
          name: "workload",
          question: "How much work are you willing to put in?",
          type: "slide",
          start: 0,
          end: 10
        },
        {
          name: "interest",
          question: "How much do you prioritise your CAP this semester?",
          type: "slide",
          start: 0,
          end: 10
        },
        {
          name: "cap",
          question: "How much do you prioritise your interest this semester?",
          type: "slide",
          start: 0,
          end: 10
        },
        {
          name: "modules",
          question: "How many modules do you plan to take this semester?",
          type: "input",
          placeholder: ""
        },
        {
          name: "core",
          question:
            "How many Core/UE/GE modules do you want to be allocated?",
          type: "input",
          placeholder: ""
        }
      ]
    };
  },
  methods: {
    onSubmit(name) {
      var that = this;
      this.$refs[name].validate(valid => {
        if (valid) {
          that.$http
            .post("/api/login", {
              uid: that.form.name,
              password: that.form.password
            })
            .then(function() {
              console.log("123");
            })
            .catch(function() {
              console.log("xxx");
            });
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    onReset(name) {
        this.$refs[name].resetFields() 
    }
  }
};
</script>
<style>
.questions {
  padding: 20px;
}
.question-item {
  font-size: 20px;
}
.question-answer {
  padding-left: 20px;
}
</style>

