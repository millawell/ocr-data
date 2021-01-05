import json
import click


@click.command()
@click.option('--book')
def main(book):
    
    f = open("../data/data.json", "r+")
    data = json.load(f)
    f.close()

    out = ""
    for i in data[book]["pagenr"]:
        out+=str(i[2]+i[3])
        out+=" "
    out = list(out)

    print(data[book]["id"])
    print(len(data[book]["transcribes"]))
    print("".join(out[:-1]))
    
if __name__ == '__main__':
    main()


