
const aspectRatio = 16 / 9;

const margin = {top: 70, right:30, bottom: 40, left:80};
const width = 1200 - margin.left - margin.right;
const height = 500 - margin.top - margin.bottom;

const x = d3.scaleTime()
    .range([0,width])
const y = d3.scaleLinear()
    .range([height, 0])

const svg = d3.select("chart-container")
    .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
    .append("g")
        .attr("transform", "translate(${margin.left}, ${margin.top})");



function renderChart(data){

    

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


