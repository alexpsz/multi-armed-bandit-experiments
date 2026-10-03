# Legacy notes

These notes describe the files recovered in October 2026. Original programs, notebooks, the PDF, and extracted figures are preserved byte for byte. The HTML report has two local user-home paths in library warnings replaced with `<user-home>/`; its original and published hashes are recorded in the manifest. This archive does not silently fix the historical implementation.

## Nine-machine simulation

- The initial tables contain 396 records across nine machines: 32, 40, 4, 100, 39, 60, 8, 66, and 47 records. Their original collection method is not established by the saved files.
- In `data.py`, machine 1's 21st record is `(0,71, 2)`, a three-element tuple. The program reads its cost as 71. It may have been intended as `(0.71, 2)`, but that cannot be confirmed from the recovered code.
- `simulate_machine_play()` selects the cost multiplier and the prize-table multiplier independently. Their relationship should be reviewed before using a corrected model.
- Some prize amounts are randomized when `data.py` is imported. The original program does not set a random seed.
- The main loop uses 100,000 additional plays and prints the final averages. No separate output file from that run was recovered.
- `reward_prize_list.py` is an empty historical placeholder.

## MovieLens environment

The local dataset recovery found 1,000,209 ratings, 6,040 users, 3,883 movie metadata records, and 18 genres. There are 3,706 movies with ratings. These raw files are deliberately excluded from Git.

Each genre is an arm. Multi-genre movies contribute their ratings to each corresponding genre. A pull samples a rating from that genre's empirical frequency distribution, with replacement. This is a stationary simulation built from rating data; it does not implement personalized recommendations or replay logged user interactions.

## Experimental settings

| Section | Saved configuration |
| --- | --- |
| Q1 | 50,000 steps; 10 and 100 runs; UCB, ETC, TS |
| Q2 | 500, 5,000, 50,000, 500,000, 5,000,000 steps; 100 runs each |
| Q3 | 50,000 steps; 100 runs; total ETC exploration lengths 50, 500, 2,000, 5,000, 10,000 |
| Q4 | 50,000 steps; 100 runs; UCB `lota=1,2,4` and a variant using `f(t)=1+t*(log(t))²` |
| Q5 | 1,000,000 steps; 100 runs; TS, ETC, Standard UCB (`lota=4`), and the variant named Optimal UCB in the code |

The experiment calls generally use seed 122. The independent ETC notebook has 100 runs; independent UCB and TS have 10. The multiprocessing script currently uses 500 steps and 100 runs.

## Metrics and implementation

- Most comparison functions calculate regret as the current largest empirical arm mean minus the sampled reward. The reference changes with the algorithm and its observations. Historical rankings should be treated as reported observations, not a newly verified benchmark.
- The independent ETC notebook obtains its reference from an extra exploration pass, unlike the comparison notebooks.
- TS samples from a Gaussian distribution with standard deviation `sqrt(4/count)`. Beta parameters are present but are not used for arm selection.
- The first 18 TS initialization pulls are omitted from the regret accumulation.
- Independent UCB uses `log(t)`; the basic comparison and multiprocessing UCB use `log(n)`.
- Error bars represent the standard deviation across runs, not confidence intervals.
- The name Optimal UCB is preserved from the source. This archive makes no claim of theoretical optimality.
- The multiprocessing implementation seeds only the parent process and does not assign an explicit independent seed to each trial.

## Notebook versions and reports

Cell numbers below are zero-based, matching the extracted figure filenames.

- `Homework.ipynb` contains a saved `KeyboardInterrupt` in cell 7, for the 50,000-step / 100-run calculation. Later saved figures are still present; they do not establish a clean end-to-end execution of the current source.
- Both versions contain six figures. Their Q1 ten-run figures are identical.
- In Q2 cell 15, the original notebook selects the standard deviation for each horizon; v2 instead repeats `std_devs_500` five times. This is incompatible with the other curve lengths.
- The saved v2 Q2 figure has titles `Title 1` through `Title 5` and repeats the same 500-step curves. It does not match its saved source and must not be used as the five-horizon comparison.
- v2 adds dedicated Q3/Q4/Q5 plotting functions and clearer Q4/Q5 legends. The original's final Q5 interpretation is absent from v2.
- Execution counters are incomplete and sometimes out of order. A `_v2` filename alone does not establish the authoritative version.
- The HTML and PDF retain the original five-horizon comparison. The PDF records `Homework(1).ipynb` as its export source; that notebook was not recovered separately.

For historical review, use `Homework.ipynb` alongside the exported reports. The v2 Q4/Q5 legends can help interpret the colors. The reports record TS as best in Q5, but this ranking has not been rerun or independently validated during archival.

No standalone arrays of per-step rewards or regrets were recovered. The saved plots and prose are available; exact numerical trajectories cannot be restored solely from those images.

## Illustrations

The three `example_curve_*.py` programs draw hypothetical curves over 1,000 points: `sqrt(x)` for ETC/UCB, `log(x)` for TS. They do not execute bandit algorithms or use MovieLens. They are preserved as illustrations, not empirical results.

## Maintenance boundary

The 2026 archival work added structure, documentation, extracted figures, data-download instructions, and a hash/syntax check. It did not recreate the 2023 environment, correct the model, rerun the full notebooks, or replace historical figures with new results.

Future fixes should live separately from the recovered source and record the metric definition, random seeds, dependencies, and newly generated numerical results.
