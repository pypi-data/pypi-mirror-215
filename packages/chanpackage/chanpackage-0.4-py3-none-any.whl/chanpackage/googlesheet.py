import gspread
from oauth2client.service_account import ServiceAccountCredentials


def get(filename,sheetname):

    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    key = "gkey/stackpython-369707-846992bb8d7e.json"
    cerds = ServiceAccountCredentials.from_json_keyfile_name(key, scope)
    client = gspread.authorize(cerds)
    sheet = client.open(filename).worksheet(sheetname) # เป็นการเปิดไปยังหน้าชีตนั้นๆ
    # print(sheet)
    # sheet.update_cell(4,2,"แก้ไข")
    # data = sheet.get_all_records()  # การรับรายการของระเบียนทั้งหมด reture dict
    # data = sheet.get_values()
    data_googlesheet = sheet.get_all_values()  # reture list

    return data_googlesheet