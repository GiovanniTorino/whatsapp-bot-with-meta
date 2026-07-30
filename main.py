import os
import requests

def obter_noticias_com_openrouter():
    OPENROUTER_KEY = os.environ["OPENROUTER_KEY"]

    prompt = (
        "Traga um resumo das 3 principais notícias do futebol mundial desta última semana. "
        "Formate o texto de maneira limpa para o WhatsApp: use marcadores, negritos (*exemplo*) "
        "e inclua o título e uma breve explicação de 2 linhas para cada notícia."
        "Apenas forneça o resumo formatado. Não inclua números de citação entre colchetes, notas de rodapé nem mensagens no final oferecendo ajuda."
    )

    print("🤖 Consultando a OpenRouter e buscando notícias...")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://localhost",
        "X-Title": "WhatsApp News Bot"
    }

    data = {
        "model": "perplexity/sonar",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data
    )

    if response.status_code == 200:
        resultado = response.json()
        return resultado["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Erro na API da OpenRouter: {response.status_code} - {response.text}")


def enviar_whatsapp_cloud_api(numero_destino, corpo_variavel):
    """
    Envia mensagem via WhatsApp Cloud API oficial, usando o template
    pré-aprovado 'resumo_noticias' com uma variável {{1}}.
    """
    WHATSAPP_TOKEN = os.environ["WHATSAPP_TOKEN"]
    PHONE_NUMBER_ID = os.environ["PHONE_NUMBER_ID"]

    url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": numero_destino,
        "type": "template",
        "template": {
            "name": "resumo_noticias",
            "language": {"code": "pt_BR"},
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": corpo_variavel}
                    ]
                }
            ]
        }
    }

    print("🚀 Enviando mensagem via WhatsApp Cloud API...")
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("✅ Mensagem enviada com sucesso!")
    else:
        raise Exception(f"Erro ao enviar WhatsApp: {response.status_code} - {response.text}")


def tarefa_semanal():
    print("\n⏰ Iniciando processo...")
    NUMERO = os.environ.get("NUMERO_DESTINO", "5545998282477")

    try:
        noticias = obter_noticias_com_openrouter()

        print("\n--- Mensagem gerada: ---\n")
        print(noticias)
        print("\n-------------------------\n")

        enviar_whatsapp_cloud_api(NUMERO, noticias)
    except Exception as e:
        print(f"❌ Ocorreu um erro durante a execução: {e}")
        raise


if __name__ == "__main__":
    tarefa_semanal()