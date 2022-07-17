function onDOMLoaded(){

    timeLoop();

    addEventListeners();

    render(window.location.hash);

    sessionStorage.clear();

}


function addEventListeners(){

    //handler for SPA navigation
    window.onhashchange = function(){
        // render function is called every hash change.
        render(window.location.hash);
    };

}

function render(hasKey){

    let pages = document.querySelectorAll(".page");
    for (let i=0; i<pages.length; i++){
        pages[i].style.display = 'none';
    }

    let navList = document.querySelectorAll(".nav-item");
    for (let i=0; i<navList.length; i++){
        navList[i].classList.remove("active")
    }

    switch (hasKey) {
        case "":
            pages[0].style.display = 'block';
            document.getElementById("li_home").classList.add("active");
            break;
        case "#home":
            pages[0].style.display = 'block';
            document.getElementById("li_home").classList.add("active");
            break;
        //case "#management":
        //    pages[1].style.display = 'block';
        //    document.getElementById("li_management").classList.add("active");
        //    break;
        case "#trading":
            pages[1].style.display = 'block';
            document.getElementById("li_trading").classList.add("active");
            break;
        case "#psei_live":
            pages[2].style.display = 'block';
            document.getElementById("li_psei_live").classList.add("active");
            break;
        //case "#operational":
        //    pages[2].style.display = 'block';
        //    document.getElementById("li_operational").classList.add("active");
        //    break;
        //case "#project":
        //    pages[3].style.display = 'block';
        //    document.getElementById("li_project").classList.add("active");
        //    break;
        case "#harqis_metrics":
            pages[3].style.display = 'block';
            document.getElementById("li_harqis_metrics").classList.add("active");
            break;
        case "#habits":
            pages[4].style.display = 'block';
            document.getElementById("li_habits").classList.add("active");
            break;
        default:
            pages[0].style.display = 'block';
            document.getElementById("li_home").classList.add("active");
            break;

    }
}

function timeLoop(){
    let timeSpan = document.getElementById('time');

    setInterval(function(){
        timeSpan.innerHTML = formatTime();
    }, 1000);
}

function formatTime() {
    var d = new Date(),
        minutes = d.getMinutes().toString().length == 1 ? '0'+d.getMinutes() : d.getMinutes(),
        hours = d.getHours().toString().length == 1 ? '0'+d.getHours() : d.getHours(),
        months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
        days = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'],
        seconds = d.getSeconds().toString().length == 1 ? '0'+d.getSeconds() : d.getSeconds();

    return months[d.getMonth()]+' '+d.getDate()+' '+d.getFullYear()+' '+hours+':'+minutes+':'+seconds;
}