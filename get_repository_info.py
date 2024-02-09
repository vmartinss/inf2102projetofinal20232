import requests
import csv

def get_repo_info(github_repo_url, token):
    repo_name = github_repo_url.split('/')[-1]
    user_name = github_repo_url.split('/')[-2]
    
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'Bearer {token}'
    }
    
    try:
        repo_info_url = f"https://api.github.com/repos/{user_name}/{repo_name}"
        response = requests.get(repo_info_url, headers=headers)
        data = response.json()

        if 'message' in data and data['message'] == 'Not Found':
            print(f"Repository {github_repo_url} not found.")
            return None

        # Contagem de contribuidores
        contributors_url = f"https://api.github.com/repos/{user_name}/{repo_name}/contributors"
        contributors_response = requests.get(contributors_url, headers=headers)
        contributors_data = contributors_response.json()

        # Contagem de commits
        commits_url = f"https://api.github.com/repos/{user_name}/{repo_name}/commits"
        commits_response = requests.get(commits_url, headers=headers)
        commits_data = commits_response.json()

        # Adquirir LOC
        languages_url = f"https://api.github.com/repos/{user_name}/{repo_name}/languages"
        languages_response = requests.get(languages_url, headers=headers)
        languages_data = languages_response.json()
        loc = sum(languages_data.values()) 

        return {
            'Repository Name': data['name'],
            'Stars': data['stargazers_count'],
            'Number of Contributors': len(contributors_data),
            'Watching': data['subscribers_count'],
            'Commits': len(commits_data),
            'LOC': loc
        }
    except Exception as e:
        print(f"Error fetching data for {github_repo_url}. Error: {e}")
        return None

def save_to_csv(repositories_info, file_name="repository_info.csv"):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Repository Name', 'Stars', 'Number of Contributors', 'Watching', 'Commits', 'LOC'])
        
        for repo_info in repositories_info:
            if repo_info:
                writer.writerow([repo_info['Repository Name'], repo_info['Stars'], 
                                 repo_info['Number of Contributors'], repo_info['Watching'],
                                 repo_info['Commits'], repo_info['LOC']])


token = "insira_seu_token_aqui" #Insira seu token do GitHub aqui
repository_urls = ["https://github.com/weblegacy/struts1", "https://github.com/r5v9/persist"]  # Adicione as URLs dos repositórios aqui

repositories_info = [get_repo_info(repo,token) for repo in repository_urls]
repositories_info = [info for info in repositories_info if info is not None]

save_to_csv(repositories_info)