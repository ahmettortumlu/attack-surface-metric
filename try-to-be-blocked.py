import subprocess

def run_nmap(target):
    command = f'nmap {target}'
    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        print(f"Scan result for {target}:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error while scanning {target}:\n{e.stderr}")

def main():
    target_domain = input("Enter the URL: ")
    num_scans = 1000

    for _ in range(num_scans):
        run_nmap(target_domain)

if __name__ == "__main__":
    main()
