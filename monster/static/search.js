var search_bar = $('#search_bar')
var result = $('#result')

document.addEventListener('click', (event) => {
    if (!search_bar[0].contains(event.target)){
        result.html('')
    }
})







function add_elems(data) {
    result.append(data)

    var next_data = $('#next')
    var page = next_data.data('page')

    try {
        var load_more = $('#load_more')
        load_more.remove()
    } catch (error) {
        
    }

    if (Number(next_data.data('next'))) {
        let el = "<button id='load_more' class='w-48 h-16 text-[#EBEBF580] bg-[#252526] hover:bg-[#313134] py-2 px-4 duration-300 m-auto border border-[#252526] rounded-lg my-4 text-center'> Загрузить ещё </button>"
        result.append(el)
        console.info(result)
        var load_more = $('#load_more')
        console.info(load_more)

        load_more.on('click', () => {
            next_data.remove()

            search_add(q_el, page+1)
        }
    )
    }
}

var search_add = debounce((q, page) => {
    if (q.val()==''){
        result.empty()
    }
    else {
        $.ajax({
            url: q.data('url'),
            method: 'get',
            dataType: 'html',
            data: {'q': q.val(), 'page':page},
            success: function(data){
                add_elems(data)
            }
        });
    }
}, 1)

var search = debounce((q, page) => {
    if (q.val()==''){
        result.empty()
    }
    else {
        $.ajax({
            url: q.data('url'),
            method: 'get',
            dataType: 'html',
            data: {'q': q.val(), 'page':page},
            success: function(data){
                result.html('')
                add_elems(data)
            }
        });
    }
}, 500)


function debounce(callback, delay) {
    let event_q
    return (...args) => {
        clearTimeout(event_q)
        event_q = setTimeout(() => {
            callback(...args)
        }, delay);
    }
}

var q_el = $('#q')

q_el.on('input', () => {
        search(q_el, 1)
    }
)





