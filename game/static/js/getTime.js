function sendJSON() {

    const minutes = document.getElementById("minutes").textContent;
    const seconds = document.getElementById("seconds").textContent;

    const dict_values = {minutes, seconds}
    const time = JSON.stringify(dict_values);
    console.log(time);

    yourdiv = "test"

    $.ajax({
        type: 'post',
        url: '/divinfo',
        data: JSON.stringify(yourdiv),
        contentType: "application/json; charset=utf-8",
        success: function (data) {
            console.log(data);
        }
    });
}