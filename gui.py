
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# API CONFIGURATION
API_URL = "link"

BG = "#080D14"
PANEL = "#111D29"

NEON_GREEN = "#39F5A3"
CYAN = "#39D9FF"
ORANGE = "#FFB84D"
PURPLE = "#D18BFF"

WHITE = "#FFFFFF"
GRAY = "#71869A"
GRID = "#263746"


root = tk.Tk()

root.title("SMART PLANT | IOT MONITORING SYSTEM")
root.geometry("1200x950")
root.configure(bg=BG)

header = tk.Frame(root, bg=BG)
header.pack(fill="x", padx=25, pady=20)

tk.Label(
    header,
    text=" SMART PLANT SYSTEM",
    font=("Arial", 24, "bold"),
    fg=WHITE,
    bg=BG
).pack(side="left")

system_status = tk.Label(
    header,
    text="● SYSTEM STARTING",
    font=("Arial", 12, "bold"),
    fg=ORANGE,
    bg=BG
)

system_status.pack(side="right")

tk.Label(
    root,
    text="IOT MONITORING DASHBOARD / LIVE SENSOR ANALYTICS",
    font=("Arial", 10),
    fg=GRAY,
    bg=BG
).pack(anchor="w", padx=28)

cards_frame = tk.Frame(root, bg=BG)
cards_frame.pack(fill="x", padx=20, pady=20)


def create_card(parent, title, color):

    card = tk.Frame(
        parent,
        bg=PANEL,
        highlightbackground=GRID,
        highlightthickness=1
    )

    card.pack(
        side="left",
        expand=True,
        fill="both",
        padx=7,
        ipady=15
    )

    tk.Label(
        card,
        text=title,
        font=("Arial", 10, "bold"),
        fg=color,
        bg=PANEL
    ).pack(pady=(12, 5))

    value = tk.Label(
        card,
        text="--",
        font=("Arial", 25, "bold"),
        fg=WHITE,
        bg=PANEL
    )

    value.pack(pady=5)

    condition = tk.Label(
        card,
        text="WAITING FOR DATA",
        font=("Arial", 9),
        fg=GRAY,
        bg=PANEL
    )

    condition.pack(pady=(0, 10))

    return value, condition


temp_value, temp_condition = create_card(
    cards_frame, "TEMPERATURE", NEON_GREEN
)

humid_value, humid_condition = create_card(
    cards_frame, "HUMIDITY", CYAN
)

soil_value, soil_condition = create_card(
    cards_frame, "SOIL MOISTURE", ORANGE
)

light_value, light_condition = create_card(
    cards_frame, "LIGHT SENSOR", PURPLE
)

chart_frame = tk.Frame(root, bg=BG)

chart_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)

fig, (ax1, ax2, ax3) = plt.subplots(
    3,
    1,
    figsize=(11, 7),
    dpi=90
)

fig.patch.set_facecolor(BG)

fig.subplots_adjust(
    left=0.10,
    right=0.97,
    top=0.95,
    bottom=0.08,
    hspace=0.65
)

canvas = FigureCanvasTkAgg(
    fig,
    master=chart_frame
)

canvas.get_tk_widget().pack(
    fill="both",
    expand=True
)


def style_chart(ax, title, color):

    ax.set_facecolor(PANEL)

    ax.set_title(
        title,
        color=color,
        fontsize=11,
        fontweight="bold",
        loc="left",
        pad=10
    )

    ax.tick_params(
        axis="both",
        colors=WHITE,
        labelcolor=WHITE,
        labelsize=9
    )

    ax.grid(
        color=GRID,
        linestyle="--",
        alpha=0.7
    )

    for spine in ax.spines.values():
        spine.set_color(GRID)


log_frame = tk.Frame(root, bg=PANEL)

log_frame.pack(
    fill="x",
    padx=27,
    pady=(5, 20)
)

tk.Label(
    log_frame,
    text="◈ SYSTEM ACTIVITY LOG",
    font=("Arial", 11, "bold"),
    fg=NEON_GREEN,
    bg=PANEL
).pack(
    anchor="w",
    padx=12,
    pady=8
)

text = tk.Text(
    log_frame,
    height=6,
    bg="#080D14",
    fg="#B8CBD9",
    font=("Consolas", 10),
    insertbackground=WHITE,
    relief="flat",
    bd=0
)

text.pack(
    fill="x",
    padx=12,
    pady=(0, 12)
)


def log(message):

    text.insert(tk.END, message + "\n")
    text.see(tk.END)



