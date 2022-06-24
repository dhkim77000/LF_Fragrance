import os
import re
import shutil
import time
if __name__ == "__main__":
    while True:
        for directory in os.listdir('/tmp/') :
            print('--------------cleaning cache-------------')
            if re.fullmatch('.*.com.google.Chrome..*',directory):
                try:
                    print(directory)
                    shutil.rmtree('/tmp/'+directory)
                except NotADirectoryError:
                    continue
            time.sleep(30*60)
