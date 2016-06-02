    var checkAddId = ['field-title','field-extras-0-value','field-notes','field-extras-1-value',
        'field-extras-2-value','field-extras-3-value',
        'field-maintainer','field-extras-7-value','field-extras-8-value'];
    var checkAddMsg = ['資料集名稱','資料集類型','資料集描述','資料量',
        '授權說明網址','計費方式',
        '提供機關聯絡人','提供機關聯絡人電話','提供機關地址'];


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
	if($('#field-extras-11').val()==='000'){
          alert('請選擇[服務分類]!');
	  return false;
	}
        return true;
      });
    });
