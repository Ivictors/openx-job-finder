from playwright.sync_api import sync_playwright
import json
from datetime import datetime, timedelta
import re
import os

SEARCH_TERMS = [
    "Java Junior",
    "Java Estagiario",
    "Backend Junior",
    "Spring Boot",
    "Desenvolvedor Java",
    "Programador Java",
]

OUTPUT_DIR = "output"

VALID_LOCATIONS = [
    "remoto",
    "remote",
    "sao paulo",
    "são paulo",
    "sp",
    "capital",
    "brasil",
    "brazil",
    "home office",
    "hibrido",
    "hybrid",
]


def is_valid_location(location_text):
    if not location_text:
        return True
    
    location_lower = location_text.lower()
    
    invalid_locations = [
        "india", "mexico", "argentina", "chile", "colombia",
        "usa", "united states", "estados unidos", "europa",
        "alemanha", "espanha", "portugal"
    ]
    
    for invalid in invalid_locations:
        if invalid in location_lower:
            return False
    
    return True


def is_relevant_junior(title):
    title_lower = title.lower()

    has_level = any(
        kw in title_lower
        for kw in ["junior", "jr", "estagiario", "trainee", "pleno", "entry level", "intern"]
    )

    has_tech = any(
        kw in title_lower
        for kw in [
            "java",
            "spring",
            "backend",
            "back-end",
            "software",
            "developer",
            "programador",
            "desenvolvedor",
            "engineer",
        ]
    )

    has_exclude = any(
        kw in title_lower
        for kw in [
            "senior",
            "sênior",
            "sr",
            "lead",
            "arquiteto",
            "architect",
            "director",
            "gerente",
            "manager",
            "head",
            "php",
            "node",
            "react",
            "angular",
            "vue",
            "frontend",
            "mobile",
        ]
    )

    has_java_backend = "java" in title_lower or "spring" in title_lower or (
        ("backend" in title_lower or "back-end" in title_lower) and has_level
    )

    return has_level and has_tech and not has_exclude and has_java_backend


def parse_relative_date(date_text):
    today = datetime.now()
    date_text = date_text.lower()

    if any(kw in date_text for kw in ["hoje", "today", "hora", "hour", "agora", "now"]):
        return today.strftime("%Y-%m-%d")

    if any(kw in date_text for kw in ["ontem", "yesterday"]):
        return (today - timedelta(days=1)).strftime("%Y-%m-%d")

    if any(kw in date_text for kw in ["semana", "week"]):
        if any(kw in date_text for kw in ["1", "uma", "one"]):
            return (today - timedelta(days=7)).strftime("%Y-%m-%d")
        if any(kw in date_text for kw in ["2", "duas", "two"]):
            return (today - timedelta(days=14)).strftime("%Y-%m-%d")

    match = re.search(r"(\d+)", date_text)
    if match and any(kw in date_text for kw in ["dia", "day", "d", "dias", "days"]):
        days = int(match.group(1))
        return (today - timedelta(days=days)).strftime("%Y-%m-%d")

    return today.strftime("%Y-%m-%d")


def scrape_programathor(page):
    jobs = []

    for term in SEARCH_TERMS:
        try:
            url = f"https://programathor.com.br/jobs?search={term.replace(' ', '%20')}"
            page.goto(url, timeout=25000)
            page.wait_for_timeout(2000)

            job_cards = page.query_selector_all('article, .job-item, [class*="job"]')

            for card in job_cards:
                try:
                    title_elem = card.query_selector('a[href*="/jobs/"], h2 a, h3 a')
                    if not title_elem:
                        continue

                    title = title_elem.inner_text().strip()
                    link = title_elem.get_attribute("href")
                    if link and not link.startswith("http"):
                        link = "https://programathor.com.br" + link

                    location_elem = card.query_selector(
                        '.location, .local, [class*="location"], [class*="local"]'
                    )
                    location = location_elem.inner_text().strip() if location_elem else ""

                    if not is_valid_location(location):
                        continue

                    date_elem = card.query_selector('time, .date, [class*="date"], [class*="posted"]')
                    job_date = None
                    if date_elem:
                        date_text = date_elem.inner_text().strip()
                        job_date = parse_relative_date(date_text)

                    if title and is_relevant_junior(title):
                        jobs.append(
                            {
                                "title": title,
                                "company": "",
                                "location": location or "Remoto",
                                "link": link,
                                "source": "ProgramaThor",
                                "posted_date": job_date,
                            }
                        )
                except:
                    continue
        except:
            continue

    return jobs


