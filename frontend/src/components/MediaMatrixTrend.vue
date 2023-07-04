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
            selected: {'topics': new Set(), 'date': new Set()},
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
            // self.drawExample(self.width, self.height, self.currMedium);
            self.render1Example(self.currMedium);
        }
    },
    mounted: function () {
        let self = this;
        self.width = self.$refs.mediamatrixtrend.clientWidth;
        self.height = self.$refs.mediamatrixtrend.clientHeight;
        self.draw1Example(self.width, self.height);
        self.render1Example(self.currMedium);
    },
    methods: {
        drawExample(width, height, domain) {
            // https://observablehq.com/d/8d37e6aa05ce1b9a
            let self = this;

            let data1 = sysDatasetObj.mediaMatrixDataSet.filter(ele => ele['domain'] == domain)[0];
            // console.log(data1);
            let xdata = data1['values'][0]['details'].map(ele=>ele['date0']);
            // console.log(xdata);
            let ydata = data1.values.map(ele => ele.topic);
            let m = ({ l: 30, r: 25, t: 10, b: 10 });            
            let x = d3.scaleTime().range([m.l, width - m.r]).domain(d3.extent(xdata, d => new Date(d)));
            let y = d3.scaleLinear()
                .domain(d3.extent(ydata, d => +d))
                .range([m.t, height - m.b]);
            
            let xAxis = g => g.append('g')
                .attr('transform', `translate(0, ${height - m.b})`)
                .call(d3.axisBottom(x))

            let yAxis = g => g.append('g')
                .attr('transform', `translate(${m.l}, 0)`)
                .call(d3.axisLeft(y).ticks(20))

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
                
            let charts = rectsG.selectAll('g')
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
                .attr("stroke", 'steelblue')
            
            // charts.append('title')
            //     .text(d=>`from ${d.date0} to ${d.date1}, avgtone: ${d.value}`)

            let brush = d3.brush()
                .extent([[0, 0], [width, height]])
                .on('start brush end', brushed)

            function brushed() {
                let selection = d3.event.selection;
                if (selection === null){
                    charts.attr('fill', d=> d.value != 0 ? 'steelblue' : 'none');
                    self.selected = {'topics': new Set(), 'date': new Set()};
                }
                else {
                    let [minX, minY] = d3.event.selection[0] || [];
                    let [maxX, maxY] = d3.event.selection[1] || [];

                    charts.attr('stroke', (d,i) =>{ // i represents the i-th time range index
                        if(minX <= x(new Date(d.date0)) 
                            && x(new Date(d.date0)) <= maxX
                            && minY <= y(d.topic)
                            && y(d.topic) <= maxY 
                        ){
                            self.selected['topics'].add(d.topic);
                            self.selected['date'].add(i);
                            // self.selected['date'].add(d.date0);
                            return 'red';
                        }
                        else{
                            return 'steelblue';
                        }
                    })
                }
            }

            let brushG = svg.append('g')
                .attr("class", "brushG")
                .call(brush)
                .select('.selection').append('title')
                .text('aaa')
        },
        draw1Example(width, height) {
            // https://observablehq.com/d/8d37e6aa05ce1b9a
            let self = this;
            self.m = ({ l: 30, r: 25, t: 10, b: 10 });

            self.svg = d3.select(self.$el)
                .append('svg')
                .attr('width', width)
                .attr('height', height);
            
            self.rectsG = self.svg.append('g')
                .attr('class', 'rectsG');
            
            self.xyG = self.svg.append('g')
                .attr('class', 'xyG');
            
            self.x = d3.scaleTime().range([self.m.l, width - self.m.r]);//.domain(d3.extent(xdata, d => new Date(d)));
            self.y = d3.scaleLinear()
                .range([self.m.t, height - self.m.b]);
            
            self.yAxis = d3.axisLeft(self.y).ticks(20);
            self.xyG.append("g")
                .attr("class","myYaxis")
                .attr('transform', `translate(${self.m.l}, 0)`);
                
            self.brush = d3.brush()
                .extent([[0, 0], [width, height]])
                .on('start brush end', brushed)

            function brushed() {
                let selection = d3.event.selection;
                if (selection === null){
                    self.charts.attr('fill', d=> d.value != 0 ? 'steelblue' : 'none');
                    self.selected = {'topics': new Set(), 'date': new Set()};
                }
                else {
                    let [minX, minY] = d3.event.selection[0] || [];
                    let [maxX, maxY] = d3.event.selection[1] || [];

                    self.charts.attr('stroke', (d,i) =>{ // i represents the i-th time range index
                        if(minX <= self.x(new Date(d.date0))
                            && self.x(new Date(d.date0)) <= maxX
                            && minY <= self.y(d.topic)
                            && self.y(d.topic) <= maxY 
                        ){
                            self.selected['topics'].add(d.topic);
                            self.selected['date'].add(i);
                            // self.selected['date'].add(d.date0);
                            return 'red';
                        }
                        else{
                            return 'steelblue';
                        }
                    })
                }
            }
        },
        render1Example(domain) {
            let self = this;
            let data1 = sysDatasetObj.mediaMatrixDataSet.filter(ele => ele['domain'] == domain)[0];
            let xdata = data1['values'][0]['details'].map(ele=>ele['date0']);
            let ydata = data1.values.map(ele => ele.topic);

            self.x.domain(d3.extent(xdata, d => new Date(d)));
            self.y.domain(d3.extent(ydata, d => +d));
            self.xyG.selectAll(".myYaxis")
                .call(self.yAxis);
            

            const t = self.rectsG.transition()
                .duration(1000);

            self.charts = self.rectsG.selectAll('g')
                .data(data1.values)
                .join('g')
                .attr('class', 'ggg')
                .attr('transform', d=>`translate(${0}, ${self.y(d.topic) - 5 / 2})`)
                .selectAll('rect')
                .data(d=>d.details)
                .join(
                    enter => enter.append("rect")
                            .attr("x", d=> self.x(new Date(d.date0)))
                            .attr("rx",2)
                            .attr("ry",2)
                            .attr("width",8)
                            .attr("height",8)
                            .attr("fill", d=> d.value != 0 ? 'steelblue' : 'none')
                            .attr("stroke", 'steelblue')
                        ,
                    update => update.call(
                            update => update.transition(t)
                            .attr("x", d=> self.x(new Date(d.date0)))
                            .attr("rx",2)
                            .attr("ry",2)
                            .attr("width",8)
                            .attr("height",8)
                            .attr("fill", d=> d.value != 0 ? 'steelblue' : 'none')
                            .attr("stroke", 'steelblue')
                        ),
                    exit => exit
                            .remove()
                );
            

            self.svg.append('g')
                .attr("class", "brushG")
                .call(self.brush)
                .select('.selection').append('title')
                .text('aaa')
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
.media_matrix_rect{
    /* stroke: steelblue; */
    stroke-width: 1px;
}
</style>