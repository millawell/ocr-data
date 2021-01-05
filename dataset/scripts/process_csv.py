from pprint import pprint
import click
import json

#TODO set offsets


@click.command()
@click.option('--book')
@click.option('--csv')
def main(book, csv):
    
    data = {}
    
    f = open(csv)
    lines = f.readlines()
    
    for i in range(3, len(lines)):
        s = lines[i].split(",")
        if len(s)>4:
            if ".png" in s[3]:
                if s[5] != "" or s[10]=="*\n":
                    pagenr= int(s[9].replace("\n", "").split("/")[0])
                    
                    if s[10]!="*\n":
                        pagenr-=4
                        
                    offset = 0
                        
                    data[name]["pagenr"].append([s[1], s[3], pagenr, offset])
                    if s[1] not in data[name]["transcribes"]:
                        data[name]["transcribes"].append(s[1])

            elif s[3]=="":
                pass
            else:
                name=s[3]
                data[name] = {}
                data[name]["pagenr"]=[] 
                data[name]["id"] = s[5]
                data[name]["transcribes"] = []
                data[name]["pdfs"]=s[2].split(" ")
    
    
    f.close()  
    
    out = ""
    for i in data[book]["pagenr"]:
        out+=str(i[2]+i[3])
        out+=" "
    out = list(out)
    
    print(data[book]["id"])
    print(len(data[book]["transcribes"]))
    print("".join(out[:-1]))
    
    json_out = json.dumps(data)
    f = open("../data/data.json","w")
    f.write(json_out)
    f.close()
    
    return




if __name__ == '__main__':
    main()
