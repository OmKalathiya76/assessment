
# DA Assessment - Core Python — OOP Solutions
# Generated: October 13, 2025
# Classes: ClinicAppointment, SchoolManagement, BusReservation
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import itertools, re, uuid

# -------- ClinicAppointment --------
@dataclass
class Appointment:
    name: str
    age: int
    mobile: str
    doctor: str
    slot: str  # '10am','11am','12pm','2pm','3pm'
    appt_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

class ClinicAppointment:
    def __init__(self, doctors: List[str]):
        self.doctors = doctors
        self.slots = ["10am","11am","12pm","2pm","3pm"]
        self.max_per_slot = 3
        self.bookings: Dict[str, Dict[str, List[Appointment]]] = {
            d: {s: [] for s in self.slots} for d in self.doctors
        }
        self.by_mobile: Dict[str, Appointment] = {}

    def book(self, name: str, age: int, mobile: str, doctor: str, slot: str) -> str:
        if doctor not in self.doctors:
            raise ValueError("Unknown doctor")
        if slot not in self.slots:
            raise ValueError("Invalid slot")
        if not re.fullmatch(r"\d{10}", mobile):
            raise ValueError("Mobile must be 10 digits")
        bucket = self.bookings[doctor][slot]
        if len(bucket) >= self.max_per_slot:
            raise RuntimeError("Slot full")
        appt = Appointment(name, age, mobile, doctor, slot)
        bucket.append(appt)
        self.by_mobile[mobile] = appt
        return appt.appt_id

    def view(self, mobile: str) -> Optional[Appointment]:
        return self.by_mobile.get(mobile)

    def cancel(self, mobile: str) -> bool:
        appt = self.by_mobile.pop(mobile, None)
        if not appt:
            return False
        bucket = self.bookings[appt.doctor][appt.slot]
        self.bookings[appt.doctor][appt.slot] = [a for a in bucket if a.appt_id != appt.appt_id]
        return True

# -------- SchoolManagement --------
@dataclass
class Student:
    student_id: int
    name: str
    age: int
    std_class: int
    guardian_mobile: str

class SchoolManagement:
    def __init__(self):
        self._id_counter = itertools.count(1001)
        self.students: Dict[int, Student] = {}

    def _validate(self, age: int, std_class: int, mobile: str):
        if not (5 <= age <= 18):
            raise ValueError("Age must be between 5 and 18")
        if not (1 <= std_class <= 12):
            raise ValueError("Class must be 1–12")
        if not re.fullmatch(r"\d{10}", mobile):
            raise ValueError("Guardian mobile must be 10 digits")

    def admit(self, name: str, age: int, std_class: int, guardian_mobile: str) -> int:
        self._validate(age, std_class, guardian_mobile)
        sid = next(self._id_counter)
        self.students[sid] = Student(sid, name, age, std_class, guardian_mobile)
        return sid

    def view(self, student_id: int) -> Optional[Student]:
        return self.students.get(student_id)

    def update_mobile(self, student_id: int, new_mobile: str) -> bool:
        if not re.fullmatch(r"\d{10}", new_mobile):
            raise ValueError("Mobile must be 10 digits")
        st = self.students.get(student_id)
        if not st:
            return False
        st.guardian_mobile = new_mobile
        return True

    def update_class(self, student_id: int, new_class: int) -> bool:
        if not (1 <= new_class <= 12):
            raise ValueError("Class must be 1–12")
        st = self.students.get(student_id)
        if not st:
            return False
        st.std_class = new_class
        return True

    def remove(self, student_id: int) -> bool:
        return self.students.pop(student_id, None) is not None

# -------- BusReservation --------
@dataclass
class Ticket:
    ticket_id: str
    name: str
    age: int
    mobile: str
    route: str
    seat_no: int
    price: int

class BusReservation:
    def __init__(self, routes_with_price: Dict[str, int], capacity: int = 40):
        self.routes_with_price = routes_with_price
        self.capacity = capacity
        self.tickets: Dict[str, List[Ticket]] = {r: [] for r in routes_with_price}

    def available_routes(self) -> Dict[str, int]:
        return dict(self.routes_with_price)

    def _next_seat(self, route: str) -> int:
        return len(self.tickets[route]) + 1

    def book(self, name: str, age: int, mobile: str, route: str) -> str:
        if route not in self.routes_with_price:
            raise ValueError("Unknown route")
        if not re.fullmatch(r"\d{10}", mobile):
            raise ValueError("Mobile must be 10 digits")
        if len(self.tickets[route]) >= self.capacity:
            raise RuntimeError("Bus full for this route")
        seat = self._next_seat(route)
        price = self.routes_with_price[route]
        tid = str(uuid.uuid4())[:8]
        self.tickets[route].append(Ticket(tid, name, age, mobile, route, seat, price))
        return tid

    def view(self, ticket_id: str) -> Optional[Ticket]:
        for route_list in self.tickets.values():
            for t in route_list:
                if t.ticket_id == ticket_id:
                    return t
        return None

    def cancel(self, ticket_id: str) -> bool:
        for route, lst in self.tickets.items():
            for i, t in enumerate(lst):
                if t.ticket_id == ticket_id:
                    del lst[i]
                    return True
        return False

if __name__ == "__main__":
    clinic = ClinicAppointment(doctors=["Dr. Shah","Dr. Patel"])
    appt_id = clinic.book("Aarav", 27, "9876543210", "Dr. Shah", "10am")
    print("Booked appointment:", appt_id, clinic.view("9876543210"))

    school = SchoolManagement()
    sid = school.admit("Neha", 12, 7, "9123456789")
    print("Admitted student:", sid, school.view(sid))

    routes = {"Mumbai to Pune": 500, "Delhi to Jaipur": 600}
    bus = BusReservation(routes)
    tid = bus.book("Riya", 30, "9988776655", "Mumbai to Pune")
    print("Booked ticket:", tid, bus.view(tid))
