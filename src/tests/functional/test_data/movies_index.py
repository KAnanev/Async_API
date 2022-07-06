INDEX: dict = {
  "settings": {
    "refresh_interval": "1s",
    "analysis": {
      "filter": {
        "english_stop": {
          "type": "stop",
          "stopwords": "_english_"
        },
        "english_stemmer": {
          "type": "stemmer",
          "language": "english"
        },
        "english_possessive_stemmer": {
          "type": "stemmer",
          "language": "possessive_english"
        },
        "russian_stop": {
          "type": "stop",
          "stopwords": "_russian_"
        },
        "russian_stemmer": {
          "type": "stemmer",
          "language": "russian"
        }
      },
      "analyzer": {
        "ru_en": {
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "english_stop",
            "english_stemmer",
            "english_possessive_stemmer",
            "russian_stop",
            "russian_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "dynamic": "strict",
    "properties": {
      "uuid": {
        "type": "keyword"
      },
      "title": {
        "type": "text",
        "analyzer": "ru_en",
        "fields": {
          "raw": {
            "type": "keyword"
          }
        }
      },
      "imdb_rating": {
        "type": "float"
      },
      "description": {
        "type": "text",
        "analyzer": "ru_en"
      },
      "genre": {
        "type": "nested",
        "dynamic": "strict",
        "properties": {
          "uuid": {
            "type": "keyword"
          },
          "name": {
            "type": "keyword"
          }
        }
      },
      "actors": {
        "type": "nested",
        "dynamic": "strict",
        "properties": {
          "uuid": {
            "type": "keyword"
          },
          "full_name": {
            "type": "text",
            "analyzer": "ru_en"
          }
        }
      },
      "writers": {
        "type": "nested",
        "dynamic": "strict",
        "properties": {
          "uuid": {
            "type": "keyword"
          },
          "full_name": {
            "type": "text",
            "analyzer": "ru_en"
          }
        }
      },
      "directors": {
        "type": "nested",
        "dynamic": "strict",
        "properties": {
          "uuid": {
            "type": "keyword"
          },
          "full_name": {
            "type": "text",
            "analyzer": "ru_en"
          }
        }
      }
    }
  }
}
