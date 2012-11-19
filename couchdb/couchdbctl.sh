#!/bin/bash

# Marcos Martínez
# frommelmak@gmail.com

host='localhost'
port='5984'
user=''
pass=''
rev='2'

dbs=$(curl -s http://$user:$pass@$host:$port/_all_dbs |sed 's/[]|\[|\"|\,]/ /g')

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
  curl -s http://$host:$port/$db | python -m json.tool
  done
  ;;
-settings|-s)
  curl -s http://$user:$pass@$host:$port/_config | python -m json.tool
  ;;
-version|-v)
  curl -s http://$user:$pass@$host:$port | python -m json.tool
  ;;
-all_dbs|-a)
  curl -s http://$user:$pass@$host:$port/_all_dbs | python -m json.tool
  ;;
*)
  echo "USAGE: $0 [-compact|-c] | [-tasks|-t] | [-info|-i] | [-settings|-s] | [-version|-v] | \
                      [-all_dbs|-a]"
  ;;
esac
