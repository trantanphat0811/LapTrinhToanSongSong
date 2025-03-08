import threading
import random
import time
from datetime import datetime
from collections import Counter

TOTAL_TICKETS = 1_000_000
MAX_TICKETS_PER_BUYER = 10
MATCH_NUMBERS_TO_WIN = 3
MIN_WINNERS = 3
PRIZE_PER_WINNER = 1_000_000  
NUMBERS_PER_TICKET = 3
NUMBER_RANGE = 100


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
                ticket = [random.randint(0, NUMBER_RANGE - 1) for _ in range(NUMBERS_PER_TICKET)]
                self.tickets.append((buyer_id, ticket))
                buyer_tickets_list.append(ticket)
                self.tickets_sold += 1

            self.buyer_tickets[buyer_id] = buyer_tickets_list
            self.total_buyers += 1
            print(f" Buyer {buyer_id} đã mua {tickets_to_sell} vé: {buyer_tickets_list}")

            if self.tickets_sold >= TOTAL_TICKETS:
                self.sold_out = True
                print(f"\n Đã bán đủ {TOTAL_TICKETS} vé, dừng bán vé!\n")
            return True

    def draw_winning_numbers(self):
        self.winning_numbers = [random.randint(0, NUMBER_RANGE - 1) for _ in range(NUMBERS_PER_TICKET)]
        print(f"\n  Kết quả xổ số: {self.winning_numbers}\n")

    def check_winners(self):
        winners = []
        for buyer_id, tickets in self.buyer_tickets.items():
            for ticket in tickets:
                matches = sum(1 for i in range(NUMBERS_PER_TICKET) if ticket[i] == self.winning_numbers[i])
                if matches >= MATCH_NUMBERS_TO_WIN:
                    winners.append((buyer_id, ticket, matches))
        return winners


class Buyer(threading.Thread):
    def __init__(self, buyer_id, lottery):
        super().__init__()
        self.buyer_id = buyer_id
        self.lottery = lottery

    def run(self):
        while not self.lottery.sold_out:
            time.sleep(random.uniform(0.01, 0.05))
            if self.lottery.sell_ticket(self.buyer_id):
                break


def main():
    lottery = Lottery()
    buyers = []
    buyer_id = 0

    print("🏁 Bắt đầu bán vé...\n")
    start_time = datetime.now()

    while not lottery.sold_out:
        buyer = Buyer(buyer_id, lottery)
        buyers.append(buyer)
        buyer.start()
        buyer_id += 1

    for buyer in buyers:
        buyer.join()

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
        print(f" - Buyer {buyer_id} với vé {ticket} ({matches} số trùng đúng vị trí) => Nhận {PRIZE_PER_WINNER:,} VND")

    print(f"\n Tổng giải thưởng đã trao: {total_prize:,} VND\n")
    print(f" Tổng số vé trúng thưởng: {len(winners)}")

    buyer_ticket_counts = {buyer_id: len(tickets) for buyer_id, tickets in lottery.buyer_tickets.items()}
    top_buyers = Counter(buyer_ticket_counts).most_common(5)

    with open("result.txt", "w") as f:
        f.write("=== BÁO CÁO KẾT QUẢ XỔ SỐ ===\n\n")
        f.write(f"🕒 Thời gian bắt đầu bán vé: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"🕒 Thời gian kết thúc bán vé: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"⏳ Tổng thời gian bán vé: {(end_time - start_time).total_seconds():.2f} giây\n\n")
        f.write(f"🔄 Số lần quay số: {attempt}\n")
        f.write(f"🎯 Kết quả xổ số: {lottery.winning_numbers}\n\n")
        f.write(f"🎟️ Tổng vé đã bán: {lottery.tickets_sold}\n")
        f.write(f"👥 Số người mua: {lottery.total_buyers}\n")
        f.write(f"🏆 Số vé trúng thưởng: {len(winners)}\n\n")
        f.write("📊 Top 5 người mua nhiều vé nhất:\n")
        for buyer_id, ticket_count in top_buyers:
            f.write(f"- Buyer {buyer_id}: {ticket_count} vé\n")
        f.write("\n")
        f.write("🏅 Danh sách người trúng thưởng:\n")
        for buyer_id, ticket, matches in winners:
            f.write(f"- Buyer {buyer_id} - Vé {ticket} ({matches} số trùng đúng vị trí) => {PRIZE_PER_WINNER:,} VND\n")
        f.write("\n")
        f.write(f"💰 Tổng giải thưởng đã trao: {total_prize:,} VND\n")
        f.write("=== KẾT THÚC BÁO CÁO ===\n")


if __name__ == "__main__":
    main()