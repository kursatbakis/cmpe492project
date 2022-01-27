import pymongo
from scheduler.models import Instructor, Classroom, TimeSlot, Course, InstructorAvailableSlot

INSTRUCTOR = 'instructor'
CLASSROOM = 'classroom'
COURSE = 'course'
AVAILABLE_SLOTS = 'instructorAvailableSlots'
TIME_SLOT = 'time_slot'


def get_db_collection(collection_name):
    client = pymongo.MongoClient(
        "mongodb+srv://admin:01237@cmpe492.dbcdq.mongodb.net/Scheduler?retryWrites=true&w=majority")
    db = client['Scheduler']
    collection = db[collection_name]
    return collection


def get_all_instructors():
    collection = get_db_collection(INSTRUCTOR)
    instructors = collection.find()
    all_instructors = []
    for instructor in instructors:
        i = Instructor(instructor)
        all_instructors.append(i)
    return all_instructors


def get_all_classrooms():
    collection = get_db_collection(CLASSROOM)
    classrooms = collection.find()
    all_classrooms = []
    for classroom in classrooms:
        i = Classroom(classroom)
        all_classrooms.append(i)
    return all_classrooms


def get_all_courses():
    collection = get_db_collection(COURSE)
    courses = collection.find()
    all_courses = []
    for course in courses:
        i = Course(course)
        all_courses.append(i)
    return all_courses


def get_all_slots():
    collection = get_db_collection(TIME_SLOT)
    slots = collection.find()
    all_slots = []
    for slot in slots:
        i = TimeSlot(slot)
        all_slots.append(i)
    return all_slots


def get_all_available_slots():
    collection = get_db_collection(AVAILABLE_SLOTS)
    slots = collection.find()
    all_slots = []
    for slot in slots:
        all_slots.append(InstructorAvailableSlot(slot))
    return all_slots


def map_object_id_to_time_slots(objectIdList):
    collection = get_db_collection(TIME_SLOT)
    return [TimeSlot(collection.find({'_id': x})) for x in objectIdList]


def getRelatedSlots(slot):
    if slot.length == 1:
        return [slot]

    if slot.length == 2:
        filtered = filter(lambda s: s.day == slot.day and s.length == 1 and (s.slot == slot.slot or s.slot == slot.slot + 1), allSlots)
        filtered2 = filter(lambda s: s.day == slot.day and s.length == 2 and abs(s.slot - slot.slot) <= 1, allSlots)
        return list(filtered) + list(filtered2)



allInstructors = get_all_instructors()
allCourses = get_all_courses()
allClassrooms = get_all_classrooms()
allSlots = get_all_slots()