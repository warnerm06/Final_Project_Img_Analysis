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
        
//     // //Breaks here.... with a data.foreach is not a function......
//     // data.forEach((data) => {
//     //     console.log("Step3");
//     //     var row = tbody.append("tr");
//     //     Object.entries(data).forEach(([key, value]) => {
    //     //         var cell = tbody.append("td").text(value);
    //     //     });
    //     // });
};

//When our submit button is clicked call the build table function//
var str = JSON.stringify(tableData, undefined, 4);

document.getElementById("buttonID").onclick = output(syntaxHighlight(str));
//network time? //

function output(inp) {
    console.log("onclick",str)
    document.body.appendChild(document.createElement('pre')).innerHTML = inp;
}

function syntaxHighlight(json) {
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
        var cls = 'number';
        if (/^"/.test(match)) {
            if (/:$/.test(match)) {
                cls = 'key';
            } else {
                cls = 'string';
            }
        } else if (/true|false/.test(match)) {
            cls = 'boolean';
        } else if (/null/.test(match)) {
            cls = 'null';
        }
        return '<span class="' + cls + '">' + match + '</span>';
    });
}

// setTimeout(() => {
    //     var str = JSON.stringify(tableData, undefined, 4);
    // }, 2000);
// }, 2000);

// output(str);

