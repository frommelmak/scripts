#!/usr/bin/env python
#
# Delete old documents from couchDB database
#
# Note: This script assumes that the documents have a field to store a Unix
#       timestamp value. The field name can be passed at execution time as an
#       argument
#
# Copyright (c) 2013 Marcos Martinez - <frommelmak@gmail.com>
#

import sys
from couchdb.client import Server
from datetime import datetime, timedelta
import argparse


def delete_old_entries(server, db, age, ts, remove):
    server = Server(server)
    db = server[db]
    total = 0
    deleted = 0
    untouched = 0
    now = datetime.now()
    map_fun = '''function(doc) {
              if(doc.%s) {
                emit(doc._id,doc.%s);
              }
    }''' % (ts, ts)

    for row in db.query(map_fun):
        doc_timestamp = int(row.value)
        doc_datetime = datetime.fromtimestamp(doc_timestamp)
        doc_id = row.key
        elapsed = now - doc_datetime
        total = total + 1
        if total == 1:
            print "DOC_NUM | DOC_ID | DATETIME| AGE | ACTION"
            print "========================================="
        if elapsed > timedelta(days=age):
            print ("%s | %s | %s | %s | DELETE"
                    % (total, doc_id, doc_datetime, elapsed))
            deleted = deleted + 1
            if remove:
                doc = db[doc_id]
                db.delete(doc)
        else:
            print ("%s | %s | %s | %s | NONE"
                    % (total, doc_id, doc_datetime, elapsed))
            untouched = untouched + 1
    return {'total': total, 'deleted': deleted, 'untouched': untouched}


def compact(server, db):
    server = Server(server)
    db = server[db]
    result = db.compact()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server', default='http://127.0.0.1:5984',
            help="CouchDB server URL")
    parser.add_argument('-d', '--db', required=True, help="CouchDB database")
    parser.add_argument('-a', '--age', default='120',
            help="CouchDB maximun document age allowed")
    parser.add_argument('-t', '--ts', default='timestamp',
            help="Timestamp field name as defined in doc database")
    parser.add_argument('-r', '--remove', action='store_true',
            help="Delete older documents")
    parser.add_argument('-c', '--compact', action='store_true',
            help="Compact database if documents were deleted. Requires -r.")
    args = parser.parse_args()
    result = delete_old_entries(args.server, args.db, int(args.age), args.ts,
            args.remove)
    print ("Documents processed: %s, Deleted: %s, Untouched: %s"
            % (result['total'], result['deleted'], result['untouched']))
    if compact and args.remove and result['deleted'] > 0:
        result = compact(args.server, args.db)
        print ("Compact: %s") % result

if __name__ == '__main__':
    sys.exit(main())
