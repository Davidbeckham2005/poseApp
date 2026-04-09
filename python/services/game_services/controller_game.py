from time import sleep
import time
from Pattern.exercise_factory import ExerciseFactory
import asyncio
from utils.calc import format_time, calculating_caloris
# plan dạng: [{"type": "pushup", "target": 10}, {"type": "squat", "target": 10}]
class WorkoutController:
    def __init__(self,plan):
        self.rest_time = 10
        self.plan = plan
        self.current_index = 0
        self.is_finish = False
        self.current_service = self.load_service()
    # lưu thông tin thời gian
        self.start_workout_time = time.time()
        self.current_exercise_duration = 0.0
        self.last_frame_time = None
        self.total_duration = 0
    # lưu thông tin cho cả quá trình tập luyện, bao gồm cả bài tập hiện tại, số rep đã hoàn thành, thời gian nghỉ giữa các bài tập, v.v.
        self.total_caloris = 0.0
        self.total_reps = 0
        self.total_reps_good = 0
        self.workout_history = []
    def load_service(self):
        if self.current_index < len(self.plan):
            self.current_exercise_duration = 0.0  # reset thời gian tập luyện cho bài tập mới
            self.last_frame_time = None  # reset thời gian của frame cuối cùng
            current_plan = self.plan[self.current_index]
            return ExerciseFactory.get_service(current_plan['type'])
        return None


    async def update(self,landmarks,websocket):
        if self.is_finish:
            return "workout Complete!"
        if not self.current_service:
            return "not have service"
        if self.last_frame_time is not None:
            delta_time = time.time() - self.last_frame_time
            if delta_time < 0.5:
                self.current_exercise_duration += delta_time
        self.last_frame_time = time.time()
        self.current_service.run_estimate(landmarks,None)
        result = self.current_service.get_data_live()
        target = self.plan[self.current_index]["target"]
        # Thêm thông tin về tiến độ tổng thể
        result["current_duration"] = format_time(self.current_exercise_duration)
        result["workout_progress"] = f"{self.current_index + 1}/{len(self.plan)}"
        result["target_of_current"] = target
        result["exercise_type"] = self.plan[self.current_index]["type"]
        print(result)
        await websocket.send_json(result)
        if self.current_service.count_total >=target:
            exercise_log = self.current_service.get_data_game(self.current_exercise_duration)
            self.total_caloris += exercise_log["calory"]
            self.total_reps += exercise_log["total"]
            self.total_reps_good += exercise_log["good"]
            self.workout_history.append({
                "exercise": self.plan[self.current_index]["type"],
                "actual_reps": exercise_log["total"],
                "good_reps": exercise_log["good"],
                "accuracy": exercise_log["accuracy"],
                "duration": format_time(self.current_exercise_duration),
                "calories": exercise_log["calory"]
            })
            await self.switch_to_next_exercise(websocket)
       
        
    async def switch_to_next_exercise(self,websocket):
        self.current_index +=1
        if self.current_index < len(self.plan):
            await websocket.send_json({
                "data" : self.current_service.get_data_game(self.current_exercise_duration),
                "event" : "rest_start",
                "seconds": self.rest_time,
                "next_exercise": self.plan[self.current_index]["type"],
                "message": ""})
            await asyncio.sleep(10)
            await websocket.send_json({
                "event": "rest_end",
                
            })
            self.current_service = self.load_service()
        else:
            self.is_finish = True
            print("Workout complete!",self.workout_history)
            await websocket.send_json({
                "event" : "workout_complete",
                "history": self.workout_history,
                "total_calories": round(self.total_caloris, 2),
                "total_reps": self.total_reps,
                "total_good_reps": self.total_reps_good,
            })
