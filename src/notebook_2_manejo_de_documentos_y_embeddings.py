# -*- coding: utf-8 -*-
"""notebook_2_manejo_de_documentos_y_embeddings.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wCaBnujwWiki68pgwwL8aADDKKwFEi-7

# Indexes o índices

Los índices se refieren a las formas de estructurar documentos para que los Modelos de Lenguaje de Masivos (LLMs) puedan interactuar con ellos de la mejor manera posible. Esta es una tarea esencial para optimizar la eficiencia y velocidad de las operaciones de búsqueda y recuperación de información en sistemas de procesamiento de lenguaje natural.

Puedes pensar en los índices como en el índice de un libro. En un libro el índice te ayuda a localizar rápidamente un capítulo o sección específica sin tener que hojear todas las páginas. De manera similar, los índices en LangChain permiten a los LLMs encontrar rápidamente documentos o información relevantes sin tener que procesar todos los documentos disponibles.

## Índices y recuperación

El uso más común de los índices en las cadenas de procesamiento de datos es en un paso denominado **"recuperación"**. Este paso se refiere a tomar la consulta de un usuario y devolver los documentos más relevantes. Sin embargo, es importante hacer una distinción aquí porque:

1. Un índice puede utilizarse para otras cosas además de la recuperación.
2. La recuperación puede utilizar otras lógicas además de un índice para encontrar documentos relevantes.

La mayoría de las veces, cuando hablamos de índices y recuperación, nos referimos a la indexación y recuperación de datos no estructurados, como documentos de texto. En este contexto, "no estructurado" significa que los datos no siguen un formato fijo o predecible, como lo hace, por ejemplo, una tabla de base de datos. En cambio, los documentos de texto pueden variar ampliamente en términos de longitud, estilo, contenido, etc.

## Retriever en LangChain

El **Retriever** es un componente fundamental en el ecosistema de LangChain. Su responsabilidad principal es localizar y devolver documentos relevantes según una consulta específica. Imagínate un bibliotecario diligente que sabe exactamente dónde encontrar el libro que necesitas en una gran biblioteca; eso es lo que hace el Retriever en LangChain.

Para realizar esta tarea, el Retriever debe implementar el método `get_relevant_documents`. Aunque este método puede ser implementado de la forma que el usuario considere más conveniente, en LangChain se ha diseñado una estrategia para recuperar documentos lo más eficientemente posible. Esta estrategia se basa en el concepto de **Vectorstore**, por lo que vamos a centrarnos en el Retriever tipo Vectorstore en el resto de esta guía.

### Vectorstore y Vectorstore Retriever

Para entender qué es un **Retriever** tipo **Vectorstore**, primero debemos entender qué es un Vectorstore. Un Vectorstore es un tipo de base de datos especialmente diseñada para gestionar y manipular vectores de alta dimensionalidad, comúnmente utilizados para representar datos en aprendizaje automático y otras aplicaciones de inteligencia artificial.

En la analogía de la biblioteca mencionada anteriormente, si el Retriever es el bibliotecario, entonces el Vectorstore sería el sistema de clasificación y organización de la biblioteca que permite al bibliotecario encontrar exactamente lo que busca.

En LangChain, el sistema Vectorstore predeterminado que se utiliza es Chroma. Chroma se utiliza para indexar y buscar embeddings (vectores que representan documentos en el espacio multidimensional). Estos embeddings son una forma de condensar y representar la información de un documento para que pueda ser fácilmente comparable con otros documentos.

El Retriever tipo Vectorstore, por lo tanto, es un tipo de Retriever que utiliza una base de datos Vectorstore (como Chroma) para localizar documentos relevantes para una consulta específica. Primero transforma la consulta en un vector (a través de un proceso de incrustación (embedding)), luego busca en la base de datos Vectorstore los documentos cuyos vectores son más cercanos (en términos de distancia coseno u otras métricas de similitud) a la consulta vectorizada.
"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip install langchain

!pip show langchain

"""## 1. La clase Document

Esta clase es la base de cuando carguemos nuestros documentos. En LangChain se les llama schemas a estas clases base y se encuentran en langchain.schema. Así es el schema para Document:

```
class Document(Serializable):
    '''Interface for interacting with a document.'''

    page_content: str
    metadata: dict = Field(default_factory=dict)
```




