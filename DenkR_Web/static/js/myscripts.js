////Home

//Class Toggle

function toggleClass(like_btn) {
    if (like_btn.classList.contains("liked")) {
        like_btn.classList.remove("liked");
        like_btn.classList.add("unliked");
    } else if (like_btn.classList.contains("unliked")) {
        like_btn.classList.remove("unliked");
        like_btn.classList.add("liked");
    }
}

//Reload Cache

window.addEventListener("pageshow", function (event) {
    var perfEntries = performance.getEntriesByType("navigation");

    if (perfEntries[0].type === "back_forward") {
        location.reload();
    }
});

////Ideathon & Resources

function openTabs(evt, category) {
    var i, tabcontent, tablinks, selectedtab;

    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    selectedtab = document.getElementsByClassName(category);
    for (i = 0; i < selectedtab.length; i++) {
        selectedtab[i].style.display = "block";
    }

    evt.currentTarget.className += " active";

    //document.getElementById("defaultOpen").click();
}


//// Search

function getSearch() {
    var url_string = window.location.href
    var url = new URL(url_string);
    var v = url.searchParams.get("value");
    document.getElementById("searched_val").textContent = v;
    var param = url.searchParams.get("search_option")
    document.getElementById("searched_param").textContent = param;
}

////Ajax

//Like

$('.like-wrapper').click(function (e) {
    e.preventDefault();
    var id;
    id = $(this).attr("data-id");
    $.ajax(
        {
            type: "GET",
            url: "/like",
            data: {
                post_id: id
            }
        })
});

//Register Ideathon 

$('.register-wrapper').click(function (e) {
    $.ajax(
        {
            type: "GET",
            url: "/register-event",
        })
});