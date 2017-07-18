
function saveAsCSVFile () {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var editorSheet = ss.getSheetByName("Editor");
  var emailName = editorSheet.getRange(2,2,1,1).getValue().toLowerCase().replace(/ /g,'_') + '_csv_';
  var folders = DriveApp.getFoldersByName("Constructor_Emails");

  var projectFolder = setupDirectory_(folders, emailName);

  var scriptsI = projectFolder.getFoldersByName("scripts");
  var scripts = scriptsI.next();
  var csvFile = convertRangeToCsvFile_(emailName + ".csv", editorSheet);
  scripts.addFile(csvFile);
}

function setupDirectory_(folders, emailName) {
  if (folders.hasNext()) {
    var constructFolder = folders.next();
    var eFolders = constructFolder.getFolders();

    while (eFolders.hasNext()) {
      var eFolder = eFolders.next();
      if (eFolder.getName() == "email-template") {
        var template = eFolder;
      }

      if (eFolder.getName() == emailName) {
         return eFolder;
      }
    }
  }

  return buildFolder_(constructFolder, emailName, template, true);
}

// Copies the files and folders
function copyFolder_(source, desitation) {
  var dir;
  var newdir;

  copyFiles_(source, desitation)

  var dirs = source.getFolders();
  while(dirs.hasNext()) {
    dir = dirs.next();
    newdir = desitation.createFolder(dir.getName());
    copyFolder_(dir, newdir);
  }
};

// Copies the files from sfolder to dfolder
function copyFiles_(source, desitation) {
  var files = source.getFiles();
  var file;
  var fname;

  while(files.hasNext()) {
    file = files.next();
    fname = file.getName();
    file.makeCopy(fname, desitation);
  }
};

function buildFolder_(folder, name, template, isNew) {
  if (isNew) {
    var newFolder = folder.createFolder(name);
    var templateFolders = template.getFolders();
    copyFolder_(template, newFolder);
  }
  return newFolder;
}


function convertRangeToCsvFile_(csvFileName, sheet) {
  // get available data range in the spreadsheet
  var activeRange = sheet.getDataRange();
  try {
    var data = activeRange.getValues();
    var csvFile = undefined;

    // loop through the data in the range and build a string with the csv data
    if (data.length > 1) {
      var csv = "";
      for (var row = 0; row < data.length; row++) {
        for (var col = 0; col < data[row].length; col++) {
          if (data[row][col].toString().indexOf(",") != -1) {
            data[row][col] = "\"" + data[row][col] + "\"";
          }
        }

        // join each row's columns
        // add a carriage return to end of each row, except for the last one
        if (row < data.length-1) {
          csv += data[row].join(",") + "\r\n";
        }
        else {
          csv += data[row];
        }
      }
      csvFile = DriveApp.createFile(csvFileName,csv);
    }
    return csvFile;
  }
  catch(err) {
    Logger.log(err);
    Browser.msgBox(err);
  }
}

function onOpen() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var csvMenuEntries = [{name: "[Dan]Export CSV", functionName: "saveAsCSVFile"}];
  ss.addMenu("Custom", csvMenuEntries);
};
