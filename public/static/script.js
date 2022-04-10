$('#check1').change(function() {
    if ($("#action2").attr("hidden", true)) {
        $("#action2").attr("hidden", false);
    }
})
$('#chec').change(function() {
    if ($("#actionss").attr("hidden", true)) {
        $("#actionss").attr("hidden", false);
    }
})
$('#vaccineinventory').change(function() {
    if ($("#vaccineinventoryform").attr("hidden", true)) {
        $("#healthform").attr("hidden", true);
        $("#health").prop("checked", false);
        $("#healthform input[id=date2]").val('');
        $("#healthform input[id=date3]").val('')
        $("#healthfilter").attr("hidden", true)
        $("#btn2").prop("checked", false)
        $("#vaccineinventoryform").attr("hidden", false);
    }
})
$('#btn1').change(function() {
    if ($("#vaccineinventoryfilter").attr("hidden", true)) {
        $("#vaccineinventoryfilter").attr("hidden", false);
    }
})
$('#health').change(function() {
    if ($("#healthform").attr("hidden", true)) {
        $("#vaccineinventoryform").attr("hidden", true);
        $("#vaccineinventoryform input[id=date]").val('');
        $("#vaccineinventoryform input[id=date1]").val('');
        $("#vaccineinventoryfilter").attr("hidden", true);
        $("#btn1").prop("checked", false);
        $("#vaccineinventory").prop("checked", false)
        $("#healthform").attr("hidden", false);

    }
})
$('#btn2').change(function() {
    if ($("#healthfilter").attr("hidden", true)) {
        $("#healthfilter").attr("hidden", false);
    }
})
$('#death').change(function() {
    if ($("#deathform").attr("hidden", true)) {
        $("#inseminationsform").attr("hidden", true);
        $("#inseminations").prop("checked", false);
        $("#calving").prop("checked", false)
        $("#inseminationsform input[id=date8]").val('');
        $("#inseminationsform input[id=date9]").val('')
        $("#inseminationsfilter").attr("hidden", true)
        $("#calvingform").attr("hidden", true);
        $("#calvingform input[id=date4]").val('');
        $("#calvingform input[id=date5]").val('');
        $("#calvingfilter").attr("hidden", true);
        $("#btn5").prop("checked", false)
        $("#btn3").prop("checked", false);
        $("#deathform").attr("hidden", false);
    }
})
$('#btn4').change(function() {
    if ($("#deathfilter").attr("hidden", true)) {
        $("#deathfilter").attr("hidden", false);
    }
})
$('#inseminations').change(function() {
    if ($("#inseminationsform").attr("hidden", true)) {
        $("#deathform").attr("hidden", true);
        $("#deathform input[id=date6]").val('');
        $("#deathform input[id=date7]").val('');

        $("#calvingform").attr("hidden", true);
        $("#calvingform input[id=date4]").val('');
        $("#calvingform input[id=date5]").val('');
        $("#calvingfilter").attr("hidden", true);
        $("#deathfilter").attr("hidden", true);
        $("#btn4").prop("checked", false);
        $("#btn3").prop("checked", false);
        $("#death").prop("checked", false)
        $("#calving").prop("checked", false)
        $("#inseminationsform").attr("hidden", false);

    }
})
$('#calving').change(function() {
    if ($("#calvingform").attr("hidden", true)) {
        $("#inseminationsform").attr("hidden", true);
        $("#inseminations").prop("checked", false);
        $("#inseminationsform input[id=date8]").val('');
        $("#inseminationsform input[id=date9]").val('')
        $("#deathfilter").attr("hidden", true);
        $("#deathform").attr("hidden", true);
        $("#deathform input[id=date6]").val('');
        $("#deathform input[id=date7]").val('');
        $("#inseminationsfilter").attr("hidden", true)
        $("#btn5").prop("checked", false)
        $("#btn4").prop("checked", false);
        $("#death").prop("checked", false)

        $("#calvingform").attr("hidden", false);
    }
})
$('#milksale').change(function() {
    if ($("#milksaleform").attr("hidden", true)) {
        $("#milkcollectionform").attr("hidden", true);
        $("#milkcollection").prop("checked", false);
        $("#unservedmilksalefilter").attr("hidden", true);

        $("#milkcollectionform input[id=date12]").val('');
        $("#milkcollectionform input[id=date13]").val('')
        $("#unservedmilksaleform input[id=date30]").val('');
        $("#unservedmilksaleform input[id=date31]").val('');
        $("#milkcollectionfilter").attr("hidden", true)
        $("#btn7").prop("checked", false)
        $("#btn32").prop("checked", false);
        $("#milksaleform").attr("hidden", false);
        $("#unservedmilksaleform").attr("hidden", false);
        $("#unservedmilksaleform").attr("hidden", true);
        $("#unservedmilksale").prop("checked", false);
    }
})
$('#unservedmilksale').change(function() {
    if ($("#uservedmilksaleform").attr("hidden", true)) {
        $("#milksaleform").attr("hidden", true);
        $("#unservedmilksaleform").attr("hidden", false);
        $("#milkcollectionform").attr("hidden", true);
        $("#milkcollection").prop("checked", false);
        $("#milkcollectionform input[id=date12]").val('');
        $("#milkcollectionform input[id=date13]").val('')
        $("#milksaleform input[id=date10]").val('');
        $("#milksaleform input[id=date11]").val('');
        $("#milkcollectionfilter").attr("hidden", true)
        $("#btn6").prop("checked", false);
        $("#btn7").prop("checked", false)
        $("#milksaleform").attr("hidden", true);
        $("#milksalefilter").attr("hidden", true);
        $("#milksale").prop("checked", false);


        $("#milksale").prop("checked", false);
    }
})
$('#btn6').change(function() {
    if ($("#milksalefilter").attr("hidden", true)) {
        $("#milksalefilter").attr("hidden", false);
    }
})
$('#btn32').change(function() {
    if ($("#unservedmilksalefilter").attr("hidden", true)) {
        $("#unservedmilksalefilter").attr("hidden", false);
    }
})
$('#milkcollection').change(function() {
    if ($("#milkcollectionform").attr("hidden", true)) {
        $("#milksaleform").attr("hidden", true);
        $("#milksaleform input[id=date10]").val('');
        $("#milksaleform input[id=date11]").val('');
        $("#unservedmilksaleform input[id=date30]").val('');
        $("#unservedmilksaleform input[id=date31]").val('');
        $("#milksalefilter").attr("hidden", true);
        $("#unservedmilksalefilter").attr("hidden", true);
        $("#btn6").prop("checked", false);
        $("#btn32").prop("checked", false);
        $("#milksale").prop("checked", false);
        $("#milkcollectionform").attr("hidden", false);
        $("#unservedmilksale").prop("checked", false);
        $("#unservedmilksaleform").attr("hidden", true);

    }
})
$('#btn7').change(function() {
    if ($("#milkcollectionfilter").attr("hidden", true)) {
        $("#milkcollectionfilter").attr("hidden", false);
    }
})
$('#btn3').change(function() {
    if ($("#calvingfilter").attr("hidden", true)) {
        $("#calvingfilter").attr("hidden", false);
    }
})
$('#btn5').change(function() {
    if ($("#inseminationsfilter").attr("hidden", true)) {
        $("#inseminationsfilter").attr("hidden", false);
    }
})
$('#cowsfeeding').change(function() {
    if ($("#cowsfeedingform").attr("hidden", true)) {
        $("#cowsfeedinventoryform").attr("hidden", true);
        $("#cowsfeedinventory").prop("checked", false);
        $("#cowsfeedinventoryform input[id=date16]").val('');
        $("#cowsfeedinventoryform input[id=date17]").val('')
        $("#cowsfeedinventoryfilter").attr("hidden", true)
        $("#btn9").prop("checked", false)
        $("#btn").prop("checked", false)
        $("#cowsfeedingform").attr("hidden", false);
    }
})
$('#btn8').change(function() {
    if ($("#cowsfeedingfilter").attr("hidden", true)) {
        $("#cowsfeedingfilter").attr("hidden", false);
    }
})
$('#cowsfeedinventory').change(function() {
    if ($("#cowsfeedinventoryform").attr("hidden", true)) {
        $("#cowsfeedingform").attr("hidden", true);
        $("#cowsfeedingform input[id=date14]").val('');
        $("#cowsfeedingform input[id=date15]").val('');
        $("#cowsfeedingfilter").attr("hidden", true);
        $("#btn8").prop("checked", false);
        $("#cowsfeeding").prop("checked", false)
        $("#cowsfeedinventoryform").attr("hidden", false);

    }
})
$('#btn9').change(function() {
    if ($("#cowsfeedinventoryfilter").attr("hidden", true)) {
        $("#cowsfeedinventoryfilter").attr("hidden", false);
    }
})
$(function() {
    $('#date0').datetimepicker({
        format: 'yyyy/MM/DD hh:mm A',
        maxDate: new Date(),
        ignoreReadonly: true
    });
})
$(function() {
    $('#date00').datetimepicker({
        format: 'yyyy/MM/DD hh:mm A',
        maxDate: new Date(),
        // minDate: $('#date0').val(),
        ignoreReadonly: true
    });
})
$(function() {
    $('#dat0').datetimepicker({
        format: 'yyyy/MM/DD hh:mm A',
        maxDate: new Date(),
        ignoreReadonly: true
    });
})
$(function() {
    $('#dat00').datetimepicker({
        format: 'yyyy/MM/DD hh:mm A',
        maxDate: new Date(),
        // minDate: $('#date0').val(),
        ignoreReadonly: true
    });
})
$(function() {
    $('#date').datetimepicker({
        format: 'yyyy/MM/DD hh:mm A',
        maxDate: new Date(),
        ignoreReadonly: true
    });
})
$(function() {
    $('#date1').datetimepicker({
        format: 'yyyy/MM/DD hh:mm A',
        maxDate: new Date(),
        ignoreReadonly: true
    });
})
$(function() {
    $('#date2').datetimepicker({
        format: 'yyyy/MM/DD hh:mm A',
        maxDate: new Date(),
        ignoreReadonly: true
    });
})
$(function() {
    $('#date3').datetimepicker({
        format: 'yyyy/MM/DD hh:mm A',
        maxDate: new Date(),
        ignoreReadonly: true
    });
})
$(function() {
    $('#date4').datetimepicker({
        format: 'yyyy/MM/DD hh:mm A',
        maxDate: new Date(),
        ignoreReadonly: true
    });
})
$(function() {
    $('#date5').datetimepicker({
        format: 'yyyy/MM/DD hh:mm A',
        maxDate: new Date(),
        ignoreReadonly: true
    });
})
$(function() {
    $('#date6').datetimepicker({
        format: 'yyyy/MM/DD hh:mm A',
        maxDate: new Date(),
        ignoreReadonly: true
    });
})
$(function() {
    $('#date7').datetimepicker({
        format: 'yyyy/MM/DD hh:mm A',
        maxDate: new Date(),
        ignoreReadonly: true
    });
})
$(function() {
    $('#date8').datetimepicker({
        format: 'yyyy/MM/DD hh:mm A',
        maxDate: new Date(),
        ignoreReadonly: true
    });
})
$(function() {
    $('#date9').datetimepicker({
        format: 'yyyy/MM/DD hh:mm A',
        maxDate: new Date(),
        ignoreReadonly: true
    });
})
$(function() {
    $('#date10').datetimepicker({
        format: 'yyyy/MM/DD hh:mm A',
        maxDate: new Date(),
        ignoreReadonly: true
    });
})
$(function() {
    $('#date11').datetimepicker({
        format: 'yyyy/MM/DD hh:mm A',
        maxDate: new Date(),
        ignoreReadonly: true
    });
})
$(function() {
    $('#date12').datetimepicker({
        format: 'yyyy/MM/DD hh:mm A',
        maxDate: new Date(),
        ignoreReadonly: true
    });
})
$(function() {
    $('#date13').datetimepicker({
        format: 'yyyy/MM/DD hh:mm A',
        maxDate: new Date(),
        ignoreReadonly: true
    });
})
$(function() {
    $('#date14').datetimepicker({
        format: 'yyyy/MM/DD hh:mm A',
        maxDate: new Date(),
        ignoreReadonly: true
    });
})
$(function() {
    $('#date15').datetimepicker({
        format: 'yyyy/MM/DD hh:mm A',
        maxDate: new Date(),
        ignoreReadonly: true
    });
})
$(function() {
    $('#date16').datetimepicker({
        format: 'yyyy/MM/DD hh:mm A',
        maxDate: new Date(),
        ignoreReadonly: true
    });
})
$(function() {
    $('#date17').datetimepicker({
        format: 'yyyy/MM/DD hh:mm A',
        maxDate: new Date(),
        ignoreReadonly: true
    });
})
$(function() {
    $('#date30').datetimepicker({
        format: 'yyyy/MM/DD hh:mm A',
        maxDate: new Date(),
        ignoreReadonly: true
    });
})
$(function() {
    $('#date31').datetimepicker({
        format: 'yyyy/MM/DD hh:mm A',
        maxDate: new Date(),
        ignoreReadonly: true
    });
})