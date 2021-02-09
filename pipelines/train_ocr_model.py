import subprocess
import click
from pathlib import Path
from lxml import  etree
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
        baseline_stdout = Path(f"../models/baseline_{identifier}.txt")
        with open(baseline_stdout, "w") as fout:
            subprocess.call(command, shell=True, stdout=fout, stderr=fout)

        command = f"OMP_NUM_THREADS=1 ketos train --output ../models/model_{identifier} --resize add --epochs 4 -i {baseline_model} --training-files {train_manifest_path} --evaluation-files {eval_manifest_path}"
        subprocess.call(command, shell=True)

        best_model_name = Path(f"../models/model_{identifier}_best.mlmodel")
        
        command = f"ketos test -m {best_model_name} --evaluation-files {test_manifest_path}"
        fine_tuned_stdout = Path(f"../models/fine_tuned_{identifier}.txt")
        with open(fine_tuned_stdout, "w") as fout:
            subprocess.call(command, shell=True, stdout=fout, stderr=fout)

        fname_ds_description = Path(f"../models/dataset_description_{identifier}.txt")

        description = [{
            "identifier": identifier,
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
# p = Path(".")
# results = []
# for f in p.iterdir():
#     if f.suffix == '.txt' and f.stem.startswith('dataset_description'):
#         results.append(pd.read_csv(f))
# results = pd.concat(results)
# results['improvement'] = results.fine_tuned_acc - results.baseline_acc
# 0  J4knAAAAMAAJ               20  ...         86.57           86.57
# 0  fAoOAAAAQAAJ               40  ...         96.35           97.08
# 0  MzQJAAAAQAAJ               36  ...         10.61           10.10
# 0  rDUJAAAAQAAJ               82  ...         96.54           97.12
# 0  u4cnAAAAMAAJ               76  ...         93.68           97.40
# 0  2jMfAAAAMAAJ              157  ...         90.22           96.29
# 0  8dAyAQAAMAAJ               88  ...         74.91           83.96
# 0  _QgOAAAAQAAJ               60  ...         90.72           94.20
# 0  Fy4JAAAAQAAJ               20  ...         85.48           91.94
# 0  t88yAQAAMAAJ               84  ...         89.53           95.94
# 0  DNUwAQAAMAAJ               76  ...         53.42           44.86
# 0  oNEyAQAAMAAJ               73  ...         73.84           81.10
# 0  3pVMAAAAcAAJ               92  ...         95.90           99.39
# 0  D5pMAAAAcAAJ               88  ...         90.51           93.85
# 0  YAZXAAAAcAAJ             1752  ...         82.15           93.50
# 0  WjMfAAAAMAAJ              183  ...         68.81           92.20
# 0  XtEyAQAAMAAJ               86  ...         79.30           89.25
# 0  wggOAAAAQAAJ               19  ...         92.94           92.94
# 0  aNQwAQAAMAAJ               52  ...         96.83           98.42
# 0  AdiKyqdlp4cC               77  ...         91.70           97.30
# 0  4zQfAAAAMAAJ              159  ...         92.32           97.20
# 0  HCRMAAAAcAAJ              125  ...         92.99           98.29
# 0  H9UwAQAAMAAJ               76  ...         97.10           99.28
# 0  zDTMtgEACAAJ               76  ...         17.68            4.16
# 0  7JVMAAAAcAAJ               89  ...         84.18           96.71
