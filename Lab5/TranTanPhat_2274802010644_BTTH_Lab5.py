import threading
import random
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

TOTAL_TICKETS = 1_000_000
MAX_TICKETS_PER_BUYER = 10
MATCH_NUMBERS_TO_WIN = 3
MIN_WINNERS = 10
PRIZE_PER_WINNER = 1_000_000
NUMBERS_PER_TICKET = 3
NUMBER_RANGE = 100
COUNTDOWN_TIME = 300
MAX_WORKERS = 500  


class Lottery:
    def __init__(self):
        self.tickets_sold = 0
        self.tickets = []
        self.lock = threading.Lock()
        self.winning_numbers = []
        self.sold_out = False
        self.buyer_tickets = {}
        self.total_buyers = 0
        self.remaining_time = COUNTDOWN_TIME

    def sell_ticket(self, buyer_id):
        with self.lock:
            if self.sold_out:
                return False

            tickets_available = TOTAL_TICKETS - self.tickets_sold
            tickets_to_sell = min(random.randint(1, MAX_TICKETS_PER_BUYER), tickets_available)

            if tickets_to_sell == 0:
                self.sold_out = True
                return False

            buyer_tickets_list = []
            for _ in range(tickets_to_sell):
                ticket = [random.randint(0, NUMBER_RANGE - 1) for _ in range(NUMBERS_PER_TICKET)]
                self.tickets.append((buyer_id, ticket))
                buyer_tickets_list.append(ticket)
                self.tickets_sold += 1

            self.buyer_tickets[buyer_id] = buyer_tickets_list
            self.total_buyers += 1
            print(f" {self.remaining_time}s | Buyer {buyer_id} đã mua {tickets_to_sell} vé: {buyer_tickets_list}")

            if self.tickets_sold >= TOTAL_TICKETS:
                self.sold_out = True
                print(f"\n {self.remaining_time}s | Đã bán đủ {TOTAL_TICKETS} vé, dừng bán vé!\n")
            return True

    def draw_winning_numbers(self):
        self.winning_numbers = [random.randint(0, NUMBER_RANGE - 1) for _ in range(NUMBERS_PER_TICKET)]
        print(f"\n Kết quả xổ số: {self.winning_numbers}\n")

    def check_winners(self):
        winners = []
        for buyer_id, tickets in self.buyer_tickets.items():
            for ticket in tickets:
                matches = len(set(ticket) & set(self.winning_numbers))
                if matches >= MATCH_NUMBERS_TO_WIN:
                    winners.append((buyer_id, ticket, matches))
        return winners


def buyer_task(buyer_id, lottery):
    while not lottery.sold_out:
        time.sleep(random.uniform(1.0, 2.0))  
        if lottery.sell_ticket(buyer_id):
            break


def countdown(lottery):
    while lottery.remaining_time > 0:
        with lottery.lock:
            if lottery.sold_out:
                break
            lottery.remaining_time -= 1
        time.sleep(1)
    with lottery.lock:
        lottery.sold_out = True
    print("\n Hết thời gian! Dừng bán vé và tiến hành quay số.\n")


def main():
    lottery = Lottery()
    buyer_id = 0

    print(" Bắt đầu bán vé...\n")
    start_time = datetime.now()

    countdown_thread = threading.Thread(target=countdown, args=(lottery,))
    countdown_thread.start()

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        while not lottery.sold_out:
            futures.append(executor.submit(buyer_task, buyer_id, lottery))
            buyer_id += 1
            time.sleep(0.01)  

        for future in as_completed(futures):
            pass  

    countdown_thread.join()

    end_time = datetime.now()
    print(f"\n Tổng vé đã bán: {lottery.tickets_sold} vé với {lottery.total_buyers} người mua.")
    print(f" Thời gian bán vé: {(end_time - start_time).total_seconds():.2f} giây.\n")

    attempt = 1
    while True:
        print(f" Lần quay số thứ {attempt}")
        lottery.draw_winning_numbers()
        winners = lottery.check_winners()

        if len(winners) >= MIN_WINNERS:
            break
        else:
            print(f" Chỉ có {len(winners)} vé trúng thưởng. Quay lại...\n")
            attempt += 1

    total_prize = len(winners) * PRIZE_PER_WINNER
    print("\n Danh sách người trúng thưởng:")
    for buyer_id, ticket, matches in winners:
        print(f" - Buyer {buyer_id} với vé {ticket} ({matches} số trùng) => Nhận {PRIZE_PER_WINNER:,} VND")

    print(f"\n Tổng giải thưởng đã trao: {total_prize:,} VND\n")
    print(f" Tổng số vé trúng thưởng: {len(winners)}")

    with open("result.txt", "w") as f:
        f.write(f"Kết quả xổ số: {lottery.winning_numbers}\n")
        f.write(f"Tổng vé đã bán: {lottery.tickets_sold}\n")
        f.write(f"Số người mua: {lottery.total_buyers}\n")
        f.write(f"Số vé trúng thưởng: {len(winners)}\n")
        for buyer_id, ticket, matches in winners:
            f.write(f"Buyer {buyer_id} - Vé {ticket} ({matches} số trùng)\n")
        f.write(f"Tổng giải thưởng: {total_prize:,} VND\n")


if __name__ == "__main__":
    main()
