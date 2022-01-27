import argparse
import csv
from utils import *
from addModels import *
import gurobiSolver
# 1-Hoca available slotlarini verir = hocanin ismi, csv dosyasi
# 2-Hoca verecegi dersleri verir = hocanin ismi, csv dosyasi
# 3-Sistem solveri calistirir
# MONDAY, 1
# TUESDAY, 5
# TUESDAY, 8
# TUESDAY, 6

def add_slots_to_db(reader, name):
    collection = get_db_collection('instructorAvailableSlots')
    slots = get_db_collection('time_slot')
    instructors = get_db_collection('instructor')
    instructor = instructors.find_one({'full_name': name})
    arr = []
    print(name)
    reader = sorted(reader)
    for i in range(len(reader)-1):
        if len(reader[i]) == 0:
            continue
        if reader[i][0] == reader[i+1][0] and int(reader[i][1]) == int(reader[i+1][1]) - 1:
            query = {
                'day': reader[i][0].upper(),
                'length': 2,
                'slot': int(reader[i][1])
            }
            slot = slots.find_one(query)
            arr.append(slot)

    for row in reader:
        if len(row) == 0:
            continue
        query = {
            'day': row[0].upper(),
            'length': 1,
            'slot': int(row[1])
        }
        slot = slots.find_one(query)
        arr.append(slot)

    collection.insert_one({
        'instructor': instructor,
        'slots': arr
    })
    print('inserted to db')

def add_courses_to_db(reader, name):
    instructors = get_db_collection('instructor')
    courses = get_db_collection('course')
    arr = []
    for course in reader:
        json = {
            'department': course[0],
            'code': int(course[1]),
            'section': int(course[2]),
            'quota': int(course[3]),
            'hours': int(course[4])
        }
        result = courses.insert_one(json)
        arr.append(result.inserted_id)

    instructors.find_one_and_update({'full_name': name}, {'$set': {'courses': arr}})

def main():
    parser = argparse.ArgumentParser(description='Project parser')
    parser.add_argument('mode', type=int,
                        help='A value that indicates the run mode. 1 for adding courses and available slots. "slots_<surname> and courses_<surname>, 2 for running gurobi solver.')
    parser.add_argument('--name', type=str, help='Instructor name')
    args = parser.parse_args()
    if args.mode == 2:
        gurobiSolver.solve()
        return

    instructor_name = args.name
    lastname = instructor_name.split()[-1].lower()
    course_csv_path = "CSV/courses_{}.csv".format(lastname)
    slots_csv_path = "CSV/slots_{}.csv".format(lastname)
    course_csv_file = open(course_csv_path)
    slots_csv_file = open(slots_csv_path)
    course_csv_reader = csv.reader(course_csv_file)
    slots_csv_reader = csv.reader(slots_csv_file)

    add_slots_to_db(slots_csv_reader, instructor_name)
    add_courses_to_db(course_csv_reader, instructor_name)

if __name__ == '__main__':
    main()
