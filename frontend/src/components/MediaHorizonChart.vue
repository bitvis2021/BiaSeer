<template>
    <div class="media-horizonchart-container" ref="mediahorizonchart">
    </div>
</template>
  
<script>

import { mapState, mapMutations } from 'vuex';

export default {
    name: 'MediaHorizonChart',
    props: {
        msg: String,
        topic_code: String,
    },
    data() {
        return {
            overlap: 2,
            margin: null,
            step: null,
            colorScale: null,
            mirror: null,
            xValue: null,
            yValue: null,
            max: null,
            yScale: null,
            xScale: null,
            tmpdata: null,
            draw_data: null,
            data: null,
            svg: null,
            horizong: null,
            xg: null,
            clipPath: null,

        }
    },
    computed: {
        ...mapState([
            'currMedium',
        ]),
    },
    watch: {
        currMedium: function () {
            let self = this;
        },
    },
    mounted: function () {
        let self = this;
        self.width = self.$refs.mediahorizonchart.clientWidth;
        self.height = self.$refs.mediahorizonchart.clientHeight;
        console.log(self.currMedium);
        self.gainMediaHorizonChartData(self.currMedium);
        self.drawMediaHorizonChart(self.width, self.height);
        self.renderMediaHorizonChart(self.width, self.height);
    },
    methods: {
        gainMediaHorizonChartData(domain){
            let self = this;
            self.domain = domain;
            self.tmpdata = sysDatasetObj.mediaDataSet['details'].filter(ele => ele['domain'] == self.domain)[0];
            self.data = Object.values(self.tmpdata['doctone']).flat();
            self.draw_data = Object.values(self.tmpdata['doctone']).map(function (item, id) {
                return {'key': id + 1, 'values': item};
            });
        },
        drawMediaHorizonChart(width, height) {
            let self = this;
            //==================
            self.overlap = 2;
            self.margin = {top: 30, right: 10, bottom: 0, left: 15};
            self.step = (height - (self.margin.top + self.margin.bottom) ) /  self.draw_data.length - 1;
            self.step = self.step * 2;
            self.colorScale = d3.scaleLinear().domain([-self.overlap, self.overlap]).range([0, 1]);
            self.mirror = false;
            self.xValue = d => new Date(d.date);
            self.yValue = d => d.value + d.value1;
            self.max = d3.max(self.data, d => Math.abs(self.yValue(d)));
            self.yScale = d3.scaleLinear().range([self.overlap * self.step, -self.overlap * self.step]).domain([-self.max, +self.max]);
            self.xScale = d3.scaleTime().range([0, width]).domain(d3.extent(self.data, self.xValue));
            
            self.xAxis = g => g
                .attr("transform", `translate(0,${self.margin.top})`)
                .call(d3.axisTop(self.xScale).ticks(width / 80).tickSizeOuter(0))
                .call(g => g.selectAll(".tick").filter(d => self.xScale(d) < self.margin.left || self.xScale(d) >= width - self.margin.right).remove())
                .call(g => g.select(".domain").remove());
            
            self.areaGenerator = d3.area()
                .x(d => self.xScale(self.xValue(d)))
                .y0(d => 0)
                .y1(d => self.yScale(self.yValue(d)));
            
            self.svg = d3.select(self.$el)
                .append("svg")
                .attr("width", width)
                .attr("height", height)
                .attr("viewBox", [0, 0, width, height])
                .attr("style", "max-width: 100%; height: auto; font: 10px sans-serif;");
            
            self.xg = self.svg.append("g")
                .call(self.xAxis);
            
            self.horizong = self.svg.append("g");
            
        },
        renderMediaHorizonChart(width, height){
            let self = this;

            const t = self.horizong.transition()
                .duration(750);
            
            self.clipPath = self.horizong.selectAll("g")
                .data(self.draw_data)
                .join(
                    enter => enter.append("g")
                            .attr("transform", (d, i) => `translate(0,${i * (self.step + 1) + self.margin.top})`),
                    update => update
                        .call(update => update.transition(t)
                            .attr("transform", (d, i) => `translate(0,${i * (self.step + 1) + self.margin.top})`)),
                    exit => exit
                            .remove()
                );
            
            self.clipPath
                .join(
                    enter => enter.append("clipPath")
                                .attr("id", (d,i)=>"area-clip-"+i)
                            .append("rect")
                                .attr("width", width)
                                .attr("height", self.step),
                    update => update
                        .call(update => update.transition(t)
                                .attr("width", width)
                                .attr("height", self.step)
                        ),
                    exit => exit
                            .remove()
                );
            
            self.clipPath
                .join(
                    enter => enter.append("defs")
                        .append("path")
                            .attr("id", (d,i)=>{
                                d.path = {'id': "path-defs-"+i, 'href': '#path-defs-'+i}
                                return "path-defs-"+i;
                            })
                            .attr("d", d => self.areaGenerator(d.values)),
                    update => update
                        .call(update => update.transition(t)
                                .attr("id", (d,i)=>{
                                    d.path = {'id': "path-defs-"+i, 'href': '#path-defs-'+i}
                                    return "path-defs-"+i;
                                })
                                .attr("d", d => self.areaGenerator(d.values))
                        ),
                    exit => exit
                            .remove()
                );
            
            self.clipPath.append("g")
                    .attr("clip-path", (d,i) => "url(#area-clip-" + i + ")")
                .selectAll("use")
                .data(d => {
                    return Array.from(
                        {length: self.overlap * 2}, 
                        (_, i) => {
                            return Object.assign({index: i < self.overlap ? -i - 1 : i - self.overlap}, d)
                        }
                    )
                })
                .enter().append("use")
                    .attr("fill", d => {
                        return d3.interpolateReds(self.colorScale(d.index))
                    })
                    .attr("transform", d => self.mirror && i < 0
                        ? `scale(1,-1) translate(0,${d.index * self.step})`
                        : `translate(0,${(d.index + 1) * self.step})`)
                    .attr("xlink:href", d => d.path.href);
            
            self.clipPath
                .join(
                    enter => enter.append("text")
                            .attr("x", 4)
                            .attr("y", self.step / 2)
                            .attr("dy", "0.35em")
                            .text(d => d.key),
                    update => update
                        .call(update => update.transition(t)
                            .attr("x", 4)
                            .attr("y", self.step / 2)
                            .attr("dy", "0.35em")
                            .text(d => d.key)
                        ),
                    exit => exit
                            .remove()
                );

        },
        renderMediaHorizonChart(width, height){
            let self = this;
            
            self.horizong = self.svg.append("g")
                .selectAll("g")
                .data(self.draw_data)
                .enter().append("g")
                .attr("transform", (d, i) => `translate(0,${i * (self.step + 1) + self.margin.top})`);
            
            self.horizong.append("clipPath")
                    .attr("id", (d,i)=>"area-clip-"+i)
                .append("rect")
                    .attr("width", width)
                    .attr("height", self.step);
            
            self.horizong.append("defs").append("path")
                .attr("id", (d,i)=>{
                    d.path = {'id': "path-defs-"+i, 'href': '#path-defs-'+i}
                    return "path-defs-"+i;
                })
                .attr("d", d => self.areaGenerator(d.values));
            
            self.horizong.append("g")
                    .attr("clip-path", (d,i) => "url(#area-clip-" + i + ")")
                .selectAll("use")
                .data(d => {
                    return Array.from(
                        {length: self.overlap * 2}, 
                        (_, i) => {
                            console.log(i);
                            return Object.assign({index: i < self.overlap ? -i - 1 : i - self.overlap}, d)
                        }
                    )
                })
                .enter().append("use")
                    .attr("fill", d => {
                        return d3.interpolateReds(self.colorScale(d.index))
                    })
                    .attr("transform", d => self.mirror && i < 0
                        ? `scale(1,-1) translate(0,${d.index * self.step})`
                        : `translate(0,${(d.index + 1) * self.step})`)
                    .attr("xlink:href", d => d.path.href);
            
            self.horizong.append("text")
                .attr("x", 4)
                .attr("y", self.step / 2)
                .attr("dy", "0.35em")
                .text(d => d.key);
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

<style>
/* path{
    fill: steelblue;
} */
</style>