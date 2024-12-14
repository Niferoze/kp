window.onload = function () {
    var table = document.getElementById("table3"); // Получите таблицу по id
    makeSortable(table); // Сделайте эту таблицу сортируемой
};

function makeSortable(table) {
    var th = table.getElementsByTagName("th"), i;
    if (th) i = th.length;
    else return; // если нет, то ничего не делаем
    while (--i >= 0) (function (i) {
        var dir = 1;
        th[i].addEventListener('click', function () {sortTable(table, i, (dir = 1 - dir))});
    }(i));
}

function sortTable(table, col, reverse) {
    var tb = table.tBodies[0], // используем только тело таблицы (содержимое)
        tr = Array.prototype.slice.call(tb.rows, 0), // все строки
        i;
    reverse = -((+reverse) || -1);
    tr = tr.sort(function (a, b) { // сортировка строк
        return reverse * (a.cells[col].textContent.trim() // используем данные ячейки
                             .localeCompare(b.cells[col].textContent.trim(), undefined, {numeric: true, sensitivity: 'base'}))
    });
    for(i = 0; i < tr.length; ++i) tb.appendChild(tr[i]); // добавляем строки в таблицу
}
