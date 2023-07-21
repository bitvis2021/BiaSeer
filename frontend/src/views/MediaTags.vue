<template>
    <div class="mediatags">
        <el-tag 
            size="medium"
            :key="tag" 
            v-for="tag in dynamicTags" 
            closable 
            :disable-transitions="false"
            @close="handleClose(tag)">
            {{ tag }}
        </el-tag>
        <el-button type="primary" size="mini" @click="gainConcatDiff">Concat</el-button>
    </div>
</template>
  
<script>
// Structors
import { mapState, mapMutations } from 'vuex';

export default {
    name: 'MediaTags',
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
            'UPDATE_MEDIA_DIFF_CONCAT_SIGNAL',
            'UPDATE_MEDIA_SCATTER_CLICK'
        ]),
        handleClose(tag) {
            this.dynamicTags.splice(this.dynamicTags.indexOf(tag), 1);
        },
        gainConcatDiff(){
            console.log("gain diff data...");
            let self = this;
            self.UPDATE_MEDIA_DIFF_CONCAT_SIGNAL();
            self.UPDATE_MEDIA_SCATTER_CLICK();
            sysDatasetObj.mediaScatterSelected = self.dynamicTags;
        }
    },
    computed: {
        ...mapState([
            'mediaScatterClick'
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
.mediatags{
    height: 100%;
    display: flex;
    justify-items: center;
    flex-direction: row;
}
</style>