from models.Portfolio import Portfolio
from views.Dashboard import Dashboard

if __name__ == "__main__":
    portfolio = Portfolio()
    app = Dashboard(portfolio)
    app.mainloop()