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
        <div class="media-concat-list">
          <MediaTags></MediaTags>
        </div>
        <div class="media-concat-diffarea">
          <MediaMatrixTrend></MediaMatrixTrend>
        </div>
        
      </div>
    </div>
    <div class="event-evolution">
      <div class="union-event-evolution" id="story_tree_div">
        <!-- <MediaHorizonChart></MediaHorizonChart> -->
        <MediaStoryTree :storytree__loading="storytree__loading"></MediaStoryTree>
      </div>
      <div class="single-event-evolution"></div>
    </div>
  </div>
</template>

<script>
// Structors
import { mapState, mapMutations } from 'vuex';
import { getMediaData, getMediaMatrixData } from '@/communication/communicator.js'
import { getMediaStoryTreeData, getMediaDiffConcatData } from '@/communication/communicator.js'
import { Dataset } from '@/dataset/dataset.js'
// Components
import MediaScatter from './components/MediaScatter.vue';
import MediaTrend from './components/MediaTrend.vue';
import MediaHorizonChart from './components/MediaHorizonChart.vue';
import MediaMatrixTrend from './components/MediaMatrixTrend.vue';
import MediaStoryTree from './components/MediaStoryTree.vue';
import MediaTags from './views/MediaTags.vue';

export default {
  name: 'App',
  data() {
    return {
      loadingData: true,
      topicCodeList: null,
      storytree__loading: true,
    }
  },
  components: {
    MediaScatter,
    MediaTrend,
    MediaHorizonChart,
    MediaMatrixTrend,
    MediaStoryTree,
    MediaTags
  },
  beforeMount: function () {
    let self = this;
    window.sysDatasetObj = new Dataset();
    // lodaing data, during beforemount 
    let mediaDataDeferObj = $.Deferred();
    let mediaMatrixDataDeferObj = $.Deferred();

    $.when(mediaDataDeferObj, mediaMatrixDataDeferObj).then(async () => {
      self.loadingData = false;
    })
    getMediaData(function (data) {
      self.topicCodeList = data['topicCodeList'];
      sysDatasetObj.updateMediaDataSet(data);
      mediaDataDeferObj.resolve();
    });
    getMediaMatrixData(function (data) {
      sysDatasetObj.updateMediaMatrixDataSet(data);
      mediaMatrixDataDeferObj.resolve();
    });

  },
  methods: {
    ...mapMutations([
      'UPDATE_STORYTREE_FINISH',
      'UPDATE_CONCATDIFF_FINISH',
    ]),
    isToGetStroytree() {
      let data = sysDatasetObj.mediaMatrixSelected;
      console.log(data);
      console.log(data['date'].size);
      if (data['date'].size > 0) {
        return true;
      }
      return false;
    },
    getStroyTree() {
      let self = this;
      self.storytree__loading = true;
      let mediaMatrixSelectedDataDeferObj = $.Deferred();
      $.when(mediaMatrixSelectedDataDeferObj).then(async () => {
        self.storytree__loading = false;
      })
      getMediaStoryTreeData(sysDatasetObj.mediaMatrixSelected,sysDatasetObj.mediaScatterSelected, function (data) {
        sysDatasetObj.updateStoryTreeDataset(data);
        self.UPDATE_STORYTREE_FINISH();
        mediaMatrixSelectedDataDeferObj.resolve();
      });
    },
  },
  computed: {
    ...mapState([
      'currMedium',
      'mediaMatrixSelectedSignal',
      'mediaDiffConcatSignal',
    ])
  },
  watch: {
    mediaMatrixSelectedSignal: function () {
      let self = this;
      console.log(self.mediaMatrixSelectedSignal);
      if (self.isToGetStroytree()) {
        self.getStroyTree();
      }
    },
    mediaDiffConcatSignal: function(){
      let self = this;
      console.log("listening mediaDiffConcatSignal");
      let mediaDiffConcatDataDeferObj = $.Deferred();
      $.when(mediaDiffConcatDataDeferObj).then(async () => {
        self.UPDATE_CONCATDIFF_FINISH();
      })
      getMediaDiffConcatData(sysDatasetObj.mediaScatterSelected, function (data) {
        sysDatasetObj.updateMediaConcatDiffDataSet(data);
        mediaDiffConcatDataDeferObj.resolve();
      });
    }
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

  .media-topic {
    position: absolute;
    top: 0%;
    bottom: 65%;
    left: 0%;
    right: 0%;

    // background-color: steelblue;
    // margin: 5px;
    .media-topic-vector-reduction-view {
      position: absolute;
      top: 0%;
      bottom: 0%;
      left: 0%;
      right: 50%;
      border: 1px solid steelblue;
    }

    .media-topic-difference-concat-view {
      position: absolute;
      top: 0%;
      bottom: 0%;
      left: 50%;
      right: 0%;
      border: 1px solid steelblue;
      .media-concat-list{
        position: absolute;
        top: 0%;
        bottom: 90%;
        left: 0%;
        right: 0%;
      }
      .media-concat-diffarea{
        position: absolute;
        top: 10%;
        bottom: 0%;
        left: 0%;
        right: 0%;
      }
    }
  }

  .event-evolution {
    position: absolute;
    top: 35%;
    bottom: 0%;
    left: 0%;
    right: 0%;
    margin: 0px !important;

    .union-event-evolution {
      position: absolute;
      top: 0%;
      bottom: 30%;
      left: 0%;
      right: 0%;

      border: 1px solid steelblue;
    }

    .single-event-evolution {
      position: absolute;
      top: 70%;
      bottom: 0%;
      left: 0%;
      right: 0%;

      border: 1px solid steelblue;
    }
  }
}</style>
