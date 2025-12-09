import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats


def _save_residual_plots(results, outdir):
    """Generate residual diagnostic plots for a MixedLM model."""
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
