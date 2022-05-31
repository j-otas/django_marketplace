function put_favorite(pk) {
    $.ajax({
        url: $('.add_favorite').attr('data-url'),

        success: function (response) {
            if (response.result) {
                $('.favorite_block').html(response.result);
            }
        }
    });
}


function delete_favorite(pk) {
    $.ajax({
        url: $('.delete_favorite').attr('data-url'),

        success: function (response) {
            if (response.result) {
                $('.favorite_block').html(response.result);
            }
        }
    });
}
function delete_favorite_list(pk) {
    $.ajax({
        url: $('.favorit_list_delete-'+pk).attr('data-url'),

        success: function (response) {
            if (response.result) {
                $('.favorite_products_container').html(response.result);
            }
        }
    });
}