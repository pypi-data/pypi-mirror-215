from pstl.utls.plasmas.sheath import transitional
from pstl.utls.plasmas.sheath import thick

__all__ = [
    'find_ab_coefs',
    transitional,
    thick,
]


def find_ab_coefs(sheath, shape, *args, **kwargs):
    raise ValueError("find ab coefs")


def get_probe_to_sheath_ratio(r_p, lambda_D, *args, **kwargs):
    ratio = r_p/lambda_D
    if ratio <= 3:
        sheath_type = "thick"
    elif ratio > 3 and ratio < 50:
        sheath_type = "transitional"
    elif ratio >= 50:
        sheath_type = "thin"
    else:
        raise ValueError(
            "ratio is not in bounds check r_p and lambda_D: {r_p} and {lambda_D}")
    return ratio, {"sheath": sheath_type}
