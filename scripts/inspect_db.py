import sqlite3, sys
import pathlib

if __name__ == '__main__':
    db = 'data/intel.db'
    p = pathlib.Path(db)
    if not p.exists():
        print('DB not found:', db)
        sys.exit(0)
    conn = sqlite3.connect(db)
    c = conn.cursor()
    print('TABLES:', [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")])
    print('\nPAGES (up to 10):')
    for row in c.execute('SELECT url,fetched_at,status_code,title,error FROM pages LIMIT 10'):
        print(row)
    print('\nINDICATORS (up to 10):')
    for row in c.execute('SELECT page_url,indicator,type FROM indicators LIMIT 10'):
        print(row)
    conn.close()
