import hashlib 

id1 = 1
id2 = 1

room_name = hashlib.md5(f'{id1}-{id2}'.encode()).hexdigest()
print(room_name)