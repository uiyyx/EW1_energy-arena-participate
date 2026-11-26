import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
import subprocess
import sys

def main(): # find first possible target, initiate clock, check for outstanding submissions
    print("### START of SCRIPT ###")

    # choose path for saving the payloads
    payloads_path = Path(__file__).parent / "payloads"
    payloads_path.mkdir(parents=True, exist_ok=True)
    print(f"Payloads will be saved in: {payloads_path.resolve()}")

    # choose challenge
    challenge = 2
    print(f"Challenge {challenge} selected.")

    # find first possible target
    first_possible_target = find_first_possible_target()

    # derive the times at which it is time to compute the next payload
    upcoming_targets_and_times_for_payload_computation = derive_upcoming_targets_and_times_for_payload_computation(first_possible_target)
    
    print("### upcoming_targets_and_times_for_payload_computation ###")
    for name, daten in upcoming_targets_and_times_for_payload_computation.items():
        print(f"=== {name} ===")
        for schluessel, wert in daten.items():
            print(f"  {schluessel}: {wert}")
    x=1

    # initiate clock
    print("### START of CLOCK ###")
    while True:
        now = datetime.now(timezone(timedelta(hours=1)))
        print(f"Script is running. Current UTC time: {now.isoformat()}")
        time.sleep(1)  # sleep for 1 seconds before printing the time again

        # check if it is time_to_compute_the_next_payload
        if now.second % 5 == 0: #TODO change later to 30mins or whatever is appropriate
            payloads_to_compute = is_it_time_to_compute_the_next_payload(now, upcoming_targets_and_times_for_payload_computation)

            # initiate payload computation if there are payloads that must be submitted soon
            if payloads_to_compute != {}:
                print("### START of PAYLOAD COMPUTATION ###")
                for target, payload_related_data in payloads_to_compute.items():
                    #subprocess_1 = compute_payload_for_target(payloads_path,challenge, now, target, payload_related_data)

                    #submit the payload to the Energy Arena
                    identifyer_payload = payloads_path / f"payload_{target.replace(':', '-').replace(' ', '_')}.json"
                    subprocess_2= submit_payload_to_energy_arena(identifyer_payload)

                    # update the submitted status for the computed payload
                    identifyer_target = target.split(" ")[0]
                    identifyer_Submission = target.split(" ")[1]
                    upcoming_targets_and_times_for_payload_computation[identifyer_target][f"submitted_{identifyer_Submission}"] = True
                    print("Submit status updated")

def derive_upcoming_targets_and_times_for_payload_computation(first_possible_target):
    upcoming_targets_and_times_for_payload_computation = {}
    x=1

    # define arbitrary last target
    runtime = 60 # days
    last_target = first_possible_target + timedelta(days=runtime)
    
    # confirm last target
    confirmation = input(f"Choose last target {last_target} with enter: ")
    if confirmation == "":
        print("Confirmed")
    else:
        print("Not confirmed, exiting")
        exit()

    # derive upcoming targets
    for i in range(0, runtime):
        #target_name = f"target_{i}"
        target = first_possible_target + timedelta(days=i)

        # derive the the times at which it is time to compute the next payload for this target
        compute_S1_at = target - timedelta(days=3) + timedelta(hours=11, minutes=30)
        submitted_S1 = False

        compute_S2_at = target - timedelta(days=2) + timedelta(hours=11, minutes=30)
        submitted_S2 = False

        compute_S3_at = target - timedelta(days=1) + timedelta(hours=6, minutes=30)
        submitted_S3 = False

        compute_S4_at = target - timedelta(days=1) + timedelta(hours=7, minutes=30)
        submitted_S4 = False

        compute_S5_at = target - timedelta(days=1) + timedelta(hours=8, minutes=30)
        submitted_S5 = False

        compute_S6_at = target - timedelta(days=1) + timedelta(hours=9, minutes=30)
        submitted_S6 = False

        compute_S7_at = target - timedelta(days=1) + timedelta(hours=10, minutes=30)
        submitted_S7 = False

        compute_S8_at = target - timedelta(days=1) + timedelta(hours=11, minutes=30)
        submitted_S8 = False

        # put all into dictionary
        name_target = f"Target_{i+1}__{target.date()}"

        upcoming_targets_and_times_for_payload_computation[name_target] = {
            name_target: target,
            "compute_S1_at": compute_S1_at,
            "submitted_S1": submitted_S1,
            
            "compute_S2_at": compute_S2_at,
            "submitted_S2": submitted_S2,
            
            "compute_S3_at": compute_S3_at,
            "submitted_S3": submitted_S3,

            "compute_S4_at": compute_S4_at,
            "submitted_S4": submitted_S4,
            
            "compute_S5_at": compute_S5_at,
            "submitted_S5": submitted_S5,
            
            "compute_S6_at": compute_S6_at,
            "submitted_S6": submitted_S6,
            
            "compute_S7_at": compute_S7_at,
            "submitted_S7": submitted_S7,
            
            "compute_S8_at": compute_S8_at,
            "submitted_S8": submitted_S8
        }
    
    return upcoming_targets_and_times_for_payload_computation
        
