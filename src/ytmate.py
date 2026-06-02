print("Loading....")
import yt_dlp as ytdlp
import converter as con
import subprocess as sbp
import setup
import platform as plf
sbp.run("clear")

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
    print("1. Quick download (Best Quality)")
    print("2. Download single video")
    print("3. Download playlist")
    print("4. Exit")

    choice = int(input("Choice: "))

    # Quick download
    if choice == 1:
        link = str(input("Enter video link: "))
        try:
            ydl_opts = {
                'format': 'bv+ba/b',
                'quiet': False,
                'no_warnings': False,
            }
            with ytdlp.YoutubeDL(ydl_opts) as ydl:
                print("Downloading best quality...")
                ydl.download([link])
            sbp.run("clear")
            print("Downloaded !!!")
        except Exception as e:
            print(f"Error: {e}")
            print("Please try again.")
    
    # Single Video with format information
    elif choice == 2:
        yt_url = str(input("Enter video link:"))
        audio_ext = str(input("enter the audio extension:"))
        video_ext = str(input("enter the video extension:"))
        
        if(video_ext =="mp4") :
            video_type = 137
        elif(video_ext =="webm"):
            video_type = 248
        elif(video_ext =="mov"):
            video_type = 123
        else:
            video_type = 137
        
        if(audio_ext =="webm"):
            audio_type = 251
        elif(audio_ext =="m4a"):
            audio_type = 140
        else:
            audio_type = 251

        try:
            ydl_opts = {
                'quiet': False,
                'no_warnings': True,
                'format': f'{video_type} + {audio_type}',
                'merge_output_format' : 'mp4'
            }
            with ytdlp.YoutubeDL(ydl_opts) as ydl:
                print("downloading...")
                ydl.download([yt_url])
            sbp.run("clear")
            print("yayy it worked")
        except Exception as e:
            print("please try again")
    
    # Playlist Download
    elif choice == 3:
        try:
            playlist_url = input("Enter playlist link: ")
            
            # Get playlist info
            ydl_opts_info = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': 'in_playlist',
            }
            with ytdlp.YoutubeDL(ydl_opts_info) as ydl:
                info = ydl.extract_info(playlist_url, download=False)
                playlist_title = info.get('title', 'playlist')
                print(f"\nPlaylist: {playlist_title}\n")
            
            # Create folder for playlist
            playlist_folder = sanitizePath(playlist_title)
            sbp.run(["mkdir", "-p", playlist_folder])
            
            # Download playlist with best quality audio+video merged
            ydl_opts_download = {
                'format': 'bv+ba/b',
                'outtmpl': f'{playlist_folder}/%(title)s.%(ext)s',
                'quiet': False,
                'no_warnings': False,
            }
            with ytdlp.YoutubeDL(ydl_opts_download) as ydl:
                print(f"Downloading playlist to {playlist_folder}...")
                ydl.download([playlist_url])
            sbp.run("clear")
            print("Playlist downloaded !!!")
        except Exception as e:
            print(f"Error: {e}")
            print("Please use other options or try again later.")
    
    # Exit
    elif choice == 4:
        sbp.run("clear")
        print("Thank you!!")
        break
    
    # Invalid input
    else:

        sbp.run("clear")
        print("Invalid Input!! Try again")
