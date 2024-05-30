import subprocess
from pathlib import Path

def git_pull_in_directories(root_dir):
    for path in Path(root_dir).rglob('*.git'):
        parent_dir = path.parent
        print(f"Exécution de 'git pull' dans : {parent_dir}")
        
        try:
            status_process = subprocess.run(['git', 'status', '--porcelain'], cwd=parent_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            if status_process.stdout:
                print(f"\033[91mDes modifications locales ont été détectées dans {parent_dir}. 'git clean' ne sera pas exécuté pour éviter des conflits.\033[0m")
                continue
        
            process = subprocess.Popen(['git', 'clean', '-fdx'], cwd=parent_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

            for line in process.stdout:
                print(line, end='')

            process.wait()
            if process.returncode != 0:
                print(f"Erreur lors de l'exécution de 'git clean' dans {parent_dir}")
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de l'exécution de 'git clean' dans {parent_dir}: {e.stderr.decode()}")

    print("git clean a été exécuté dans tous les dossiers parent .git trouvés.")

if __name__ == '__main__':
    try:
        git_pull_in_directories('C:/Data/Repos')
    except Exception as e:
        print(f"Une erreur est survenue lors de l'exécution du script: {e}")
    finally:
        input('Appuyez sur une touche pour continuer...')