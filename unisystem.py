import csv
    
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def length(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def to_list(self):  #فقط برای محاسبات و مرتب‌سازی linkedlist into list
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result


class Student:
    def __init__(self, name, student_id, gpa):
        self.name = name
        self.student_id = student_id
        self.gpa = float(gpa)

    def __str__(self):
        return f"{self.name} ({self.student_id}) - معدل: {self.gpa:.2f}"


class Professor:
    def __init__(self, name, professor_id):
        self.name = name
        self.professor_id = professor_id

    def __str__(self):
        return f"{self.name} ({self.professor_id})"


class Major:
    def __init__(self, name, space_sqm):
        self.name = name
        self.space = float(space_sqm)
        self.students = LinkedList()
        self.professors = LinkedList()

    def __str__(self):
        return self.name


def find_major(majors_ll, major_name):  #it has a ll of major and a name  to find
    current = majors_ll.head
    while current:
        if current.data.name == major_name:
            return current.data
        current = current.next
    return None


def load_from_csv(filename):  #it takes info from csv and gives it to ll
    majors = LinkedList()
   
    try:
        with open(filename, "r", encoding="utf-8-sig", newline="") as f:  
            reader = csv.DictReader(f)  #every row of csv would be read like dict
            required = {"type", "major", "space_sqm", "name", "id", "gpa"}
            if not required.issubset(set(reader.fieldnames or [])):  
                print("فرمت CSV درست نیست. ستون‌های لازم:", required)
                return majors

            for row in reader:
                row_type = (row["type"] or "").strip().lower()
                major_name = (row["major"] or "").strip()
                space = (row["space_sqm"] or "").strip()
                name = (row["name"] or "").strip()
                _id = (row["id"] or "").strip()
                gpa = (row["gpa"] or "").strip()

                if not major_name:
                    continue

                # تعریف رشته
                if row_type == "major":
                    m = find_major(majors, major_name)
                    if not m:
                        majors.append(Major(major_name, space if space else 0))
                    else:
                        if space:
                            m.space = float(space)

                # دانشجو
                elif row_type == "student":
                    m = find_major(majors, major_name)
                    if not m:
                        # اگر رشته قبلش نیومده بود، بسازش
                        majors.append(Major(major_name, 0))
                        m = find_major(majors, major_name)
                    if name and _id and gpa:
                        m.students.append(Student(name, _id, gpa))

                # استاد
                elif row_type in ("prof", "professor"):
                    m = find_major(majors, major_name)
                    if not m:
                        majors.append(Major(major_name, 0))
                        m = find_major(majors, major_name)
                    if name and _id:
                        m.professors.append(Professor(name, _id))

        print(f" اطلاعات از فایل '{filename}' بارگذاری شد.")
        return majors

    except FileNotFoundError:
        print(f"فایل پیدا نشد: {filename}")
        return majors
    except Exception as e:
        print(" خطا در خواندن CSV:", e)
        return majors
 
  #توابع مورد نیاز

def show_number_of_students(majors_ll):
    print("\n=== تعداد دانشجویان هر رشته ===")
    majors = majors_ll.to_list()
    for major in majors:
        num = major.students.length()
        print(f"رشته {major.name}: {num} دانشجو")


def show_top_3_students(majors_ll):
    print("\n=== ۳ دانشجوی برتر هر رشته (بر اساس معدل) ===")
    majors = majors_ll.to_list()
    for major in majors:
        students = major.students.to_list()
        if not students:
            print(f"رشته {major.name}: دانشجویی ثبت نشده")
            continue
        top3 = sorted(students, key=lambda s: s.gpa, reverse=True)[:3]  
        print(f"\nرشته {major.name}:")
        for i, student in enumerate(top3, 1):
            print(f"  {i}. {student}")


def show_average_gpa(majors_ll):
    print("\n=== میانگین معدل دانشجویان هر رشته ===")
    majors = majors_ll.to_list()
    for major in majors:
        students = major.students.to_list()
        avg = (sum(s.gpa for s in students) / len(students)) if students else 0
        print(f"رشته {major.name}: {avg:.2f}")


def show_professor_ratio(majors_ll):
    print("\n=== تعداد اساتید و نسبت استاد به دانشجو ===")
    majors = majors_ll.to_list()
    for major in majors:
        num_prof = major.professors.length()
        num_std = major.students.length()

        if num_std == 0:
            ratio_str = "تعریف‌ نشده (دانشجو ندارد)"
        else:
            ratio_str = f"{num_prof/num_std:.2f}"

        print(f"رشته {major.name}: {num_prof} استاد | دانشجو: {num_std} | نسبت استاد/دانشجو: {ratio_str}")


def show_space_per_student(majors_ll):
    print("\n=== نسبت فضای فیزیکی به هر دانشجو (متر مربع) ===")
    majors = majors_ll.to_list()
    for major in majors:
        num = major.students.length()
        if num == 0:
            print(f"رشته {major.name}: دانشجویی وجود ندارد")
        else:
            ratio = major.space / num
            print(f"رشته {major.name}: {ratio:.1f} متر مربع به ازای هر دانشجو")




def main():
    print("=== سامانه مدیریت اطلاعات دانشگاه (با Linked List) ===\n")

    majors = LinkedList()  

    while True:
        print("\nمنو:")
        print("1. نمایش تعداد دانشجویان هر رشته")
        print("2. نمایش ۳ دانشجوی برتر هر رشته")
        print("3. نمایش میانگین معدل هر رشته")
        print("4. نمایش نسبت تعداد اساتید به دانشجو در هر رشته")
        print("5. نمایش نسبت فضای فیزیکی به هر دانشجو")
        print("6. بارگذاری اطلاعات از فایل CSV")
        print("7. خروج")

        choice = input("\nانتخاب کنید (1-7): ").strip()

        if choice == "1":
            show_number_of_students(majors)
        elif choice == "2":
            show_top_3_students(majors)
        elif choice == "3":
            show_average_gpa(majors)
        elif choice == "4":
            show_professor_ratio(majors)
        elif choice == "5":
            show_space_per_student(majors)
        elif choice == "6":
            filename = input("نام فایل CSV (مثلاً data.csv): ").strip()
            majors = load_from_csv(filename)
        elif choice == "7":
            print("khodahafez")
            break
        else:
            print("ورودی نامعتبر!")

        input("\nبرای ادامه Enter بزن...")


if __name__ == "__main__":
    main()