def scrape_linkedin(page):
    jobs = []

    searches = [
        ("Junior%20Java%20Developer", "1,2"),
        ("Java%20Backend%20Junior", "1,2"),
        ("Spring%20Boot%20Junior", "1,2"),
        ("Software%20Engineer%20Junior%20Java", "1,2"),
    ]

    for search, exp_level in searches:
        try:
            url = f"https://www.linkedin.com/jobs/search/?keywords={search}&location=Sao%20Paulo%2C%20Sao%20Paulo%2C%20Brazil&f_E={exp_level}&f_TPR=r86400"

            page.goto(url, timeout=30000)
            page.wait_for_timeout(3000)

            elements = page.query_selector_all('a[href*="/jobs/view/"]')
            for elem in elements[:15]:
                try:
                    title = elem.inner_text().strip()
                    link = elem.get_attribute("href")

                    parent = elem.evaluate_handle(
                        'el => el.closest("li, div[data-entity-urn], .job-search-card")'
                    )
                    
                    location = ""
                    date_elem = None
                    
                    try:
                        parent_elem = parent.as_element()
                        location_elem = parent_elem.query_selector(
                            '.job-search-card__location, .location, [class*="location"]'
                        )
                        if location_elem:
                            location = location_elem.inner_text().strip()
                        
                        date_elem = parent_elem.query_selector(
                            'time, .job-search-card__listdate, [class*="date"]'
                        )
                    except:
                        pass

                    job_date = None
                    if date_elem:
                        date_text = date_elem.inner_text().strip()
                        job_date = parse_relative_date(date_text)

                    if title and is_relevant_junior(title) and link:
                        jobs.append(
                            {
                                "title": title,
                                "company": "",
                                "location": location,
                                "link": link,
                                "source": "LinkedIn",
                                "posted_date": job_date,
                            }
                        )
                except:
                    continue
        except:
            continue

    return jobs


def scrape_workana(page):
    jobs = []
    searches = ["java%20junior%20remoto", "java%20desenvolvedor", "backend%20java"]

    for search in searches:
        try:
            url = f"https://www.workana.com/jobs?language=pt&query={search}"
            page.goto(url, timeout=25000)
            page.wait_for_timeout(2500)

            elements = page.query_selector_all('.project-item, a[href*="/job/"]')
            for elem in elements[:12]:
                try:
                    title = elem.inner_text().strip()
                    link = elem.get_attribute("href")
                    if link and not link.startswith("http"):
                        link = "https://www.workana.com" + link

                    parent = elem.evaluate_handle('el => el.closest(".project-item, tr, .job-item")')
                    
                    location = ""
                    date_elem = None
                    
                    try:
                        parent_elem = parent.as_element()
                        location_elem = parent_elem.query_selector(
                            '.location, .local, [class*="location"], [class*="country"]'
                        )
                        if location_elem:
                            location = location_elem.inner_text().strip()
                        
                        date_elem = parent_elem.query_selector(
                            '.date, time, [class*="date"], [class*="posted"]'
                        )
                    except:
                        pass

                    if not is_valid_location(location):
                        continue

                    job_date = None
                    if date_elem:
                        date_text = date_elem.inner_text().strip()
                        job_date = parse_relative_date(date_text)

                    if title and is_relevant_junior(title) and len(title) > 5:
                        jobs.append(
                            {
                                "title": title,
                                "company": "",
                                "location": location or "Remoto",
                                "link": link,
                                "source": "Workana",
                                "posted_date": job_date,
                            }
                        )
                except:
                    continue
        except:
            continue

    return jobs


