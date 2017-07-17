function updateModules(newValue, oldValue) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var editorSheet = ss.getSheetByName("Editor");
  var moduleSheet = ss.getSheetByName("Module");

  var moduleRange = moduleSheet.getRange(1, 1, 2, 7);

  if (newValue > oldValue) {
    addRows(editorSheet, moduleRange, oldValue, newValue);
    setRowNumbers(editorSheet, newValue);
  } else if (newValue < oldValue) {
    removeRows(editorSheet, newValue, oldValue);
  }
}

function setRowNumbers(sheet, rowCount) {
  var rowsFound = 0;
  var currentRow = 7;

  while(rowsFound < rowCount) {
    var range = sheet.getRange(currentRow, 2, 1, 1);
    if (range.getValue() == "Module Type") {
      rowsFound++;
      sheet.getRange(currentRow, 1, 1, 1).setValue(rowsFound);
    }
    currentRow++;
  }
}

function addRows(editorSheet, moduleRange, oldValue, newValue) {
  var rowsFound = 0;
  var startingRow = 7;

  while (rowsFound < oldValue) {
    var tempRange = editorSheet.getRange(startingRow, 7, 1, 1);
    if (tempRange.getValue() == "Number of CTAs") {
      startingRow += parseInt(editorSheet.getRange(startingRow + 1, 7, 1, 1).getValue() * 2);
      startingRow += 2;
      rowsFound++;
    }
    startingRow++;
  }

  for (var i = 0; i < newValue - oldValue; i++) {
    var range = editorSheet.getRange(startingRow + (i * 3), 1, 3, 7);
    editorSheet.setRowHeight(startingRow + (i * 3), 100);
    moduleRange.copyTo(range);
  }
}

function removeRows(editorSheet, smallerNum, largerNum) {

  var firstRow = 0;
  var index = 7;
  while (firstRow == 0 || index == 100) {
    if (parseInt(editorSheet.getRange(index, 1, 1, 1).getValue()) == smallerNum + 1) {
      firstRow = index + 1;
    }
    index++;
  }

  for (var i = 0; i < largerNum - smallerNum; i++) {
    var ctaNum = parseInt(editorSheet.getRange(firstRow + (i * 3), 7, 1, 1).getValue());
    if (ctaNum > 0) {
      removeCTAs (editorSheet, ctaNum, ctaNum, firstRow + (i * 3));
    }
  }
  for (var i = largerNum - smallerNum - 1; i >= 0; i--) {
    var range = editorSheet.getRange(firstRow - 1 + (3 * i), 1, 2, 7);
    range.clear();
    range.setDataValidation(null);
    editorSheet.setRowHeight(firstRow - 1 + (3 * i), 21);
    editorSheet.setRowHeight(firstRow + (3 * i), 21);
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
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var editorSheet = ss.getSheetByName("Editor");

  if (e.range.getRow() === 3 && e.range.getColumn() === 2) {
    updateModules(parseInt(e.value), parseInt(e.oldValue));
  }

  if (e.range.getColumn() === 7) {
    updateCTA(parseInt(e.value), parseInt(e.oldValue), parseInt(e.range.getRow()));
  }
}

function genericTester() {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
  var editorSheet = ss.getSheetByName("Editor");
  var moduleSheet = ss.getSheetByName("Module");

  var moduleRange = moduleSheet.getRange(1, 1, 2, 7);
  addRows(editorSheet, moduleRange, 5, 7) ;
}
