<template>
    <div class="media-horizonchart-container" ref="mediahorizonchart">
    </div>
</template>
  
<script>

import { mapState, mapMutations } from 'vuex';

import d3 from '../assets/js/d3_horizon.js';

export default {
    name: 'MediaHorizonChart',
    props: {
        msg: String,
        topic_code: String,
        startColor: { type: String, default: '#ff7e71' },
        endColor: { type: String, default: '#00bd62' },
    },
    data() {
        return {
        }
    },
    computed: {
        ...mapState([
            'currMedium',
        ]),
        colors () {
            let i = d3.interpolate(this.startColor, this.endColor)
            return [i(0.0), i(0.25), i(0.5), i(0.75), i(1)]
        }
    },
    watch: {
        currMedium: function () {
            let self = this;
        },
        data: {
            handler: 'renderChart',
            deep: true
        }
    },
    mounted: function () {
        let self = this;
        self.width = self.$refs.mediahorizonchart.clientWidth;
        self.height = self.$refs.mediahorizonchart.clientHeight;
        console.log(self.currMedium);
        self.drawMediaHorizonChart(self.width / 1.5, self.height / 2);
    },
    methods: {
        drawMediaHorizonChart(width, height) {
            let self = this;

            let tmpdata = sysDatasetObj.mediaDataSet['details'].filter(ele=>ele['domain'] == 'msn.com')[0];

            let draw_data = tmpdata['doctone']['1'];

            let series = draw_data.map(ele=> ele.value + ele.value1);

            console.log(draw_data);

            // let series = [];
            // for (let i = 0, letiance = 0; i < 1500; i++) {
            //     letiance += (Math.random() - 0.5) / 10;
            //     series.push(Math.cos(i / 100) + letiance);
            // }            

            let chart = d3.horizon()
                .width(width)
                .height(height)
                .bands(this.colors.length)
                .mode('offset')
                .curve(d3.curveMonotoneX)
                .colors(this.colors)

            let data = []
            for (var i in series) {
                data.push([i, series[i]])
            }
            var svg = d3.select(this.$el)
                .append('svg')
                .attr('width', width)
                .attr('height', height)

            svg.data([data]).call(chart)

        }
    }
}
</script>
  
  <!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
.media-horizonchart-container {
    width: 100%;
    height: 100%;
}
</style>

<style></style>