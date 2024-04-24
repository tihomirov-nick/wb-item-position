import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests

def search_item(product_id, query):
    page_count = 1
    query_result_product_id = 0

    while True:

      try:
        r = requests.get(f'https://search.wb.ru/exactmatch/ru/common/v4/search?appType=1&curr=rub&dest=-1257218&page={str(page_count)}&query={str(query)}&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false')
        request_result = r.json()

        if len(request_result['data']['products']) == 1:
          while len(request_result['data']['products']) == 1:
            r = requests.get(f'https://search.wb.ru/exactmatch/ru/common/v4/search?appType=1&curr=rub&dest=-1257218&page={str(page_count)}&query={str(query)}&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false')
            request_result = r.json()

      except:
        return 'NOT FOUND'
        break

      while query_result_product_id < 100:

        try:
          if int(product_id) == request_result['data']['products'][query_result_product_id]['id']:
            query_result_product_id_position = (query_result_product_id + 1) + 100 * (page_count - 1)
            return query_result_product_id_position

          query_result_product_id += 1
        except Exception as e:
          return 'NOT FOUND'

      page_count += 1
      query_result_product_id = 0

def main():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
    client = gspread.authorize(creds)

    spreadsheet_name = 'SHEET NAME'
    spreadsheet = client.open(spreadsheet_name)
    sheet = spreadsheet.sheet1

    first_column = sheet.col_values(1)
    second_column = sheet.col_values(2)

    for i in range(1, len(first_column)):
        product_id = first_column[i]
        query = second_column[i]

        position = search_item(product_id, query)

        sheet.update_cell(i + 1, 3, position)

if __name__ == '__main__':
    main()