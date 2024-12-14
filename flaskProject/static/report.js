document.getElementById('report').addEventListener('click', function() {
    var table = document.getElementById('table3').cloneNode(true);
    // Convert dates and account numbers to strings
    for (var i = 0, row; row = table.rows[i]; i++) {
        for (var j = 0, cell; cell = row.cells[j]; j++) {
            if (j == 3) { // Assuming the date is in the 2nd column and the account number is in the 4th column
                cell.textContent = "'" + cell.textContent;
            }
        }
    }
    var wb = XLSX.utils.book_new();
    var ws = XLSX.utils.table_to_sheet(table);
    XLSX.utils.book_append_sheet(wb, ws, "Report");
    XLSX.writeFile(wb, "report.xlsx");


});
