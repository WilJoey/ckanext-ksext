$(document).ready(function (){
    mainColumnMerge();

    $('#selOrg').change(orgChanged);
    $('#btnDownload').click(function (){
        //alert(12345);
        console.log($('#selOrg').val());    
        window.open('/tnstats/orgCsv?id='+$('#selOrg').val());
    });
});
    
function orgChanged(evt){
    var url = '/tnstats/orgApi?id=' + evt.target.value;
        $.post(url, function (res){
            RemoveTr();
            var tb = $("#dtStat");
            $(res).each(function (i, d){
                var aps = '<tr>';
                aps += '<td class="metric">' + d.org_name + '</td>';
                aps += '<td><a href="/dataset/' + d.name + '">'+ d.title + '</a></td>';
                aps += '<td class="metric">' + d.dataset_views + '</td>';
                aps += '<td class="metric">' + d.resource_views + '</td>';
                aps += '<td class="metric">' + d.resource_downloads + '</td>';
                aps += '</tr>';
                tb.append(aps);
            });
            mainColumnMerge();
        });
}

function RemoveTr(){
    $(".table tr").each(function (i, d) {
        if(i==0) return;
        $(d).remove();
    });
}

function mainColumnMerge(){

    var checkName = '',
        rowCount = 1,
        checkTd = null;

    $('.table tr').each(function(i, d) {
        if (i == 0) return;
        var td = $(d).children().first();
        if (td.html() != checkName) {
            checkName = td.html();
            if (checkTd) {
                checkTd.attr("rowspan", rowCount);
            }
            rowCount = 1;
            checkTd = td;
        } else {
            td.remove();
            rowCount++;
        }
    });
    
    checkTd.attr("rowspan", rowCount);
}