(function () {
    let top = window.scrollY;
    if (top < 50)
        document.getElementById("main_menu").classList.remove("bg-light");

    window.onscroll = function() {
        top = window.scrollY;
        if (top < 50) {
            document.getElementById("main_menu").classList.remove("bg-light");
        } else {
            document.getElementById("main_menu").classList.add("bg-light");
        }
    };
})();