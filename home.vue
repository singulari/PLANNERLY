<template>
  <div class="home">

    <el-row class="tac">
      <el-col
        :span="4"
        class="left-menu"
      >
        <div class="title">
          <h2>{{menu.title}}</h2>
        </div>
        <el-menu
          default-active="2"
          class="el-menu-vertical-demo"
          router
          active-text-color="#409EFF"
        >
          <el-menu-item
            v-for="(item,index) in menu.children"
            v-bind:key="index"
            :index="item.url"
          >
            <i class="el-icon-menu"></i>
            <span slot="title" :title="item.name">{{item.name}}</span>
          </el-menu-item>

        </el-menu>
      </el-col>
      <el-col
        :span="20"
        class="right-content"
      >
        <el-row class="top-menu"></el-row>
        <el-row class="content">
          <router-view></router-view>
        </el-row>

      </el-col>
    </el-row>
  </div>

</template>
<script>
export default {
  name: "home",
  data() {
    return {
      msg: "hello world",
      menu: {
        title: "Plannerly",
        children: [
          {
            url: "/dashboard",
            name: "PATH BOARD"
          },
        /*  {
            url: "/preferences",
            name: "PREFERENCES"
          },*/
          {
            url: "/enrolment",
            name: "ENROLMENT"
          },
          /*{
            url: "recommendation",
            name: "RECOMMENTDATION"
          },*/
          {
            url: "/questions",
            name: "PREFERENCE INDICATION"
          },{
            url: "/distribution",
            name: "MODULE COMPARISION CHART"
          }
        ]
      }
    };
  }
};
</script>
<style>
.top-menu {
  position: fixed;
  left: auto;
  top: 0;
  height: 60px;
  width: 100%;
  background: #00a9f4;
  z-index: 10001;
  -webkit-box-shadow: 5px 0px 9px 0px rgba(0, 0, 0, 0.06);
  -moz-box-shadow: 5px 0px 9px 0px rgba(0, 0, 0, 0.06);
  box-shadow: 5px 0px 9px 0px rgba(0, 0, 0, 0.06);
}
.home {
  height: 100%;
}

.tac {
  height: 100%;
  width: 100%;
}
.left-menu {
  height: 100%;
  -webkit-box-shadow: 5px 0px 9px 0px rgba(0, 0, 0, 0.06);
  -moz-box-shadow: 5px 0px 9px 0px rgba(0, 0, 0, 0.06);
  box-shadow: 5px 0px 9px 0px rgba(0, 0, 0, 0.06);
  position: fixed;
  top: 0;
  left: 0;
  
}
.left-menu .el-menu{
text-align: left;
}
.content {
  margin-top: 60px;
  padding: 20px;
}
.right-content {
  margin-left: 16.66667%;
}
.title {
  margin: 0;
  padding: 5px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
}
body {
  margin: 0;
  height: 100%;
  padding: 0;
  background: none !important;
}

</style>
>
>
