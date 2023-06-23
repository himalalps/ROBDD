from enum import Enum
import os


class nodeType(Enum):
    boolean = 0
    variable = 1
    operator = 2


class Node:
    def __init__(self, label: str, type: nodeType, false, true):
        self.label = label
        self.type = type
        self.false = false
        self.true = true

    def __eq__(self, other):
        return (
            self.label == other.label
            and self.type == other.type
            and self.false == other.false
            and self.true == other.true
        )

    def output(self):
        """output the node in an html page"""
        html = """
<!DOCTYPE html>
<meta charset="utf-8">
<style>.link {  fill: none;  stroke: #666;  stroke-width: 1.5px;}#licensing {  fill: green;}.link.licensing {  stroke: green;}.link.resolved {  stroke-dasharray: 0,2 1;}circle {  fill: #ccc;  stroke: #333;  stroke-width: 1.5px;}text {  font: 12px Microsoft YaHei;  pointer-events: none;  text-shadow: 0 1px 0 #fff, 1px 0 0 #fff, 0 -1px 0 #fff, -1px 0 0 #fff;}.linetext {    font-size: 12px Microsoft YaHei;}</style>
<body>
<input type="file" id="files" style="display: none" />
<script src="d3.v3.min.js"></script>
<script>
        """
        html += "\nvar links = [" + self.getLinks() + "];"
        html += """
var nodes = {};
links.forEach(function(link)
{
  link.source = nodes[link.source] || (nodes[link.source] = {name: link.source});
  link.target = nodes[link.target] || (nodes[link.target] = {name: link.target});
});
var width = 1920, height = 1080;
var force = d3.layout.force()
    .nodes(d3.values(nodes))
    .links(links)
    .size([width, height])
    .linkDistance(180)
    .charge(-1500)
    .on("tick", tick)
    .start();
var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);
var marker=
    svg.append("marker")
    .attr("id", "resolved")
    .attr("markerUnits","userSpaceOnUse")
    .attr("viewBox", "0 -5 10 10")
    .attr("refX",32)
    .attr("refY", -1)
    .attr("markerWidth", 12)
    .attr("markerHeight", 12)
    .attr("orient", "auto")
    .attr("stroke-width",2)
    .append("path")
    .attr("d", "M0,-5L10,0L0,5")
    .attr('fill','#000000');
var edges_line = svg.selectAll(".edgepath")
    .data(force.links())
    .enter()
    .append("path")
    .attr({
          'd': function(d) {return 'M '+d.source.x+' '+d.source.y+' L '+ d.target.x +' '+d.target.y},
          'class':'edgepath',
          'id':function(d,i) {return 'edgepath'+i;}})
    .style("stroke",function(d){
         var lineColor;
		 lineColor="#B43232";
         return lineColor;
     })
    .style("pointer-events", "none")
    .style("stroke-width",0.5)
    .attr("marker-end", "url(#resolved)" )
    .attr("stroke-dasharray", function(d) {
         if (d.type == "resolved") {
             return "5,0";
         } else {
             return "5,5";
         }
    });
var edges_text = svg.append("g").selectAll(".edgelabel")
.data(force.links())
.enter()
.append("text")
.style("pointer-events", "none")
.attr({  'class':'edgelabel',
               'id':function(d,i){return 'edgepath'+i;},
               'dx':80,
               'dy':0
               });
edges_text.append('textPath')
.attr('xlink:href',function(d,i) {return '#edgepath'+i})
.style("pointer-events", "none")
.text(function(d){return d.rela;});
var circle = svg.append("g").selectAll("circle")
    .data(force.nodes())
    .enter().append("circle")
    .style("fill",function(node){
        var color;
        var link=links[node.index];
		color="#F9EBF9";
        return color;
    })
    .style('stroke',function(node){ 
        var color;
        var link=links[node.index];
		color="#A254A2";
        return color;
    })
    .attr("r", 28)
    .on("click",function(node)
	{
        edges_line.style("stroke-width",function(line){
            console.log(line);
            if(line.source.name==node.name || line.target.name==node.name){
                return 4;
            }else{
                return 0.5;
            }
        });
    })
    .call(force.drag);
var text = svg.append("g").selectAll("text")
    .data(force.nodes())
    .enter()
    .append("text")
    .attr("dy", ".35em")  
    .attr("text-anchor", "middle")
    .style('fill',function(node){
        var color;
        var link=links[node.index];
		color="#A254A2";
        return color;
    }).attr('x',function(d){
        var re_en = /[a-zA-Z]+/g;
        if(d.name.match(re_en)){
             d3.select(this).append('tspan')
             .attr('x',0)
             .attr('y',2)
             .text(function(){return d.name;});
        }
        
        else if(d.name.length<=4){
             d3.select(this).append('tspan')
            .attr('x',0)
            .attr('y',2)
            .text(function(){return d.name;});
        }else{
            var top=d.name.substring(0,4);
            var bot=d.name.substring(4,d.name.length);
            d3.select(this).text(function(){return '';});
            d3.select(this).append('tspan')
                .attr('x',0)
                .attr('y',-7)
                .text(function(){return top;});
            d3.select(this).append('tspan')
                .attr('x',0)
                .attr('y',10)
                .text(function(){return bot;});
        }
    });
function tick() {
  circle.attr("transform", transform1);
  text.attr("transform", transform2);
  edges_line.attr('d', function(d) { 
      var path='M '+d.source.x+' '+d.source.y+' L '+ d.target.x +' '+d.target.y;
      return path;
  });  
    
  edges_text.attr('transform',function(d,i){
        if (d.target.x<d.source.x){
            bbox = this.getBBox();
            rx = bbox.x+bbox.width/2;
            ry = bbox.y+bbox.height/2;
            return 'rotate(180 '+rx+' '+ry+')';
        }
        else {
            return 'rotate(0)';
        }
   });
}
function linkArc(d) {
  return 'M '+d.source.x+' '+d.source.y+' L '+ d.target.x +' '+d.target.y
}
function transform1(d) {
  return "translate(" + d.x + "," + d.y + ")";
}
function transform2(d) {
      return "translate(" + (d.x) + "," + d.y + ")";
}

var drag = force.drag()
    .on("dragstart", dragstart);

function dragstart(d) {
  d3.select(this).classed("fixed", d.fixed = true);
}

</script>
        """
        cwd = os.path.dirname(__file__)
        open(os.path.join(cwd, "graph.html"), "w").write(html)

    def getLinks(self):
        """get the links of the graph"""
        if self.type == nodeType.boolean:
            return ""
        else:
            return (
                f"{{source: '{self.label}', target: '{self.false.label}', 'rela': '0', type: 'dashed'}},\n {{source: '{self.label}', target: '{self.true.label}', 'rela': '1', type: 'resolved'}},\n"
                + self.false.getLinks()
                + self.true.getLinks()
            )


def parser(s: str):
    """parse a string into a logical tree"""
    raise NotImplementedError


FalseNode = Node("False", nodeType.boolean, None, None)
TrueNode = Node("True", nodeType.boolean, None, None)
node = Node("a", nodeType.variable, FalseNode, TrueNode)
node.output()
