// create variable from HTML {{azureResults}} variable

var tableData = azureResults

//Function to build a table from our API data//
// function azureTable(data) {
// };

//When our submit button is clicked call the build table function//
var str = JSON.stringify(tableData, undefined, 4);


document.getElementById("buttonID").onclick =output(syntaxHighlight(str)); 

// document.getElementById("buttonID").onclick =toTable();

    
 

// toTable();
//network time? //

function output(inp) {
    console.log("onclick",str)
    // document.body.appendChild(document.createElement('pre')).innerHTML = inp;
    document.getElementById("azurePtag").innerHTML = inp;

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

// test----------------------------------------------------------------------
// var obj = [{
//     "key": "apple",
//     "value": 1.90
// }, {
//     "key": "berry",
//     "value": 1.7
// }, {
//     "key": "banana",
//     "value": 1.5
// }, {
//     "key": "cherry",
//     "value": 1.2
// }];

// var tbody = document.getElementById('tbody');
// var tList= [tableData]
// function toTable() {
//     console.log("TableFunction")
//     // console.log("azure",azureResults)
//     console.log([tableData])
//     console.log([tableData].length)
//     for (var i = 0; i < tList.length; i++) {
//         var tr = "<tr>";

//         /* Verification to add the last decimal 0 */
//         if (tList[i].value.toString().substring(tList[i].value.toString().indexOf('.'), tList[i].value.toString().length) < 2) 
//             tList[i].value += "0";

//         /* Must not forget the $ sign */
//         tr += "<td>" + tList[i].key + "</td>" + "<td>$" + tList[i].value.toString() + "</td></tr>";

//         /* We add the table row to the table body */
//         tbody.innerHTML += tr;
//         console.log("Here")
//     };
// }