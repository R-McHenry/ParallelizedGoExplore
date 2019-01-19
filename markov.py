import numpy as np

def sampleMarkov(state, cpt):
    """
    Get the next state as an integer given the current state and conditional probability table
    """
    return np.random.choice(cpt.shape[0],p=cpt[state])

def createMarkov(trajectory, size):
    """
    Create a markov chain by counting all action transitions from one frame to the next in a given trajectory
    """
    #initialize with ones to prevent divide by zero and allow some random actions to be possible still
    cpt = np.ones((size,size))
    for i in range(len(trajectory)-1):
        crt = trajectory[i]
        nxt = trajectory[i+1]
        cpt[crt,nxt] += 1
    for i in range(size):
        cpt[i,:] /= cpt[i,:].sum()
    return cpt

def randMarkov(eye, size):
    """
    Create a random markov chain by summing random uniform values with an identity matrix scaled by eye.
    """
    cpt = np.random.rand(size,size)
    cpt += np.eye(size)*eye    
    for i in range(size):
        cpt[i,:] /= cpt[i,:].sum()
    return cpt