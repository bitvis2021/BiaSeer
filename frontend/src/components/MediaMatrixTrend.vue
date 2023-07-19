<template>
    <div class="media-matrix-trend-container" ref="mediamatrixtrend">
    </div>
</template>
  
<script>

import { mapState, mapMutations } from 'vuex';
import { getTopic } from '../assets/data/topicList';

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
            selected: {'topics': new Set(), 'date_index': new Set(), 'date': new Set()},
        }
    },
    computed: {
        ...mapState([
            'currMedium',
            'concatdiff_finish',
        ])
    },
    watch: {
        currMedium: function () {
            let self = this;
            self.drawExample(self.width, self.height, self.currMedium, 'single');
        },
        concatdiff_finish: function() {
            let self = this;
            self.drawExample(self.width, self.height, self.currMedium, 'concat');
        }
    },
    mounted: function () {
        let self = this;
        self.width = self.$refs.mediamatrixtrend.clientWidth;
        self.height = self.$refs.mediamatrixtrend.clientHeight;
        self.drawExample(self.width, self.height, self.currMedium, 'single');

    },
    methods: {
        ...mapMutations([
            'UPDATE_MATRIX_SELECTED_SIGNAL'
        ]),
        drawExample(width, height, domain, flag) {
            // https://observablehq.com/d/8d37e6aa05ce1b9a
            let self = this;
            let data1 = null;
            if(flag === 'single'){
                data1 = sysDatasetObj.mediaMatrixDataSet.filter(ele => ele['domain'] == domain)[0];
            }
            else if(flag === 'concat'){
                data1 = sysDatasetObj.mediaConcatDiffDataSet[0];
            }
            console.log(data1);
            
            let xdata = data1['values'][0]['details'].map(ele=>ele['date0']);
            // console.log(xdata);
            let ydata = data1.values.map(ele => ele.topic);
            let vdata = [];
            data1.values.forEach(element => {
                element.details.forEach(ele=>{
                    vdata.push(ele.value);
                })
            });

            let computeColorNeg = d3.interpolate('red', 'white');
            let linearVDataNeg = d3.scaleLinear()  
                .domain([d3.min(vdata), 0])
                .range([0, 1]);
            
            let computeColorPos = d3.interpolate('white', 'green');
            let linearVDataPos = d3.scaleLinear()  
                .domain([0, d3.max(vdata)])
                .range([0, 1]);
            
            let rectWH = 10;
            let m = ({ l: 95, r: 25, t: 10, b: 30 });            
            let x = d3.scaleTime().range([m.l, width - m.r]).domain(d3.extent(xdata, d => new Date(d)));
            let y = d3.scaleLinear()
                .domain(d3.extent(ydata, d => +d))
                .range([m.t, height - m.b]);
            
            let xAxis = g => g.append('g')
                .attr('transform', `translate(0, ${height - m.b + rectWH})`)
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
            
            let yG = svg.append('g')
                .attr('class', 'xyG')
                .call(yAxis);
            
            let xG = svg.append('g')
                .attr('class', 'xyG')
                .call(xAxis);
            
            xG.select(".domain").remove();
            yG.select(".domain").remove();
            yG.selectAll("text")
                .text((d,i)=> {
                    return getTopic((i + 1).toString())});
                
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
                // .attr("rx",2)
                // .attr("ry",2)
                .attr("width", rectWH)
                .attr("height", rectWH)
                .attr('fill', d=> {
                    if(d.value > 0) return computeColorPos(linearVDataPos(d.value));
                    else if((d.value < 0)) return computeColorNeg(linearVDataNeg(d.value));
                    else return '#f9f9f9';
                })
                // .attr("fill", d=> d.value != 0 ? 'steelblue' : 'none')
                // .attr("stroke", 'steelblue')
            
            charts.append('title')
                .text(d=>`from ${d.date0} to ${d.date1}, avgtone: ${d.value}`)

            let brush = d3.brush()
                .extent([[0, 0], [width, height]])
                .on('start brush', brushed)
                .on('end', d=>{ // ending brush, gain storytree and draw stroytree
                    sysDatasetObj.updateMediaMatrixSelected(self.selected);
                    self.UPDATE_MATRIX_SELECTED_SIGNAL();
                    return brushed;
                })

            function brushed() {
                let selection = d3.event.selection;
                if (selection === null){
                    charts.attr('fill', d=> {
                        if(d.value > 0) return computeColorPos(linearVDataPos(d.value));
                        else if((d.value < 0)) return computeColorNeg(linearVDataNeg(d.value));
                        else return '#f9f9f9';
                    })
                    self.selected = {'topics': new Set(), 'date_index': new Set(), 'date': new Set()};
                }
                else {
                    let [minX, minY] = d3.event.selection[0] || [];
                    let [maxX, maxY] = d3.event.selection[1] || [];
                    
                    self.selected = {'topics': new Set(), 'date_index': new Set(), 'date': new Set()};

                    charts.attr('stroke', (d,i) =>{ // i represents the i-th time range index
                        if(minX <= x(new Date(d.date0)) 
                            && x(new Date(d.date0)) <= maxX
                            && minY <= y(d.topic)
                            && y(d.topic) <= maxY 
                        ){
                            self.selected['topics'].add(d.topic);
                            self.selected['date_index'].add(i);
                            self.selected['date'].add(d.date0);
                            return 'red';
                        }
                        else{
                            // return 'steelblue';
                            return '';
                        }
                    })                    
                }
            }

            let brushG = svg.append('g')
                .attr("class", "brushG")
                .call(brush)
                .select('.selection').append('title')
                .text('aaa');
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