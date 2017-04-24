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
