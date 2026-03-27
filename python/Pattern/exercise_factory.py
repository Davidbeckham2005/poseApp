from services.pushup_service import pushupService
from services.plank_service import plankService
from services.lungue_service import lungService
from services.bicep_service import bicep_service
from services.shoulder_press_service import ShoulderPressServices
from services.squat_services import squatService
from schemas.video_schemas import Webcam_Schemas
class ExerciseFactory:
    @staticmethod
    def get_service(exercise_type):
        services = {
            'squat' : squatService,
            'pushup' : pushupService,
            'lungue': lungService,
            'bicep_curls': bicep_service,
            'shoulder_press': ShoulderPressServices
        }
        data = Webcam_Schemas(Analyst_FPS=False,type=exercise_type)
        service_class = services.get(exercise_type)
        if service_class:
            return service_class(None,None,None,data)
        return None