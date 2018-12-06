// create variable from HTML {{info}} variable
var tableData = info

//When our submit button is clicked call the build table function//
var str = JSON.stringify(tableData, undefined, 4);

function output(inp) {
    // document.body.appendChild(document.createElement('pre')).innerHTML = inp;
    document.getElementById("azurePtag").innerHTML = inp;
}

// function to add color to our JSON object
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
// call our function
output(syntaxHighlight(str)); 
