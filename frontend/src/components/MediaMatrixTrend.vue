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
            domain: 'msn.com',
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
            self.drawExample(self.width, self.height, self.currMedium);
        }
    },
    mounted: function () {
        let self = this;
        self.width = self.$refs.mediamatrixtrend.clientWidth;
        self.height = self.$refs.mediamatrixtrend.clientHeight;
        self.drawExample(self.width, self.height, self.currMedium);
    },
    methods: {
        drawExample(width, height, domain) {
            let self = this;
            let data = d3.range(200).map(d => {
                return { x: d, y: Math.random() }
            });

            console.log(data);

            let data1 = sysDatasetObj.mediaMatrixDataSet.filter(ele => ele['domain'] == domain)[0];
            console.log(data1);

            let xdata = data1['values'][0]['details'].map(ele=>ele['date0']);
            console.log(xdata);
            let ydata = data1.values.map(ele => ele.topic);


            let m = ({ l: 25, r: 25, t: 10, b: 10 });

            
            let x = d3.scaleTime().range([m.l, width - m.r]).domain(d3.extent(xdata, d => new Date(d)));
            
            let y = d3.scaleLinear()
                .domain(d3.extent(ydata, d => +d))
                .range([height - m.b, m.t])
            
            let xAxis = g => g.append('g')
                .attr('transform', `translate(0, ${height - m.b})`)
                .call(d3.axisBottom(x))

            let yAxis = g => g.append('g')
                .attr('transform', `translate(${m.l}, 0)`)
                .call(d3.axisLeft(y))

            d3.select(self.$el).select('svg').remove();

            // svg
            let svg = d3.select(self.$el)
                .append('svg')
                .attr('width', width)
                .attr('height', height);
            
            let rectsG = svg.append('g')
                .attr('class', 'rectsG');
            
            let xyG = svg.append('g')
                .attr('class', 'xyG')
                // .call(xAxis)
                .call(yAxis);
            xyG.select(".domain").remove();
                
            rectsG.selectAll('g')
                .data(data1.values)
                .join('g')
                .attr('class', 'ggg')
                .attr('transform', d=>`translate(${0}, ${y(d.topic) - 5 / 2})`)
                .selectAll('rect')
                .data(d=>d.details)
                .join('rect')
                .attr('class', 'media_matrix_rect')
                .attr("x", d=> x(new Date(d.date0)))
                .attr("rx",2)
                .attr("ry",2)
                .attr("width",8)
                .attr("height",8)
                .attr("fill", d=> d.value != 0 ? 'steelblue' : 'none')

            
            
            

            // charts
            // let chart = svg.append('g')
            //     .call(xAxis)
            //     .call(yAxis)
            //     .selectAll('circle')
            //     .data(data)
            //     .join('circle')
            //     .attr('cx', d => x(d.x))
            //     .attr('cy', d => y(d.y))
            //     .attr('r', 5)
            //     // .attr('fill', 'steelblue')
            //     .attr('opacity', 0.4)
                // .on('mouseover', function() { d3.select(this).attr('fill', 'red') })
                // .on('mouseout', function() { d3.select(this).attr('fill', 'steelblue') })

            // chart.append('title')
            //     .text(d => d.y)

            // brush

            // let brush = d3.brushX()
            //     .extent([[m.l, m.t], [width - m.r, height - m.b]])
            //     .on('start brush end', brushed)

            // function brushed() {
            //     let selection = d3.event.selection

            //     if (selection === null) chart.attr('fill', null)
            //     else {
            //         let sx = selection.map(x.invert)
            //         chart.attr('fill', d => (sx[0] < d.x && d.x < sx[1]) ? 'red' : null)
            //             .attr('opacity', d => (sx[0] < d.x && d.x < sx[1]) ? 0.7 : 0.4)
            //             .attr('stroke', d => (sx[0] < d.x && d.x < sx[1]) ? 'red' : null)
            //     }
            // }

            // svg.append('g').call(brush)
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
<style>
/* .media_matrix_rect{
    fill-opacity: 0.5;
} */
</style>