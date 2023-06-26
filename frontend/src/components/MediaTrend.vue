<template>
    <div class="media-trend-container" ref="mediatrend">
    </div>
</template>
  
<script>

import { mapState, mapMutations } from 'vuex';

export default {
    name: 'MediaTrend',
    props: {
        msg: String
    },
    data() {
        return{
            xScale: null,
            xScale_1: null,
            yScale: null,
            xValue: null,
            yValue: null,
            xAxis: null,
            yAxis: null,
            xyg: null,
            clip: null,
            brush: null,
            svg: null,
            margin: null,
            innerHeight: null,
            innerWidth: null,
            lineg: null,
            lineGenerate: null,
            all: null,
            actor1: null,
            actor2: null,
            keys: ["all"]
        }
    },
    computed: {
        ...mapState([
            'currMedium',
        ])
    },
    mounted: function() {
        let self = this;
        self.width = self.$refs.mediatrend.clientWidth;
        self.height = self.$refs.mediatrend.clientHeight;
        console.log(self.currMedium);
        self.drawFeatureLine(self.width, self.height);
        self.renderFeatureTrending();
    },
    methods: {
        drawFeatureLine(width, height) {
            let self = this;
            self.margin = { top: 10, right: 10, bottom: 35, left: 40 };
            self.innerWidth = width - self.margin.left - self.margin.right;
            self.innerHeight = height - self.margin.top - self.margin.bottom;

            self.svg = d3.select(self.$el)
                .append("svg")
                .attr("class", "feature_trending")
                .attr("id", self.currMedium.replaceAll(".","_"))
                .attr("width", width)
                .attr("height", height);
            
            self.xyg = self.svg.append('g')
                .attr('transform', `translate(${self.margin.left},${self.margin.top})`);
            
            self.xScale = d3.scaleTime().range([0, self.innerWidth]);
            self.xAxis = d3.axisBottom(self.xScale).ticks(5);
            self.xyg.append("g")
                .attr('transform', `translate(${0},${self.innerHeight})`)
                .attr("class","myXaxis");
            
            self.yScale = d3.scaleLinear().range([self.innerHeight, 0]);
            self.yAxis = d3.axisLeft(self.yScale).ticks(5);
            self.xyg.append("g")
                .attr("class","myYaxis");
            
            // Add a clipPath: everything out of this area won't be drawn.
            self.clip = self.xyg.append("defs").append("svg:clipPath")
                .attr("id", "clip")
                .append("svg:rect")
                .attr("width", self.innerWidth)
                .attr("height", self.innerHeight)
                .attr("x", 0)
                .attr("y", 0);
            
            self.brush = d3.brushX()
                .extent([[0, 0], [self.innerWidth, self.innerHeight]]);
            
            self.lineg = self.xyg.append('g')
                .attr("clip-path", "url(#clip)")
                .attr("class", "brush")
                .attr("cursor", "pointer")
                .attr("width", self.innerWidth)
                .attr("height", self.innerHeight)
                .attr("x", 0)
                .attr("y", 0);
        },
        renderFeatureTrending(){
            let self = this;
            let data = sysDatasetObj.mediaDataSet;
            // console.log('data:', data);
            let medium = self.currMedium;
            // all data of msn.com
            let tmpdata = data['details'].filter(ele=>ele['domain'] == medium)[0];
            // console.log("tmpdata: ", tmpdata);

            let draw_data = tmpdata['doctone']['1'];
            console.log("draw_data: ", draw_data);

            
            let toneValue = d => d.value;
            let toneMinMax = d3.extent(draw_data, toneValue);
            console.log('toneMinMax', toneMinMax);
            let min_extent = toneMinMax[0];
            let max_extent = toneMinMax[1];

            
            // let keys = Object.keys(tmpdata[0]);
            // console.log("keys: ", keys);
            
            // let keys_extent = new Array();
            // let min_extent = 9999;
            // let max_extent = -999;
            // keys.forEach(ele=>{
            //     keys_extent[ele] = d3.extent(tmpdata.map(el=>el[ele]));
            //     if(keys_extent[ele][0] < min_extent){
            //         min_extent = keys_extent[ele][0];
            //     }
            //     if(keys_extent[ele][1] > max_extent){
            //         max_extent = keys_extent[ele][1]
            //     }
            // })
            // console.log("keys_extent: ", keys_extent);
            // console.log("min_max_extent: ", min_extent, max_extent);


            let xValue = d => new Date(d.date);
            let yValue = d => d.value;
            
            self.xValue = xValue;
            self.yValue = yValue;

            self.xScale.domain(d3.extent(draw_data, xValue));
            // sysDatasetObj.updateBrushTimeScopexScale(self.xScale);

            self.xyg.selectAll(".myXaxis").transition()
                .duration(2000)
                .call(self.xAxis);
            self.xyg.selectAll(".myXaxis").select('.domain').attr("stroke-width", 0.5);
            self.xyg.selectAll(".myXaxis")
                .selectAll("text")
                .attr("transform", "translate(-0,0)rotate(-30)")
                .style("text-anchor", "end")
                .on("mouseover", function(d) {
                        d3.select(this).classed("line-hover", true);
                    })
                .on("mouseout", function(d) {
                    d3.select(this)
                        .classed("line-hover", false);
                });

            
            // self.yScale.domain(d3.extent(data, yValue));
            self.yScale.domain([min_extent, max_extent]);

            console.log("self.yScale.domain", self.yScale.domain);

            self.xyg.selectAll(".myYaxis").transition()
                .duration(2000)
                .call(self.yAxis);
            
            self.xyg.selectAll(".myYaxis").select('.domain').attr("stroke-width", 0.5);
            self.xyg.selectAll(".myYaxis").select('.feature_trending_title').remove();
            self.xyg.selectAll(".myYaxis").append('text')
                .attr('class', 'feature_trending_title')
                .attr('y', 3)
                .attr('x', self.innerWidth)
                .attr('fill', '#606266')
                .attr('font-size', '1.3em')
                .style('text-anchor', 'end')
                .text(self.currMedium);
            
            self.xyg.selectAll(".myYaxis").selectAll("text")
                    .on("mouseover", function(d) {
                        d3.select(this).classed("line-hover", true);
                    })
                    .on("mouseout", function(d) {
                        d3.select(this)
                            .classed("line-hover", false);
                    });
            
            let updateg = self.lineg.selectAll(".line-path")
                .data(draw_data);
            
            self.lineGenerate = d3.line()
                    .x(d => self.xScale(self.xValue(d)))
                    .y(d => self.yScale(self.yValue(d)));
            
            updateg.exit().remove();
            
            // updateg
            //     .enter()
            //     .append("path")
            //     .attr("class", d=> "line-path "+ "line-path-" + d)
            //     .merge(updateg)
            //     .transition()
            //     .duration(2000)
            //     .attr("d", d=>{
            //         console.log(d);
            //         self.yValue = xd => xd[feature_name][d];
            //         return self.lineGenerate(data)
            //     });
            
            
            updateg
                .join(
                    enter => enter.append("path")
                        .attr("class", 'feature_trending')
                        // .attr("class", d=> "line-path "+ "line-path-" + d)
                        // .transition()   // 注释掉之后就可以 brush 了， 为什么？
                        // .duration(2000)
                        .attr("d", d=>{
                            // self.yValue = xd => xd[feature_name][d];
                            return self.lineGenerate(draw_data)
                        }),
                    update => update
                        .call(update => update
                            .attr("class", 'feature_trending')
                            // .attr("class", d=> "line-path "+ "line-path-" + d)
                            .transition()
                            .duration(2000)
                            .attr("d", d=>{
                                // self.yValue = xd => xd[feature_name][d];
                                return self.lineGenerate(draw_data)
                            })
                        ),
                    exit => exit
                        .remove()
                );



            // feature_trending_tooltip(
            //     self.svg, self.xyg, data,
            //     xValue, yValue,
            //     self.xScale, self.yScale,
            //     self.margin, self.feature_name,
            //     self.innerHeight, self.innerWidth,
            //     self.update_hover_date,
            //     self.update_hover_mouseY
            // );

            // self.brush.on("end", updateChart);

            // self.lineg.call(self.brush);


            // let idleTimeout;
            // function idled() { idleTimeout = null; }
            // function updateChart() {
            //     let extent = d3.event.selection;
            //     if (!extent) {
            //         if (!idleTimeout) return idleTimeout = setTimeout(idled, 350);
            //         self.xScale.domain(d3.extent(data, xValue));
            //         if (self.system_topic_event == "RUS_UKR"){
            //             self.update_brush_timescope("2021-06-01" + "+" + "2022-08-31");
            //         }
            //         if (self.system_topic_event == "GBR_EUR"){
            //             self.update_brush_timescope("2019-10-01" + "+" + "2020-02-01");
            //         }
            //         if (self.system_topic_event == "JPN_JPN"){
            //             self.update_brush_timescope("2020-01-01" + "+" + "2023-03-20");
            //         }

            //         sysDatasetObj.updateBrushTimeScopexScale(self.xScale);
            //         // self.update_brush_timescope(xScale);
            //     } else {

            //         let tmpbegintime = self.xScale.invert(extent[0]);
            //         var nowTime = new Date(tmpbegintime);
            //         let begintime = nowTime.getFullYear() + '-' + (nowTime.getMonth() + 1) + '-' +nowTime.getDate();
                    
            //         let begintimes = []
            //         begintime.split("-").forEach(ele=>{
            //             if(ele.length < 2){
            //                 begintimes.push("0"+ele);
            //             }else{
            //                 begintimes.push(ele);
            //             }
            //         })

            //         console.log("begintimes: ", begintimes.join("-"));  // 2021-12-02

            //         let tmpendtime = self.xScale.invert(extent[1]);
            //         var nowTime = new Date(tmpendtime);
            //         let endtime = nowTime.getFullYear() + '-' + (nowTime.getMonth() + 1) + '-' +nowTime.getDate();

            //         let endtimes = []
            //         endtime.split("-").forEach(ele=>{
            //             if(ele.length < 2){
            //                 endtimes.push("0"+ele);
            //             }else{
            //                 endtimes.push(ele);
            //             }
            //         })
            //         console.log("endtimes: ",endtimes.join("-"));  // 2021-12-02

            //         self.update_brush_timescope(begintimes.join("-") + "+" + endtimes.join("-"));

            //         // data.filter(d => self.xScale(xValue(d)) > extent[0] & self.xScale(xValue(d)) < extent[1]);
            //         self.xScale.domain([self.xScale.invert(extent[0]), self.xScale.invert(extent[1])]);
            //         sysDatasetObj.updateBrushTimeScopexScale(self.xScale);


            //         self.xyg.select(".brush").call(self.brush.move, null);
            //     }
            //     self.xyg.selectAll(".myXaxis").transition().duration(2000).call(d3.axisBottom(self.xScale).ticks(5));
            //     self.xyg.selectAll(".myXaxis")
            //         .selectAll("text")
            //         .attr("transform", "translate(-0,0)rotate(-30)")
            //         .style("text-anchor", "end");
            //     self.lineg.selectAll('.line-path')
            //         .transition().duration(2000)
            //         .attr('d', d=>{
            //             self.yValue = xd => xd[feature_name][d];
            //             return self.lineGenerate(data)
            //         });
            // }

        },
    }
}
</script>
  
  <!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
.media-trend-container {
    width: 100%;
    height: 50%;
}
</style>

<style>
.feature_trending{
    fill: steelblue;
}
</style>