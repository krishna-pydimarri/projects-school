function getJsonObject(path, success, error) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                if (success) success(JSON.parse(xhr.responseText));
            } else {
                if (error) error(xhr);
            }
        }
    };
    xhr.open("GET", path, true);
    xhr.send();
}

function createHtmlTable(arrayVal) {
    var old_tbody = document.getElementById("titlesTbl").getElementsByTagName('tbody')[1];
    var new_tbody = document.createElement('tbody');
    arrayVal.forEach(function(rowData) {
        var row = new_tbody.insertRow();
        console.log(rowData['img']);
        console.log('$'+rowData['price']);
        var authorCell = document.createElement('td');
        authorCell.appendChild(document.createTextNode(rowData['authors']));
        var yearCell = document.createElement('td');
        yearCell.appendChild(document.createTextNode(rowData['year']));
        var priceCell = document.createElement('td');
        priceCell.appendChild(document.createTextNode('$'+rowData['price']));
        var publisherCell = document.createElement('td')
        publisherCell.appendChild(document.createTextNode(rowData['publisher']));
        var categoryCell =document.createElement('td')
        categoryCell.appendChild(document.createTextNode(rowData['category']));
        categoryCell.classList.add("bookCategory");
        var titleCell = document.createElement('td');
        titleCell.appendChild(document.createTextNode(rowData['title']));
        titleCell.classList.add("titleItalic");
        var checkbox = document.createElement('input');
        checkbox.type = "checkbox"; 
        checkbox.name = "titleSelected"; 
        checkbox.value = rowData['title'];
        checkbox.classList.add("titleCheckBox"); 
        var checkboxCell=document.createElement('td');
        checkboxCell.appendChild(checkbox);
        var titleIconCellMain = document.createElement('td');
        var titleIconCell = document.createElement('img');
        titleIconCell.classList.add("smallImg");
        titleIconCell.src=rowData['img'];
        titleIconCellMain.appendChild(titleIconCell);
        var blankStarCell = document.createElement('img');
        blankStarCell.classList.add("starIcon");
        blankStarCell.src='images/outline-star-16.ico';
        var filledStarCell = document.createElement('img');
        filledStarCell.classList.add("starIcon");
        filledStarCell.src='images/star-16.ico';
        var ratingImageCell = document.createElement('td');
        var ratingRowDiv=document.createElement('div');
        ratingRowDiv.classList.add("ratingRow");
        for (i=1;i<=5;i++){
            if (i<=rowData['rating']){
                x=filledStarCell.cloneNode(true);
                ratingRowDiv.appendChild(x);
                console.log(x);
            }
            else {
                y=blankStarCell.cloneNode(true);
                ratingRowDiv.appendChild(y);
                console.log(blankStarCell);
            }
        }
        ratingImageCell.appendChild(ratingRowDiv);
        //console.log(ratingImageCell);
        var cellsArr = [checkboxCell,titleIconCellMain,titleCell,ratingImageCell,authorCell,yearCell,priceCell,publisherCell,categoryCell];
        cellsArr.forEach(function(cellData){row.appendChild(cellData)});
    });
    old_tbody.parentNode.replaceChild(new_tbody, old_tbody)
}

function createOtherElements(arrayVal) {
    var divRow = document.getElementById("searchBox");
    var filter = document.getElementById("filterCategory");
    var allCategories= new Array();
    for (i=0;i<arrayVal.length;i++){
        //console.log(allCategories.indexOf(arrayVal[i]['category']));
        if (allCategories.indexOf(arrayVal[i]['category'])==-1){
        var option = document.createElement("option");
        option.text = arrayVal[i]['category'];
        allCategories.push(arrayVal[i]['category']);
        filter.add(option);
        }
    }
    //console.log(allCategories);
}

