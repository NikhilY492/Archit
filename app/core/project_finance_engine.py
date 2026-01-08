def compute_project_financials(
    snapshots,
    invoices
):
    total_value = sum(float(s.total) for s in snapshots)

    total_invoiced = sum(float(i.amount) for i in invoices)

    total_paid = sum(
        float(i.amount) for i in invoices
        if i.status == "paid"
    )

    outstanding = round(total_invoiced - total_paid, 2)

    milestone_status = {}
    for inv in invoices:
        milestone_status[inv.milestone] = inv.status

    return {
        "total_project_value": round(total_value, 2),
        "total_invoiced": round(total_invoiced, 2),
        "total_paid": round(total_paid, 2),
        "outstanding": outstanding,
        "milestones": milestone_status
    }
