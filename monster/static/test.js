function render_main_info(manga_name) {
    var stats_url = $('#urls')
    let canvas
    let lable
    let arr

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
            canvas = $('#toxic_chapters_compressed')
            lable = $('#toxic_chapters_compressed_text')
            lable.text('Средняя токсичность глав')
            arr = Object.keys(data.chapter_toxic_compressed)
            let arr_new = []
            arr.forEach(element => {
                element = parseFloat(element)
                arr_new.push(element)
            });
            arr_new = arr_new.sort(function(a,b) { return a - b;});
            let new_dict = {}
            arr_new.forEach(element => {
                new_dict[element] = data.chapter_toxic_compressed[element]
            });
            render_graph_one(canvas, [], manga_name, new_dict)

            function getKeyByValue(object, value) {
                return Object.keys(object).find(key => object[key] === value);
            }
            canvas = $('#page_of_chapter_toxic_compressed')
            lable = $('#page_of_chapter_toxic_compressed'+'_text')
            new_arr = (Array.from({length: data.page_of_chapter_toxic_compressed.length}, (_, i) => i + 1))
            let m = Math.max(...Object.values(data.chapter_toxic_compressed))
            let index = getKeyByValue(data.chapter_toxic_compressed, m)
            lable.text('Средняя токсичность страниц на самой токсичной главе ' + `(${index})`)
            render_graph_one(canvas, new_arr, manga_name, data.page_of_chapter_toxic_compressed)
        },
        error: function(xhr, status, error){
            alert(status)
            alert(error)
            console.error(xhr.responseText);
        }
    });

    $.ajax({
        url: $('#at_days').text(), // Замените на URL вашего серверного скрипта
        type: 'GET', // Или 'POST', в зависимости от вашего запроса
        dataType: 'json', // Ожидаемый тип данных
        success: function(data){
            arr = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресение']

            canvas = $('#comments_at_days_of_the_week')
            lable = $('#comments_at_days_of_the_week' + '_text')
            lable.text('Написание комментариев по дням недели')
            render_graph_one_line(canvas, arr, manga_name, data.comments_at_days_of_the_week)

            canvas = $('#chapters_at_days_of_the_week')
            lable = $('#chapters_at_days_of_the_week' + '_text')
            lable.text('Выход глав по дням недели')
            render_graph_one_line(canvas, arr, manga_name, data.chapters_at_days_of_the_week)
        },
        error: function(xhr, status, error){
            alert(status)
            alert(error)
            console.error(xhr.responseText);
        }
    });

    $.ajax({
        url: $('#at_days_percent').text(), // Замените на URL вашего серверного скрипта
        type: 'GET', // Или 'POST', в зависимости от вашего запроса
        dataType: 'json', // Ожидаемый тип данных
        success: function(data){
            arr = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресение']


            canvas = $('#comments_at_days_of_the_weekk_percent')
            lable = $('#comments_at_days_of_the_weekk_percent' + '_text')
            lable.text('Написание комментариев по дням в процентах')
            render_graph_one_line_many_percent(canvas, arr, manga_name, data.comments_at_days_of_the_weekk_percent, 'В среднем по Mangalib', data.comments_at_days_of_the_weekk_percent_avg)

            canvas = $('#chapters_at_days_of_the_week_percent')
            lable = $('#chapters_at_days_of_the_week_percent' + '_text')
            lable.text('Выход глав по дням недели в процентах')
            render_graph_one_line_many_percent(canvas, arr, manga_name, data.chapters_at_days_of_the_week_percent, 'В среднем по Mangalib', data.chapters_at_days_of_the_week_percent_avg)
        },
        error: function(xhr, status, error){
            alert(status)
            alert(error)
            console.error(xhr.responseText);
        }
    });

    $.ajax({
        url: $('#at_24_h').text(), // Замените на URL вашего серверного скрипта
        type: 'GET', // Или 'POST', в зависимости от вашего запроса
        dataType: 'json', // Ожидаемый тип данных
        success: function(data){
            arr = (Array.from({length: 24}, (_, i) => i + 1))

            canvas = $('#chapters_at_24_hours')
            lable = $('#chapters_at_24_hours' + '_text')
            lable.text('Выход глав по часам')
            render_graph_one_pie(canvas, arr, manga_name, data.chapters_at_24_hours)

            canvas = $('#comments_at_24_hours')
            lable = $('#comments_at_24_hours' + '_text')
            lable.text('Написание комментариев по часам')
            render_graph_one_pie(canvas, arr, manga_name, data.comments_at_24_hours)
        },
        error: function(xhr, status, error){
            alert(status)
            alert(error)
            console.error(xhr.responseText);
        }
    });
}
function render_graph_one_pie(canvas, labels, label_dataset, data) {
    
    var percentage_config = {
        type: 'radar', // указываем тип графика (например, 'bar', 'line', 'pie', 'radar')
        data: {
            labels: labels,
            datasets: [
                /* rgba(40, 167, 69, 0.9) */
                {
                    label: label_dataset,
                    data: data,
                    backgroundColor: 'rgba(40, 167, 69, 0.2)',
                    borderColor: 'rgb(40, 167, 69, .9)',
                    borderWidth: 1, // Толщина линии
                    pointRadius: 2, // Радиус точек
                    pointBackgroundColor: 'rgb(40, 167, 69, .9)', // Цвет точек
                    pointBorderColor: 'rgb(40, 167, 69, .9)', // Цвет границ точек
                    pointBorderWidth: 1, // Толщина границ точек

                },
            ]
        },
        options: {
            scales: {
                r: { // https://www.chartjs.org/docs/latest/axes/radial/
                  ticks: { // https://www.chartjs.org/docs/latest/axes/radial/#ticks
                    color: 'white',
                    backdropColor: 'transparent' // https://www.chartjs.org/docs/latest/axes/_common_ticks.html
                  }
                }
            },
            plugins: {
                legend: {
                    display: true, // изменено на true
                },
            },
        },
    }

    // Создаем и отображаем график
    var myChart = new Chart(canvas, config=percentage_config);
}

