var result = $('#result')


function add_elems(data) {
    result.html(data)

    let next_data = $('#next')

    if (Number(next_data.data('next'))) {
        
    }
}
var search = debounce((q, page) => {
    console.info(q)
    console.info(q.val())
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





