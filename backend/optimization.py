
"""Week 3: Budget-constrained customer discount optimization."""

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import lil_matrix


def optimize_discount_allocation(
    incremental_revenue,
    discounts,
    budget,
):
    """
    Maximize expected net gain subject to a strict budget.

    Each customer can receive at most one positive discount.
    incremental_revenue[i, j] is the modeled incremental revenue
    for customer i at discount j.
    """
    revenue = np.asarray(incremental_revenue, dtype=float)
    discounts = np.asarray(discounts, dtype=float)
    budget = float(budget)

    if revenue.ndim != 2:
        raise ValueError("incremental_revenue must be a 2D array.")

    n_customers, n_options = revenue.shape

    if n_options != len(discounts):
        raise ValueError("Discount count must match revenue columns.")

    if not np.isfinite(budget) or budget < 0:
        raise ValueError("Budget must be finite and non-negative.")

    if not np.all(np.isfinite(discounts)):
        raise ValueError("Discounts must be finite.")

    if np.any(discounts < 0):
        raise ValueError("Discounts cannot be negative.")

    if not np.all(np.isfinite(revenue)):
        raise ValueError("Incremental revenue values must be finite.")

    # Zero-discount choices are represented by not selecting a variable.
    positive_columns = np.flatnonzero(discounts > 0)

    if n_customers == 0 or len(positive_columns) == 0 or budget == 0:
        return []

    discounts_positive = discounts[positive_columns]
    revenue_positive = revenue[:, positive_columns]

    # Net gain = modeled incremental revenue - discount cost.
    net_gain = revenue_positive - discounts_positive[None, :]

    # Only choices with positive net gain can improve the objective.
    eligible = net_gain > 0

    customer_indices, option_indices = np.where(eligible)

    if len(customer_indices) == 0:
        return []

    gains = net_gain[customer_indices, option_indices]
    costs = discounts_positive[option_indices]

    n_variables = len(gains)

    # Constraint 1: each customer can receive at most one discount.
    # Constraint 2: total discount spending cannot exceed budget.
    constraints = lil_matrix(
        (n_customers + 1, n_variables),
        dtype=float,
    )

    for variable, customer_index in enumerate(customer_indices):
        constraints[customer_index, variable] = 1.0

    constraints[n_customers, :] = costs

    upper_bounds = np.concatenate([
        np.ones(n_customers),
        np.array([budget]),
    ])

    constraint = LinearConstraint(
        constraints.tocsr(),
        lb=np.full(n_customers + 1, -np.inf),
        ub=upper_bounds,
    )

    result = milp(
        c=-gains,
        integrality=np.ones(n_variables),
        bounds=Bounds(
            lb=np.zeros(n_variables),
            ub=np.ones(n_variables),
        ),
        constraints=constraint,
        options={"time_limit": 120.0},
    )

    if result.x is None:
        raise RuntimeError(
            f"Optimization did not find a feasible allocation: {result.message}"
        )

    selected_variables = np.flatnonzero(result.x > 0.5)

    allocation = []

    for variable in selected_variables:
        customer_index = int(customer_indices[variable])
        option_index = int(option_indices[variable])

        discount = float(discounts_positive[option_index])
        incremental = float(
            revenue_positive[customer_index, option_index]
        )
        gain = float(net_gain[customer_index, option_index])

        allocation.append({
            "customer_index": customer_index,
            "discount": discount,
            "expected_incremental_revenue": incremental,
            "expected_net_gain": gain,
        })

    # Most profitable allocations first for display.
    allocation.sort(
        key=lambda item: item["expected_net_gain"],
        reverse=True,
    )

    total_spend = sum(item["discount"] for item in allocation)

    if total_spend > budget + 1e-6:
        raise RuntimeError("Optimizer returned an allocation over budget.")

    return allocation
