<template>
    <div>
        <el-tag 
            size="medium"
            :key="tag" 
            v-for="tag in dynamicTags" 
            closable 
            :disable-transitions="false"
            @close="handleClose(tag)">
            {{ tag }}
        </el-tag>
    </div>
</template>
  
<script>
// Structors
import { mapState, mapMutations } from 'vuex';

export default {
    name: 'App',
    data() {
        return {
            dynamicTags:['msn.com'],
        }
    },
    components: {
    },
    beforeMount: function () {
    },
    methods: {
        ...mapMutations([
            // 'UPDATE_STORYTREE_FINISH',
        ]),
        handleClose(tag) {
            this.dynamicTags.splice(this.dynamicTags.indexOf(tag), 1);
        },
    },
    computed: {
        ...mapState([
            'mediaScatterClick'
            // 'currMedium',
            // 'mediaMatrixSelectedSignal',
        ])
    },
    watch: {
        mediaScatterClick: function(){
            this.dynamicTags = sysDatasetObj.mediaScatterSelected;
        }
    }
}
</script>
  
<style lang="less" scoped>
</style>
<style>
.el-tag + .el-tag {
    margin-left: 10px;
    margin-top: 3px;
}
</style>