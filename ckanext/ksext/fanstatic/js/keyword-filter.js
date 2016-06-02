$(document).ready(function (){
    var d= new Date();
    $(".dpicker").datepicker({
        format:'yyyy/mm/dd'}
    ).on('changeDate', function (ev){
        if(ev.viewMode=='days') $(this).datepicker('hide');
    });
    
    var m = d.getMonth()+1;
    if(m<10) m="0"+m;
    $("#txtStart").val(d.getFullYear() + "/" + m + "/01");
    
    m = d.getMonth()+2;
    if(m<10) m="0"+m;
    $("#txtEnd").val(d.getFullYear() + "/" + m + "/01");

    $('#btnFilter').click(DateFilter);
    $('#btnAll').click(AllKeyword);
});
    
function DateFilter(){
    var url ='/tnstats/kwfilter?start='+$("#txtStart").val()+"&end="+$("#txtEnd").val();
    KeywordApi(url);
}

function AllKeyword(){
    var url ='/tnstats/kwfilter?all=true';
    KeywordApi(url);
}
    
function RemoveTr(){
    $(".table tr").each(function (i, d) {
        if(i==0) return;
        $(d).remove();
    });
}

function AppendResult(data){
    var tb = $(".table");
    $(data).each(function (i, d){
        tb.append("<tr><td>" + d.content + "</td><td>" + d.count + "</td></tr>");
    });
}

function KeywordApi(url){
    console.log(url);
    $.ajax(url).done(function(data){
        console.log(data.status);
        console.log(data.data);
        if(data.status){
            RemoveTr();
            AppendResult(data.data);
        }else{
            alert('錯誤！確認輸入的日期格式。');
        }
  });
}
  