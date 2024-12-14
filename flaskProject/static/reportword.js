document.getElementById('reportword').addEventListener('click', function() {
    const { Document, Packer, Paragraph, Table, TableCell, TableRow } = window.docx;



    // Извлеките данные из таблицы table3
    const tableElement = document.getElementById('table3');
    const rows = tableElement.querySelectorAll('tbody tr');

    // Создайте массив для хранения строк таблицы
    const tableRows = [];
    let totalSum = 0;
    let totalBalance = 0;

    // Добавьте заголовки столбцов
    const headerCells = tableElement.querySelectorAll('th');
    const headerRow = new TableRow({
        children: Array.from(headerCells).map(cell => new TableCell({
            children: [new Paragraph(cell.textContent)],
            width: { size: 2000, type: 'dxa' } // Установите ширину ячеек по вашему усмотрению
        }))
    });
    tableRows.push(headerRow); // Добавляем заголовки в массив строк таблицы

    // Обработайте каждую строку таблицы
    rows.forEach(row => {
        const cells = row.querySelectorAll('td'); // Получить все ячейки
        const rowData = [];

        const transactionAmount = parseFloat(cells[2].textContent) || 0; // "Сумма транзакции"
        const balance = parseFloat(cells[6].textContent) || 0; // "Остаток"

        // Суммируем значения
        totalSum += transactionAmount;
        totalBalance += balance;

        cells.forEach(cell => {
            rowData.push(new TableCell({
                children: [new Paragraph(cell.textContent)]
            }));
        });

        // Добавьте строку в массив
        tableRows.push(new TableRow({
            children: rowData
        }));
    });

    // Создайте таблицу из массива строк
    const table = new Table({
        rows: tableRows,
    });

    // Добавьте таблицу и итоги в одну секцию
     const doc = new Document({
        sections: [{
            properties: {},
            children: [
            table,
            new Paragraph("Итоги:"),
            new Paragraph(`Общая сумма транзакций: ${totalSum.toFixed(2)}`),
            new Paragraph(`Общий остаток: ${totalBalance.toFixed(2)}`)
            ],
        }],
    });

    // Сохраните документ
    Packer.toBlob(doc).then(blob => {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'report.docx';
        a.click();
        URL.revokeObjectURL(url);
    });
});