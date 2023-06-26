<template>
    <div class="media-scatter-container" ref="mediascatter">
    </div>
</template>
  
<script>

import { mapState, mapMutations } from 'vuex';


export default {
    name: 'MediaScatter',
    props: {
        msg: String
    },
    data() {
        return{

        }
    },
    mounted: function() {
        this.width = this.$refs.mediascatter.clientWidth;
        this.height = this.$refs.mediascatter.clientHeight;
        this.drawContour(this.width, this.height);
    },
    methods: {
        ...mapMutations([
            'UPDATE_CURRENT_MEDIUM'
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

            const margin = { top: 10, right: 10, bottom: 20, left: 10 };
            const innerWidth = width - margin.left - margin.right;
            const innerHeight = height - margin.top - margin.bottom;

            const svg = d3
                .select(self.$el)
                .append("svg")
                .attr("class", "media__contour__svg")
                .attr('viewBox', [0, 0, width, height])

            let contour_g = svg.append("g")
                .attr("class", "media-point-contour-g");

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
                rScale = (nums) =>{
                    if(data.topic == "RUS_UKR"){
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
                            .attr("id", d=>"media_id_"+ d.domain.replaceAll(".","_"))
                            .attr("cx", function (d) { return xScale(d.x1); })
                            .attr("cy", function (d) { return yScale(d.x2); })
                            .attr("r", d=> rScale(d.nums)),
                        update => update
                            .call(update => update
                                .attr("transform", transform)
                                .attr("id", d=>"media_id_"+d.domain.replaceAll(".","_"))
                                .attr("cx", function (d) { return xScale(d.x1); })
                                .attr("cy", function (d) { return yScale(d.x2); })
                                .attr("r", d=> rScale(d.nums))),
                        exit => exit
                            .remove()
                    )
                    .on("mouseover", function(d) {
                        console.log(d);
                        self.UPDATE_CURRENT_MEDIUM(d.domain);
                    })
                    // .on("mouseover", function(d) {
                    //     console.log(d.media_name);


                    //     d3.select(this)
                    //         .classed("dot-hover", true);
                        
                    //     let m_data = [];
                    //     let m_cols = ["EventNums", "NumMentions", "NumArticles", "NumSources", "GoldsteinScale", "AvgTone"];
                    //     m_cols.forEach(ele=>{
                    //         // m_data.push(+d[ele]);
                    //         console.log(ele, d[ele]);
                    //         m_data.push(feature_extent_list[ele](+d[ele]));
                    //     })
                    //     console.log(m_data);
                    //     // console.log(m_cols);

                    //     let m_width = 100;
                    //     let m_height = 80;
                    //     let m_margin = { top: 5, right: 5, bottom: 5, left: 5 };
                    //     let m_innerWidth = m_width - m_margin.left - m_margin.right;
                    //     let m_innerHeight = m_height - m_margin.top - m_margin.bottom;

                    //     let tmp_g = circle_g
                    //         .append('g')
                    //             .attr('class', 'circlr_g__contour_tooltip')
                    //             .attr("transform",`translate(${xScale(d.x1)+45} , ${yScale(d.x2)+50} )`);
                        
                    //     let show_m_cols = ["Nums", "Mentions", "Articles", "Sources", "Impact", "Tone"];
                    //     let tmp_data = {
                    //         fieldNames: show_m_cols,
                    //         values: [
                    //             m_data
                    //         ]
                    //     };

                    //     console.log(tmp_data);
                        
                    //     // 设定一些方便计算的常量
                    //     let radius = 55;
                    //     let total = m_data.length;
                    //     let level = 4;
                    //     let rangeMin = 0;
                    //     let rangeMax = 100;
                    //     let arc = 2 * Math.PI;
                    //     let onePiece = arc / total;
                    //     // 计算网轴的正多边形的坐标
                    //     let polygons = {
                    //         webs: [],
                    //         webPoints: []
                    //     };
                    //     for(var k=level;k>0;k--) {
                    //         var webs = '',
                    //         webPoints = [];
                    //         var r = radius / level * k;
                    //         for(var i=0;i<total;i++) {
                    //             var x = r * Math.sin(i * onePiece),
                    //             y = r * Math.cos(i * onePiece);
                    //             webs += x + ',' + y + ' ';
                    //             webPoints.push({
                    //                 x: x,
                    //                 y: y
                    //             });
                    //         }
                    //         polygons.webs.push(webs);
                    //         polygons.webPoints.push(webPoints);
                    //     }
                    //     // 绘制网轴
                    //     var webs = tmp_g.append('g')
                    //             .classed('webs', true);
                    //     webs.selectAll('polygon')
                    //             .data(polygons.webs)
                    //             .enter()
                    //             .append('polygon')
                    //             .attr("id", (d,i) =>"webs-ploygon-" + i)
                    //             .attr('points', function(d) {
                    //                 return d;
                    //             });
                        
                    //     // 添加纵轴
                    //     var lines = tmp_g.append('g')
                    //             .classed('lines', true);
                    //     lines.selectAll('line')
                    //             .data(polygons.webPoints[0])
                    //             .enter()
                    //             .append('line')
                    //             .attr('x1', 0)
                    //             .attr('y1', 0)
                    //             .attr('x2', function(d) {
                    //                 return d.x;
                    //             })
                    //             .attr('y2', function(d) {
                    //                 return d.y;
                    //             });
                        
                    //     // 计算雷达图表的坐标
                    //     var areasData = [];
                    //     var values = tmp_data.values;
                    //     for(var i=0;i<values.length;i++) {
                    //         var value = values[i],
                    //         area = '',
                    //         points = [];
                    //         for(var k=0;k<total;k++) {
                    //             var r = radius * (value[k] - rangeMin)/(rangeMax - rangeMin);
                    //             var x = r * Math.sin(k * onePiece),
                    //             y = r * Math.cos(k * onePiece);
                    //             area += x + ',' + y + ' ';
                    //             points.push({
                    //                 x: x,
                    //                 y: y
                    //             })
                    //         }
                    //         areasData.push({
                    //             polygon: area,
                    //             points: points
                    //         });
                    //     }
                    //     // 添加g分组包含所有雷达图区域
                    //     var areas = tmp_g.append('g')
                    //             .classed('areas', true);
                    //     // 添加g分组用来包含一个雷达图区域下的多边形以及圆点
                    //     areas.selectAll('g')
                    //             .data(areasData)
                    //             .enter()
                    //             .append('g')
                    //             .attr('class',function(d, i) {
                    //                 return 'area' + (i+1);
                    //             });
                    //     for(var i=0;i<areasData.length;i++) {
                    //         // 依次循环每个雷达图区域
                    //         var area = areas.select('.area' + (i+1)),
                    //         areaData = areasData[i];
                    //         // 绘制雷达图区域下的多边形
                    //         area.append('polygon')
                    //                 .attr('points', areaData.polygon)
                    //                 // .attr('stroke', (d,i)=> getColor(i))
                    //                 // .attr('fill', (d,i)=> getColor(i));
                    //                 .attr('stroke', "#a65628")
                    //                 .attr('fill', "#a65628");
                                    
                    //         // 绘制雷达图区域下的点
                    //         var circles = area.append('g')
                    //                 .classed('circles', true);
                    //         circles.selectAll('circle')
                    //                 .data(areaData.points)
                    //                 .enter()
                    //                 .append('circle')
                    //                 .attr('cx', d=> d.x)
                    //                 .attr('cy', d=> d.y)
                    //                 .attr('r', 3)
                    //                 // .attr('stroke', (d,i)=>getColor(i))
                    //                 // .attr('fill', (d,i)=>getColor(i));
                    //                 .attr('stroke', "#a65628")
                    //                 .attr('fill', "#a65628");
                    //     }
                    //     // 计算文字标签坐标
                    //     var textPoints = [];
                    //     let delta_dis = 5;
                    //     var textRadius = radius + delta_dis;
                    //     for(var i=0; i < total; i++) {
                    //         var x = textRadius * Math.sin(i * onePiece);
                    //         var y = textRadius * Math.cos(i * onePiece);
                    //         textPoints.push({
                    //             x: x,
                    //             y: y
                    //         });
                    //     }
                    //     // 绘制文字标签
                    //     var texts = tmp_g.append('g')
                    //             .classed('texts', true);
                    //     texts.selectAll('text')
                    //             .data(textPoints)
                    //             .enter()
                    //             .append('text')
                    //             .attr('x', d=> d.x)
                    //             .attr('y', (d,i) => {
                    //                 if(i==0){
                    //                     return d.y + delta_dis;
                    //                 }
                    //                 return d.y
                    //             })
                    //             .attr('fill', "gray")
                    //             // .attr('fill', (d,i)=> getColor(i))
                    //             .attr('text-anchor', (d,i)=> {
                    //                 if(i==0 || i==3){
                    //                     return "middle";
                    //                 }else if(i==1 || i==2){
                    //                     return "start";
                    //                 }else{
                    //                     return "end";
                    //                 }
                    //             })
                    //             .text((d, i) => tmp_data.fieldNames[i]);
                        
                    //     // domain title
                    //     tmp_g.append("g")
                    //         .append('text')
                    //         .attr('class', 'domain-title')
                    //         .attr('y', textPoints[3].y - 2.5 * delta_dis)
                    //         .attr('x' , textPoints[3].x )
                    //         .text(d.media_name + " " + d.nums.toFixed(0));
                        
                    // })
                    // .on("mouseout", function(d) {
                    //     d3.select(this)
                    //         .classed("dot-hover", false);  
                    //     circle_g
                    //         .select(".circlr_g__contour_tooltip")
                    //         .remove();
                        
                    //     d3.select(self.$el)
                    //         .select(".media__contour__svg")
                    //         .select(".media-point-circle-g")
                    //         .selectAll("circle").classed("dot-search-hover", false);
                    // })
                    // .on("click", function(d) {
                    //     self.mSrc_list.forEach((ele,ie)=>{
                    //         d3.select("#media_id_"+ele.replaceAll(".","_")).classed("dot-click-"+ie, false)
                    //     })
                    //     if(self.click_media_id_list.indexOf(d.media_id)==-1){
                    //         self.click_count = self.click_count + 1;
                    //         self.click_media_id_list[self.click_count % self.click_media_id_list.length] = d.media_id;
                    //         self.mSrc_list[self.click_count % self.click_media_id_list.length] = d.media_name;
                    //         console.log("self.mSrc_list", self.mSrc_list);
                    //         self.update_selected_media_sources(self.mSrc_list.join("+"))
                            
                    //         // keep red-click
                    //         for(let i=0;i<17;i++){
                    //             d["zoom_"+i] = "1"
                    //         }
                    //     }
                    //     self.mSrc_list.forEach((ele,ie)=>{
                    //         d3.select("#media_id_"+ele.replaceAll(".","_")).classed("dot-click-"+ie, true)
                    //     });

                    // });
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
        }
    }
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
.dot{
    fill: steelblue;
    opacity: 0.5;
}
</style>