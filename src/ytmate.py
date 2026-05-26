print("Loading....")
import pytube as py
from pytube import YouTube
import converter as con
import subprocess as sbp
import setup
import platform as  plf
sbp.run("clear")

#####################################################################################################
def filterStream(video):
    #Get the list of itag
    iTaglist = sbp.run(["pytube", "{}".format(video), "--list"], text=True, stdout=sbp.PIPE)
    iTaglist = (iTaglist.stdout).split("\n")
    #Filter out any stream without webm
    temp = []
    for stream in iTaglist:
        try:
            stream.index("webm")
            temp.append(stream)
        except:
            pass
    #Print those streams
    for stream in temp : print(stream)
#####################################################################################################
def sanitizePath(PATH):
    temp = ""
    for char in PATH:
        if char not in "qwertyuiopasdfghjklzxcvbnm1234567890QWERTYUIOPASDFGHJKLZXCVBNM":
            temp+=" "
        else:
            temp+=char
    PATH = temp
    return PATH
#####################################################################################################
while(True):
    try:
        sbp.run(["rm", "-rf", "temp"])
    except:
        pass
    #menu
    print("1. Quick download(Most friendly, however may or may not work)")
    print("2. Single Video with link")
    print("3. Full Playlist with link of playlist")
    print("4. Combine video and audio")
    print("5. Exit")

    choice = int(input("Choice: "))

    #New feature of Quick download
    if choice == 1:
        link = str(input("Enter Clean Link: "))
        yt = YouTube(link)
        print("Downloading...")
        try:
            yt.streams.filter(progressive=True, file_extension="mp4").desc().first().download()
            sbp.run("clear")
            print("Downloaded !!!")
        except:
            print("Please use the other options to download the video.")
    
    #Single Video
    elif choice == 2:
        video = str(input("Clean link: "))
        yt = py.YouTube(url=video)
        try:
            print(yt.title)
            videoStreams=yt.streams.filter(file_extension="webm", only_video=True)
            iTags = []
            for stream in videoStreams:
                list = (str)(stream).split('"')
                iTags.append(list[1]);
                print(f"Input \"{list[1]}\" for \"{list[5]}\" resolution")
            #List all formats
            InputItag = -1
            while(InputItag not in iTags):
                InputItag = str(input("Enter the itag: "))

            #Download video
            video_Down = sbp.run(["pytube", "{}".format(video), "--itag={}".format(InputItag)])
            if video_Down.returncode != 0:
                sbp.run("clear")
                print("Error Downloading")
                RuntimeWarning
            else:
                name = sbp.run(["ls"], capture_output=True)
                name = name.stdout.decode('ascii')
                name = name.split(sep="\n")
                for item in name:
                    if ".webm" in item:
                        name = item
                sbp.run(["mv", "{}".format(name), "{}.mp4".format(sanitizePath(yt.title))])
                sbp.run("clear")
                print("Downloaded !!!")
            ###########################################################################################
            print(yt.title)
            audioStreams=yt.streams.filter(file_extension="mp4", only_audio=True)
            iTags = []
            for stream in audioStreams:
                list = (str)(stream).split('"')
                iTags.append(list[1]);
                print(f"Input {list[1]} for \"{list[5]}\" & \"{list[7]}\" audio codec")
            #List all formats
            InputItag = -1
            while(InputItag not in iTags):
                InputItag = str(input("Enter the itag: "))

            #Download audio
            audio_Down = sbp.run(["pytube", "{}".format(video), "--itag={}".format(InputItag)])
            if audio_Down.returncode != 0:
                sbp.run("clear")
                print("Error Downloading")
                RuntimeWarning
            else:
                name = sbp.run(["ls"], capture_output=True)
                name = name.stdout.decode('ascii')
                name = name.split(sep="\n")
                for item in name:
                    if ".mp4" in item:
                        name = item
                sbp.run(["mv", "{}".format(name), "{}.mp4".format(sanitizePath(yt.title))])
                sbp.run("clear")
                print("Downloaded !!!")
        except:
            print("Downloading...")
            try:
                yt.streams.filter(progressive=True, file_extension="mp4").desc().first().download()
                sbp.run("clear")
                print("Video Downloaded !!!")
            except:
                print("Please use the other options to download the video.")
    #Playlist Download
    elif choice == 3:
        try:
            #Get the playlist link
            playlist=py.Playlist(input("Enter Clean link: "))

            #Create a folder to put all the videos
            print("")
            sbp.run(["mkdir", "{}".format(sanitizePath(playlist.title))])

            #Get the links to all the videos in the playlist
            playlist_videos = []
            videoTitles = []
            for url in playlist.video_urls:
                playlist_videos.append(url)

            #same Itage function: sameItag[0] = flag, and sameItag[1] = value of Itag 
            sameItag = [-1,1]

            #No of videos to create indexing when downloading via playlist
            no_of_videos = playlist.length
            index=0

            for video in playlist_videos:

                #Indexing at the top of every video
                index=index+1
                print("\n{} of {}".format(index, no_of_videos))

                #Print the title
                yt = py.YouTube(url=video)
                videoTitles.append(yt.title)
                print(yt.title)

                #Checking the sameItag flag
                if sameItag[0] == 1:

                    InputItag = sameItag[1]
                elif sameItag[0] == 0:

                    filterStream(video)

                    InputItag = int(input("Enter the itag(Enter -1 to skip this video): "))

                #used for first time set-up
                if sameItag[0] == -1:
                    sameItag[0] = int(input("Do you want to keep this setting for all the videos(1-Yes/0-No)"))

                    if sameItag[0] == 1:

                        #Since only webm video and mp4 audio can merge therefore 
                        # i am filtering out anything thats not webm for video

                        #Get the list of itag
                        iTaglist = sbp.run(["pytube", "{}".format(video), "--list"], text=True, stdout=sbp.PIPE)
                        iTaglist = (iTaglist.stdout).split("\n")
                        #Filter out any stream without webm
                        temp = []
                        for stream in iTaglist:
                            try:
                                stream.index("webm")
                                temp.append(stream)
                            except:
                                pass
                        #Print those streams
                        for stream in temp : print(stream)

                        sameItag[1] = InputItag = int(input("Enter the itag: "))
                    elif sameItag[0] == 0:

                        #Since only webm video and mp4 audio can merge therefore 
                        # i am filtering out anything thats not webm for video

                        #Get the list of itag
                        iTaglist = sbp.run(["pytube", "{}".format(video), "--list"], text=True, stdout=sbp.PIPE)
                        iTaglist = (iTaglist.stdout).split("\n")
                        #Filter out any stream without webm
                        temp = []
                        for stream in iTaglist:
                            try:
                                stream.index("webm")
                                temp.append(stream)
                            except:
                                pass
                        #Print those streams
                        for stream in temp : print(stream)

                        InputItag = int(input("Enter the itag(Enter -1 to skip this video): "))

                #Option to skip a video normally without raising an error
                if InputItag == -1:

                    sbp.run("clear")
                    print("skipping {} ....".format(yt.title))
                    continue
                
                #Downloading the video
                sbp.run(["pytube", "{}".format(video), "--itag={}".format(InputItag), "-f",])

                #pwd = sbp.run("pwd", capture_output=True, text=True)
                #pwd = (pwd.stdout)[:-1]
                #videoPath = sanitizePath(f"temp/{index}.webm")
                #audioPath = sanitizePath(f"temp/{index}.mp4")
                #titlePath = sanitizePath(f"{playlist.title}/{index}")
                
                #Alert:- You have used a OS specific symbol to fix this# You are forcing mp4 for audio and webm for video
                #Alert:- You have used a OS specific symbol to fix this# You are forcing mp4 for audio and webm for video
                #Alert:- You have used a OS specific symbol to fix this# You are forcing mp4 for audio and webm for video
                #con.convert(videoPath, audioPath, titlePath)
                #Alert:- You have used a OS specific symbol to fix this# You are forcing mp4 for audio and webm for video
                #Alert:- You have used a OS specific symbol to fix this# You are forcing mp4 for audio and webm for video
                #Alert:- You have used a OS specific symbol to fix this# You are forcing mp4 for audio and webm for video
        except:
            print("Please use other options or try again later.")

    #Combine Audio and Video
    elif choice == 4:
        try:
            #Get the video and audio files and the title of the output file
            video = str(input("Enter the video file name with extension: "))
            audio = str(input("Enter the audio file name with extension: "))
            title = str(input("Enter the name of the output file without extension: "))
            
            #Convert
            con.convert(video, audio, title)
        except:
            print("Please use other options or try again later.")
    
    #Exit
    elif choice == 5:

        sbp.run("clear")
        print("Thank you!!")
        break
    
    #Invalid input
    else:

        sbp.run("clear")
        print("Invalid Input!! Try again")
