#!/bin/bash

# Marcos Martínez
# frommelmak@gmail.com

host='localhost'
port='5984'
user='root'
pass=''
dbs='db1 db2'
rev='2'

case $1 in 
-compact|-c)
  for db in $dbs; do
    echo "Setting revisions to $rev, and compact and cleanup $db"
    curl -X PUT -d "$rev" http://$user:$pass@$host:$port/$db/_revs_limit
    curl -H "Content-Type: application/json" -X POST http://$host:$port/$db/_compact
    curl -H "Content-Type: application/json" -X POST http://$host:$port/$db/_compact/$db
    curl -H "Content-Type: application/json" -X POST http://$host:$port/$db/_view_cleanup
  done
  ;;
-tasks|-t)
  echo "Active Tasks:"
  curl http://$user:$pass@$host:$port/_active_tasks
  ;;
-info|-i)
  for db in $dbs; do
  echo "$db"
  curl -s http://$host:$port/$db | python -mjson.tool
  done
  ;;
-settings|-s)
  curl -s http://$user:$pass@$host:$port/_config | python -mjson.tool
  ;;
-version|-v)
  curl -s http://$user:$pass@$host:$port
  ;;
*)
  echo "USAGE: $0 [-compact|-c] | [-tasks|-t] | [-info|-i] | [-settings|-s] | [-version|-v]"
  ;;
esac
