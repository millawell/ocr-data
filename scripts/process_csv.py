from pprint import pprint
import click



@click.command()
@click.option('--book')
def main(book):
    
    data = {}
    
    f = open("sheet3_v2.csv")
    lines = f.readlines()
    
    for i in range(3, len(lines)):
        s = lines[i].split(",")
        if len(s)>4:
            if ".png" in s[3]:
                if s[5] != "" or s[10]=="*\n":
                    pagenr= int(s[9].replace("\n", "").split("/")[0])
                    
                    if s[10]!="*\n":
                        pagenr-=4
                        
                    data[name].append([s[3], pagenr])

            elif s[3]=="":
                pass
            else:
                name=s[3]
                data[name]=[]
    
    f.close()    
    out = ""
    for i in data[book]:
        out+=str(i[1]+4)
        out+=" "
    out = list(out)
    print("".join(out[:-1]))
    
    return




if __name__ == '__main__':
    main()