"""

from langchain.schema import Document

page_content = "Textooooooooolargoooooo ejemplo"
metadata = {'fuente': 'platzi', 'clase': 'langchain'}

doc = Document(
    page_content=page_content, metadata=metadata
)

doc.page_content

"""## 2. Document loaders

La primera etapa en la indexación de documentos en LangChain implica cargar los datos en "Documentos". Este es el nombre de la clase con la que trabajaremos, ubicada en el directorio de esquemas en el repositorio de LangChain. Simplificando, un "Documento" es básicamente un fragmento de texto. El propósito del cargador de documentos es simplificar este proceso de carga.

### Document transformers

Los transformadores de carga son utilidades que convierten los datos desde un formato específico al formato "Documento". Por ejemplo, existen transformadores para los formatos CSV y SQL. En su mayoría, estos cargadores obtienen datos de archivos, pero a veces también de URLs.

Existen varios cargadores de documentos dependiendo de la fuente de nuestros datos. A continuación, se muestran algunos ejemplos (para más información, consulta la documentación):

- Airtable
- OpenAIWhisperParser
- CoNLL-U
- Copy Paste
- CSV
- Email
- EPub
- EverNote
- Microsoft Excel
- Facebook Chat
- File Directory
- HTML
- Images
- Jupyter Notebook
- JSON
- Markdown
- Microsoft PowerPoint
- Microsoft Word
- Open Document Format (ODT)
- Pandas DataFrame
- PDF

Al mismo tiempo, también puedes utilizar servicios como los datasets de Hugging Face, o incluso obtener datos de servicios como Slack, Snowflake, Spreedly, Stripe, 2Markdown, entre otros.

Cada mes se añaden nuevas fuentes y tipos de conjuntos de datos que podemos utilizar. Te recomendamos revisar la documentación con regularidad para mantenerte actualizado.

Comencemos con ejemplos, usemos un paper descargado de internet y de alta relevancia para nuestras vidas.
"""

import requests

url = 'https://www.cs.virginia.edu/~evans/greatworks/diffie.pdf'
response = requests.get(url)

with open('public_key_cryptography.pdf', 'wb') as f:
    f.write(response.content)

"""Quizás el Document Loader más relevante es el unstructured pues se encuentra como la base de otros Document Loaders. Sirve por ejemplo para documentos de texto como .txt o .pdf."""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip install unstructured[pdf]==0.7.12
#

from langchain.document_loaders import UnstructuredFileLoader

loader = UnstructuredFileLoader("./public_key_cryptography.pdf")
data = loader.load()

data[0].page_content[:300]

type(data)

len(data)

data[0].metadata

data[0].page_content

"""Existen alternativas que mantienen las páginas del documento PDF en caso de ser necesario esto. Probablemente el más usado es usando PyPDFLoader."""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip install pypdf

from langchain.document_loaders import PyPDFLoader

loader = PyPDFLoader("./public_key_cryptography.pdf")
dataPdf = loader.load()

dataPdf[17].metadata





"""Otro uso frecuente es leer datos de CSVs o Spreadsheets (como Excel), muchas empresas tienen sus datos en este formato. Primero, debemos tener el archivo en formato de un DataFrame de Pandas.

### CSV a Pandas DataFrame
"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip install pandas

import pandas as pd

df = pd.read_csv('repos_cairo.csv')
df.head()

from langchain.document_loaders import DataFrameLoader

loader = DataFrameLoader(df, page_content_column="repo_name")
data = loader.load()

print(f"El archivo es de tipo {type(data)} y tiene una longitud de {len(data)} debido a la cantidad de observaciones en el CSV.")

from pprint import pprint

pprint(data[:5])

"""### JSONL

Veamos un caso más complejo. No tenemos una implementación directa de LangChain para importar **JSONLs** sin embargo es muy común tener que importar estos formatos.

El siguiente ejemplo muestra cómo importar un JSONL personalizado para nuestra base de datos de Transformers, pero aplica para otros formatos de datos que no necesariamente se encuentran entre los disponibles por LangChain. Nosotros creamos nuestros Document según lo que queramos asignar como page_content y metadata.
"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip install jsonlines

from langchain.schema import Document
import jsonlines
from typing import List

class TransformerDocsJSONLLoader:
  def __init__(self, file_path: str):
    self.file_path = file_path

  def load(self):
    with jsonlines.open(self.file_path) as reader:
      documents = []
      for obj in reader:
        page_content = obj.get("text", "")
        metadata = {
            'title': obj.get("title", ""),
            'repo_owner' : obj.get("repo_owner", ""),
            'repo_name' : obj.get("repo_name", ""),
        }
        documents.append(
            Document(page_content=page_content, metadata=metadata)
        )
    return documents

loader = TransformerDocsJSONLLoader("transformers_docs.jsonl")
data = loader.load()

for doc in data:
  print(doc)

"""## Text Splitters

