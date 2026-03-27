from time import sleep

from Pattern.exercise_factory import ExerciseFactory
import asyncio

# plan dạng: [{"type": "pushup", "target": 10}, {"type": "squat", "target": 10}]
class WorkoutController:
    def __init__(self,plan):
        self.plan = plan
        self.current_index = 0
        self.is_finish = False
        self.current_service = self.load_service()
    
    def load_service(self):
        if self.current_index < len(self.plan):
            current_plan = self.plan[self.current_index]
            return ExerciseFactory.get_service(current_plan['type'])
        return None


    async def update(self,landmarks,websocket):
        if self.is_finish:
            return "workout Complete!"
        if not self.current_service:
            return "not have service"

        self.current_service.run_estimate(landmarks,None)
        result = self.current_service.get_data_live()
        target = self.plan[self.current_index]["target"]
        # Thêm thông tin về tiến độ tổng thể
        result["workout_progress"] = f"{self.current_index + 1}/{len(self.plan)}"
        result["target_of_current"] = target
        result["exercise_type"] = self.plan[self.current_index]["type"],
        # type, target_rep = self.excercises[self.current_index]
        # success = current_service.run_estimate(landmarks,None)
        print(result)
        await websocket.send_json(result)
        if self.current_service.count_total >=target:
            await self.switch_to_next_exercise(websocket)
       
        
    async def switch_to_next_exercise(self,websocket):
        self.current_index +=1
        if self.current_index < len(self.plan):
            await websocket.send_json({
                "event" : "rest_start",
                "seconds": 10,
                "next_exercise": self.plan[self.current_index]["type"],
                "message": ""})
            await asyncio.sleep(10)
            await websocket.send_json({
                "event": "rest_end"
            })
            self.current_service = self.load_service()
        else:
            self.is_finish = True
            await websocket.send_json({
                "event" : "workout_complete"
            })
  