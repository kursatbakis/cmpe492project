class Course:
    def __init__(self, json):
        self.department = json["department"]
        self.code = json["code"]
        self.section = json["section"]
        self.quota = json["quota"]
        self.hours = json["hours"]
        self.id = json["_id"]


class Instructor:
    def __init__(self, json):
        self.id = json["_id"]
        self.full_name = json["full_name"]
        if "courses" in json:
            self.courses = json["courses"]


class TimeSlot:
    def __init__(self, json):
        self.id = json["_id"]
        self.day = json["day"]
        self.slot = json["slot"]
        self.length = json["length"]

    def __lt__(self, other):
        allDays = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"]
        if self.day != other.day:
            return allDays.index(self.day) < allDays.index(other.day)
        return self.slot < other.slot

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

class Classroom:
    def __init__(self, json):
        self.code = json["code"]
        self.capacity = json["capacity"]


class InstructorAvailableSlot:
    def __init__(self, json):
        self.instructor = json['instructor']['_id']
        self.slots = json['slots']
