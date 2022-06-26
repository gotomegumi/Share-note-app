$(function(){
    $('.delete').click(function(){
        $('#cover, #confirm-modal, .modal-wrap').show();
        var id = $(this).val();
        $('#id').val(id);
    })
    $('#cover, .confirm-cancel').click(function(){
        $('#confirm-modal, #cover, #update-modal, .modal-wrap').hide();
    })
    $('#yes').click(function(){
        $('.send-delete').attr('action', '/delete');
        $('.send-delete').submit();
    })

    $('.name-edit, .data-edit').click(function(){
        $('#cover, #update-modal, .modal-wrap').show();
        var id = $(this).val();
        var title = $(this).parents('.note').find('.note-name-wrap').find('.note-name').text();
        var data = $(this).find('a').text();
        $('#title-update').val(title);
        $('#data-update').text(data);
        $('#id2').val(id)
    })
})