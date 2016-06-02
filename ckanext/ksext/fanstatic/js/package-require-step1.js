    var checkAddId = ['field-title','field-extras-0-value','field-notes','field-extras-1-value',
        'field-extras-2-value','field-extras-3-value'];
    var checkAddMsg = ['資料集名稱','資料集類型','資料集描述','資料量',
        '授權說明網址','計費方式'];

    $(document).ready(function (){

      $('button[name=save]').click(function(){
        //console.log($(this).val());
        for(var i in checkAddId){
          var item=$("#"+checkAddId[i]);
          if(item.val().trim()==''){
            item.focus();
            alert("欄位 [" + checkAddMsg[i] + "] 必填!");
            return false;
          }
        }
        return true;
      });
    });