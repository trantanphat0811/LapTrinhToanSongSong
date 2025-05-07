import multiprocessing
import random
import time

def visualize_hotel(hotel_display_data, current_time, roof_patient_count, total_nurses):
    print(f"Time: {current_time}")
    print(f"Saved Patients: {roof_patient_count.value}")
    print(f"Remaining Nurses: {total_nurses}")
    print("=" * 50)
    for floor_id in range(len(hotel_display_data)):
        print(" | ".join(hotel_display_data[floor_id]))
    print("=" * 50)

def flood_controller(N, M, X, flood_queue, flood_status, room_flood_status, hotel_display_data):
    pass

def floor_process(floor, M, X, flood_queue, patient_queues, hotel, nurses, room_flood_status, flood_status, roof_patient_count, hotel_display_data):
    pass

if __name__ == "__main__":
    N = 6  
    M = 12  
    X = 0.05  

    flood_queue = multiprocessing.Queue()
    patient_queues = [multiprocessing.Queue() for _ in range(N - 1)]  
    
    hotel = [[random.randint(5, 15) for _ in range(M)] for _ in range(N - 1)]
    nurses = [M // 3 for _ in range(N - 1)] + [0]  
    
    room_flood_status = [[False for _ in range(M)] for _ in range(N - 1)]
    flood_status = [False for _ in range(N)]
    flood_status[0] = True  
    
    roof_patient_count = multiprocessing.Value('i', 0)
    manager = multiprocessing.Manager()
    hotel_display_data = manager.list(
        [[f"T{floor+1} P{room+1}: {hotel[floor][room]}P : {nurses[floor]}N" for room in range(M)] for floor in range(N - 1)] + [[]]
    )  

    flood_process = multiprocessing.Process(target=flood_controller,
                                            args=(N, M, X, flood_queue, flood_status, room_flood_status,
                                                  hotel_display_data))
    floor_processes = [multiprocessing.Process(target=floor_process,
                                               args=(i, M, X, flood_queue, patient_queues, hotel, nurses,
                                                     room_flood_status, flood_status, roof_patient_count,
                                                     hotel_display_data)) for i in range(N - 1)]
    
    flood_process.start()
    for p in floor_processes:
        p.start()
    
    current_time = 0
    while not flood_status[N - 2]:  
        visualize_hotel(hotel_display_data, current_time, roof_patient_count, sum(nurses[:-1]))
        time.sleep(X)
        current_time += 1
    
    flood_process.join()
    for p in floor_processes:
        p.join()
    
    print(f"Final Saved Patients: {roof_patient_count.value}")
    print(f"Final Remaining Nurses: {sum(nurses[:-1])}")