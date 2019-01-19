import os
import sys
import time
import retro.data
import numpy as np
import ray
import imageio

#Action set for sonic the hedgehog
#Allowing for any combination of valid moves
#Removing redundant and useless actions like look up, hold down left and right, other jump buttons, etc
action_set = [
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,0,0,0,0],
    [1,0,0,0,0,1,0,0,0,0,0,0],
    [1,0,0,0,0,0,1,0,0,0,0,0],
    [1,0,0,0,0,0,0,1,0,0,0,0],
    [0,0,0,0,0,1,1,0,0,0,0,0],
    [0,0,0,0,0,1,0,1,0,0,0,0],
    [1,0,0,0,0,1,1,0,0,0,0,0],
    [1,0,0,0,0,1,0,1,0,0,0,0]
]

def trajectoryToGif(game, state, trajectory, skip, name):
    """
    Re run a saved trajectory and save the result
    """
    frames = []
    env = retro.make(game=game,state=state)
    observation = env.reset()
    i=0
    for action in trajectory:
        observation, reward, done, info = env.step(action_set[ action] )
        if (skip and i%2==0) or (not skip):
            frames.append(observation)
        i+=1
    
    imageio.mimwrite(name, frames, format='GIF-FI', fps=30)
    env.close()

def frameToCell(frame, info):
    """
    Convert a frame and game info to a cell representation
    """
    return str((info['x']//32,info['y']//32,info['act'],info['zone']))

def getInitial(game, state):
    """
    Output an initial cell, emulator state, trajectory and trajectory score
    """
    env = retro.make(game=game, state=state)

    env.reset()
    observation, reward, done, info = env.step( env.action_space.sample() )
    env.reset()

    cell = frameToCell(observation, info)
    state =  env.em.get_state()
    env.close()
    return (cell, state, [], 0)

def verifyTrajectory(game, initialState, trajectory, finalState):
    """
    Verify that a trajectory of moves reaches the associated game state, in case saved trajectories to become out of sync with the emulator states
    """
    env = retro.make(game=game,state=initialState)
    observation = env.reset()

    for action in trajectory:
        observation, reward, done, info = env.step(action_set[ action] )

    observation, reward, done, info = env.step(action_set[ 0 ] )
    a = (str(info['x']) +', '+str(info['y']))

    env.em.set_state(finalState)
    observation, reward, done, info = env.step(action_set[ 0 ] )
    b = (str(info['x']) +', '+str(info['y']))
    env.close()
    if a==b:
        print('Verified trajectory')
    else:
        print('Verify failed, locations not equal:')
        print(a)
        print(b)

def install_games_from_rom_dir(romdir):
    """
    Add the ROMs to the Retro Game list
    """
    roms = [os.path.join(romdir, rom) for rom in os.listdir(romdir)]
    retro.data.merge(*roms, quiet=False)
    
    
