// you receive an array of objects which you must sort in the by the key "sortField" in the "sortDirection"
function getSortedItems(items, sortField, sortDirection) {
    console.log(items)
    console.log(sortField)
    console.log(sortDirection)

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    items.sort((item1, item2)=> {
        if (item1[sortField] > item2[sortField]) {
            if (sortDirection === "asc") {
                return 1

            }else {
                return -1
            }
        }else {
            if (sortDirection === "asc") {
                return -1
            }else {
                return 1
            }
        }
    })
    return items
}

// you receive an array of objects which you must filter by all it's keys to have a value matching "filterValue"
function getFilteredItems(items, filterValue) {
    //console.log(items)
    //console.log(filterValue)

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //

    let filteredItems = []

    switch (filterValue.includes(':')) {
        case true:
            for (let i = 0; i < items.length; i++) {
                if (filterValue[0] == "D" && items[i]['Description'].includes(filterValue.slice(filterValue.indexOf(':') + 1))) {
                    filteredItems.push(items[i])
                } else if (filterValue[0] == "!" && !items[i]['Description'].includes(filterValue.slice(filterValue.indexOf(':') + 1))) {
                    filteredItems.push(items[i])
                }
            }
            break;

        case false:
            for (let i = 0; i < items.length; i++) {
                if (filterValue[0] == "!" && !items[i]['Title'].includes(filterValue.slice(1, filterValue.length))) {
                    filteredItems.push(items[i]);
                } else if (items[i]['Title'].includes(filterValue)) {
                    filteredItems.push(items[i]);
                }

            }
            break;
    }


    return filteredItems
}

function toggleTheme() {
    console.log("toggle theme")
}

function increaseFont() {
    console.log("increaseFont")
}

function decreaseFont() {
    console.log("decreaseFont")
}