import constants
import Lightweight

if __name__ == '__main__':

    process = Lightweight.Lightweight(constants.PA_PORT, "A3")
    process.start()
