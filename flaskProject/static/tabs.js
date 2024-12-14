function openTab(tabId) {
    // Скрыть все вкладки
    var i, tabcontent;
    tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Отобразить выбранную вкладку
    document.getElementById(tabId).style.display = "block";
}
