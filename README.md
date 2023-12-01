
# A very basic HELICS example, and how to setup a basic federate. 

## How to run:

0. Install pyHELICS: `pip install helics`

![image](https://github.com/jmythms/CoolerChips-2/assets/45446967/adbcd66a-f943-425b-9d50-306233822f28)



1. Clone this repo: `git clone <copied link from above>`
2. Move to the cloned directory: `cd <path to cloned directory>`
3. Run using the runner.json:  `helics run --path=Runner.json`

## What is happening here?

There are two federates (in our case models), that are running together.

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

## Expected results when you run this:

![image](https://github.com/jmythms/CoolerChips-2/assets/45446967/ce6e1125-238f-4af3-8c8d-cfb2f7916b1e)

## What should I do with this?

Figure out how to make your model work like in one of the Fedn.py files. ([Example](https://github.com/jmythms/CoolerChips-2/blob/aefb615a4e076054735904efac840f0805a1799b/Fed1.py#L59-L62))
