import multiprocessing
from .dummy_main import start as start_exercise_function
import os
import requests
import json

def machine_available():
    FILENAME = os.path.dirname(__file__) + '\\status.txt'
    with open(FILENAME, 'r') as f:
        return f.readline() == '1'

def start_exercise(context):
    if not machine_available():
        return False
    print(f"Starting the exercise {context.get('exercise').get('name')}")
    process = multiprocessing.Process(target=start_exercise_function, args=[context])
    process.start()

    return True


class MachineManager:
    '''
    Manager for manage the exercise machines
    '''
    FILENAME = os.path.join(os.path.dirname(__file__), "status.txt")
    STATUS = 1

    def __init__(self):
        MachineManager.STATUS = self._get_machine_status()

    def isready(self):
        return MachineManager.STATUS == 1

    def start_exercise(self, context):
        """
        Start the exercise on seperate thread.
        """
        if not self.isready():
            return False    
        self._set_machine_status(0)
        # Create and start exercise process
        exercise = multiprocessing.Process(target=start_exercise_function, args=[context, self.end_exercise])
        exercise.start()

        return True


    def end_exercise(self, success=False, data=None):
        """ End exercuse and save data in database on seccess. """
        self._set_machine_status(1)
        
        if success:
            self._save_workout_in_database(data)        

    def _get_machine_status(self):
        """
        Returns the status the exercise machine
        """
        with open(MachineManager.FILENAME, 'r') as f:
            status_binary = f.readline()

        return True if status_binary == '1' else False 


    def _set_machine_status(self, status):
        """
        Change machine status
        """
        VALID_STATUS_CODES = ['0', '1']
        status = str(status)
        if status not in VALID_STATUS_CODES:
            return False

        with open(MachineManager.FILENAME, 'w') as f:
            f.write(status)

        MachineManager.STATUS = status

        return True

    def _save_workout_in_database(self, data):
        server_url = 'http://localhost:8000/add_workout/'
        if data:
            data['auth_token'] = os.environ.get('AUTH_TOKEN')
            request = requests.post(server_url, data=data)
            if request.status_code == 201:
                print("Workout added successfully")
            else:
                print(f"Error adding workout : {request.status_code}")