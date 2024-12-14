// Обработчик для кнопки "Импорт"
document.getElementById("import").addEventListener("click", function() {
    // Активируем скрытое поле выбора файла
    document.getElementById('fileInput').click();
});

// Обработка выбора файла
document.getElementById('fileInput').addEventListener('change', function(event) {
    var file = event.target.files[0];
    if (file) {
        var formData = new FormData();
        formData.append('file', file);

        $.ajax({
            url: '/import',
            method: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function() {
                alert('Данные успешно импортированы!');
            },
            error: function() {
                alert('Ошибка при импорте данных');
            }
        });
    } else {
        alert('Выберите файл для импорта');
    }
});

// Обработчик для кнопки "Экспорт"
document.getElementById("export").addEventListener("click", function() {
    $.ajax({
        url: '/export',
        method: 'POST',
        success: function(data) {
            // Создаём ссылки для скачивания каждого файла
            data.files.forEach(function(fileUrl) {
                const link = document.createElement('a');
                link.href = fileUrl;
                link.download = fileUrl.split('/').pop(); // Извлекаем имя файла из URL
                document.body.appendChild(link);
                link.click(); // Программно кликаем по ссылке для инициирования скачивания
                document.body.removeChild(link); // Убираем ссылку из DOM
            });
            alert('Экспорт завершен. Файлы загружены.');
        },
        error: function() {
            alert('Ошибка при экспорте данных');
        }
    });
});