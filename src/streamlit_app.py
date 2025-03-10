import streamlit as st
import numpy as np
import pandas as pd
from dice_statistics import dice_statistics, parse_roll_expression

def main():
    st.title("Dice Statistics Comparison")

    # Dice selection
    st.sidebar.header("Dice Selection")
    num_dice = st.sidebar.number_input("Number of Dice", min_value=1, max_value=100, value=1)
    dice_type = st.sidebar.selectbox("Type of Dice", ['d4', 'd6', 'd8', 'd10', 'd12', 'd20'])
    modifier = st.sidebar.number_input("Modifier", min_value=-1000000, max_value=1000000, value=0)

    # Roll type selection
    st.sidebar.header("Roll Type")
    roll_type = st.sidebar.radio("Roll Type", ["Normal", "Advantage", "Disadvantage"])

    # Number of samples
    num_samples = st.sidebar.number_input("Number of Samples", min_value=100, max_value=1000000, value=10000)

    # Difficulty Class (DC)
    enable_dc = st.sidebar.checkbox("Enable DC")
    dc = None
    if enable_dc:
        dc = st.sidebar.number_input("Difficulty Class (DC)", min_value=1, max_value=1000, value=10)

    # Run simulation button
    if st.sidebar.button("Run Simulation"):
        roll_expression = f'{num_dice}{dice_type}'
        if modifier > 0:
            roll_expression += f'+{modifier}'
        elif modifier < 0:
            roll_expression += f'{modifier}'

        advantage = roll_type == "Advantage"
        disadvantage = roll_type == "Disadvantage"

        try:
            mean, var, min_value, max_value = dice_statistics(roll_expression, advantage=advantage, disadvantage=disadvantage)
            st.write(f"**{roll_expression}{' with Advantage' if advantage else ''}{' with Disadvantage' if disadvantage else ''}**")
            st.write(f"**Mean:** {mean}")
            st.write(f"**Variance:** {var}")
            st.write(f"**Min Value:** {min_value}")
            st.write(f"**Max Value:** {max_value}")

            # Generate rolls
            num_dice, num_sides, modifier = parse_roll_expression(roll_expression)
            if advantage:
                rolls = [max(np.random.randint(1, num_sides + 1), np.random.randint(1, num_sides + 1)) + modifier for _ in range(num_samples)]
            elif disadvantage:
                rolls = [min(np.random.randint(1, num_sides + 1), np.random.randint(1, num_sides + 1)) + modifier for _ in range(num_samples)]
            else:
                rolls = [sum(np.random.randint(1, num_sides + 1, num_dice)) + modifier for _ in range(num_samples)]

            # Probability of Success
            if dc is not None:
                success_probability = np.sum(np.array(rolls) >= dc) / len(rolls) * 100
                st.write(f"**Probability of Success (DC {dc}):** {success_probability:.2f}%")

            # Plot histogram
            st.subheader("Histogram")
            hist_values, hist_edges = np.histogram(rolls, bins=range(min(rolls), max(rolls) + 2))
            hist_df = pd.DataFrame({"Roll Result": hist_edges[:-1], "Frequency": hist_values})
            st.bar_chart(hist_df.set_index("Roll Result"))

            # Plot CDF
            st.subheader("Cumulative Distribution Function (CDF)")
            sorted_rolls = np.sort(rolls)
            cdf = np.arange(1, len(sorted_rolls) + 1) / len(sorted_rolls)
            cdf_df = pd.DataFrame({"Roll Result": sorted_rolls, "CDF": cdf})
            st.line_chart(cdf_df.set_index("Roll Result"))

        except ValueError as e:
            st.error(str(e))

if __name__ == "__main__":
    main()