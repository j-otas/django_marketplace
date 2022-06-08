function setEventEnterOnInputs($a){
    $a.on("keypress", "input", function(e){
        if(e.which == 13){
            event.preventDefault();
            $a.find("button").click();
        }
    });
}

$('body').on('click', '#show_change_modal', function (event) { //Кнопка "Редактировать"
    let $form = $(event.currentTarget).parent();
    var edit_form = $("#edit_form");
    $.ajax({
        url: $('button[name="send_object_data"]').data("data-url"),
        type: "POST",
        data: $form.serialize(),
        dataType: "html",

        success: function (response) {
            $("#modal_window").html(JSON.parse(response)['result']);
            $('#exampleModal').modal("show");
            setEventEnterOnInputs($("#exampleModal"));
        }
    });
});
$('body').on('click', '#acceptButton', function (event) { //Кнопка отправки формы "Принять изменения"
    let $form = $('#edit_form');
    $.ajax({
        url: '/admin_panel/accept_data',
        type: "POST",
        data: $form.serialize(),
        dataType: "html",

        success: function (response) {
            $("#table_block").html(JSON.parse(response)['result']);
            $('#exampleModal').modal("hide");
        }
    });
});
$('body').on('click', '#deleteButton', function (event) { //Кнопка "Удалить"
    let $form = $(event.currentTarget).parent();
    $.ajax({
        url: $('button[name="deleteButton"]').attr('data-url'),
        type: "POST",
        data: $form.serialize(),
        dataType: "html",

        success: function (response) {
            $("#table_block").html(JSON.parse(response)['result']);
        }
    });
});
$('body').on('click', '#addButton', function (event) { //Кнопка добавить объект
    let $form = $(event.currentTarget).parent();
    $.ajax({
        url: $('#addButton').attr('data-url'),
        type: "POST",
        data: $form.serialize(),
        dataType: "html",

        success: function (response) {
            $("#modal_add_window").html(JSON.parse(response)['result']);
            $('#addModal').modal("show");
            setEventEnterOnInputs($("#modal_add_window"));


        }
    });
});
$("body").on('click', '#acceptAddButton', function (event) {
    let $form = $('#add_form');
    $.ajax({
        url: $('#acceptAddButton').attr('data-url'),
        type: "POST",
        data: $form.serialize(),
        dataType: "html",

        success: function (response) {
            if (JSON.parse(response)['errors']) {
                //$("#addModal").modal('hide').on('hidden.bs.modal', functionThatEndsUpDestroyingTheDOM);
                $('.modal-backdrop').remove();
                $("#modal_add_window").html(JSON.parse(response)['result']);
                $('#addModal').modal("show");


            } else {

                $('.table_block').html(JSON.parse(response)['result']);
                $('#addModal').modal("hide");
            }


        }
    });
});

$('body').on('click', '#set_role_btn', function (event) { //Кнопка "Установить роль"
    let $form = $(event.currentTarget).closest("form");
    $.ajax({
        type: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        url: $(this).attr("data-url"),
        data: $form.serialize(),
        dataType: "html",

        success: function (response) {
            $('.table_block').html(JSON.parse(response)['result']);
        },
        failed: function () {
            console.log('ajax FAILED!');
        }
    });
});


$('.search_user_input').on('keyup', function(){
    //Продолжить отсюда, начать с отправки запроса и выполнения поиска
});




function accept_product(pk) {
    $.ajax({
        url: $('.accept_product_button').attr('data-url'),

        success: function (data) {
            $('.accept_product_button').parent().parent('#product_block-'+pk).remove()
        },
        failed: function () {
            console.log('ajax FAILED!');
        }
    });
}

function cancel_product(pk) {
    $.ajax({
        url: $('.cancel_product_button').attr('data-url'),

        success: function (data) {
            $('.cancel_product_button').parent().parent('#product_block-'+pk).remove()
        },
        failed: function () {
            console.log('ajax FAILED!');
        }
    });
}

function accept_user(pk) {
    $.ajax({
        url: $('.accept_user_button').attr('data-url'),

        success: function (data) {
            $('.accept_user_button').parent().parent('#user_block-'+pk).remove()
        },
        failed: function () {
            console.log('ajax FAILED!');
        }
    });
}

function cancel_user(pk) {
    $.ajax({
        url: $('.cancel_user_button').attr('data-url'),

        success: function (data) {
            $('.cancel_user_button').parent().parent('#user_block-'+pk).remove()
        },
        failed: function () {
            console.log('ajax FAILED!');
        }
    });
}




