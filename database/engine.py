from sqlalchemy import create_engine, text, TextClause
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv
import os

load_dotenv()

USER = os.getenv('PROJECT')
PASS = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
DB   = os.getenv('DB')

URL = f'postgresql+psycopg2://{USER}:{PASS}@{HOST}:{PORT}/{DB}?sslmode=require'

engine = create_engine(URL)


from sources.web.request import Request

request = Request()

def add_or_update_institutions():
    upsert_institutions = text('''
        INSERT INTO institutions (id, code, category, year)
        VALUES (:id, :code, :category, :year)
        ON CONFLICT (id) DO UPDATE SET
            code                       = EXCLUDED.code,
            category                   = EXCLUDED.category,
            year                       = EXCLUDED.year
    ''')

    upsert_names = text("""
        INSERT INTO institution_names (institution, name, year)
        VALUES (:institution, :name, :year)
        ON CONFLICT (institution, year) DO UPDATE SET
            name            = EXCLUDED.name
    """)

    upsert_termtypes = text("""
        INSERT INTO institution_termtypes (institution, type, year)
        VALUES (:institution, :type, :year)
        ON CONFLICT (institution, year) DO UPDATE SET
            type            = EXCLUDED.type
    """)

    institutions = request.institutions()

    with engine.begin() as connection:
        connection.execute(upsert_institutions, [ 
            {
                'id':                           i.id,
                'code':                         i.code.strip(),
                'category':                     i.category,
                'year':                         i.beginId
            }
            for i in institutions
        ])

        connection.execute(upsert_names, [
            {
                'institution':  i.id,
                'name':         n.name,
                'year':         n.fromYear or 0
            }
            for i in institutions
            for n in i.names
        ])

        connection.execute(upsert_termtypes, [
            {
                'institution':  i.id,
                'type':         n.termType,
                'year':         n.fromYear or 0
            }
            for i in institutions
            for n in i.termTypeAcademicYears
        ])

def add_years():
    years = request.years()

    with engine.begin() as connection:
        insert = text('''
            INSERT INTO years (id, code)
            VALUES (:Id, :FallYear)
            ON CONFLICT DO NOTHING
        ''')

        connection.execute(insert, [year.model_dump() for year in years])

from sources.web.agreements import Agreement
# def get_courses():
#     institutions = request.institutions()

#     count = 0
#     for institution in institutions[:1]:
#         agreements = request.agreements(institution.id)

#         print(institution.names[0])

#         for agreement in agreements:
#             for year in agreement.sendingYearIds:
#                 if year >= 74:

#                     print('here')
#                     gold = request.agreement(year, institution.id, agreement.institutionParentId, Agreement.Type.ALLMAJORS)
#                     count += 1
#                     print('\t', agreement.institutionName, year)

def get_ivc():
    agreements = request.agreements(124)

    for agreement in agreements:
        for year in agreement.receivingYearIds:
            if year >= 74:
                request.agreement(year, agreement.institutionParentId, 124, Agreement.Type.ALLMAJORS)

get_ivc()