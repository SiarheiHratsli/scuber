$(document).ready(function() {
    var running = false;
    var startTime;
    var interval;
    var spaceCount = 0;

    function formatTime(elapsedTime) {
        var minutes = Math.floor(elapsedTime / 60000);
        var seconds = Math.floor((elapsedTime % 60000) / 1000);
        var milliseconds = Math.floor((elapsedTime % 1000) / 10);

        if (minutes > 0) {
                    return (minutes < 10 ? "0" : "") + minutes + "." +
                        (seconds < 10 ? "0" : "") + seconds + "." +
                        (milliseconds < 10 ? "0" : "") + milliseconds;
                } else {
                    return (seconds < 10 ? "0" : "") + seconds + "." +
                        (milliseconds < 10 ? "0" : "") + milliseconds;
                }
    }

    function startTimer() {
        document.getElementById('scramble').style.display = 'none';
        document.getElementById('tools').style.display = 'none';
        console.log("Start Timer"); // Отладочный вывод
        startTime = new Date().getTime();
        interval = setInterval(function() {
            var currentTime = new Date().getTime();
            var elapsedTime = currentTime - startTime;
            $("#timer").text(formatTime(elapsedTime));
        }, 10);
        running = true;
    }

    function stopTimer() {
        document.getElementById('scramble').style.display = 'block';
        document.getElementById('tools').style.display = 'flex';
        console.log("Stop Timer"); // Отладочный вывод
        clearInterval(interval);
        running = false;
        spaceCount = 0;

        // Отправка асинхронного запроса на сервер
        $.ajax({
            url: "/generate_scramble",
            type: "GET",
            success: function(response) {
                console.log("Scramble Updated:", response); // Отладочный вывод
                // Обновление значения скрамбла на странице
                $("#scramble").text(response);
            },
            error: function(xhr, status, error) {
                console.error("Ошибка получения скрамбла:", error);
            }
        });
    }

    $(document).keydown(function(event) {
        if (event.keyCode === 32) { // Код клавиши пробела
            event.preventDefault(); // Предотвращаем прокрутку страницы при нажатии пробела
            if (running) {
                stopTimer();
            } else {
                if (spaceCount === 1) {
                    stopTimer();
                } else {
                    startTimer();
                    spaceCount++;
                }
            }
        }
    });
});
