import multiprocessing
import random
import time

def visualize_hotel(hotel, nurses, current_time, roof_patient_count, dead_patient_count, total_nurses, total_patients, saved_log, dead_log):
    saved_percentage = (roof_patient_count.value / total_patients) * 100 if total_patients > 0 else 0
    print(f"\n===== Time: {current_time} =====")
    print(f"Saved Patients: {roof_patient_count.value} ({saved_percentage:.2f}%)")
    print(f"Dead Patients: {dead_patient_count.value}")
    print(f"Remaining Nurses: {total_nurses}")
    print("=" * 50)
    for floor_id, floor in enumerate(hotel):
        print(f"Floor {floor_id + 1}: " + " | ".join(f"{p}P, {nurses[floor_id]}N" for p in floor))
    print("=" * 50)
    saved_log.append(roof_patient_count.value)
    dead_log.append(dead_patient_count.value)

def flood_controller(N, M, X, flood_status, dead_patient_count, hotel):
    for floor in range(N - 1):
        time.sleep(random.uniform(0.5, 1.5) * X)
        flood_status[floor] = True
        with dead_patient_count.get_lock():
            dead_patient_count.value += sum(hotel[floor])
        hotel[floor] = [0] * M
        print(f" Floor {floor + 1} is flooding! ")

def patient_movement(N, M, hotel, flood_status):
    for floor in range(N - 2, -1, -1):
        if not flood_status[floor]:
            for room in range(M):
                if hotel[floor][room] > 0 and random.random() < 0.1:
                    new_room = min(M - 1, max(0, room + random.choice([-1, 1])))
                    hotel[floor][new_room] += 1
                    hotel[floor][room] -= 1

def floor_process(floor, M, X, hotel, nurses, flood_status, roof_patient_count):
    while not flood_status[floor]:
        time.sleep(X)
        for room in range(M):
            if hotel[floor][room] > 0 and nurses[floor] > 0:
                patients_to_save = min(hotel[floor][room], nurses[floor])
                hotel[floor][room] -= patients_to_save
                nurses[floor] -= patients_to_save
                with roof_patient_count.get_lock():
                    roof_patient_count.value += patients_to_save

def run_simulation(N, M, X, initial_nurses, min_patients, max_patients):
    hotel = [[random.randint(min_patients, max_patients) for _ in range(M)] for _ in range(N - 1)]
    nurses = [initial_nurses for _ in range(N - 1)] + [0]
    flood_status = [False for _ in range(N)]
    flood_status[0] = True
    
    roof_patient_count = multiprocessing.Value('i', 0)
    dead_patient_count = multiprocessing.Value('i', 0)
    total_patients = sum(sum(floor) for floor in hotel)
    
    saved_log = []
    dead_log = []
    
    flood_process = multiprocessing.Process(target=flood_controller, args=(N, M, X, flood_status, dead_patient_count, hotel))
    floor_processes = [multiprocessing.Process(target=floor_process, args=(i, M, X, hotel, nurses, flood_status, roof_patient_count)) for i in range(N - 1)]
    
    flood_process.start()
    for p in floor_processes:
        p.start()
    
    current_time = 0
    while not flood_status[N - 2]:  
        patient_movement(N, M, hotel, flood_status)
        visualize_hotel(hotel, nurses, current_time, roof_patient_count, dead_patient_count, sum(nurses[:-1]), total_patients, saved_log, dead_log)
        time.sleep(X)
        current_time += 1
    
    flood_process.join()
    for p in floor_processes:
        p.join()
    
    saved_percentage = (roof_patient_count.value / total_patients) * 100 if total_patients > 0 else 0
    print(f"\n===== Final Results =====")
    print(f"Final Saved Patients: {roof_patient_count.value} ({saved_percentage:.2f}%)")
    print(f"Final Dead Patients: {dead_patient_count.value}")
    print(f"Final Remaining Nurses: {sum(nurses[:-1])}")
    
    print("\n===== Patient Status Over Time =====")
    for i, (s, d) in enumerate(zip(saved_log, dead_log)):
        print(f"Time {i}: Saved {s}, Dead {d}")

def main():
    num_simulations = int(input("Nhập số lần mô phỏng: "))
    N = int(input("Nhập số tầng của khách sạn (bao gồm mái): "))
    M = int(input("Nhập số phòng trên mỗi tầng: "))
    initial_nurses = int(input("Nhập số y tá ban đầu trên mỗi tầng: "))
    min_patients = int(input("Nhập số bệnh nhân tối thiểu trong mỗi phòng: "))
    max_patients = int(input("Nhập số bệnh nhân tối đa trong mỗi phòng: "))
    X = float(input("Nhập hệ số tốc độ mô phỏng: "))
    
    for i in range(num_simulations):
        print(f"\n===== Running Simulation {i + 1} =====\n")
        run_simulation(N, M, X, initial_nurses, min_patients, max_patients)

if __name__ == "__main__":
    main()