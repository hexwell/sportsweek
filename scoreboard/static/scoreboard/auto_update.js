var events = $(".event").map(function() {
    return this.id;
}).get();

function update_wrapper(url){
   return (function(){
       $.get(url+events.join("."), function(data, status){
            events.forEach(function (event_id, index, events) {
                var event_element = $('#' + event_id);
                event_element.find(".squad0").html(data[event_id]['score0']);
                event_element.find(".squad1").html(data[event_id]['score1']);
            })
       });
   });
}

function sendData(url){
    $.get(url, function(data, status){});
}

function updateLocal(event_id, score, val) {
    var elem, container = $('#' + event_id);
    if(score === 0){
        elem = container.find(".squad0")[0];
        if(val === '+'){
            elem.innerHTML = parseInt(elem.innerHTML) + 1
        }
        else if(val === '-'){
            elem.innerHTML = parseInt(elem.innerHTML) - 1
        }
    } else if (score === 1){
        elem = container.find(".squad1")[0];
        if(val === '+'){
            elem.innerHTML = parseInt(elem.innerHTML) + 1
        }
        else if(val === '-'){
            elem.innerHTML = parseInt(elem.innerHTML) - 1
        }
    }
}
