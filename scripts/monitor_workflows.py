import os, sys, requests, argparse
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--fail-on-red', action='store_true')
    args = ap.parse_args()
    token = os.environ.get('GITHUB_TOKEN')
    if not token: sys.exit("GITHUB_TOKEN not set")
    headers = {"Authorization": f"token {token}"}
    r = requests.get(f"https://api.github.com/repos/{args.repo}/actions/runs?per_page=5", headers=headers)
    for run in r.json().get('workflow_runs', []):
        print(f"[{run['conclusion']}] {run['name']} - {run['html_url']}")
        if args.fail_on_red and run['conclusion'] == 'failure':
            sys.exit(1)
if __name__ == '__main__': main()
