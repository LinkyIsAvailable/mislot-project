import requests
from tavily import TavilyClient


MISTRAL_API_KEY = "your mistral api key here"
TAVILY_API_KEY = "your tavily api key here"


tavily_client = TavilyClient(api_key=TAVILY_API_KEY)



def extract_keywords(prompt):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
    
    data = {
        "model": "mistral-tiny",
        "messages": [ 
            {"role": "system", "content": """Vous êtes un assistant qui parle uniquement français de la mission locale qui travail sur des questions de logement, emploi, formation, santé et mobilité, et uniquement ça, si d'autres demandent sont dites, tu ne pourras répondre uniquement une phrase d'excuse, qui extrait des mots-clés utiles des utilisateurs à partir d'une question que l'utilisateur de pose. Hésite pas à mettre des liens de tes sources pour que les utilisateurs puissent copier coller. Tu te base en France donc les résultats doivent être uniquement en france. , Si la demande de l'utilisateur ne se base pas sur le logement, la formation, l'emploi, la santé OU la mobilité, tu réponds 'Je suis désolé mais je ne peux pas répondre à votre demande.

Générez au maximum 5 des requêtes de recherche qui vous aideront à recueillir les informations suivantes :

<schema>
Schéma d'extraction par défaut
</schema>

Voici les éventuelles notes complémentaires de l'utilisateur :
<user_notes>
Note d'utilisateur
</user_notes>

Votre requête doit
1. Se concentrer sur la recherche d'informations factuelles sur le logement, mobilité, formation, santé et / ou emploi.
2. Donner la priorité à la recherche d'informations correspondant aux exigences du schéma
3. Être suffisamment précis pour éviter les résultats non pertinents

Créez une requête ciblée qui maximisera les chances de trouver des informations pertinentes pour le schéma.

Sortie attendue : une liste de requêtes de recherche générées séparée par une virgule et sans guillemet autour de chaque requête.
<output>
Exemple de requête, Autre exemple de requête, ...
</output>
"""},


            {"role": "user", "content": f"Extrait les mots-clés de cette phrase : {prompt}"}
        ]
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return None

def search_information(keywords):
    try:
        response = tavily_client.search(query=keywords, search_depth="advanced", max_results=5)
        
        if response and "results" in response:
            return response["results"]
        else:
            print("La recherche n'a pas donné de résultats")
            return []
    except Exception as e:
        error_msg = str(e)
        if "400" in error_msg:
            print("Erreur : Veuillez vérifier que votre clé API Tavily est valide et active")
        else:
            print(f"Erreur lors de la recherche : {e}")
        return []

def summarize_results(results):
    if not results:
        return "Aucun résultat trouvé"
    
    summary = ""
    for i, result in enumerate(results, 1):
        title = result.get("title", "Sans titre")
        url = result.get("url", "Pas de lien disponible")
        content = result.get("content", "Pas de description disponible")
        
        summary += f"{i}) {title}\n   {content}\n   Lien : {url}\n\n"
    
    return summary

while True:
    user_query = input("\n- Entrez votre recherche (ou tapez 'annuler' pour quitter) : ")
    
    if user_query.lower() == "annuler":
        print("- Fin du programme.")
        break

    print("\n- Chargement d'une réponse, cela peut prendre jusqu'à 10 secondes...")
    keywords = extract_keywords(user_query)

    if keywords:
        # print(f"- Mots-clés extraits : {keywords}")

        # print("- Recherche d'informations...")
        results = search_information(keywords)

        if results:
            # print("- Génération d'une synthèse...")
            summary = summarize_results(results)
            print("\n- Voici ce que j'ai trouvé pour vous sur internet :\n", summary)
        else:
            print("/!\ Aucun résultat trouvé. Veuillez faire une demande concernant le logement, la formation, l'emploi, la santé et / ou la mobilité.") 
    else:
        print("/!\ Impossible d'extraire des mots-clés.")