Imagina que estás trabajando con un libro muy grueso y necesitas pasarlo por una ventana muy estrecha. ¿Qué harías? Probablemente, lo cortarías en secciones más manejables y las pasarías una por una. Ahora, cambia el libro por un documento largo y la ventana por el modelo de procesamiento de lenguaje natural que estás utilizando. Este escenario es exactamente por qué necesitamos los separadores de texto en el campo de la inteligencia artificial.

LangChain, comprendiendo este desafío, tiene incorporados varios separadores de texto para facilitar la división, combinación, filtrado y manipulación de los documentos. De este modo, puedes transformarlos para que se adapten mejor a tu aplicación.

Cuando nos enfrentamos a textos largos, es imprescindible dividirlos en fragmentos. Aunque esto suena sencillo, no es tan simple como parece. Queremos mantener las partes del texto que están semánticamente relacionadas juntas. Y esto de "semánticamente relacionado" puede variar dependiendo del tipo de texto con el que estés trabajando.

Piensa en el texto como un rompecabezas, cada pieza (o fragmento) tiene su propio significado, pero también contribuye a la imagen general (o el contexto). Queremos separar el rompecabezas en piezas, pero sin perder el sentido de la imagen completa.

Entonces, ¿cómo funcionan exactamente los separadores de texto?

1. Primero, dividen el texto en fragmentos pequeños y semánticamente significativos (a menudo oraciones).
2. Luego, comienzan a combinar estos fragmentos pequeños en un fragmento más grande hasta que alcanzan un tamaño determinado (medido por alguna función).
3. Una vez que alcanzan ese tamaño, hacen de ese fragmento su propio texto y luego comienzan a crear un nuevo fragmento de texto con cierta superposición. Esto es para mantener el contexto entre fragmentos.

En este proceso, puedes personalizar tu separador de texto en dos aspectos: cómo se divide el texto y cómo se mide el tamaño del fragmento.

## RecursiveCharacterTextSplitter

Para facilitar las cosas, LangChain ofrece un separador de texto por defecto: el `RecursiveCharacterTextSplitter`. Este separador de texto toma una lista de caracteres y trata de crear fragmentos basándose en la división del primer carácter. Pero, si algún fragmento resulta demasiado grande, pasa al siguiente carácter, y así sucesivamente. Los caracteres que intenta dividir son ["\n\n", "\n", " ", ""]

El `RecursiveCharacterTextSplitter` ofrece una ventaja importante: intenta preservar tanto contexto semántico como sea posible manteniendo intactos los párrafos, las oraciones y las palabras. Estas unidades de texto suelen tener fuertes relaciones semánticas, lo que significa que las palabras dentro de ellas a menudo están estrechamente relacionadas en significado. Esta es una característica sumamente beneficiosa para muchas tareas de procesamiento del lenguaje natural.

Piensa en una conversación cotidiana, es más fácil entender una idea cuando escuchas la oración completa en lugar de palabras o frases sueltas. Esta misma lógica se aplica a los modelos de procesamiento de lenguaje natural. Al mantener intactos los párrafos, oraciones y palabras, se preserva el 'flujo de conversación' en el texto, lo que puede mejorar la eficacia del modelo al interpretar y comprender el texto.

A partir de nuestros `Document` podemos crear más `Document` con `RecursiveCharacterTextSplitter`, es decir, podemos partirlos manteniendo nuestra metadata.
"""

from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    length_function=len,
    chunk_overlap=200
)

documents = text_splitter.split_documents(dataPdf)

len(documents)

documents[20]

"""### Tamaño del fragmento y superposición

Imagina que estás trabajando con un rompecabezas de palabras, donde cada pieza es una porción de texto. Para que este rompecabezas sea manejable, necesitas asegurarte de que las piezas son del tamaño correcto y se superponen adecuadamente. En el mundo del procesamiento de texto, estas "piezas" son los fragmentos de texto, y su tamaño y superposición pueden ser esenciales para el rendimiento de tus modelos de aprendizaje automático.

