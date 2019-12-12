## -------------------------------------------------------------------
## BH Merging Simulation
## (C) Gabriele LUCULLI
## -------------------------------------------------------------------
## -- added merging in the baricenter
## -- added run_stats to compute final mass distribution

import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
import multiprocessing as mp
import ray
import time
import random

def randomGrid(N, mass, mass_prob):
    """returns a grid of NxN random values of mass_prob"""
    t = int( time.time() * 1000.0 )
    np.random.seed( ((t & 0xff000000) >> 24) +
             ((t & 0x00ff0000) >>  8) +
             ((t & 0x0000ff00) <<  8) +
             ((t & 0x000000ff) << 24)   )
    # method 1         
    # dat = np.zeros(shape=(N,N))
    # for k in range(N):
    #     dat[k,:] = np.random.choice(mass, N, p=mass_prob, replace=True)

    # method 2
    dat = np.random.choice(mass, N * N, p=mass_prob).reshape(N, N)

    # method 3
    # fig=plt.imshow(dat)
    # plt.show()
    return dat

class BH_Merger_Model():
    def __init__(self, mass, mass_prob, updateInterval, N, alpha, **kw):
        # save params
        self.mass = mass
        self.mass_prob = mass_prob
        self.updateInterval = updateInterval
        self.N = N
        self.alpha = alpha

        # init local vars
        self.ctr = 0
        self.grid = randomGrid(N, mass, mass_prob)

    def run_stats(self, dmax):
        tot_grid = np.empty((0,), dtype=int)
        nruns = 1000

        # define main task
        @ray.remote
        def __task(id=0):
            grid = randomGrid(self.N, self.mass, self.mass_prob)

            total_mergers = -1
            while total_mergers != 0:
                grid, total_mergers = self.__update(grid, self.N, dmax)
            
            return grid[grid.nonzero()]

         # parallel execution of task
        ray.init(num_cpus=8)
        tmp = ray.get([__task.remote(k) for k in range(nruns)])
    
        tot_grid = np.concatenate(tmp).ravel()

        # plot benchmakr histogram
        plt.hist(tot_grid, bins=200, normed=True)
        H,X = np.histogram(tot_grid)
        plt.show()

    def run(self, dmax, save_to_file=""):
        # set up animation
        fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(12,6))
        img0 = ax[0].imshow(self.grid, interpolation='nearest')
        img1 = ax[1]
        img2 = ax[2]

        img1.grid()

        # execution
        self.ani = animation.FuncAnimation(fig, self.__run_animation, fargs=(img0, img1, img2, self.grid, self.N, dmax),
                                    frames=100,
                                    interval=self.updateInterval,
                                    save_count=50)

        if save_to_file != "":
             self.ani.save(save_to_file, fps=30, extra_args=['-vcodec', 'libx264'])

    def __run_animation(self, frameNum, img_grid, img_cdf, img_h, grid, N, dmax):
        total_mergers = 0

        # 1 discrete time step update
        grid, total_mergers = self.__update(grid, N, dmax)

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
            self.__print_final_state(grid)
            self.ani.event_source.stop()

        return grid

    
    # update grid after 1 run
    def __update(self, grid, N, dmax):
        total_mergers = 0
        self.ctr = self.ctr + 1
        done_ctr = 0
        dmask = np.ones((N,N))
        lmt = math.trunc(N*N*0.80)

        # for i in range(N):
            # for j in range(N):
        
        while done_ctr != N*N:
            found = 0
            for k in range(lmt):
                # select i, j
                i = random.randint(0, N-1)
                j = random.randint(0, N-1)

                if dmask[i,j] == 1:
                    found = 1
                    done_ctr += 1
                    break
            
            if found == 0:
                ndone = dmask.nonzero()
                p = random.randint(0, len(ndone[1])-1)

                if len(ndone[1]) == 0:
                    break

                i = ndone[0][p]
                j = ndone[1][p]

                done_ctr +=1

            dmask[i,j] = 0

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

        return grid, total_mergers

    # simple output function
    def __print_final_state(self, gr):
        print("\n** Simulation completed!")
        H,X = np.histogram(gr[gr.nonzero()])

        i=0
        print("** Biggest BH of " + str(X[len(X)-1]) + " at : " + str(np.argwhere(self.grid == X[len(X)-1])))
        print("** Total numer of BH : " + str(sum(H)))
        # print("** test "+str(len(H)) + " " + str(H[len(H)-1]))
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
    parser.add_argument('--run-type', dest='run_type', required=False)
    parser.add_argument('--zero-mass-density', dest='zero_mass_density', required=False)
    parser.add_argument('--mov-file', dest='movfile', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
   
    args = parser.parse_args()

    # set grid size
    N = 100
    if args.N and int(args.N) > 8:
        N = int(args.N)

    # set max distance for merging
    dmax = 5
    if args.dmax:
        dmax = int(args.dmax)

    # set run type
    run_type = 1
    if args.run_type:
        run_type = int(args.run_type)

     # set mass_prob_zero
    mass_prob_zero = 0.90
    if args.zero_mass_density:
        mass_prob_zero = float(args.zero_mass_density)

    # set output video file
    movfile = ""
    if args.movfile:
        movfile = args.movfile

    # set animation update interval
    updateInterval = 0
    if args.interval:
        updateInterval = int(args.interval)

    # setting up the values of BH masses for the grid
    umassd = 20  
    mass = range(umassd)
    mass_prob = [(1 - mass_prob_zero)/(len(mass) - 1) for i in mass]  # uniform mass distribution in 1:umassd
    mass_prob[0] = mass_prob_zero

    # mass loss percentage after merger
    alpha = 0.20

    # print info on config
    print("** Configuration: <grid-size, max-distance, unif-mass-dist, zero-mass-density> = <%3d, %3d, %3d, %1.2f>" % (N, dmax, umassd, mass_prob_zero))

    if run_type == 1:
        # single run in animation mode
        model = BH_Merger_Model(mass, mass_prob, updateInterval, N, alpha)
        final_grid = model.run(dmax, save_to_file=movfile)

        plt.show()
    else:
        # compute global stats by MC
        model = BH_Merger_Model(mass, mass_prob, updateInterval, N, alpha)
        model.run_stats(dmax)


# call main
if __name__ == '__main__':
    main()
