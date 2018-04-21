/**
 * Created by chenquan on 2018/4/21.
 */
const randomBox = $('#random-box');
if (randomBox) {
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
    const allStudents = [];
    let i0 = 0;
    $.each(data.data.allstus, (index,stu) => {
      allStudents.push([index, stu.key, stu.value]);
      index += 1
      $('#all-stu-table').append(`<tr><td> ${index} </td><td>${stu.key}</htd><td>${stu.value}</td></tr>`);
    });
    // lucky students
    // needs animation effects
    const luckyStudents = [];
    $.each(data.data.studs, (idx, weight) => {
      luckyStudents.push([idx, weight]);
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
        console.log(ele);
        c1 += 1;
        $('#lucky-stu-table').append(`<tr><td> ${c1} </td><td>${ele[1]}</td></tr>`);
        if (luckyStudents.length === 0) {
          clearInterval(effectIntervalId);
          randomSpan.html('');
        }
      }
      c2 += 1;
      randomSpan.html(allStudents[c2 % allStudents.length][1]);
    }, 50);
  }).fail((err) => {
    console.warn(err);
  });
}
