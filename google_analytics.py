#-*- coding: utf-8 -*-

import argparse
import xlwt
import xlrd
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import pprint
import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools
import datetime
from datetime import timedelta
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
DISCOVERY_URI = ('https://analyticsreporting.googleapis.com/$discovery/rest')
KEY_FILE_LOCATION = 'client_secrets.p12'
SERVICE_ACCOUNT_EMAIL = 'eugene@python-149108.iam.gserviceaccount.com'

Platforms = {"LG": "116060770", "Samsung": "116048361", "Android": "125654904", "iOS": "125643516"}

def initialize_analyticsreporting():
  credentials = ServiceAccountCredentials.from_p12_keyfile(SERVICE_ACCOUNT_EMAIL, KEY_FILE_LOCATION, scopes=SCOPES)
  http = credentials.authorize(httplib2.Http())
  analytics = build('analytics', 'v4', http=http, discoveryServiceUrl=DISCOVERY_URI)
  return analytics


def get_report(analytics, query):
  return analytics.reports().batchGet(body=query).execute()


def get_response(response):
  x_mass = []
  y_mass = []
  for report in response.get('reports', []):
    columnHeader = report.get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
    rows = report.get('data', {}).get('rows', [])

    for row in rows:
      dimensions = row.get('dimensions', [])
      dateRangeValues = row.get('metrics', [])

      for header, dimension in zip(dimensionHeaders, dimensions):
        x_mass.append(int(dimension))


      for i, values in enumerate(dateRangeValues):
        for metricHeader, value in zip(metricHeaders, values.get('values')):
          y_mass.append(int(value))

  return x_mass, y_mass


def query_builder(VIEW_ID, startdate, enddate, eventCategory, eventAction, film):
  query = {
    'reportRequests': [
      {
        'viewId': VIEW_ID,
        'dateRanges': [{'startDate': startdate, 'endDate': enddate}],
        'metrics': [{'expression': 'ga:totalEvents'}],
        "filtersExpression": "ga:eventCategory==" + eventCategory + ";ga:eventAction==" + eventAction + ";ga:eventLabel=@" + film
      }
    ]
  }
  return query

def week_filler(row, col, startdate, enddate, film, ws):

  """Для каждой платформы свой тип запроса (мобильные\smartTV)"""
  for platform in Platforms.keys():

    if platform not in ["iOS", "Android"]:
      eventCategory = "watches"
      eventAction = "film_watch_25"
    else:
      eventCategory = "Watches"
      eventAction = "Watch"

    query = query_builder(Platforms[platform], str(startdate), str(enddate), eventCategory, eventAction, film)
    analytics = initialize_analyticsreporting()

    """пробуем выполнить запрос"""
    try:
      response = get_report(analytics, query)
      x, y = get_response(response)

      """пробуем получить значение"""
      try:
        print str(y[0])
        ws.write(row, col, int((y[0])))
      except:
        print 0
    except:
      pass
    col += 1
  ws.write(row, col, (enddate - startdate).days)


def to_date(rb, date):
  year, month, day, hour, minute, second = xlrd.xldate_as_tuple(date, rb.datemode)
  return datetime.date(year, month, day)


def get_films():
  Collections = {}
  promo = {}
  new = {}
  Recommended = {}
  rb = xlrd.open_workbook('bearing.xlsx')
  sheet = rb.sheet_by_index(0)
  for rownum in range(sheet.nrows-1):
    row = sheet.row_values(rownum+1)

    if row[3]==u'Промо':
      promo[row[0]] = {}
      promo[row[0]]["appear"] = to_date(rb, row[1])
      promo[row[0]]["first_report"] = to_date(rb, row[2])

    if row[3] == u'Новое':
      new[row[0]] = {}
      new[row[0]]["appear"] = to_date(rb, row[1])
      new[row[0]]["first_report"] = to_date(rb, row[2])

    if row[3] == u'Рекомендуемое':
      Recommended[row[0]] = {}
      Recommended[row[0]]["appear"] = to_date(rb, row[1])
      Recommended[row[0]]["first_report"] = to_date(rb, row[2])

  Collections["Promo"] = promo
  Collections["New"] = new
  Collections["Recommended"] = Recommended
  return Collections


def count_films(collection):
  return len(Collections[collection].keys())

def main(Collections):

  wb = xlwt.Workbook()
  ws = wb.add_sheet('Watches')
  row=2
  collection_cursor = 2
  data_row = 2
  data_col = 2

  """формируем структуру"""
  ws.write_merge(r1=0, r2=0, c1=2, c2=6, label="week 1")
  ws.write_merge(r1=0, r2=0, c1=7, c2=11, label="week 2")
  ws.write_merge(r1=0, r2=0, c1=12, c2=16, label="week 3")
  ws.write_merge(r1=0, r2=0, c1=17, c2=21, label="week 4")
  ws.write_merge(r1=0, r2=0, c1=22, c2=26, label="week 5")

  j=0
  ws.write(1, 1, "Films")
  for i in range(5):
    ws.write(1, 2+j*5, "LG")
    ws.write(1, 3+j*5, "ANDROID")
    ws.write(1, 4+j*5, "iOS")
    ws.write(1, 5+j*5, "SAMSUNG")
    ws.write(1, 6+j*5, "monitoring period")
    j+=1

  collection_cursor_shift = 0

  """для каждой коллекции"""
  for collection in Collections.keys():
    ws.write_merge(r1=collection_cursor+collection_cursor_shift, r2=count_films(collection)+1+collection_cursor_shift, c1=0, c2=0, label=collection)
    collection_cursor_shift += count_films(collection)

    """для каждого фильма в коллекции"""
    for film in Collections[collection].keys():
      print film

      print Collections[collection][film]["appear"]
      ws.write(row, 1, film)
      row+=1

      """первая неделя"""
      print "first_week_report", Collections[collection][film]["appear"], Collections[collection][film]["first_report"]
      week_filler(data_row, data_col, Collections[collection][film]["appear"], Collections[collection][film]["first_report"], film, ws)

      """вторая неделя"""
      print "second_week_report", Collections[collection][film]["first_report"], Collections[collection][film]["first_report"]+timedelta(days=7)
      week_filler(data_row, data_col+5, Collections[collection][film]["first_report"], Collections[collection][film]["first_report"]+timedelta(days=7), film, ws)

      """третья неделя"""
      print "third_week_report", Collections[collection][film]["first_report"]+ timedelta(days=7), Collections[collection][film]["first_report"] + timedelta(days=14)
      week_filler(data_row, data_col+10, Collections[collection][film]["first_report"]+timedelta(days=7), Collections[collection][film]["first_report"]+timedelta(days=14), film, ws)

      """четвертая неделя"""
      print "fourth_week_report", Collections[collection][film]["first_report"] + timedelta(days=14), Collections[collection][film]["first_report"] + timedelta(days=21)
      week_filler(data_row, data_col+15, Collections[collection][film]["first_report"]+timedelta(days=14), Collections[collection][film]["first_report"]+timedelta(days=21), film, ws)

      """пятая неделя"""
      print "fifth_week_report", Collections[collection][film]["first_report"] + timedelta(days=21), Collections[collection][film]["first_report"] + timedelta(days=28)
      week_filler(data_row, data_col+20, Collections[collection][film]["first_report"]+timedelta(days=21), Collections[collection][film]["first_report"]+timedelta(days=28), film, ws)
      data_row+=1

    data_col=2
  wb.save('Watches.xls')

Collections = get_films()
main(Collections)
