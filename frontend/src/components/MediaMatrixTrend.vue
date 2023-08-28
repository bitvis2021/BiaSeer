<template>
    <div class="media-matrix-trend-container" ref="mediamatrixtrend">
    </div>
</template>
  
<script>

import { mapState, mapMutations } from 'vuex';
import { getTopic } from '../assets/data/topicList';
let reorder = require('@/assets/js/reorder');

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
            self.drawMediaMatrixTrend(self.width, self.height, self.currMedium, 'single');
        },
        concatdiff_finish: function() {
            let self = this;
            self.drawMediaMatrixTrend(self.width, self.height, self.currMedium, 'concat');
        }
    },
    mounted: function () {
        let self = this;
        self.width = self.$refs.mediamatrixtrend.clientWidth;
        self.height = self.$refs.mediamatrixtrend.clientHeight;
        self.drawMediaMatrixTrend(self.width, self.height, self.currMedium, 'single');

    },
    methods: {
        ...mapMutations([
            'UPDATE_MATRIX_SELECTED_SIGNAL'
        ]),
        drawMediaMatrixTrend(width, height, domain, flag) {
            // https://observablehq.com/d/8d37e6aa05ce1b9a
            let self = this;
            let data1 = null;
            if(flag === 'single'){
                data1 = sysDatasetObj.mediaMatrixDataSet.filter(ele => ele['domain'] == domain)[0];
            }
            else if(flag === 'concat'){
                data1 = sysDatasetObj.mediaConcatDiffDataSet[0];
            }
            // console.log(data1);

            let xdata = data1['values'][0]['details'].map(ele=>ele['date0']);
            let ydata = data1.values.map(ele => ele.topic);
            let matrix = []; // for reordering
            let vdata = [];
            data1.values.forEach(element => {
                matrix.push(element.details.map(ele=>ele.value));
                element.details.forEach(ele=>{
                    vdata.push(ele.value);
                })
            });

            let row_labels = [];
            let col_labels = [];
            for(let i = 0; i < matrix.length; i++){
                row_labels.push("" + (i + 1));
            }
            for(let i = 0; i < matrix[0].length; i++){
                col_labels.push("" + (i + 1));
            }

            // console.log(row_labels);
            // console.log(col_labels);

            var transpose = reorder.transpose(matrix),
                dist_rows = reorder.dist()(matrix),
                dist_cols = reorder.dist()(transpose),
                order = reorder.optimal_leaf_order(),
                row_perm = order.distanceMatrix(dist_rows)(matrix),
                col_perm = order.distanceMatrix(dist_cols)(transpose);
            

            let row_inv = reorder.inverse_permutation(row_perm);
            let col_inv = reorder.inverse_permutation(col_perm);
            // console.log(row_inv);
            // console.log(col_inv);
            // console.log(matrix);
            // console.log(vdata);

            let computeColorNeg = d3.interpolate('red', '#f9f9f9');
            let linearVDataNeg = d3.scaleLinear()  
                .domain([d3.min(vdata), 0])
                .range([0, 1]);
            
            let computeColorPos = d3.interpolate('#f9f9f9', 'green');
            if(flag === 'concat'){
                computeColorPos = d3.interpolate('#f9f9f9', 'gray');
            }
            let linearVDataPos = d3.scaleLinear()
                .domain([0, d3.max(vdata)])
                .range([0, 1]);
            
            let rectWH = 9;
            let m = ({ l: 97, r: 20, t: 6, b: 20 });
            let x = d3.scaleTime().range([m.l, width - m.r]).domain(d3.extent(xdata, d => new Date(d)));
            // let innerHeight = height - m.t - m.b;
            // let innerWidth = width - m.l;
  
            // let y = d3.scaleLinear()
            //     .domain(d3.extent(ydata, d => +d))
            //     .range([m.t, height - m.b]);
            let y = d3.scaleBand()
                .domain(ydata)
                .range([m.t, height - m.b]);
            
            let xAxis = g => g.append('g')
                .attr('transform', `translate(0, ${height - m.b})`)
                .call(d3.axisBottom(x))

            let yAxis = g => g.append('g')
                .attr('transform', `translate(${m.l}, ${0})`)
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
                .attr('class', 'yG')
                .call(yAxis);
            
            let xG = svg.append('g')
                .attr('class', 'xG')
                .call(xAxis);
            
            xG.select(".domain").remove();
            yG.select(".domain").remove();
            yG.selectAll("text")
                .text((d,i)=> {
                    return getTopic((i + 1).toString())
                });
                
            let charts = rectsG.selectAll('g')
                .data(data1.values)
                .join('g')
                .attr('class', 'ggg')
                .attr('transform', d=>`translate(${0}, ${y(d.topic)})`)
                .selectAll('rect')
                .data(d=>d.details)
                .join('rect')
                .attr('class', 'media_matrix_rect')
                .attr("x", d=> x(new Date(d.date0)))
                .attr("width", rectWH)
                .attr("height", rectWH)
                .attr('fill', d=> {
                    if(d.value > 0) return computeColorPos(linearVDataPos(d.value));
                    else if((d.value < 0)) return computeColorNeg(linearVDataNeg(d.value));
                    else return 'white';
                })
            
            charts.append('title')
                .text(d=>`from ${d.date0} to ${d.date1}, avgtone: ${d.value}`);
            
            
            var topicLocation = {}; // label i-th topic's location index
            var new_ydate = [];
            var t = svg.transition().duration(1000);
            t.selectAll(".ggg")
                .attr("transform", function(d, i) {
                    // console.log(i,'---',row_inv[i]+1);
                    topicLocation[row_inv[i]+1] = i + 1;
                    return "translate(0," + y((row_inv[i]+1).toString()) + ")"; 
                })
            
            t.selectAll(".yG").selectAll("text")
                .text((d,i)=> {
                    return getTopic(topicLocation[i+1].toString())});
                
            // console.log(topicLocation);
            new_ydate = Object.values(topicLocation).map(ele=>ele.toString())
            // console.log(new_ydate);
            let new_y = d3.scaleBand()
                .domain(new_ydate)
                .range([m.t, height - m.b]);

            let brush = d3.brush()
                .extent([[m.l, m.t], [width, height]])
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
                        else return white;
                    })
                    self.selected = {'topics': new Set(), 'date_index': new Set(), 'date': new Set()};
                }
                else {
                    let [minX, minY] = d3.event.selection[0] || [];
                    let [maxX, maxY] = d3.event.selection[1] || [];
                    
                    self.selected = {'topics': new Set(), 'date_index': new Set(), 'date': new Set()};

                    charts.attr('stroke', (d,i) =>{ // i represents the i-th time range index
                        // console.log(topicLocation)

                        if(minX <= x(new Date(d.date0)) 
                            && x(new Date(d.date0)) <= maxX
                            && minY <= new_y(d.topic)
                            && new_y(d.topic) <= maxY
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