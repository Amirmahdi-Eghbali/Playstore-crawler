import json
import redis
import schedule
import time
from datetime import date, datetime
from google_play_scraper import app, reviews, Sort
import psycopg2
# client to redeis
redis_client = redis.StrictRedis(host='redis', port=6379, db=0)


postgre_connection = psycopg2.connect(
    user='postgres',
    password='AmIrMaHdI',
    host='postgres',
    port=5432
)
cursor = postgre_connection.cursor()



cursor.execute(
'''
CREATE TABLE IF NOT EXISTS application_info(
    crawl_date TIMESTAMP PRIMARY KEY,
    app_id VARCHAR(255),
    min_installs BIGINT,
    real_installs BIGINT,
    score NUMERIC(2,1),
    ratings INTEGER,
    reviews INTEGER,
    last_updated_on TIMESTAMP,
    version VARCHAR(255),
    ad_supported BOOLEAN
)
'''
)


cursor.execute(
'''
CREATE TABLE IF NOT EXISTS apps_id(
    id SERIAL PRIMARY KEY,
    app_id VARCHAR(255) NOT NULL,
    genre VARCHAR(255)
)
''')


cursor.execute(
'''
CREATE TABLE IF NOT EXISTS application_reviews(
    review_id VARCHAR(255) PRIMARY KEY,
    app_id VARCHAR(255),
    review_date TIMESTAMP,
    user_name VARCHAR(255),
    thumbs_up_count INTEGER,
    score NUMERIC(2,1),
    content TEXT,
    crawl_date TIMESTAMP
)
'''
)

postgre_connection.commit()

# applications names list
def get_apps():
    cursor.execute('SELECT app_id FROM "apps_id"')
    apps = cursor.fetchall()
    return[app[0] for app in apps]


def get_app_info(app_id):
    try:
        print('info')
        app_info = app(app_id)
        print(app_info)
        info = {
            'minInstalls' : app_info['minInstalls'],
            'realInstalls' : app_info['realInstalls'],
            'score' : app_info['score'],
            'ratings' : app_info['ratings'],
            'reviews' : app_info['reviews'],
            'lastUpdatedOn' : app_info['lastUpdatedOn'],
            'version' : app_info['version'],
            'adSupported' : app_info.get('adSupported', False),
        }
        
        redis_client.set(f'app_info:{app_id}', json.dumps(info))
        print('Succeed and stored info for:'+app_id)
    except Exception as e:
        print('could not get info for:'+f'{app_id}:{e}')

def get_reviews(app_id):
    try:
        print(('reviews'))

        revs, _ = reviews(
        app_id,
        count=1000,
    )       
        print(len(revs))
        for review in revs:
            if isinstance(review['at'], (datetime, date)):
                review['at'] = review['at'].isoformat()
            review_data = {
                'reviewId': review['reviewId'],
                'at': review['at'],
                'userName': review['userName'],
                'thumbsUpCount': review['thumbsUpCount'],
                'score': review['score'],
                'content': review['content'],
            }
            redis_client.lpush(f'app_reviews:{app_id}', json.dumps(review_data))
        print('Succeed and stored reviews for:'+app_id)
    except Exception as e:
        print('could not get reviews for:'+f'{app_id}:{e}')

def start():
    apps = get_apps()
    for app_id in apps:
        get_app_info(app_id)
        get_reviews(app_id)


def store_data_in_database():
    apps = get_apps()
    for app_id in apps:
        app_data = redis_client.get(f'app_info:{app_id}')
        redis_client.delete(f'app_info:{app_id}')
        if app_data is not None:
            app_info = json.loads(app_data)
            now = datetime.now()
            cursor.execute('''
                INSERT INTO application_info (app_id, min_installs, real_installs, score, ratings, reviews, last_updated_on, version, ad_supported, crawl_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (app_id, app_info['minInstalls'], app_info['realInstalls'], app_info['score'],
                  app_info['ratings'], app_info['reviews'],
                  app_info['lastUpdatedOn'], app_info['version'],
                  app_info['adSupported'], now))

        review_list = f'app_reviews:{app_id}'
        while True:
            review_data = redis_client.rpop(review_list)
            if  not review_data:
                break
            review = json.loads(review_data)
            cursor.execute('''
                INSERT INTO application_reviews(review_id, app_id, review_date, user_name, thumbs_up_count, score, content, crawl_date)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (review_id) DO UPDATE
                SET thumbs_up_count = EXCLUDED.thumbs_up_count
                ''',(review['reviewId'], app_id, review['at'],
                     review['userName'], review['thumbsUpCount'],
                     review['score'], review['content'], now))
    
    postgre_connection.commit()
    print('data stored in database')


start()
schedule.every(60).minutes.do(start)


while True:
    schedule.run_pending()
    for app_id in get_apps():
        if redis_client.exists(f'app_info:{app_id}') or redis_client.llen(f'app_reviews:{app_id}')>0:
            store_data_in_database()
            break
    time.sleep(10)
        



