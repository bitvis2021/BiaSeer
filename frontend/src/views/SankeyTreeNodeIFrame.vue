<template>
    <div class="sankeytree-node-iframe" ref="iframediv">

        <div class="mytip" v-for="(item,index) in node_details2">
            <el-collapse>
                <el-collapse-item >
                    <template #title>
                        <h3 class="el-collapse-item-title"> {{ item.title.split("+")[0]+"."  }}</h3>
                    </template>
                    <p> {{ item.lines }}</p>
                </el-collapse-item>
            </el-collapse>
        </div>

        <!-- <div class="wordcloud">
            <div ref='wordCloudBox'></div>
        </div> -->

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
        },
        drawWordCloud(){
            let root = d3.hierarchy(sysDatasetObj.storyTreeDataset);
            let wordList = [];
            root.each(d=>{
                if(d.data.name == 'ROOT' || d.data.time_e == 'time'){return}
                wordList.push(...d.data.tree_topickey)
                wordList.push(...d.data.tree_keyword.flat())
                wordList.push(...d.data.tree_titlekeyword.flat())
            })
            // console.log(wordList);
            const wordListCountDict = wordList.reduce((obj,key)=>{
                if (key in obj){
                    obj[key]++
                }else{
                    obj[key]=1
                }
                return obj
            },{})
            wordList = []
            for (const [key, value] of Object.entries(wordListCountDict)) {
                wordList.push({text: key, size: value * 10})
            }
            this.getWordCloud(wordList);
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
                // self.node_details2.push(...d.node_detail_info);
                d.node_detail_info.forEach(ele=>{
                    self.node_details2.push(ele)
                    if(ele.related_infos.length > 0){
                        ele.related_infos.forEach(e=>{
                            self.node_details2.push(e)
                        })
                    }
                })
            })
            console.log('node_details2', self.node_details2)
            // 全局数据
            self.isShowCarousel = true;
        },
        storytree_finish: function(){
            let self = this;
            let data = sysDatasetObj.storyTreeDataset;
            let root = d3.hierarchy(data);
            self.node_details = [];
            self.node_details2 = [];
            root.each(d=>{
                if(d.data.name == 'ROOT' || d.data.time_e == 'time'){return}
                // self.node_details.push(...d.data.node_detail_info);
                d.data.node_detail_info.forEach(ele=>{
                    self.node_details2.push(ele)
                    if(ele.related_infos.length > 0){
                        ele.related_infos.forEach(e=>{
                            self.node_details2.push(e)
                        })
                    }
                })
            })
            self.activeNames = ['1', '2'];


            
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