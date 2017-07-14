function updateModules(newValue, oldValue) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var editorSheet = ss.getSheetByName("Editor");
  var moduleSheet = ss.getSheetByName("Module");

  var moduleRange = moduleSheet.getRange(1, 1, 2, 7);

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
    var range = sheet.getRange(7 + (3 * i), 1, 1, 1);
    range.setValue(i + 1);
  }
}

function addRows(editorSheet, moduleRange, moduleNum) {
  var range = editorSheet.getRange(7 + (3 * moduleNum), 1, 3, 7);
  editorSheet.setRowHeight(8 + (3 * moduleNum), 100);
  moduleRange.copyTo(range);

  editorSheet.getRange(7 + (3 * moduleNum), 1, 1, 1).setValue(Math.round(moduleNum + 1));
}

function removeRows(editorSheet, end, start) {
  for (var i = start; i >= end; i--) {
    var ctaNum = editorSheet.getRange(7 + (3 * i) + 1, 7, 1, 1).getValue();
    var range = editorSheet.getRange(7 + (3 * i), 1, 3, 7);
    editorSheet.getRange(7 + (3 * i) + 1, 9, 1, 1).setValue(ctaNum);
  //  removeCTAs(editorSheet, ctaNum,ctaNum, (7 + (3 * i) + 1));
  //  range.clear();
 //   range.setDataValidation(null);
 //   editorSheet.setRowHeight(7 + (3 * i), 21);
  //  editorSheet.setRowHeight(8 + (3 * i), 21);
  }
}

function updateCTA(newValue, oldValue, row) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var editorSheet = ss.getSheetByName("Editor");
  var moduleSheet = ss.getSheetByName("Module");

  var ctaRange = moduleSheet.getRange(3, 1, 2, 7);

  if (newValue > oldValue) {
    for (var i = oldValue; i < newValue; i++) {
      addCTA(editorSheet,  ctaRange, row, i);
    }
  } else if (newValue < oldValue) {
    removeCTAs(editorSheet, oldValue - newValue, oldValue, row);
  }
}

function addCTA (sheet, ctaRange, rowNum, ctaNum) {
  sheet.insertRowAfter(rowNum + (ctaNum * 2));
  sheet.insertRowAfter(rowNum + (ctaNum * 2));
  var range = sheet.getRange(rowNum + (ctaNum * 2) + 1, 1, 2, 7);
  ctaRange.copyTo(range);
  sheet.setRowHeight(rowNum + (ctaNum * 2) + 1, 28);
  sheet.setRowHeight(rowNum + (ctaNum * 2) + 2, 32);
}

function removeCTAs (sheet, amount, ctaCount, rowNum) {
  sheet.deleteRows(rowNum + 1 + (ctaCount - amount) * 2, amount * 2);
}

function onEdit(e) {
  if (e.range.getRow() === 3 && e.range.getColumn() === 2) {
    updateModules(e.value, e.oldValue);
  }

  if (e.range.getColumn() === 7) {
    updateCTA(e.value, e.oldValue, e.range.getRow());
  }
}
