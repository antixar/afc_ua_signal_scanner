import random
import sys
from collections import defaultdict
from tabulate import tabulate
import hashlib
from copy import deepcopy
import datetime
from dateutil import relativedelta
from functools import lru_cache

# ------------------------------------------------------
first_date = datetime.date(2022, 10, 1)

duties = {
    # skill_level, last duty day, group, max count of dublicated assistants 
    'pavlenok': (1, '2022/09/30', "cp", 5),  
    'semerich': (0.3, '2022/09/29', "cp", 5),
    'vydra': (0, '2022/09/28', "cp", 5),
    
}

unique_weekdays = [6, 7]

assistants = {
     # skill_level, priority days or all days if pisible, last duty day, max duty days, group
     
    "gromenko": (1, [1, 7, 8, 14, 15, 21, 22, 28, 29], '2022/09/17', None, "gp", False),
    "tkachenko": (1, [i for i in range(6, 31)], "2022/09/19", 2, "gp", False),
    "skoropad": (1, None, '2022/09/27', 3, "gp", True),
    
    "zozulia": (0.4, None, '2022/09/21', None, "gs", True ),
    "zhura": (0.3, None, '2022/09/24', None, "gs", True),
    
    "krykun": (1, None, '2022/09/28', None, "gl", False),
    "yovchenko": (0.3, None, '2022/09/30', None, "gl", False),
    
    "panasenko": (0, None, '2022/09/18', None, "gl", False),
    
    "tregubenko": (1, None, '2022/09/29', None, "gl", False),
}
#-------------------------------------------------------
min_delay = 4
min_group_delay = 1
max_count = 4
min_count = 3
min_total_skill = 0.6


#===========================================================================

def last_date():
    return first_date + relativedelta.relativedelta(months=1) - datetime.timedelta(days=1)

def month_size():
    return int((last_date() -  first_date).days) + 1

def daterange():
    for n in range(month_size()):
        yield first_date + datetime.timedelta(n)


def generate_duty_pairs(date, last_duty_dates, last_group_dates):
    day_number = int(date.day)
    available_duties = [d for d in duties if last_duty_dates[d] if (date - last_duty_dates[d]).days >= len(duties)]
    for duty in available_duties:
        duty_skill = duties[duty][0]
        for assistant, (assistant_skill, available_days, _, _, group, _) in assistants.items():
            if (assistant_skill + duty_skill) < min_total_skill:
                # check minimal pair skill level
                # print(f"1 {assistant}")
                pass
            elif available_days and day_number not in available_days:
                # skip all not available days
                # print(f"2 {assistant}")
                pass
            elif (date - last_duty_dates[assistant]).days < min_delay + 1:
                # skip recent duty days
                # print(f"3 {assistant}")
                pass
            elif date.isoweekday() != 7 and (date - last_group_dates[group]).days < min_group_delay + 1:
                # skip recent group days
                # this logic doesn't work on Sunday
                # print(f"4 {assistant}")
                pass
            else:
                yield date, duty, assistant
    

def check_combination(combination, finished=False):
    res = {}
    
    for a in assistants:
        count = len([c for c in combination if c[2] == a])
        if finished and assistants[a][5]:
            used_weekdays = [c[0].isoweekday() for c in combination if (
                c[2] == a and
                c[0].isoweekday() in unique_weekdays
            )]
            if len(used_weekdays) > 1:
                return None

        limit = assistants[a][3] or max_count
        assistant_min_count = assistants[a][3] if (assistants[a][3] and assistants[a][3] < min_count) else min_count
        if count > limit:
            return None
        if finished and count < assistant_min_count:
                return None
        res[a] = count
        
    if finished:
        for d in duties:
            unique_assistants = defaultdict(lambda: 0)
            for c in combination:
                if c[1] == d:
                    unique_assistants[c[2]] += 1
            # if len(unique_assistants) < 3:
            #    return None
            
            for u in unique_assistants.values():
                if u > duties[d][3]:
                    return None
        
    return res

def generate_combinations(date, last_duty_dates, last_group_dates, prev_combination=None):
    # print(f"date: {date}, {last_date()}")
    prev_combination = prev_combination or []
    if date <= last_date():
        for pair in generate_duty_pairs(date, last_duty_dates, last_group_dates):
            tmp_last_duty_dates = deepcopy(last_duty_dates)
            tmp_last_duty_dates[pair[1]]= date
            tmp_last_duty_dates[pair[2]]= date
            # raise Exception(f"{pair}")
            tmp_last_group_dates = deepcopy(last_group_dates)
            tmp_last_group_dates[assistants[pair[2]][4]] = date
            updated_combination = prev_combination + [pair]
            if not check_combination(updated_combination):
                continue

            for combination in generate_combinations(date + datetime.timedelta(days=1), tmp_last_duty_dates, tmp_last_group_dates, updated_combination):
                if check_combination(combination):
                    yield combination
    else:
        yield prev_combination

