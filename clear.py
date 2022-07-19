import os
import re
import shutil
import time
import pdb
if __name__ == "__main__":
    while True:
        for directory in os.listdir('/tmp/') :
            #pdb.set_trace()
            print('--------------cleaning cache-------------')
            print(directory)
            if re.fullmatch('.*.com.google.Chrome..*',directory) != None:
                try:
                    print("Deleting------"+directory)
                    shutil.rmtree('/tmp/'+directory)
                except NotADirectoryError:
                    continue
        time.sleep(30*60)