function render_graph_one_line_many_percent(canvas, labels, dataset1, data1, dataset2, data2) {
    
    var percentage_config = {
        type: 'line', // указываем тип графика (например, 'bar', 'line', 'pie' и т. д.)
        data: {
            labels: labels,
            datasets: [
                {
                    label: dataset1,
                    data: data1,
                    backgroundColor: 'rgba(40, 167, 69, 0.2)',
                    borderColor: 'rgb(40, 167, 69, .9)',
                    borderWidth: 2, // Толщина линии
                    pointRadius: 5, // Радиус точек
                    pointBackgroundColor: 'rgb(40, 167, 69, .9)', // Цвет точек
                    pointBorderColor: 'rgb(40, 167, 69, .9)', // Цвет границ точек
                    pointBorderWidth: 2, // Толщина границ точек
                    stack: 'Stack 2',
                    fill: 'origin',
                },
                {
                    label: dataset2,
                    data: data2,
                    backgroundColor: 'rgb(167, 40, 69, .2)',
                    borderColor: 'rgb(167, 40, 69, .9)',
                    borderWidth: 2, // Толщина линии
                    pointRadius: 5, // Радиус точек
                    pointBackgroundColor: 'rgb(167, 40, 69, .9)', // Цвет точек
                    pointBorderColor: 'rgb(167, 40, 69, .9)', // Цвет границ точек
                    pointBorderWidth: 2, // Толщина границ точек
                    stack: 'Stack 2',
                    fill: 'origin',
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
                    stacked: false,
                    beginAtZero: false,
                    ticks: {
                        font: {
                            family: 'Arial', // Новый шрифт
                            size: 14, // Новый размер
                            style: 'italic', // Новый стиль (например, 'normal', 'italic', 'oblique')
                            color: 'blue' // Новый цвет
                        },
                        callback: function(value) {
                            return Math.round((value + Number.EPSILON) * 1000) / 1000 + '%';
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
        },
    }

    // Создаем и отображаем график
    var myChart = new Chart(canvas, config=percentage_config);
}

function render_graph_one_line(canvas, labels, label_dataset, data) {
    
    var percentage_config = {
        type: 'line', // указываем тип графика (например, 'bar', 'line', 'pie' и т. д.)
        data: {
            labels: labels,
            datasets: [
                {
                    label: label_dataset,
                    data: data,
                    backgroundColor: 'rgba(40, 167, 69, 0.2)',
                    borderColor: 'rgb(40, 167, 69, .9)',
                    borderWidth: 2, // Толщина линии
                    pointRadius: 5, // Радиус точек
                    pointBackgroundColor: 'rgb(40, 167, 69, .9)', // Цвет точек
                    pointBorderColor: 'rgb(40, 167, 69, .9)', // Цвет границ точек
                    pointBorderWidth: 2, // Толщина границ точек
                    stack: 'Stack 2',
                    fill: 'origin',
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
                    stacked: false,
                    beginAtZero: false,
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
            if (data.data.length == 0) {
                similar_div.append('<div class=" text-center w-full h-full align-middle text-3xl text-[#BFBFBF] my-auto ">Тут ничего нет</div>')
            }
            data.data.forEach(el => {
                similar_div.append(`
                                <div class="w-auto min-w-96 h-32 rounded-lg bg-[#252527] flex m-1 similarr cursor-pointer" data-slug="${el.media.slug_url}"> 
                                    <img src='${el.media.cover.default}' class='h-32 w-auto max-w-28 rounded-lg object-cover overflow-hidden '></img>
                                    <div class='flex flex-col justify-start m-2 w-auto'>
                                        <span class='text-[#77A5D8] text-sm'>${el.similar}</span>
                                        <span class='text-[#BFBFBF]'>${el.media.rus_name}</span>
                                        <span class='text-[#EBEBF580] text-sm mt-auto'>${el.media.type.label} . ${el.media.status.label}</span>
                                    </div>
                                </div>
                                `)
            });
            $('.similarr').on("click", function() {
                console.log($(this))
                console.log($(this).data('slug'))
                window.location.replace($("#manga").text().replace('pass', $(this).data('slug')))
            })
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
            if (data.data.length == 0) {
                relations_div.append('<div class=" text-center w-full h-full align-middle text-3xl text-[#BFBFBF] my-auto ">Тут ничего нет</div>')
            }
            data.data.forEach(el => {
                relations_div.append(`
                                    <div class="w-auto min-w-96 h-32 rounded-lg bg-[#252527] flex m-1 relationn cursor-pointer" data-slug="${el.media.slug_url}"> 
                                        <img src='${el.media.cover.default}' class='h-32 w-auto max-w-28 rounded-lg object-cover overflow-hidden '></img>
                                        <div class='flex flex-col justify-start m-2 w-auto'>
                                            <span class='text-[#77A5D8] text-sm'>${el.related_type.label}</span>
                                            <span class='text-[#BFBFBF]'>${el.media.rus_name}</span>
                                            <span class='text-[#EBEBF580] text-sm mt-auto'>${el.media.type.label} . ${el.media.status.label}</span>
                                        </div>
                                    </div>
                                    `);
            }
            );
            $('.relationn').on("click", function() {
                console.log($(this))
                console.log($(this).data('slug'))
                window.location.replace($("#manga").text().replace('pass', $(this).data('slug')))
            })

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