function highlightOnSearch() {
    var searchText=document.getElementById("searchTtl");
    var table = document.getElementById("titlesTbl");
    searchKey = searchText.value.toUpperCase();
    tr = table.getElementsByTagName("tr");
    //table.style.backgroundColor = "#FAFCFF";
    var totalSearchResults=0;
    var existingColor="";
    var darkModeCheck=document.getElementById("darkMode");
    console.log(darkModeCheck.checked);
    if (darkModeCheck.checked==true){
        existingColor="#494E52";
        existingTextColor = "FloralWhite";
    }
    else{
        existingColor="#FAFCFF";
        existingTextColor ="black";
    }
    for (i=1;i<tr.length;i++){
        titleTd = tr[i].getElementsByClassName("titleItalic");
        //console.log(titleTd);
        var txtVal=titleTd[0].textContent;
        console.log(txtVal);
        if (txtVal.toUpperCase().indexOf(searchKey)!=-1 & searchKey!='') {
            console.log("Highlighting");
                tr[i].style.backgroundColor = "#DAF7A6";
                tr[i].style.color = "black";
                totalSearchResults++;
        }
        else 
        {   console.log("removing highlight");
            tr[i].style.backgroundColor = existingColor;
            tr[i].style.color = existingTextColor;
        }

    }
    let searchWarn= document.getElementById("searchWarn");
    if (totalSearchResults==0 & searchKey!=''){
        //alert("No titles found for the searched term!");
        searchWarn.innerHTML="<p id='searchWarn'> *No searched titles found!</p>";
    }
    else{
        searchWarn.innerHTML="<p id='searchWarn'></p>";
    }
}

function filterCategory(bookList){
    createHtmlTable(bookList);
    var category=document.getElementById("filterCategory");
    var table = document.getElementById("titlesTbl");
    filterKey = category.value;
    tr = table.getElementsByTagName("tr");
    for (i=1;i<tr.length;i++){
        console.log(i);
        console.log(tr.length);
        categoryTd = tr[i].getElementsByClassName("bookCategory");
        var categVal=categoryTd[0].textContent;
        console.log(categVal);
        console.log(this.filterKey);
        if (categVal!=this.filterKey & filterKey != "Category") {
            console.log("removing record");
            table.deleteRow(i);
            i=i-1;
        }
        else 
        {   
            console.log("Keeping record");
        }
    }
}

window.onload = function(e){
    
    bookList = []; // book list container
    getJsonObject('data.json',
        function(data) {
            bookList = data; // store the book list into bookList
            createHtmlTable(bookList);
            createOtherElements(bookList);
            var totalItems=0;
            var searchClick=document.getElementById("search_button");
            searchClick.addEventListener("click", function(event) {
                highlightOnSearch();
                //filterCategory(bookList);
                event.preventDefault();
            });
            var filterClick=document.getElementById("filter_button");
            filterClick.addEventListener("click", function(event) {
                filterCategory(bookList);
           //     highlightOnSearch();
                event.preventDefault();
            });
            var addClick=document.getElementById("add_button");
            addClick.addEventListener("click", function(event) {
                var checkTitles= document.getElementsByClassName("titleCheckBox");
                let totalItemsSelected=0;
                for(i=0;i<checkTitles.length;i++){
                    if (checkTitles[i].checked==true){
                        let promptText = "Please enter quantity for title:\n" + checkTitles[i].value;
                        var getQuantity= parseInt(prompt(promptText, 1));
                        if(getQuantity>0){
                        totalItems=totalItems+getQuantity;
                        var numItems= document.getElementById("numItems");
                        numItems.innerHTML=`<p id='numItems'>(${totalItems})</p>`;
                        }
                        totalItemsSelected++;
                    }
                    checkTitles[i].checked=false;
                }
                if(totalItemsSelected==0){
                    alert('No titles selected to add to cart!');

                }
                console.log(totalItemsSelected);
                event.preventDefault();
            });
            var resetClick=document.getElementById("reset_button");
            resetClick.addEventListener("click", function(event) {
              if (confirm("Are you sure? Press Ok to reset else press Cancel")) {
                var itemsReset= document.getElementById("numItems");
                itemsReset.innerHTML="<p id='numItems'>(0)</p>";
                totalItems=0;
              }
              event.preventDefault();
            });
            var darkMode=document.getElementById("darkMode");
            darkMode.addEventListener("click", function(event) {
                if(darkMode.checked){
                    document.body.classList.add("darkModeOn");
                    var searchBoxClass=document.getElementById("searchBox");
                    searchBoxClass.classList.add("darkModeOn");
                    var listBoxClass=document.getElementById("listBox");
                    listBoxClass.classList.add("darkModeOn");
                    highlightOnSearch();
                }
                else {
                    document.body.classList.remove("darkModeOn");
                    var searchBoxClass=document.getElementById("searchBox");
                    searchBoxClass.classList.remove("darkModeOn");
                    var listBoxClass=document.getElementById("listBox");
                    listBoxClass.classList.remove("darkModeOn");
                    highlightOnSearch();
                }
               // event.preventDefault();
            });
        },
        function(xhr) { console.error(xhr); }
    );
}