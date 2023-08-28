<template>
    <div class="sankeytree-node-iframe">
        <el-collapse v-model="node_details" @change="handleChange">
            <el-collapse-item v-for="(item,index) in node_details" :title="item.name" :name="index">
                <template #title>
                    <div class="el-collapse-item-title">{{ " [" + (index + 1) +"] " + item.name.split("+")[0]+"." }}</div>
                </template>
                <p> {{ item.node_detail_info[0].lines }}</p>
            </el-collapse-item>
        </el-collapse>
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
            node_details: []
        }
    },
    components: {
    },
    beforeMount: function () {
    },
    mounted: function () {
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
                size:[400,257],  // 盒子的宽高
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
            'storytree_finish'
        ])
    },
    watch: {
        storytree_finish:function(){
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