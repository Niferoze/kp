$(document).ready(function() {
  $('#export').click(function() {
    // Отправка запроса на сервер без выбора пути
    $.post('/export')
      .done(function(response) {
      })
      .fail(function(error) {
      });
  });
});