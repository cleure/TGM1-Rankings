
import os, sys, argparse, sqlite3
from Rankings.TGM import *

DATABASE_PATH = 'rankings.db'
DB = None

def load_rankings():
    rankings = []
    cursor = DB.cursor()
    cursor.execute('SELECT * FROM tgm1_rankings')
    
    keys = [i[0] for i in cursor.description]
    
    for i in cursor.fetchall():
        entry = dict(zip(keys, i))
        rankings.append(TGM1_Sortable(entry))
    
    rankings.sort()
    return rankings

def print_rankings(rankings):
    def print_separator():
        print('------------------------------------------------------------')

    print('                  *** WESTERN RANKING ***')
    print('\nRank--Name---------------- Grade - Lvl @ Time     - Date')
    
    last_time = 0
    last_grade = 0
    for i in range(len(rankings)):
        rank = '   '
        name = '-----------------------'
        e = rankings[i].entry
        r = str(i+1)
        
        if str(e['grade']) == 'Gm' and e['time'].minutes > 0 and e['time'].minutes != last_time:
            print_separator()
            last_time = e['time'].minutes
        elif last_grade == 'Gm' and not str(e['grade']) == last_grade:
            print_separator()
            
        name = e['name'] + name[len(e['name']):]
        rank = rank[len(r):] + r
        
        print(' %s--%s %s - %s @ %s - %s - %s' % (
            rank,
            name,
            e['grade'],
            e['level'],
            e['time'],
            e['date'],
            e['notes']
        ))
        
        last_grade = str(e['grade'])

def load_db():
    """ Loads DB, and automatically creates needed tables. """
    
    global DB
    global DATABASE_PATH
    
    DB = sqlite3.connect(DATABASE_PATH)
    cursor = DB.cursor()
    
    cursor.execute(("SELECT name FROM sqlite_master "
                    "WHERE type='table' AND name='tgm1_rankings'"))
    
    if cursor.fetchone() is None:
        create_table = (
            "CREATE TABLE tgm1_rankings ( "
                "rank INTEGER UNIQUE, "
                "name VARCHAR(96) UNIQUE, "
                "grade CHAR(2), "
                "level VARCHAR(3), "
                "time VARCHAR(10), "
                "date VARCHAR(10), "
                "notes VARCHAR(256) "
            ");"
        )
        
        cursor.execute(create_table)
        DB.commit()

def handle_list(args):
    """ Prints rankings list """
    print_rankings(load_rankings())

def handle_add(args):
    """ Adds/Updates ranking entry """
    global DB

    keys = ['name', 'grade', 'level', 'time', 'date', 'notes']
    cursor = DB.cursor()

    if args.name is None:
        sys.stdout.write('--name is required for add\n')
        sys.exit(1)
    
    if args.grade is None:
        sys.stdout.write('--grade is required for add\n')
        sys.exit(1)
    
    entry = {
        k : getattr(args, k) if getattr(args, k) is not None else ''
        for k in keys
    }
    
    cursor.execute('SELECT * FROM tgm1_rankings WHERE name = ?', [args.name])
    if cursor.fetchone() is None:
        query = (
            'INSERT INTO tgm1_rankings (%s) VALUES (%s)' % (
                ', '.join(entry.keys()),
                ', '.join(['?' for i in entry.keys()])))
        
        escape = list(entry.values())
    else:
        query = (
            'UPDATE tgm1_rankings SET %s WHERE name = ?' % (
                ', '.join(['%s = ?' % (k) for k in entry.keys()])))
        
        escape = list(entry.values())
        escape.append(args.name)
    
    cursor.execute(query, escape)
    DB.commit()
    
    print('Database Updated')

def handle_del(args):
    """ Deletes ranking entry """
    global DB
    
    cursor = DB.cursor()
    if args.name is None:
        sys.stdout.write('--name is required for del\n')
        sys.exit(1)
    
    cursor.execute('DELETE FROM tgm1_rankings WHERE name = ?', [args.name])
    DB.commit()
    
    print('Database Updated')

def main():
    global DATABASE_PATH

    fn_table = {
        'list': handle_list,
        'add': handle_add,
        'del': handle_del
    }

    parser = argparse.ArgumentParser(description='TGM1 Ranking Tool')
    
    parser.add_argument('action',       help='list, add, del', choices=['list', 'add', 'del'])
    parser.add_argument('--database',   help='Sqlite3 DB (path)')
    
    parser.add_argument('--name',       help='User Name (required for add/del)')
    parser.add_argument('--grade',      help='Grade... GM, S9 (required for add)')
    parser.add_argument('--level',      help='0 - 999', default='---')
    parser.add_argument('--time',       help='MM:SS:MS', default='--:--:--')
    parser.add_argument('--date',       help='MM/DD/YY', default='--/--/--')
    parser.add_argument('--notes',      help='Performance Notes')
    
    args = parser.parse_args()
    if args.database is not None:
        DATABASE_PATH = args.database
    
    load_db()
    fn_table[args.action](args)
    
    DB.close()
    sys.exit(0)

if __name__ == '__main__':
    main()
