


$(document).ready(function(){
    // Выполняем AJAX-запрос после загрузки страницы
    const pattert = 'manga/(.*?)/'
    const href = window.location.href

    var match = href.match(new RegExp(pattert));

    if (match && match[1]) {
        var manga_name = match[1];
        var url = `https://api.lib.social/api/manga/${manga_name}/stats?bookmarks=true&rating=true`;
        console.log(url); // Выведет URL с результатом вместо *тут должен быть результат*
    } else {
        console.log("Не удалось найти совпадение в URL");
    }
    
    
    $.ajax({
        url: url, // Замените на URL вашего серверного скрипта
        type: 'GET', // Или 'POST', в зависимости от вашего запроса
        dataType: 'json', // Ожидаемый тип данных
        success: function(data){
            console.log(data)
            render_bookmarks(data.data.bookmarks.stats, manga_name)
            render_rating(data.data.rating.stats, manga_name)
        },
        error: function(xhr, status, error){
            // Обработка ошибки
            console.error(xhr.responseText); // Вывод ошибки в консоль
        }
    });




});

function render_graph(labels, label_data, label_avg, data, data_avg, canvas) {
    
    var percentage_config = {
        type: 'bar', // указываем тип графика (например, 'bar', 'line', 'pie' и т. д.)
        data: {
            labels: labels,
            datasets: [
                {
                    label: label_data,
                    data: data,
                    backgroundColor: 'rgb(40, 167, 69, .9)',
                    stack: 'Stack 2',
                },
                {
                    label: 'В среднем по Mangalib',
                    data: data_avg,
                    backgroundColor: 'rgb(167, 40, 69, .9)',
                    stack: 'Stack 1',
                },
            ]
        },
        options: {
            responsive: true,
            legend: {
                display: true,
                position: 'top', // Позиция легенды
                labels: {
                    fontColor: 'green', // Новый цвет текста легенды
                    fontSize: 16 // Новый размер текста легенды
                }
            },
            scales: {
                y: {
                    max: 100,
                    min: 0,
                    stacked: false,
                    beginAtZero: true,
                    ticks: {
                        font: {
                            family: 'Arial', // Новый шрифт
                            size: 14, // Новый размер
                            style: 'italic', // Новый стиль (например, 'normal', 'italic', 'oblique')
                            color: 'blue' // Новый цвет
                        },
                        callback: function(value) {
                            return value + "%";
                        }
                    }
                }
            },
            plugins: {
                tooltip: {
                    titleFont: {
                        size: 16
                    },
                    bodyFont: {
                        size: 16
                    },
                    footerFont: {
                        size: 16 // there is no footer by default
                    },
                    callbacks: {
                        label: function(context) {
                            var datasetIndex = context.datasetIndex;
                            var dataIndex = context.dataIndex;

                            var datasetLabel = context.chart.data.datasets[datasetIndex].label || '';

                            var value = context.chart.data.datasets[datasetIndex].data[dataIndex] || 0;
                            /* console.log(value) */
                            /* var percentage = ((value / total) * 100).toFixed(1) + '%'; */
                            return datasetLabel + ': ' + ' ' + value + '%';
                            return datasetLabel + ': ' + values[dataIndex] + ' (' + percentage + ')';
                        }
                    },

                }
            },
        }
    }

    // Создаем и отображаем график
    var myChart = new Chart(canvas, config=percentage_config);
}

function render_rating(data, manga_name) {
    
    // Инициализируем новый график с помощью Chart.js
    var labels = data.map(item => item.label);
    var values = data.map(item => item.value);
    // Ваши исходные данные (в числовом формате)
    var total = values.reduce((acc, curr) => acc + curr, 0);

    // Преобразование значений в проценты
    var percentages = values.map(value => ((value / total) * 100).toFixed(2));

    var ctx = document.getElementById('rating').getContext('2d');
    
    var data_avg = [10,10,5,35,30,10,0,0,0,0]
    render_graph(labels, manga_name, 'test', percentages, data_avg, ctx)
}


function render_bookmarks(data, manga_name) {
    
    // Инициализируем новый график с помощью Chart.js
    var labels = data.map(item => item.label);
    var values = data.map(item => item.value);
    // Ваши исходные данные (в числовом формате)
    var total = values.reduce((acc, curr) => acc + curr, 0);

    // Преобразование значений в проценты
    var percentages = values.map(value => ((value / total) * 100).toFixed(2));

    var ctx = document.getElementById('bookmarks').getContext('2d');
    

    var data_avg = [10,10,5,35,30,10]
    render_graph(labels, manga_name, 'test', percentages, data_avg, ctx)
}

