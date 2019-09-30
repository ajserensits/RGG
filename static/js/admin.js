$(document).ready(verify);

var PROTOCOL = window.location.protocol;
var HOST = window.location.hostname;
var BASE_PATH = PROTOCOL + "//" + HOST;
var MAPPINGS = undefined;

function init()
{
        fillHoursOfOperationSelects();
        getHoursOfOperation();
        getRecordings();
        getSpreadsheets();
        checkForUploadSuccess();
        attachEventHandlers();
}

function verify()
{

    var url_string = window.location.href
    var url = new URL(url_string);
    var user = url.searchParams.get("user");
    var token = url.searchParams.get("token");

    $('#upload_spreadsheet_user').val(user);
    $('#upload_recordings_user').val(user);

    $('#auth_token').val(token);
    $('#upload_spreadsheet_token').val(token);
    $('#upload_recordings_token').val(token);

    var end = "&user=" + user + "&token=" + token;

    var action = $('#spreadsheets_form')[0].action;
    action = action + end;
    $('#spreadsheets_form')[0].action = action;

    action = $('#recordings_form')[0].action;
    action = action + end;
    $('#recordings_form')[0].action = action;

    $.get(BASE_PATH + "/authenticated/?user=" + user + "&token=" + token , function(data){
         console.log(data);
         if(data["Authenticated"] == "True") {
            console.log("Verified");
             init();
         } else {
             window.location.href = "login.html";
         }
    });

}



function checkForUploadSuccess()
{
    var url_string = window.location.href
    var url = new URL(url_string);
    var c = url.searchParams.get("upload_status");
    var type = url.searchParams.get("type");
    if(c == "success") {
        if(type == "recordings") {
            alert("Successfully uploaded the recording.");
        } else {
            alert("Successfully uploaded the spreadsheet.");
        }
    }
    console.log(c);
}

function attachEventHandlers()
{
        //$('#upload_spreadsheet').click(uploadSpreadsheet);
        //$('#upload_recording').click(uploadRecording);

        $('#download_recording').click(downloadRecording);
        $('#delete_recording').click(deleteRecording);

        $('#download_spreadsheet').click(downloadSpreadsheet);
        $('#delete_spreadsheet').click(deleteSpreadsheet);

        $('#update_hours').click(updateHoursOfOperation);

        $('#number_mappings_select').change(updateNumberMappingsDiv);
        $('#update_mapping').click(updateNumberMappings)
}

function fillHoursOfOperationSelects()
{
    var i = 0;
    for(i = 0; i < 24; i++) {
        var option = document.createElement('option');
        option.innerHTML = i;
        option.value = i;
        $('#hours_open').append(option);
    }

    for(i = 0; i < 24; i++) {
        var option = document.createElement('option');
        option.innerHTML = i;
        option.value = i;
        $('#hours_closed').append(option);
    }
}

function getNumberMappings()
{
        $.get(BASE_PATH + "/getNumberMappings/" , function(data) {
                console.log("Number Mappings: " , data);
                MAPPINGS = data;
        });
}

function getRecordings()
{
        $.get(BASE_PATH + "/getRecording/" , function(data) {
                console.log("Recordings: " , data);
                fillRecordingsSelect(data);
        });
}

function getSpreadsheets()
{
        $.get(BASE_PATH + "/getSpreadsheet/" , function(data) {
                console.log("Spreadsheets: " , data);
                fillSpreadsheetsSelect(data);
                fillNumberMappingsSelect(data);
                getNumberMappings();

        });
}

function getHoursOfOperation()
{
        $.get(BASE_PATH + "/getHoursOfOperation/" , function(data) {
                console.log("Hours: " , data);
                fillHoursOfOperation(data);
        });

}

function fillHoursOfOperation(json)
{
        $('#hours_open').val(json.open);
        $('#hours_closed').val(json.closed);
}

function updateHoursOfOperation()
{
        var user = $('#upload_recordings_user').val();
        var token = $('#auth_token').val();
        var open = $('#hours_open').val();
        var closed = $('#hours_closed').val();
        var r = confirm("Are you sure you want to update the hours of operation?");
        if(r == false) {
            return;
        }
        $.get(BASE_PATH + "/updateHours/?open=" + open + "&closed=" + closed + "&user=" + user + "&token=" + token, function(data) {
                console.log("Update Hours of Operation Response: " , data);
                if(data["Status"] == "Success") {
                    alert("Successfully updated the hours of operation.");
                }
        });

}

function downloadRecording()
{
        var recording = $('#recordings_select').val();
        if(recording == undefined || recording == null) {
                return;
        }

       window.open(BASE_PATH + '/media/recordings/' + recording , '_blank');
}

function downloadSpreadsheet()
{
        var spreadsheet = $('#spreadsheets_select').val();
        if(spreadsheet == undefined || spreadsheet == null) {
                return;
        }

       window.open(BASE_PATH + '/media/spreadsheets/' + spreadsheet , '_blank');
}

