function feedinginfos() {
    var container = document.getElementById('recents');
    var border = document.getElementById('border');
    var table = document.getElementById('feedinginfos');
    var table2 = document.getElementById('food_inventorys')

    if (container.hidden == true || container.hidden == false) {
        border.classList.toggle("border");
        container.hidden = false;
        table.hidden = false;
        table2.hidden = true;

    }
}

function feed_inventorys() {
    var container = document.getElementById('recents');
    var border = document.getElementById('border');
    var table = document.getElementById('food_inventorys');
    var table2 = document.getElementById('feedinginfos');

    if (container.hidden == true || container.hidden == false) {
        container.hidden = false;
        border.classList.add("border");
        table.hidden = false;
        table2.hidden = true;
    }
}

function milkcollections() {
    var container = document.getElementById('recents');
    var table = document.getElementById('milkcollections');
    var border = document.getElementById('border');
    var table2 = document.getElementById('milksales');
    var table3 = document.getElementById('unservedmilksales');

    if (container.hidden == true || container.hidden == false) {
        container.hidden = false;
        border.classList.add("border");
        table3.hidden = true;
        table.hidden = false;
        table2.hidden = true;
    }
}

function milksales() {
    var container = document.getElementById('recents');
    var table = document.getElementById('milksales');
    var border = document.getElementById('border');
    var table3 = document.getElementById('unservedmilksales');
    var table2 = document.getElementById('milkcollections');

    if (container.hidden == true || container.hidden == false) {
        container.hidden = false;
        border.classList.add("border");
        table.hidden = false;
        table3.hidden = true;
        table2.hidden = true;
    }
}

function unservedmilksales() {
    var container = document.getElementById('recents');
    var table = document.getElementById('milksales');
    var table3 = document.getElementById('unservedmilksales');
    var border = document.getElementById('border');
    var table2 = document.getElementById('milkcollections');

    if (container.hidden == true || container.hidden == false) {
        container.hidden = false;
        border.classList.add("border");
        table.hidden = true;
        table3.hidden = false;
        table2.hidden = true;
    }
}

function inseminationss() {
    var container = document.getElementById('recents');
    var table = document.getElementById('inseminationss');
    var border = document.getElementById('border');
    var table2 = document.getElementById('calvings');
    table3 = document.getElementById('deaths')

    if (container.hidden == true || container.hidden == false) {
        container.hidden = false;
        border.classList.add("border");
        table.hidden = false;
        table2.hidden = true;
        table3.hidden = true;
    }
}

function calvings() {
    var container = document.getElementById('recents');
    var table = document.getElementById('calvings');
    var border = document.getElementById('border');
    var table2 = document.getElementById('deaths');
    var table3 = document.getElementById('inseminations')

    if (container.hidden == true || container.hidden == false) {
        container.hidden = false;
        border.classList.add("border");
        table.hidden = false;
        table2.hidden = true;
        table3.hidden = true
    }
}

function deaths() {
    var container = document.getElementById('recents');
    var table = document.getElementById('deaths');
    var border = document.getElementById('border');
    var table2 = document.getElementById('calvings');
    var table3 = document.getElementById('inseminations')

    if (container.hidden == true || container.hidden == false) {
        container.hidden = false;
        table.hidden = false;
        border.classList.add("border");
        table2.hidden = true;
        table3.hidden = true;
    }
}

function vaccines() {
    var container = document.getElementById('recents');
    var table = document.getElementById('vaccines');
    var border = document.getElementById('border');
    var table2 = document.getElementById('healths');

    if (container.hidden == true || container.hidden == false) {
        container.hidden = false;
        border.classList.add("border");
        table.hidden = false;
        table2.hidden = true;
    }
}

function healths() {
    var container = document.getElementById('recents');
    var table = document.getElementById('healths');
    var border = document.getElementById('border');
    var table2 = document.getElementById('vaccines');

    if (container.hidden == true || container.hidden == false) {
        container.hidden = false;
        table.hidden = false;
        border.classList.add("border");
        table2.hidden = true;
    }
}

function cowinfos() {
    var container = document.getElementById('recents');
    var table = document.getElementById('cowinfos');
    var border = document.getElementById('border');

    if (container.hidden == true || container.hidden == false) {
        container.hidden = false;
        border.classList.add("border");
        table.hidden = false;
    }
}

function hide() {
    var container = document.getElementById('recents');
    var border = document.getElementById('border');
    if (container.hidden == true || container.hidden == false) {
        border.classList.toggle("border");
        container.hidden = true;

    }
}