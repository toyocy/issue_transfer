## Read Me

- Python 3.6+

## Confirmed Environment

- Redmine 3.4.6
- Elasticsearch 6.4

## Installation

1. pip install -r requirement.txt
2. edit 'secret.py.sample' and rename 'secret.py'
3. run test mode
```sh
  python3 issue_transfer.py --testrun
```

result example

```sh
Connecting Redmine ----- [OK]
Get Issue -------------- [OK]
```

## Run mode

### Get all issues in Redmine
```sh
python3 issue_transfer.py --initial
``` 

### Get recently updated issues
Get updated issues the day before script execution.
```sh
python3 issue_tranfer.py
```
