from app.database import db
from werkzeug.security import generate_password_hash, check_password_hash
import heapq, json

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    interests = db.Column(db.JSON, nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def update_interests(self, document_keywords):
        max_keywords_count = 20

        user_keywords = json.loads(self.interests)
        document_keywords = self.prepare_document_keywords(document_keywords)

        for document_keyword in document_keywords:
            if document_keyword in user_keywords:
                user_keywords[document_keyword]+=1
            else:
                user_keywords[document_keyword] = 1

        prepared_keywords = dict(heapq.nlargest(max_keywords_count, user_keywords.items(), key=lambda item: item[1]))
        
        self.interests = json.dumps(prepared_keywords)
        db.session.commit()
    
    def prepare_document_keywords(self, keywords):
        first_document_keywords_count = 4

        keywords = keywords.replace('[', "")
        keywords = keywords.replace(']', "")
        keywords = keywords.replace(' ', "")
        keywords = keywords.replace('\'', "")
        keywords = keywords.split(',')

        first_document_keywords = keywords[:first_document_keywords_count]

        return first_document_keywords