def scrape_geekhunter(page):
    jobs = []
    try:
        url = "https://www.geekhunter.com.br/vagas?search=Java&level=Junior&work=remoto"
        page.goto(url, timeout=25000)
        page.wait_for_timeout(2500)

        elements = page.query_selector_all('a[href*="/vagas/"]')
        for elem in elements[:15]:
            try:
                title = elem.inner_text().strip()
                link = elem.get_attribute("href")
                if link and not link.startswith("http"):
                    link = "https://www.geekhunter.com.br" + link

                parent = elem.evaluate_handle('el => el.closest("tr, .job-item, article")')
                location = ""
                
                try:
                    parent_elem = parent.as_element()
                    location_elem = parent_elem.query_selector(
                        '.location, .local, [class*="location"]'
                    )
                    if location_elem:
                        location = location_elem.inner_text().strip()
                except:
                    pass

                if not is_valid_location(location):
                    continue

                if title and is_relevant_junior(title):
                    jobs.append(
                        {
                            "title": title,
                            "company": "",
                            "location": location or "Remoto",
                            "link": link,
                            "source": "GeekHunter",
                            "posted_date": None,
                        }
                    )
            except:
                continue
    except:
        pass
    return jobs


def is_within_two_weeks(date_str):
    if not date_str:
        return True

    try:
        job_date = datetime.strptime(date_str, "%Y-%m-%d")
        two_weeks_ago = datetime.now() - timedelta(days=14)
        return job_date >= two_weeks_ago
    except:
        return True


def main():
    today = datetime.now()
    two_weeks_ago = today - timedelta(days=14)

    print("=" * 70)
    print("BUSCA VAGAS JUNIOR - JAVA / SPRING BOOT / BACKEND")
    print("=" * 70)
    print(f"\nData atual: {today.strftime('%d/%m/%Y')}")
    print(f"Filtro: Vagas postadas apos {two_weeks_ago.strftime('%d/%m/%Y')}")
    print("\nFiltros aplicados:")
    print("  [OK] Nivel: Junior, Estagiario, Trainee, Pleno")
    print("  [OK] Tech: Java, Spring, Backend, Software Developer")
    print("  [OK] Local: Remoto ou Sao Paulo (Capital)")
    print("  [X]  Excluidos: Senior, Lead, Manager")
    print("  [OK] Periodo: Ultimas 2 semanas")
    print()

    all_jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            locale="pt-BR",
        )
        page = context.new_page()

        print("Buscando em ProgramaThor...")
        jobs = scrape_programathor(page)
        all_jobs.extend(jobs)
        print(f"  {len(jobs)} vagas encontradas")

        print("\nBuscando em LinkedIn...")
        jobs = scrape_linkedin(page)
        all_jobs.extend(jobs)
        print(f"  {len(jobs)} vagas encontradas")

        print("\nBuscando em Workana...")
        jobs = scrape_workana(page)
        all_jobs.extend(jobs)
        print(f"  {len(jobs)} vagas encontradas")

        print("\nBuscando em GeekHunter...")
        jobs = scrape_geekhunter(page)
        all_jobs.extend(jobs)
        print(f"  {len(jobs)} vagas encontradas")

        browser.close()

    seen = set()
    unique_jobs = []
    for job in all_jobs:
        key = job["title"].lower().strip()[:50]
        if key not in seen:
            seen.add(key)
            unique_jobs.append(job)

    recent_jobs = []
    older_jobs = []

    for job in unique_jobs:
        if is_within_two_weeks(job.get("posted_date")):
            recent_jobs.append(job)
        else:
            older_jobs.append(job)

    all_filtered_jobs = recent_jobs + older_jobs[: max(0, 10 - len(recent_jobs))]

    all_filtered_jobs.sort(
        key=lambda x: (
            0 if "junior" in x["title"].lower() or "jr" in x["title"].lower() else 1,
            0 if "java" in x["title"].lower() else 1,
            x.get("posted_date") or "9999-99-99",
        )
    )

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    output_file = os.path.join(OUTPUT_DIR, "vagas_junior_java.json")

    result = {
        "search_metadata": {
            "search_date": today.strftime("%Y-%m-%d %H:%M:%S"),
            "filter_date_from": two_weeks_ago.strftime("%Y-%m-%d"),
            "location_filter": "Remoto ou Sao Paulo (Capital)",
            "total_jobs": len(all_filtered_jobs),
            "recent_jobs": len(recent_jobs),
        },
        "jobs": all_filtered_jobs,
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 70)
    print("RESULTADO:")
    print(f"  - {len(recent_jobs)} vagas nas ultimas 2 semanas")
    print(f"  - {len(all_filtered_jobs)} vagas total")
    print(f"\nSalvo em: {output_file}")
    print("=" * 70)


if __name__ == "__main__":
    main()
