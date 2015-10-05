$('#receptionAdd').click(function(){
    var receptionPanel = $('#receptionAddPanel');
    receptionPanel.toggle(!receptionPanel.is(":visible"));
});

$('#id_reception_date').datepicker(
    { dateFormat: 'yy-mm-dd' }
);