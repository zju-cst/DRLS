/**
 * Created by chenquan on 2018/4/21.
 */
const randomBox = $('#random-box');
if (randomBox && randomBox.length > 0) {
  console.log(randomBox);
  $.ajax({
    url: '/rand/',
    type: 'POST',
    chache: false,
    data: new FormData($('#rand-form')[0]),
    processData: false,
    contentType: false,
  }).done((data) => {
    // because allstus is a object, we need a indicator to
    // get the index

    if (data.code === 0) {
      const allStudents = [];
      $.each(data.data.allstus, (index, stu) => {
        allStudents.push([index, stu.key, stu.value]);
        index += 1;
        $('#all-stu-table').append(`<tr><th scope="row"> ${index} </th><td>${stu.key}</htd><td>${stu.value}</td></tr>`);
      });
          // lucky students
          // needs animation effects
      const luckyStudents = [];
      $.each(data.data.studs, (idx, ele) => {
        luckyStudents.push([idx, ele]);
      });

      let c1 = 0;
      let c2 = 0;
      const randomSpan = $('.random-span');
      const effectIntervalId = setInterval(() => {
        if (c2 >= allStudents.length) {
          c2 = 0;
        }
        if (c2 % 10 === 6) {
          const ele = luckyStudents.pop();
          c1 += 1;
          $('#lucky-stu-table').append(`<tr><th scope="row"> ${c1} </th><td>${(ele[1] +'').trim()}</td></tr>`);
          if (luckyStudents.length === 0) {
            clearInterval(effectIntervalId);
            randomSpan.val('');
          }
        }
        c2 += 1;
        randomSpan.val(allStudents[c2 % allStudents.length][1]);
      }, 50);
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
}
