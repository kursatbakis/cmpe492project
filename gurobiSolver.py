import gurobipy as gp
from gurobipy import GRB
from scheduler.utils import *
import csv

W = {}
days = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"]
departments = ["CMPE"]


def create_W_matrix():
    global W
    allAvailableSlots = get_all_available_slots()
    for availableSlot in allAvailableSlots:
        for slot in availableSlot.slots:
            if slot is None:
                continue
            if availableSlot.instructor in W:
                W[availableSlot.instructor].append(TimeSlot(slot))
            else:
                W[availableSlot.instructor] = [TimeSlot(slot)]


def does_intersect(slot1, slot2):
    if slot1.day != slot2.day:
        return False
    if slot1.slot == slot2.slot:
        return True
    if slot1.length == 2 and slot1.slot + 1 == slot2.slot:
        return True
    if slot2.length == 2 and slot2.slot + 1 == slot1.slot:
        return True
    return False


def solve():
    m = gp.Model('Scheduling')
    create_W_matrix()

    X = m.addVars(allInstructors, allCourses, allSlots, allClassrooms, name="X", vtype=GRB.BINARY)

    constr1 = m.addConstrs(
        gp.quicksum(X[f, c, s, r] for c in allCourses for r in allClassrooms) <= 1 for f in allInstructors for s in
        allSlots)

    constr2 = m.addConstrs(
        (gp.quicksum(X[f, c, s, r] for f in allInstructors for c in allCourses) <= 1 for s in allSlots for r in
         allClassrooms))

    constr3 = m.addConstrs((gp.quicksum(
        X[f, c, s, r] * c.quota for f in allInstructors for s in allSlots) <= gp.quicksum(
        X[f, c, s, r] * r.capacity for f in allInstructors for s in allSlots))
                           for c in allCourses for r in allClassrooms)

    constr4 = m.addConstrs(
        gp.quicksum(X[f, c, s, r] for c in allCourses for r in allClassrooms) == 0 for f in allInstructors for s in
        allSlots if f.id in W and s not in W[f.id])

    constr5 = m.addConstrs(gp.quicksum(
        X[f, c, s, r] * s.length for s in allSlots for r in allClassrooms for f in allInstructors) == c.hours for c in
                           allCourses)

    constr6 = m.addConstrs(
        gp.quicksum(X[f, c, s, r] for s in allSlots for r in allClassrooms) == 0 for f in allInstructors for c in
        allCourses if c.id not in f.courses)

    constr7 = m.addConstrs(
        gp.quicksum(X[f, c, rs, r] for rs in getRelatedSlots(s) for r in allClassrooms for c in allCourses) <= 1
        for f in allInstructors for s in allSlots)

    constr8 = m.addConstrs(
        gp.quicksum(X[f, c, s, r] for r in allClassrooms for f in allInstructors for s in allSlots if s.day == d) <= 1
        for d in days for c in allCourses)

    # Dersleri 2 + 1 seklinde ayirabilmek icin.
    constr9 = m.addConstrs(
        gp.quicksum(X[f, c, s, r] for r in allClassrooms for s in allSlots) <= 2 for f in allInstructors for c in
        allCourses
    )

    constr11 = m.addConstrs(
        gp.quicksum(X[f, c, rs, r] for rs in getRelatedSlots(s) for f in allInstructors for c in allCourses) <= 1
        for r in allClassrooms for s in allSlots)

    #  constr10 = m.addConstrs(
    #     gp.quicksum(X[f, c, ss, r] for c in allCourses if 100 * Class <= c.code < 100 * (Class + 1) and c.department == d for f in allInstructors for r in allClassrooms for ss in allSlots if does_intersect(ss, s)) <= 1 for Class in range(1, 5) for d in departments for s in allSlots
    # )

    obj = gp.quicksum(
        X[f, c, s, r] for f in allInstructors for s in allSlots for c in allCourses for r in allClassrooms)
    m.setObjective(obj, GRB.MAXIMIZE)
    m.optimize()
    solution = m.getAttr('X', X)
    for instructor, course, slot, classroom in X.keys():
        if solution[instructor, course, slot, classroom] > 0.5:
            with open('results/{}.csv'.format(classroom.code), 'a+') as f:
                writer = csv.writer(f)
                writer.writerow(
                    [slot.day, slot.slot, slot.length, instructor.full_name, course.department, course.code])
            with open('results/{}.csv'.format(instructor.full_name), 'a+') as f:
                writer = csv.writer(f)
                writer.writerow([slot.day, slot.slot, slot.length, classroom.code, course.department, course.code])
