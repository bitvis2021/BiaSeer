<template>
  <div id="app" v-if="!loadingData">
    <div class="media-topic">
      <div class="media-topic-vector-reduction-view">
        <MediaScatter></MediaScatter>
      </div>
      <div class="media-topic-difference-concat-view">
        <!-- <MediaTrend></MediaTrend> -->
        <!-- <MediaTrend v-for="item in topicCodeList" :topic_code='item'></MediaTrend> -->
        <!-- <MediaHorizonChart></MediaHorizonChart> -->
        <MediaMatrixTrend></MediaMatrixTrend>
      </div>
    </div>
    <div class="event-evolution">
      <div class="union-event-evolution">
        <!-- <MediaHorizonChart></MediaHorizonChart> -->
      </div>
      <div class="single-event-evolution"></div>
    </div>
  </div>
</template>

<script>
// Structors
import { mapState, mapMutations } from 'vuex';
import { getMediaData, getMediaMatrixData } from '@/communication/communicator.js'
import { Dataset } from '@/dataset/dataset.js'
// Components
import MediaScatter from './components/MediaScatter.vue';
import MediaTrend from './components/MediaTrend.vue';
import MediaHorizonChart from './components/MediaHorizonChart.vue';
import MediaMatrixTrend from './components/MediaMatrixTrend.vue';


export default {
  name: 'App',
  data() {
    return {
      loadingData: true,
      topicCodeList: null,
    }
  },
  components: {
    MediaScatter,
    MediaTrend,
    MediaHorizonChart,
    MediaMatrixTrend,
  },
  beforeMount: function () {
    let self = this;
    window.sysDatasetObj = new Dataset();
    // lodaing data, during beforemount 
    let mediaDataDeferObj = $.Deferred();
    let mediaMatrixDataDeferObj = $.Deferred();

    $.when(mediaDataDeferObj, mediaMatrixDataDeferObj).then(async() => {
      self.loadingData = false;
    })
    getMediaData(function(data){
      self.topicCodeList = data['topicCodeList'];
      sysDatasetObj.updateMediaDataSet(data);
      mediaDataDeferObj.resolve();
    });
    getMediaMatrixData(function(data){
      sysDatasetObj.updateMediaMatrixDataSet(data);
      mediaMatrixDataDeferObj.resolve();
    });

  },
  methods: {

  },
  computed: {

  },
  watch: {

  }
}
</script>

<style lang="less">
// div{
//   border-radius: 5px;
//   margin: .5px;
// }
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  position: absolute;
  top: 0%;
  bottom: 0%;
  left: 0%;
  right: 0%;
  overflow-x: hidden;
  overflow-y: hidden;
  .media-topic{
    position: absolute;
    top: 0%;
    bottom: 65%;
    left: 0%;
    right: 0%;
    // background-color: steelblue;
    // margin: 5px;
    .media-topic-vector-reduction-view{
      position: absolute;
      top: 0%;
      bottom: 0%;
      left: 0%;
      right: 50%;
      border: 1px solid steelblue;
    }
    .media-topic-difference-concat-view{
      position: absolute;
      top: 0%;
      bottom: 0%;
      left: 50%;
      right: 0%;
      border: 1px solid steelblue;
    }
  }
  .event-evolution{
    position: absolute;
    top: 35%;
    bottom: 0%;
    left: 0%;
    right: 0%;
    margin: 0px !important;

    .union-event-evolution{
      position: absolute;
      top: 0%;
      bottom: 30%;
      left: 0%;
      right: 0%;

      border: 1px solid steelblue;
    }

    .single-event-evolution{
      position: absolute;
      top: 70%;
      bottom: 0%;
      left: 0%;
      right: 0%;

      border: 1px solid steelblue;
    }
  }
}
</style>
