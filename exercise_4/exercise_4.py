import time
import objective_functions as ob
import optimization as op

# Rosenbrock is working according to task 2 where PSO is more favourable than DE, but there are other objective functions to try as well.
# If you want ot try other function, uncomment it in objective_fucntions.py, but keep in mind that some of them might not work properly.

# parameter average_graph is for showing development of each generation's average
# parameter show_gen is for showing each generation's average in console
# parameter plot_candidate is for plotting location of each individual in the population, only work when number_of_variables = 2 or 3
    # plot_candidate = True is task 3

# Not reccommended to put average_graph=True and plot_candidate=True ate the same time
# Program will work but very slowly

def exercise_4(inputs): # DO NOT CHANGE THIS LINE

    runs = 30
    lower = -5
    upper = 10
    begin = time.time()
    try:
        op.compare_x_runs(runs, ob.rosenbrock, 1000, 3, 100, lower, upper, average_graph=False, show_gen=False, plot_candidate=False, plot_delay=0.0001)
    except KeyboardInterrupt:
        print("Exiting...")
        quit()
    print(f"Total time used: {time.time()-begin} seconds for {runs} run(s)")

    output = inputs

    return output       # DO NOT CHANGE THIS LINE

exercise_4(1)