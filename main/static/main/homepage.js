
const aspectRatio = 16 / 9;

let xScale, yScale, svg, chartGroup, xAxis, yAxis, harrisLine, trumpLine, kennedyLine;

function renderChart(data){
    var containerWidth = d3.select("#chart-container").node().getBoundingClientRect().width;
    var containerHeight = containerWidth / aspectRatio;

    var margin = {top : 20, right:30, bottom:40, left:50};

    var width = containerWidth - margin.left - margin.right;
    var height = containerHeight - margin.top - margin.bottom;


    if (!svg) {
        svg = d3.select("#chart-container").append("svg")
            .attr("id", "chart-svg")
            .attr("width", containerWidth)
            .attr("height", containerHeight);

        // Initialize chartGroup
        chartGroup = svg.append("g")
            .attr("transform", `translate(${margin.left}, ${margin.top})`);
    } else {
        svg.attr("width", containerWidth).attr("height", containerHeight);
    }
    
    xScale = d3.scaleTime().range([0,width]);
    yScale = d3.scaleLinear().range([height, 0]);

    xScale.domain(d3.extent(data, d => d.date));
    yScale.domain([0,d3.max(data, d => Math.max(d.harris_support, d.trump_support))]);

    xAxis = chartGroup.append("g")
        .attr("transform", "translate(0, ${height}")
        .call(d3.axisBottom(xScale).ticks(10));
    
    yAxis = chartGroup.append("g")
        .call(d3.axisLeft(yScale))
    
    harrisLine = d3.line()
        .x(d => xScale(d.date))
        .y(d=> yScale(d.harris_support))
    trumpLine = d3.line()
        .x(d => xScale(d.date))
        .y(d => yScale(d.trump_support))

    harrisPath = chartGroup.selectAll(".harris-line")
        .data([data]);
    trumpPath = chartGroup.selectAll(".trump-line")
        .data([data]);

    harrisPath.enter()
        .append("path")
        .attr("class", "harris-line")
        .attr("stroke", "blue")
        .attr("stroke-width", 2)
        .attr("d", harrisLine)
    
    trumpPath.enter()
        .datum(data)
        .attr("fill", "none")
        .attr("stroke", "red")
        .attr("stroke-width", 2)
        .attr("d", trumpLine)
        
        

}



d3.json("/api/polling-aggregate").then(function(data){ // data is an array, and all of the code below will execute for each data bit within the array. 
    console.log(data);

    var pollingData = data.map(d => ({ // originally we had objects, we then json serialized them inside of views.py to send them to the front end, now we are creating objects based on the json data.
        date: new Date(d.date),
        trump_support: d.trump_support,
        harris_support:d.harris_support,
        kennedy_support: d.kenney_support || null, // this null protects us in case we have a h2h poll. it has a default value of null here. 
        includes_third_party: d.includes_third_party
    }));

    h2hData = pollingData.filter(d => !d.includes_third_party);

    threeWayData = pollingData.filter(d => d.includes_third_party); // function(d) { return !d.includes_third_party;} this notation d => is basically doing this right here. it is taking each data member we have in our list 
    // polling data and filtering based on whether there is a thirdparty or not. 
    renderChart(h2hData);
})

window.addEventListener("resize", function(){
    var containerWidth = d3.select("#chart-container").node().getBoundingClientRect().width;
    var containerHeight = containerWidth / aspectRatio;

        // Update SVG dimensions
    svg.attr("width", containerWidth).attr("height", containerHeight);

        // Update scales with new dimensions
    var margin = { top: 20, right: 30, bottom: 40, left: 50 };
    var width = containerWidth - margin.left - margin.right;
    var height = containerHeight - margin.top - margin.bottom;

    xScale.range([0, width]);
    yScale.range([height, 0]);

        // Update axes
    xAxis.call(d3.axisBottom(xScale).ticks(5));
    yAxis.call(d3.axisLeft(yScale));

        // Update the line paths
    chartGroup.select("path:nth-of-type(1)")
        .attr("d", harrisLine);

    chartGroup.select("path:nth-of-type(2)")
        .attr("d", trumpLine);

})

