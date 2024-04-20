import pandas as pd
from surprise import Dataset, KNNBasic, Reader, dump
from surprise.model_selection import GridSearchCV

ratings_df = pd.read_csv("data/processed/ratings_explicit.csv")

reader = Reader(rating_scale=(1, 10))

data = Dataset.load_from_df(ratings_df[["user_id", "isbn", "book_rating"]], reader)

# TODO: adjust params
param_grid = {
    "k": [10, 20, 40],
    "sim_options": {
        "name": ["msd", "pearson"],
        "user_based": [False],
    },
}


gs = GridSearchCV(KNNBasic, param_grid, measures=["rmse", "mae"], cv=5)

gs.fit(data)

print(f"RMSE score: {gs.best_score['rmse']}")
print(f"MAE score: {gs.best_score['mae']}")

print(f"RMSE params: {gs.best_params['rmse']}")
print(f"MAE params: {gs.best_params['mae']}")

# contains all logging informaiton for MLflow
results_df = pd.DataFrame.from_dict(gs.cv_results)

print(results_df)

# TODO: save both RMSE and MAE versions IF they are different
algo = gs.best_estimator["rmse"]
algo.fit(data.build_full_trainset())

dump.dump("src/models/SVD", algo=algo)
