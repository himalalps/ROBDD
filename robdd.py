from enum import Enum
import os
import re


class nodeType(Enum):
    boolean = 0
    variable = 1
    operator = 2


cnt = 0


class Node:
    def __init__(self, label: str, type: nodeType, false, true):
        self.label = label
        self.type = type
        self.false = false
        self.true = true
        global cnt
        self.id = cnt
        cnt += 1

    def __eq__(self, other):
        return (
            self.label == other.label
            and self.type == other.type
            and self.false == other.false
            and self.true == other.true
        )

    def __repr__(self, indent=4):
        if self.type == nodeType.boolean:
            if self.label == "True":
                return "TrueNode"
            else:
                return "FalseNode"
        return f'Node(\n{" " * indent}"{self.label}",\n{" " * indent}{self.type},\n{" " * indent}{self.false.__repr__(indent + 4)},\n{" " * indent}{self.true.__repr__(indent + 4)}\n{" " * (indent - 4)})'

    def __hash__(self) -> int:
        return hash(self.__repr__())

    def output(self):
        """output the Node in an html page"""
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
  link.source = nodes[link.sourceid] || (nodes[link.sourceid] = {name: link.source, id: link.sourceid});
  link.target = nodes[link.targetid] || (nodes[link.targetid] = {name: link.target, id: link.targetid});
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
            if(line.source.id==node.id || line.target.id==node.id){
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
                f'{{source: "{self.label}", sourceid: {self.id}, target: "{self.false.label}", targetid: {self.false.id}, "rela": "0", type: "dashed"}},\n {{source: "{self.label}", sourceid: {self.id}, target: "{self.true.label}", targetid: {self.true.id}, "rela": "1", type: "resolved"}},\n'
                + self.false.getLinks()
                + self.true.getLinks()
            )


FalseNode = Node("False", nodeType.boolean, None, None)
TrueNode = Node("True", nodeType.boolean, None, None)


def parser(s: str):
    """parse a string into a Node
    >>> parser("T")
    TrueNode
    >>> parser("F")
    FalseNode
    >>> parser("abc")
    Node(
        "abc",
        nodeType.variable,
        FalseNode,
        TrueNode
    )
    >>> parser("~a")
    Node(
        "->",
        nodeType.operator,
        Node(
            "a",
            nodeType.variable,
            FalseNode,
            TrueNode
        ),
        FalseNode
    )
    >>> parser("(p->r)&(q<->(r|p))")
    Node(
        "&",
        nodeType.operator,
        Node(
            "->",
            nodeType.operator,
            Node(
                "p",
                nodeType.variable,
                FalseNode,
                TrueNode
            ),
            Node(
                "r",
                nodeType.variable,
                FalseNode,
                TrueNode
            )
        ),
        Node(
            "<->",
            nodeType.operator,
            Node(
                "q",
                nodeType.variable,
                FalseNode,
                TrueNode
            ),
            Node(
                "|",
                nodeType.operator,
                Node(
                    "r",
                    nodeType.variable,
                    FalseNode,
                    TrueNode
                ),
                Node(
                    "p",
                    nodeType.variable,
                    FalseNode,
                    TrueNode
                )
            )
        )
    )
    """
    s = s.replace(" ", "")
    if len(s) == 0:
        return None
    if s == "T":
        return TrueNode
    elif s == "F":
        return FalseNode
    elif s[0] == "~":
        return Node("->", nodeType.operator, parser(s[1:]), FalseNode)
    elif s[0] == "(":
        i = 1
        # balance the parentheses
        for j in range(1, len(s)):
            if s[j] == "(":
                i += 1
            elif s[j] == ")":
                i -= 1
            if i == 0:
                break
        if j == len(s) - 1 and s[j] == ")":
            return parser(s[1:-1])
        elif j == len(s) - 1:
            raise SyntaxError("Invalid input")
        else:
            left = parser(s[1:j])
            if s[j + 1] == "&" or s[j + 1] == "|":
                return Node(s[j + 1], nodeType.operator, left, parser(s[j + 2 :]))
            elif s[j + 1 : j + 3] == "->":
                return Node("->", nodeType.operator, left, parser(s[j + 3 :]))
            elif s[j + 1 : j + 4] == "<->":
                return Node("<->", nodeType.operator, left, parser(s[j + 4 :]))
            else:
                raise SyntaxError("Invalid input")
    else:
        iter = re.finditer(r"(&|\||->|<->)", s)
        try:
            op = next(iter)
        except StopIteration:
            return Node(s, nodeType.variable, FalseNode, TrueNode)
        op = op.span()
        return Node(
            s[op[0] : op[1]],
            nodeType.operator,
            parser(s[: op[0]]),
            parser(s[op[1] :]),
        )


