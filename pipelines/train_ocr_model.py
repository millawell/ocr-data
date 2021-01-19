import subprocess
import click
from pathlib import Path
from lxml import  etree
import tempfile
from shutil import copy2
from sklearn.model_selection import train_test_split



@click.command()
@click.option('--pdf_path')
def main(pdf_path):

    pdf_file_name = Path(pdf_path).name
    identifier = Path(pdf_path).stem
    xml_file_name = Path(f"../data/xml_output/{pdf_file_name}")
    xml_file_name = xml_file_name.with_suffix(".hocr")

    with open(xml_file_name) as fin:
        tree = etree.fromstring(fin.read())

    language = tree.find(".//meta[@name='dc:language']").attrib['content']

    if language == "en":
        baseline_model = '../data/baseline_models/en_best.mlmodel'
    elif language == "de":
        baseline_model = '../data/baseline_models/fraktur_1_best.mlmodel'

    with tempfile.TemporaryDirectory() as tmp_dir:
        files = []
        for fn in Path("../data/pair_output/").iterdir():
            if fn.stem.startswith(identifier):
                if fn.suffix =='.png':
                    copy2(fn, tmp_dir)
                    files.append(Path(tmp_dir) / fn.name)
                elif fn.suffix =='.txt':
                    dst = Path(tmp_dir) / f"{fn.stem}.gt{fn.suffix}"
                    copy2(fn, dst)

        train_files, other_files = train_test_split(files, train_size=.8)
        eval_files, test_files = train_test_split(other_files, train_size=.5)

        train_manifest_path = Path(tmp_dir) / 'train_manifest.txt'
        with open(train_manifest_path, "w") as fout:
            fout.write("\n".join(map(str, train_files)))
        
        eval_manifest_path = Path(tmp_dir) / 'eval_manifest.txt'
        with open(eval_manifest_path, "w") as fout:
            fout.write("\n".join(map(str, eval_files)))

        test_manifest_path = Path(tmp_dir) / 'test_manifest.txt'
        with open(test_manifest_path, "w") as fout:
            fout.write("\n".join(map(str, test_files)))

        command = f"ketos test -m {baseline_model} --evaluation-files {test_manifest_path}"
        with open(Path(f"../models/baseline_{identifier}.txt"), "w") as fout:
            subprocess.call(command, shell=True, stdout=fout, stderr=fout)

        command = f"OMP_NUM_THREADS=1 ketos train --output ../models/model_{identifier} --resize add --epochs 4 -i {baseline_model} --training-files {train_manifest_path} --evaluation-files {eval_manifest_path}"
        subprocess.call(command, shell=True)

        best_model_name = Path(f"../models/model_{identifier}_best.mlmodel")
        
        command = f"ketos test -m {best_model_name} --evaluation-files {test_manifest_path}"
        with open(Path(f"../models/fine_tuned_{identifier}.txt"), "w") as fout:
            subprocess.call(command, shell=True, stdout=fout, stderr=fout)

if __name__ == '__main__':
    main()
