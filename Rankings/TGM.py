
from Rankings.Sortable import *

class TGM_Interval(Sortable):
    """ TGM Time Interval Class """

    def __init__(self, minutes=-1, seconds=-1, milliseconds=-1, from_string=None):
        def check_value(name, value, max):
            if value > max:
                raise ValueError('%s must be less than %s' % (name, max))
        
        def real_value(value):
            return -1 if value == '--' else int(value)
        
        self.string_value = None
        if isinstance(from_string, str) or isinstance(from_string, unicode):
            self.string_value = str(from_string)
            minutes, seconds, milliseconds = [i for i in from_string.split(':')]
        
        minutes = real_value(minutes)
        seconds = real_value(seconds)
        milliseconds = real_value(milliseconds)
        
        check_value('minutes', minutes, 59)
        check_value('seconds', seconds, 59)
        check_value('milliseconds', milliseconds, 99)
        
        self.minutes = minutes
        self.seconds = seconds
        self.milliseconds = milliseconds
        
        sort_minutes = minutes
        sort_seconds = seconds
        sort_milliseconds = milliseconds
        
        if sort_minutes < 0:
            sort_minutes = 60
        
        if sort_seconds < 0:
            sort_seconds = 60
        
        if sort_milliseconds < 0:
            sort_milliseconds = 100
        
        super(self.__class__, self).__init__(self, (
            sort_minutes << 14 |
            sort_seconds << 7  |
            sort_milliseconds
        ))
    
    def __str__(self):
        values = [self.minutes, self.seconds, self.milliseconds]
        
        for x in range(3):
            i = values[x]
            if i < 0:
                i = '--'
            else:
                i = str(i)
                if len(i) < 2:
                    i = '0' + i
            
            values[x] = i
        
        return ':'.join(values)

class TGM1_Grade(Sortable):
    """ TGM1 Grade Class """

    grades = (   'GM', 'S9', 'S8', 'S7', 'S6', 'S5', 'S4', 'S3', 'S2', 'S1',
                         '9', '8',  '7',  '6',  '5',  '4',  '3',  '2',  '1')
    
    def __init__(self, grade):
        grade = str(grade.upper())
        self.grades_lk = {}
        
        for i in range(len(self.grades)):
            self.grades_lk[self.grades[i]] = i
        
        if grade not in self.grades_lk:
            raise ValueError('Grade "%s" is invalid' % (grade))
        
        self.grade = grade
        super(self.__class__, self).__init__(self, self.grades_lk[grade])
    
    def __str__(self):
        return self.grade[0] + self.grade[1].lower()

class TGM1_Level(Sortable):
    """ TGM1 Level Class """

    def __init__(self, level):
        self.level = level
        
        if isinstance(level, str) or isinstance(level, unicode):
            if level == '---':
                level = -1
            else:
                if level[1] == '-':
                    level = int(level[0]) * 100 - 0.5
                elif level[2] == '-':
                    level = int(level[0:2]) * 10 - 0.5
                else:
                    level = int(level)
        
        super(self.__class__, self).__init__(self, 1000 - level)
    
    def __str__(self):
        return self.level

class TGM1_Sortable(Sortable):
    """ TGM1 Sortable Entry """

    def __init__(self, entry):
        self.entry = entry
        
        entry['time'] = TGM_Interval(from_string=entry['time'])
        entry['grade'] = TGM1_Grade(entry['grade'])
        entry['level'] = TGM1_Level(entry['level'])
        
        super(self.__class__, self).__init__(self, (
            entry['grade'],
            entry['level'],
            entry['time']
        ))

