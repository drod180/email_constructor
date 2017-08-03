function downloadAsCsvFile() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var editorSheet = ss.getSheetByName("Editor");
  ContentService.createTextOutput(editorSheet)
                .downloadAsFile("MyData.csv")
                .setMimeType(ContentService.MimeType.CSV);
}

function saveAsCSVFile () {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var editorSheet = ss.getSheetByName("Editor");
  var emailName = editorSheet.getRange(2,2,1,1).getValue().toLowerCase().replace(/ /g,'_') + 'EC_';
  var folders = DriveApp.getFoldersByName("Constructor_Emails");

  var projectFolder = setupDirectory_(folders, emailName);

  var scriptsI = projectFolder.getFoldersByName("scripts");
  var scripts = scriptsI.next();
  var csvFile = convertRangeToCsvFile_("constructedEmail_.csv", editorSheet);

  var duplicateCSVs = scripts.getFilesByName("constructedEmail_.csv");
  while (duplicateCSVs.hasNext()) {
    var file = duplicateCSVs.next();
    file.setTrashed(true);
  }

  scripts.addFile(csvFile);
  promptDownload_(projectFolder);

}

function promptDownload_(projectFolder) {
  var zipped = Utilities.zip(getBlobs_(projectFolder, ''), projectFolder.getName()+'.zip');
  var zipFile = projectFolder.getParents().next().createFile(zipped);
  var url = zipFile.getDownloadUrl();

  var htmlString = '<div><button style="height: 50px; width: 100%; text-align: center; font-size: 32px; background-color: grey; border-radius: 5px; border: 2px solid black;"><a type="button" style="width: 100%; text-decoration: none; color: white;" href="'+url.slice(0, -8)+'" target="_blank"/>DOWNLOAD NOW</a></button></div>'
  var htmlOutput = HtmlService
    .createHtmlOutput(htmlString)
    .setSandboxMode(HtmlService.SandboxMode.IFRAME)
    .setHeight(80);

  SpreadsheetApp
    .getUi()
    .showModalDialog(htmlOutput, 'Download Folders...');
}

function getBlobs_(rootFolder, path) {
  var blobs = [];
  var files = rootFolder.getFiles();
  while (files.hasNext()) {
    var file = files.next().getBlob();
    file.setName(path+file.getName());
    blobs.push(file);
  }
  var folders = rootFolder.getFolders();
  while (folders.hasNext()) {
    var folder = folders.next();
    var fPath = path+folder.getName()+'/';
    blobs.push(Utilities.newBlob([]).setName(fPath)); //comment/uncomment this line to skip/include empty folders
    blobs = blobs.concat(getBlobs_(folder, fPath));
  }
  return blobs;
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
