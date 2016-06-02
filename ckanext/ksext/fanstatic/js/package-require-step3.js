    var checkAddId = ['field-maintainer','field-extras-7-value','field-extras-8-value'];
    var checkAddMsg = ['提供機關聯絡人','提供機關聯絡人電話','提供機關地址'];


    $(document).ready(function (){

      $('button[value=finish]').click(function(){
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