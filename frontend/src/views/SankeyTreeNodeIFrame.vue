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
    </div>
</template>
  
<script>
// Structors
import { mapState, mapMutations } from 'vuex';

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
        // self.drawStoryTree(self.width, self.height);
    },
    methods: {
        ...mapMutations([
            // 'UPDATE_STORYTREE_FINISH',
        ]),  
        handleChange(val) {
            console.log(val);
        },
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
            root.each(d=>{
                // console.log(d);
                if(d.data.name == 'ROOT' || d.data.time_e == 'time'){return}
                self.node_details.push(d.data);
            })
            // console.log(self.node_details);
            self.activeNames = ['1', '2']
        },
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