import subprocess
from pathlib import Path


def get_current_branch(cwd):
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    return result.stdout.strip()


def get_all_branches(cwd):
    result = subprocess.run(
        ["git", "branch", "--list"],
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    branches = result.stdout.strip().split("\n")
    return [branch.strip().lstrip('* ') for branch in branches]


def git_fast_forward(cwd, branch):
    print(f"Tentative de mise à jour de la branche {branch}")
    result = subprocess.run(
        ["git", "checkout", branch],
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    if result.returncode != 0:
        print(f"Erreur lors de l'exécution de 'git checkout {branch}' : {result.stderr.strip()}")
        return

    result = subprocess.run(
        ["git", "pull", "--ff-only"],
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    if result.returncode != 0:
        print(f"Erreur lors de l'exécution de 'git pull --ff-only' : {result.stderr.strip()}")
    else:
        print(f"Branche {branch} mise à jour avec succès.")


def git_pull_all_branches(root_dir):
    for path in Path(root_dir).rglob("*.git"):
        parent_dir = path.parent
        print(f"#############################################")
        print(f"Mise à jour de : {parent_dir}")

        try:
            status_process = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=parent_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )
            if status_process.stdout:
                print(
                    f"\033[91mDes modifications locales ont été détectées dans {parent_dir}. 'git pull' ne sera pas exécuté pour éviter des conflits.\033[0m"
                )
                continue

            current_branch = get_current_branch(parent_dir)
            branches = get_all_branches(parent_dir)

            for branch in branches:
                git_fast_forward(parent_dir, branch)

            # Revenir à la branche initiale
            subprocess.run(
                ["git", "checkout", current_branch],
                cwd=parent_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )
            print(f"Revenu à la branche {current_branch} dans {parent_dir}")

        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de l'exécution de 'git pull' dans {parent_dir}: {e.stderr.decode()}")
        except Exception as e:
            print(f"Une erreur inattendue est survenue dans {parent_dir}: {e}")
        finally:
            print(f"#############################################")


if __name__ == "__main__":
    try:
        git_pull_all_branches("C:/Data/Business Evolution")
        git_pull_all_branches("C:/Data/Qualité/Projets")
        print("git pull a été exécuté dans tous les dossiers parent .git trouvés.")
    except Exception as e:
        print(f"Une erreur est survenue lors de l'exécution du script: {e}")
    finally:
        input("Appuyez sur une touche pour continuer...")
