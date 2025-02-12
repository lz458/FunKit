from datetime import datetime
import yfinance as yf
import streamlit as st
import matplotlib.pyplot as plt

in2024 = datetime(2024, 4, 2)
in2025 = datetime(2025, 4, 2)
in2026 = datetime(2026, 4, 2)
today = datetime.today()

sinceInvestment = today - in2024

notional = 20000
fixedRate = 0.06
profitSharingRatio = 0.0
interestForTheYear = notional * fixedRate
# AccruedInterest = interestForTheYear * (sinceInvestment.days / (in2025 - in2024).days)
ticker = "0P00000RGK.L"


def getHistoricalData(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    hist = stock.history(start=start_date, end=end_date)
    
    return hist



def calculateSharpeRatio(data):
    # Calculate the mean and standard deviation of daily returns
    mean_return = data['Total PnL'].mean()
    std_return = data['Total PnL'].std()
    
    # Annualize the mean return and standard deviation
    annualized_return = mean_return * 250
    annualized_std = std_return * (250 ** 0.5)
    
    # Assume risk-free rate is 0 for simplicity
    risk_free_rate = 0
    
    # Calculate Sharpe Ratio
    sharpe_ratio = (annualized_return - risk_free_rate) / annualized_std
    return sharpe_ratio

historicalData = getHistoricalData(ticker, in2024, today)


historicalData['Daily Return'] = historicalData['Close'].pct_change()
historicalData = historicalData.iloc[1:]
historicalData['Shared PnL'] = historicalData['Daily Return'] * profitSharingRatio
historicalData['Accured Interest'] = fixedRate / 250
historicalData['Cash Accured Interest'] = historicalData['Accured Interest'] * notional
historicalData['Cumulative Cash Accured Interest'] = historicalData['Cash Accured Interest'].cumsum()
historicalData['Total PnL'] = historicalData['Shared PnL'] + historicalData['Accured Interest']
historicalData['Cash PnL'] = historicalData['Total PnL'] * notional
historicalData['cumulative PnL'] = historicalData['Cash PnL'].cumsum()
AccruedInterest = historicalData['Cumulative Cash Accured Interest'].iloc[-1]
sharpe_ratio = calculateSharpeRatio(historicalData)

def check_password():
    def password_entered():
        if st.session_state["password"] == "123456":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("Password incorrect")
        return False
    else:
        return True

if check_password():

    st.write("### 2025 Trade Information")
    st.write(f"**Notional:** £{30000}")
    st.write(f"**Fixed Rate:** {fixedRate * 100}%")
    st.write(f"**Interest For The Year:** £{interestForTheYear:.2f}")
    st.write(f"**Profit Share:** {0.5 * 100:.2f}%")
    st.write(f"**Start Date:** {in2025.strftime('%Y-%m-%d')}")
    st.write(f"**Renewnal Date:** {in2026.strftime('%Y-%m-%d')}")
    st.write(f"**Linked fund:** {ticker}")

    st.write("---")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### 2024 Trade Information")
        st.write(f"**Notional:** £{notional}")
        st.write(f"**Fixed Rate:** {fixedRate * 100}%")
        st.write(f"**Interest For The Year:** £{interestForTheYear:.2f}")
        st.write(f"**Profit Share:** {profitSharingRatio * 100:.2f}%")
        st.write(f"**Start Date:** {in2024.strftime('%Y-%m-%d')}")
        st.write(f"**Renewnal Date:** {in2025.strftime('%Y-%m-%d')}")

    with col2:
        st.write("### PnL Information")
        st.write(f"**PnL Since Start Date:** £{historicalData['cumulative PnL'].iloc[-1]:.2f}")
        st.write(f"**Accrued Interest:** £{AccruedInterest:.2f}")
        st.write(f"**Profit Share:** £{historicalData['cumulative PnL'].iloc[-1] - AccruedInterest:.2f}")

        st.write("### Performance Information")

        # Calculate annualized return
        days_invested = (today - in2024).days
        annualized_return = (historicalData['cumulative PnL'].iloc[-1] / notional) * (365 / days_invested) * 100
        st.write(f"**Annualized Return:** {annualized_return:.2f}%")
        st.write(f"**Sharpe Ratio:** {sharpe_ratio:.2f}")

        voo_data = getHistoricalData("VOO", in2024, today)
        voo_data['Daily Return'] = voo_data['Close'].pct_change()
        voo_data['Total PnL'] = voo_data['Daily Return'] * profitSharingRatio
        voo_sharpe_ratio = calculateSharpeRatio(voo_data)
        # Calculate annualized return for VOO
        voo_annualized_return = voo_data['Daily Return'].mean() * 250
        st.write(f"**S&P Annualized Return:** {voo_annualized_return * 100:.2f}%")
        st.write(f"**S&P Sharpe Ratio:** {voo_sharpe_ratio:.2f}")


    # Plot cumulative PnL
    plt.figure(figsize=(10, 5))
    plt.plot(historicalData.index, historicalData['cumulative PnL'], label='Cumulative PnL', color='green')
    plt.xlabel('Date')
    plt.ylabel('Cumulative PnL')
    plt.title('Cumulative PnL Over Time')
    plt.legend()
    plt.grid(True)

    st.pyplot(plt)

    st.write(historicalData[['Close', 'Daily Return', 'Shared PnL', 'Accured Interest', 'Cash Accured Interest','Cumulative Cash Accured Interest','Total PnL', 'Cash PnL', 'cumulative PnL']])

    def plotHistoricalData(data):
        plt.figure(figsize=(10, 5))
        plt.plot(data.index, data['Close'], label='Close Price')
        plt.xlabel('Date')
        plt.ylabel('Close Price')
        plt.title('Historical Stock Data')
        plt.legend()
        plt.grid(True)
        voo_data = getHistoricalData("VOO", data.index[0], data.index[-1])
        # Normalize VOO's price to the same level as data['Close']
        voo_data['Normalized Close'] = voo_data['Close'] * (data['Close'].iloc[0] / voo_data['Close'].iloc[0])
        plt.plot(voo_data.index, voo_data['Normalized Close'], label='VOO Normalized Close Price')
        plt.legend()  # Ensure the legend is displayed
        return plt
    st.subheader("Historical Data")
    plot = plotHistoricalData(historicalData)
    st.pyplot(plot)