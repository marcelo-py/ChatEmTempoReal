import uuid

id1 ='123'
id2 = '60'

room_name = str(uuid.uuid3(uuid.NAMESPACE_URL, '-'.join(sorted([id1, id2]))))

print(room_name)