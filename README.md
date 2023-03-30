# Data Version Control: demo for engineering seminar

### 1. Initialize DVC
1.1. Create project folder

```
mkdir dvc_demo; cd dvc_demo
```

1.2. Install DVC
```
pip install dvc
```

1.3. Initialize git and DVC
```
git init
dvc init
```

1.4. Connect storage

We will use Google Drive. Create folder on Drive and copy last part of URL into cmd.
```
dvc remote add --default storage gdrive://1kSbUT3YuapUG-Pea_a9uctG8tbq8qxRW
```

1.5. git commit
```
git add .
git commit
```
<br>
The project is initiated and has the following structure:

```
dvc_demo
├── .dvc            - DVC internals.
│   ├── tmp         - Misc temp files.
│   ├── .gitignore  - Files ignored by git - DVC internals, cache, large files and secrets.
│   └── config      - Main DVC config file - only remote storage for now.
└── .dvcignore      - Analogous to git ignore but for DVC.
```
<br>

### 2. Data

2.1. Create a data folder and copy the data

```
mkdir data, copy xyz/data.csv data/data.csv
```

2.2. Add data to DVC
```
dvc add data/data.csv
```

2.3. Push data to DVC remote
```
dvc push
```

2.4. git commit
```
git add .
git commit
```
<br>
Data was added to DVC and pushed to remote. Project has the following structure:

```
dvc_demo
├── .dvc
│   ├── cache            - Cached DVC files - push/pull to/from remote.
│   │   └── a9/e16...    - Cached data/data.csv file. Addressed by md5, same as in data/data.csv.dvc.
│   ├── tmp
│   ├── .gitignore
│   └── config
├── data
│   ├── .gitignore       - git ignores data.csv (large file).
│   ├── data.csv         - Data file.
│   └── data.csv.dvc     - Metafile (or link file) for DVC tracking. Contains size, path and md5 - a9e16...
└── .dvcignore
```
<br>

### 3. Pipeline

3.1. Create preprocess, train, eval script.
```
mkdir src
copy xyz/src/preprocess.py src/preprocess.py
copy xyz/src/train.py src/train.py
```

3.2. Create DVC parameters file
```
echo "solver: lbfgs" > params.yaml
```

3.3. Create a DVC pipeline file
```
echo "
stages:                             # Stages of pipeline
  preprocess:                       # Stage 1 - Preprocess
    cmd: python src/preprocess.py   # Stage 1 runs with this command
    deps:                           # Stage 1 dependency
      - src/preprocess.py           # Stage 1 depends on preprocess script
      - data/data.csv               # Stage 1 depends on raw data
    outs:                           # Stage 1 output
      - data/clean.csv              # Stage 1 outputs prepared dataset
  train:                            # Stage 2 - Train
    cmd: python src/train.py        # Stage 2 runs with this command
    deps:                           # Stage 2 dependencies
      - src/train.py                # Stage 2 depends on the train script
      - data/clean.csv              # Stage 2 depends on prepared data
    params:                         # Stage 2 parameters
      - solver                      # Stage 2 uses "solver" param from params.yaml
    metrics:                        # Stage 2 metrics
      - metrics.json                # Stage 2 special output metrics.json
" > dvc.yaml
```

3.4. Explore and run the pipeline
```
dvc dag
dvc repro
```

3.5. Push data and git commit
```
dvc push
git add .
git commit
```
<br>
Data was added to DVC and pushed to remote. The project has the following structure:

```
dvc_demo
├── .dvc
│   ├── cache
│   │   └── a9/e16...
│   │   ├── d3/1db...   - Cached metrics.json file.
│   │   └── runs        - Cached artifacts of stages from dvc.yaml.
│   ├── tmp
│   ├── .gitignore
│   └── config
├── data
│   ├── .gitignore      - Ignores both data.csv and clean.csv - too large for git and tracked by DVC.
│   ├── clean.csv       - Cleaned data from Stage 1 - preprocess.
│   ├── data.csv
│   └── data.csv.dvc
├── src                 - Scripts folder.
│   ├── preprocess.py   - Preprocess script.
│   └── train.py        - Train (and eval) script.
├── .dvcignore
├── .gitignore          - Ignores metrics.json because it is tracked by DVC.
├── dvc.lock            - Tracks md5 of all inputs, scripts, params and dependencies. In case of change, DVC repro reruns stage.
├── dvc.yaml            - Pipeline file defining stages.
├── metrics.json        - Metrics output defined in src/train.py script and tracked by DVC.
└── params.yaml         - Parameters file.
```

### 4. Traversing project
There are three commits on current branch.
```
git log
```

```
commit hash_3
  Pipeline run.
  
commit hash_2
  Added raw data.

commit hash_1
  Init project.
```

Move through commits as usual with git and DVC pull data after every checkout.

Move to initial stage:
```
git checkout hash_1
dvc pull
```

Move to data stage:
```
git checkout hash_2
dvc pull
```

Move to pipeline stage:
```
git checkout hash_3
dvc pull
```
