import asyncio
import aiohttp
from more_itertools import chunked
from models import init_db, Person, Session
from models import engine


async def get_person(client, person_id):
    async with client.get(f'https://swapi.dev/api/people/{person_id}/') as response:
        if response.status == 200:
            return await response.json()


async def add_people_to_db(people):
    async with Session() as session:
        for person_data in people:
            if person_data:
                person = Person(
                    name=person_data['name'],
                    birth_year=person_data['birth_year'],
                    eye_color=person_data['eye_color'],
                    films=", ".join(person_data['films']),
                    gender=person_data['gender'],
                    hair_color=person_data['hair_color'],
                    height=person_data['height'],
                    homeworld=person_data['homeworld'],
                    mass=person_data['mass'],
                    skin_color=person_data['skin_color'],
                    species=", ".join(person_data['species']),
                    starships=", ".join(person_data['starships']),
                    vehicles=", ".join(person_data['vehicles'])
                )
                session.add(person)
        await session.commit()


async def main():
    await init_db()
    async with aiohttp.ClientSession() as client:
        for chunk in chunked(range(1, 100), 10):
            tasks = [get_person(client, person_id) for person_id in chunk]
            people = await asyncio.gather(*tasks)
            await add_people_to_db(people)
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