En primer lugar, hablemos del tamaño del fragmento. La pregunta que podrías hacerte es, ¿cuán grande debe ser cada fragmento de texto? Bien, la respuesta depende del modelo de embedding de texto que estés utilizando. Un "modelo de embedding" puede parecer un término intimidante, pero es simplemente una herramienta que convertimos palabras, oraciones o documentos completos en vectores numéricos que las máquinas pueden entender.

Por ejemplo, el modelo de incrustación `text-embedding-ada-002` de OpenAI es excelente para muchas aplicaciones, pero puede manejar hasta 8191 tokens. Ahora, podrías preguntarte, ¿qué es un 'token'? Un token no es lo mismo que un carácter. Un token puede ser una palabra o incluso un signo de puntuación. Por lo tanto, un token podría tener desde un solo carácter hasta una decena de ellos. De esta manera, tu fragmento de texto podría tener miles de caracteres, pero debes asegurarte de que no contenga más de 8191 tokens.

Mantener los fragmentos entre 500 y 1000 caracteres suele ser un buen equilibrio. Este tamaño asegura que el contenido semántico es preservado sin sobrepasar el límite de tokens del modelo.

En cuanto a la superposición, este parámetro decide cuánto texto queremos repetir entre fragmentos. ¿Por qué querríamos hacer esto? Bueno, la superposición ayuda a mantener el contexto entre fragmentos contiguos. Es como tener una pequeña ventana de memoria que se traslada de un fragmento a otro. Generalmente, se recomienda ajustar la superposición al 10-20% del tamaño del fragmento. Esto asegura cierta conexión entre los fragmentos sin causar demasiada repetición. Si la superposición es demasiado grande, puede ralentizar el proceso y aumentar los costos de procesamiento.

Por lo tanto, si estás lidiando con textos relativamente largos, esta es la configuración que podrías utilizar.
"""

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap  = 50,
    length_function = len,
)

# o

# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size = 1000,
#     chunk_overlap  = 100,
#     length_function = len,
# )

documents = text_splitter.split_documents(dataPdf)

documents[0].page_content

"""## Modelos de embeddings
Los modelos de incrustaciones de texto son fundamentales en el procesamiento de lenguaje natural (NLP). Transforman palabras, frases y documentos en representaciones vectoriales que capturan su significado y las relaciones semánticas entre ellas. Esto posibilita que los algoritmos de aprendizaje automático procesen texto y realicen operaciones como la búsqueda semántica, que se basa en la similitud de los textos en el espacio vectorial.

### Comprendiendo el espacio de alta dimensión

En un espacio de alta dimensión, cada dimensión representa una característica única de los datos. Al igual que utilizamos longitud, anchura y altura para localizar una posición en un espacio tridimensional, en un espacio de alta dimensión usamos múltiples dimensiones para ubicar y describir un punto de datos.

Las incrustaciones de vectores, por tanto, son como 'direcciones' numéricas para puntos de datos en este espacio. Así, un espacio vectorial en el que mapeamos palabras relacionadas con emociones, podría tener dimensiones para capturar cuán 'feliz' es una palabra, la intensidad de la emoción, si es una emoción positiva o negativa, etc. Cuantas más dimensiones usemos, más características podremos encapsular de cada palabra.

### Los embeddings: herramientas esenciales para la comprensión del lenguaje

La clase `Embeddings` de LangChain proporciona una interfaz para trabajar con modelos de incrustaciones de texto. Esta clase no está vinculada a un proveedor específico de modelos de incrustaciones, sino que ofrece una interfaz estándar para interactuar con varios proveedores como OpenAI, Cohere y Hugging Face.

Las incrustaciones de texto son como un traductor que transforma las palabras, frases y documentos en representaciones numéricas de tamaño fijo que capturan su significado y estructura.

Por ejemplo, una oración como "Esto es cómo funcionan las incrustaciones" se procesa de la siguiente manera:

1. Se tokeniza la oración en palabras individuales: ["Esto", "es", "cómo", "funcionan", "las", "incrustaciones"].
2. Un modelo de incrustaciones pre-entrenado convierte cada palabra en su vector de incrustaciones correspondiente, representado como una matriz de números de longitud fija.

