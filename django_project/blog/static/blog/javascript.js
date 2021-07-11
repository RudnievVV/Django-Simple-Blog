// Functions to define url parameters
const url_params = window.location.search.slice(1)
    .split('&')
    .reduce(function _reduce(/*Object*/ a, /*String*/ b) {
        b = b.split('=');
        a[b[0]] = decodeURIComponent(b[1]);
        return a;
    }, {});
function encodeQueryData(data) {
    const ret = [];
    for (let d in data)
        ret.push(encodeURIComponent(d) + '=' + encodeURIComponent(data[d]));
    return ret.join('&');
}
function buildUrlAndGo(paramName, value) {
    url = location.host + location.pathname
    if (Object.keys(url_params)[0].length) {
        url_params[paramName] = value
        window.location.href = '//' + url + '?' + encodeQueryData(url_params)
    }
    else {
        window.location.href = '//' + url + `?${paramName}=` + value
    }
}


// Function for comments sort option dropdown change on post page
document.getElementById("comments-sorting").onchange = function (choice) {
    buildUrlAndGo('sort_option', choice.target.value)
}


// Fucntion for comments sort option button click on post page
const sortOrderBtn = document.getElementById("sort-order-btn")
sortOrderBtn.onclick = () => {
    buildUrlAndGo('sort_order', sortOrderBtn.value)
}

// Function for pagination page buttons with url parameters
function paginationBtn(value) {
    buildUrlAndGo('page', value)
}