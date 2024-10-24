import pypandoc

if __name__ == '__main__':
    data = pypandoc.convert_file('data/100.md', 'plain')
    print(data)