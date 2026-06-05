def main(env_dir="venv", req_file="requirements.txt"):
    import venv
    import os
    import sys
    import subprocess as sbp

    env_builder = venv.EnvBuilder(with_pip=True, clear=True)
    env_builder.create(env_dir=env_dir)

    if sys.platform == "win32":
        python_exe = os.path.join(env_dir, "Scripts", "python.exe")
    else:
        python_exe = os.path.join(env_dir, "bin", "python")
    
    if os.path.exists(req_file):
        print(f"Installing requirements from {req_file}...")
        sbp.check_call([python_exe, "-m", "pip", "install", "-r", req_file])
        # for mac os
        if sys.platform == "darwin":
            #installing homebrew 
            try:
                brew_command = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
                os.system(brew_command)
                
                # now with this im installing ffmpeg
                sbp.check_call(["brew","install","ffmpeg"])
                print("worked!")
            except:
                print("unable to instal ffmpeg on macos")
                
        elif sys.platform == "win32":
            try:    
                winget_command = 'Install-Script -Name winget-install -Force; winget-install'
                os.system(winget_command)
                # now with this installing ffmpeg
                sbp.check_call(["powershell", "-Command","Install-Script -Name winget-install -Force; winget-install"])
                print("workeddd!")
            except:
                print("unable to install ffmpeg on windows")
                
        else:
            try:
                # apt is pre-installed in ubuntu systems 
                sbp.check_call(["sudo","apt","install","ffmpeg"])
                print("worked")
            except:
                print("unable to install ffmpeg on linux(ubuntu)")
    else:
        print(f"No {req_file} found. Skipping installation.")


if __name__ == "__main__":
    main()