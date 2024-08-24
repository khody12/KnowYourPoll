
function renderChart(data){

    const margin = {top: 70, right:30, bottom: 40, left:80};
    const width = 1200 - margin.left - margin.right;
    const height = 500 - margin.top - margin.bottom;

    const x = d3.scaleTime()
        .range([0,width])
    const y = d3.scaleLinear()
        .range([height, 0])

    const svg = d3.select("#chart-container")
        .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
        .append("g")
            .attr("transform", `translate(${margin.left}, ${margin.top})`);

    const tooltip = d3.select("body")
        .append("div")
        .attr("class", "tooltip");
    
    const tooltipTwo = d3.select("body")
        .append("div")
        .attr("class", "tooltipTwo");
    const tooltipThree = d3.select("body")
        .append("div")
        .attr("class", "tooltipThree")


    // defining our domains
    x.domain(d3.extent(data, d=> d.date));
    y.domain([0, 60]);

    //adding the x axis here

    svg.append("g")
        .attr("transform", `translate(0, ${height})`)
        .call(d3.axisBottom(x)
            .ticks(d3.timeDay.every(3))
            .tickFormat(d3.timeFormat("%b %d")));
    //adding the y axis here

    svg.append("g")
        .call(d3.axisLeft(y))
    
    const harrisLine = d3.line()
        .x(d => x(d.date))
        .y(d => y(d.harris_support))
        .curve(d3.curveBumpX);
    
    svg.append("path")
        .datum(data)
        .attr("fill", "none")
        .attr("stroke", "blue")
        .attr("stroke-width", 2)
        .attr("d", harrisLine);
    
    const trumpLine = d3.line()
        .x(d => x(d.date))
        .y(d => y(d.trump_support))
        .curve(d3.curveBumpX);
    
    svg.append("path")
        .datum(data)
        .attr("fill", "none")
        .attr("stroke", "red")
        .attr("stroke-width", 2)
        .attr("d", trumpLine);
    
    const verticalLine = svg.append("line")
        .attr("y1", 0)
        .attr("y2", height)
        .attr("fill", "lightblue")
        .style("stroke", "dash")
        .style("stroke","black")
        .attr("stroke-width", 2)
        .attr("opacity", 0.70)
        .style("pointer-events", "none")
        .style("stroke-dasharray", 3.5);

    const listeningRect = svg.append("rect")
        .attr("width", width)
        .attr("height", height);

    listeningRect.on("mousemove", function(event){
        const [xCoord] = d3.pointer(event, this);
        const bisectDate = d3.bisector(d => d.date).left;
        const x0 = x.invert(xCoord);
        const i = bisectDate(data, x0, 1);
        const d0 = data[i-1];
        const d1 = data[i];
        const d = x0 - d0.date > d1.date - x0 ? d1 : d0;
        const xPos = x(d.date);
        const yPos = y(d.harris_support);

        verticalLine.attr("x1", xPos)
            .attr("x1", xPos)
            .attr("x2", xPos);

        tooltip
            .style("display", "block")
            .style("left", `${xPos + 200}px`)
            .style("top", `${yPos + 10}px`)
            .html(`<br><strong>Harris:</strong> ${d.harris_support} `);
        
        tooltipTwo
            .style("display", "block")
            .style("left", `${xPos + 200}px`)
            .style("top", `${yPos + 60}px`)
            .html(`  <br><strong>Trump:</strong> ${d.trump_support}`);
        tooltipThree
            .style("display", "block")
            .style("top", `${yPos}px`)
            .style("left", `${xPos + 120}px`)
            .html(`${d.date.toLocaleDateString()}`)


    });
    
    

    

}



d3.json("/api/polling-aggregate").then(function(data){ // data is an array, and all of the code below will execute for each data bit within the array. 
    

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


