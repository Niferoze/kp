$(document).ready(function() {
    // Обработка нажатия кнопки "Submit"
    $('#submitUser').click(function() {
        // Получение данных из таблицы
        var data = [];
        $('#table2 tr').each(function() {
            var row = [];
            $(this).find('td:not(:has(:button))').each(function() {
                row.push($(this).text());
            });
            data.push(row);
        });

        // Отправка данных на сервер
        $.ajax({
            url: '/updateUser',
            method: 'POST',
            data: JSON.stringify(data),
            contentType: 'application/json',
            success: function() {
                alert('Данные успешно обновлены!');
            }
        });
    });

    // Обработка нажатия кнопки "Удалить"
    $(document).on('click', '.deleteUser', function() {
        // Получение данных из строки
        var row = [];
        $(this).closest('tr').find('td:not(:has(:button))').each(function() {
            row.push($(this).text());
        });

        // Отправка данных на сервер
        $.ajax({
            url: '/deleteUser',
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

    // Обработка нажатия кнопки "Добавить"
    $('#addUser').click(function() {
        openUserModal(); // Открытие модального окна
    });
});

// Функция открытия модального окна для добавления пользователя
function openUserModal() {
    document.getElementById("myUserModal").style.display = "block";
}

// Функция закрытия модального окна
function closeUserModal() {
    document.getElementById("myUserModal").style.display = "none";
}

// Функция добавления данных пользователя
function addUserData() {
    const form = document.getElementById('userForm');
    const formData = new FormData(form);
    const email = formData.get('email');
    const password = formData.get('password');

    // Создание новой строки с введенными данными
    var row = $('<tr>');
    row.append('<td contenteditable="false"></td>')
    row.append('<td contenteditable="false">' + email + '</td>'); // Email
    row.append('<td contenteditable="false">' + password + '</td>'); // Password
    row.append('<td><button class="deleteUser button">Удалить</button></td>');

    // Добавление строки в таблицу
    $('#table2 tbody').append(row);
    closeUserModal();

    // Отправка данных на сервер
    var data = [email, password];
    $.ajax({
        url: '/addUser',
        method: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function() {
            alert('Пользователь успешно добавлен!');
            location.reload();
        }
    });
}