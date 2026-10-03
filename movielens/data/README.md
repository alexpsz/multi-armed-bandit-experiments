# MovieLens 1M setup

Obtain the dataset from the [official GroupLens page](https://grouplens.org/datasets/movielens/1m/) and read its [usage conditions](https://files.grouplens.org/datasets/movielens/ml-1m-README.txt).

The original programs load files from the current working directory. Extract these files into `movielens/`, alongside the notebooks:

```text
movielens/
  movies.dat
  ratings.dat
  users.dat
  Homework.ipynb
  ...
```

For example, from the repository root on macOS/Linux:

```sh
curl --fail --location --output /tmp/ml-1m.zip \
  https://files.grouplens.org/datasets/movielens/ml-1m.zip
unzip /tmp/ml-1m.zip -d /tmp
cp /tmp/ml-1m/movies.dat /tmp/ml-1m/ratings.dat /tmp/ml-1m/users.dat movielens/
```

Only the three data files are needed by the historical code. Keep the official README with your local download for its terms and attribution. Raw `.dat` files and dataset archives are ignored by Git and are not redistributed in this repository.
