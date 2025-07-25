import random

class SignalLogic:
    def __init__(self, detected_car_counts, total_cycle=120, min_green=20, max_green=40):
        # 입력 받은 도로 이름을 내부적으로 사용할 이름으로 변환
        self.direction_map = {
            "Road #1": "N",
            "Road #2": "E",
            "Road #3": "S",
            "Road #4": "W"
        }

        # 전달받은 딕셔너리의 키를 새로운 이름으로 변환
        mapped_car_counts = {
            self.direction_map.get(original_name, original_name): count 
            for original_name, count in detected_car_counts.items()
        }
        
        # 변환된 차량 수 데이터를 사용
        self.car_counts = mapped_car_counts
        
        # 파라미터를 설정
        self.T = total_cycle
        self.min_green = min_green
        self.max_green = max_green
        
        # 계산 결과를 저장할 변수를 설정
        self.r = 0
        self.weights = {}
        self.alloc_green = {}
        # 최종 결과를 저장할 리스트
        self.logic_results = [] 
        
        print(f"입력된 차량 수: {self.car_counts}")

    def apply_traffic_logic(self):
        num_directions = len(self.car_counts)
        if sum(self.car_counts.values()) == 0:
            for direction in self.car_counts:
                self.alloc_green[direction] = 10
        else:
            base_alloc = {
                d: (10 if self.car_counts[d] == 0 else self.min_green)
                for d in self.car_counts
            }
            total_vehicles = sum(self.car_counts.values())
            self.r = self.T - sum(base_alloc.values())
            weights = {}
            for direction, count in self.car_counts.items():
                weights[direction] = count / total_vehicles if count > 0 else 0

            first_alloc = {}
            for direction in self.car_counts:
                add_time = int(round(self.r * weights[direction]))
                proposed = base_alloc[direction] + add_time
                if proposed > self.max_green:
                    first_alloc[direction] = self.max_green
                else:
                    first_alloc[direction] = proposed

            self.alloc_green = first_alloc.copy()

            # 2차 보정: 잔여 시간 다시 분배 (max_green 제한 X, min_green은 유지)
            current_sum = sum(self.alloc_green.values())
            difference = self.T - current_sum

            if difference != 0:
                adjustable = [d for d in self.car_counts if self.car_counts[d] > 0]
                adjustable.sort(key=lambda d: weights[d], reverse=True)

                for i in range(abs(difference)):
                    target = adjustable[i % len(adjustable)]
                    if difference > 0:
                        self.alloc_green[target] += 1
                    else:
                        if self.alloc_green[target] > self.min_green:
                            self.alloc_green[target] -= 1

        print(f"보정 후 최종 할당 녹색 시간: {self.alloc_green}")
        print(f"보정 후 총합: {sum(self.alloc_green.values())}초")

        grouped_by_time = {}
        for direction, time in self.alloc_green.items():
            grouped_by_time.setdefault(time, []).append(direction)

        sorted_times = sorted(grouped_by_time.keys(), reverse=True)
        final_sorted_directions = []
        for time in sorted_times:
            directions = grouped_by_time[time]
            random.shuffle(directions)
            final_sorted_directions.extend(directions)

        self.logic_results = []
        for i, direction in enumerate(final_sorted_directions):
            self.logic_results.append([
                direction,
                self.alloc_green[direction],
                i + 1
            ])

        print(f"할당된 녹색 시간 및 순서: {self.logic_results}\n\n")
        return self.logic_results