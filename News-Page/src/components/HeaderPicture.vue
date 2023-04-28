<template>
  <div style="margin-top: 5px; margin-bottom: 5px;">
    <el-row>
      <el-col :span="4">
        <div>&nbsp;</div>
      </el-col>
      <el-col :span="12">
        <el-carousel
          :interval="8000"
          height="400px"
          style="vertical-align: auto;"
        >
          <el-carousel-item
            v-for="(item, index) in newsdetail"
            :key="'info2-' + index"
            :label="item.title"
          >
            <img
              class="carouselpic"
              ref="bannerHeight"
              alt=""
              :onerror="defaultImg"
              :src="item.pic_url"
              @click="toNewsDetail(item.newsid)"
            />
          </el-carousel-item>
        </el-carousel>
      </el-col>
      <el-col :span="5" style="height: 400px; margin-left: 5px;">
        <div
          style="text-align: center; font-size: 20px; font-weight: 500; color: #fff; background-color: rgba(28,49,78,0.25); border-radius: 20px; margin-bottom: 5px;"
        >
          <h3>新闻速递</h3>
        </div>
        <div v-for="item in lastestNews" :key="item.id">
          <p style="line-height: 20px; cursor: pointer;" @click="toNewsDetail(item.id)">{{ item.title }}</p>
          <el-divider></el-divider>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { getPicture, dailyNews } from "@/api";
export default {
  name: "HeaderPicture",
  computed: {
    defaultImg() {
      return 'this.src="' + require("@/assets/imgs/404.jpg") + '"';
    }
  },
  created() {
    getPicture().then(res => {
      this.$Loading.start();
      // console.log('res', res)
      this.newsdetail = res.message;
      this.getDailyNews();
      this.$Loading.finish();
    });
  },
  data() {
    return {
      newsdetail: "",
      value2: 0,
      lastestNews: []
    };
  },
  methods: {
    getDailyNews() {
      dailyNews().then(res => {
        this.lastestNews = res.data;
      });
    },
    toNewsDetail(newsid) {
      // console.log(newsid)
      this.$router.push({ path: "/newspage/" + newsid });
    }
  }
};
</script>

<style scoped>
.carouselpic {
  position: absolute;
  width: 100%;
}
.el-carousel__item h3 {
  position: absolute;
  color: #cbcfd7;
  font-size: 14px;
  opacity: 0.75;
  line-height: 200px;
  margin: 0;
}

.el-carousel__item:nth-child(2n) {
  background-color: #ffffff;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #ffffff;
}
.imgaes {
  position: fixed;
  text-align: center;
  vert-align: middle;
  width: 100%;
  height: 100%;
}
.pic_item h2 {
  position: absolute;
  color: #ffffff;
  /*bottom:2rem;*/
}
</style>
