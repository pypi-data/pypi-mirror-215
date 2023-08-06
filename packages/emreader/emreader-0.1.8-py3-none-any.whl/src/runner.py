import os
import subprocess

def run():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    subprocess.call(['streamlit', 'run', 'app.py'])


if __name__ == '__main__':
    run()
