$(document).ready(function() {
    // Обработка нажатия кнопки "Submit"
    $('#submit').click(function() {
        // Получение данных из таблицы
        var data = [];
        $('#table1 tr').each(function() {
            var row = [];
            $(this).find('td:not(:has(:button))').each(function() {
                row.push($(this).text());
            });
            data.push(row);
        });

        // Отправка данных на сервер
        $.ajax({
            url: '/update',
            method: 'POST',
            data: JSON.stringify(data),
            contentType: 'application/json',
            success: function() {
                alert('Данные успешно обновлены!');
            }
        });
    });
});

$(document).ready(function() {
    // Обработка нажатия кнопки "Удалить"
    $('.delete').click(function() {
        // Получение данных из строки
        var row = [];
        $(this).closest('tr').find('td:not(:has(:button))').each(function() {
            row.push($(this).text());
        });

        // Отправка данных на сервер
        $.ajax({
            url: '/delete',
            method: 'POST',
            data: JSON.stringify(row),
            contentType: 'application/json',
            success: function() {
                alert('Строка успешно удалена!');
            }
        });

        // Удаление строки из таблицы
        $(this).closest('tr').remove();
    });
});
$(document).ready(function() {
    // Существующий код

    // Обработка нажатия кнопки "Добавить"
    $('#add').click(function() {
        // Открытие модального окна для ввода данных
        openModal();
    });

    // Обработка нажатия кнопки "Добавить" в модальном окне
    $('#dataForm button[type="button"]').click(function() {
        // Получение данных из формы
        var sum = $('input[name="amount"]').val();
        var typeid = $('select[name="transactionType"]').val();

        // Проверка на наличие данных
        if (!sum || !typeid) {
            alert("Пожалуйста, заполните все поля.");
            return;
        }

        // Создание новой строки с введенными данными и текущей датой
        var row = $('<tr>');
        row.append('<td contenteditable="false">' + new Date().toISOString().slice(0, 10) + '</td>'); // Дата
        row.append('<td contenteditable="false">' + sum + '</td>'); // Сумма
        row.append('<td contenteditable="false">' + typeid + '</td>'); // Тип операции
        row.append('<td contenteditable="false"></td>'); // Номер счёта
        row.append('<td contenteditable="false"></td>'); // Orgid
        row.append('<td><button class="delete button">Удалить</button></td>');

        // Добавление строки в таблицу
        $('#table1 tbody').append(row);

        // Отправка данных на сервер
        var data = [new Date().toISOString().slice(0, 10), sum, typeid];
        $.ajax({
            url: '/add',
            method: 'POST',
            data: JSON.stringify(data),
            contentType: 'application/json',
            success: function() {
                closeModal(); // Закрытие модального окна
                location.reload(); // Перезагрузка страницы для обновления данных
                alert('Строка успешно добавлена!');
            },
            error: function() {
                alert('Ошибка при добавлении строки.');
            }
        });
    });
});