function deleteRecording()
{
        var recording = $('#recordings_select').val();
        if(recording == undefined || recording == null) {
                return;
        }

        var r = confirm("Are you sure you want to delete the recording named " + recording + "?");
        if(r == false) {
            return;
        }

        $.get(BASE_PATH + "/deleteRecording?file_name=" + recording , function(data) {
                $('#recordings_select').find('option[value="' + recording + '"]').remove();
        });
}

function deleteSpreadsheet()
{
        var spreadsheet = $('#spreadsheets_select').val();
        if(spreadsheet == undefined || spreadsheet == null) {
                return;
        }

        var r = confirm("Are you sure you want to delete the spreadsheet named " + spreadsheet + "?");
        if(r == false) {
            return;
        }

        $.get(BASE_PATH + "/deleteSpreadsheet?file_name=" + spreadsheet , function(data) {
                $('#spreadsheets_select').find('option[value="' + spreadsheet + '"]').remove();
        });
}

function fillRecordingsSelect(json)
{
        json.sort(function(a, b) {
            return compareStrings(a, b);
        });

        var i = 0;
        for(i = 0; i < json.length; i++)
        {
                var option = document.createElement('option');
                option.value = json[i];
                option.innerHTML = json[i].replace(".mp3" , "");
                $('#recordings_select').append(option);
        }
}

function fillSpreadsheetsSelect(json)
{
        json.sort(function(a, b) {
            return compareStrings(a, b);
        });

        var i = 0;
        for(i = 0; i < json.length; i++)
        {
                var option = document.createElement('option');
                option.value = json[i];
                option.innerHTML = json[i].replace(".xlsx" , "");
                $('#spreadsheets_select').append(option);
        }
}

function fillNumberMappingsSelect(json)
{
        json.sort(function(a, b) {
            return compareStrings(a, b);
        });

        var i = 0;
        for(i = 0; i < json.length; i++)
        {
                var option = document.createElement('option');
                option.value = json[i].replace(".xlsx" , "");
                option.innerHTML = json[i].replace(".xlsx" , "");
                $('#number_mappings_select').append(option);
        }
}



function checkSpreadsheetForm()
{

    var file = $('#spreadsheet_file_input')[0].files[0];
    if(file == undefined || file == null || file == "") {
            alert("You must choose a spreadsheet file to upload.");
            return false;
    }
    var spreadsheet = $('#spreadsheets_select').val();
    $('#hidden_spreadsheet_input').val(spreadsheet);
    var message = "Are you sure you would like to replace the spreadsheet named " + spreadsheet + "?";
    var r = confirm(message);
    return r;
}

function checkRecordingsForm()
{
    var file = $('#recordings_file_input')[0].files[0];
    if(file == undefined || file == null || file == "") {
            alert("You must choose a recording file to upload.");
            return false;
    }
    var recording = $('#recordings_select').val();
    $('#hidden_recordings_input').val(recording);
    var message = "Are you sure you would like to replace the recording named " + recording + "?";
    var r = confirm(message);
    return r;
}

function updateNumberMappingsDiv()
{
    var mapping = $('#number_mappings_select').val();

    var radial = MAPPINGS[mapping]["Radial"];
    var rgg = MAPPINGS[mapping]["RGG"];

    $('#mapping_radial').val(radial);
    $('#mapping_rgg').val(rgg);
}

function updateNumberMappings()
{
    var user = $('#upload_recordings_user').val();
    var token = $('#auth_token').val();
    var mapping = $('#number_mappings_select').val();
    var radial = $('#mapping_radial').val();
    var rgg = $('#mapping_rgg').val();


    if(radial == "" || radial == undefined) {
        alert("Must enter a value for Radial.");
        return;
    }

    if(rgg == "" || rgg == undefined) {
        alert("Must enter a value for RGG.");
        return;
    }

    if(mapping == "" || mapping == undefined) {
        alert("Must select a mapping to change.");
        return;
    }

    var r = confirm("Are you sure you want to update the number mapping for " + mapping + "?");
    if(r == false) {
        return;
    }

    radial = radial.replace("+" , "");
    rgg = rgg.replace("+" , "");

    radial = removeAllNonNumeric(radial);
    rgg = removeAllNonNumeric(rgg);

    $.get(BASE_PATH + "/updateNumberMappings?rgg=" + rgg + "&radial=" + radial + "&mapping=" + mapping + "&user=" + user + "&token=" + token , function(data) {
            console.log("Update Number Mapping Return: " , data);
            if(data["Status"] == "Success") {
                alert("Successfully updated number mapping");
            }
            getNumberMappings();
    });
}

function removeAllNonNumeric(str)
{
    if(str == undefined || str == null || str == "") {
        return str;
    }

    return str.replace(/\D/g,'');
}

function compareStrings(a, b) {
  // case-insensitive comparison
  a = a.toLowerCase();
  b = b.toLowerCase();

  return (a < b) ? -1 : (a > b) ? 1 : 0;
}











