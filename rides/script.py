import datetime

DEBUG = True


def solve(problem):
    result = []

    rides = problem["rides"].copy()

    start = {
        "number": "start",
        "start_row": 0,
        "start_column": 0,
        "finish_row": 0,
        "finish_column": 0,
        "start_after": 0}

    for _ in range(problem["vehicles"]):
        closest_to_start = closest_connected_ride(start, rides)
        rides.remove(closest_to_start)
        result.append([closest_to_start])

    not_changed = False
    while(True):
        if not_changed:
            break
        not_changed = True

        for ride_plan in result:
            if len(rides) == 0:
                break
            [last_ride] = ride_plan[-1:]
            best_connection = closest_connected_ride(last_ride, rides)

            if valid_ride_plan(problem, ride_plan + [best_connection]):
                if DEBUG:
                    print("Valid connection, adding to ride")
                rides.remove(best_connection)
                ride_plan.append(best_connection)
                not_changed = False

    print("Missed {} rides".format(len(rides)))
    return result


def valid_ride_plan(problem, ride_plan):
    vehicle = {"row": 0, "column": 0}
    step = 0

    if DEBUG:
        print("Simulating ride_plan: {}".format(format_ride_plan(ride_plan)))
    for ride in ride_plan:

        if DEBUG:
            print("Starting ride {} at step {}".format(ride["number"], step))

        step += start_distance(ride, vehicle)
        if step < ride["start_after"]:
            step = ride["start_after"]
        step += ride_distance(ride)

        vehicle = update_vehicle(ride)

        if DEBUG:
            print("Ending ride {} at step {}".format(ride["number"], step))

        if step > ride["finish_before"]:
            if DEBUG:
                print("Failed to finish")
            return False

    return True


def update_vehicle(ride):
    return {"row": ride["finish_row"], "column": ride["finish_column"]}


def start_distance(ride, vehicle):
    return distance(vehicle["row"],
                    vehicle["column"],
                    ride["start_row"],
                    ride["start_column"])


def closest_connected_ride(ride_to_check, rides):
    r1 = ride_to_check["finish_row"]
    c1 = ride_to_check["finish_column"]

    arrival = ride_to_check["start_after"] + ride_distance(ride_to_check)
    closest_ride = {}
    minimum = -1000

    for ride in rides:
        r2 = ride["start_row"]
        c2 = ride["finish_column"]
        value = distance(r1, c1, r2, c2)

        if arrival < ride["start_after"]:
            waiting_penalty = ride["start_after"] - arrival
            value += waiting_penalty
            value -= problem["bonus"]

        if DEBUG:
            print("Found value {} for ride {}".format(value, ride["number"]))

        if minimum > value or minimum == -1000:
            minimum = value
            closest_ride = ride

    if DEBUG:
        msg = "Found that {} connects best to {}"
        print(msg.format(closest_ride["number"], ride_to_check["number"]))

    return closest_ride


def ride_distance(ride):
    return distance(ride["start_row"],
                    ride["start_column"],
                    ride["finish_row"],
                    ride["finish_column"])


def distance(start_row, start_column, finish_row, finish_column):
    return abs(start_row - finish_row) + abs(start_column - finish_column)


def load_file(filename):
    result = {}

    with open(filename) as f:
        lines = f.read().splitlines()

        [rows, columns, vehicles, rides, bonus, steps] = lines[0].split(' ')

        result["rows"] = int(rows)
        result["columns"] = int(columns)
        result["vehicles"] = int(vehicles)
        result["rides"] = int(rides)
        result["bonus"] = int(bonus)
        result["steps"] = int(steps)

        rides = []
        for ride_number, line in enumerate(lines[1:]):
            [start_row, start_column, finish_row, finish_column,
             start_after, finish_before] = line.split(' ')

            ride = {}
            ride["number"] = ride_number
            ride["start_row"] = int(start_row)
            ride["start_column"] = int(start_column)
            ride["finish_row"] = int(finish_row)
            ride["finish_column"] = int(finish_column)
            ride["start_after"] = int(start_after)
            ride["finish_before"] = int(finish_before)
            rides.append(ride)

        result["rides"] = rides

    return result


def export(name, data):
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M")
    output_dir = './output/'
    filename = timestamp + '_' + name + '.txt'

    with open(output_dir + filename, 'w') as file:
        for rides in data:
            line = "{} {}\n".format(str(len(rides)), format_ride_plan(rides))
            file.write(line)

        print('file was written in directory: ' + output_dir + filename)


def format_ride_plan(ride_plan):
    return " ".join(str(ride["number"]) for ride in ride_plan)


if __name__ == "__main__":
    if DEBUG:
        datasets = ['b_should_be_easy']
    else:
        datasets = ['a_example', 'b_should_be_easy', 'c_no_hurry',
                    'd_metropolis', 'e_high_bonus']

    for dataset in datasets:
        problem = load_file(dataset + '.in')
        solution = solve(problem)
        if DEBUG:
            print(solution)
        export(dataset, solution)
