<template>
    <div class="media-scatter-container" ref="mediascatter">
    </div>
</template>
  
<script>

import { mapState, mapMutations } from 'vuex';
import { getTopic } from '../assets/data/topicList'


export default {
    name: 'MediaScatter',
    props: {
        msg: String
    },
    data() {
        return {
            width: null,
            height: null,
            innerWidth: null,
            innerHeight: null,
            overlap: 2,
            margin: null,
            step: null,
            color: null,
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
            mouse_this: null,
            horizon_chart_class: null,
            lineGenerator: null,
        }
    },
    mounted: function () {
        this.width = this.$refs.mediascatter.clientWidth;
        this.height = this.$refs.mediascatter.clientHeight;
        this.drawContour(this.width, this.height);
    },
    computed: {
        ...mapState([
            'currMedium',
        ]),
    },
    watch: {
        currMedium: function () {
            let self = this;
            self.gainMediaHorizonChartData(self.currMedium);
            self.drawMediaHorizonChart(self.currMedium);
        },
    },
    methods: {
        ...mapMutations([
            'UPDATE_CURRENT_MEDIUM',
            'UPDATE_MEDIA_SCATTER_CLICK'
        ]),

        drawContour(width, height) {
            // https://vizhub.com/curran/65a26f760f5b4d3f976d1cd7cb43a221

            let self = this;

            d3.select(self.$el)
                .select(".media__contour__svg")
                .remove();

            const xValue = d => d.x1;
            const yValue = d => d.x2;
            const rValue = d => d.nums;

            const margin = { top: 20, right: 20, bottom: 20, left: 20 };
            const innerWidth = width - margin.left - margin.right;
            const innerHeight = height - margin.top - margin.bottom;

            const svg = d3
                .select(self.$el)
                .append("svg")
                .attr("class", "media__contour__svg")
                .attr('viewBox', [0, 0, width, height])

            let contour_g = svg.append("g")
                .attr("class", "media-point-contour-g");
            
            let graph_g = svg.append("g")
                .attr("class", "media-point-graph-g")
                .attr("width", innerWidth)
                .attr("height", innerHeight)
                .attr("transform", `translate(${margin.left}, ${margin.top})`)

            let circle_g = svg.append("g")
                .attr("class", "media-point-circle-g")
                .attr("width", innerWidth)
                .attr("height", innerHeight)
                .attr("transform", `translate(${margin.left}, ${margin.top})`)

            let xScale = d3.scaleLinear().range([0, innerWidth]);
            let yScale = d3.scaleLinear().range([innerHeight, 0]);
            let rScale = null;

            let xScaleCopy = xScale.copy();
            let yScaleCopy = yScale.copy();

            const colorScale = d3.scaleSequential(d3.interpolate(d3.interpolateReds(0), d3.interpolateReds(0.4)));
            let zoomScale_k = null;
            const t = svg.transition().duration(1000);
            const circle_r = 3.5;


            function xyScale(data) {
                let sdata = data['details'];
                xScale.domain(d3.extent(sdata, xValue));
                yScale.domain(d3.extent(sdata, yValue));
                let rMaxMin = d3.extent(sdata, rValue);
                console.log(rMaxMin);
                rScale = (nums) => {
                    if (data.topic == "RUS_UKR") {
                        return d3.scaleLinear().domain(rMaxMin).range([5, 13])(nums);
                    }
                }
                self.xScale = xScale;
                self.yScale = yScale;
                xScaleCopy.domain(d3.extent(data, xValue));
                yScaleCopy.domain(d3.extent(data, yValue));
            }

            function renderContours(data, bandwidth) {
                let sdata = data['details'];
                const contourData = d3.contourDensity()
                    .x(d => xScale(xValue(d)))
                    .y(d => yScale(yValue(d)))
                    .size([innerWidth, innerHeight])
                    .bandwidth(bandwidth)
                    (sdata);

                colorScale.domain(d3.extent(contourData, d => d.value));

                const contours = contour_g
                    .attr("stroke-linejoin", "round")
                    .selectAll("path").data(contourData);

                contours
                    .join(
                        enter => enter.append("path")
                            .attr("d", d3.geoPath())
                            .attr("fill", d => colorScale(d.value)),
                        update => update
                            .call(update => update
                                .attr("d", d3.geoPath())
                                .attr("fill", d => colorScale(d.value))
                            ),
                        exit => exit
                            .remove()
                    );
            }

            function renderCircles(data) {

                const circles = circle_g
                    .selectAll(".dot")
                    .data(data['details']);

                circles
                    .join(
                        enter => enter.append("circle")
                            .attr("class", "dot")
                            .attr("transform", transform)
                            .attr("id", d => "media_id_" + d.domain.replaceAll(".", "_"))
                            .attr("cx", function (d) { return xScale(d.x1); })
                            .attr("cy", function (d) { return yScale(d.x2); })
                            .attr("r", d => rScale(d.nums)),
                        update => update
                            .call(update => update
                                .attr("transform", transform)
                                .attr("id", d => "media_id_" + d.domain.replaceAll(".", "_"))
                                .attr("cx", function (d) { return xScale(d.x1); })
                                .attr("cy", function (d) { return yScale(d.x2); })
                                .attr("r", d => rScale(d.nums))),
                        exit => exit
                            .remove()
                    )
                    .on("mouseover", function (d) {
                        self.UPDATE_CURRENT_MEDIUM(d.domain);
                        self.mouse_this = d3.mouse(this);
                        // hover highlight
                        d3.select(this).classed("dot_mouseover", true);
                        // draw mediagraph
                        self.drawMediaGraph(d.domain);
                    })
                    .on("mouseout", function (d) {
                        // d3.select(this).classed("dot_mouseover", false);
                    })
                    .on("click", function (d) {
                        self.UPDATE_MEDIA_SCATTER_CLICK();
                        sysDatasetObj.updateMediaScatterSelected(d.domain);
                    })

            }

            function transform(d) {
                return `translate(${0}, ${0})`;
            }

            let data = sysDatasetObj.mediaDataSet;
            data['details'].forEach(d => {
                d.x1 = +d.x1;
                d.x2 = +d.x2;
                d.id = +d.id;
                d.nums = +d.nums;
            });

            console.log('data:', data);

            xyScale(data);
            let tdata = data;
            // let tdata = data.filter(d=> +d.zoom_0 == 1);
            renderCircles(tdata);
            // renderContours(tdata, 55);
            // d3.select(this.$el).select(".media-point-contour-g").on('mousemove', () => {
            //     renderContours(tdata, (d3.event.x / 10) );
            // });
            // self.zoomOperator = d3.zoom()
            //     .extent([[0, 0], [innerWidth, innerHeight]])
            //     .scaleExtent([self.zoomMinRatio, self.zoomMaxRatio])
            //     .duration(1000)
            //     .on("zoom", zoomed);
            // svg.call(self.zoomOperator);

            // function zoomed() {
            //     // 1. clear media circle tooltip.
            //     circle_g
            //         .select(".circlr_g__contour_tooltip")
            //         .remove();
            //     // 2. rescale x y.
            //     xScale = d3.event.transform.rescaleX(xScaleCopy);
            //     yScale = d3.event.transform.rescaleY(yScaleCopy);

            //     // 3. get zoom scale.
            //     let zoomScale_k = d3.event.transform.k;
            //     tdata = data.filter(d=> +d["zoom_"+Math.floor(zoomScale_k-1)] == 1);
            //     // 4. transform media circle.
            //     d3.select(self.$el).selectAll(".dot").attr("transform", transform);                 
            //     // 5. 
            //     renderCircles(tdata);
            //     // 6. filter media which can be viewed.
            //     let dots = d3.select(self.$el).selectAll(".dot").filter(function() {
            //         return d3.select(this).attr("cx") > margin.left &&
            //         d3.select(this).attr("cx") < innerWidth &&
            //         d3.select(this).attr("cy") > margin.top &&
            //         d3.select(this).attr("cy") < innerHeight;
            //     });
            //     // console.log("dots: ", dots);
            //     tdata = []
            //     dots.filter(d=>{
            //         tdata.push(d);
            //     });
            //     renderCircles(tdata);
            //     renderContours(tdata, 25);
            // }
        },
        drawMediaHorizonChart(domain) {
            console.log(domain);
            let self = this;
            let width = 761 / 2;
            let height = 293 / 2;

            let delta = 30;

            self.horizon_chart_class = "media_horizon_chart_tooltip_div";
            d3.select("body").selectAll("." + self.horizon_chart_class).remove();

            let add_div = d3.select("body").append("div")
                .attr("class", self.horizon_chart_class)
                .attr("id", "div1024")
                .style('position', 'absolute')
                .style('top', d => {
                    return delta + self.mouse_this[1] + "px";
                })
                .style('left', function () {
                    return delta + self.mouse_this[0] + "px"
                })
                .style('width', width + "px")
                .style('height', height + 19 + "px");

            add_div.append("i")
                .attr("class", "el-icon-close close-icon")
                .on("click", function () {
                    d3.select("body").select("#div1024").remove();
                })

            add_div.append("div")
                .append("span")
                .attr("class", "summary_container_title")
                .text(domain)

            self.move("div1024");
            self.drawMediaHorizonChartII(width, height, self.horizon_chart_class);
        },
        drawMediaHorizonChartII(width, height, selected_div) {
            let self = this;
            //==================
            self.overlap = 2;

            self.margin = { top: 0, right: 0, bottom: 0, left: 0 };
            self.innerWidth = width - self.margin.left - self.margin.right;
            self.innerHeight = height - self.margin.top - self.margin.bottom;

            self.step = (height - (self.margin.top + self.margin.bottom)) / self.draw_data.length - 1;
            let colorArr = ["#fddbc7", "#f4a582", "#4393c3", "#92c5de", "#d6604d", "#b2182b", "#67001f"];
            self.color = i => colorArr[i + (i >= 0) + self.overlap];
            self.mirror = false;
            self.xValue = d => new Date(d.date);
            self.yValue = d => d.value + d.value1;
            self.max = d3.max(self.data, d => Math.abs(self.yValue(d)));
            self.yScale = d3.scaleLinear().range([self.overlap * self.step, -self.overlap * self.step]).domain([-self.max, +self.max]);
            self.xScale = d3.scaleTime().range([0, width]).domain(d3.extent(self.data, self.xValue));

            self.xAxis = g => g
                .attr("transform", `translate(0,${self.margin.top})`)
                .call(d3.axisTop(self.xScale).ticks(width / 40).tickSizeOuter(0))
                .call(g => g.selectAll(".tick").filter(d => self.xScale(d) < self.margin.left || self.xScale(d) >= width - self.margin.right).remove())
                .call(g => g.select(".domain").remove());

            self.areaGenerator = d3.area()
                .curve(d3.curveBasis)
                .x(d => self.xScale(self.xValue(d)))
                .y0(d => 0)
                .y1(d => self.yScale(self.yValue(d)));

            self.svg = d3.select("." + selected_div)
                .append("svg")
                .attr("width", width)
                .attr("height", height)
                .attr("viewBox", [0, 0, width, height])
                .attr("style", "font: 6px sans-serif;");

            self.horizong = self.svg.append("g").attr("class", "horizon-graph");

            self.horizong.selectAll('g').remove();

            self.clipPath = self.horizong.selectAll("g")
                .data(self.draw_data)
                .enter().append("g")
                .attr("class", "horizon-graph-sub")
                .attr("transform", (d, i) => `translate(0,${i * (self.step + 1) + self.margin.top})`)

            self.clipPath.append("clipPath")
                .attr("id", (d, i) => "area-clip-" + i)
                .append("rect")
                .attr("width", width)
                .attr("height", self.step);

            self.clipPath.append("defs").append("path")
                .attr("id", (d, i) => {
                    d.path = { 'id': "path-defs-" + i, 'href': '#path-defs-' + i }
                    return "path-defs-" + i;
                })
                .attr("d", d => self.areaGenerator(d.values));

            self.clipPath.append("g")
                .attr("clip-path", (d, i) => "url(#area-clip-" + i + ")")
                .selectAll("use")
                .data(d => {
                    return Array.from(
                        { length: self.overlap * 2 },
                        (_, i) => {
                            return Object.assign({ index: i < self.overlap ? -i - 1 : i - self.overlap }, d)
                        }
                    )
                })
                .enter().append("use")
                .attr("fill", d => {
                    return self.color(d.index)
                })
                .attr("transform", d => self.mirror && i < 0
                    ? `scale(1,-1) translate(0,${d.index * self.step})`
                    : `translate(0,${(d.index + 1) * self.step})`)
                .attr("xlink:href", d => d.path.href);

            self.clipPath.append("text")
                .attr("x", 4)
                .attr("y", self.step / 2)
                .attr("dy", "0.35em")
                .text(d => getTopic(d.key));
        },
        gainMediaHorizonChartData(domain) {
            let self = this;
            self.domain = domain;
            self.tmpdata = sysDatasetObj.mediaDataSet['details'].filter(ele => ele['domain'] == self.domain)[0];
            self.data = Object.values(self.tmpdata['doctone']).flat();
            self.draw_data = Object.values(self.tmpdata['doctone']).map(function (item, id) {
                return { 'key': id + 1, 'values': item };
            });
        },
        move(div_id) {
            console.log('div_id', div_id);
            var _move = false;
            div_id = '#' + div_id
            var _x, _y;
            $(div_id).click(function () {
                // alert("click")
            }).mousedown(function (e) {
                _move = true;
                _x = e.pageX - parseInt($(div_id).css("left"));
                _y = e.pageY - parseInt($(div_id).css("top"));
                $(div_id).fadeTo(20, 0.5);
            });
            $(document).mousemove(function (e) {
                if (_move) {
                    var x = e.pageX - _x;
                    var y = e.pageY - _y;
                    $(div_id).css({ top: y, left: x });
                }
            }).mouseup(function () {
                _move = false;
                $(div_id).fadeTo("fast", 1);
            });
        },
        clearHorizonGraphTooltip() {
            let self = this;
            d3.select("body").selectAll("." + self.horizon_chart_class).remove();
        },
        drawMediaGraph(domain) {
            let self = this;
            // console.log(sysDatasetObj.mediaDataSet);
            // console.log(tmpdata);
            let mediagraph = sysDatasetObj.mediaDataSet['mediagraph'];
            // console.log(mediagraph);
            let mediagraphValues = Object.values(mediagraph);

            let domainLinks = {}
            Object.entries(mediagraph).forEach(([key, value]) => {
                if (key.split("_").includes(domain)) {
                    domainLinks[key] = value
                }
            });
            let items = Object.keys(domainLinks).map(
                (key) => { return [key, domainLinks[key]] });
            items.sort(
                (first, second) => { return second[1] - first[1] }
            );
            let keys = items.map(e=>e[0]);
            let domainOneStep = {}

            let circles = d3.select(self.$el).select(".media__contour__svg").select(".media-point-circle-g").selectAll('circle')
            let circlesLocation = {}
            circles.each(function () {
                const thisD3 = d3.select(this)
                d3.select(this).classed("dot_mouseover", false);
                circlesLocation[thisD3.attr('id').split('media_id_')[1]] = [+thisD3.attr('cx'), +thisD3.attr('cy')]
            })
            // console.log(circlesLocation)

            for(let i = 0; i < 5; i++){
                let link_domain = keys[i].split("_");
                let path = [];
                path.push(circlesLocation[link_domain[0].replaceAll('.','_')])
                path.push(circlesLocation[link_domain[1].replaceAll('.','_')])
                domainOneStep[keys[i]] = {location: path, value: domainLinks[keys[i]]}
            }
            // console.log(keys);
            console.log(domainOneStep);
            // console.log(domaingraphValues);

            // circles.each(function () {
            //     if(Object.keys(domainOneStep).includes(d3.select(this).attr('id').split('media_id_')[1])){
            //         d3.select(this).classed("dot_mouseover", true);   
            //     }
            // })

            Object.keys(domainOneStep).forEach(ele=>{
                let link_domain = ele.split("_");
                d3.select(this.$el).select(".media__contour__svg").select(".media-point-circle-g")
                    .select('#media_id_' + link_domain[0].replaceAll(".","_"))
                    .classed("dot_mouseover", true)            
                d3.select(this.$el).select(".media__contour__svg").select(".media-point-circle-g")
                    .select('#media_id_' + link_domain[1].replaceAll(".","_"))
                    .classed("dot_mouseover", true)            
            })

            self.lineGenerator = d3.line()
                .x(d => d[0])
                .y(d => d[1]);

            const t = d3.select(self.$el).select(".media__contour__svg").select(".media-point-graph-g").transition()
                .duration(300);
            d3.select(self.$el).select(".media__contour__svg").select(".media-point-graph-g")
                .selectAll("path")
                .data(Object.keys(domainOneStep))
                .join(
                    enter => enter.append("path")
                        .attr("class", "link")
                        .attr("d", d=>{
                            console.log(d.split("_"));
                            console.log("enter");
                            return self.lineGenerator(domainOneStep[d]['location']);
                        })
                        ,
                    update => update
                        .call(update => update.transition(t)
                            .attr("d", d=>{
                                console.log(d.split("_"));
                                console.log("update");
                                return self.lineGenerator(domainOneStep[d]['location']);
                            })
                        ),
                    exit => exit
                        .remove()
                )
        }
    },
}
</script>
  
  <!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
.media-scatter-container {
    width: 100%;
    height: 100%;
}
</style>

<style>
.dot {
    fill: steelblue;
    opacity: 0.5;
}

.dot_mouseover {
    fill: red;
    stroke-width: 1.5px;
    stroke: red;
    opacity: 0.5;
}

.media_horizon_chart_tooltip_div {
    border: 1px solid black;
    background-color: white;
}

.summary_container_title {
    text-align: center;
    display: block;
    font: sans-serif;
    /* font-weight: bold; */
}

.close-icon {
    float: right;
    right: 12px;
}

.link{
    stroke: red;
    stroke-opacity: 0.5;
}
</style>