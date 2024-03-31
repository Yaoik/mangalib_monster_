function render_main_info(manga_name) {
    var stats_url = $('#urls')

    $.ajax({
        url: stats_url.data('page-compressed'), // Замените на URL вашего серверного скрипта
        type: 'GET', // Или 'POST', в зависимости от вашего запроса
        dataType: 'json', // Ожидаемый тип данных
        success: function(data){
            let population_page_compressed = $('#population_page_compressed')
            let population_page_compressed_text = $('#population_page_compressed_text')
            population_page_compressed_text.text('Количество комментариев по страницам')
            let arr_population_page_compressed = (Array.from({length: data.population_page_compressed.length}, (_, i) => i + 1))
            render_graph_one(population_page_compressed, arr_population_page_compressed, manga_name, data.population_page_compressed)

            let population_chapter_compressed = $('#population_chapter_compressed')
            let population_chapter_compressed_text = $('#population_chapter_compressed_text')
            population_chapter_compressed_text.text('Количество комментариев по главам')
            let arr_population_chapter_compressed = (Array.from({length: data.population_chapter_compressed.length}, (_, i) => i + 1))
            render_graph_one(population_chapter_compressed, arr_population_chapter_compressed, manga_name, data.population_chapter_compressed)

        },
        error: function(xhr, status, error){
            alert(status)
            alert(error)
            console.error(xhr.responseText);
        }
    });
    $.ajax({
        url: stats_url.data('page-compressed-toxic'), // Замените на URL вашего серверного скрипта
        type: 'GET', // Или 'POST', в зависимости от вашего запроса
        dataType: 'json', // Ожидаемый тип данных
        success: function(data){
            let canvas = $('#toxic_chapters_compressed')
            let lable = $('#toxic_chapters_compressed_text')
            lable.text('Средняя токсичность глав')
            let arr = (Array.from({length: data.chapter_toxic_compressed.length}, (_, i) => i + 1))
            render_graph_one(canvas, arr, manga_name, data.chapter_toxic_compressed)
        },
        error: function(xhr, status, error){
            alert(status)
            alert(error)
            console.error(xhr.responseText);
        }
    });

}

function render_graph_one(canvas, labels, label_dataset, data) {
    
    var percentage_config = {
        type: 'bar', // указываем тип графика (например, 'bar', 'line', 'pie' и т. д.)
        data: {
            labels: labels,
            datasets: [
                {
                    label: label_dataset,
                    data: data,
                    backgroundColor: 'rgb(40, 167, 69, .9)',
                    stack: 'Stack 2',
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
                            return value;
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
                }
            },
        },
    }

    // Создаем и отображаем график
    var myChart = new Chart(canvas, config=percentage_config);
}


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
    
    render_similar(manga_name)
    render_relations(manga_name)
    render_main_info(manga_name)
    $.ajax({
        url: url, // Замените на URL вашего серверного скрипта
        type: 'GET', // Или 'POST', в зависимости от вашего запроса
        dataType: 'json', // Ожидаемый тип данных
        success: async function(data){

            var data_1 = await get_avg()

            var arr = {'bookmarks':[], 'rating':[]}

            arr['rating'].unshift(data_1['rating']['rating_1_percent_avg'])
            arr['rating'].unshift(data_1['rating']['rating_2_percent_avg'])
            arr['rating'].unshift(data_1['rating']['rating_3_percent_avg'])
            arr['rating'].unshift(data_1['rating']['rating_4_percent_avg'])
            arr['rating'].unshift(data_1['rating']['rating_5_percent_avg'])
            arr['rating'].unshift(data_1['rating']['rating_6_percent_avg'])
            arr['rating'].unshift(data_1['rating']['rating_7_percent_avg'])
            arr['rating'].unshift(data_1['rating']['rating_8_percent_avg'])
            arr['rating'].unshift(data_1['rating']['rating_9_percent_avg'])
            arr['rating'].unshift(data_1['rating']['rating_10_percent_avg'])

            arr['bookmarks'].unshift(data_1['bookmarks']['bookmarks_another_percent_avg'])
            arr['bookmarks'].unshift(data_1['bookmarks']['bookmarks_favorite_percent_avg'])
            arr['bookmarks'].unshift(data_1['bookmarks']['bookmarks_readed_percent_avg'])
            arr['bookmarks'].unshift(data_1['bookmarks']['bookmarks_drop_percent_avg'])
            arr['bookmarks'].unshift(data_1['bookmarks']['bookmarks_in_plan_percent_avg'])
            arr['bookmarks'].unshift(data_1['bookmarks']['bookmarks_read_percent_avg'])

            render_bookmarks(data.data.bookmarks.stats, manga_name, data_avg=arr['bookmarks'])
            render_rating(data.data.rating.stats, manga_name, data_avg=arr['rating'])

            $('#bookmarks_text').text('В списках у '+ data.data.bookmarks.count + ' человек')
            $('#rating_text').text(data.data.rating.count+' оценок пользователей')
            add_stats(data)
        },
        error: function(xhr, status, error){
            // Обработка ошибки
            console.error(xhr.responseText); // Вывод ошибки в консоль
        }
    });

});

