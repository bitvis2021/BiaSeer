<template>
    <div class="sankeytree-node-iframe" ref="iframediv">

        <div class="mytip" v-for="(item,index) in node_details2">
            <!-- <h4> {{ item.name.split("+")[0]+"."  }}</h4>
            <p> {{ item.node_detail_info[0].lines }}</p> -->
            <el-collapse>
                <el-collapse-item >
                    <template #title>
                        <h3 class="el-collapse-item-title"> {{ item.name.split("+")[0]+"."  }}</h3>
                        <!-- <div class="el-collapse-item-title">{{ " [" + (index + 1) +"] " + item.name.split("+")[0]+"." }}</div> -->
                    </template>
                    <p> {{ item.node_detail_info[0].lines }}</p>
                </el-collapse-item>
            </el-collapse>
        </div>

        <div class="wordcloud">
            <div ref='wordCloudBox'></div>
        </div>

    </div>
</template>
<script>
// Structors
import { mapState, mapMutations } from 'vuex';
import myCloud from '@/assets/js/myCloud.js';

export default {
    name: 'SankeyTreeNodeIFrame',
    props: {
        domain: String,
        storytree__loading: Boolean,
    },
    data() {
        return {
            activeNames: ['1'],
            node_details: [],
            node_details2: [],
            isShowCarousel: false,
            width: 400,
        }
    },
    components: {
    },
    beforeMount: function () {
    },
    mounted: function () {
        this.isShowCarousel = false
        this.width = this.$refs.iframediv.clientWidth;
        // let wordList = [
        //         {text:'vue',size:20},
        //         {text:'html',size:25},
        //         {text:'js',size:30},
        //     ]
        // this.getWordCloud(wordList);
    },
    methods: {
        ...mapMutations([
            // 'UPDATE_STORYTREE_FINISH',
        ]),  
        handleChange(val) {
            console.log(val);
        },
        getWordCloud(wordList){
            let wordOption = {  
                wordList, 
                size:[this.width,257],  // 盒子的宽高
                svgElement: this.$refs.wordCloudBox  //使用ref选择节点
            }
            myCloud(wordOption,this.getArticleList)
        },
        //回调
        getArticleList(){
            console.log("...")
        }
    },
    computed: {
        ...mapState([
            'storytree_finish',
            'clickSankeyTreeNode'
        ])
    },
    watch: {
        clickSankeyTreeNode: function(){
            // 更新新闻列表
            console.log("更新新闻列表...")
            let self = this;
            let data = sysDatasetObj.SankeyTreePathNode;
            data.reverse();
            console.log('data', data);
            self.node_details2 = []
            data.forEach(d=>{
                console.log(d);
                if(d.name == 'ROOT' || d.time_e == 'time'){return}
                self.node_details2.push(d);
                console.log('node_details', self.node_details2)
                })
            // 那全局数据
            self.isShowCarousel = true;
        },
        storytree_finish: function(){
            let self = this;
            let data = sysDatasetObj.storyTreeDataset;
            let root = d3.hierarchy(data);
            self.node_details = [];
            let wordList = [];
            root.each(d=>{
                // console.log(d);
                if(d.data.name == 'ROOT' || d.data.time_e == 'time'){return}
                self.node_details.push(d.data);
                wordList.push(...d.data.tree_topickey)
                wordList.push(...d.data.tree_keyword.flat())
                wordList.push(...d.data.tree_titlekeyword.flat())
            })
            // console.log(self.node_details);
            self.activeNames = ['1', '2'];

            console.log(wordList);
            const wordListCountDict = wordList.reduce((obj,key)=>{
                if (key in obj){
                    obj[key]++
                }else{
                    obj[key]=1
                }
                return obj
            },{})
            console.log(wordListCountDict);
            wordList = []
            for (const [key, value] of Object.entries(wordListCountDict)) {
                wordList.push({text: key, size: value * 10})
            }
            // wordList = [
            //     {text:'vue',size:20},
            //     {text:'html',size:25},
            //     {text:'js',size:30},
            // ]
            this.getWordCloud(wordList);
        }
    }
}
</script>
  
<style lang="less" scoped>
.sankeytree-node-iframe{
    width: 100%;
    height: 100%;
    overflow-y: scroll;
    .el-collapse-item-title{
        width: 90%;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        text-align: left;
    }
}
</style>

<style>
  .el-carousel__item h3 {
    color: #475669;
    font-size: 14px;
    opacity: 0.75;
    line-height: 200px;
    margin: 0;
  }
  
  .el-carousel__item:nth-child(2n) {
    background-color: #99a9bf;
  }
  
  .el-carousel__item:nth-child(2n+1) {
    background-color: #d3dce6;
  }


  .el-carousel__item--card{
    /* display: flex;
    align-items: center;
    justify-items: center; */
    overflow-y: auto;
    /* overflow-x: auto; */
  }

  .mytip {
    padding: 8px 16px;
    background-color: #ecf8ff;
    border-radius: 4px;
    border-left: 5px solid #50bfff;
    margin-top: 5px;
    }
    .el-collapse{
        background-color: #ecf8ff !important;
    }

    .el-collapse-item__header,.el-collapse-item__wrap {
        background-color: transparent !important;
    }
</style>