De esta manera, la oración se convierte en una secuencia de vectores numéricos, y sobre estos vectores podemos realizar operaciones poderosas como búsquedas semánticas, recuperando los resultados más relevantes basados en la similitud entre las incrustaciones.

### **La clase embeddings en LangChain**

En LangChain la clase base **`Embeddings`** proporciona dos métodos:

- uno para incrustar documentos.
- otro para incrustar consultas.

El primer método acepta múltiples textos, mientras que el segundo solo uno. Esto se debe a que algunos proveedores de incrustaciones tienen diferentes métodos para los documentos y las consultas.

### **Integración con proveedores de modelos de incrustaciones**

LangChain integra una variedad de proveedores de modelos de incrustaciones de texto, incluyendo:

- Aleph Alpha
- AzureOpenAI
- Cohere
- Fake Embeddings
- Hugging Face Hub
- InstructEmbeddings
- Jina
- Llama-cpp
- OpenAI
- SageMaker Endpoint Embeddings
- Self Hosted Embeddings
- Sentence Transformers Embeddings
- TensorFlow Hub

Estos proveedores ofrecen una gran variedad de opciones, permitiéndote elegir el modelo de incrustaciones que mejor se adapte a tus necesidades. En futuras secciones, profundizaremos en cómo usar estos proveedores de modelos de incrustaciones para mejorar el procesamiento de texto en LangChain.

### OpenAI embeddings
"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip install openai

from getpass import getpass
import os

OPENAI_API_KEY = getpass('Enter the secret value: ')
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

from langchain.embeddings import OpenAIEmbeddings

# Las capacidades multilingues de "text-embedding-ada-002" no son claras
embedding_openai = OpenAIEmbeddings(model="text-embedding-ada-002")

embedding_openai

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip install tiktoken

documentos_a_incrustar = [
    "¡Hola parce!",
    "¡Uy, hola!",
    "¿Cómo te llamas?",
    "Mis parceros me dicen Omar",
    "¡Hola Mundo!"
  ]

incrustaciones = embedding_openai.embed_documents(documentos_a_incrustar)

len(incrustaciones[3])

consulta_incrustada = embedding_openai.embed_query(documentos_a_incrustar[0])

consulta_incrustada

"""### Hugging Face embeddings"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip install sentence_transformers

from langchain.embeddings import SentenceTransformerEmbeddings

embeddings_st = SentenceTransformerEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

# Otro modelo en español que podríamos usar es "symanto/sn-xlm-roberta-base-snli-mnli-anli-xnli"

incrustaciones = embeddings_st.embed_documents(documentos_a_incrustar)
len(incrustaciones)

len(incrustaciones[0])

incrustacion = embeddings_st.embed_query(documentos_a_incrustar[0])

len(incrustacion)

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip install InstructorEmbedding sentence_transformers

from langchain.embeddings import HuggingFaceInstructEmbeddings

# A junio de 2023 no hay modelos Instruct para español
embedding_instruct = HuggingFaceInstructEmbeddings(
    model_name="hkunlp/instructor-large",
    model_kwargs={"device":"cuda"}
)

# El device podría ser cpu

incrustaciones = embedding_instruct.embed_documents(documentos_a_incrustar)

len(incrustaciones[4])

incrustacion = embedding_instruct.embed_query(documentos_a_incrustar[0])

len(incrustacion)

"""### La importancia del tamaño de los embeddings

Los modelos de incrustaciones de texto (embeddings) son un recurso crucial en el procesamiento del lenguaje natural. Sin embargo, es importante tener en cuenta que estos modelos tienen una capacidad limitada en términos de la cantidad de tokens que pueden manejar antes de truncar los textos.

Cada proveedor de modelos de incrustaciones puede tener un límite de tokens diferente y estos límites pueden variar con el tiempo. Es recomendable que consultes la documentación actualizada del proveedor para obtener información precisa. Esta guía se creó a medidados de 2023 y, por lo tanto, los límites específicos pueden haber cambiado.

Para los modelos de OpenAI, por ejemplo, las actualizaciones a menudo se anuncian en blogs o en su página de modelos. Para los modelos del Hub de Hugging Face, puedes usar el método `.client` para conocer el límite de tokens. Para los modelos de Cohere, aunque no está especificado claramente, se recomienda mantener los textos menores a 512 tokens.

#### Recomendaciones generales de tamaño de incrustaciones

