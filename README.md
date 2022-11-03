# 🐠

## Requirements
```bash
pip install pandas tqdm tabulate
```

## Input file format
```
- <name1>
day: start-end, start-end
day: start-end, start-end, start-end
day: start-end
day: start-end
day: start-end
- <name2>
day: start-end
day: start-end
.
.
.
```

For example,
```
- 한만혁
월: 15-18
화: 15-18
수: 15-18
목: 15-18
금: 15-18
- 혁만혁
화: 11-16
수: 11-16
- 만혁혁
화: 16-19
수: 16-17
목: 16-17
금: 13-15
```
See [`input.txt`](./input.txt).

## Usage
```bash
python main.py <path_to_input_file> -n <num_solutions> -o <output>
# python main.py input.txt -n 3 -o timetable
# > timetable_0.csv
# > timetable_1.csv
# > timetable_2.csv
```