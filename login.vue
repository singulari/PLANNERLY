<template>
  <div class="login">
    <el-form
      ref="loginform"
      :model="form"
      label-width="0px"
      :rules="rules"
      class="login-form"
    >
      <el-row class="header-info">
        <label class="lb-1"></label>
        <label class="lb-2"></label>
        <label class="lb-3"></label>
      </el-row>
      <el-row class="av-icon">
        <img src="../assets/avtar.png">
      </el-row>
      <el-row
        type="flex"
        class="row-bg"
        justify="center"
      >
        <el-form-item
          label=""
          prop="name"
          style="width:60%;height:40px"
        >
          <el-input
            v-model="form.name"
            placeholder="username"
          >

          </el-input>
        </el-form-item>
      </el-row>
      <el-row
        type="flex"
        class="row-bg"
        justify="center"
      >
        <el-form-item
          label=""
          prop="pwd"
          style="width:60%;height:40px"
        >
          <el-input
            v-model="form.pwd"
            show-password
            placeholder="password"
          >

          </el-input>
        </el-form-item>
      </el-row>
      <el-row
        type="flex"
        class="row-bg"
        justify="center"
      >
        <el-button
          class="login-btn"
          @click="onSubmit('loginform')"
        >login</el-button>
      </el-row>
    </el-form>

  </div>

</template>
<script>
export default {
  name: "login",
  data() {
    let validatePass = (rule, value, callback) => {
      let re = /^(\w-*\.*)+@u.nus.edu/;
      if (!re.test(value)) {
        callback(new Error("please enter valid username"));
      } else {
        callback();
      }
    };
    return {
      form: {
        name: "",
        pwd: ""
      },
      tokens: [
        "37376_13",
        "13680_21",
        "40862_24",
        "37627_64",
        "37666_87",
        "52478_114",
        "52269_129",
        "60058_433",
        "36055_485",
        "41915_538",
        "37834_660",
        "53587_676",
        "11756_940s",
        "11298_1367"
      ],
      rules: {
        name: [
          { required: true, message: "please enter username", trigger: "blur" },
          {
            validator: validatePass,
            trigger: "blur"
          }
        ],
        pwd: [
          {
            required: true,
            message: "please enter password",
            trigger: "blur"
          }
        ]
      }
    };
  },
  methods: {
    onSubmit(formName) {
      var that = this;
      this.$refs[formName].validate(valid => {
        if (valid) {
          let num = Math.floor(Math.random() * that.tokens.length);
          localStorage.setItem("tokens", that.tokens[num]);
          that.$router.push("/dashboard");
        }
      });
    },
    onReset(formName) {
      this.$refs[formName].resetFields();
    }
  }
};
</script>
<style>

.login-form {
  background: #2b2b36;
  position: relative;
  width: 30%;
  margin: 10% auto 0 auto;
  text-align: center;
  border-radius: 15px;
  -webkit-border-radius: 15px;
}
.header-info {
  padding: 5px 0;
  text-align: center;
  font-weight: 600;
  font-size: 2em;
  color: #fff;
  background: #23232e;
  height: 50px;
  border-top-left-radius: 10px;
  -webkit-border-top-left-radius: 10px;
  -moz-border-top-left-radius: 10px;
  -o-border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  -webkit-border-top-right-radius: 10px;
}
.lb-1 {
  background: #6756ea;
  width: 20px;
  height: 20px;
  display: block;
  float: right;
  border-radius: 50%;
  margin: 16px 10px 0px 0px;
}
.lb-2 {
  background: #ea569a;
  width: 20px;
  height: 20px;
  display: block;
  float: right;
  border-radius: 50%;
  margin: 16px 10px 0px 0px;
}
.lb-3 {
  background: #f1c85f;
  width: 20px;
  height: 20px;
  display: block;
  float: right;
  border-radius: 50%;
  margin: 16px 10px 0px 0px;
}
.av-icon img {
  margin: 2em 0 0;
}
.login-btn {
  font-size: 30px;
  color: #fff;
  outline: none;
  border: none;
  background: #3ea751;
  width: 100%;
  padding: 18px 0;
  border-bottom-left-radius: 15px;
  -webkit-border-bottom-left-radius: 15px;
  -moz-border-bottom-left-radius: 15px;
  -o-border-bottom-left-radius: 15px;
  border-bottom-right-radius: 15px;
  -webkit-border-bottom-right-radius: 15px;
  -moz-border-bottom-right-radius: 15px;
  -o-border-bottom-right-radius: 15px;
  cursor: pointer;
}
body {
  background: url("../assets/bg1.jpg") no-repeat;
}
input {
  background-color: #23232e;
}
</style>
>