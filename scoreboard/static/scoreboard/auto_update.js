var events = $(".event").map(function() {
    return this.id;
}).get();

function update_wrapper(url){
   return (function(){
       $.get(url+events.join("."), function(data, status){
            console.log(data);
       });
   });
}
