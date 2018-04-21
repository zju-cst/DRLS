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
      console.log(data);
    }
  }).fail((err) => {
    console.warn(err);
  });
});
