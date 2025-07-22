import random

class SignalLogic:
    def __init__(self, detected_car_counts, total_cycle=120, min_green=20, max_green=40):
        # 입력 받은 도로 이름을 내부적으로 사용할 이름으로 변환
        self.direction_map = {
            "Road #1": "N",
            "Road #2": "W",
            "Road #3": "S",
            "Road #4": "E"
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
        
        print(f"파라미터 설정 완료: T={self.T}초, 최소 녹색={self.min_green}초, 최대 녹색={self.max_green}초")
        print(f"입력된 차량 수: {self.car_counts}")

    def apply_traffic_logic(self):
        # 잉여 시간 계산
        num_directions = len(self.car_counts)
        self.r = self.T - (num_directions * self.min_green)
        if self.r < 0:
            print("오류: 최소 녹색 시간의 합이 전체 사이클보다 큽니다.")
            return None
        print(f"계산된 잉여 시간(r): {self.r}초")

        # 차량 비율 및 가중치 계산
        total_vehicles = sum(self.car_counts.values())
        if total_vehicles == 0:
            weight_val = 1 / num_directions
            for direction in self.car_counts:
                self.weights[direction] = weight_val
        else:
            for direction, count in self.car_counts.items():
                self.weights[direction] = count / total_vehicles
        print(f"계산된 방향별 가중치: {self.weights}")

        # 1차 녹색 할당 시간 계산
        for direction in self.weights:
            calculated_time = self.min_green + (self.r * self.weights[direction])
            adjusted_time = int(round(calculated_time))

            if adjusted_time > self.max_green:
                self.alloc_green[direction] = self.max_green
            else:
                self.alloc_green[direction] = adjusted_time
        
        print(f"1차 할당된 녹색 시간: {self.alloc_green}")

        # 총합 120초를 맞추기 위한 보정 로직
        current_sum = sum(self.alloc_green.values())
        difference = self.T - current_sum
        
        print(f"1차 할당 후 총합: {current_sum}초, 보정 필요량: {difference}초")

        if difference != 0:
            if difference > 0:
                filter_func = lambda d: self.alloc_green[d] < self.max_green
            else:
                filter_func = lambda d: self.alloc_green[d] > self.min_green
            
            eligible_directions = list(filter(filter_func, self.alloc_green.keys()))
            eligible_directions.sort(key=lambda d: self.weights[d], reverse=True)

            if not eligible_directions:
                print("경고: 모든 방향이 최대/최소 녹색 시간에 도달하여 보정이 불가능합니다.")
            else:
                for i in range(abs(difference)):
                    direction_to_adjust = eligible_directions[i % len(eligible_directions)]
                    if difference > 0:
                        self.alloc_green[direction_to_adjust] += 1
                    else:
                        self.alloc_green[direction_to_adjust] -= 1

        print(f"보정 후 최종 할당 녹색 시간: {self.alloc_green}")
        print(f"보정 후 총합: {sum(self.alloc_green.values())}초")
        
        # 우선순위 부여를 위한 정렬
        # alloc_green을 기준으로 그룹화
        grouped_by_time = {}
        for direction, time in self.alloc_green.items():
            if time not in grouped_by_time:
                grouped_by_time[time] = []
            grouped_by_time[time].append(direction)

        # 내림차순으로 정렬
        sorted_times = sorted(grouped_by_time.keys(), reverse=True)

        # 정렬된 리스트 생성 (동일 시간 그룹은 무작위)
        final_sorted_directions = []
        for time in sorted_times:
            directions = grouped_by_time[time]
            random.shuffle(directions)
            final_sorted_directions.extend(directions)

        # 우선순위를 리스트 형식으로 부여
        for i, direction in enumerate(final_sorted_directions):
            self.logic_results.append([
                direction,
                self.alloc_green[direction],
                i + 1
            ])

        print(f"할당된 녹색 시간 및 순서: {self.logic_results}")

        return {
            "return_value": self.logic_results
        }