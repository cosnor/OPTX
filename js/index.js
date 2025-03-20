document.addEventListener("DOMContentLoaded", function() {
    const btnEnigma = document.getElementById("enigma");
    const btnEureka = document.getElementById("eureka");
    const btnLacuna = document.getElementById("lacuna");
    const btnReplica = document.getElementById("replica");

    btnEnigma.addEventListener("click", () => {
        window.location.href = "templates/enigma.html";
    });

    btnEureka.addEventListener("click", () => {
        window.location.href = "templates/eureka.html";
    });

    btnLacuna.addEventListener("click", () => {
        window.location.href = "templates/lacuna.html";
    });

    btnReplica.addEventListener("click", () => {
        window.location.href = "templates/replica.html";
    });

});