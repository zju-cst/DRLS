$('#file-upload').on('change', () => {
  $.ajax({
    url: '/upload/',
    type: 'POST',
    chache: false,
    data: new FormData($('#upload-form')[0]),
    processData: false,
    contentType: false,
  }).done((data) => {
    $('#upload-form')[0].reset();
    console.log(data);
    if (data && data.code === 0) {
      window.location.replace('/random/');
    } else {
      $('.warn-code').html(data.code);
      $('.warn-msg').html(data.msg);
      $('#warn-modal').modal();
    }
  }).fail((err) => {
    $('.warn-code').html(9999);
    const msg = err || 'internal system error';
    $('.warn-msg').html(msg);
    $('#warn-modal').modal();
  });
});
