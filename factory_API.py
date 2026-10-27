from fastapi import FastAPI
import random
from datetime import datetime

app = FastAPI()


@app.get("/factory")
def get_factory_data():

    robots = []

    for number in range(1, 9):

        machine_id = f"R-3{number:02d}"

        temperature = round(random.uniform(55, 95), 1)

        power_consumption = round(random.uniform(10,50),1)

        produced_parts = random.randint(600, 1200)

        defective_parts = random.randint(0,40)

        
        robot = {
            "ID": machine_id,
            "Temperature": temperature,
            "Parts": produced_parts,
            "Defects": defective_parts,
            "Power": power_consumption,
        }

        robots.append(robot)

    return {
        "timestamp": datetime.now().isoformat(),
        "robots": robots
    }
