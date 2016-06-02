// ckan.module('favorite',function (jQuery, _){
//     return {
//         initialize:function (){
//             consoloe.log("I've been initialized for element: %o", this.el);
            
//         }
//     };
// });

$(document).ready(function (){

    var pickers = $(".dpicker input[type=text]").datepicker({
        format:'yyyy/mm/dd'}
    ).on('changeDate', function (ev){
      if(ev.viewMode=='days') $(this).datepicker('hide');
    });

    var n = new Date();
    var y = n.getFullYear();
    var m = n.getMonth()+1;
    if(m<10) m="0"+m;
    var d = n.getDate();
    if(d<10) d="0"+d;

    $("#field-extras2").val(y +"/"+ m +"/"+d);

});
