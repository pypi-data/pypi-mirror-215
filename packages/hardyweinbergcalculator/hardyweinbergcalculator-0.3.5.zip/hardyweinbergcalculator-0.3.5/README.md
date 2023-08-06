[![Build test and deploy to package repository](https://github.com/dellius-alexander/Hardy-Weinberg/actions/workflows/deploy.yml/badge.svg)](https://github.com/dellius-alexander/Hardy-Weinberg/actions/workflows/deploy.yml)

---

# Hardy Weinberg Equilibrium


Hardy-Weinberg Equilibrium Calculator. Calculates the expected 
genotype frequencies based on the allele frequencies of a 
population in Hardy-Weinberg equilibrium.

## Installation

```bash
pip install hardyweinbergcalculator
```

## Usage

```text
usage: hwc [-h] [--version] [--verbose] [--debug] [--samples SAMPLES] [--p P] [--q Q] [--tpop TPOP] [--ppop PPOP] [--qpop QPOP] [--pq2pop PQ2POP] [--genes GENES [GENES ...]] [--json JSON [JSON ...]]

Hardy-Weinberg Equilibrium Calculator. Calculates the expected genotype frequencies based on the allele frequencies of a population in Hardy-Weinberg equilibrium. See: https://en.wikipedia.org/wiki/Hardy%E2%80%93Weinberg_principle


optional arguments:
  -h, --help         show this help message and exit
  --version          show program's version number and exit
  --verbose          Enable verbose logging. (default: False)
  --debug            Enable debug logging. (default: False)
  --samples SAMPLES  Number of samples to generate, if using random data generator. (default: None)
  --p P              Frequency of dominant allele. (default: None)
  --q Q              Frequency of recessive allele. (default: None)
  --tpop TPOP        Total population. (default: None)
  --ppop PPOP        Original population of dominant allele. (default: None)
  --qpop QPOP        Original population of recessive allele. (default: None)
  --pq2pop PQ2POP    Original population of heterozygous allele. (default: None)

Example: python3 -m hwc --ppop 10 --qpop 10 --pq2pop 200 --verbose
```

### Generate random data

```bash 
python3 -m hwc --samples 1000 --verbose
```

### Calculate from known data

```bash
python3 -m hwc --ppop 10 --qpop 10 --pq2pop 200 --verbose
```

## In your code

### Test for Hard-Weinberg Equilibrium from generated data

```python
from hwc import generate_population, HardyWeinberg

# Generate random data
population = generate_population(n=1000)
res = HardyWeinberg(genes=population)
print(res)
```

### Test for Hardy-Weinberg Equilibrium from known data

```python
from hwc import HardyWeinberg

# Known data
res = HardyWeinberg(
            homozygous_dominant_population=20,
            homozygous_recessive_population=44,
            heterozygous_population=95
            )
print(res)
```

### Results Data Object

The results returned from the Hardyweinberg test will ultimately look like this, in json format:

```json
{
    "2*pq": 0.4986501057404244,
    "chi_square_test": 20.439848879167698,
    "expected_heterozygous_population": 1132.434390136504,
    "expected_homozygous_dominant_population": 510.28280493174816,
    "expected_homozygous_recessive_population": 628.2828049317482,
    "genes": 0,
    "heterozygous_population": 1025.0,
    "homozygous_dominant_population": 564.0,
    "homozygous_recessive_population": 682.0,
    "p": 0.47402025539409953,
    "p + q": 1.0,
    "p**2": 0.22469520252388733,
    "p**2 + 2*pq + q**2": 1.0,
    "q": 0.5259797446059005,
    "q**2": 0.2766546917356883,
    "total_population": 2271.0
}

```
