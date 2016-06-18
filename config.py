import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'postgresql://bas:bas@localhost/bas'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False


QUESTIONS_ADDR = "app/data/questions.json"
AGGREGATED_ADDR = "app/data/aggregated_data.json"
QUESTIONS_TO_SHOW = [1,2,3,6,7]
QUESTIONS_TO_STATISTICS = [1,2,3,4,5,6,7]