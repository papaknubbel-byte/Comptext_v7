import cProfile
import pstats
from src.core.kvtc import IndustrialKVTCStrategy

def profile_kvtc():
    strategy = IndustrialKVTCStrategy()
    large_text = "--- SOURCE: MO360 ---\nLINE_A: HEARTBEAT OK | UPTIME 98.2% | ROBOT_A1: NOMINAL\n" * 1000 + "VIN: WDB906232N3123456 | DTC: P0300"
    
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Run compress multiple times to gather good stats
    for _ in range(100):
        strategy.compress(large_text)
        
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats(20)

if __name__ == "__main__":
    profile_kvtc()
