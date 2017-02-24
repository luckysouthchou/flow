import numpy as np
import random
import traci

def never_change_lanes_controller():

    def controller(carID, env):
        return env.vehicles[carID]["lane"]

    return controller


def stochastic_lane_changer(speedThreshold = 5, prob = 0.5,
                            dxBack = 0, dxForward = 60,
                            gapBack = 10, gapForward = 5):
    """
    Intelligent lane changer
    :param speedThreshold: minimum speed increase required
    :param prob: probability change will be requested if warranted = this * speedFactor
    :param dxBack: Farthest distance back car can see
    :param dxForward: Farthest distance forward car can see
    :param gapBack: Minimum required clearance behind car
    :param gapForward: Minimum required clearance in front car
    :return: carFn to input to a carParams
    """
    def controller(carID, env):
        num_lanes = env.scenario.lanes
        v = [0] * env.scenario.lanes
        for lane in range(num_lanes):
            # count the cars in this lane?
            leadID = env.get_leading_car(carID, lane)
            trailID = env.get_trailing_car(carID, lane)

            if not leadID or not trailID:
                # empty lane
                v[lane] = env.vehicles[carID]['max_speed']
                continue

            leadPos = env.get_x_by_id(leadID)
            trailPos = env.get_x_by_id(trailID)

            thisPos = env.get_x_by_id(carID)

            headway = (leadPos - thisPos) % env.scenario.length # d_l
            footway = (thisPos - trailPos) % env.scenario.length # d_f

            if headway < gapForward or footway < gapBack:
                # if cars are too close together??
                v[lane] = 0
                continue

            # otherwise set v[lane] to the mean velocity of all cars in the region?
            # and if there are zero cars then it's the max speed?
            # but then why is there setting v[lane] to 0? too packed to merge

            other_car_ids = env.get_cars(carID, dxBack = dxBack, dxForward = dxForward, lane = lane)

            if len(other_car_ids) > 0:
                v[lane] = np.mean([env.vehicles[other_id]["speed"] for other_id in other_car_ids])
            else: # no cars in lane
                v[lane] = env.vehicles[carID]['max_speed']
        maxv = max(v)
        maxl = v.index(maxv)
        myv = v[env.vehicles[carID]['lane']]

        if maxl != env.vehicles[carID]['lane'] and \
           (maxv - myv) > speedThreshold and \
           random.random() < prob:
           return maxl
        return env.vehicles[carID]['lane']

    return controller