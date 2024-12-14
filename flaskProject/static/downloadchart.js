// Получите ссылку на кнопку скачивания
var download = document.getElementById('DownloadChart');

// Добавьте обработчик события клика на кнопку
download.addEventListener('click', function() {
    // Создайте изображение из графика с помощью библиотеки html2canvas
    html2canvas(document.getElementById('myChart')).then(function(canvas) {
        // Преобразуйте изображение в формате base64 в blob-объект
        var dataURL = canvas.toDataURL();
        var blob = dataURLToBlob(dataURL);

        // Создайте ссылку для скачивания blob-объекта
        var url = window.URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = 'График.png';

        // Имитируйте клик по ссылке и удалите ее
        document.body.appendChild(a);
        a.click();
        a.remove();
    });
});

// Функция для преобразования base64 в blob
function dataURLToBlob(dataURL) {
    var parts = dataURL.split(';base64,');
    var contentType = parts[0].split(":")[1];
    var raw = window.atob(parts[1]);
    var rawLength = raw.length;
    var uInt8Array = new Uint8Array(rawLength);
    for (var i = 0; i < rawLength; ++i) {
        uInt8Array[i] = raw.charCodeAt(i);
    }
    return new Blob([uInt8Array], {type: contentType});
}
