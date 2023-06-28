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
        self.drawMediaHorizonChart(self.width, self.height, self.currMedium);
    },
    methods: {
        drawMediaHorizonChart(width, height, domain) {
            let self = this;

            let tmpdata = sysDatasetObj.mediaDataSet['details'].filter(ele => ele['domain'] == domain)[0];

            let data = Object.values(tmpdata['doctone']).flat();

            var draw_data = Object.values(tmpdata['doctone']).map(function (item, id) {
                return {'key': id + 1, 'values': item};
            });

            console.log(draw_data);

            //==================
            let overlap = 2;
            let margin = {top: 30, right: 10, bottom: 0, left: 15};
            let step = (height - (margin.top + margin.bottom) ) /  draw_data.length - 1;
            // step = step * 10;
            let colorScale = d3.scaleLinear().domain([-overlap, overlap]).range([0, 1]);
            let mirror = false;
            let xValue = d => new Date(d.date);
            let yValue = d => d.value + d.value1;
            const max = d3.max(data, d => Math.abs(yValue(d)));
            console.log(max);
            let yScale = d3.scaleLinear().range([overlap * step, -overlap * step]).domain([-max, +max]);
            let xScale = d3.scaleTime().range([0, width]).domain(d3.extent(data, xValue));
            
            let xAxis = g => g
                .attr("transform", `translate(0,${margin.top})`)
                .call(d3.axisTop(xScale).ticks(width / 80).tickSizeOuter(0))
                .call(g => g.selectAll(".tick").filter(d => xScale(d) < margin.left || xScale(d) >= width - margin.right).remove())
                .call(g => g.select(".domain").remove());
            
            let areaGenerator = d3.area()
                .x(d => xScale(xValue(d)))
                .y0(d => 0)
                .y1(d => yScale(yValue(d)));

            //==================

            const svg = d3.select(self.$el)
                .append("svg")
                .attr("width", width)
                .attr("height", height)
                .attr("viewBox", [0, 0, width, height])
                .attr("style", "max-width: 100%; height: auto; font: 10px sans-serif;");
            
            const g = svg.append("g")
                .selectAll("g")
                .data(draw_data)
                .enter().append("g")
                .attr("transform", (d, i) => `translate(0,${i * (step + 1) + margin.top})`);
            
            g.append("clipPath")
                .attr("id", (d,i)=>"area-clip-"+i)
            .append("rect")
                .attr("width", width)
                .attr("height", step);
            
            g.append("defs").append("path")
                .attr("id", (d,i)=>{
                    d.path = {'id': "path-defs-"+i, 'href': '#path-defs-'+i}
                    return "path-defs-"+i;
                })
                .attr("d", d => areaGenerator(d.values));
            
            g.append("g")
                    .attr("clip-path", (d,i) => "url(#area-clip-" + i + ")")
                .selectAll("use")
                .data(d => {
                    console.log(d)
                    return Array.from(
                        {length: overlap * 2}, 
                        (_, i) => {
                            console.log(i);
                            return Object.assign({index: i < overlap ? -i - 1 : i - overlap}, d)
                        }
                    )
                })
                .enter().append("use")
                    .attr("fill", d => {
                        console.log(d);
                        return d3.interpolateGreens(colorScale(d.index))
                    })
                    .attr("transform", d => mirror && i < 0
                        ? `scale(1,-1) translate(0,${d.index * step})`
                        : `translate(0,${(d.index + 1) * step})`)
                    .attr("xlink:href", d => d.path.href);
            

            g.append("text")
                .attr("x", 4)
                .attr("y", step / 2)
                .attr("dy", "0.35em")
                .text(d => d.key);

            svg.append("g")
                .call(xAxis);

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