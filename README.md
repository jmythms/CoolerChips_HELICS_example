

# A very basic HELICS example, and how to setup a basic federate. 

## How to run this example:

1. Install pyHELICS: `pip install helics`

![image](https://github.com/jmythms/CoolerChips_HELICS_example/assets/45446967/8ac2d911-1bce-4a48-9758-66f77f84d88f)

2. Clone this repo: `git clone <copied link from above>`
3. Move to the cloned directory: `cd <path to cloned directory>`
4. Run using the runner.json:  `helics run --path=Runner.json`

## What is happening here?

There are two federates (in our case models), that are running together.

 - Federate 1 runs on a one second timestep, Federate 2 runs on a two second timestep.
 - The timesteps are being co-ordinated by HELICS. 
 - They are also
   subscribed to each other.

  

The first federate (Fed 1) generates two signals, 
`sin(pi*simulation_time/6)` 
and 
`cos(pi*simulation_time/6)`.
It publishes these values (sends it to HELICS).

  
The second federate (Fed 2) is subscribed to these two signals. 

 - When it receives these signals, it will amplify them (multiply the
   value by 2). 
   It will then publish these amplified values which can be seen by the first federate.

## What do these files do, can I learn more?

Runner.json: This file tells HELICS to launch three federates named `cooler_chips_example_broker`, `First_federate`, and `Second_federate`. 

Fed1.py, Fed2.py: Instances of simulation executables that models a group of objects or an individual objects.

Fed1Config.json, Fed2Config.json: Specifies how the federates will communicate with to other federates in the federation. 

These definitions were taken from or adapted from the official HELICS documentation. You can read more of the same here:  (https://docs.helics.org/en/latest/user-guide/fundamental_topics/fundamental_topics_index.html)

## Expected results when you run this:

![image](https://github.com/jmythms/CoolerChips_HELICS_example/assets/45446967/5a9a1a10-f54a-46e1-9db4-24fcf6d26557)

## What am I expected to do with this?

Figure out how to make your model work like in one of the Fedn.py files. ([Example](https://github.com/jmythms/CoolerChips-2/blob/aefb615a4e076054735904efac840f0805a1799b/Fed1.py#L59-L62))
