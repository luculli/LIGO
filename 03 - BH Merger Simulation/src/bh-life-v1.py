## -------------------------------------------------------------------
## BH Merging Simulation
## (C) Gabriele LUCULLI
## -------------------------------------------------------------------
## -- added merging in the baricenter

import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

def randomGrid(N, mass, mass_prob):
    """returns a grid of NxN random values"""
    return np.random.choice(mass, N * N, p=mass_prob).reshape(N, N)

class Anim():
    def __init__(self, grid, updateInterval, N, alpha, **kw):
        # save params
        self.grid = grid
        self.updateInterval = updateInterval
        self.N = N
        self.alpha = alpha

        self.ctr = 0

    def run(self, fig, img0, img1, img2, dmax):
        self.ani = animation.FuncAnimation(fig, self.update, fargs=(img0, img1, img2, self.grid, self. N, dmax),
                                    frames=100,
                                    interval=self.updateInterval,
                                    save_count=50)
    
    # update grid after 1 run
    def update(self, frameNum, img_grid, img_cdf, img_h, grid, N, dmax):
        total_mergers = 0
        self.ctr = self.ctr + 1

        for i in range(N):
            for j in range(N):

                # apply BH rules
                if grid[i, j] != 0:
                    stop = False

                    for k in [x+1 for x in range(dmax)]:
                        if stop == True:
                            break

                        # line 0 : y constant
                        dx = ([-x for x in range(k+1)] + [x for x in range(k+1)])[1:]
                        dy = [k, -k]

                        for p_x in dx:
                            if stop == True:
                                break

                            for p_y in dy:
                                newx = (i+p_x) % N
                                newy = (j+p_y) % N

                                if grid[newx, newy] != 0:
                                    # baricenter
                                    x_m = math.trunc((i*grid[i,j]+p_x*grid[newx, newy])/(grid[i,j]+grid[newx, newy])) % N
                                    y_m = math.trunc((j*grid[i,j]+p_y*grid[newx, newy])/(grid[i,j]+grid[newx, newy])) % N

                                    # mass merging
                                    grid[x_m,y_m] = (grid[i,j] + grid[newx, newy]) * (1-self.alpha)
                                    grid[i,j] = 0
                                    grid[newx, newy] = 0

                                    # mixed info
                                    total_mergers = total_mergers + 1
                                    stop = True
                                    break

                        if stop == True:
                            break

                        # line 1 : x constant
                        dx = [k, -k]
                        dy = ([-x for x in range(k+1)] + [x for x in range(k+1)])[1:]

                        for p_x in dx:
                            if stop == True:
                                break

                            for p_y in dy:
                                newx = (i+p_x) % N
                                newy = (j+p_y) % N

                                if grid[newx, newy] != 0:
                                    # baricenter
                                    x_m = math.trunc((i*grid[i,j]+p_x*grid[newx, newy])/(grid[i,j]+grid[newx, newy])) % N
                                    y_m = math.trunc((j*grid[i,j]+p_y*grid[newx, newy])/(grid[i,j]+grid[newx, newy])) % N

                                    # mass merging
                                    grid[x_m,y_m] = (grid[i,j] + grid[newx, newy]) * (1-self.alpha)
                                    grid[i,j] = 0
                                    grid[newx, newy] = 0

                                    # mixed info
                                    total_mergers = total_mergers + 1
                                    stop = True
                                    break               

        # compute mass distribution
        H,X = np.histogram(grid[grid.nonzero()])
        delta = X[1] - X[0]
        CDF = np.cumsum(H)*delta

        # update plots
        img_grid.set_data(grid)
        img_cdf.plot(X[1:], CDF)
        img_h.hist(grid[grid.nonzero()])

        # info text output
        print("Run #" + str(self.ctr) +  " completed");

        # stop
        if total_mergers == 0:
            print_final_state(grid)
            self.ani.event_source.stop()

        return grid

def print_final_state(gr):
    print("\n** Simulation completed!")
    H,X = np.histogram(gr[gr.nonzero()])

    i=0
    for k in range(len(H)):
        if H[k] !=0:
            i = i + 1
            print("Set BH #"+str(i)+" : "+str(H[k])+" times the mass range ("+str(math.trunc(X[k]))+"-"+str(math.trunc(X[k+1]))+")")



# main() function
def main():

    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(
        description="Runs Game of BH Merger simulation.")

    # add arguments
    parser.add_argument('--grid-size', dest='N', required=False)
    parser.add_argument('--max-dist', dest='dmax', required=False)
    parser.add_argument('--mov-file', dest='movfile', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
   
    args = parser.parse_args()

    # set grid size
    N = 100
    if args.N and int(args.N) > 8:
        N = int(args.N)

    # set max distance for merging
    dmax = 10
    if args.dmax:
        dmax = int(args.dmax)

    # set animation update interval
    updateInterval = 50
    if args.interval:
        updateInterval = int(args.interval)

    # setting up the values of BH masses for the grid
    umassd = 20
    mass = range(umassd)
    mass_prob_zero = 0.8
    mass_prob = [(1 - mass_prob_zero)/(len(mass) - 1) for i in mass]
    mass_prob[0] = mass_prob_zero

    # mass loss percentage after merge
    alpha = 0.20

    # print info on config
    print("** Configuration: <grid-size, max-distance, unif-mass-dist, zero-mass-density> = <%3d, %3d, %3d, %1.2f>" % (N, dmax, umassd, mass_prob_zero))

    # declare grid
    grid = np.array([])

    # populate grid with random masses
    grid = randomGrid(N, mass, mass_prob)

    # set up animation
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(12,6))
    img0 = ax[0].imshow(grid, interpolation='nearest')
    img1 = ax[1]
    img2 = ax[2]

    img1.grid()

    # run
    ani = Anim(grid, updateInterval, N, alpha)
    final_grid = ani.run(fig, img0, img1, img2, dmax)

    # # of frames?
    # set output file
    if args.movfile:
        ani.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264'])

    plt.show()


# call main
if __name__ == '__main__':
    main()
