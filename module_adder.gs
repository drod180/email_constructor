function addModules(newValue, oldValue) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var editorSheet = ss.getSheetByName("Editor");
  var moduleSheet = ss.getSheetByName("Module");

  var moduleRange = moduleSheet.getRange(1, 1, 4, 7);
  var value = editorSheet.getRange(3,2).getValue();

  if (newValue > oldValue) {
    for (var i = oldValue; i < newValue; i++) {
      addRows(editorSheet,  moduleRange, i);
    }
  } else if (newValue < oldValue) {
    removeRows(editorSheet, newValue, oldValue);
  }

  setRowNumbers(editorSheet, newValue);
}

function setRowNumbers(sheet, rowCount) {
  for (var i = 0; i < rowCount; i++) {
    var range = sheet.getRange(7 + ((4 + 1) * i), 1, 1, 1);
    range.setValue(i + 1);
  }
}

function addRows(editorSheet, moduleRange, moduleNum) {
  var range = editorSheet.getRange(7 + ((4 + 1) * moduleNum), 1, 5, 7);
  editorSheet.setRowHeight(8 + ((4 + 1) * moduleNum), 100);
  moduleRange.copyTo(range);

  editorSheet.getRange(7 + ((4 + 1) * moduleNum), 1, 1, 1).setValue(Math.round(moduleNum + 1));
}

function removeRows(editorSheet, end, start) {
  for (var i = start; i >= end; i--) {
    var range = editorSheet.getRange(7 + ((4 + 1) * i), 1, 5, 7);
    range.clear();
    range.setDataValidation(null);
    editorSheet.setRowHeight(7 + ((4 + 1) * i), 21);
    editorSheet.setRowHeight(8 + ((4 + 1) * i), 21);
    editorSheet.setRowHeight(9 + ((4 + 1) * i), 21);
    editorSheet.setRowHeight(10 + ((4 + 1) * i), 21);
  }
}


function onEdit(e) {

  if (e.range.getRow() === 3 && e.range.getColumn() === 2) {
    addModules(e.value, e.oldValue);
  }

}
