import os
import sys
import glob

#define template to simplify the script above
CMDTEMPLATE = 'cmd.exe /C "__PATH__\\__EXEFILE__ $@"'

#Generate customized scripts inner env path scripts to simplify the use of binaries inside wsl bash
def generateCmdHackScripts(directory):
  for file in glob.glob(os.path.join(directory, 'Scripts','*.exe')):
    fullPath = os.path.abspath(file)
    path, exeFile = os.path.split(fullPath)

    cmdCommand = CMDTEMPLATE.replace('__PATH__', path).replace('__EXEFILE__',exeFile).replace('\\','\\\\')
    
    with open(os.path.splitext(fullPath)[0], 'w', newline='\n') as f:
        f.write(cmdCommand)

#Use conda to activate de environment
def activateEnvironment(directory):
    activatePath = os.path.join(os.path.abspath(directory), 'Scripts', 'activate')

    with open(activatePath, 'r', newline='\n') as f:
        activateContent = f.read()
        
        pathComponents = os.path.abspath(directory).split(os.path.sep)
        pathComponents[0] = pathComponents[0][:-1].lower()

        wslPath = '/mnt/' + '/'.join(pathComponents) + '/Scripts/'
        print(wslPath)


def main():
  if len (sys.argv) < 2:
    print('Usage: activateWsl.sh: <path>')
    sys.exit(1)

  dir = sys.argv[1]
  print('Processing directory: %s' % (os.path.abspath(dir)))
  print('\n')
  generateCmdHackScripts(dir)
  activateEnvironment(dir)

if __name__ == "__main__":
	main()
