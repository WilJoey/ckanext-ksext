$(function() {
    AverageInit();
    UserInit();

    $('#frmRanking').submit(function(){ 
        var score = parseInt($('#hidUserRate').val());
        if( score<1 || score>5){
            alert('請先給予資料集評分.');
            return false;
        }
        return true;
    });

    function AverageInit(){
        var avg = $('#hidRateAvg').val();
        $('#lblRateAvg').html(Math.round(avg * 10 / 10));
        $("#dsRate").jRate({
            startColor: 'cyan',
            endColor: 'blue',
            backgroundColor: 'lightgray',
            width: 40,
            height: 40,
            rating: avg,
            count: 5,
            precision: 0.5,
            readOnly: true
        });
    }

    function UserInit(){
        var avg = $('#hidUserRate').val();
        $("#userRate").jRate({
            startColor: 'pink',
            endColor: 'red',
            backgroundColor: 'lightgray',
            rating: avg,
            count: 5,
            precision: avg === '-1' ? 1 : 0.5,
            readOnly: avg !== '-1',
            onSet: function(rating) {
                 $('#hidUserRate').val(rating);
                 $('#lblInfo').html('您的評分：' + rating + ' 顆星');
            }
        });
    }
});