function render_similar(manga_name) {

    let url = `https://api.lib.social/api/manga/${manga_name}/similar`
    let similar_div = $('#similar')

    

    $.ajax({
        url: url, // Замените на URL вашего серверного скрипта
        type: 'GET', // Или 'POST', в зависимости от вашего запроса
        dataType: 'json', // Ожидаемый тип данных
        success: function(data){
            console.log(data)
            if (data.data.length == 0) {
                similar_div.append('<div class=" text-center w-full h-full align-middle text-3xl text-[#BFBFBF] my-auto ">Тут ничего нет</div>')
            }
            data.data.forEach(el => {
                similar_div.append(`
                                <div class="w-auto min-w-96 h-32 rounded-lg bg-[#252527] flex m-1"> 
                                    <img src='${el.media.cover.default}' class='h-32 w-auto max-w-28 rounded-lg object-cover overflow-hidden '></img>
                                    <div class='flex flex-col justify-start m-2 w-auto'>
                                        <span class='text-[#77A5D8] text-sm'>${el.similar}</span>
                                        <span class='text-[#BFBFBF]'>${el.media.rus_name}</span>
                                        <span class='text-[#EBEBF580] text-sm mt-auto'>${el.media.type.label} . ${el.media.status.label}</span>
                                    </div>
                                </div>
                                `)
            });
        },
        error: function(xhr, status, error){
            console.error(xhr.responseText); // Вывод ошибки в консоль
        }
    });
}

function render_relations(manga_name) {

    let url = `https://api.lib.social/api/manga/${manga_name}/relations`
    let relations_div = $('#relations')

    $.ajax({
        url: url, // Замените на URL вашего серверного скрипта
        type: 'GET', // Или 'POST', в зависимости от вашего запроса
        dataType: 'json', // Ожидаемый тип данных
        success: function(data){
            console.log(data)
            if (data.data.length == 0) {
                relations_div.append('<div class=" text-center w-full h-full align-middle text-3xl text-[#BFBFBF] my-auto ">Тут ничего нет</div>')
            }
            data.data.forEach(el => {
                relations_div.append(`
                                    <div class="w-auto min-w-96 h-32 rounded-lg bg-[#252527] flex m-1"> 
                                        <img src='${el.media.cover.default}' class='h-32 w-auto max-w-28 rounded-lg object-cover overflow-hidden '></img>
                                        <div class='flex flex-col justify-start m-2 w-auto'>
                                            <span class='text-[#77A5D8] text-sm'>${el.related_type.label}</span>
                                            <span class='text-[#BFBFBF]'>${el.media.rus_name}</span>
                                            <span class='text-[#EBEBF580] text-sm mt-auto'>${el.media.type.label} . ${el.media.status.label}</span>
                                        </div>
                                    </div>
                                    `)
            });


        },
        error: function(xhr, status, error){
            console.error(xhr.responseText); // Вывод ошибки в консоль
        }
    });
}

function get_avg() {
    return new Promise((resolve, reject) => {

    var stats_url = $('#urls')

    $.ajax({
        url: stats_url.data('get-stats-urs'), // Замените на URL вашего серверного скрипта
        type: 'GET', // Или 'POST', в зависимости от вашего запроса
        dataType: 'json', // Ожидаемый тип данных
        success: function(data){
            resolve(data)
        },
        error: function(xhr, status, error){
            console.error(xhr.responseText); // Вывод ошибки в консоль
        }
    });

    })
    
}

function add_stats(data) {
    var stats_url = $('#urls')

    $.ajax({
        url: stats_url.data('stats'), // Замените на URL вашего серверного скрипта
        type: 'POST', // Или 'POST', в зависимости от вашего запроса
        dataType: 'json', // Ожидаемый тип данных
        data: {'data': JSON.stringify(data.data), 'manga':stats_url.data('manga-id')},
        headers: {
            'X-CSRFToken': stats_url.data('csrf') // Установка CSRF-токена в заголовок
        },
        success: function(data){

        },
        error: function(xhr, status, error){
            alert(status)
            alert(error)
            console.error(xhr.responseText);
        }
    });
}

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

function render_rating(data, manga_name, data_avg) {
    
    // Инициализируем новый график с помощью Chart.js
    var labels = data.map(item => item.label);
    var values = data.map(item => item.value);
    // Ваши исходные данные (в числовом формате)
    var total = values.reduce((acc, curr) => acc + curr, 0);

    // Преобразование значений в проценты
    var percentages = values.map(value => ((value / total) * 100).toFixed(2));

    var ctx = document.getElementById('rating').getContext('2d');
    
    render_graph(labels, manga_name, 'test', percentages, data_avg, ctx)
}


function render_bookmarks(data, manga_name, data_avg) {
    
    // Инициализируем новый график с помощью Chart.js
    var labels = data.map(item => item.label);
    var values = data.map(item => item.value);
    // Ваши исходные данные (в числовом формате)
    var total = values.reduce((acc, curr) => acc + curr, 0);

    // Преобразование значений в проценты
    var percentages = values.map(value => ((value / total) * 100).toFixed(2));

    var ctx = document.getElementById('bookmarks').getContext('2d');
    
    render_graph(labels, manga_name, 'test', percentages, data_avg, ctx)
}

