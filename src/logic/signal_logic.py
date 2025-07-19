from enum import Enum, auto
from dataclasses import dataclass
from typing import Dict, List

class Direction(Enum):
    EAST  = auto()
    WEST  = auto()
    SOUTH = auto()
    NORTH = auto()

@dataclass(frozen=True)
class TrafficCounts:
    east: int
    west: int
    south: int
    north: int

@dataclass(frozen=True)
class GreenTimes:
    east: int
    west: int
    south: int
    north: int

# 임의의 데이터 수집 함수
def fetch_dummy_counts() -> TrafficCounts:
    # 지금은 실제 데이터를 받아올 수 없기 때문에 일단 하드코딩함 --25.07.19
    return TrafficCounts(east=15, west=12, south=5, north=17)

def compute_green_times(
    counts: TrafficCounts,
    cycle: int = 120,
    base_min: int = 10,
    alpha: float = 0.5
) -> GreenTimes:
    """
    1) 모든 방향에 base_min 확보
    2) 남은 시간 = cycle - base_min*4
    3) 남은 시간을 차량 수 비례로 분배
    4) 반올림 및 보정: 총 합이 cycle이 안 나올 수 있기 때문에 보정 코드를 추가함
    5) base_min + extra → 최종 GreenTimes
    """
    num_dirs = len(Direction)
    if cycle < base_min * num_dirs:
        raise ValueError("전체 신호 주기가 각 방향에 할당된 최소 시간보다 작습니다.")

    min_times = {d: base_min for d in Direction}

    remaining = cycle - base_min * num_dirs

    raw_counts = {d: getattr(counts, d.name.lower()) for d in Direction}
    total_vehicles = sum(raw_counts.values())
    
    if total_vehicles == 0:
        extras = {d: remaining // num_dirs for d in Direction}
    else:
        raw_extra = {d: raw_counts[d] / total_vehicles * remaining for d in Direction}
        extras = {d: int(round(raw_extra[d])) for d in Direction}
        # 총 합이 cycle과 일치할 수 있도록 보정
        diff = remaining - sum(extras.values())
        dirs: List[Direction] = list(Direction)
        idx = 0
        while diff:
            d = dirs[idx % num_dirs]
            step = 1 if diff > 0 else -1
            extras[d] = max(0, extras[d] + step)
            diff -= step
            idx += 1

    finals = {d: min_times[d] + extras[d] for d in Direction}

    return GreenTimes(
        east  = finals[Direction.EAST],
        west  = finals[Direction.WEST],
        south = finals[Direction.SOUTH],
        north = finals[Direction.NORTH],
    )

if __name__ == '__main__':
    CYCLE_TIME = 120
    BASE_MIN = 10

    # 차량 수 수집
    counts = fetch_dummy_counts()
    print("Collected vehicle counts:")
    print(f"  East : {counts.east}")
    print(f"  West : {counts.west}")
    print(f"  South: {counts.south}")
    print(f"  North: {counts.north}\n")

    # 최종 녹색시간 계산
    greens = compute_green_times(counts, cycle=CYCLE_TIME, base_min=BASE_MIN)
    print("Minimum green times:")
    for d in Direction:
        print(f"  {d.name.title():5s}: {BASE_MIN}s")
    print()

    print("=== Final Green Times ===")
    for d in Direction:
        sec = getattr(greens, d.name.lower())
        print(f"{d.name.title():5s}: {sec}s")
    total = sum(getattr(greens, d.name.lower()) for d in Direction)
    print(f"총합  : {total} (cycle={CYCLE_TIME})")