from scheduler.utils import get_db_collection
import random

def removeThreeBlockSlots():
    collection = get_db_collection('time_slot')
    collection.delete_many({'length': 3})

def addSlots():
    collection = get_db_collection('time_slot')
    collection.delete_many({})
    days = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY']
    for i in range(1, 11):
        for length in range(1, 4):
            for day in days:
                if i + length - 1 > 10:
                    continue
                slot = {
                    'day': day,
                    'length': length,
                    'slot': i
                }
                collection.insert_one(slot)


def addInstructors():
    instructors = [{"full_name": "Emre Ugur"},
                   {"full_name": "Ali Akkaya"},
                   {"full_name": "Pinar Yolum"},
                   {"full_name": "Sadik Fikret Gurgen"},
                   {"full_name": "Arzucan Ozgur"},
                   {"full_name": "Can Ozturan"},
                   {"full_name": "Ethem Alpaydin"},
                   {"full_name": "Taylan Cemgil"},
                   {"full_name": "Arda Yurdakul"},
                   {"full_name": "Tuna Tugcu"},
                   {"full_name": "Suzan Uskudarli"},
                   {"full_name": "Cem Ersoy"},
                   {"full_name": "Cem Say"},
                   {"full_name": "Alper Şen"},
                   {"full_name": "Fatma Basak Aydemir"},
                   {"full_name": "Fatih Alagoz"},
                   {"full_name": "Haluk Bingol"},
                   ]
    collection = get_db_collection('instructor')
    collection.delete_many({})
    for instructor in instructors:
        collection.insert_one(instructor)


def addClassrooms():
    classrooms = [{"code": "BM-B5", "capacity": 30},
                  {"code": "BM-A3", "capacity": 60},
                  {"code": "BM-A6", "capacity": 25},
                  {"code": "BM-B4", "capacity": 80},
                  {"code": "NH401", "capacity": 200},
                  {"code": "NH405", "capacity": 250},
                  ]
    collection = get_db_collection('classroom')
    for classroom in classrooms:
        collection.insert_one(classroom)


def addCourses():
    courses = [{"department": "CMPE", "code": 150, "section": 1, "quota": 240},
               {"department": "CMPE", "code": 210, "section": 1, "quota": 70},
               {"department": "CMPE", "code": 220, "section": 1, "quota": 230},
               {"department": "CMPE", "code": 230, "section": 1, "quota": 126},
               {"department": "CMPE", "code": 250, "section": 1, "quota": 75},
               {"department": "CMPE", "code": 300, "section": 1, "quota": 100},
               {"department": "CMPE", "code": 322, "section": 1, "quota": 115},
               {"department": "CMPE", "code": 343, "section": 1, "quota": 95},
               {"department": "CMPE", "code": 344, "section": 1, "quota": 80},
               {"department": "CMPE", "code": 350, "section": 1, "quota": 50},
               {"department": "CMPE", "code": 436, "section": 1, "quota": 40},
               {"department": "CMPE", "code": 443, "section": 1, "quota": 131}
               ]
    collection = get_db_collection('course')
    collection.insert_many(courses)


def addHoursToCourses():
    collection = get_db_collection('course')
    collection.update_many({}, {"$set": {"hours": 2}})


def addAvailableSlots():
    collection = get_db_collection('instructorAvailableSlots')
    collection.delete_many({})
    days = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"]
    availableSlots = get_db_collection('instructorAvailableSlots')
    slots = get_db_collection('time_slot')
    instructors = get_db_collection('instructor')

    for ins in instructors.find():
        list = []
        for s in slots.find({"day": {'$ne': days[random.randint(0, 4)]}}):
            list.append(s["_id"])
        availableSlots.insert_one({"instructor": ins, "slots": list})
