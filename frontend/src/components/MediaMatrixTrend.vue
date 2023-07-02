<template>
    <div class="media-matrix-trend-container" ref="mediamatrixtrend">
    </div>
</template>
  
<script>

import { mapState, mapMutations } from 'vuex';

export default {
    name: 'MediaMatrixTrend',
    props: {
        msg: String,
        topic_code: String,
    },
    data() {
        return {
            width: null,
            height: null,
        }
    },
    computed: {
        ...mapState([
            'currMedium',
        ])
    },
    watch: {
        currMedium: function () {
            let self = this;
        }
    },
    mounted: function () {
        let self = this;
        self.width = self.$refs.mediamatrixtrend.clientWidth;
        self.height = self.$refs.mediamatrixtrend.clientHeight;
        self.drawExample(self.width, self.height);
    },
    methods: {
        drawExample(width, height) {
            let self = this;
            let data = d3.range(200).map(d => {
                return { x: d, y: Math.random() }
            });
            let m = ({ l: 50, r: 30, t: 30, b: 50 });

            // x y axis
            let x = d3.scaleLinear()
                .domain(d3.extent(data, d => d.x))
                .range([m.l, width - m.r])
            let y = d3.scaleLinear()
                .domain(d3.extent(data, d => d.y))
                .range([height - m.b, m.t])
            let xAxis = g => g.append('g')
                .attr('transform', `translate(0, ${height - m.b})`)
                .call(d3.axisBottom(x))
            let yAxis = g => g.append('g')
                .attr('transform', `translate(${m.l}, 0)`)
                .call(d3.axisLeft(y))

            // svg
            let svg = d3.select(self.$el)
                .append('svg')
                .attr('width', width)
                .attr('height', height)

            // charts
            let chart = svg.append('g')
                .call(xAxis)
                .call(yAxis)
                .selectAll('circle')
                .data(data)
                .join('circle')
                .attr('cx', d => x(d.x))
                .attr('cy', d => y(d.y))
                .attr('r', 5)
                // .attr('fill', 'steelblue')
                .attr('opacity', 0.4)
            // .on('mouseover', function() { d3.select(this).attr('fill', 'red') })
            // .on('mouseout', function() { d3.select(this).attr('fill', 'steelblue') })

            chart.append('title')
                .text(d => d.y)

            // brush

            let brush = d3.brushX()
                .extent([[m.l, m.t], [width - m.r, height - m.b]])
                .on('start brush end', brushed)

            function brushed() {
                let selection = d3.event.selection

                if (selection === null) chart.attr('fill', null)
                else {
                    let sx = selection.map(x.invert)
                    chart.attr('fill', d => (sx[0] < d.x && d.x < sx[1]) ? 'red' : null)
                        .attr('opacity', d => (sx[0] < d.x && d.x < sx[1]) ? 0.7 : 0.4)
                        .attr('stroke', d => (sx[0] < d.x && d.x < sx[1]) ? 'red' : null)
                }
            }

            svg.append('g').call(brush)
        }
    }
}
</script>
  
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
.media-matrix-trend-container {
    width: 100%;
    height: 100%;
}
</style>

<style></style>