def find_first_possible_target():
    now = datetime.now(timezone(timedelta(hours=1)))
    if now.hour < 12:
        first_possible_target_day_in_x_days = 3
    elif now.hour >= 12:
        first_possible_target_day_in_x_days = 4
    else: 
        print("ERROR: Could not determine first possible target. Script stopped.")
        exit()

    first_possible_target = now
    first_possible_target = first_possible_target.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=first_possible_target_day_in_x_days)

    # confirm first target
    confirmation = input(f"Choose first possible target {first_possible_target} with enter: ")
    if confirmation == "":
        print("Confirmed")
    else:
        print("Not confirmed, exiting")
        exit()

    return first_possible_target

def is_it_time_to_compute_the_next_payload(now, upcoming_targets_and_times_for_payload_computation):
    print(f"is_it_time_to_compute_the_next_payload now at: {now.isoformat()} ?")

    # initiate local variables
    decision = False # might be updated to True

    ## data manipiulation TODO delete later
    #upcoming_targets_and_times_for_payload_computation["Target_2__2026-11-30"]["submitted_S2"] = True
    #upcoming_targets_and_times_for_payload_computation["Target_2__2026-11-30"]["compute_S1_at"] = now - timedelta(minutes=30)

    upcoming_targets_and_times_for_payload_computation["Target_2__2026-11-30"]["compute_S2_at"] = now - timedelta(minutes=30)
    ## TODO delete later

    # check if it is time to compute payloads
    payloads_to_compute = {}
    for target, target_related_submission_deadlines in upcoming_targets_and_times_for_payload_computation.items():
        for S in range(1, 9):
            compute_at = target_related_submission_deadlines[f"compute_S{S}_at"]
            submitted = target_related_submission_deadlines[f"submitted_S{S}"]

            if now >= compute_at and not submitted:
                payloads_to_compute[f"{target} S{S}"] = {
                    "compute_at": compute_at,
                    "submitted": submitted
                }
    x=1

    # print decision
    if payloads_to_compute != {}:
        decision = True
        print(decision)

        # print payloads_to_compute
        print("### payloads_to_compute ###")
        for payload, payload_related_data in payloads_to_compute.items():
            print(f" - {payload}: {payload_related_data['compute_at']}")
    else:
        print(decision)

    return payloads_to_compute

def compute_payload_for_target(payloads_path, challenge, now, target, payload_related_data):
    print(f"# Computing payload for {target} at {now.isoformat()} (scheduled at {payload_related_data['compute_at']})")

    iso_target = datetime(2026, 11, 29, 0, 0, tzinfo=timezone(timedelta(hours=1)))
    iso_target = iso_target.isoformat(timespec='seconds')
    
    # iso time of the target for which the payload is computed
    iso_target = (payload_related_data['compute_at'] + timedelta(minutes=30)).isoformat(timespec='seconds')

    
    # path to save the payload
    payloads_path = Path(payloads_path) / f"payload_{target.replace(':', '-').replace(' ', '_')}.json"
    payloads_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [sys.executable, "run_forecast_model.py",
            "--target_start", iso_target,
            "--challenge_id", str(challenge),
            "--save_payload", str(payloads_path)]

    # TODO  CONTINUE HEEEEERRRREEEE   
    # 1.implement payload computation trigger/logic here

    x = subprocess.run(cmd, check=True, text=True, capture_output=True) # test computation via the base model of the forked repository
    print(f"Payload for {target} computed and saved successfully.")
    return x #test computation via the base model of the forked repository

def submit_payload_to_energy_arena(payload):
    print("\n### Payload Submission ###")
    print(f"payload to be submitted: {payload.name}")

    payload_path = Path(str(payload))
    payload_path = Path(*payload_path.parts[payload_path.parts.index("payloads"):])
    str_payload_path = str(payload_path)

    cmd = [sys.executable, "submit_forecast_to_energy_arena.py",
           "--payload_path", str_payload_path]

    x = subprocess.run(cmd, check=True, text=True, capture_output=True)
    print(f"Payload for {payload.name} submitted successfully")
    return x

if __name__ == "__main__":
    main()
