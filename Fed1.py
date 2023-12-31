import numpy as np
import helics as h
import logging
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math


# Good practice to set up logging so we know what is going on.
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(
    logging.DEBUG
)  # Set this to INFO if you want less log messages (We can get a huge amount of messages if we set this to DEBUG)

# Function to destroy this federate once we've finished the co-simulation.
def destroy_federate(fed):
    h.helicsFederateDestroy(fed)
    logger.info("Federate finalized")


if __name__ == "__main__":

    ##############  Creating Federate and Pub/Sub messaging  ##################

    fed = h.helicsCreateValueFederateFromConfig("Fed1Config.json")
    logger.info("Created federate from config")

    sub_count = h.helicsFederateGetInputCount(fed)
    subid = {}
    for i in range(0, sub_count):
        subid[i] = h.helicsFederateGetInputByIndex(fed, i)

    pub_count = h.helicsFederateGetPublicationCount(fed)
    pubid = {}
    for i in range(0, pub_count):
        pubid[i] = h.helicsFederateGetPublicationByIndex(fed, i)

    ##############  Entering Execution Mode  ##################################
    h.helicsFederateEnterExecutingMode(fed)
    logger.info("Entered HELICS execution mode")

    # Define the total simulation time and the time interval
    total_seconds = 24
    time_interval_seconds = 1

    # Initialize the granted time and the results dictionary
    granted_time = 0
    results = {
        "Generated sin": [],
        "Generated cos": [],
        "Amplified Sin": [],
        "Amplified Cos": [],
    }

    ########## Main co-simulation loop ########################################
    while granted_time < total_seconds:

        # Get the values from the subscriptions (Or inputs from other federates)
        # If the subscription is not updated, I set the value as None
        # You could do something else, like raise an error or use the previous value
        amplified_sin = (
            h.helicsInputGetDouble(subid[0])
            if h.helicsInputIsUpdated(subid[0])
            else None
        )
        amplified_cos = (
            h.helicsInputGetDouble(subid[1])
            if h.helicsInputIsUpdated(subid[1])
            else None
        )

        # Put your logic / model / calculations here
        sin_value = math.sin((math.pi / 6) * (granted_time))
        cos_value = math.cos((math.pi / 6) * (granted_time))
        logger.debug(
            f"Sin value: {sin_value}, Cos value: {cos_value} at time {granted_time} seconds"
        )

        # A basic way of publishing the values to the other federates. You could use a loop to go through all the publications
        h.helicsPublicationPublishDouble(pubid[0], sin_value)
        h.helicsPublicationPublishDouble(pubid[1], cos_value)

        # Store the results in the results dictionary for plotting later, you don't need to do this
        results["Generated sin"].append(sin_value)
        results["Generated cos"].append(cos_value)
        results["Amplified Sin"].append(amplified_sin)
        results["Amplified Cos"].append(amplified_cos)
        logger.debug(
            f"Amplified Sin value: {amplified_sin}, Amplified Cos value: {amplified_cos} at time {granted_time} seconds"
        )

        # Time request for the next physical interval to be simulated
        requested_time_seconds = granted_time + time_interval_seconds
        granted_time = h.helicsFederateRequestTime(fed, requested_time_seconds)
        logger.debug(
            f"Granted time {granted_time} seconds while requested time {requested_time_seconds} seconds with time interval {time_interval_seconds} seconds"
        )

    # Cleaning up the federate once we've finished the co-simulation.
    destroy_federate(fed)

    # Plotting the results
    plt.figure()
    plt.title("Plot generated by Fed1")
    plt.plot(results["Generated sin"], label="Unamplified Sin", color="red")
    plt.plot(results["Generated cos"], label="Unamplified Cos", color="blue")
    amp_sin_x = [i for i, y in enumerate(results["Amplified Sin"]) if y is not None]
    amp_sin_y = [y for y in results["Amplified Sin"] if y is not None]

    plt.plot(amp_sin_x, amp_sin_y, label="Amplified Sin, from Fed 2", color="green")

    amp_cos_x = [i for i, y in enumerate(results["Amplified Cos"]) if y is not None]
    amp_cos_y = [y for y in results["Amplified Cos"] if y is not None]

    plt.plot(amp_cos_x, amp_cos_y, label="Amplified Cos, from Fed 2", color="magenta")
    plt.xlabel("Time (seconds)")
    plt.legend()
    ax = plt.gca()
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))  # Set minor tick frequency
    plt.grid(True, which="both", axis="x", color="gray", alpha=0.2)  # Reduced opacity

    plt.show()
