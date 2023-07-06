<template>
    <div class="media-storytree-container" ref="mediastorytree">
        <svg id="storytree__svg"></svg>
    </div>
</template>
  
<script>

import { mapState, mapMutations } from 'vuex';
import { getMediaStoryTreeData } from '@/communication/communicator.js'

export default {
    name: 'MediaStoryTree',
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
            'mediaMatrixSelectedSignal',
        ])
    },
    watch: {
        currMedium: function () {
            let self = this;
        },
        mediaMatrixSelectedSignal: function(){
            let self = this;
            console.log(self.mediaMatrixSelectedSignal);
            if(self.isToGetStroytree()){
                self.getStroyTree();
                self.drawStoryTree(self.width, self.height);
            }
        }
    },
    mounted: function () {
        let self = this;
        self.width = self.$refs.mediastorytree.clientWidth;
        self.height = self.$refs.mediastorytree.clientHeight;
        // drawStoryTree(self.width, self.height);
    },
    methods: {
        isToGetStroytree(){
            let data = sysDatasetObj.mediaMatrixSelected;
            console.log(data);
            console.log(data['date'].size);
            if(data['date'].size > 0){
                return true;
            }
            return false;
        },
        getStroyTree(){
            let self = this;
            let mediaMatrixSelectedDataDeferObj = $.Deferred();
            $.when(mediaMatrixSelectedDataDeferObj).then(async() => {
                // self.loadingData = false;
            })
            getMediaStoryTreeData(sysDatasetObj.mediaMatrixSelected, function(data){
                sysDatasetObj.updateStoryTreeDataset(data);
                mediaMatrixSelectedDataDeferObj.resolve();
            });
        },
        drawStoryTree(width, height) {
            let self = this;
            console.log(width, height);
            let margin = { top:15, bottom:55, left:10, right:20 };
            let innerWidth = width - margin.left - margin.right;
            let innerHeight = height - margin.top - margin.bottom;
            

            let renderStoryTree = (root, reScale, reScaleCircleRadia, delta_timeScale, attrsMaxMin, dx, dy, timescope) => {
                let x0 = Infinity;
                let x1 = -x0;
                root.each(d => {
                    if (d.x > x1) x1 = d.x;
                    if (d.x < x0) x0 = d.x;
                });
                d3.select(self.$el).select("#storytree__svg").selectAll('g').remove();
                
                const svg = d3.select(self.$el).select("#storytree__svg")
                    .attr("width", width - 10)
                    .attr("height", height - 10);

                svg.append("defs").html(`
                    <style>
                    .highlight circle { fill:black }
                    .highlight circle { fill:black }
                    .highlight text { fill:black }
                    .leaf circle { fill:black }
                    .leaf circle { fill:black }
                    .leaf text { fill:black }
                    path.highlight { stroke:black }
                    <style>`);

                const g = svg
                    .append("g")
                    .attr("font-family", "sans-serif")
                    .attr("font-size", 10)
                    .attr("transform", `translate(${margin.left},${margin.top})`);
                
                const timeAxis = d3.axisBottom(reScale);
                const xAxisG = g.append('g').call(timeAxis)
                    .attr('transform', `translate(${0},${innerHeight})`);
                xAxisG.selectAll("text")
                    .attr("transform", "translate(-0,0)rotate(-30)")
                    .style("text-anchor", "end")
                    .on("mouseover", function(d) {
                        d3.select(this).classed("line-hover", true);
                    })
                    .on("mouseout", function(d) {
                        d3.select(this)
                            .classed("line-hover", false);
                    });
                xAxisG.selectAll('.domain').remove();

                let delta_time_space = 3
                const delta_time_g = g
                    .append("g")
                    .attr('transform', `translate(${0},${innerHeight})`)
                    .attr("class", "delta_time_g")
                    .selectAll('.delta_time_rect')
                    .data(delta_time)
                    .enter()
                    .append('rect')
                    .attr('class', 'delta_time_rect')
                    .attr('x', (d,i)=>reScale(uni_delta_timescope[i + 1]) - reScale.bandwidth() / 2 + delta_time_space)
                    .attr('y', d => delta_time_space - delta_timeScale(d) / 2)
                    .attr('rx', d=> delta_timeScale(d) / 2)
                    .attr('width', reScale.bandwidth() - 2 * delta_time_space)
                    .attr('height', d=> delta_timeScale(d))
                    .on("mouseover", function(d) {
                        d3.select(this).classed("line-hover", true);
                    })
                    .on("mouseout", function(d) {
                        d3.select(this)
                            .classed("line-hover", false);
                    });
                    



                const link = g
                    .append("g")
                    .attr('transform', `translate(${reScale.bandwidth()/2},${0})`)
                    .attr("fill", "none")
                    .attr("stroke", "steelblue")
                    .attr("stroke-opacity", 0.4)
                    .selectAll("path")
                    .data(root.links())
                    .join("path")
                    .attr("d", d=>{
                        if(d.source.data.time_e == d.target.data.time_e){
                            alert("duplicate time [parent, child]")
                            let PosData = []
                            PosData.push([reScale(d.source.data.time_e), d.source.x])
                            PosData.push([reScale(d.target.data.time_e) + reScale.bandwidth()/2, d.target.x])
                            let lineGenerator = d3.line().curve(d3.curveStepBefore)
                            let lineData = lineGenerator(PosData)
                            return lineData;
                        }
                        else{
                            return d3.linkHorizontal()
                                .x(d => reScale(d.data.time_e))
                                .y(d => d.x)(d)
                        }
                    })
                    .attr("stroke-width", d=>{
                        return lineWidthScale(+d.target.data.tree_maxCompatibility)
                    })
                    .attr("stroke-opacity", d=>{
                        return lineFillScale(+d.target.data.tree_maxCompatibility)
                    })
                    .on("mouseover", function(d) {
                        d3.select(this).classed("line-hover", true);
                    })
                    .on("mouseout", function(d) {
                        d3.select(this)
                            .classed("line-hover", false);
                    });

                let node = g
                    .append("g")
                    .attr("class", "storytree__node")
                    .attr('transform', `translate(${reScale.bandwidth()/2},${0})`)
                    .attr("stroke-linejoin", "round")
                    .attr("stroke-width", 3)
                    .selectAll(".story_tree_node")
                    .data(root.descendants())
                    .join("g")
                    .attr("class", "story_tree_node")
                    .attr("id",d=>{
                        return "story_tree_node_" + d.index;
                    })
                    .attr("transform", d => {
                        if(d.depth > 1 && d.parent.data.time_e == d.data.time_e){
                            d.y = reScale(d.data.time_e) + reScale.bandwidth() / 2;
                            return `translate(${reScale(d.data.time_e) + reScale.bandwidth() / 2},${d.x})`;
                        }
                        return `translate(${reScale(d.data.time_e)},${d.x})`;                        
                    });
                
                // ===================circle=================//
                // node
                //     .append("circle")
                //     .attr("fill", "steelblue")
                //     // .attr("r", 8);
                //     .attr("r", d=> d.data.totalbias !="null" ? reScaleCircleRadia(+d.data.totalbias) : 1);
                
                // ===================pie=================//
                let piecolorScale = d3.scaleOrdinal()
                        .domain(d3.range(4))
                        .range(d3.schemeCategory10);
                
                let piecolorScale_1 = (i)=>{
                    let colorArray=['#1d6d99','#e56b10','#a6761d','#c6c361']
                    return colorArray[i%4];
                }
                
                
                self.piecolorScale = piecolorScale_1;
                
                let pie = d3.pie();

                node.each(ele=>{
                    self.mediasources = ele.data.mSrc_list;
                    // console.log("mediasources", self.mediasources);
                    let ele_g = d3.select(this.$el).select("#story_tree_node_" + ele.index).append("g")
                        .attr("class", "ele-g");
                    
                    let pie_r = ele.data.totalbias !="null" ? reScaleCircleRadia(+ele.data.totalbias) : 1;
                    
                    ele_g.selectAll(".story_tree_node_pie")
                        .data(d=>{
                            let dataset = d.data.tree_nodeSrcN.map(Number);
                            return pie(dataset);
                        })
                        .enter()
                        .append("g")
                        .attr("class", "story_tree_node_pie")
                            .append("path")
                            .attr("d",function(d,i){
                                return d3.arc()
                                    .innerRadius(0)
                                    .outerRadius(pie_r)(d);
                            })
                            .attr("fill",function(d,i){
                                return self.piecolorScale(i);
                            });
                });
                

                node
                    .append("text")
                    .attr("dy", "1.5em")
                    .attr("text-anchor", "middle")
                    .attr("fill", "steelblue")
                    .text(d=>{
                        let show_str = d.data.tree_topickey.slice(0,3).toString().replaceAll(",","; ")
                        return show_str == 'null' ? 'Story' : show_str;
                    })
                    .clone(true)
                    .lower()
                    .attr("stroke", "white");
                
                
            
                // ===================color tips=================//
                const corlortips = svg.append("g").attr("class", "story_tree_colortips")
                    .attr('transform', `translate(${innerWidth/5.5},${margin.top/2})`);
                
                let circles_tips = corlortips.selectAll("story_tree_colortips_icircle")
                    .data(self.mediasources)
                    .enter()
                    .append("g")
                    .attr("class", "story_tree_colortips_icircle");

                circles_tips.append("circle")
                    .attr("r", 5)
                    .attr("cx", (d,i) => {return i * 150 + 150})
                    .attr("fill", (d,i) => self.piecolorScale(i));

                circles_tips.append("text")
                    .attr("class", "story_tree_colortips_itext")
                    .attr("x", (d,i) => {return i * 150 + 150})
                    .attr("dy", "0.31em")
                    .attr("dx", "0.5em")
                    .attr("text-anchor", "start")
                    .attr("font-size", 15)
                    .attr("fill", (d,i) => self.piecolorScale(i))
                    .text(d=>{return d});
                
                
                // ===================node click=================//
                node.on("click", function(d) {
                    console.log(d);
                    self.UPDATE_TREE_NODE_CLICK(d.index + "+" + self.randomString(6));
                    self.drawer = true;
                });

                self.initLeftTopPos();

                // node.append("title")
                //     .text(d => self.title(d.data));
                function dist2(a, b) {
                    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2;
                }
                g.selectAll(".storytree__node")
                    .on("mouseover", function () {
                        const m = d3.mouse(this);
                        console.log("m:", m);
                        const leaf = node.data()[
                            d3.scan(node.data().map(d => dist2([reScale(d.data.time_e), d.x], m)))
                        ];
                        // console.log("leaf:", leaf);

                        let d = root
                            .links()
                            .filter(d => d.target === leaf)
                            .pop().target;
                        
                        d.m0 = m[0];
                        d.m1 = m[1];
                        
                        // console.log("d:", d);
                        d3.select("body").select("#div"+d.index).classed("hover_tree_node_click_div_highlight", true);

                        // add tree node hover tooltip
                        let m_width = 200;
                        let m_height = 80;
                        let m_margin = { top: 10, right: 5, bottom: 25, left: 30 };
                        let m_innerWidth = m_width - m_margin.left - m_margin.right;
                        let m_innerHeight = m_height - m_margin.top - m_margin.bottom;

                        let div_top = self.divPos.top;
                        let div_left = self.divPos.left;
                        let div_height = self.divPos.height;
                        let div_width = self.divPos.width;

                        d3.select("body").selectAll(".tree_node_hover_tooltip_div").remove();

                        let add_div = d3.select("body").append("div")
                            .attr("class", "tree_node_hover_tooltip_div");
                        
                        let hover_summary = add_div.append("div")
                            .attr("class", "tree_node_hover_tooltip_div_sub")
                            .attr("id","hover_summary"+m[0]);
                        
                        var sub_div = document.getElementById("hover_summary"+m[0]);
                        sub_div.innerHTML += d.data.name.split("+")[0] + ".";
                        let sub_div_height = sub_div.getBoundingClientRect().height;
                        let m_height_all = m_height + sub_div_height
                        add_div
                            .style('position','absolute')
                            .style('top', d=>{
                                // console.log("location: ", m[1], m_height_all, m[1] + m_height_all, div_height)
                                if(m[1] + m_height_all > div_height){
                                    return (div_top + m[1] - m_height_all) + "px"
                                }
                                else{
                                    return div_top + m[1] - m_height +"px"
                                }
                            })
                            .style('left', function(){
                                if(m[0] + m_width  > div_width){
                                    return (div_left + m[0] - m_width) + "px"
                                }
                                else{
                                    return div_left + m[0] - 2 * m_height_all + "px"
                                }
                            })
                            .style('width', m_width + "px")
                            .style('background-color', "white");

                        
                        let hover_toltip = add_div.append("svg")
                            .attr("class", "tree_node_hover_tooltip")
                            .attr("width", m_width)
                            .attr("height", m_height_all)
                            .append("g")
                            .attr("transform",`translate(${m_margin.left} , ${m_margin.top} )`);
                        
                        let x_Attrs = ["tone","impact","#mentions","#articles","#sources", "#ratio"]//"#nums"]
                        let dataset = []
                        dataset.push(+d.data.tree_vari_avgTone)
                        dataset.push(+d.data.tree_vari_gold)
                        dataset.push(+d.data.tree_vari_nummention)
                        dataset.push(+d.data.tree_vari_numarticle)
                        dataset.push(+d.data.tree_vari_numresouce)
                        dataset.push(+d.data.tree_vari_mSrcN)

                        // // Add X axis
                        var x = d3.scaleBand()
                            .domain(x_Attrs)
                            .range([0, m_innerWidth])
                            .padding(0.1);
                        
                        hover_toltip.append("g")
                            .attr("transform", "translate(0," + m_innerHeight + ")")
                            .call(d3.axisBottom(x).ticks(4))
                            .selectAll("text")
                            .attr("transform", "translate(-6,0)rotate(-30)")
                            .style("text-anchor", "end");
                        
                        // Y axis
                        var y = d3.scaleLinear()
                            .range([m_innerHeight, 0])
                            .domain(d3.extent(attrsMaxMin));
                        
                        hover_toltip.append("g")
                            .attr("class", "hover_toltip_axisYg")
                            .call(d3.axisLeft(y).ticks(3));
                        
                        hover_toltip.append("g").selectAll("rect")
                            .data(dataset)
                            .enter()
                            .append("rect")
                            .attr("class", "myRect")
                            .attr("fill", "steelblue")
                            .attr("opacity", 0.4)
                            .attr("x", function (d, i) {
                                return x(x_Attrs[i]);
                            })
                            .attr("y", function (d) {
                                return y(d);
                            })
                            .attr("width", x.bandwidth())
                            .attr("height", function (d) {
                                return m_innerHeight - y(d);
                            });   
                        hover_toltip.selectAll(".hover_toltip_axisYg").append('text')
                            .attr('class', 'variance_of_characteristics')
                            .attr('y', 3)
                            .attr('x', m_innerWidth)
                            .attr('fill', '#606266')
                            .attr('font-size', '1.3em')
                            .style('text-anchor', 'end')
                            .text("features variance");
                        
                        // compute this path node selection
                        const path__node = [];
                        const path = [];
                        do {
                            path__node.push(d);
                            path.push(d.data);
                        } while ((d = d.parent));

                        // console.log("path:", path);
                        self.gridData = []
                        
                        path.reverse();
                        path.forEach(ele=>{
                            if(ele.time_e != "time"){
                                let dic = new Array();
                                dic['date'] = ele.time_e;
                                dic['name'] = ele.tree_topickey.toString();
                                let medias = ele.tree_nodeSrcN;
                                for(let i=0;i<self.mediasources.length;i++){
                                    console.log(medias[i]);
                                    console.log(self.mediasources[i]);
                                    dic[self.mediasources[i].replaceAll(".","")] = medias[i];
                                }
                                self.gridData.push(dic);
                            }
                        })
                        self.ego_path = path;
                        self.ego_path__node = path__node;
                        node.classed("highlight", d => path.indexOf(d.data) > -1);
                        node.classed("leaf", d => path.indexOf(d.data) === 0);
                        link.classed("highlight", d => path.indexOf(d.target.data) > -1);

                    })
                    .on("mouseout", function () {
                        
                        d3.select("body").selectAll(".tree_node_hover_tooltip_div").remove();

                        d3.select("body").selectAll(".tree_node_detail_tooltip_div")
                            .classed("hover_tree_node_click_div_highlight", false);


                        node.classed("highlight", false);
                        node.classed("leaf", false);
                        link.classed("highlight", false);
                    })

            }


            let data = sysDatasetObj.storyTreeDataset;
            
            let rootnode = d3.hierarchy(data);
            let dx = innerHeight / (rootnode.children.length + 3);
            let dy = innerWidth / (rootnode.height + 3);
            let nodes = rootnode.descendants().filter(ele => ele.data.time_e);
            let timescope = nodes.map(ele => ele.data.time_e.replaceAll("-", "")).sort((a, b) => a - b)
                .map(ele=>ele=="time" ? "time" : ele.slice(0,4)+"-"+ele.slice(4,6)+"-"+ele.slice(6,8));
            self.tree_timescope = timescope;
            let delta_timescope = timescope.filter(ele=>ele != "time");
            let uni_delta_timescope = [...new Set(delta_timescope)];
            let delta_time = [];
            for(let i = 0; i < uni_delta_timescope.length - 1; i++){
                delta_time.push(
                    Date.parse(uni_delta_timescope[i + 1]) - Date.parse(uni_delta_timescope[i])
                );
            }
            
            let delta_timeScale = d3.scaleLinear().domain(d3.extent(delta_time)).range([1,4]);

            let reScale = d3.scaleBand().domain(timescope).range([0, innerWidth]);
            let biasMaxMin = nodes.filter(ele=> ele.data.totalbias != "null").map(ele=>+ele.data.totalbias);
            // console.log("biasMaxMin: ", biasMaxMin);

            let attrsMaxMin = []
            let tree_maxCompatibilityMaxMin = []
            nodes.filter(ele=> ele.data.totalbias != "null")
                .map(ele=>{
                    attrsMaxMin.push(+ele.data.tree_vari_avgTone)
                    attrsMaxMin.push(+ele.data.tree_vari_gold)
                    attrsMaxMin.push(+ele.data.tree_vari_nummention)
                    attrsMaxMin.push(+ele.data.tree_vari_numarticle)
                    attrsMaxMin.push(+ele.data.tree_vari_numresouce)
                    attrsMaxMin.push(+ele.data.tree_vari_mSrcN)
                    tree_maxCompatibilityMaxMin.push(+ele.data.tree_maxCompatibility)
                })

            // let lineWidthScale = d3.scaleLinear().domain([0, 0.5]).range([1, 10]);
            // let lineFillScale = d3.scaleLinear().domain([0, 0.5]).range([0.4, 1]);
            
            let lineWidthScale = d3.scaleLinear().domain(d3.extent(tree_maxCompatibilityMaxMin)).range([2, 5]);
            let lineFillScale = d3.scaleLinear().domain(d3.extent(tree_maxCompatibilityMaxMin)).range([0.4, 1]);

            let reScaleCircleRadia = d3.scaleLinear().domain(d3.extent(biasMaxMin)).range([5,10]);
            // console.log(timescope);
            // console.log(reScale("time"));
            let tree = data => {
                let i = 0;
                const root = d3.hierarchy(data).eachBefore(d=>{d.index = i++;});
                // root.dx = innerHeight / (root.children.length + 3);
                // root.dy = innerWidth / (root.height + 3);
                // return d3.tree().nodeSize([root.dx, root.dy])(root);
                // return d3.tree().size([innerHeight,innerWidth])(root);
                return d3.cluster().size([innerHeight,innerWidth])(root);
            }
            let root = tree(data);
            renderStoryTree(root, reScale, reScaleCircleRadia, delta_timeScale, attrsMaxMin, dx, dy, timescope);

        },
    }
}
</script>
  
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
.media-storytree-container {
    width: 100%;
    height: 100%;
}
</style>
<style>
</style>