Para todos los modelos de incrustaciones que manejamos, una regla general sería mantener los textos menores a 512 tokens. Esta restricción de tamaño ayuda a garantizar que los modelos puedan procesar eficientemente el texto sin truncarlo.

Existe una gran posibilidad de que los modelos de incrustaciones futuras puedan manejar contextos más grandes (es decir, más tokens) sin perder capacidad de procesamiento. Sin embargo, al menos hasta junio de 2023 y probablemente durante todo el año 2023, la recomendación seguirá siendo mantener los textos dentro del límite de 512 tokens.

Aunque los modelos de incrustaciones de OpenAI pueden mencionar la capacidad de manejar hasta 8192 tokens, es importante recordar que el rendimiento óptimo del modelo puede no alcanzarse con textos de este tamaño. Por lo tanto, se recomienda la cautela y el cumplimiento de la recomendación general de 512 tokens.

"""

embedding_instruct.client, embeddings_st.client

"""## Bases de datos vectoriales

Imagina que eres un bibliotecario, pero tu biblioteca consta de vectores de alta dimensión en lugar de libros, y tus usuarios son agentes de IA en lugar de humanos. Por futurista que parezca, esta es la realidad de una base de datos de vectores: un banco de memoria para la IA, diseñado para almacenar y recuperar datos vectoriales de alta dimensión con eficiencia y precisión. Al igual que un bibliotecario organizaría y buscaría libros, una base de datos de vectores proporciona un método para gestionar y encontrar vectores en un espacio de alta dimensión.

En este capítulo, profundizaremos en las complejidades de las bases de datos de vectores. Desentrañaremos su creciente importancia, entenderemos qué implica la data vectorial y exploraremos los aspectos prácticos de las bases de datos de vectores.

## El ascenso y la significancia de las bases de datos vectoriales

Las bases de datos de vectores están ganando prominencia en la industria tecnológica, evidenciado por las significativas inversiones en tecnologías de bases de datos de vectores en los últimos años. Algunos ejemplos incluyen la inversión de $28M de Pinecone, la ronda semilla de $10M de LangChain y la ronda semilla de $18M de Chroma. El flujo de dinero habla mucho sobre el futuro y el potencial de las bases de datos de vectores en la IA.

La evolución de las tecnologías de gestión de datos puede asemejarse a un río: siempre fluyendo, adaptándose continuamente al paisaje. Desde esquemas rígidos y estructurados en bases de datos relacionales hasta el manejo flexible de datos no estructurados o semi-estructurados en bases de datos NoSQL, la gestión de datos es un dominio en flujo, evolucionando para satisfacer nuestras crecientes necesidades de datos.

La aparición de las bases de datos de vectores es el último desarrollo en este viaje. Estas bases de datos abordan los desafíos de gestionar y consultar datos vectoriales de alta dimensión, también conocidos como "incrustaciones de vectores".

### El rol de las bases de datos vectoriales

Las bases de datos de vectores, también conocidas como bases de datos de búsqueda de similitud o bases de datos de búsqueda del vecino más cercano, están especialmente diseñadas para almacenar y recuperar incrustaciones de vectores. Estas bases de datos pueden realizar operaciones como encontrar elementos similares a un vector dado o buscar elementos que cumplan con ciertos criterios de similitud. Imagina poder preguntarle a tu base de datos, "encuéntrame más palabras como 'alegre'" y obtener respuestas como 'contento', 'feliz' y 'jubiloso'. Las bases de datos tradicionales no están diseñadas para este tipo de consultas, donde las bases de datos de vectores destacan.

Con los conceptos básicos cubiertos, ahora estamos preparados para adentrarnos más en el mundo de la gestión de datos vectoriales. En las siguientes secciones, exploraremos cómo integrar las bases de datos de vectores usando Python y compararemos algunas de las plataformas líderes como Pinecone, Chroma y LangChain.

Las bases de datos tienen una rica historia, evolucionando desde simples registros hasta estructuras complejas capaces de capturar, consultar y analizar información a lo largo del tiempo. Nos encontramos en un momento crucial, ya que el auge de la IA generativa se entrelaza con nuestras herramientas de gestión de datos, creando nuevos potenciales y desafíos.

Los vectores representan 'objetos' de datos, llevando información sobre el tiempo, el lugar, los atributos y más, permitiéndonos enriquecer nuestros datos. Ayudan a rastrear tendencias temporales, permitiéndonos

### Chroma

