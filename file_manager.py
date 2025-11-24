import os

def save_game_seed(seed, filename="rec/minesweeper_save.txt"):
    #Saving RNG seed
    try:
        with open(filename, "w") as f:
            f.write(f"Seed: {seed}\n")
    except IOError as err:
        print(f"Error saving seed: {err}")

def load_best_time(filename="best_time.txt"):
    try:
        with open(filename, "r") as f:
            best = f.read().strip()
    except FileNotFoundError:
        # file doesn't exist yet
        with open(filename, "w") as f:
            f.write("N/A")
        best = "N/A"
    return best

def save_best_time(current_time, filename="best_time.txt"):
    # current_time is a float
    best = load_best_time(filename)
    if best == "N/A":
        # no previous best, so current becomes best
        with open(filename, "w") as f:
            f.write(str(current_time))
        return current_time
    else:
        try:
            best_float = float(best)
            if current_time < best_float:
                # we have a new best!
                with open(filename, "w") as f:
                    f.write(str(current_time))
                return current_time
            else:
                # no change
                return best_float
        except ValueError:
            #rewriting time
            with open(filename, "w") as f:
                f.write(str(current_time))
            return current_time
