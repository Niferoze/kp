
document.getElementById('reportchart').addEventListener('click', function() {
    // Получите данные из таблицы
    var dates = []; // Даты
    var balances = []; // Остатки
    var table = document.getElementById('table3');
    for (var i = 1, row; row = table.rows[i]; i++) {
        dates.push(row.cells[1].innerHTML); // Дата - вторая колонка
        balances.push(row.cells[6].innerHTML); // Остаток - седьмая колонка
    }

    // Создайте график
    var ctx = document.getElementById('myChart').getContext('2d');
    var chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: 'Остаток',
                data: balances,
                fill: false,
                borderColor: 'rgb(255, 0, 0)',
                tension: 0.1
            }]
        }
    });
    document.getElementById('chartContainer').style.display = 'block';

});
