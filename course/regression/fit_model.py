import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from pathlib import Path
from course.utils import find_project_root


VIGNETTE_DIR = Path('data_cache') / 'vignettes' / 'regression'


def _fit_model(df):
    """Given data frame df containing columns 'shortfall', 'n_rooms', 'age' and
    'local_authority_code'
    Fit a linear mixed model with shortfall as the response variable
    n_rooms and age as fixed predictors
    with local_authority_code as a random effect"""
    model = smf.mixedlm("shortfall ~ n_rooms + age", data=df,
                        groups=df["local_authority_code"])
    result = model.fit()
    return result


def _save_model_summary(model, outpath):
    with open(outpath, "w") as f:
        f.write(model.summary().as_text())


def _random_effects(results):
    re_df = pd.DataFrame(results.random_effects).T
    re_df.columns = ['Intercept'] + [f"Slope_{i}" for i in range(len(re_df.columns)-1)]
    re_df['group'] = re_df.index
    stderr = np.sqrt(results.cov_re.iloc[0, 0])
    re_df['lower'] = re_df['Intercept'] - 1.96 * stderr
    re_df['upper'] = re_df['Intercept'] + 1.96 * stderr
    re_df = re_df.sort_values('Intercept')
    return re_df


def _save_residual_plots(results, outdir):
    """Generate residual diagnostic plots for a MixedLM model."""
    import matplotlib.pyplot as plt
    import scipy.stats as stats

    outdir.mkdir(parents=True, exist_ok=True)

    resid = results.resid
    fitted = results.fittedvalues
    sigma = np.sqrt(results.scale)
    std_resid = resid / sigma

    # -----------------------
    # 1. Residuals vs Fitted
    # -----------------------
    plt.figure(figsize=(6, 4))
    plt.scatter(fitted, resid, alpha=0.5)
    plt.axhline(0, color='red', linestyle='--')
    plt.xlabel("Fitted values")
    plt.ylabel("Residuals")
    plt.title("Residuals vs Fitted")
    plt.tight_layout()
    plt.savefig(outdir / "residuals_vs_fitted.png")
    plt.close()

    # -----------------------
    # 2. Normal QQ plot
    # -----------------------
    plt.figure(figsize=(6, 4))
    stats.probplot(std_resid, dist="norm", plot=plt)
    plt.title("Normal Q–Q Plot (Std Residuals)")
    plt.tight_layout()
    plt.savefig(outdir / "qq_plot.png")
    plt.close()

    # -----------------------
    # 3. Scale–Location Plot
    # -----------------------
    plt.figure(figsize=(6, 4))
    plt.scatter(fitted, np.sqrt(np.abs(std_resid)), alpha=0.5)
    plt.xlabel("Fitted values")
    plt.ylabel("√|Standardized Residuals|")
    plt.title("Scale–Location Plot")
    plt.tight_layout()
    plt.savefig(outdir / "scale_location.png")
    plt.close()


def fit_model():
    base_dir = find_project_root()
    df = pd.read_csv(base_dir / 'data_cache' / 'la_energy.csv')
    results = _fit_model(df)

    # Ouput directories
    model_dir = base_dir / 'data_cache' / 'models'
    diag_dir = model_dir / 'diagnostics'
    model_dir.mkdir(parents=True, exist_ok=True)
    diag_dir.mkdir(parents=True, exist_ok=True)

    # Save summary + random effects
    _save_model_summary(results, VIGNETTE_DIR / 'model_fit.txt')
    _random_effects(results).to_csv(model_dir / 'reffs.csv', index=False)

    # Save diagnostic plots
    _save_residual_plots(results, diag_dir)
