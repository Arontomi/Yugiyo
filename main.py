import streamlit as st
import requests
import matplotlib.pyplot as plt

def get_card_data(card_name):
    url = f"https://db.ygoprodeck.com/api/v7/cardinfo.php?name={card_name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "data" in data:
            return data["data"][0]  # Return first result
    return None

def plot_price_history(prices):
    if prices:
        sources = list(prices.keys())
        values = list(prices.values())

        plt.figure(figsize=(8, 4))
        plt.bar(sources, values, color='skyblue')
        plt.xlabel("Market")
        plt.ylabel("Price ($)")
        plt.title("Price Comparison Across Platforms")
        st.pyplot(plt)
    else:
        st.write("No price data available.")

def get_price_data(card_data):
    """ Extracts the latest price data from different platforms """
    if "card_prices" in card_data:
        price_info = card_data["card_prices"][0]
        return {
            "TCGPlayer": float(price_info.get("tcgplayer_price", 0)),
            "eBay": float(price_info.get("ebay_price", 0)),
            "Amazon": float(price_info.get("amazon_price", 0)),
            "CoolStuffInc": float(price_info.get("coolstuffinc_price", 0)),
        }
    return {}

def main():
    st.title("Yu-Gi-Oh! Card Tracker")
    card_name = st.text_input("Enter the card name:")

    if card_name:
        card_data = get_card_data(card_name)
        if card_data:
            st.image(card_data["card_images"][0]["image_url"], caption=card_name, width=250)
            
            prices = get_price_data(card_data)
            if prices:
                st.write(f"**Current Price (TCGPlayer):** ${prices.get('TCGPlayer', 'N/A')}")
                plot_price_history(prices)
            else:
                st.write("No price data available.")
        else:
            st.error("Card not found!")

if __name__ == "__main__":
    main()
