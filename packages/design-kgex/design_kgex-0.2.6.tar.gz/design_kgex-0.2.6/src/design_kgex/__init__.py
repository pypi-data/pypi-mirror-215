import subprocess
import sys
import os
from IPython import get_ipython

try:
    __IPYTHON__
    _in_ipython_session = True
except NameError:
    _in_ipython_session = False

if ('COLAB_GPU' in os.environ) or (_in_ipython_session):
    subprocess.run(['pip', 'install', 'Ipython', '--upgrade'])
    ipython = get_ipython()
    ipython.magic("load_ext autoreload")
    ipython.magic("autoreload 2")

if 'en_core_web_sm' not in sys.modules:
    print("The required language model 'en_core_web_sm' is not installed. \n Installing now...")
    subprocess.run(['python', '-m', 'spacy', 'download', 'en_core_web_sm'], stdout=subprocess.PIPE)
    print("The required language model 'en_core_web_sm' is installed successfully!")

if 'en_core_web_trf' not in sys.modules:
    print("The required language model 'en_core_web_trf' is not installed. \n Installing now...")
    subprocess.run(['python', '-m', 'spacy', 'download', 'en_core_web_trf'], stdout=subprocess.PIPE)
    print("The required language model 'en_core_web_trf' is installed successfully! \n\n **************************************\n\nIf you are importing the module in a colab environment, the runtime could restart. In that case, please re-run the cells instead of terminating the instance.\n")




