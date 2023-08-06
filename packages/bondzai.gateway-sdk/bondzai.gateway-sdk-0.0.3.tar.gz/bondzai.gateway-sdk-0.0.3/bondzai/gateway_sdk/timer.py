import time


TIME_MULT = 1


class Timer():
    time_started: int = 0

    @classmethod
    def init(cls) -> None:
        cls.time_started = int(time.time() * TIME_MULT)
    
    @classmethod
    def get_elapsed_time(cls) -> int:
        now_time = int(time.time() * TIME_MULT)
        return now_time - cls.time_started

    @classmethod
    def get_timestamp(cls) -> int:
        return cls.get_elapsed_time()
    
    @classmethod
    def wait(cls, sec_to_wait: float) -> None:
        if sec_to_wait < 0:
            return
        time.sleep(sec_to_wait)
        