def fetch_data():

    try:

        response = requests.get(
            API_URL,
            timeout=5
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:

        print("[FETCH ERROR]", e)
        return []



def update_dashboard():

    data = fetch_data()

    if not isinstance(data, list) or not data:

        system_status.config(
            text="● NO DATA RECEIVED",
            fg=ORANGE
        )

        root.after(1000, update_dashboard)
        return

    try:

        latest = data[-1]

        x = list(range(len(data)))

        temp = [
            float(d["temperature"])
            for d in data
        ]

        hum = [
            float(d["humidity"])
            for d in data
        ]

        soil = [
            float(d["soil_moisture"])
            for d in data
        ]

        light = str(
            latest["light_status"]
        ).upper()


        # SENSOR VALUES

        temp_value.config(text=f"{temp[-1]:.1f}°C")
        humid_value.config(text=f"{hum[-1]:.1f}%")
        soil_value.config(text=f"{soil[-1]:.1f}%")

        light_value.config(
            text="DETECTED" if light == "MALIWANAG" else "DARK",
            font=("Arial", 18, "bold")
        )



        temp_condition.config(
            text="HIGH" if temp[-1] > 35 else "NORMAL",
            fg=ORANGE if temp[-1] > 35 else NEON_GREEN
        )

        humid_condition.config(
            text="LOW" if hum[-1] < 40 else "NORMAL",
            fg=ORANGE if hum[-1] < 40 else CYAN
        )

        soil_condition.config(
            text="DRY" if soil[-1] < 30 else "GOOD",
            fg=ORANGE if soil[-1] < 30 else NEON_GREEN
        )

        light_condition.config(
            text="LIGHT ACTIVE" if light == "LIGHT" else "NO LIGHT",
            fg=PURPLE
        )


        ax1.clear()

        style_chart(
            ax1,
            "TEMPERATURE HISTORY",
            NEON_GREEN
        )

        ax1.plot(
            x,
            temp,
            color=NEON_GREEN,
            linewidth=2.5,
            marker="o"
        )

        ax1.set_ylabel(
            "Temperature (°C)",
            color=WHITE
        )


        ax2.clear()

        style_chart(
            ax2,
            "HUMIDITY HISTORY",
            CYAN
        )

        ax2.fill_between(
            x,
            hum,
            color=CYAN,
            alpha=0.15
        )

        ax2.plot(
            x,
            hum,
            color=CYAN,
            linewidth=2.5
        )

        ax2.set_ylabel(
            "Humidity (%)",
            color=WHITE
        )


        ax3.clear()

        style_chart(
            ax3,
            "SOIL MOISTURE HISTORY",
            ORANGE
        )

        ax3.plot(
            x,
            soil,
            color=ORANGE,
            linewidth=2.5,
            marker="o"
        )

        ax3.set_ylabel(
            "Soil Moisture (%)",
            color=WHITE
        )

        ax3.set_xlabel(
            "SENSOR READINGS",
            color=WHITE
        )

        ax1.title.set_color(NEON_GREEN)
        ax2.title.set_color(CYAN)
        ax3.title.set_color(ORANGE)

        for ax in (ax1, ax2, ax3):

            ax.tick_params(
                axis="both",
                which="both",
                labelcolor=WHITE,
                colors=WHITE
            )

            for label in ax.get_xticklabels():
                label.set_color(WHITE)

            for label in ax.get_yticklabels():
                label.set_color(WHITE)

            ax.yaxis.label.set_color(WHITE)

        ax3.xaxis.label.set_color(WHITE)



        canvas.draw_idle()


        text.delete("1.0", tk.END)

        log("[ONLINE] Live sensor connection established")

        log(
            f"[TEMPERATURE] {temp[-1]}°C - "
            f"{'HIGH' if temp[-1] > 35 else 'NORMAL'}"
        )

        log(
            f"[HUMIDITY] {hum[-1]}% - "
            f"{'LOW' if hum[-1] < 40 else 'NORMAL'}"
        )

        log(
            f"[SOIL] {soil[-1]}% - "
            f"{'DRY' if soil[-1] < 30 else 'GOOD'}"
        )

        log(f"[LIGHT] {light}")



        system_status.config(
            text="● SYSTEM ONLINE",
            fg=NEON_GREEN
        )


    except (
        KeyError,
        ValueError,
        TypeError,
        IndexError
    ) as e:

        print("[DATA ERROR]", e)

        system_status.config(
            text="● INVALID SENSOR DATA",
            fg=ORANGE
        )


    root.after(1000, update_dashboard)


update_dashboard()

root.mainloop()
