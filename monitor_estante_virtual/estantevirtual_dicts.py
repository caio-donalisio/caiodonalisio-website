from .models import Query

def transform_query(query: dict, page) -> dict:
    query = add_price_key(query)
    query = add_search_field(query)
    query = get_api_terms(query)
    query = add_extra_params(query, page)
    return query

def add_search_field(query: dict) -> dict:
    translations = {
        'titulo':'titulo',
        'titulo_ou_autor':'titulo-autor',
        'autor':'autor',
        'isbn':'isbn', 
        'editora':'editora',
        }
    for key in query:
        if key in translations:
            query = {**query, 'searchField':translations[key]}
            break
    return query

def add_price_key(query: dict) -> dict:
    if any(key in query for key in ['preco_min', 'preco_max'] if key): 
        query['_preco'] = f"{(query.get('preco_min') or 1) * 100}-{(query.get('preco_max') or 99_999) * 100}"
        query.pop('preco_max', None), query.pop('preco_min', None)
    return query

def get_api_terms(query: dict) -> dict:
    termos = {
        'editora': 'q',
        'titulo_ou_autor': 'q',
        'titulo':'q',
        'autor':'q',
        'isbn':'q',
        'filtro': 'qt',
        'cidade': 'cidade',
        'vendedor': 'vendedor',
        'idioma': 'idioma',
        'ano_de_publicacao': 'ano-de-publicacao',
        'assunto': 'estante'
    }   
    return  {termos.get(termo, termo): query[termo] for termo in query if query[termo]}

def add_extra_params(query: dict, page=1) -> dict:
    return {
        **query,
        "page": page,
        "sort": "new-releases",
        "nsCat": "Natural"
    }

def get_request_params(query: Query, page=1) -> dict:
    query = query.__dict__
    query.pop('_state', None)
    query.pop('id', None)
    query.pop('user_id', None)
    query.pop('created_at', None)
    query.pop('updated_at', None)
    return transform_query(query, page)
