import time


class SummaryService:

    def generate(self, sleep_hours: float, steps: int) -> dict:
        time.sleep(2)
        score = sleep_hours * 10 + steps * 0.01
        return {
            "score": round(score, 2),
            "message": "Fake health report"
        }