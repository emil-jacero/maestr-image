# image_controller.py

from app import api
from app.services import Image, Images, TargetImage, TargetImages, Schedule, Schedules, RunManually

## Services
api_v1 = '/api/v1'
api.add_resource(Image, f'{api_v1}/image/')
api.add_resource(Images, f'{api_v1}/images/')
api.add_resource(TargetImage, f'{api_v1}/target_image/')
api.add_resource(TargetImages, f'{api_v1}/target_images/')
api.add_resource(Schedule, f'{api_v1}/scheduler/')
api.add_resource(Schedules, f'{api_v1}/schedulers/')
api.add_resource(RunManually, f'{api_v1}/run_manually/<string:uuid>/')
