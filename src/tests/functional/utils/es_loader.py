from elasticsearch.helpers import async_bulk


async def create_index(es_client, index_name: str, index: dict) -> None:
    if not await es_client.indices.exists(index=index_name):
        await es_client.indices.create(index=index_name, body=index)


def generate_data(index_name: str, data: list[dict]) -> list[dict]:
    return [{"_index": index_name, "_id": doc.get('uuid'), **doc} for doc in data]


async def load_data_es(es_client, index_name, index: dict, data: list) -> None:
    await create_index(es_client, index_name, index)
    await async_bulk(es_client, generate_data(index_name=index_name, data=data))


async def delete_index(es_client, index_name) -> None:
    if await es_client.indices.exists(index=index_name):
        await es_client.indices.delete(index=index_name)
