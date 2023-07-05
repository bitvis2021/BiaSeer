<template>
    <div class="media-storytree-container" ref="mediastorytree">
    </div>
</template>
  
<script>

import { mapState, mapMutations } from 'vuex';
import { getMediaStoryTreeData } from '@/communication/communicator.js'

export default {
    name: 'MediaStoryTree',
    props: {
        msg: String,
        topic_code: String,
    },
    data() {
        return {
            width: null,
            height: null,
            domain: 'msn.com',
        }
    },
    computed: {
        ...mapState([
            'currMedium',
            'mediaMatrixSelectedSignal',
        ])
    },
    watch: {
        currMedium: function () {
            let self = this;
        },
        mediaMatrixSelectedSignal: function(){
            let self = this;
            console.log(self.mediaMatrixSelectedSignal);
            if(self.isToGetStroytree()){
                self.getStroyTree();
            }
        }
    },
    mounted: function () {
        let self = this;
        self.width = self.$refs.mediastorytree.clientWidth;
        self.height = self.$refs.mediastorytree.clientHeight;

    },
    methods: {
        isToGetStroytree(){
            let data = sysDatasetObj.mediaMatrixSelected;
            console.log(data);
            console.log(data['date'].size);
            if(data['date'].size > 0){
                return true;
            }
            return false;
        },
        getStroyTree(){
            let self = this;
            let mediaMatrixSelectedDataDeferObj = $.Deferred();
            $.when(mediaMatrixSelectedDataDeferObj).then(async() => {
                // self.loadingData = false;
            })
            getMediaStoryTreeData(sysDatasetObj.mediaMatrixSelected, function(data){
                sysDatasetObj.updateStoryTreeDataset(data);
                mediaMatrixSelectedDataDeferObj.resolve();
            });
        }
    }
}
</script>
  
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
.media-storytree-container {
    width: 100%;
    height: 100%;
}
</style>
<style>
</style>