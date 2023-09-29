def handle_file(f):
    with open(f'media/{f.name}', 'wb') as file:
        if f.multiple_chunks():
            for chunks in f.chunks():
                file.write(chunks)
        else:
            file.write(f.read())