Chroma es un proyecto de código abierto que provee una base de datos específicamente diseñada para guardar y consultar incrustaciones, en conjunción con sus respectivos metadatos. Fue diseñada para trabajar con Modelos Grandes de Lenguaje (LLM).
"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip install chromadb

"""Embed and store the texts. Supplying a persist_directory will store the embeddings on disk"""

from langchain.vectorstores import Chroma

NOMBRE_INDICE_CHROMA = "instruct-embeddings-public-crypto"

vectorstore_chroma = Chroma.from_documents(
    documents=documents,
    embedding=embedding_instruct,
    persist_directory=NOMBRE_INDICE_CHROMA
)

type(embedding_instruct)

"""Hacer que nuestra vectorstore persista en nuestro disco."""

vectorstore_chroma.persist()

vectorstore_chroma = Chroma(
    persist_directory=NOMBRE_INDICE_CHROMA,
    embedding_function=embedding_instruct
)

"""Podemos cargar la base de datos persistente desde el disco y usarla en cualquier momento."""

query = "What is public key cryptography?"

docs = vectorstore_chroma.similarity_search_with_score(query, k=5)

len(docs)

docs[3]

"""#### Creando un Retriever

Un retriever es una herramienta esencial para realizar búsquedas dentro de nuestros 'vectorstores'. En términos sencillos, un retriever es algo así como un "buscador" o "recuperador".

El retriever permite definir el número de documentos relevantes que queremos obtener como resultado de nuestras búsquedas. Esto se puede ajustar mediante el argumento `search_kwargs` en el método `.as_retriever()`.

Es posible especificar la estrategia que se usará para encontrar los documentos relevantes usando `search_type`. Este parámetro puede tomar dos valores: "similarity" y "exact_match".

**Similaridad ("similarity")**: Busca documentos que sean similares a la consulta. Los documentos se clasifican según su puntuación de similitud, donde una puntuación más baja indica una mejor coincidencia.

**Coincidencia Exacta ("exact_match")**: Busca documentos que coincidan exactamente con la consulta. No considera la similitud entre la consulta y los documentos.
"""

retriever_chroma = vectorstore_chroma.as_retriever(
    search_kwargs={'k': 2}
)

retriever_chroma.get_relevant_documents("What are the recent advances on public key cryptography?")

"""#### Creando una cadena para preguntar"""

from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    model_name='gpt-3.5-turbo',
    temperature=0.0
)

from langchain.chains import RetrievalQAWithSourcesChain

qa_chain_with_sources = RetrievalQAWithSourcesChain.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever_chroma
)

query = "What is the relevance of public key crypto?"
respuesta = qa_chain_with_sources(query)
respuesta

query = "What is crypto?"
respuesta = qa_chain_with_sources(query)
respuesta

"""Todos estos son resultados buenos y relevantes. Pero, ¿qué podemos hacer con ellos? Existen diversas tareas que podemos realizar, pero una de las más interesantes (y muy bien soportada por LangChain) es la "Generación de Preguntas y Respuestas" o GQA.

En la Generación de Preguntas y Respuestas (GQA), un modelo de lenguaje se utiliza para generar respuestas a preguntas basadas en un texto dado. Esto puede ser particularmente útil en una variedad de aplicaciones, desde chatbots inteligentes que pueden responder a preguntas basadas en manuales de usuario o documentación de productos, hasta motores de búsqueda más avanzados que pueden responder a preguntas en lugar de simplemente proporcionar una lista de documentos relevantes.

Los modelos de GQA trabajan generando representaciones vectoriales de los documentos y las consultas, y luego usan medidas de similitud (como las mencionadas anteriormente) para identificar los documentos o partes de documentos que son más relevantes para la consulta. Esto va más allá de la simple búsqueda de palabras clave, ya que los modelos pueden capturar la semántica y el contexto de las consultas y documentos, lo que les permite responder preguntas más complejas y proporcionar respuestas más precisas y detalladas.

En GQA, tomamos la consulta como una pregunta que debe ser respondida por un LLM, pero el LLM debe responder la pregunta basándose en la información que se le devuelve desde el almacén de vectores.

Para hacer esto, inicializamos un objeto RetrievalQA, pero antes creamos un objeto de tipo llm y en este caso usaremos el modelo `gpt-3.5-turbo` de OpenAI.
"""

from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    model_name='gpt-3.5-turbo',
    temperature=0.0
)