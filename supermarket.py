import random    

class Node:                 #برای لیست پیوندی صف
    def __init__(self, data):
        self.data = data
        self.next = None 
        
class Queue:
    def __init__(self):
        self.front = None   
        self.rear = None     
        self._size = 0

    def enqueue(self, item):    #برای اضافه کردن به ته صف
        new_node = Node(item)
        if self.rear is None:           # صف خالی بود
            self.front = new_node
            self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self._size += 1

    def dequeue(self):   #حذف از سر صف
        if self.front is None:
            return None
        item = self.front.data
        self.front = self.front.next
        if self.front is None:          # صف خالی شد
            self.rear = None
        self._size -= 1
        return item

    def is_empty(self):
        return self.front is None

    def size(self):
        return self._size

    def peek(self):   #فقط برای نشون دادن نفر اول بدون حذف
        if self.front:
            return self.front.data
        return None


class Customer:
    def __init__(self, arrival_time, service_time):
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.wait_time = 0

class Checkout:
    def __init__(self):
        self.waiting = Queue()              # صف مشتریان منتظر این صندوق
        self.current_customer = None        # مشتری در حال سرویس
        self.remaining_time = 0

def simulate():    #تابع شبیه سازی سوپر
    print("شبیه‌سازی صف صندوق فروشگاه\n")

    n = int(input("تعداد صندوق‌ها: "))
    T = int(input("مدت زمان شبیه‌سازی (دقیقه): "))
    p = float(input("احتمال ورود مشتری در هر دقیقه (0 تا 1): "))
    min_t = int(input("حداقل زمان سرویس (دقیقه): "))
    max_t = int(input("حداکثر زمان سرویس (دقیقه): "))

    checkouts = [Checkout() for _ in range(n)]

    arrived = 0
    served = 0
    total_wait = 0
    max_wait = 0
    sum_queue_lengths = 0

    for t in range(1, T + 1):
        if random.random() < p:  #عدد رندوم باید کوچکتر از پی باشه تا مشتری بیاد
            service_time = random.randint(min_t, max_t)  #عدد رندوم صحیح
            cust = Customer(t, service_time)

            # کوتاه‌ترین "کل خط صندوق" رو پیدا کن (صف انتظار + مشتری در حال سرویس)
            min_idx = 0
            min_len = checkouts[0].waiting.size() + (1 if checkouts[0].current_customer is not None else 0)

            for i in range(1, n):
                curr_len = checkouts[i].waiting.size() + (1 if checkouts[i].current_customer is not None else 0)
                if curr_len < min_len:
                    min_len = curr_len
                    min_idx = i

            checkouts[min_idx].waiting.enqueue(cust)
            arrived += 1

        # پردازش هر صندوق
        for ch in checkouts:
            # اگر مشتری فعلی نداریم → مشتری جدید بگیر
            if ch.current_customer is None and not ch.waiting.is_empty():
                cust = ch.waiting.dequeue()
                cust. wait_time = t - cust.arrival_time
                ch.current_customer = cust
                ch.remaining_time = cust.service_time

            # یک دقیقه سرویس بده
            if ch.current_customer is not None:
                ch.remaining_time -= 1
                if ch.remaining_time <= 0:
                    served += 1
                    total_wait += ch.current_customer.wait_time
                    max_wait = max(max_wait, ch.current_customer.wait_time)
                    ch.current_customer = None
                    ch.remaining_time = 0

        # جمع طول صف‌ها (فقط منتظرها) در این لحظه
        sum_queue_lengths += sum(ch.waiting.size() for ch in checkouts)
    
    # محاسبه دقیق مشتریان باقی‌مانده (در صف + در حال سرویس)
    left_in_queues = sum(ch.waiting.size() for ch in checkouts)
    in_service = sum(1 for ch in checkouts if ch.current_customer is not None)
    remaining = left_in_queues + in_service

    # گزارش
    print("\n" + "═" * 50)
    print("          گزارش نهایی شبیه‌سازی")
    print("═" * 50)
    print(f"تعداد مشتریان وارد شده          : {arrived}")
    print(f"تعداد مشتریان سرویس‌شده          : {served}")
    print(f"مشتریان باقی‌مانده (صف/سرویس)    : {remaining}")
    if served > 0:
        print(f"میانگین زمان انتظار               : {total_wait / served:.2f} دقیقه") #تا دو رقم اعشار
    print(f"بیشترین زمان انتظار مشاهده‌شده     : {max_wait} دقیقه")
    print(f"میانگین طول کل صف‌های انتظار در زمان : {sum_queue_lengths / T:.2f}") # به طور متوسط در هر دقیقه چند نفر در صف انتظار بودند
    print("═" * 50)


if __name__ == "__main__":
    simulate()
                     