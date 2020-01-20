import subprocess
import os

cwd = os.getcwd()
for root, dirs, files in os.walk(cwd):
    for dir in dirs:
        if dir.startswith("TMHMM"):
            path = os.path.join(root, dir)
            for file in os.listdir(path):
                if file.endswith(".gnuplot"):
                    print(os.path.join(path, file))
                    file_path = os.path.join(path, file)
                    subprocess.check_output(["gnuplot", file_path]) # gets eps file
                    file_split = file.split("gnuplot")
                    source = file_split[0] + "eps"
                    source = os.path.join(path, source)
                    dest = file_split[0] + "jpg"
                    dest_dir = os.path.join(cwd, "plots")
                    dest = os.path.join(dest_dir, dest)
                    subprocess.check_output(["convert", "-density", "150", source, dest]) # converts to jpg and stores in plots directory

# "gnuplot <file>"
# "convert -density 150 file.eps file.jpg"
