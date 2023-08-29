<template>
  <div id="app" v-if="!loadingData">
    <el-menu
      class="el-menu-demo"
      mode="horizontal"
      background-color="#676767"
      text-color="#fff"
      :default-active="activeIndex"
      active-text-color="#ffd04b">
      <el-menu-item class='labelIcon' id="title">
        {{appName}}
      </el-menu-item>
      <!-- <el-tooltip class='labelIcon' v-for="operation in operationArray" :key="operation" :content="operation" effect="light">
        <el-menu-item :index="operation">
          <div type="text" v-if="operation==='submit selection'" @click="submitSelect" :loading="loadingSelect">
            {{loadingSelectInfo}}<i class="el-icon-upload el-icon--right"></i>
          </div>
          <div type="text" v-if="operation==='counter'">
            {{counter}}/100
          </div>
        </el-menu-item>
      </el-tooltip> -->
    </el-menu>


    <div class="media-topic">
      <div class="media-topic-vector-reduction-view">
        <MediaScatter></MediaScatter>
      </div>
      <div class="media-topic-difference-concat-view">
        <div class="media-concat-list">
          <MediaTags></MediaTags>
        </div>
        <div class="media-concat-diffarea">
          <MediaMatrixTrend></MediaMatrixTrend>
        </div>
        
      </div>
    </div>
    <div class="event-evolution">
      <div class="union-event-evolution">
        <div class="event-evolution-storytree" id="story_tree_div">
          <!-- <MediaStoryTree :storytree__loading="storytree__loading"></MediaStoryTree> -->
          <MediaSankeyTree :storytree__loading="storytree__loading"></MediaSankeyTree>
        </div>
        <div class="event-iframeview">
          <SankeyTreeNodeIFrameVue></SankeyTreeNodeIFrameVue>
          <!-- <iframe :src="iframeSrc" class="iframe-class"></iframe> -->
        </div>
        
      </div>
      <div class="single-event-evolution">
        <div class="single-domain-tree" v-model="currentSelectedMedia" v-for="item in currentSelectedMedia" :key="item.domain" :id="item.domain.replaceAll('.','_')">
          <SingleTree :storytree__loading="storytree__loading" :domain="item.domain"></SingleTree>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// Structors
import { mapState, mapMutations } from 'vuex';
import { getMediaData, getMediaMatrixData} from '@/communication/communicator.js'
import { getMediaStoryTreeData, getMediaDiffConcatData } from '@/communication/communicator.js'
import { Dataset } from '@/dataset/dataset.js'
// Components
import MediaScatter from './components/MediaScatter.vue';
import MediaTrend from './components/MediaTrend.vue';
import MediaHorizonChart from './components/MediaHorizonChart.vue';
import MediaMatrixTrend from './components/MediaMatrixTrend.vue';
import MediaStoryTree from './components/MediaStoryTree.vue';
import MediaSankeyTree from './components/MediaSankeyTree.vue';
import MediaTags from './views/MediaTags.vue';
import SingleTree from './views/SingleTree.vue';
import SankeyTreeNodeIFrameVue from './views/SankeyTreeNodeIFrame.vue';

export default {
  name: 'App',
  data() {
    return {
      appName: "BiaSeer",
      loadingData: true,
      topicCodeList: null,
      storytree__loading: false,
      drawer: true,
      currentSelectedMedia: null,
      iframeSrc: 'https://www.runoob.com'
    }
  },
  components: {
    MediaScatter,
    MediaTrend,
    MediaHorizonChart,
    MediaMatrixTrend,
    MediaStoryTree,
    MediaSankeyTree,
    MediaTags,
    SingleTree,
    SankeyTreeNodeIFrameVue
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
  mounted() {
    this.currentSelectedMedia = this.gainCurrentSelectedMedia();
  },
  methods: {
    ...mapMutations([
      'UPDATE_STORYTREE_FINISH',
      'UPDATE_CONCATDIFF_FINISH',
    ]),
    gainCurrentSelectedMedia(){
      let result = []
      sysDatasetObj.mediaScatterSelected.forEach(element => {
        result.push({domain: element})
      });
      console.log(result);
      return result;
    },
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
      'mediaScatterClick'
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
    },
    mediaScatterClick: function(){
      this.currentSelectedMedia = this.gainCurrentSelectedMedia();
    }
  }
}
</script>

<style lang="less">
// div{
//   border-radius: 5px;
//   margin: .5px;
// }

@menu-height: 2.5rem;
@title-container-height: 160px;
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

  .el-menu.el-menu--horizontal {
    .el-menu-item {
      height: @menu-height;
      line-height: @menu-height;
    }
    .el-menu-item {
      border-bottom-color: rgb(84, 92, 100) !important;
      font-weight: bolder;
      font-size: 1rem;
      color: #dadada !important;
      padding: 0 10px;
      .icon {
        color: #dadada !important;
      }
    }
  }
  .labelIcon {
    font-size: 1rem;
  }

  .media-topic {
    position: absolute;
    // top: 0%;
    top: @menu-height;
    bottom: 65%;
    left: 0%;
    right: 0%;
    .media-topic-vector-reduction-view {
      position: absolute;
      top: 0%;
      bottom: 0%;
      left: 0%;
      right: 50%;
      border-left: 1px solid gray;
      border-top: 1px solid gray;
    }

    .media-topic-difference-concat-view {
      position: absolute;
      top: 0%;     
      bottom: 0%;
      left: 50%;
      right: 0%;
      // border: 1px solid gray;
      .media-concat-list{
        position: absolute;
        top: 0%;
        bottom: 92%;
        left: 0%;
        right: 0%;
        border: 1px solid gray;
        display: flex;
        align-items: center;
      }
      .media-concat-diffarea{
        position: absolute;
        top: 8%;
        bottom: 0%;
        left: 0%;
        right: 0%;
        border-left: 1px solid gray;
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
      // border: 1px solid gray;
      .event-evolution-storytree{
        position: absolute;
        top: 0%;
        bottom: 0%;
        left: 0%;
        right: 30%;
        border: 1px solid gray;
      }
      .event-iframeview{
        position: absolute;
        top: 0%;
        bottom: 0%;
        left: 70%;
        right: 0%;
        border-top: 1px solid gray;
        border-bottom: 1px solid gray;
        border-right: 1px solid gray;
        .iframe-class{
          width: 100%;
          height: 100%;
        }
      }
    }

    .single-event-evolution {
      position: absolute;
      top: 70%;
      bottom: 0%;
      left: 0%;
      right: 0%;
      overflow-x: scroll;
      display: flex;
      .single-domain-tree{
        flex: 1;
        margin: 4px;
      }
    }
  }
}</style>
