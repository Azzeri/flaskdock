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

    def update_user_interests(self, document_synsets):
        max_synsets_count = 20
        user_synsets = json.loads(self.interests)
        document_synsets = self.prepare_document_synsets(document_synsets)

        for document_synset in document_synsets:
            if document_synset in user_synsets:
                user_synsets[document_synset] += 1
            else:
                user_synsets[document_synset] = 1

        prepared_synsets = dict(
            heapq.nlargest(
                max_synsets_count, user_synsets.items(), key=lambda item: item[1]
            )
        )
        self.interests = json.dumps(prepared_synsets)
        db.session.commit()

    def prepare_document_synsets(self, synsets):
        first_document_synsets_count = 4

        synsets = synsets.replace("[", "")
        synsets = synsets.replace("]", "")
        synsets = synsets.replace(" ", "")
        synsets = synsets.replace("'", "")
        synsets = synsets.split(",")

        first_document_synsets = synsets[:first_document_synsets_count]

        return first_document_synsets
