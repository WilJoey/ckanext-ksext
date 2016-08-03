$(function() {
    var jr = $("#jRate").jRate({
        startColor: 'cyan',
        endColor: 'blue',
        width: 60,
        height: 60,
        rating: 5,
        count: 5,
        precision: 1,
        readOnly: false,
        onSet: function(rating) {
            console.log('onSet');
        }
    });
    console.log(jr.getRating());
    jr.setRating(1);
    jr.setReadOnly(true);
});