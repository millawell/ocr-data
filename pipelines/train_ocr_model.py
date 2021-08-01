import subprocess
import click
from pathlib import Path
from lxml import  etree
import sys
sys.path.append("../utils/")
from mets import parse_mets
import tempfile
from shutil import copy2
from sklearn.model_selection import train_test_split
import pandas as pd
import re

def extract_accuracy(str_):
    return float(
        re.search(
            r'Average accuracy: [0123456789]+.[0123456789]+', 
            str_
        ).group().replace('Average accuracy: ','')
    )


@click.command()
@click.option('--pdf_paths', multiple=True)
def main(pdf_paths):
    
    pdf_file_names = []
    identifiers = []
    sheet_records = []
    for pdf_path in pdf_paths:
        pdf_file_names.append(Path(pdf_path).name)
        identifiers.append(Path(pdf_path).stem)
        sheet_records.append(parse_mets(pdf_file_names[-1]))

    languages = list(set([sr["language"] for sr in sheet_records]))
    assert len(languages) == 1, "you provided pdfs with different languages."

    if languages[0] == "en":
        baseline_model = '../data/baseline_models/en_best.mlmodel'
    elif languages[0] == "de":
        baseline_model = '../data/baseline_models/fraktur_1_best.mlmodel'

    with tempfile.TemporaryDirectory() as tmp_dir:
        files = []
        for fn in Path("../data/pair_output/").iterdir():
            if any(fn.stem.startswith(id_) for id_ in identifiers):
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

        if len(identifiers)>1:
            joined_identifier = '-'.join([ide[:3] for ide in identifiers])
        else:
            joined_identifier = identifiers[0]

        command = f"ketos test -m {baseline_model} --evaluation-files {test_manifest_path}"
        baseline_stdout = Path(f"../models/baseline_{joined_identifier}.txt")
        with open(baseline_stdout, "w") as fout:
            subprocess.call(command, shell=True, stdout=fout, stderr=fout)

        command = f"OMP_NUM_THREADS=1 ketos train --output ../models/model_{joined_identifier} --resize add --epochs 4 -i {baseline_model} --training-files {train_manifest_path} --evaluation-files {eval_manifest_path}"
        subprocess.call(command, shell=True)

        best_model_name = Path(f"../models/model_{joined_identifier}_best.mlmodel")
        
        command = f"ketos test -m {best_model_name} --evaluation-files {test_manifest_path}"
        fine_tuned_stdout = Path(f"../models/fine_tuned_{joined_identifier}.txt")
        with open(fine_tuned_stdout, "w") as fout:
            subprocess.call(command, shell=True, stdout=fout, stderr=fout)

        fname_ds_description = Path(f"../models/dataset_description_{joined_identifier}.txt")

        description = [{
            "identifier": joined_identifier,
            "train_num_lines": len(train_files), 
            "test_num_lines": len(test_files), 
            "train_num_chars": sum(len((
                Path(tmp_dir) / f"{fn.stem}.gt.txt"
            ).open().read()) for fn in train_files),
            "test_num_chars": sum(len((
                Path(tmp_dir) / f"{fn.stem}.gt.txt"
            ).open().read()) for fn in test_files), 
            "baseline_acc": extract_accuracy(baseline_stdout.open().read()),
            "fine_tuned_acc": extract_accuracy(fine_tuned_stdout.open().read()),
        }]

        pd.DataFrame(description).to_csv(fname_ds_description, index=False)


if __name__ == '__main__':
    main()

# from pathlib import Path
# import pandas as pd
# p = Path("../models/")
# results = []
# for f in p.iterdir():
#     if f.suffix == '.txt' and f.stem.startswith('dataset_description'):
#         results.append(pd.read_csv(f))
# results = pd.concat(results)
# results['improvement'] = results.fine_tuned_acc - results.baseline_acc
# results.sort_values('fine_tuned_acc')
