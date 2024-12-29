## bqcli

![PyPI](https://badge.fury.io/py/bqcli.svg)
![Test](https://github.com/jancervenka/bqcli/actions/workflows/test.yml/badge.svg)
![Publish](https://github.com/jancervenka/bqcli/actions/workflows/publish.yml/badge.svg)

<img src=".assets/bqcli.png" align="center" />

### Installation and Usage

The program can be installed with `pip`, it will set up an entry point called `bqcli`.

```bash
pip install bqcli
bqcli
```

Or you can use the tool command `uvx` from `uv` and run `bqcli` without installing it first.

```bash
uvx bqcli
```

### GCP Authentication

All the standard methods such as `gcloud` or `GOOGLE_APPLICATION_CREDENTIALS` should work.