# @lru_cache(maxsize=None)
def sort_combination(combination):
    # weekdays = defaultdict(lambda: defaultdict(lambda: 0))
    weekdays = {a: [datetime.datetime.strptime(assistants[a][2], '%Y/%m/%d').date().weekday()] for a in assistants if assistants[a][2]}

    pair_counts = set()
    for d in combination:
        assistant = d[2]
        if assistants[assistant][1] and int(d[0].day) in assistants[assistant][1]:
            # skip a calculation for available days, because they are customed
            continue
        weekdays[assistant].append(d[0].weekday())
        # weekdays[assistant][d[0].weekday()] += 1
        pair_counts.add((d[1], d[2]))
    for a, w in weekdays.items():
        temp = defaultdict(list)
        
        found = False
        for i in range(len(w)-1):
            if w[i] == w[i+1]:
                found = True
                if not temp[w[i]] or not temp[w[i]][-1]:
                    temp[w[i]].append(1)
                temp[w[i]][-1] += 1
            elif found:
                found = False
                temp[w[i-1]].append(0)
        temp = {k: sorted(v)[-1] for k, v in temp.items()}  
        temp2 = defaultdict(lambda: 0)
        for ww in w:
            temp2[ww] += 1
            
        weekdays[a] = temp, temp2         

    weekday_weights = []
    for a, (w, w2) in weekdays.items():
        
        temp = []
        for i in range(7):
            temp.append(int(str((w[i] if i in w else 0) + 1) + str(w2[i] if i in w2 else 0)))
        # print(temp)
        weekday_weights.append(sorted(temp)[-1])
    weekday_weights = "".join([str(w) for w in sorted(weekday_weights, reverse=True)])
    #    weekday_weights.append(int(''.join(sorted(t, reverse=True))))
    # raise Exception(f"{weekdays} => {weekday_weights}")
    # weekday_weights.sort()
    return int(weekday_weights)
    return 100000 - len(pair_counts), sorted(weekday_weights)[-1], 
    

def generate():
    # parse all last duty days (from previus month)
    gap_date = first_date - datetime.timedelta(days=100)
    last_duty_dates = {a: datetime.datetime.strptime(assistants[a][2], '%Y/%m/%d').date() if assistants[a][2] else gap_date for a in assistants}
    last_duty_dates.update({
       d: datetime.datetime.strptime(duties[d][1], '%Y/%m/%d').date() if duties[d][1] else gap_date for d in duties
     })
    last_group_dates = defaultdict(list)
    for a in assistants:
        last_group_dates[assistants[a][4]].append(last_duty_dates[a])
    for g in last_group_dates:
        last_group_dates[g] = sorted(last_group_dates[g])[-1]
    successful_count = 0
    combinations = []

    for i, combination in enumerate(generate_combinations(first_date, last_duty_dates, last_group_dates)):
        
        if not check_combination(combination, finished=True):
           continue
        # print(successful_count)
        # raise Exception(combination)
        successful_count += 1
        combinations.append(combination)
        if not (successful_count % 10) or successful_count == 1:
           print(successful_count, combination)
        
        if i > 1000:
          break

       
    print(f"found {successful_count}")
    combinations.sort(key=sort_combination)
    for i, combination in enumerate(combinations[:40]):
        headers = ["name"] + [str(i.day) for i in daterange()]
        table = [ [d] + [ c[0].isoweekday() if c[1] == d else "" for c in combination] for d in duties]
        table.append(["-" for i in daterange()])
        counts = defaultdict(int)
        for c in combination:
            counts[c[2]] += 1
        table += [ [a + f"({counts[a]})"] + [ c[0].isoweekday() if c[2] == a else "" for c in combination] for a in assistants]

        res = tabulate(table, headers=headers,  tablefmt="plain")
        with open(f"results/test_{i}.txt", "w") as f:
            f.write(tabulate(table, headers=headers,  tablefmt="pretty"))
        
    return 0

# --------------------------
if __name__ == '__main__':    
    generate()
