import requests
from bs4 import BeautifulSoup

# URL da busca no Job Bank para Halifax
url = "https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring=data+engineer&location=Halifax"

# Faz a requisição HTTP para obter o HTML da página
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = soup.find_all("a", class_="resultJobItem")
    seen_links = set()  # Para evitar duplicatas

    for job in jobs:
        title = job.find("span", class_="noctitle").text.strip()
        company = job.find("li", class_="business").text.strip()

        # Verifica se é remoto
        remote_tag = job.find("span", class_="telework")
        is_remote = remote_tag and "Remote" in remote_tag.text

        # Obtém a localização
        location_tag = job.find("li", class_="location")
        location = location_tag.text.replace("Location", "").strip() if location_tag else "Not specified"

        # Se for remoto, sobrescrevemos a localização
        if is_remote:
            location = "Remote"

        # Filtrar apenas Halifax e Remote
        if location != "Halifax (NS)" and location != "Remote":
            continue  # Pula a vaga se não for de interesse

        # Obtém o salário
        salary_tag = job.find("li", class_="salary")
        salary = salary_tag.text.replace("Salary:", "").strip() if salary_tag else "Not specified"

        # Obtém a data de postagem
        date_posted = job.find("li", class_="date").text.strip()

        # Método de aplicação
        apply_method_tag = job.find("span", class_="appmethod")
        apply_method = apply_method_tag.text.strip() if apply_method_tag else "Not specified"

        # Link da vaga
        link = "https://www.jobbank.gc.ca" + job["href"]

        # Evita duplicatas
        if link in seen_links:
            continue
        seen_links.add(link)

        # Exibindo os dados formatados
        print(f"Title: {title}")
        print(f"Company: {company}")
        print(f"Location: {location}")
        print(f"Salary: {salary}")
        print(f"Date Posted: {date_posted}")
        print(f"Apply Method: {apply_method}")
        print(f"Link: {link}")
        print("-" * 50)

else:
    print("Failed to retrieve job listings. Status code:", response.status_code)
