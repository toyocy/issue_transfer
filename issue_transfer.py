import requests
import json
import datetime
import argparse
import sys

from secrets import REDMINE_URL, REDMINE_USERS_KEY, ES_HOST
from elasticsearch import Elasticsearch
from elasticsearch import helpers

def test_run():
  payload = {
    "limit": "1",
    "offset": 0,
    "key": REDMINE_USERS_KEY
  }

  res = requests.get(REDMINE_URL, params=payload)
  if (res.status_code == 200):
    print("Response Code:" + str(res.status_code))
    print("Get Issue [OK]")
  else:
    print(res)
    print("Get Issue [NG]")

  sys.exit()

def get_issue_list(args):
  json_dict = {}
  page = 0
  offset = 0
  page_size = 100
  limit = "100"

  # コマンドライン引数で --initial が渡された場合、初回実行と判定し、全件取得する。
  # 引数が渡されない場合は、スクリプト実行の前日に更新したチケットを取得する。
  yesterday = datetime.date.today() - datetime.timedelta(days=1)
  url = REDMINE_URL
  if not(args.initial):
    url = url + "?updated_on=><" + yesterday.strftime("%Y-%m-%d") + "|" + yesterday.strftime("%Y-%m-%d")

  while page_size >= 100:
    payload = {
      "limit": limit,
      "status_id" : "*",
      "offset": offset,
      "key": REDMINE_USERS_KEY
    }

    res = requests.get(url, params=payload)
    json_dict[page] = res.json()
    page_size = len(json_dict[page]["issues"])

    if page !=0:
      json_dict["issues"].extend(json_dict[page]["issues"])
    else:
      json_dict = json_dict[page]

    page = page + 1
    offset = offset + 100

  return json_dict["issues"]

def main():
    
  parser = argparse.ArgumentParser()
  parser.add_argument("--initial", help="You can get all issues. By default, get the updated ticket the day before running this script.", action="store_true")
  parser.add_argument("--testrun", help="Test run.", action="store_true")
  args = parser.parse_args()
  
  # Test Run では1件だけ Redmine からチケットを取得し、get_issue_list() が問題なく動作するか確認できる。
  if (args.testrun):
    test_run()

  today = datetime.date.today().strftime("%Y%m%d")
  es = Elasticsearch([ES_HOST])
  es_index = f"{'redmine-' + today}"
  es_type = "issues"
  actions = []

  # TODO: リファクタリング予定
  for issue in get_issue_list(args):
    data = {
      "project": issue['project']['name'],
      "tracker": issue['tracker']['name'],
      "status": issue['status']['name'],
      "priority": issue['priority']['name'],
      "author": issue['author']['name'],
      "subject": issue['subject'],
      "created_on": issue['created_on'],
      "updated_on": issue['updated_on']
    }

    if 'start_date' in issue.keys():
      data.update({"start_date": issue['start_date']})
    
    if 'description' in issue.keys():
      data.update({"description": issue['description']})

    if 'due_date' in issue.keys():
      data.update({"due_date": issue['due_date']})
      
    if 'assigned_to' in issue.keys():
      data.update({"assigned_to": issue['assigned_to']['name']})

    actions.append({'_op_type':'index','_id':issue['id'], '_index':es_index, '_type':es_type, '_source':data})

    if len(actions) > 1000:
      helpers.bulk(es, actions)
      actions = []
      
  if len(actions) > 0:
    helpers.bulk(es, actions)

if __name__ == '__main__':
  main()