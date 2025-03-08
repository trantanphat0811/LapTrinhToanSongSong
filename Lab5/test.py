import threading
import random
import time

TOTAL_TICKETS = 1_000_000
MAX_TICKETS_PER_BUYER = 10
MATCH_NUMBERS_TO_WIN = 3
PRINT_PROGRESS_EVERY = 100_000  


class Lottery:
    def __init__(self):
        self.tickets_sold = 0
        self.tickets = []
        self.lock = threading.Lock()
        self.winning_numbers = []
        self.sold_out = False
        self.buyer_tickets = {}
        self.total_buyers = 0

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
                ticket = [random.randint(0, 99) for _ in range(3)]
                self.tickets.append((buyer_id, ticket))
                buyer_tickets_list.append(ticket)
                self.tickets_sold += 1

                if self.tickets_sold % PRINT_PROGRESS_EVERY == 0:
                    print(f" Đã bán {self.tickets_sold} vé...")

            self.buyer_tickets[buyer_id] = buyer_tickets_list
            self.total_buyers += 1
            # Có thể bỏ hoặc giữ log này nếu muốn
            # print(f" Buyer {buyer_id} đã mua {tickets_to_sell} vé.")

            if self.tickets_sold >= TOTAL_TICKETS:
                self.sold_out = True
                print(f"\n  Đã bán đủ {TOTAL_TICKETS} vé, dừng bán vé!\n")
            return True

    def draw_winning_numbers(self):
        self.winning_numbers = [random.randint(0, 99) for _ in range(3)]
        print(f"\n Kết quả xổ số: {self.winning_numbers}\n")

    def check_winners(self):
        winners = []
        for buyer_id, tickets in self.buyer_tickets.items():
            for ticket in tickets:
                matches = len(set(ticket) & set(self.winning_numbers))
                if matches >= MATCH_NUMBERS_TO_WIN:
                    winners.append((buyer_id, ticket, matches))
        return winners


class Buyer(threading.Thread):
    def __init__(self, buyer_id, lottery):
        super().__init__()
        self.buyer_id = buyer_id
        self.lottery = lottery

    def run(self):
        time.sleep(random.uniform(0.0001, 0.001))  # Giảm thời gian chờ để tăng tốc
        if not self.lottery.sell_ticket(self.buyer_id):
            print(f" Buyer {self.buyer_id} không mua kịp vé...")


def main():
    lottery = Lottery()
    buyers = []
    buyer_id = 0

    print(" Bắt đầu bán vé...\n")

    while not lottery.sold_out:
        buyer = Buyer(buyer_id, lottery)
        buyers.append(buyer)
        buyer.start()
        buyer_id += 1

    for buyer in buyers:
        buyer.join()

    print(f"\n Tổng vé đã bán: {lottery.tickets_sold} vé với {lottery.total_buyers} người mua.\n")

    lottery.draw_winning_numbers()
    winners = lottery.check_winners()

    if winners:
        print(" Danh sách người trúng thưởng:")
        for buyer_id, ticket, matches in winners:
            print(f" - Buyer {buyer_id} với vé {ticket} ({matches} số trùng)")
    else:
        print(" Không có ai trúng thưởng.")


if __name__ == "__main__":
    main()
