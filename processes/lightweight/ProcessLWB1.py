import constants
import Lightweight

if __name__ == '__main__':

    process = Lightweight.Lightweight(constants.PB_PORT, "B1")
    process.start()
