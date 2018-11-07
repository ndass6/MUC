import imageio
imageio.plugins.ffmpeg.download()

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import easygui, sys, os, subprocess


if not easygui.ccbox("Select the full video."):
    sys.exit(0)
videoPath = easygui.fileopenbox(filetypes=['*.mp4'])

if not easygui.ccbox('Determine the time in the full video when the "Start Experiment" button was pressed.'):
    sys.exit(0)
if sys.platform == "win32":
    os.startfile(videoPath)
else:
    opener ="open" if sys.platform == "darwin" else "xdg-open"
    subprocess.call([opener, videoPath])

offset = easygui.integerbox('Type in the time in the full video when the "Start Experiment" button was pressed.')
if not offset:
    sys.exit(0)

if not easygui.ccbox("Select the clip directory."):
    sys.exit(0)
clipPath = easygui.diropenbox()

if not easygui.ccbox("Select the log file."):
    sys.exit(0)
logPath = easygui.fileopenbox(filetypes=['*.txt'])

logFile = open(logPath, 'r')
times = [int(line.split(' ')[0]) for line in logFile]
for pos in range(len(times) - 1):
    ffmpeg_extract_subclip(videoPath, offset + times[pos], offset + times[pos + 1],
        targetname = clipPath + "/Clip" + ("0" if pos + 1 < 10 else "") + str(pos + 1) + ".mp4")
