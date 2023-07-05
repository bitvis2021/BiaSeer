<template>
    <div class="media-storytree-container" ref="mediastorytree">
    </div>
</template>
  
<script>

import { mapState, mapMutations } from 'vuex';

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
            console.log(sysDatasetObj.mediaMatrixSelected);
        }
    },
    mounted: function () {
        let self = this;
        self.width = self.$refs.mediastorytree.clientWidth;
        self.height = self.$refs.mediastorytree.clientHeight;

    },
    methods: {

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