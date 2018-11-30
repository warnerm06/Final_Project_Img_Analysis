// create variable from HTML {{azureResults}} variable
var tableData = azureResults
console.log("Step1");

//Function to build a table from our API data//
function azureTable(data) {
    console.log("Step2")

    console.log(data)
    console.log(typeof(data))
    var tbody = d3.select("tbody");

    Object.entries(data).forEach(
        ([key, value]) => console.log(key, value)
        );
        
    // //Breaks here.... with a data.foreach is not a function......
    // data.forEach((data) => {
    //     console.log("Step3");
    //     var row = tbody.append("tr");
    //     Object.entries(data).forEach(([key, value]) => {
    //         var cell = tbody.append("td").text(value);
    //     });
    // });
};

//When our submit button is clicked call the build table function//
document.getElementById("buttonID").onclick = azureTable(tableData);


