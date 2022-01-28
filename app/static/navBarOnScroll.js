document.getElementById("container").addEventListener("scroll", myFunction);

function myFunction() {
    if (window.scrollY > 100) {
        document.getElementById("container").classList.add("active");
    } else {
        document.getElementById("container").classList.remove("active");
    }
}

