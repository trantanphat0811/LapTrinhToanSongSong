import threading
import time
import random
import queue

class ApartmentManager:
    def __init__(self, num_rooms=5, total_girlfriends=10):
        self.num_rooms = num_rooms
        self.rooms = [False] * num_rooms  # False: phòng trống, True: có người
        self.waiting_queue = queue.Queue()
        self.lock = threading.Lock()
        self.total_girlfriends = total_girlfriends

    def display_status(self):
        """ Hiển thị trạng thái phòng và hàng đợi """
        with self.lock:
            room_status = "".join("[X]" if occupied else "[ ]" for occupied in self.rooms)
            queue_size = self.waiting_queue.qsize()
            print(f"{room_status}  Hàng đợi: {queue_size} người đang chờ")

    def use_room(self, girlfriend_id):
        """ Xử lý khi một bạn gái đến sử dụng phòng """
        # Giả lập thời gian đến ngẫu nhiên
        time.sleep(random.uniform(5, 20))

        with self.lock:
            print(f"Bạn gái {girlfriend_id} đã đến!")
            self.display_status()

        # Chờ phòng trống
        while True:
            with self.lock:
                available_room = next((i for i, occupied in enumerate(self.rooms) if not occupied), -1)

                if available_room != -1:
                    # Chiếm phòng
                    self.rooms[available_room] = True
                    self.display_status()
                    break
                else:
                    # Không có phòng trống, phải vào hàng đợi
                    print(f"Bạn gái {girlfriend_id} phải chờ!")
                    self.waiting_queue.put(girlfriend_id)
                    self.display_status()

            time.sleep(1)  # Chờ 1 giây rồi kiểm tra lại

        # Giả lập thời gian sử dụng phòng
        usage_time = random.uniform(5, 10)
        time.sleep(usage_time)

        # Giải phóng phòng
        with self.lock:
            self.rooms[available_room] = False
            print(f"Bạn gái {girlfriend_id} đã rời đi sau {usage_time:.2f}s")
            self.display_status()

            # Kiểm tra hàng đợi
            if not self.waiting_queue.empty():
                next_girlfriend = self.waiting_queue.get()
                print(f"Bạn gái {next_girlfriend} được vào từ hàng đợi!")
                threading.Thread(target=self.use_room, args=(next_girlfriend,), daemon=True).start()

def main():
    manager = ApartmentManager()
    print("Bắt đầu mô phỏng quản lý phòng nhà ở!")
    manager.display_status()

    threads = []
    for gf_id in range(1, 11):
        t = threading.Thread(target=manager.use_room, args=(gf_id,), daemon=True)
        threads.append(t)
        t.start()

    time.sleep(60)  # Chạy mô phỏng trong 60 giây
    print("\nKết thúc mô phỏng!")

if __name__ == "__main__":
    main()
