# uuid.uuid4().hex --> '8a0c1722b227489388497600ecf8dae9' // 32 chars


from base64 import standard_b64decode
from string import ascii_letters, digits
from random import choices
from uuid import uuid4


class Note:
    def create_note(_enc_message, _hash_password, _uuid=uuid4().hex):

