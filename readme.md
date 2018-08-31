## Read Me

- Python 3.6+

## Installation

1. pip install -r requirement.txt
2. edit 'secrets.py.sample' and rename 'secrets.py'
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

### Get all issues on Redmine
Get all issues of Redmine.
```sh
python3 issue_transfer.py --initial
``` 

### Get recently updated issues
Get updated issues the day before script execution.
```sh
python3 issue_tranfer.py
```

