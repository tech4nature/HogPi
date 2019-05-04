import client

post = client.clientPost()

place = input('Where are you?')
print(post.create_location('box-9082242689124', 'Test Location'))
print(post.create_weight('box-9082242689124', 'hog-4006200763017', 100.00))
print(post.create_inside_temp('box-9082242689124', 100.00))
print(post.create_outside_temp('box-9082242689124', 100.00))
print(post.upload_video('box-9082242689124', 'hog-4006200763017',
                        '/home/jack/Videos/2019-02-16-11-23-37.mp4'))