def apply(n: Node):
    """apply the rules to the Node"""
    if n.type == nodeType.boolean:
        return n
    elif n.type == nodeType.operator:
        if n.true.type == nodeType.operator:
            n.true = apply(n.true)
        if n.false.type == nodeType.operator:
            n.false = apply(n.false)
        label = n.label
        if n.true.type == nodeType.boolean and n.false.type == nodeType.boolean:
            # return according to the truth table
            if label == "&":
                if n.false == TrueNode and n.true == TrueNode:
                    return TrueNode
                else:
                    return FalseNode
            elif label == "|":
                if n.false == FalseNode and n.true == FalseNode:
                    return FalseNode
                else:
                    return TrueNode
            elif label == "->":
                if n.false == TrueNode and n.true == FalseNode:
                    return FalseNode
                else:
                    return TrueNode
            elif label == "<->":
                if n.false == n.true:
                    return TrueNode
                else:
                    return FalseNode
            else:
                raise SyntaxError("Invalid input")

        if n.true.type == nodeType.boolean or (
            n.false.type != nodeType.boolean and n.false.label < n.true.label
        ):
            falseNode = apply(Node(label, nodeType.operator, n.false.false, n.true))
            trueNode = apply(Node(label, nodeType.operator, n.false.true, n.true))
            if falseNode == trueNode:
                return falseNode
            return Node(n.false.label, nodeType.variable, falseNode, trueNode)
        elif n.false.type == nodeType.boolean or n.false.label > n.true.label:
            falseNode = apply(Node(label, nodeType.operator, n.false, n.true.false))
            trueNode = apply(Node(label, nodeType.operator, n.false, n.true.true))
            if falseNode == trueNode:
                return falseNode
            return Node(n.true.label, nodeType.variable, falseNode, trueNode)
        else:
            falseNode = apply(
                Node(label, nodeType.operator, n.false.false, n.true.false)
            )
            trueNode = apply(Node(label, nodeType.operator, n.false.true, n.true.true))
            if falseNode == trueNode:
                return falseNode
            return Node(n.true.label, nodeType.variable, falseNode, trueNode)


def returnSet(n: Node):
    """return the set of variables in the Node"""
    if n.type == nodeType.operator:
        raise SyntaxError("Invalid input")
    elif n.type == nodeType.boolean:
        return set()
    else:
        return {n} | returnSet(n.true) | returnSet(n.false)


def reduce(n: Node, s: set):
    """reduce the Node to a simpler form according to set"""
    if n.type == nodeType.boolean:
        return n
    if n.true.type != nodeType.boolean and n.true in s:
        n.true = list(s)[list(s).index(n.true)]
    if n.false.type != nodeType.boolean and n.false in s:
        n.false = list(s)[list(s).index(n.false)]
    n.true = reduce(n.true, s)
    n.false = reduce(n.false, s)
    return n


def eval(s: str):
    """apply elimination on the Node"""
    n = apply(parser(s.replace('"', '\\"')))
    s = returnSet(n)
    return reduce(n, s)


if __name__ == "__main__":
    # eval('(p1"->r1)&(q1<->(r1|p1"))').output()
    eval(
    "((~a1)&(~a2)&(~a1')&(~a2'))|((~a1)&(~a2)&(~a1')&a2')|((~a1)&(~a2)&a1'&(~a2'))|((~a1)&a2&a1'&a2')|(a1&(~a2)&(~a1')&a2')|(a1&(~a2)&a1'&a2')|(a1&a2&(~a1')&(~a2'))"
    ).output()
